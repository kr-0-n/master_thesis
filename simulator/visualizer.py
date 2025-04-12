import networkx as nx
import matplotlib.pyplot as plt

graph_styles = {
    "node": {
        "shape": "rect",
        "colorscheme": "blues3",
        "style": "filled",
        "color": "2",
        "fillcolor": "1"
    },
    "pod": {
         "shape": "ellipse",
        "colorscheme": "greens3",
        "style": "filled",
        "color": "2",
        "fillcolor": "1"
    }
}

def vertex_styles(kind):
    return graph_styles[kind]

def edge_styles(kind, link):
    if kind == "wanted_connection":
        return {"label": str(link["latency"]) + "ms " + str(link["throughput"]) + "mbps", "weight": 1}
    elif kind == "connection":
        max_line_width = 3
        min_line_width = 0.5
        max_link_throughput = 500
        width = (link["throughput"]/max_link_throughput)*(max_line_width-min_line_width)+min_line_width

        overload = 0
        if "wanted_service" in link:
            for wanted_connection in list(link["wanted_service"].values()):
                if wanted_connection.m > link["service"].m:
                    overload += (wanted_connection.m - link["service"].m)/link["service"].m
        overload = min(overload, 100)/100
        return {"label": str(link["latency"]) + "ms " + str(link["throughput"]) + "mbps", "weight": 100*(1/link["latency"]), "penwidth": width, "color": "#{:02x}0000".format(int(overload*255)) }
    elif kind == "assign":
        return {"len": 0.2}

def draw_graph(graph,  title, graph_data=None):
    for pod in graph.nodes:
        if graph.nodes[pod]["type"] == "pod":
            for connection in graph.nodes[pod]["network"]:
                if graph.has_node(connection[0]):
                    graph.add_edge(pod, connection[0], latency=connection[1], throughput=connection[2], type="wanted_connection")
    biggest_node = max([node for node in graph.nodes if graph.nodes[node]["type"] == "node"], key=lambda x: graph.nodes[x]["cpu"] + graph.nodes[x]["mem"])
    biggest_node = graph.nodes[biggest_node]["cpu"] + graph.nodes[biggest_node]["mem"]  
    max_allowed_size = 1.5
    for node in graph.nodes:
        if graph.nodes[node]["type"] == "node":
            graph.nodes[node].update(graph_styles["node"])
            size = graph.nodes[node]["cpu"] + graph.nodes[node]["mem"]
            graph.nodes[node]["width"] = max_allowed_size*(size/biggest_node)
            graph.nodes[node]["height"] = (max_allowed_size*(size/biggest_node))/2
        if graph.nodes[node]["type"] == "pod":
            graph.nodes[node].update(graph_styles["pod"])
    
    for edge in graph.edges:
        if "type" in graph.edges[edge] and graph.edges[edge]["type"] == "wanted_connection":
            graph.edges[edge].update(edge_styles("wanted_connection", graph.edges[edge]))
        if "type" in graph.edges[edge] and graph.edges[edge]["type"] == "connection":
            graph.edges[edge].update(edge_styles("connection", graph.edges[edge]))
        if "type" in graph.edges[edge] and graph.edges[edge]["type"] == "assign":
            graph.edges[edge].update(edge_styles("assign", graph.edges[edge]))
    
    nx.drawing.nx_pydot.write_dot(graph, "graph.dot")
