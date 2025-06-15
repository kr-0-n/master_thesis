import conf as conf
import simulation as sim
import k8.algorithm as alg

runs_postfix = ["ant_colony_demo"]
algorithms = [alg.ant_colony_solve]


for i, run in enumerate(runs_postfix):
    conf.algorithm = algorithms[i]
    conf.metrics_name_postfix = run
    sim.run_simulation()
