package visualizer

import (
	"k8_scheduler/common"
	"os"
	"strconv"
	"time"

	gograph "github.com/dominikbraun/graph"
	"github.com/dominikbraun/graph/draw"
)

func DrawGraph(graph gograph.Graph[string, *common.Node]) {
	// fmt.Println("Drawing graph")
	file, _ := os.Create("./output/" + strconv.Itoa(int(time.Now().Unix())) + ".gv")
	_ = draw.DOT(graph, file,
		draw.GraphAttribute("layout", "fdp"),
		draw.GraphAttribute("splines", "line"),
		draw.GraphAttribute("K", "0.6"),
		draw.GraphAttribute("overlap", "false"),
	)
}
