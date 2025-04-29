from k8 import kubernetes_wrapper
import chaos_monkey
import conf
from random import Random
import network_administration
import metrics
import Time as time
from utils import *


def run_simulation():
    time.reset_time()
    rnd = Random()

    rnd.seed(conf.random_seed)
    chaos_monkey.rnd = rnd

    run_id = rnd.randint(1000, 9999)

    metrics.initialize(conf.metrics_name_postfix, run_id)
    print("metrics initialized")
    k8 = kubernetes_wrapper.Kubernetes(network_administration.setup_network(conf.graph), conf.algorithm)
    k8.deploy(conf.deployment)

    while time.current_time_step() < 1440:
        k8.tick()
        if time.current_time_step() % 5 == 0:
            print(f"network repaired at {time.current_time_step()}")
            network_administration.repair_network(k8.graph)
            # k8.scheduler.optimize(k8.graph)

        # invoke the chaos monkey
        chaos_monkey.delete_nodes(k8.graph)
        chaos_monkey.delete_links(k8.graph)
        chaos_monkey.delete_pods(k8.graph)

        time.increment_time()
        print(f"{__name__}: Time: {time.current_time_step()}")
    print(f"Simulation k8_simulation_{run_id}_{conf.metrics_name_postfix} finished at {time.current_time_step()}")
