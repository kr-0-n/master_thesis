from k8 import kubernetes_wrapper
import chaos_monkey
import conf
import random as rnd
import network_administration

time = 0
k8 = kubernetes_wrapper.Kubernetes(network_administration.setup_network())
k8.deploy(conf.deployment)

while True:
    k8.tick(time)
    # randomely invoke the chaos monkey
    if rnd.random() < 0.1:
        if len([node for node in k8.graph.nodes if k8.graph.nodes[node]["type"] == "node"]) > 1:
            chaos_monkey.delete_node(k8.graph)
    if rnd.random() < 0.1:
        chaos_monkey.delete_pod(k8.graph)
    if rnd.random() < 0.1:
        chaos_monkey.delete_link(k8.graph)
    # periodically repair the network
    if time % 5 == 0:
        network_administration.repair_network(k8.graph)
        k8.scheduler.optimize(k8.graph)
    time += 1
    print(f"{__name__}: Time: {time}")
