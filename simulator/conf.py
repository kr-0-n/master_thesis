from k8.algorithm import *
def get_node_node(id):
    return (id, {"type": "node"})

mini_graph={
    "nodes": [(1, {"type": "node", "cpu": 100, "mem": 100, "labels": ["1"]}), (2, {"type": "node", "cpu": 100, "mem": 100, "labels": ["2"]}), (3, {"type": "node", "cpu": 100, "mem": 100, "labels": ["3"]})],
    "edges": [(1, 3, {"throughput": 1, "latency": 220}), (2, 3, {"throughput": 1, "latency": 220})],
    "pos": {1: [0, 0]}
}
# Start with index 1. Index 0 is the nonexistent node
small_graph={
    "nodes": [(1, {"type": "node", "cpu": 100, "mem": 100, "labels": ["SSD"], "stability": 0.70}),
              (2, {"type": "node", "cpu": 100, "mem": 100, "stability": 0.70}),
              (3, {"type": "node", "cpu": 100, "mem": 100, "stability": 0.99}),
              (4, {"type": "node", "cpu": 100, "mem": 100, "stability": 0.99}),],
    "edges": [(1, 2, {"throughput": 5, "latency": 2, "stability": 0.99}), (1, 3, {"throughput": 1, "latency": 3, "stability": 0.99}), (2, 4, {"throughput": 3, "latency": 4, "stability": 0.99}), (3, 4, {"throughput": 10, "latency": 10, "stability": 0.99}), (4, 3, {"throughput": 10, "latency": 10, "stability": 0.99}), (4, 2, {"throughput": 10, "latency": 10, "stability": 0.99}), (3, 1, {"throughput": 10, "latency": 10, "stability": 0.99}), (2, 1, {"throughput": 10, "latency": 10, "stability": 0.99})],
    "pos": {1: [-0.34833021,  0.09425495], 2: [ 0.01927328, -0.07205069], 3: [-0.43677531,  0.66727785], 4: [ 0.50957367, -0.06202244], 5: [0.98649442, 0.24973923], 6: [-0.84259233, -0.21467222], 7: [-0.89098206,  0.34020218], 8: [ 0.00333854, -0.64498511], 9: [ 1, -0.35774376]}
}

medium_graph={
    "nodes": [(1, {"type": "node", "cpu": 100, "mem": 64, "stability": 0.99}),
              (2, {"type": "node", "cpu": 100, "mem": 64, "stability": 0.90}),
              (3, {"type": "node", "cpu": 100, "mem": 64, "stability": 0.70}),
              (4, {"type": "node", "cpu": 100, "mem": 64, "stability": 0.50}),
              (5, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (6, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (7, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (8, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (9, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (10, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (11, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (12, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (13, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (14, {"type": "node", "cpu": 50, "mem": 32, "labels": ["camera"], "stability": 0.99}),
              (15, {"type": "node", "cpu": 20, "mem": 16, "labels": ["camera", "sensor"], "stability": 0.99}),
              (16, {"type": "node", "cpu": 20, "mem": 16, "labels": ["camera", "sensor"], "stability": 0.99}),
              (17, {"type": "node", "cpu": 20, "mem": 16, "labels": ["camera", "sensor"], "stability": 0.99}),
              (18, {"type": "node", "cpu": 20, "mem": 16, "labels": ["camera", "sensor"], "stability": 0.99}),
              (19, {"type": "node", "cpu": 20, "mem": 16, "labels": ["camera", "sensor"], "stability": 0.99}),
              (20, {"type": "node", "cpu": 20, "mem": 16, "labels": ["camera", "sensor"], "stability": 0.99}),
              ],
    "edges": [
        # Strong interconnections between base Stations
        (1, 2, {"throughput": 500, "latency": 7, "stability": 0.99}), (2, 1, {"throughput": 500, "latency": 7, "stability": 0.99}), (1, 3, {"throughput": 500, "latency": 7, "stability": 0.99}), (3, 1, {"throughput": 500, "latency": 7, "stability": 0.99}), (1, 4, {"throughput": 500, "latency": 10, "stability": 0.99}), (4, 1, {"throughput": 500, "latency": 10, "stability": 0.99}), (2, 3, {"throughput": 500, "latency": 7, "stability": 0.99}), (3, 2, {"throughput": 500, "latency": 7, "stability": 0.99}), (2, 4, {"throughput": 500, "latency": 7, "stability": 0.99}), (4, 2, {"throughput": 500, "latency": 7, "stability": 0.99}), (3, 4, {"throughput": 500, "latency": 7, "stability": 0.99}), (4, 3, {"throughput": 500, "latency": 7, "stability": 0.99})
        # Clients connect to basestations
        , (5, 1, {"throughput": 100, "latency": 15, "stability": 0.99}), (1, 5, {"throughput": 100, "latency": 15, "stability": 0.99}), (6, 1, {"throughput": 100, "latency": 15, "stability": 0.99}), (1, 6, {"throughput": 100, "latency": 15, "stability": 0.99}), (7, 1, {"throughput": 100, "latency": 15, "stability": 0.99}), (1, 7, {"throughput": 100, "latency": 15, "stability": 0.99})
        , (8, 2, {"throughput": 100, "latency": 15, "stability": 0.99}), (2, 8, {"throughput": 100, "latency": 15, "stability": 0.99}), (9, 2, {"throughput": 100, "latency": 15, "stability": 0.99}), (2, 9, {"throughput": 100, "latency": 15, "stability": 0.99}), (10, 2, {"throughput": 100, "latency": 15, "stability": 0.99}), (2, 10, {"throughput": 100, "latency": 15, "stability": 0.99})
        , (11, 3, {"throughput": 100, "latency": 15, "stability": 0.99}), (3, 11, {"throughput": 100, "latency": 15, "stability": 0.99}), (12, 3, {"throughput": 100, "latency": 15, "stability": 0.99}), (3, 12, {"throughput": 100, "latency": 15, "stability": 0.99})
        , (13, 4, {"throughput": 100, "latency": 15, "stability": 0.99}), (4, 13, {"throughput": 100, "latency": 15, "stability": 0.99}), (14, 4, {"throughput": 100, "latency": 15, "stability": 0.99}), (4, 14, {"throughput": 100, "latency": 15, "stability": 0.99})
    # Sattelite clients
        , (15, 1, {"throughput": 10, "latency": 100, "stability": 0.99}), (1, 15, {"throughput": 10, "latency": 100, "stability": 0.99}), (16, 1, {"throughput": 10, "latency": 100, "stability": 0.99}), (1, 16, {"throughput": 10, "latency": 100, "stability": 0.99})
        , (17, 2, {"throughput": 10, "latency": 100, "stability": 0.99}), (2, 17, {"throughput": 10, "latency": 100, "stability": 0.99}), (18, 2, {"throughput": 10, "latency": 100, "stability": 0.99}), (2, 18, {"throughput": 10, "latency": 100, "stability": 0.99})
        , (19, 3, {"throughput": 10, "latency": 100, "stability": 0.99}), (3, 19, {"throughput": 10, "latency": 100, "stability": 0.99})
        , (20, 4, {"throughput": 10, "latency": 100, "stability": 0.99}), (4, 20, {"throughput": 10, "latency": 100, "stability": 0.99})
    ],
    "pos": {1: [-0.34833021,  0.09425495], 2: [ 0.01927328, -0.07205069], 3: [-0.43677531,  0.66727785], 4: [ 0.50957367, -0.06202244], 5: [0.98649442, 0.24973923], 6: [-0.84259233, -0.21467222], 7: [-0.89098206,  0.34020218], 8: [ 0.00333854, -0.64498511], 9: [ 1, -0.35774376]}
}

mini_deployment = {
    "pods": [(4, {"type": "pod", "cpu": 610, "mem": 30, "network": [(8,2,100)]}),
             (5, {"type": "pod", "cpu": 60, "mem": 30, "network": [(9,2,100)]}),
            #  (6, {"type": "pod", "cpu": 60, "mem": 30, "network": []}),
            #  (7, {"type": "pod", "cpu": 60, "mem": 30, "network": []}),
             ]
}

small_deployment = {
    "pods": [(5, {"type": "pod", "cpu": 30, "mem": 30, "network": [(6,3,5)], "stability": 0.99}), # network syntax: (pod_to, latency, throughput)
             (6, {"type": "pod", "cpu": 30, "mem": 30, "network": [(7,3,2)], "stability": 0.99}),
             (7, {"type": "pod", "cpu": 30, "mem": 30, "network": [(5,3,5)], "stability": 0.99}),
             (8, {"type": "pod", "cpu": 30, "mem": 30, "network": [(8,3,1)], "stability": 0.99}),
             (9, {"type": "pod", "cpu": 30, "mem": 30, "network": [(5,3,3)], "stability": 0.99}),
             (10, {"type": "pod", "cpu": 30, "mem": 30, "network": [(5,3,3)], "stability": 0.99}),
             (11, {"type": "pod", "cpu": 30, "mem": 30, "network": [(9,5,3)], "labelSelector": ["SSD"], "stability": 0.99})
             ],
}

medium_deployment = {
    "pods": [
        # Data collection app
        (21, {"type": "pod", "cpu": 30, "mem": 8, "network": [(22,10,10)], "stability": 0.99}), # network syntax: (pod_to, latency, throughput)
        (22, {"type": "pod", "cpu": 30, "mem": 8, "network": [(21,10,10)], "stability": 0.99}),
        (23, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (24, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (25, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (26, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (27, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (28, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (29, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (30, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (31, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        (32, {"type": "pod", "cpu": 10, "mem": 1, "network": [(21,500,5)], "stability": 0.99, "labelSelector": ["sensor"]}),
        # P2P Streaming app
        (33, {"type": "pod", "cpu": 30, "mem": 4, "network": [(34,100,10), (35,100,10), (36,100,10), (37,100,10)], "stability": 0.99, "labelSelector": ["camera"]}),
        (34, {"type": "pod", "cpu": 30, "mem": 4, "network": [(33,100,10), (35,100,10), (36,100,10), (37,100,10)], "stability": 0.99, "labelSelector": ["camera"]}),
        (35, {"type": "pod", "cpu": 30, "mem": 4, "network": [(33,10,10), (34,10,10), (36,10,10), (37,10,10)], "stability": 0.99, "labelSelector": ["camera"]}),
        (36, {"type": "pod", "cpu": 30, "mem": 4, "network": [(33,10,10), (34,10,10), (35,10,10), (37,10,10)], "stability": 0.99, "labelSelector": ["camera"]}),
        (37, {"type": "pod", "cpu": 30, "mem": 4, "network": [(33,10,10), (34,10,10), (35,10,10), (36,10,10)], "stability": 0.99, "labelSelector": ["camera"]}),
        # Video Streaming app
        (38, {"type": "pod", "cpu": 60, "mem": 8, "network": [], "stability": 0.99}),
        (40, {"type": "pod", "cpu": 20, "mem": 2, "network": [(38,100,10)], "stability": 0.99}),
        (41, {"type": "pod", "cpu": 20, "mem": 2, "network": [(38,100,10)], "stability": 0.99}),
        (42, {"type": "pod", "cpu": 20, "mem": 2, "network": [(38,100,10)], "stability": 0.99}),
        (43, {"type": "pod", "cpu": 20, "mem": 2, "network": [(38,100,10)], "stability": 0.99}),
        # Web Server
        (44, {"type": "pod", "cpu": 10, "mem": 2, "network": [], "stability": 0.99}),
        (45, {"type": "pod", "cpu": 10, "mem": 2, "network": [], "stability": 0.99}),
        (46, {"type": "pod", "cpu": 10, "mem": 2, "network": [], "stability": 0.99}),
             ],
}

enable_metrics = True

graph = medium_graph
deployment = medium_deployment

algorithm = evolutionary_solve


metrics_name_postfix = "evolutionary_solve"
random_seed = 19

# Penalties
move_pod_penalty = 400
unconnected_pod_penalty = 500
label_penalty = 1000
latency_penalty = 100
throughput_penalty = 10 # calculated like this: penalty = throughput_penalty * (wanted_throughput - actual_throughput)
spread_penalty = 10 # added for every pod to many or to little from the average

# Stability is calculated like this: penalty = stability_penalty * floating_average_of_crashes
stability_penalty = 20
floating_average_window = 20

# Database connection
database_host = "127.0.0.1"
database_user = "root"
database_password = "root"