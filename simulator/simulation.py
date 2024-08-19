from k8 import kubernetes_wrapper
import chaos_monkey
import conf
import random as rnd

time = 0

kubernetes_wrapper.deploy(conf.deployment)

while True:
    # if time % 10 == 0 and current_pod < len(simple_graph['pods']):
    #     new_graph = schedule(simple_graph['pods'][current_pod], graph.copy())
    #     print(f"Step evaluation: {evaluate_step(graph, new_graph, debug=True)}")
    #     graph = new_graph
    #     current_pod += 1
    #     draw_graph(graph, simple_graph, " | Evaluation: " + str(evaluate(graph, debug=False)))
    kubernetes_wrapper.tick(time)
    # randomely invoke the chaos monkey
    if rnd.random() < 0.5:
        chaos_monkey.delete_pod(kubernetes_wrapper.graph)
    time += 1
    print(f"Time: {time}")
