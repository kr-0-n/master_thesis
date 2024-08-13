import matplotlib.pyplot as plt
import networkx as nx

# Create an undirected graph
G = nx.Graph()

# Add nodes
G.add_nodes_from([1, 2, 3, 4])

# Add edges
G.add_edges_from([(1, 2), (1, 3), (2, 4)])

# Draw the graph
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, font_size=16, font_color='black', font_weight='bold')
plt.title("Undirected Graph")
plt.show()


G.remove_node(1)

nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, font_size=16, font_color='black', font_weight='bold')
plt.title("Undirected Graph")
plt.show()