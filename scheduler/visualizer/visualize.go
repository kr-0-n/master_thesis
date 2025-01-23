package visualizer

import (
	"fmt"
	"os"
	gograph"github.com/dominikbraun/graph"
	"github.com/dominikbraun/graph/draw"
)

type Node struct {
	Name       string
	Type       string
	Properties map[string]string
}

func DrawGraph(graph gograph.Graph[string, *Node]) {
	fmt.Println("Drawing graph")
	file, _ :=os.Create("./simple.gv")
	_ = draw.DOT(graph, file)
}

