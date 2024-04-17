# -*- coding: utf-8 -*-

import json
import networkx as nx
import random
import matplotlib.pyplot as plt

def calculate_modularity(G, partition):
    modularity = 0
    m = sum(weight for _, _, weight in G.edges.data('weight', default=1))  # Somme des poids des arêtes
    for community in set(partition.values()):
        nodes_in_community = [node for node, comm in partition.items() if comm == community]
        for node_i in nodes_in_community:
            for node_j in nodes_in_community:
                if G.has_edge(node_i, node_j):
                    A_ij = G[node_i][node_j]['weight'] if 'weight' in G[node_i][node_j] else 1
                else:
                    A_ij = 0
                ki = G.degree(node_i)
                kj = G.degree(node_j)
                modularity += (A_ij - (ki * kj) / m)
    modularity /= m
    return modularity

def find_best_community(G, node, partition):
    best_community = partition[node]
    best_modularity = calculate_modularity(G, partition)
    neighbors = list(G.neighbors(node))
    random.shuffle(neighbors)
    for neighbor in neighbors:
        current_partition = partition.copy()
        current_partition[node] = current_partition[neighbor]
        current_partition_modularity = calculate_modularity(G, current_partition)
        if current_partition_modularity > best_modularity:
            best_modularity = current_partition_modularity
            best_community = current_partition[node]
    return best_community

def louvain(G):
    partition = {node: node for node in G.nodes()}  
    improved = True
    while improved:
        improved = False
        nodes = list(G.nodes())
        random.shuffle(nodes)
        for node in nodes:
            current_community = partition[node]
            best_community = find_best_community(G, node, partition)
            if best_community != current_community:
                partition[node] = best_community
                improved = True
    return partition

with open('file.json', 'r') as f:
    graph_data = json.load(f)

G = nx.node_link_graph(graph_data)

partition = louvain(G)
print(partition)

colors = [partition[node] for node in G.nodes()]
plt.figure(figsize=(8, 6))
nx.draw(G, with_labels=True, font_weight='bold', node_color=colors, cmap='viridis')
plt.title('Graph with Communities after Random Walk')
plt.show()


