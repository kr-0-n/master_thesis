import conf
import networkx as nx
import k8.scheduler as scheduler 
from k8.evaluator import evaluate_step
import visualizer
from metrics import create_metric
from metrics import update_metric

class Kubernetes:
    def __init__(self, network: nx.Graph, algorithm):
        print(f"{__name__}: Kubernetes initialized")
        self.algorithm = algorithm
        print(f"{__name__}: using {self.algorithm.__name__} algorithm")
        self.scheduler = scheduler.Scheduler(self.algorithm)
        self.graph = network

        create_metric('evaluation')
        create_metric('nodes_online')
        create_metric('pods_online')
        create_metric('links_online')
        create_metric('num_eval_func_calls')
        create_metric('network_penalty')


    def tick(self):
        if self.current_deployment is not None:
            nodes_online_count = len([node for node in self.graph.nodes if self.graph.nodes[node]["type"] == "node"])
            update_metric('nodes_online', nodes_online_count)
            pods_online_count = len([node for node in self.graph.nodes if self.graph.nodes[node]["type"] == "pod"])
            update_metric('pods_online', pods_online_count)
            links_online_count = len([edge for edge in self.graph.edges if self.graph.edges[edge]["type"] == "connection"])
            update_metric('links_online', links_online_count)


            # check if all pods from the deployment are running
            pods_to_schedule = [pod for pod in self.current_deployment['pods'] if pod[0] not in [node for node in self.graph.nodes if self.graph.nodes[node]["type"] == "pod"]] 
            if len(pods_to_schedule) > 0:
                print(f"{__name__}: Pod(s) {pods_to_schedule} are not running")
                new_graph = self.scheduler.schedule(pods_to_schedule, self.graph)
                evaluation = evaluate_step(self.graph, new_graph, debug=False)
                print(f"{__name__}: Evaluation: {evaluation}")
                update_metric('evaluation', evaluation)
                
                self.graph = new_graph

            # visualizer.draw_graph(self.graph, "k8: " )
        return

    def deploy(self, deployment):
        self.current_deployment = deployment
        return
