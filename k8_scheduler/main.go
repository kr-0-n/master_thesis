package main

import (
	"context"
	"encoding/json"
	"fmt"
	"k8_scheduler/common"
	"k8_scheduler/scheduler"
	"k8_scheduler/visualizer"
	"k8_scheduler/scheduler/evaluator"
	"log"
	"time"

	gograph "github.com/dominikbraun/graph"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "k8_scheduler/proto"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
)


func main() {
	common.LoadConfig("~/k3s.yaml")
	links := []common.Link{}

	ticker := time.NewTicker(10 * time.Second)
	quit := make(chan struct{})

	graph := gograph.New(func(node *common.Node) string {
		return node.Name
	}, gograph.Directed())

	clientset := connectToK8s()
	node_watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "nodes", metav1.NamespaceAll, fields.Everything())
	_, node_controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: node_watchlist,
		ResyncPeriod:  10 * time.Second,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				// fmt.Println("Adding node")
				node := obj.(*corev1.Node)
				// println("Adding node: ", node.Name)
				// println("Last Heartbeat Time: ", node.Status.Conditions[0].LastHeartbeatTime.Time.String())
				// println("Status: ", node.Status.Conditions[0].Status)
				if node.Status.Conditions[0].LastHeartbeatTime.After(time.Now().Add(-5*time.Minute)) && node.Status.Conditions[0].Status != "Unknown" {
					graph.AddVertex(common.NodeToVertex(*node, "node"), common.VertexAttributes("node")...)
					// fmt.Printf("Node added: %v\n", node.Status.Conditions[0].LastHeartbeatTime)
					verifyEdges(graph, links)
					visualizer.DrawGraph(graph)
				} else {
					graph.AddVertex(common.NodeToVertex(*node, "offline_node"), common.VertexAttributes("offline_node")...)
					// fmt.Printf("Node added: %v\n", node.Status.Conditions[0].LastHeartbeatTime)
					evaluator.UnavailabilityMap[node.Name] = append(evaluator.UnavailabilityMap[node.Name], time.Now())
					verifyEdges(graph, links)
					visualizer.DrawGraph(graph)
				}

			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				oldNode := oldObj.(*corev1.Node)
				newNode := newObj.(*corev1.Node)
				// println("Updating node: ", newNode.Name)
				// println("Last Heartbeat Time: ", newNode.Status.Conditions[0].LastHeartbeatTime.Time.String())
				// println("Status: ", newNode.Status.Conditions[0].Status)
				if newNode.Status.Conditions[0].LastHeartbeatTime.Time.After(time.Now().Add(-5*time.Minute)) && newNode.Status.Conditions[0].Status != "Unknown" {
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
				node := obj.(*corev1.Node)
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
				pod := obj.(*corev1.Pod)
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
						print("Deleting pod: ", pod.Name)
						clientset.CoreV1().Pods("default").Delete(context.TODO(), pod.Name, metav1.DeleteOptions{})
					} else if pod.Status.Phase == "Pending" || pod.Status.Phase == "Running" {
						// fmt.Printf("Conditions: %v\n", pod.Status.Conditions)
						graph.AddVertex(common.PodToVertex(*pod), common.VertexAttributes("pod")...)
						verifyEdges(graph, links)
						visualizer.DrawGraph(graph)
					}
				}

			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				oldPod := oldObj.(*corev1.Pod)
				newPod := newObj.(*corev1.Pod)
				podSeemsDead := false
				if len(newPod.Status.Conditions) > 1 && newPod.Status.Conditions[2].Status == "False" {
					podSeemsDead = true
				}
				if (newPod.Status.Phase == "Failed" || newPod.Status.Phase == "Succeeded" || newPod.Status.Phase == "Unknown" || podSeemsDead) && !(newPod.Status.Phase == "Pending") {
					common.RemoveVertex(graph, oldPod.Name)
					clientset.CoreV1().Pods("default").Delete(context.TODO(), oldPod.Name, metav1.DeleteOptions{})
				} else if newPod.Status.Phase == "Pending" || newPod.Status.Phase == "Running" {
					common.RemoveVertex(graph, oldPod.Name)
					graph.AddVertex(common.PodToVertex(*newPod), common.VertexAttributes("pod")...)
				}

				verifyEdges(graph, links)
				visualizer.DrawGraph(graph)
			},
			DeleteFunc: func(obj interface{}) {
				pod := obj.(*corev1.Pod)
				common.RemoveVertex(graph, pod.Name)
				fmt.Printf("Pod deleted: %v\n", pod.Name)
				realiseGraph(graph, clientset, links)
			},
		},
	})

	stop := make(chan struct{})
	defer close(stop)

	go func() {
		queryLinkApi(&links)
		verifyEdges(graph, links)
		visualizer.DrawGraph(graph)
		for {
			select {
			case <-ticker.C:
				queryLinkApi(&links)
				verifyEdges(graph, links)
				visualizer.DrawGraph(graph)
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()
	time.Sleep(5 * time.Second)
	go node_controller.Run(stop)
	time.Sleep(5 * time.Second)
	go pod_controller.Run(stop)

	select {}
}

func queryLinkApi(links *[]common.Link) {
	conn, err := grpc.NewClient("127.0.0.1:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewLinkServiceClient(conn)

	// Perform RPC call
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	resp, err := client.GetAllLinks(ctx, &pb.EmptyMessage{})

	if err != nil {
		log.Fatalf("Error calling SendData: %v", err)
	}

	if resp == nil {
		log.Fatalf("Received nil response")
	}

	temp_links := []common.Link{}

	for _, link := range resp.Links {
		temp_links = append(temp_links, common.Link{Source: link.From, Target: link.To, Latency: int(link.Latency), Throughput: int(link.Throughput)})
	}
	// print(resp.Links)

	*links = temp_links
}

func connectToK8s() *kubernetes.Clientset {
	config, err := clientcmd.BuildConfigFromFlags("", "/home/kron/uni/master_thesis/k8_deployment/playbooks/kubeconfig.yml")
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
		graph.RemoveEdge(edge.Source, edge.Target)
	}

	for _, link := range links {
		src_vertex, _ := graph.Vertex(link.Source)
		trgt_vertex, _ := graph.Vertex(link.Target)
		if src_vertex == nil || trgt_vertex == nil {
			continue
		}

		if src_vertex.Type == "offline_node" || trgt_vertex.Type == "offline_node" {
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
				adj_node, _ := graph.Vertex(node.Properties["nodeName"])
				if adj_node == nil {
					continue
				}
				if node.Properties["status"] == "Running" {
					graph.AddEdge(node.Name, adj_node.Name, common.EdgeAttributes("assign", common.Link{})...)
				} else {
					graph.AddEdge(node.Name, adj_node.Name, gograph.EdgeAttribute("style", "dotted"))
				}

			}

			if node.Properties["networkComRequirements"] != "" {
				com_req_str := node.Properties["networkComRequirements"]
				com_req := []common.NetworkComRequirement{}
				json.Unmarshal([]byte(com_req_str), &com_req)
				for _, req := range com_req {
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
				err := clientset.CoreV1().Pods("default").Bind(context.TODO(), &corev1.Binding{
					ObjectMeta: metav1.ObjectMeta{
						Name:      edge.Source,
						Namespace: "default",
					},
					Target: corev1.ObjectReference{
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
				fmt.Println("INCONSISTENCE: Pod assigned to node:", edge.Target, "but pod is assigned to node:", vertex.Properties["nodeName"])
				continue
			}

		}
		verifyEdges(graph, links)
		visualizer.DrawGraph(graph)
	}

}
