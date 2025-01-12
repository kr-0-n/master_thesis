from k8.algorithm import *
def get_node_node(id):
    return (id, {"type": "node", "color": "lightblue", "shape": "s"})
# Start with index 1. Index 0 is the nonexistent node
small_graph={
    "nodes": [(1, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100, "labels": ["SSD"]}),
              (2, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100}),
              (3, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100}),
              (4, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100}),],
    "edges": [(1, 2, {"throughput": 5, "latency": 2}), (1, 3, {"throughput": 1, "latency": 3}), (2, 4, {"throughput": 3, "latency": 4}), (3, 4, {"throughput": 10, "latency": 10})],
    "pos": {1: [-0.34833021,  0.09425495], 2: [ 0.01927328, -0.07205069], 3: [-0.43677531,  0.66727785], 4: [ 0.50957367, -0.06202244], 5: [0.98649442, 0.24973923], 6: [-0.84259233, -0.21467222], 7: [-0.89098206,  0.34020218], 8: [ 0.00333854, -0.64498511], 9: [ 1, -0.35774376]}
}

medium_graph={
    "nodes": [(1, {"type": "node", "color": "lightcoral", "shape": "s", "cpu": 100, "mem": 64}),
              (2, {"type": "node", "color": "lightcoral", "shape": "s", "cpu": 100, "mem": 64}),
              (3, {"type": "node", "color": "lightcoral", "shape": "s", "cpu": 100, "mem": 64}),
              (4, {"type": "node", "color": "lightcoral", "shape": "s", "cpu": 100, "mem": 64}),
              (5, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (6, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (7, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (8, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (9, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (10, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (11, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (12, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (13, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (14, {"type": "node", "color": "moccasin", "shape": "s", "cpu": 50, "mem": 32}),
              (15, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 20, "mem": 16}),
              (16, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 20, "mem": 16}),
              (17, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 20, "mem": 16}),
              (18, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 20, "mem": 16}),
              (19, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 20, "mem": 16}),
              (20, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 20, "mem": 16}),
              ],
    "edges": [
        # Strong interconnections between base Stations
        (1, 2, {"throughput": 500, "latency": 7}), (1, 3, {"throughput": 500, "latency": 7}), (1, 4, {"throughput": 500, "latency": 10}), (2, 3, {"throughput": 500, "latency": 7}), (2, 4, {"throughput": 500, "latency": 7}), (3, 4, {"throughput": 500, "latency": 7})
        # Clients connect to basestations
        , (5, 1, {"throughput": 100, "latency": 15}), (6, 1, {"throughput": 100, "latency": 15}), (7, 1, {"throughput": 100, "latency": 15})
        , (8, 2, {"throughput": 100, "latency": 15}), (9, 2, {"throughput": 100, "latency": 15}), (10, 2, {"throughput": 100, "latency": 15})
        , (11, 3, {"throughput": 100, "latency": 15}), (12, 3, {"throughput": 100, "latency": 15})
        , (13, 4, {"throughput": 100, "latency": 15}), (14, 4, {"throughput": 100, "latency": 15})
    # Sattelite clients
        , (15, 1, {"throughput": 10, "latency": 100}), (16, 1, {"throughput": 10, "latency": 100})
        , (17, 2, {"throughput": 10, "latency": 100}), (18, 2, {"throughput": 10, "latency": 100})
        , (19, 3, {"throughput": 10, "latency": 100})
        , (20, 4, {"throughput": 10, "latency": 100})
    ],
    "pos": {1: [-0.34833021,  0.09425495], 2: [ 0.01927328, -0.07205069], 3: [-0.43677531,  0.66727785], 4: [ 0.50957367, -0.06202244], 5: [0.98649442, 0.24973923], 6: [-0.84259233, -0.21467222], 7: [-0.89098206,  0.34020218], 8: [ 0.00333854, -0.64498511], 9: [ 1, -0.35774376]}
}

small_deployment = {
    "pods": [(5, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(6,3,5)]}), # network syntax: (pod_to, latency, throughput)
             (6, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(7,3,2)]}),
             (7, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(5,3,5)]}),
             #(8, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(8,3,1)]}),
             (9, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(5,3,3)]}),
             #(10, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(5,3,3)]}),
             #(11, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(9,5,3)]})
             ],
}

medium_deployment = {
    "pods": [
        # Data collection app
        (21, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 8, "network": [(22,10,10)]}), # network syntax: (pod_to, latency, throughput)
        (22, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 8, "network": [(21,10,10)]}),
        (23, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (24, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (25, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (26, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (27, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (28, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (29, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (30, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (31, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        (32, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 1, "network": [(21,500,5)]}),
        # P2P Streaming app
        (33, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 4, "network": [(34,100,10), (35,100,10), (36,100,10), (37,100,10)]}),
        (34, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 4, "network": [(33,100,10), (35,100,10), (36,100,10), (37,100,10)]}),
        (35, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 4, "network": [(33,10,10), (34,10,10), (36,10,10), (37,10,10)]}),
        (36, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 4, "network": [(33,10,10), (34,10,10), (35,10,10), (37,10,10)]}),
        (37, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 4, "network": [(33,10,10), (34,10,10), (35,10,10), (36,10,10)]}),
        # Video Streaming app
        (38, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 60, "mem": 8, "network": []}),
        (40, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 20, "mem": 2, "network": [(38,100,10)]}),
        (41, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 20, "mem": 2, "network": [(38,100,10)]}),
        (42, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 20, "mem": 2, "network": [(38,100,10)]}),
        (43, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 20, "mem": 2, "network": [(38,100,10)]}),
        # Web Server
        (44, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 2, "network": []}),
        (45, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 2, "network": []}),
        (46, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 10, "mem": 2, "network": []}),
             ],
}

graph = small_graph
deployment = small_deployment

algorithm = ant_colony_solve
metrics_name_postfix = "aco"
random_seed = 2

# Penalties
move_pod_penalty = 100
unconnected_pod_penalty = 1000
latency_penalty = 1
throughput_penalty = 10 # calculated like this: penalty = throughput_penalty * (wanted_throughput - actual_throughput)

# Stability is calculated like this: penalty = stability_penalty * floating_average_of_crashes
stability_penalty = 10
floating_average_window = 10


# Chaos
# Every time step the chaos monked has a defined chance to delete nodes, pods or links. Define it here
node_delete_probability = 0.1
pod_delete_probability = 0.1
link_delete_probability = 0.1

