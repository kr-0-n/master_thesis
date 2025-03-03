package algorithms

import (
	gograph "github.com/dominikbraun/graph"
	"k8_scheduler/common"
	"math/rand"
)

func Random(graph gograph.Graph[string, *common.Node], pod *common.Node, debug bool, visualize bool) gograph.Graph[string, *common.Node] {
	graph.AddVertex(pod, common.VertexAttributes("pod")...)

	adjacencyMap, _ := graph.AdjacencyMap()
	nodes := []*common.Node{}
	for vertex := range adjacencyMap {
		node, _ := graph.Vertex(vertex)
		if node.Type == "node" {
			nodes = append(nodes, node)
		}
	}
	node := nodes[rand.Intn(len(nodes))]
	// new_vertex.Properties["nodeName"] = node.Name
	graph.AddEdge(pod.Name, node.Name, common.EdgeAttributes("assign", common.Link{})...)
	if debug {
		println("Assigned pod", pod.Name, "to node", node.Name)
	}
	return graph
}
