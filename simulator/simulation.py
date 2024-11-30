from k8 import kubernetes_wrapper
import chaos_monkey
import conf
import random as rnd
import network_administration
import metrics
import Time as time

rnd.seed(1234567891234567891234567891234)

metrics.initialize()
print("metrics initialized")
k8 = kubernetes_wrapper.Kubernetes(network_administration.setup_network())
k8.deploy(conf.deployment)


while True:
    k8.tick()
    if time.current_time_step() % 5 == 0:
        network_administration.repair_network(k8.graph)
        k8.scheduler.optimize(k8.graph)
    # randomely invoke the chaos monkey
    if rnd.random() < 0.1:
        if len([node for node in k8.graph.nodes if k8.graph.nodes[node]["type"] == "node"]) > 1:
            chaos_monkey.delete_node(k8.graph)
            pass
    if rnd.random() < 0.1:
        chaos_monkey.delete_pod(k8.graph)
        pass
    if rnd.random() < 0.1:
        chaos_monkey.delete_link(k8.graph)
    # periodically repair the network

    time.increment_time()
    print(f"{__name__}: Time: {time.current_time_step()}")
