package algorithms

import (
	"k8_scheduler/common"
	"math/rand"

	gograph "github.com/dominikbraun/graph"
)

func Random(graph gograph.Graph[string, *common.Node], pod *common.Node, debug bool, visualize bool, candidates ...*common.Node) gograph.Graph[string, *common.Node] {
	graph.AddVertex(pod, common.VertexAttributes("pending_pod")...)

	var nodes []*common.Node
	if len(candidates) > 0 {
		nodes = candidates
	} else {
		adjacencyMap, _ := graph.AdjacencyMap()
		for vertex := range adjacencyMap {
			node, _ := graph.Vertex(vertex)
			if node.Type == "node" {
				nodes = append(nodes, node)
			}
		}
	}

	if len(nodes) == 0 {
		if debug {
			println("No available nodes to assign pod", pod.Name)
		}
		return graph
	}

	node := nodes[rand.Intn(len(nodes))]
	graph.AddEdge(pod.Name, node.Name, common.EdgeAttributes("assign", common.Link{})...)
	if debug {
		println("Assigned pod", pod.Name, "to node", node.Name)
	}

	return graph
}
