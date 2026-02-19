package main

import (
	"context"
	"k8_scheduler/common"
	networkgraph "k8_scheduler/networkGraph"
	"k8_scheduler/scheduler"
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
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
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

	ticker := time.NewTicker(10 * time.Second)
	quit := make(chan struct{})

	clientset := connectToK8s()

	stop := make(chan struct{})
	defer close(stop)

	go func() {
		for {
			select {
			case <-ticker.C:
				log.Println("==================================================")
				k8knowledge := queryK8API(*clientset)
				networkgraph.SetK8Knowledge(k8knowledge)

				for _, node := range k8knowledge.Nodes {
					log.Printf("Found Node: %s, Online %t\n", node.Name, common.IsNodeOnline(&node))
				}

				networkgraph.SetNetworkKnowledge(queryLinkAPI())
				unscheduledPods := []k8.Pod{}
				for _, pod := range k8knowledge.Pods {
					log.Printf("Found Pod: %s, Status: %s, NodeName: %s", pod.Name, pod.Status.Phase, pod.Spec.NodeName)
					if pod.Status.Phase == "Pending" && pod.Spec.NodeName == "" {
						unscheduledPods = append(unscheduledPods, pod)
					}
				}
				currentGraph := networkgraph.GetGraph()
				if len(unscheduledPods) > 0 {
					newGraph := scheduler.SchedulePods(currentGraph, unscheduledPods, false, false)
					visualizer.DrawGraph(newGraph)
					realiseGraph(newGraph, clientset)
				}

			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()
	time.Sleep(10 * time.Second)
	select {}
}

func queryK8API(clientset kubernetes.Clientset) common.K8Knowledge {
	podList, err := clientset.CoreV1().Pods(metav1.NamespaceDefault).List(context.Background(), metav1.ListOptions{})
	if err != nil {
		log.Println("Error interacting with K8")
	}
	pods := podList.Items

	nodeList, err := clientset.CoreV1().Nodes().List(context.Background(), metav1.ListOptions{})
	if err != nil {
		log.Println("Error interacting with K8")
	}
	nodes := nodeList.Items
	return common.K8Knowledge{Pods: pods, Nodes: nodes}
}

func queryLinkAPI() []common.Link {
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
		return []common.Link{}
	}

	if resp == nil {
		log.Fatalf("Received nil response")
	}

	tempLinks := []common.Link{}

	for _, link := range resp.Links {
		tempLinks = append(tempLinks, common.Link{Source: link.From, Target: link.To, Latency: int(link.Latency), Throughput: float64(link.Throughput), Timestamp: int(*link.Timestamp)})
	}

	return tempLinks
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

func realiseGraph(graph gograph.Graph[string, *common.Node], clientset *kubernetes.Clientset) {
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
					log.Println(err)
				} else {
					log.Printf("Pod %s assigned to node %s\n", edge.Source, edge.Target)
				}

			} else {
				log.Println("INCONSISTENCE: Pod assigned to node:", edge.Target, "but pod is assigned to node:", vertex.Properties["nodeName"])
				continue
			}

		}
		// visualizer.DrawGraph(graph)
	}
}
