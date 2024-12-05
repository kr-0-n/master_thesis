from k8 import kubernetes_wrapper
import chaos_monkey
import conf
from random import Random
import network_administration
import metrics
import Time as time

rnd = Random()
rnd.seed(43)

metrics.initialize("aco")
print("metrics initialized")
k8 = kubernetes_wrapper.Kubernetes(network_administration.setup_network())
k8.deploy(conf.deployment)

while time.current_time_step() < 1440:
    k8.tick()
    if time.current_time_step() % 5 == 0:
        print(f"chaos monkey invoked at {time.current_time_step()}")
        network_administration.repair_network(k8.graph)
        # k8.scheduler.optimize(k8.graph)

    # randomely invoke the chaos monkey
    if rnd.random() < 0.1:
        print(f"chaos monkey invoked at {time.current_time_step()}")
        if len([node for node in k8.graph.nodes if k8.graph.nodes[node]["type"] == "node"]) > 1:
            chaos_monkey.delete_node(k8.graph)
            pass
    if rnd.random() < 0.1:
        print(f"chaos monkey invoked at {time.current_time_step()}")
        chaos_monkey.delete_pod(k8.graph)
        pass
    if rnd.random() < 0.1:
        print(f"chaos monkey invoked at {time.current_time_step()}")
        chaos_monkey.delete_link(k8.graph)
    # periodically repair the network

    time.increment_time()
    print(f"{__name__}: Time: {time.current_time_step()}")
