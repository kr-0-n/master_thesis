package scheduler

import (
	"k8_scheduler/common"
	"k8_scheduler/scheduler/algorithms"
	

	gograph "github.com/dominikbraun/graph"
	corev1 "k8s.io/api/core/v1"
)

func SchedulePod(graph gograph.Graph[string, *common.Node], pod corev1.Pod, debug bool, visualize bool) gograph.Graph[string, *common.Node] {
	graph_copy := graph
	return algorithms.EvolutionarySolve(graph_copy, common.PodToVertex(pod), false, visualize)
}