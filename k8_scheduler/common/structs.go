// Package common provides code which can be used in every module of the app
package common

import k8 "k8s.io/api/core/v1"

type Node struct {
	Name       string
	Type       string
	Properties map[string]string
}

type Link struct {
	Source     string
	Target     string
	Latency    int
	Throughput float64
	Timestamp  int
}

type NetworkComRequirement struct {
	Target     string
	Latency    int
	Throughput float64
}

type PendingAssignment struct {
	Timestamp  int
	Assignment Assignment
}
type Assignment struct {
	Source string
	Target string
}

type K8Knowledge struct {
	Pods  []k8.Pod
	Nodes []k8.Node
}
