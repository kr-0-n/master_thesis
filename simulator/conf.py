
def get_node_node(id):
    return (id, {"type": "node", "color": "lightblue", "shape": "s"})
# Start with index 1. Index 0 is the nonexistent node
simple_graph={
    "nodes": [(1, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100}),
              (2, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100}),
              (3, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100}),
              (4, {"type": "node", "color": "lightblue", "shape": "s", "cpu": 100, "mem": 100}),],
    "edges": [(1, 2, {"throughput": 5, "latency": 2}), (1, 3, {"throughput": 1, "latency": 3}), (2, 4, {"throughput": 3, "latency": 4}), (3, 4, {"throughput": 10, "latency": 10})],
    "pods": [(5, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(6,3,5)]}), # network syntax: (pod_to, latency, throughput)
             (6, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(7,3,2)]}),
             (7, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(5,3,5)]}),
             (8, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(8,3,1)]}),
             (9, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(5,3,3)]}),
             (10, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(5,3,3)]}),
             (11, {"type": "pod", "color": "lightgreen", "shape": "o", "cpu": 30, "mem": 30, "network": [(9,5,3)]})],
    "pos": {1: [-0.34833021,  0.09425495], 2: [ 0.01927328, -0.07205069], 3: [-0.43677531,  0.66727785], 4: [ 0.50957367, -0.06202244], 5: [0.98649442, 0.24973923], 6: [-0.84259233, -0.21467222], 7: [-0.89098206,  0.34020218], 8: [ 0.00333854, -0.64498511], 9: [ 1, -0.35774376]}
}