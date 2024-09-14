import networkx as nx
from visualizer import draw_graph
from k8.evaluator import evaluate
import math

class Scheduler():
    def __init__(self, algorithm):
        self.selected_algorithm = algorithm
    def schedule(self, pod, graph):
        return self.selected_algorithm(graph, pod, debug=False, visualize=False)
    def optimize(self, graph):
        return self.selected_algorithm(graph, debug=False, visualize=False)
    # # Schedule new
    # for i in range(7):
    #     graph = schedule(simple_graph['pods'][i], graph)

    #     draw_graph(graph, simple_graph, "Current algorithm: " + selected_algorithm.__name__ + " | Evaluation: " + str(evaluate(graph, debug=False)))

