import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import modularity
import random


# Define function to load graph
def load(file_path):
    G = nx.read_gml(file_path, label="id")
    return G


# Define function to perform random walk
def random_walk(G, node, length):
    path = [node]
    for _ in range(length):
        neighbors = list(G.neighbors(node))
        if neighbors:
            node = random.choice(neighbors)
            path.append(node)
        else:
            break
    return path


# Define function to calculate similarity between nodes based on random walks
def calculate_similarity(G, node1, node2, length):
    path1 = random_walk(G, node1, length)
    path2 = random_walk(G, node2, length)
    intersection = len(set(path1) & set(path2))
    return intersection / length  # Normalize similarity to [0, 1]


# Define Walktrap algorithm
def walktrap(G, length, similarity_threshold, merging_threshold):
    best_modularity = float('-inf')
    best_communities = []
    best_walk_length = None
    best_similarity_threshold = None

    for walk_length in range(5, length + 1):
        for sim_threshold in range(1, int(similarity_threshold * 10) + 1):
            for merge_threshold in range(1, int(merging_threshold * 10) + 1):
                communities = []
                for node in G.nodes():
                    found = False
                    for community in communities:
                        if any(calculate_similarity(G, node, n, walk_length) > sim_threshold / 10 for n in community):
                            community.append(node)
                            found = True
                            break
                    if not found:
                        communities.append([node])

                modularity_value = modularity(G, communities)
                if modularity_value > best_modularity:
                    best_modularity = modularity_value
                    best_communities = communities
                    best_walk_length = walk_length
                    best_similarity_threshold = sim_threshold / 10

    return best_communities, best_walk_length, best_similarity_threshold


# Load the graph
file_path = 'LR_graph_Macrophages_Tcells.gml'
G = load(file_path)

# Apply Walktrap algorithm to detect communities
communities, best_walk_length, best_similarity_threshold = walktrap(G, length=10, similarity_threshold=0.5,
                                                                    merging_threshold=0.5)

# Create a color map for nodes based on community

# Créer une map de couleurs pour chaque communauté
color_map = {}
for i, community in enumerate(communities):
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    for node in community:
        color_map[node] = color
# Dessiner le graphe
pos = nx.spring_layout(G)
for community in communities:
    nx.draw_networkx_nodes(G, pos, nodelist=community, node_color=color_map[list(community)[0]])
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos)
plt.show()

# Calculate modularity
modularity_value = modularity(G, communities)
print("Modularity:", modularity_value)
print("Best Walk Length:", best_walk_length)
print("Best Similarity Threshold:", best_similarity_threshold)
