import networkx as nx
from visualizer import draw_graph
from k8.evaluator import evaluate
import math

class Scheduler():
    def __init__(self, algorithm):
        self.selected_algorithm = algorithm
    def schedule(self, pods: list[dict], graph: nx.Graph) -> nx.Graph:
        # Remove and reschedule unassigned pods
        return self.selected_algorithm(graph, pods, debug=False, visualize=False)
    def optimize(self, graph):
        return self.selected_algorithm(graph, debug=False, visualize=False)