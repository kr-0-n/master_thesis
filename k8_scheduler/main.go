package main

import (
	"context"
	"encoding/json"
	"k8_scheduler/common"
	networkgraph "k8_scheduler/networkGraph"
	"k8_scheduler/scheduler"
	"k8_scheduler/scheduler/evaluator"
	"k8_scheduler/visualizer"
	"log"
	"os"
	"time"

	gograph "github.com/dominikbraun/graph"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "k8_scheduler/proto"

	k8 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
)

func main() {
	if len(os.Args) < 2 {
		println("The scheduler expects two arguments.")
		println("arg1: /path/to/kubeconfig")
		println("		This will be used to connect to the K8 cluster")
		println("arg2: /path/to/schedulerconfig")
		println("		This will be used to configure the scheduler. Find and example config.yaml file here: https://github.com/kr-0-n/master_thesis/blob/main/k8_scheduler/common/config.yaml")
		panic("Incorrect Arguments")
	}

	common.LoadConfig(os.Args[2])
	links := []common.Link{}

	ticker := time.NewTicker(10 * time.Second)
	quit := make(chan struct{})

	graph := gograph.New(func(node *common.Node) string {
		return node.Name
	}, gograph.Directed())

	clientset := connectToK8s()
	nodeWatchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "nodes", metav1.NamespaceAll, fields.Everything())
	_, nodeController := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: nodeWatchlist,
		ResyncPeriod:  10 * time.Second,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				node := obj.(*k8.Node)
				log.Println("Adding node", node.Name)
				if isNodeOnline(node, clientset) {
					graph.AddVertex(common.NodeToVertex(*node, "node"), common.VertexAttributes("node")...)
					log.Println("Node added: ", node.Status.Conditions[0].LastHeartbeatTime)
					verifyEdges(graph, links)
					visualizer.DrawGraph(graph)
				} else {
					graph.AddVertex(common.NodeToVertex(*node, "offline_node"), common.VertexAttributes("offline_node")...)
					log.Println("Node added: ", node.Status.Conditions[0].LastHeartbeatTime)
					evaluator.UnavailabilityMap[node.Name] = append(evaluator.UnavailabilityMap[node.Name], time.Now())
					verifyEdges(graph, links)
					visualizer.DrawGraph(graph)
				}
			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				oldNode := oldObj.(*k8.Node)
				newNode := newObj.(*k8.Node)
				// log.Println("Updating node: ", newNode.Name)

				if isNodeOnline(newNode, clientset) {
					common.RemoveVertex(graph, oldNode.Name)
					graph.AddVertex(common.NodeToVertex(*newNode, "node"), common.VertexAttributes("node")...)
					verifyEdges(graph, links)
					visualizer.DrawGraph(graph)
				} else {
					common.RemoveVertex(graph, oldNode.Name)
					graph.AddVertex(common.NodeToVertex(*newNode, "offline_node"), common.VertexAttributes("offline_node")...)
					evaluator.UnavailabilityMap[newNode.Name] = append(evaluator.UnavailabilityMap[newNode.Name], time.Now())
					verifyEdges(graph, links)
					visualizer.DrawGraph(graph)
				}
			},
			DeleteFunc: func(obj interface{}) {
				node := obj.(*k8.Node)
				common.RemoveVertex(graph, node.Name)
				verifyEdges(graph, links)
				visualizer.DrawGraph(graph)
				// fmt.Printf("Node deleted: %v\n", node.Name)
			},
		},
	})

	pod_watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "pods", "default", fields.Everything())
	_, pod_controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: pod_watchlist,
		ResyncPeriod:  10 * time.Second,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				// fmt.Println("Adding pod")
				pod := obj.(*k8.Pod)
				// println("Adding pod: ", pod.Name)
				// println("Phase: ", pod.Status.Phase)

				if pod.Spec.NodeName == "" {
					vertex, _ := graph.Vertex(pod.Name)
					if vertex == nil {
						graph := scheduler.SchedulePod(graph, *pod, false, false)
						realiseGraph(graph, clientset, links)
					}
				} else {
					podSeemsDead := false
					if len(pod.Status.Conditions) > 1 && pod.Status.Conditions[2].Status == "False" {
						podSeemsDead = true
					}
					if (pod.Status.Phase == "Failed" || pod.Status.Phase == "Succeeded" || pod.Status.Phase == "Unknown" || podSeemsDead) && !(pod.Status.Phase == "Pending") {
						log.Println("Deleting pod: ", pod.Name)
						clientset.CoreV1().Pods("default").Delete(context.TODO(), pod.Name, metav1.DeleteOptions{})
					} else if pod.Status.Phase == "Pending" || pod.Status.Phase == "Running" {
						// fmt.Printf("Conditions: %v\n", pod.Status.Conditions)
						graph.AddVertex(common.PodToVertex(*pod), common.VertexAttributes("pod")...)
						verifyEdges(graph, links)
						visualizer.DrawGraph(graph)
					}
				}
			},
			UpdateFunc: func(oldObj, newObj any) {
				oldPod := oldObj.(*k8.Pod)
				newPod := newObj.(*k8.Pod)

				networkgraph.UpdatePod(*oldPod, *newPod)

				verifyEdges(graph, links)
				visualizer.DrawGraph(graph)
			},
			DeleteFunc: func(obj interface{}) {
				pod := obj.(*k8.Pod)
				common.RemoveVertex(graph, pod.Name)
				realiseGraph(graph, clientset, links)
			},
		},
	})

	stop := make(chan struct{})
	defer close(stop)

	go func() {
		queryLinkAPI(&links)
		verifyEdges(graph, links)
		visualizer.DrawGraph(graph)
		for {
			select {
			case <-ticker.C:
				queryLinkAPI(&links)
				verifyEdges(graph, links)
				visualizer.DrawGraph(graph)
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()
	time.Sleep(5 * time.Second)
	go nodeController.Run(stop)
	time.Sleep(5 * time.Second)
	go pod_controller.Run(stop)

	select {}
}

func isNodeOnline(node *k8.Node, clientset *kubernetes.Clientset) bool {
	lease, err := clientset.
		CoordinationV1().
		Leases("kube-node-lease").
		Get(context.Background(), node.Name, metav1.GetOptions{})
	if err != nil {
		log.Println(err)
		return false
	}

	for _, condition := range node.Status.Conditions {
		if condition.Type == k8.NodeReady {
			log.Println("Found ", node.Name, "Online=", condition.Status)
			return condition.Status == k8.ConditionTrue
		}
	}

	// Fallback - should never be reached
	if lease.Spec.RenewTime.After(time.Now().Add(-15 * time.Second)) {
		return true
	} else {
		log.Println("Last Heartbeat for", node.Name, "at", node.Status.Conditions[0].LastHeartbeatTime)
		log.Println("Last Lease for", node.Name, "at", lease.Spec.RenewTime.String())
		return false
	}
}

func queryLinkAPI(links *[]common.Link) {
	conn, err := grpc.Dial("127.0.0.1:50051", grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithBlock())
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewLinkServiceClient(conn)

	// Perform RPC call
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*3)
	defer cancel()

	resp, err := client.GetAllLinks(ctx, &pb.EmptyMessage{})
	if err != nil {
		log.Printf("Error calling SendData: %v", err)
		return
	}

	if resp == nil {
		log.Fatalf("Received nil response")
	}

	tempLinks := []common.Link{}

	for _, link := range resp.Links {
		tempLinks = append(tempLinks, common.Link{Source: link.From, Target: link.To, Latency: int(link.Latency), Throughput: float64(link.Throughput), Timestamp: int(*link.Timestamp)})
	}

	*links = tempLinks
}

func connectToK8s() *kubernetes.Clientset {
	config, err := clientcmd.BuildConfigFromFlags("", os.Args[1])
	if err != nil {
		// Try to use in-cluster configuration if the kubeconfig is not available
		config, err = rest.InClusterConfig()
		if err != nil {
			panic(err.Error())
		}
	}
	// Create the clientset
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		panic(err.Error())
	}
	// fmt.Println("Successfully connected to the Kubernetes API")
	return clientset
}

func verifyEdges(graph gograph.Graph[string, *common.Node], links []common.Link) {
	// fmt.Println("Verifying edges")
	// // Print all links
	// fmt.Println("Links:")
	// for _, link := range links {
	// 	fmt.Printf("- %s -> %s with latency %d and throughput %d\n", link.Source, link.Target, link.Latency, link.Throughput)
	// }
	// Remove all Edges
	edges, _ := graph.Edges()
	// fmt.Println(edges)
	for _, edge := range edges {
		err := graph.RemoveEdge(edge.Source, edge.Target)
		if err != nil {
			log.Default().Println(err)
		}
	}

	for _, link := range links {
		srcVertex, _ := graph.Vertex(link.Source)
		trgtVertex, _ := graph.Vertex(link.Target)
		if srcVertex == nil || trgtVertex == nil {
			continue
		}

		if srcVertex.Type == "offline_node" || trgtVertex.Type == "offline_node" || time.Since(time.Unix(int64(link.Timestamp), 0)) > (time.Second*time.Duration(common.Cfg.Stability.LinkTimeout)) {
			graph.AddEdge(link.Source, link.Target, common.EdgeAttributes("offline_connection", link)...)
		} else {
			graph.AddEdge(link.Source, link.Target, common.EdgeAttributes("connection", link)...)
		}

	}

	adjacencyMap, _ := graph.AdjacencyMap()
	// fmt.Println("Adjacency Map:", adjacencyMap)

	for vertex := range adjacencyMap {
		// println(vertex)
		node, _ := graph.Vertex(vertex)
		if node.Type == "pod" {
			if node.Properties["nodeName"] != "" {
				adjNode, _ := graph.Vertex(node.Properties["nodeName"])
				if adjNode == nil {
					continue
				}
				if node.Properties["status"] == "Running" {
					graph.AddEdge(node.Name, adjNode.Name, common.EdgeAttributes("assign", common.Link{})...)
				} else {
					graph.AddEdge(node.Name, adjNode.Name, gograph.EdgeAttribute("style", "dotted"))
				}

			}

			if node.Properties["networkComRequirements"] != "" {
				comReqStr := node.Properties["networkComRequirements"]
				comReq := []common.NetworkComRequirement{}
				json.Unmarshal([]byte(comReqStr), &comReq)
				for _, req := range comReq {
					destinations := common.NodesWithPrefix(graph, req.Target)
					for _, destination := range destinations {
						graph.AddEdge(node.Name, destination, common.EdgeAttributes("networkComRequirement", common.Link{Source: node.Name, Target: destination, Latency: req.Latency, Throughput: req.Throughput})...)
					}
				}
			}
		}
	}
}

func realiseGraph(graph gograph.Graph[string, *common.Node], clientset *kubernetes.Clientset, links []common.Link) {
	// println("Realising graph")
	edges, _ := graph.Edges()
	for _, edge := range edges {
		if edge.Properties.Attributes["type"] == "assign" {
			// Is this pod already assigned to the right node?
			vertex, _ := graph.Vertex(edge.Source)
			// fmt.Printf("Pod %s with properties\n", edge.Source)
			// for key, value := range vertex.Properties {
			// 	// fmt.Printf("  %s: %s\n", key, value)
			// }
			if vertex.Properties["nodeName"] == edge.Target {
				// fmt.Println("Pod already assigned to node:", edge.Target)
				continue
			} else if vertex.Properties["nodeName"] == "" {
				// fmt.Println("Pod needs binding")
				// This pod is unscheduled, but assigned
				err := clientset.CoreV1().Pods("default").Bind(context.TODO(), &k8.Binding{
					ObjectMeta: metav1.ObjectMeta{
						Name:      edge.Source,
						Namespace: "default",
					},
					Target: k8.ObjectReference{
						Kind:      "Node",
						Name:      edge.Target,
						Namespace: "default",
					},
				}, metav1.CreateOptions{})
				if err != nil {
					// fmt.Println(err)
				} else {
					// fmt.Println("Pod assigned to node:", edge.Target)
				}

			} else {
				log.Println("INCONSISTENCE: Pod assigned to node:", edge.Target, "but pod is assigned to node:", vertex.Properties["nodeName"])
				continue
			}

		}
		verifyEdges(graph, links)
		visualizer.DrawGraph(graph)
	}
}
