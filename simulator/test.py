from visualizer import draw_graph
import network_administration
import conf
from k8.kubernetes_wrapper import Kubernetes
import metrics

metrics.record_metrics = False
k8 = Kubernetes(network_administration.setup_network(conf.graph), conf.algorithm)
k8.deploy(conf.deployment)
k8.tick()

draw_graph(k8.graph, "Model Example" )