package visualizer

import (
	"os"
	"strconv"
	"time"

	"k8_scheduler/common"

	gograph "github.com/dominikbraun/graph"
	"github.com/dominikbraun/graph/draw"
)

func DrawGraph(graph gograph.Graph[string, *common.Node]) {
	// fmt.Println("Drawing graph")
	vertices, _ := graph.AdjacencyMap()
	for vertex := range vertices {
		node, _ := graph.Vertex(vertex)
		delete(node.Properties, "wanted_connection")
	}
	file, _ := os.Create("./output/" + strconv.Itoa(int(time.Now().Unix())) + ".gv")
	_ = draw.DOT(graph, file,
		draw.GraphAttribute("layout", "fdp"),
		draw.GraphAttribute("splines", "line"),
		draw.GraphAttribute("K", "0.6"),
		draw.GraphAttribute("overlap", "false"),
	)
}
