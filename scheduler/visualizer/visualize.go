package visualizer

import (
	"fmt"
	"image/color"

	// "log"
	"math/rand"

	"github.com/hmdsefi/gograph"
	"gonum.org/v1/plot"

	// "gonum.org/v1/plot/font"
	// "gonum.org/v1/plot/font"
	"gonum.org/v1/plot/plotter"
	// "gonum.org/v1/plot/text"
	"gonum.org/v1/plot/vg"
	"gonum.org/v1/plot/vg/draw"
)

type Node struct {
	Name       string
	Type       string
	x          float64
	y          float64
	Properties map[string]string
}

func DrawGraph(graph gograph.Graph[*Node]) {
	fmt.Println("Drawing graph")

	p := plot.New()

	graph = findCoordinates(graph)
	plotNodes(graph, p)

	// for _, node := range graph.GetAllVertices() {
	// 	if node.Label().Type != "node" {
	// 		continue
	// 	}
	// 	nodeCoordinates[node.Label().Name] = [2]float64{rand.Float64() * 10, rand.Float64() * 10}
	// }

	// for _, edge := range graph.AllEdges() {
	// 	from := nodeCoordinates[edge.Source().Label().Name]
	// 	to := nodeCoordinates[edge.Destination().Label().Name]
	// 	line, _ := plotter.NewLine(plotter.XYs{{from[0], from[1]}, {to[0], to[1]}})
	// 	line.LineStyle.Color = color.RGBA{R: 0, G: 200, B: 0, A: 255}
	// 	p.Add(line)
	// }
	plotEdges(graph, p)

	p.Save(8*vg.Inch, 8*vg.Inch, "graph_plot.png")
}

func findCoordinates(graph gograph.Graph[*Node]) gograph.Graph[*Node] {
	for _, node := range graph.GetAllVertices() {
		node.Label().x = rand.Float64() * 10
		node.Label().y = rand.Float64() * 10
	}
	return graph
}

func plotNodes(graph gograph.Graph[*Node], p *plot.Plot) {
	labelOffset := 0.06
	for _, node := range graph.GetAllVertices() {
		if node.Label().Type == "node" {
			scatter, _ := plotter.NewScatter(plotter.XYs{{X: node.Label().x, Y: node.Label().y}})
			scatter.GlyphStyle.Shape = draw.BoxGlyph{}
			scatter.GlyphStyle.Radius = vg.Length(10)
			scatter.Color = color.RGBA{R: 138, G: 194, B: 255, A: 255}
			p.Add(scatter)
			label, _ := plotter.NewLabels(plotter.XYLabels{
				XYs: []plotter.XY{
					{X: node.Label().x-labelOffset, Y: node.Label().y-labelOffset},
				},
				Labels: []string{node.Label().Name},
			})
			p.Add(label)

		} else if node.Label().Type == "pod" {
			scatter, _ := plotter.NewScatter(plotter.XYs{{X: node.Label().x, Y: node.Label().y}})
			scatter.GlyphStyle.Shape = draw.CircleGlyph{}
			scatter.GlyphStyle.Radius = vg.Length(10)
			scatter.Color = color.RGBA{R: 110, G: 255, B: 129, A: 255}
			p.Add(scatter)
			label, _ := plotter.NewLabels(plotter.XYLabels{
				XYs: []plotter.XY{
					{X: node.Label().x-labelOffset, Y: node.Label().y-labelOffset},
				},
				Labels: []string{node.Label().Name},
			})
			p.Add(label)
		}
	}

}

func plotEdges(graph gograph.Graph[*Node], p *plot.Plot) {
	for _, edge := range graph.AllEdges() {
		from := edge.Source().Label()
		to := edge.Destination().Label()
		line, _ := plotter.NewLine(plotter.XYs{{from.x, from.y}, {to.x, to.y}})
		line.LineStyle.Color = color.RGBA{R: 0, G: 200, B: 0, A: 255}
		p.Add(line)
	}
}
