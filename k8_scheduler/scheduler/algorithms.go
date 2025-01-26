package scheduler

import (
	corev1 "k8s.io/api/core/v1"

	gograph "github.com/dominikbraun/graph"
	"k8_scheduler/common"
	"math/rand"
)

func Random(graph gograph.Graph[string, *common.Node], pod corev1.Pod, debug bool, visualize bool) gograph.Graph[string, *common.Node] {
	new_vertex := common.PodToVertex(pod)
	graph.AddVertex(new_vertex, common.VertexAttributes("pod")...)

	adjacencyMap, _ := graph.AdjacencyMap()
	nodes := []*common.Node{}
	for vertex := range adjacencyMap {
		node, _ := graph.Vertex(vertex) 
		if node.Type == "node" {
			nodes = append(nodes, node)
		}
	}
	node := nodes[rand.Intn(len(nodes))]
	new_vertex.Properties["nodeName"] = node.Name
	graph.AddEdge(new_vertex.Name, node.Name, common.EdgeAttributes("assign", common.Link{})...)
	return graph
}
