import conf
import networkx as nx
import k8.scheduler as scheduler 
from k8.evaluator import evaluate_step
import visualizer
import k8.algorithm

class Kubernetes:
    def __init__(self, network: nx.Graph):
        print(f"{__name__}: Kubernetes initialized")
        self.algorithm = k8.algorithm.random
        print(f"{__name__}: using {self.algorithm.__name__} algorithm")
        self.scheduler = scheduler.Scheduler(self.algorithm)
        self.graph = network

    def tick(self, time):
        if self.current_deployment is not None:
            # check if all pods from the deployment are running
            for pod in self.current_deployment['pods']:
                if pod[0] not in [node for node in self.graph.nodes if self.graph.nodes[node]["type"] == "pod"]:
                    print(f"{__name__}: Pod {pod[0]} is not running")
                    new_graph = self.scheduler.schedule(pod, self.graph)
                    visualizer.draw_graph(new_graph, "k8: " + str(evaluate_step(self.graph, new_graph, time, debug=False)))
                    self.graph = new_graph
        return

    def deploy(self, deployment):
        self.current_deployment = deployment
        return