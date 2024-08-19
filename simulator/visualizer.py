import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph,  title, graph_data=None):
    if graph_data != None and len([node for node in graph.nodes if graph.nodes[node]["type"] == "node"]) == 4 and len([node for node in graph.nodes if graph.nodes[node]["type"] == "pod"]) <= 5:
        pos=graph_data['pos']
    else:
        pos = nx.spring_layout(graph)
    for pod in graph.nodes:
        if graph.nodes[pod]["type"] == "pod":
            for connection in graph.nodes[pod]["network"]:
                if graph.has_node(connection[0]):
                    graph.add_edge(pod, connection[0], latency=connection[1], throughput=connection[2], type="wanted_connection")
    nx.draw_networkx_nodes([node for node in graph.nodes if graph.nodes[node]['type']=='node'], pos=pos, node_color=[graph.nodes[node]['color'] for node in graph.nodes if graph.nodes[node]["type"]=="node"], node_size=1500, node_shape="s")
    nx.draw_networkx_nodes([node for node in graph.nodes if graph.nodes[node]['type']=='pod'], pos=pos, node_color=[graph.nodes[node]['color'] for node in graph.nodes if graph.nodes[node]["type"]=="pod"], node_size=1500, node_shape="o")
    nx.draw_networkx_labels(graph, pos=pos, font_size=16, font_color='black', font_weight='bold')
    nx.draw_networkx_edges(graph, edgelist=[edge for edge in graph.edges if "type" in graph.edges[edge] and graph.edges[edge]["type"] == "wanted_connection"], pos=pos, alpha=0.5, edge_color="green")
    nx.draw_networkx_edge_labels(graph, pos=pos, font_size=8, font_color='black', edge_labels={edge:str(graph.edges[edge]["latency"]) +"ms," + str(graph.edges[edge]["throughput"]) + "mbps" for edge in graph.edges if "type" in graph.edges[edge] and graph.edges[edge]["type"]=="wanted_connection"})

    nx.draw_networkx_edges(graph, edgelist=[edge for edge in graph.edges if "type" in graph.edges[edge] and graph.edges[edge]["type"] == "connection" ], pos=pos, alpha=0.5, edge_color="black")
    nx.draw_networkx_edge_labels(graph, pos=pos, font_size=8, font_color='black', edge_labels={edge:str(graph.edges[edge]["latency"]) +"ms," + str(graph.edges[edge]["throughput"]) + "mbps" for edge in graph.edges if "type" in graph.edges[edge] and graph.edges[edge]["type"]=="connection" and "latency" in graph.edges[edge] and "throughput" in graph.edges[edge]})
    
    nx.draw_networkx_edges(graph, edgelist=[edge for edge in graph.edges if "type" in graph.edges[edge] and graph.edges[edge]["type"] == "assign" ], pos=pos, alpha=0.5, edge_color="black")

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()