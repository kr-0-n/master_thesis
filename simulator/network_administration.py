import networkx as nx
import conf

graph = None

def setup_network():
    # Create an undirected graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(conf.simple_graph['nodes'])

    # Add edges
    G.add_edges_from(conf.simple_graph['edges'], type="connection")
    global graph
    graph = G
    return G

def repair_network(graph: nx.Graph):
    # First check nodes
    for node in conf.simple_graph['nodes']:
        if node[0] not in graph.nodes:
            print(f"{__name__}: Node {node[0]} offline")
            graph.add_node(node[0], **node[1])
            print(f"{__name__}: Node {node[0]} back online")
    # Then check edges
    for edge in conf.simple_graph['edges']:
        if (edge[0], edge[1]) not in graph.edges:
            print(f"{__name__}: Link ({edge[0]}, {edge[1]}) offline")
            graph.add_edge(edge[0], edge[1], type="connection", **edge[2])
            print(f"{__name__}: Link ({edge[0]}, {edge[1]}) back online")

    return