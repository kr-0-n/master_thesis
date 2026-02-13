// Package networkgraph contains the offline integrated networkgraph representation
package networkgraph

import (
	"errors"
	"k8_scheduler/common"
	"time"

	k8 "k8s.io/api/core/v1"

	gograph "github.com/dominikbraun/graph"
)

var networkKnowledge []common.Link

//
// K8Knowledge

// The graph which represents the current networkgraph
var graph gograph.Graph[string, *common.Node] = gograph.New(func(node *common.Node) string {
	return node.Name
}, gograph.Directed())

// AddPod adds a Kubernetes Pod to the networkgraph
// If the pod exists already, the function will throw an error
// Only add Pods which are pending or running
// Returns true if the operation was successful
func AddPod(pod k8.Pod) (bool, error) {
	// Check if there is already a pod with the same name
	existingPod, err := graph.Vertex(pod.Name)
	if err != nil {
		panic(err)
	} else if existingPod != nil {
		return false, errors.New("pod exists")
	}
	if pod.Status.Phase == "Running" || pod.Status.Phase == "Pending" {
		err := graph.AddVertex(common.PodToVertex(pod), common.VertexAttributes("pod")...)
		if err != nil {
			panic(err)
		}
		return true, nil
	} else {
		return false, nil
	}
}

// UpdatePod updates the pod by removing the old pod and adding a new one. It reapplies the edges after adding the new one
func UpdatePod(oldPod k8.Pod, newPod k8.Pod) {
	common.RemoveVertex(graph, oldPod.Name)
	AddPod(newPod)
	// TODO: Add old edges. Look them up in the k8 K8Knowledge
}

func DeletePod(pod k8.Pod) {
	common.RemoveVertex(graph, pod.Name)
}

func SetNetworkKnowledge(links []common.Link) {
	networkKnowledge = links
	applyNetworkKnowledge()
}

func applyNetworkKnowledge() {
	edges, _ := graph.Edges()

	for _, edge := range edges {
		if edge.Properties.Attributes["type"] != "connection" {
			continue
		}
		err := graph.RemoveEdge(edge.Source, edge.Target)
		if err != nil {
			panic(err)
		}
	}

	for _, link := range networkKnowledge {
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
}
