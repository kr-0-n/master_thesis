import math
import networkx as nx
from simmath.LinearFunction import LinearFunction
from simmath.maxplus import multiply, devide
from simmath.minplus import min
import Time as time
import network_administration
import conf
import metrics

def network_penalty(graph, debug=False):
    val = 0
    unconnected_pod_penalty = conf.unconnected_pod_penalty
    latency_penalty = conf.latency_penalty
    throughput_penalty = conf.throughput_penalty


    # Clean the input functions on the graph
    for edge in (edge for edge in graph.edges if graph.edges[edge].get("type") == "connection"):
        graph.edges[edge]["wanted_service"] = {(edge[0], edge[1]):LinearFunction(0, 0, 0), (edge[1], edge[0]):LinearFunction(0, 0, 0)}


    for pod in graph.nodes:
        if graph.nodes[pod]["type"] == "pod":
            for connection in graph.nodes[pod]["network"]:
                # find starting node pod
                adjacent_nodes = list(graph.neighbors(pod))
                if(len(adjacent_nodes) == 0):
                    val += 1000
                    if debug: print(f"Pod {pod} has not been scheduled!")
                    continue
                start = adjacent_nodes[0]
                # find ending node pod
                if(connection[0] not in graph.nodes) or len(list(graph.neighbors(connection[0]))) == 0:
                    if debug: print(f"Pod {pod} wants to connect to unscheduled Pod {connection[0]}!")
                    continue
                end = list(graph.neighbors(connection[0]))[0]
                try:
                    shortest_path = nx.shortest_path(graph, start, end, "latency")
                except nx.NetworkXNoPath:
                    if debug: print(f"Pod {pod} wants to connect to unscheduled Pod {connection[0]}!")
                    continue
                
                if debug: print(shortest_path)

                last_additional_output = LinearFunction(connection[2], 0, 0)


                accumulated_latency = 0
                for step in range(len(shortest_path) - 1):
                    
                    if debug: print(f"latest additional output: {last_additional_output}")
                    link = graph.edges[( shortest_path[step],shortest_path[step+1])]
                    accumulated_latency += link["latency"]
                    old_link_wanted_service = link["wanted_service"][(shortest_path[step],shortest_path[step+1])]

                    new_link_wanted_service = multiply(last_additional_output, old_link_wanted_service)
                    link["wanted_service"][(shortest_path[step],shortest_path[step+1])] = new_link_wanted_service
                    if old_link_wanted_service.m > link['service'].m:
                        last_additional_output = LinearFunction(0, 0, 0)
                    else:
                        if new_link_wanted_service.m <= link['service'].m:
                            last_additional_output = last_additional_output
                        else:
                            last_additional_output = devide(link['service'], old_link_wanted_service)

                    # In this case we have a higher usage then we can serve - this leads to a peanlty
                    if new_link_wanted_service.m > link['service'].m:
                        val += throughput_penalty * (new_link_wanted_service.m - link['service'].m)
                # print("accumulated latency", accumulated_latency)
                val += latency_penalty * accumulated_latency

    if debug: print([graph.edges[edge] for edge in graph.edges if "type" in graph.edges[edge] and graph.edges[edge]["type"] == "connection"])
    return val

def resources_penalty(graph, debug=False):
    # See if nodes are overloaded
    val = 0
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
            if debug:
                print(f"node {node}: cpu {cpu_load}/{graph.nodes[node]['cpu']} | mem {mem_load}/{graph.nodes[node]['mem']}")
    return val

def labels_penalty(graph, debug=False):
    val = 0
    for pod in (pod for pod in graph.nodes if graph.nodes[pod]["type"] == "pod"):
        if "labelSelector" not in graph.nodes[pod]:
            if debug: print(f"Pod {pod} has no labelSelector")
            continue
        else:
            labelSelector = graph.nodes[pod]["labelSelector"]
        # Get the node this pod is assigned to
        try:
            node = list(node for node in graph.neighbors(pod) if graph.nodes[node]["type"] == "node")[0]
        except IndexError:
            if debug: print(f"Pod {pod} has not been scheduled!")
            continue
        # Get the labels of the node
        if "labels" not in graph.nodes[node]:
            if debug: print(f"Node {node} has no labels")
            labels = []
        else:
            labels = graph.nodes[node]["labels"]
        for label in labelSelector:
            if label not in labels:
                val += conf.label_penalty
        
    return val

def node_stability_penalty(graph, debug=False):
    stability_penalty = conf.stability_penalty
    floating_average_window = conf.floating_average_window
    for node in (node for node in graph.nodes if graph.nodes[node]["type"] == "node"):
        amount_of_assigned_pods = len(list(pod for pod in list(graph.neighbors(node)) if graph.nodes[pod]["type"] == "pod"))
        floating_average_of_crashes = 0
        if not node in network_administration.node_failures: pass
        else: 
            crashes = 0
            for crash in network_administration.node_failures[node]:
                if time.current_time_step() - crash <= floating_average_window: crashes += 1
            floating_average_of_crashes = crashes / floating_average_window
            if debug: print(f"node {node} has {amount_of_assigned_pods} pods assigned and has a floating average of {crashes} crashes")
        
    val = stability_penalty * floating_average_of_crashes
    return val

def spread_penalty(graph, debug=False):
    val = 0
    return val

def evaluate(graph, debug=False):
    # Remove all wanted connections (they are unwanted)
    graph.remove_edges_from((edge for edge in graph.edges if graph.edges[edge]["type"] == "wanted_connection"))
    
    if debug: print("-"*50)
    val = 0
    val += resources_penalty(graph, debug)
    net_pen = network_penalty(graph, debug)
    metrics.update_metric('network_penalty', net_pen)
    val += net_pen
    val += labels_penalty(graph, debug)
    val += node_stability_penalty(graph, debug)
    val += spread_penalty(graph, debug)
    if debug:print(f"Evaluation: {round(val, 2)}")
    return round(val, 2)

def evaluate_step(old_graph, new_graph, debug=False):
    val = evaluate(new_graph, False)
    # check if a pod moved to a new node in the new graph
    # get all 'assign' connections in both graphs and compare them
    move_pod_penalty = conf.move_pod_penalty
    old_assignments = []
    new_assignments = []
    for edge in old_graph.edges:
        if old_graph.edges[edge]["type"] == "assign":
            old_assignments.append(edge)
    for edge in new_graph.edges:
        if new_graph.edges[edge]["type"] == "assign":
            new_assignments.append(edge)
    if debug:
        print(f"Old assignments: {old_assignments}")
        print(f"New assignments: {new_assignments}")
    for assignment in old_assignments:
        if assignment not in new_assignments:
            val += move_pod_penalty
    if debug:print(f"Evaluation: {round(val, 2)}")
    return round(val, 2)
