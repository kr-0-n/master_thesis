package common

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"

	corev1 "k8s.io/api/core/v1"

	gograph "github.com/dominikbraun/graph"
)

func PodToVertex(pod corev1.Pod) *Node {
	networkComString := ""
	if len(pod.Spec.Containers[0].Env) > 0 {
		for _, env := range pod.Spec.Containers[0].Env {
			if env.Name == "NetworkComRequirements" {
				networkComString = env.Value
			}
		}
	}
	json_node_selector, _ := json.Marshal(pod.Spec.NodeSelector)
	node_selector := string(json_node_selector)
	return &Node{Name: pod.Name, Type: "pod", Properties: map[string]string{"nodeName": pod.Spec.NodeName, "networkComRequirements": networkComString, "status": string(pod.Status.Phase), "cpu": strconv.FormatFloat(pod.Spec.Containers[0].Resources.Requests.Cpu().AsApproximateFloat64(), 'f', -1, 64), "mem": strconv.Itoa(int(pod.Spec.Containers[0].Resources.Requests.Memory().Value())), "nodeSelector": node_selector}}
}

func NodeToVertex(node corev1.Node, kind string) *Node {
	json_labels, _ := json.Marshal(node.Labels)
	labels := string(json_labels)
	return &Node{Name: node.Name, Type: kind, Properties: map[string]string{"cpu": strconv.Itoa(int(node.Status.Allocatable.Cpu().Value())), "memory": strconv.Itoa(int(node.Status.Allocatable.Memory().Value())), "labels": labels}}
}

func VertexAttributes(kind string) []func(*gograph.VertexProperties) {
	if kind == "pod" {
		return []func(*gograph.VertexProperties){
			gograph.VertexAttribute("shape", "ellipse"), gograph.VertexAttribute("colorscheme", "greens3"), gograph.VertexAttribute("style", "filled"), gograph.VertexAttribute("color", "2"), gograph.VertexAttribute("fillcolor", "1"),
		}
	} else if kind == "node" {
		return []func(*gograph.VertexProperties){
			gograph.VertexAttribute("shape", "rect"), gograph.VertexAttribute("colorscheme", "blues3"), gograph.VertexAttribute("style", "filled"), gograph.VertexAttribute("color", "2"), gograph.VertexAttribute("fillcolor", "1"),
		}
	} else if kind == "offline_node" {
		return []func(*gograph.VertexProperties){
			gograph.VertexAttribute("shape", "rect"), gograph.VertexAttribute("colorscheme", "reds3"), gograph.VertexAttribute("style", "filled"), gograph.VertexAttribute("color", "2"), gograph.VertexAttribute("fillcolor", "1"),
		}
	}
	return nil
}

func RemoveVertex(graph gograph.Graph[string, *Node], vertex string) gograph.Graph[string, *Node] {
	edges, _ := graph.Edges()
	for _, edge := range edges {
		if edge.Source == vertex || edge.Target == vertex {
			graph.RemoveEdge(edge.Source, edge.Target)
		}
	}
	graph.RemoveVertex(vertex)
	return graph
}

func EdgeAttributes(kind string, link Link) []func(*gograph.EdgeProperties) {
	if kind == "networkComRequirement" {
		return []func(*gograph.EdgeProperties){
			gograph.EdgeAttribute("type", "networkComRequirement"), gograph.EdgeAttribute("label", strconv.Itoa(link.Latency)+"ms "+fmt.Sprintf("%.2f", link.Throughput)+"mbps"), gograph.EdgeAttribute("color", "green"), gograph.EdgeAttribute("latency", strconv.Itoa(link.Latency)), gograph.EdgeAttribute("throughput", fmt.Sprintf("%.2f", link.Throughput)),
		}
	} else if kind == "connection" {
		return []func(*gograph.EdgeProperties){
			gograph.EdgeAttribute("type", "connection"), gograph.EdgeAttribute("throughput", fmt.Sprintf("%.2f", link.Throughput)), gograph.EdgeAttribute("latency", strconv.Itoa(link.Latency)), gograph.EdgeAttribute("label", strconv.Itoa(link.Latency)+"ms "+fmt.Sprintf("%.2f", link.Throughput)+"mbps"),
		}
	} else if kind == "offline_connection" {
		return []func(*gograph.EdgeProperties){
			gograph.EdgeAttribute("type", "offline_connection"), gograph.EdgeAttribute("throughput", fmt.Sprintf("%.2f", link.Throughput)), gograph.EdgeAttribute("latency", strconv.Itoa(link.Latency)), gograph.EdgeAttribute("label", strconv.Itoa(link.Latency)+"ms "+fmt.Sprintf("%.2f", link.Throughput)+"mbps"), gograph.EdgeAttribute("style", "dotted"),
		}
	} else if kind == "assign" {
		return []func(*gograph.EdgeProperties){
			gograph.EdgeAttribute("type", "assign"),
		}
	}
	return nil
}

func NodesWithPrefix(graph gograph.Graph[string, *Node], prefix string) []string {
	nodes := []string{}
	vertices, _ := graph.AdjacencyMap()
	for vertex := range vertices {
		node, _ := graph.Vertex(vertex)
		if strings.HasPrefix(node.Name, prefix) {
			nodes = append(nodes, node.Name)
		}
	}
	return nodes
}

// AssignedNode Returns the NodeName a Pod is assigned to in the Graph. Returns "" if not assigned
func AssignedNode(graph gograph.Graph[string, *Node], podName string) string {
	edges, _ := graph.Edges()
	for _, edge := range edges {
		if edge.Source == podName && edge.Properties.Attributes["type"] == "assign" {
			return edge.Target
		}
	}
	return ""
}

// AssignedPods Returns a list of pods which are assigned to a given node
func AssignedPods(graph gograph.Graph[string, *Node], nodeName string) []string {
	assignedPods := []string{}
	edges, _ := graph.Edges()
	for _, edge := range edges {
		if edge.Target == nodeName && edge.Properties.Attributes["type"] == "assign" {
			assignedPods = append(assignedPods, edge.Source)
		}
	}
	return assignedPods
}
