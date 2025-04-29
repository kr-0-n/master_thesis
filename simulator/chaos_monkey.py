import networkx as nx
from utils import *
rnd =None
"""
The chaos monkey creates chaos by deleting nodes, pods, and links. Beware, they are randomly chosen.
"""

def delete_nodes(graph: nx.DiGraph):
    global rnd
    for node in get_node_ids(graph):
        node_stability = graph.nodes[node]["stability"]
        if node_stability == None: 
            print(f"{__name__}: Node {node} has no stability")
            node_stability = 0.5 # Node stability hasnt been set. Default to 0.5
        if rnd.random() > node_stability:
            graph.remove_node(node)
    return graph

def delete_pods(graph: nx.DiGraph):
    global rnd
    for pod in get_pod_ids(graph):
        pod_stability = graph.nodes[pod]["stability"]
        if pod_stability == None: 
            print(f"{__name__}: Pod {pod} has no stability")
            pod_stability = 0.5 # Pod stability hasnt been set. Default to 0.5
        if rnd.random() > pod_stability:
            graph.remove_node(pod)
    return graph

def delete_links(graph: nx.DiGraph):
    global rnd
    available_links = list(link for link in graph.edges if "type" in graph.edges[link] and graph.edges[link]["type"] == "connection")
    # print(f"{__name__}: Available Connections: {available_links}")
    if len(available_links) == 0:
        return graph
    for link in available_links:
        link_stability = graph.edges[link]["stability"]
        if link_stability == None: 
            print(f"{__name__}: Link {link} has no stability")
            link_stability = 0.5 # Link stability hasnt been set. Default to 0.5
        if rnd.random() > link_stability:
            graph.remove_edge(link[0], link[1])
    return graph
