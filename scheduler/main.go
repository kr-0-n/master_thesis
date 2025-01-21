package main

import (
	"context"
	"fmt"

	corev1 "k8s.io/api/core/v1"
	policyv1 "k8s.io/api/policy/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
)

func main() {
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

	// Additional scheduler logic will go here
	// Watch for unscheduled pods
	watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "pods", "default", fields.AndSelectors(fields.OneTermEqualSelector("spec.schedulerName", "custom-scheduler")))
	_, controller := cache.NewInformerWithOptions(cache.InformerOptions{
		ListerWatcher: watchlist,
		ResyncPeriod:  0,
		Handler: cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				pod := obj.(*corev1.Pod)
				fmt.Printf("Pod added: %v\n", pod.Name)

				if pod.Spec.NodeName == "" {
					fmt.Println("Pod seems to be unscheduled")
					clientset.CoreV1().Pods(pod.Namespace).Bind(context.TODO(), &corev1.Binding{
						ObjectMeta: metav1.ObjectMeta{
							Name:      pod.Name,
							Namespace: pod.Namespace,
						},
						Target: corev1.ObjectReference{
							Kind:      "Node",
							Name:      "k8-worker-0",
							Namespace: pod.Namespace,
						},
					}, metav1.CreateOptions{})
				} else {
					fmt.Println("Pod %v -> %v", pod.Name, pod.Spec.NodeName)
				}

				if pod.Spec.NodeName == "k8-worker-0" {
					evictionError := clientset.CoreV1().Pods(pod.Namespace).EvictV1(context.TODO(), &policyv1.Eviction{
						ObjectMeta: pod.ObjectMeta,
					})

					if evictionError != nil {
						fmt.Println("Eviction error")
					}

					err := clientset.CoreV1().Pods(pod.Namespace).Bind(context.TODO(), &corev1.Binding{
						ObjectMeta: metav1.ObjectMeta{
							Name:      pod.Name,
							Namespace: pod.Namespace,
						},
						Target: corev1.ObjectReference{
							Kind:      "Node",
							Name:      "k8-worker-1",
							Namespace: pod.Namespace,
						},
					}, metav1.CreateOptions{})
					if err != nil {
						fmt.Printf("Error updating pod: %v\n", err)
					} else {
						fmt.Printf("Pod updated\n")
					}
				}
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
	go controller.Run(stop)
	// Keep the main thread running
	select {}

}
