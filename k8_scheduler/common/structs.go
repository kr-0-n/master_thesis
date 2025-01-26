package common

type Node struct {
	Name       string
	Type       string
	Properties map[string]string
}

type Link struct {
	Source     string
	Target     string
	Latency    int
	Throughput int
}

type NetworkComRequirement struct {
	Target     string
	Latency    int
	Throughput int
}