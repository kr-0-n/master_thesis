package scheduler

import (
	corev1 "k8s.io/api/core/v1"

	gograph"github.com/dominikbraun/graph"
	"k8_scheduler/common"
)

func Scheduler(graph gograph.Graph[string, *common.Node], pod corev1.Pod, debug bool, visualize bool) gograph.Graph[string, *common.Node] {
	return Random(graph, pod, debug, visualize)
}