package main

import (
	"scheduler/visualizer"
	"github.com/hmdsefi/gograph"

	// "context"
	"fmt"

	corev1 "k8s.io/api/core/v1"
	// policyv1 "k8s.io/api/policy/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
)

func main() {
	graph := gograph.New[*visualizer.Node](gograph.Directed())
	// graph.AddEdge(gograph.NewVertex(&visualizer.Node{Name: "A", Type: "node", Properties: map[string]string{"property1": "value1", "property2": "value2"}}), gograph.NewVertex(&visualizer.Node{Name: "B", Type: "node", Properties: map[string]string{"property1": "value1", "property2": "value2"}}))

	clientset := connectToK8s()
	node_watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "nodes", metav1.NamespaceAll, fields.Everything())
	_, node_controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: node_watchlist,
		ResyncPeriod:  0,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				node := obj.(*corev1.Node)
				graph.AddVertex(gograph.NewVertex(&visualizer.Node{Name: node.Name, Type: "node", Properties: map[string]string{}}))

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
				graph.AddVertex(gograph.NewVertex(new_vertex))
				fmt.Println("Pod added:", node.Name)
				for _, adj_node := range graph.GetAllVertices() {
					if adj_node.Label().Name == node.Spec.NodeName {
						edge, err :=graph.AddEdge(adj_node, graph.GetVertexByID(new_vertex))
					if err != nil {
						fmt.Println(err)
					}
					fmt.Println(edge)
					}
				}
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

func verifyEdges(graph gograph.Graph[*visualizer.Node]) {
	// Remove all Edges
	for _, edge := range graph.AllEdges() {
		graph.RemoveEdges(edge)
	}

	for _, node := range graph.GetAllVertices() {
		if node.Label().Type == "pod" {
			if node.Label().Properties["nodeName"] != "" {
				for _, adj_node := range graph.GetAllVertices() {
					if adj_node.Label().Name == node.Label().Properties["nodeName"] {
						graph.AddEdge(node, adj_node)

					}
				}
			}
		}
	}
}

