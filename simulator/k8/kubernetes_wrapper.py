import conf
import networkx as nx
import k8.scheduler as scheduler 
from k8.evaluator import evaluate_step
import visualizer
import k8.algorithm
from metrics import create_metric
from metrics import update_metric

class Kubernetes:
    def __init__(self, network: nx.Graph):
        print(f"{__name__}: Kubernetes initialized")
        self.algorithm = k8.algorithm.ant_colony_solve
        print(f"{__name__}: using {self.algorithm.__name__} algorithm")
        self.scheduler = scheduler.Scheduler(self.algorithm)
        self.graph = network
        create_metric('evaluation')
        create_metric('nodes_online')
        create_metric('pods_online')
        create_metric('links_online')
        create_metric('num_eval_func_calls')


    def tick(self):
        print(f"{__name__}: tick")
        if self.current_deployment is not None:
            nodes_online_count = len([node for node in self.graph.nodes if self.graph.nodes[node]["type"] == "node"])
            update_metric('nodes_online', nodes_online_count)
            pods_online_count = len([node for node in self.graph.nodes if self.graph.nodes[node]["type"] == "pod"])
            update_metric('pods_online', pods_online_count)
            links_online_count = len([edge for edge in self.graph.edges if self.graph.edges[edge]["type"] == "connection"])
            update_metric('links_online', links_online_count)

            # check if all pods from the deployment are running
            for pod in self.current_deployment['pods']:
                if pod[0] not in [node for node in self.graph.nodes if self.graph.nodes[node]["type"] == "pod"]:
                    print(f"{__name__}: Pod {pod[0]} is not running")
                    new_graph = self.scheduler.schedule(pod, self.graph)
                    evaluation = evaluate_step(self.graph, new_graph, debug=False)
                    print(f"{__name__}: Evaluation: {evaluation}")
                    update_metric('evaluation', evaluation)
                
                    # visualizer.draw_graph(new_graph, "k8: " + str(evaluation))
                    self.graph = new_graph
        return  

    def deploy(self, deployment):
        self.current_deployment = deployment
        return
