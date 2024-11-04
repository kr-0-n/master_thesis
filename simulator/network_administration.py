import networkx as nx
import conf
from simmath.LinearFunction import LinearFunction
from metrics import create_metric

graph = None
node_failures = {} # syntax: {node: [time_of_failure]}
node_online_metric = create_metric("nodes_online")


def setup_network():
    # Create an undirected graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(conf.simple_graph['nodes'])

    # Add edges
    G.add_edges_from(conf.simple_graph['edges'], type="connection")
    for edge in G.edges:
        G.edges[edge]["service"] = LinearFunction(G.edges[edge]["throughput"], 0, -G.edges[edge]["latency"])
        print(G.edges[edge])

    global graph
    graph = G
    return G

def repair_network(graph: nx.Graph, time):
    node_online_metric.set(len(graph.nodes))
    # First check nodes
    for node in conf.simple_graph['nodes']:
        if node[0] not in graph.nodes:
            print(f"{__name__}: Node {node[0]} offline")
            if not node[0] in node_failures: node_failures[node[0]] = []
            node_failures[node[0]].append(time)
            graph.add_node(node[0], **node[1])
            print(f"{__name__}: Node {node[0]} back online")
    # Then check edges
    for edge in conf.simple_graph['edges']:
        if (edge[0], edge[1]) not in graph.edges:
            print(f"{__name__}: Link ({edge[0]}, {edge[1]}) offline")
            graph.add_edge(edge[0], edge[1], type="connection", **edge[2], service=LinearFunction(edge[2]["throughput"], 0, -edge[2]["latency"]))
            print(f"{__name__}: Link ({edge[0]}, {edge[1]}) back online")

    return