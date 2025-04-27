import networkx as nx
import conf
from simmath.LinearFunction import LinearFunction
from metrics import create_metric
import Time as time

node_failures = {} # syntax: {node: [time_of_failure]}

def setup_network(graph_dict: dict) -> nx.Graph:
    # Create an undirected graph
    global shared_graph_dict
    shared_graph_dict = graph_dict
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(shared_graph_dict['nodes'])

    # Add edges
    G.add_edges_from(shared_graph_dict['edges'], type="connection")
    for edge in G.edges:
        G.edges[edge]["service"] = LinearFunction(G.edges[edge]["throughput"], 0, -G.edges[edge]["latency"])
        print(G.edges[edge])

    return G

def repair_network(graph: nx.Graph):
    # First check nodes
    for node in shared_graph_dict['nodes']:
        if node[0] not in graph.nodes:
            print(f"{__name__}: Node {node[0]} offline")
            if not node[0] in node_failures: node_failures[node[0]] = []
            node_failures[node[0]].append(time.current_time_step())
            graph.add_node(node[0], **node[1])
            print(f"{__name__}: Node {node[0]} back online")
    # Then check edges
    for edge in shared_graph_dict['edges']:
        if (edge[0], edge[1]) not in graph.edges:
            print(f"{__name__}: Link ({edge[0]}, {edge[1]}) offline")
            graph.add_edge(edge[0], edge[1], type="connection", **edge[2], service=LinearFunction(edge[2]["throughput"], 0, -edge[2]["latency"]))
            print(f"{__name__}: Link ({edge[0]}, {edge[1]}) back online")

    return