import networkx as nx
import random
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def generate_random_graph(num_nodes, num_edges):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    return G

def random_walk(graph, start_node, walk_length):
    current_node = start_node
    walk = [current_node]
    for _ in range(walk_length):
        neighbors = list(graph.neighbors(current_node))
        if neighbors:
            current_node = random.choice(neighbors)
            walk.append(current_node)
        else:
            break
    return walk

def detect_communities(graph, num_communities):
    adjacency_matrix = nx.convert_matrix.to_numpy_array(graph)
    kmeans = KMeans(n_clusters=num_communities)
    kmeans.fit(adjacency_matrix)
    return kmeans.labels_

# Generate a random graph
num_nodes = 20
num_edges = 30
G = generate_random_graph(num_nodes, num_edges)

# Draw the original graph without blocking
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, font_weight='bold')
plt.title('Original Graph')
plt.show(block=False)

# Perform random walk on the graph
walk_length = 10
walks = []
for node in G.nodes():
    walk = random_walk(G, node, walk_length)
    walks.extend(walk)

# Create a new graph based on the random walks
G_walks = nx.Graph()
for i in range(len(walks) - 1):
    G_walks.add_edge(walks[i], walks[i+1])

# Perform community detection on the new graph
num_communities = 3
communities = detect_communities(G_walks, num_communities)

# Get node position
node_positions = nx.spring_layout(G)

# Draw the graph with node colors based on communities, using node positions from the original graph
plt.figure(figsize=(8, 6))
nx.draw(G_walks, pos=node_positions, with_labels=True, font_weight='bold', node_color=communities, cmap='viridis')
plt.title('Graph with Communities after Random Walk')
plt.show()

