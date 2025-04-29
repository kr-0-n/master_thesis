import conf as conf
import simulation as sim
import k8.algorithm as alg

runs_postfix = ["evolutionary", "ant_colony", "simulated_annealing", "kubernetes_default"]
algorithms = [alg.evolutionary_solve,alg.ant_colony_solve, alg.simulated_annealing_solve, alg.kubernetes_default]

for i, run in enumerate(runs_postfix):
    conf.algorithm = algorithms[i]
    conf.metrics_name_postfix = run
    sim.run_simulation()
