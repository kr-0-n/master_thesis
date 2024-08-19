import k8.algorithm as algorithm
import networkx as nx
from visualizer import draw_graph
from k8.evaluator import evaluate
import math

selected_algorithm = algorithm.random


def schedule(pod, graph):
    return selected_algorithm(graph, pod, debug=False, visualize=False)
def optimize(graph):
    return selected_algorithm(graph, debug=False, visualize=False)
# # Schedule new
# for i in range(7):
#     graph = schedule(simple_graph['pods'][i], graph)

#     draw_graph(graph, simple_graph, "Current algorithm: " + selected_algorithm.__name__ + " | Evaluation: " + str(evaluate(graph, debug=False)))

