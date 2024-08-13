import math
import networkx as nx

def evaluate(graph, debug=False):
    # Remove all wanted connections (they are unwanted)
    graph.remove_edges_from((edge for edge in graph.edges if graph.edges[edge]["type"] == "wanted_connection"))
    
    print("-"*50)
    val = 0
    # See if nodes are overloaded
    for node in graph.nodes:
        if graph.nodes[node]["type"] == "node":
            cpu_load = 0
            mem_load = 0
            for neighbour in graph.neighbors(node):
                if graph.nodes[neighbour]["type"] == "pod":
                    cpu_load += graph.nodes[neighbour]["cpu"]
                    mem_load += graph.nodes[neighbour]["mem"]
            if cpu_load - graph.nodes[node]["cpu"] > 0:
                val += cpu_load - graph.nodes[node]["cpu"]
            if mem_load - graph.nodes[node]["mem"] > 0:
                val += mem_load - graph.nodes[node]["mem"]
            print(f"node {node}: cpu {cpu_load}/{graph.nodes[node]['cpu']} | mem {mem_load}/{graph.nodes[node]['mem']}")
    # See if pod network requirements are fullfilled
    # Start with latency
    for pod in graph.nodes:
        if graph.nodes[pod]["type"] == "pod":
            for connection in graph.nodes[pod]["network"]:
                # find starting node pod
                adjacent_nodes = list(graph.neighbors(pod))
                if(len(adjacent_nodes) == 0):
                    val += 1000
                    if debug:
                        print(f"Pod {pod} has not been scheduled!")
                    continue
                start = adjacent_nodes[0]
                # find ending node pod
                if(connection[0] not in graph.nodes) or len(list(graph.neighbors(connection[0]))) == 0:
                    if debug:
                        print(f"Pod {pod} wants to connect to unscheduled Pod {connection[0]}!")
                    continue
                end = list(graph.neighbors(connection[0]))[0]
                shortest_path = nx.shortest_path(graph, start, end, "latency")
                latency = 0
                for i in range(len(shortest_path) - 1):
                    latency += graph[shortest_path[i]][shortest_path[i + 1]]["latency"]
    # Now throughput
                throughput = math.inf
                for i in range(len(shortest_path) - 1):
                    if graph[shortest_path[i]][shortest_path[i + 1]]["throughput"] < throughput:
                        throughput = graph[shortest_path[i]][shortest_path[i + 1]]["throughput"]

                if latency > connection[1]:
                    val += (latency/connection[1])*100-100
                if throughput < connection[2]:
                    val += 100-(throughput/connection[2])*100
                
                print(f"for pod {pod} to connect to {connection[0]} traverse nodes: " + str(shortest_path) + " latency: " + str(latency) + "/" + str(connection[1]) + " throughput: " + str(throughput) + "/" + str(connection[2]))
    print(f"Evaluation: {round(val, 2)}")
    return round(val, 2)