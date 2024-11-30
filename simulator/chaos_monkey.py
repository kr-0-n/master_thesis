import random as rnd
import networkx as nx

"""
The chaos monkey creates chaos by deleting nodes, pods, and links. Beware, they are randomly chosen.
"""

def delete_node(graph: nx.DiGraph):
    # remove random node and all adjacent assigned pods
    node = rnd.choice(list(node for node in graph.nodes if graph.nodes[node]["type"] == "node"))
    print(f"{__name__}: Deleting node {node}")
    adjacent_nodes = list(graph.neighbors(node))
    for adj_node in adjacent_nodes:
        if graph.nodes[adj_node]["type"] == "pod":
            graph.remove_node(adj_node)
    graph.remove_node(node)
   
    return graph

def delete_pod(graph):
    pod = rnd.choice(list(pod for pod in graph.nodes if graph.nodes[pod]["type"] == "pod"))
    print(f"{__name__}: Deleting pod {pod}")
    graph.remove_node(pod)
    for edge in graph.edges:
        if edge[0] == pod or edge[1] == pod:
            graph.remove_edge(edge[0], edge[1])
    return graph

def delete_link(graph):
    available_links = list(link for link in graph.edges if "type" in graph.edges[link] and graph.edges[link]["type"] == "connection")
    # print(f"{__name__}: Available Connections: {available_links}")
    if len(available_links) == 0:
        return graph
    link = rnd.choice(available_links)
    print(f"{__name__}: Deleting link {link}")
    graph.remove_edge(link[0], link[1])
    return graph