package algorithms

import (
	"math/rand"
	"sort"

	"k8_scheduler/common"
	"k8_scheduler/scheduler/evaluator"

	gograph "github.com/dominikbraun/graph"
)

type Solution struct {
	graph gograph.Graph[string, *common.Node]
	value float64
}

func EvolutionarySolve(graph gograph.Graph[string, *common.Node], pod *common.Node, debug bool, visualize bool) gograph.Graph[string, *common.Node] {
	generations := 10
	children_per_parent := 5
	survivors_per_generation := 5

	initial_unassigned := graph

	first_solution := initial_unassigned

	first_solution = Random(first_solution, pod, false, false)

	initial_best := Solution{first_solution, evaluator.EvaluateStep(initial_unassigned, first_solution, false)}
	if debug {
		println("Initial Best: ", initial_best.value)
	}
	current_best := initial_best

	// These are the initial survivors
	survivors := make([]Solution, survivors_per_generation)
	for i := 0; i < survivors_per_generation; i++ {
		solution := Random(initial_unassigned, pod, false, false)
		survivors[i] = Solution{solution, evaluator.EvaluateStep(initial_unassigned, solution, false)}
		if survivors[i].value < current_best.value {
			current_best = survivors[i]
		}
	}

	for i := 0; i < generations; i++ {
		if debug {
			println("Generation: ", i)
		}
		if current_best.value < 0.1 {
			return current_best.graph
		}
		children := []Solution{}
		for j := 0; j < len(survivors); j++ {
			if debug {
				println("Parent: ", j)
			}

			for k := 0; k < children_per_parent; k++ {
				if debug {
					println("Solution: ", k)
				}

				child := survivors[j].graph

				// Choose a random pod for the mutation
				pods := []*common.Node{}
				adjacencyMap, _ := child.AdjacencyMap()

				for vertex := range adjacencyMap {
					node, _ := child.Vertex(vertex)
					if node.Type == "pod" {
						pods = append(pods, node)
					}
				}
				chosenPod := pods[rand.Intn(len(pods))]

				if debug {
					println("Reassign Pod: ", chosenPod.Name)
				}

				// Remove the pod from the graph
				edges, _ := child.Edges()
				for _, edge := range edges {
					if edge.Source == chosenPod.Name || edge.Target == chosenPod.Name {
						child.RemoveEdge(edge.Source, edge.Target)
					}
				}
				child.RemoveVertex(chosenPod.Name)

				child = Random(child, chosenPod, false, false)

				value := evaluator.EvaluateStep(initial_unassigned, child, false)
				if value < 0.1 {
					if debug {
						println("Found a perfect solution")
					}
					return child
				}
				children = append(children, Solution{child, value})
			}
		}
		sort.Slice(children, func(i, j int) bool {
			return children[i].value < children[j].value
		})

		if debug {
			println("we have", len(children), "children")
		}
		survivors = children[:survivors_per_generation]
		if debug {
			for i, child := range children {
				println("Child #", i, " value: ", child.value)
			}
		}

		if survivors[0].value < current_best.value {
			current_best = survivors[0]
		}
	}
	println("Best value: ", current_best.value)
	return current_best.graph
}
