import networkx as nx
import visualizer
def get_assigned_node_id(graph: nx.Graph, pod_id: int) -> dict:
    """
    Get the node that the pod is assigned to.

    Parameters
    ----------
    graph : nx.Graph
        The graph to search for the assignment
    pod : dict
        The pod to search for

    Returns
    -------
    dict
        The node id that the pod is assigned to, or None if the pod is not assigned
    """
    pod = graph.nodes[pod_id]
    if pod["type"] != "pod": raise Exception("Pod is not a pod")
    assigned_nodes = [neighbor for neighbor in graph.neighbors(pod_id) if graph.nodes[neighbor]["type"] == "node"]
  
    if len(assigned_nodes) > 1: raise Exception("Pod is assigned to more than one node")
    if len(assigned_nodes) == 1: return assigned_nodes[0]
    if len(assigned_nodes) == 0: return None

def get_pod_ids(graph: nx.Graph):
    """
    Get a list of all pod ids in the graph.

    Parameters
    ----------
    graph : nx.Graph
        The graph to search for pods

    Returns
    -------
    list
        A list of all pod ids in the graph
    """
    return [node for node in graph.nodes if graph.nodes[node]["type"] == "pod"]

def get_node_ids(graph: nx.Graph):
    """
    Get a list of all node ids in the graph.

    Parameters
    ----------
    graph : nx.Graph
        The graph to search for nodes

    Returns
    -------
    list
        A list of all node ids in the graph
    """
    return [node for node in graph.nodes if graph.nodes[node]["type"] == "node"]


def get_assigned_pod_ids(graph: nx.DiGraph, node_id: int) -> list:
    """
    Get a list of pod ids assigned to a particular node.

    Parameters
    ----------
    graph : nx.DiGraph
        The directed graph to search for assigned pods.
    node_id : int
        The id of the node to find the assigned pods for.

    Returns
    -------
    list
        A list of pod ids that are assigned to the specified node.
    """

    return [ pod for pod in graph.predecessors(node_id) if graph.nodes[pod]["type"] == "pod" ]
