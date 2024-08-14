import algorithm
import networkx as nx
from visualizer import draw_graph
from conf import simple_graph
from evaluator import evaluate
import math

selected_algorithm = algorithm.random


def schedule(node, graph):
    return selected_algorithm(node, graph, debug=False, visualize=True)

def setup_graph_from_conf(conf):
    # Create an undirected graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(conf['nodes'])

    # Add edges
    G.add_edges_from(conf['edges'], type="connection")
    return G

graph = setup_graph_from_conf(simple_graph)
# Schedule new
for i in range(7):
    graph = schedule(simple_graph['pods'][i], graph)

    draw_graph(graph, simple_graph, "Current algorithm: " + selected_algorithm.__name__ + " | Evaluation: " + str(evaluate(graph, debug=False)))

