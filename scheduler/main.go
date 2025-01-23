package main

import (
	"fmt"
	gograph"github.com/dominikbraun/graph"
	"scheduler/visualizer"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
)

func main() {
	graph := gograph.New(func(node *visualizer.Node) string {
		return node.Name
	})

	clientset := connectToK8s()
	node_watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "nodes", metav1.NamespaceAll, fields.Everything())
	_, node_controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: node_watchlist,
		ResyncPeriod:  0,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				node := obj.(*corev1.Node)
				graph.AddVertex(&visualizer.Node{Name: node.Name, Type: "node", Properties: map[string]string{}}, gograph.VertexAttribute("shape", "rect"), gograph.VertexAttribute("colorscheme", "blues3"), gograph.VertexAttribute("style", "filled"), gograph.VertexAttribute("color", "2"), gograph.VertexAttribute("fillcolor", "1"))

				fmt.Printf("Node added: %v\n", node.Name)
				verifyEdges(graph)

				visualizer.DrawGraph(graph)
			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				oldPod := oldObj.(*corev1.Pod)
				newPod := newObj.(*corev1.Pod)
				fmt.Printf("Pod updated: %v -> %v\n", oldPod.Name, newPod.Name)
			},
			DeleteFunc: func(obj interface{}) {
				pod := obj.(*corev1.Pod)
				fmt.Printf("Pod deleted: %v\n", pod.Name)
			},
		},
	})

	pod_watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "pods", metav1.NamespaceAll, fields.Everything())
	_, pod_controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: pod_watchlist,
		ResyncPeriod:  0,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				node := obj.(*corev1.Pod)
				new_vertex := &visualizer.Node{Name: node.Name, Type: "pod", Properties: map[string]string{"nodeName": node.Spec.NodeName}}
				graph.AddVertex(new_vertex, gograph.VertexAttribute("shape", "ellipse"), gograph.VertexAttribute("colorscheme", "greens3"), gograph.VertexAttribute("style", "filled"), gograph.VertexAttribute("color", "2"), gograph.VertexAttribute("fillcolor", "1"))
				fmt.Println("Pod added:", node.Name)
				verifyEdges(graph)

				visualizer.DrawGraph(graph)
			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				oldPod := oldObj.(*corev1.Pod)
				newPod := newObj.(*corev1.Pod)
				fmt.Printf("Pod updated: %v -> %v\n", oldPod.Name, newPod.Name)
			},
			DeleteFunc: func(obj interface{}) {
				pod := obj.(*corev1.Pod)
				fmt.Printf("Pod deleted: %v\n", pod.Name)
			},
		},
	})

	stop := make(chan struct{})
	defer close(stop)
	go node_controller.Run(stop)
	go pod_controller.Run(stop)
	select {}
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

func verifyEdges(graph gograph.Graph[string, *visualizer.Node]) {
	fmt.Println("Verifying edges")
	// Remove all Edges
	edges, _ := graph.Edges()
	fmt.Println(edges)
	for edge, _ := range edges {
		fmt.Println(edge)

	}

	adjacencyMap, _ := graph.AdjacencyMap()
	fmt.Println("Adjacency Map:", adjacencyMap)

	for vertex := range adjacencyMap {
		node, _ := graph.Vertex(vertex)
		if node.Type == "pod" {
			if node.Properties["nodeName"] != "" {
				adj_node, _ := graph.Vertex(node.Properties["nodeName"])
				graph.AddEdge(node.Name, adj_node.Name)

			}
		}
	}
}
