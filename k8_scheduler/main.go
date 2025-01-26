package main

import (
	"context"
	"encoding/json"
	"fmt"
	"k8_scheduler/common"
	"k8_scheduler/scheduler"
	"k8_scheduler/visualizer"
	"strings"

	gograph "github.com/dominikbraun/graph"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
)

func main() {
	graph := gograph.New(func(node *common.Node) string {
		return node.Name
	}, gograph.Directed())

	clientset := connectToK8s()
	node_watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "nodes", metav1.NamespaceAll, fields.Everything())
	_, node_controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: node_watchlist,
		ResyncPeriod:  0,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				fmt.Println("Adding node")
				node := obj.(*corev1.Node)
				graph.AddVertex(common.NodeToVertex(*node), common.VertexAttributes("node")...)
				fmt.Printf("Node added: %v\n", node.Name)
				verifyEdges(graph)
				visualizer.DrawGraph(graph)
			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				oldNode := oldObj.(*corev1.Node)
				newNode := newObj.(*corev1.Node)
				fmt.Printf("Node updated: %v -> %v\n", oldNode.Name, newNode.Name)
			},
			DeleteFunc: func(obj interface{}) {
				node := obj.(*corev1.Node)
				edges, _ := graph.Edges()
				for _, edge := range edges {
					if edge.Source == node.Name || edge.Target == node.Name {
						graph.RemoveEdge(edge.Source, edge.Target)
					}
				}
				graph.RemoveVertex(node.Name)
				verifyEdges(graph)
				visualizer.DrawGraph(graph)
				fmt.Printf("Node deleted: %v\n", node.Name)
			},
		},
	})

	pod_watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "pods", "default", fields.Everything())
	_, pod_controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: pod_watchlist,
		ResyncPeriod:  0,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				fmt.Println("Adding pod")
				pod := obj.(*corev1.Pod)
				if pod.Spec.NodeName == "" {
					scheduler.Scheduler(graph, *pod, false, false)
					realiseGraph(graph, clientset)

				} else {
					graph.AddVertex(common.PodToVertex(*pod), common.VertexAttributes("pod")...)
					fmt.Println("Pod added:", pod.Name)
					verifyEdges(graph)
					visualizer.DrawGraph(graph)
				}

			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				oldPod := oldObj.(*corev1.Pod)
				newPod := newObj.(*corev1.Pod)
				graph.RemoveVertex(oldPod.Name)
				graph.AddVertex(common.PodToVertex(*newPod), common.VertexAttributes("pod")...)
				fmt.Printf("Pod updated: %v -> %v\n", oldPod.Name, newPod.Name)
				verifyEdges(graph)
				visualizer.DrawGraph(graph)
			},
			DeleteFunc: func(obj interface{}) {
				pod := obj.(*corev1.Pod)
				edges, _ := graph.Edges()
				for _, edge := range edges {
					if edge.Source == pod.Name || edge.Target == pod.Name {
						graph.RemoveEdge(edge.Source, edge.Target)
					}
				}
				graph.RemoveVertex(pod.Name)
				fmt.Printf("Pod deleted: %v\n", pod.Name)
				verifyEdges(graph)
				visualizer.DrawGraph(graph)
			},
		},
	})

	stop := make(chan struct{})
	defer close(stop)
	go node_controller.Run(stop)
	go pod_controller.Run(stop)
	select {}
}

func queryLinkApi() []common.Link {
	return []common.Link{
		{Source: "k8-manager-0", Target: "k8-worker-0", Latency: 10, Throughput: 100},
		{Source: "k8-manager-0", Target: "k8-worker-1", Latency: 20, Throughput: 50},
		{Source: "k8-worker-0", Target: "k8-worker-1", Latency: 5, Throughput: 200},
	}
}

func connectToK8s() *kubernetes.Clientset {
	config, err := clientcmd.BuildConfigFromFlags("", "/home/kron/uni/master_thesis/k8_deployment/k3s.yaml/k8-manager-0/etc/rancher/k3s/k3s.yaml")
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
	fmt.Println("Successfully connected to the Kubernetes API")
	return clientset
}

func verifyEdges(graph gograph.Graph[string, *common.Node]) {
	fmt.Println("Verifying edges")
	links := queryLinkApi()
	// Remove all Edges
	edges, _ := graph.Edges()
	// fmt.Println(edges)
	for _, edge := range edges {
		graph.RemoveEdge(edge.Source, edge.Target)
	}

	for _, link := range links {
		graph.AddEdge(link.Source, link.Target, common.EdgeAttributes("connection", link)...)
	}

	adjacencyMap, _ := graph.AdjacencyMap()
	// fmt.Println("Adjacency Map:", adjacencyMap)

	for vertex := range adjacencyMap {
		node, _ := graph.Vertex(vertex)
		if node.Type == "pod" {
			if node.Properties["nodeName"] != "" {
				adj_node, _ := graph.Vertex(node.Properties["nodeName"])
				graph.AddEdge(node.Name, adj_node.Name)

			}

			if node.Properties["networkComRequirements"] != "" {
				com_req_str := node.Properties["networkComRequirements"]
				com_req := []common.NetworkComRequirement{}
				json.Unmarshal([]byte(com_req_str), &com_req)
				for _, req := range com_req {
					for target := range adjacencyMap {
						target_vertex, _ := graph.Vertex(target)
						if strings.HasPrefix(target_vertex.Name, req.Target) {
							graph.AddEdge(node.Name, target_vertex.Name, common.EdgeAttributes("networkComRequirement", common.Link{Source: node.Name, Target: target_vertex.Name, Latency: req.Latency, Throughput: req.Throughput})...)
						}
					}
				}
			}
		}
	}
}

func realiseGraph(graph gograph.Graph[string, *common.Node], clientset *kubernetes.Clientset) {
	fmt.Println("Realising graph")
	edges, _ := graph.Edges()
	for _, edge := range edges {
		if edge.Properties.Attributes["type"] == "assign" {
			// Is this pod already assigned to the right node?
			vertex, _ := graph.Vertex(edge.Source)
			if vertex.Properties["nodeName"] == edge.Target {
				fmt.Println("Pod already assigned to node:", edge.Target)
				continue
			} else if vertex.Properties["nodeName"] == "" {
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
					fmt.Println(err)
				} else {
					fmt.Println("Pod assigned to node:", edge.Target)

				}

			}

		}
		verifyEdges(graph)
		visualizer.DrawGraph(graph)
	}

}
