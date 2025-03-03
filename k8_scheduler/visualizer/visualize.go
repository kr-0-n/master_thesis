package visualizer

import (
	"os"
	gograph"github.com/dominikbraun/graph"
	"github.com/dominikbraun/graph/draw"
	"k8_scheduler/common"
)



func DrawGraph(graph gograph.Graph[string, *common.Node]) {
	// fmt.Println("Drawing graph")
	file, _ :=os.Create("./output/simple.gv")
	_ = draw.DOT(graph, file)
}

