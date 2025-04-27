import math
import networkx as nx
from simmath.LinearFunction import LinearFunction
from simmath.maxplus import multiply, devide
from simmath.minplus import min
import Time as time
import network_administration
import conf
import metrics
from utils import *
import visualizer

def network_penalty(graph: nx.Graph, debug=False):
    val = 0
    unconnected_pod_penalty = conf.unconnected_pod_penalty
    latency_penalty = conf.latency_penalty
    throughput_penalty = conf.throughput_penalty


    # Clean the input functions on the graph
    for edge in (edge for edge in graph.edges if graph.edges[edge].get("type") == "connection"):
        graph.edges[edge]["wanted_service"] = {(edge[0], edge[1]):LinearFunction(0, 0, 0), (edge[1], edge[0]):LinearFunction(0, 0, 0)}

    for pod_id in get_pod_ids(graph):
        assigned_node_id = get_assigned_node_id(graph, pod_id)
        if assigned_node_id == None:
            val += unconnected_pod_penalty
            continue
        for connection in graph.nodes[pod_id]["network"]:
            start = assigned_node_id
            # find ending node pod
            if connection[0] not in graph  or get_assigned_node_id(graph, connection[0]) == None:
                if debug: print(f"Pod {pod_id} wants to connect to unscheduled Pod {connection[0]}!")
                continue
            end = get_assigned_node_id(graph, connection[0])
            try:
                shortest_path = nx.shortest_path(graph, start, end, "latency")
            except nx.NetworkXNoPath:
                if debug: print(f"Pod {pod_id} wants to connect to unscheduled Pod {connection[0]}!")
                continue
            
            if debug: print(f"Shortest path from {start} to {end} is {shortest_path}")

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

def resources_penalty(graph: nx.DiGraph, debug=False):
    # See if nodes are overloaded
    val = 0
    for node in get_node_ids(graph):
        cpu_load = 0
        mem_load = 0
        for pod_id in get_assigned_pod_ids(graph, node):
            if graph.nodes[pod_id]["type"] == "pod":
                cpu_load += graph.nodes[pod_id]["cpu"]
                mem_load += graph.nodes[pod_id]["mem"]
        if cpu_load - graph.nodes[node]["cpu"] > 0:
            val += cpu_load - graph.nodes[node]["cpu"]
        if mem_load - graph.nodes[node]["mem"] > 0:
            val += mem_load - graph.nodes[node]["mem"]
        if debug:
            print(f"node {node}: cpu {cpu_load}/{graph.nodes[node]['cpu']} | mem {mem_load}/{graph.nodes[node]['mem']}")
    return val

def labels_penalty(graph, debug=False):
    val = 0
    for pod in get_pod_ids(graph):
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

def node_stability_penalty(graph: nx.DiGraph, debug=False):
    stability_penalty = conf.stability_penalty
    floating_average_window = conf.floating_average_window
    for node in get_node_ids(graph):
        amount_of_assigned_pods = len(get_assigned_pod_ids(graph, node))
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

def spread_penalty(graph: nx.DiGraph, debug=False):
    val = 0
     ## Aim for an even distribution
    num_pods = len(get_pod_ids(graph)) + 1
    num_nodes = len(get_node_ids(graph))
    avg_pods_per_node = num_pods / num_nodes

    for node in get_node_ids(graph):
        pods_per_node = len(get_assigned_pod_ids(graph, node))
        val += abs(pods_per_node - avg_pods_per_node) * conf.spread_penalty
    return val

def evaluate(graph, debug=False, record_metrics=False):
    # Remove all wanted connections (they are unwanted)
    graph.remove_edges_from((edge for edge in graph.edges if graph.edges[edge]["type"] == "wanted_connection"))
    
    val = 0
    resources_penalty_value = resources_penalty(graph, False)
    val += resources_penalty_value
    network_penalty_value = network_penalty(graph, False)
    val += network_penalty_value
    labels_penalty_value = labels_penalty(graph, False)
    val += labels_penalty_value
    node_stability_penalty_value = node_stability_penalty(graph, False)
    val += node_stability_penalty_value
    spread_penalty_value = spread_penalty(graph, False)
    val += spread_penalty_value

    if record_metrics:
        metrics.update_metric('resources_penalty', resources_penalty_value)
        metrics.update_metric('labels_penalty', labels_penalty_value)
        metrics.update_metric('node_stability_penalty', node_stability_penalty_value)
        metrics.update_metric('spread_penalty', spread_penalty_value)
        metrics.update_metric('network_penalty', network_penalty_value)
    if debug:
        print("-"*50)
        print(f"Resources penalty: {resources_penalty_value}")
        print(f"Network penalty: {network_penalty_value}")
        print(f"Labels penalty: {labels_penalty_value}")
        print(f"Node stability penalty: {node_stability_penalty_value}")
        print(f"Spread penalty: {spread_penalty_value}")
        print(f"Evaluation: {round(val, 2)}")

    return round(val, 2)

def evaluate_step(old_graph, new_graph, debug=False, record_metrics=False):
    val = evaluate(new_graph, debug)
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
