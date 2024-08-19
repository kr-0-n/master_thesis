import conf
import networkx as nx
import k8.scheduler as scheduler 
import visualizer

current_deployment = None
old_graph: nx.Graph = nx.Graph()
graph: nx.Graph = None
def tick(time):
    if current_deployment is not None:
        # check if all pods from the deployment are running
        for pod in current_deployment['pods']:
            if pod[0] not in [node for node in graph.nodes if graph.nodes[node]["type"] == "pod"]:
                print(f"Pod {pod[0]} is not running")
                scheduler.schedule(pod, graph)
                visualizer.draw_graph(graph, "k8")
    return

def setup_graph_from_conf(conf):
    # Create an undirected graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(conf['nodes'])

    # Add edges
    G.add_edges_from(conf['edges'], type="connection")
    return G

def deploy(deployment):
    global current_deployment
    current_deployment = deployment
    return

graph = setup_graph_from_conf(conf.simple_graph)