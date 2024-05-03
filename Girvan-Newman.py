# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:00:07 2024

@author: nduck
"""

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman
import networkx.algorithms.community as nx_comm
import random



# Fonction pour charger un fichier GML et attribuer un label aux nœuds s'il manque
def load_gml(file_path):
    G = nx.read_gml(file_path, label='id') #ajouter label = 'id' en cas de manque label dans l
    return G

def graph_init(G,pos):
    
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue')  # Default color for all nodes
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos)
    plt.title('Graphe initial')
    plt.show()
    
def optimal_communities_girvan_newman(G):
    communities_generator = girvan_newman(G)
    previous_modularity = 0
    optimal_num = 0
    step = 0
    
    for communities in communities_generator:
        step += 1
        # Calcul de la modularité pour cette partition
        modularity = nx_comm.modularity(G, communities)
        print(f"Step {step}: Modularité = {modularity}")
        
        # Vérifier si la modularité commence à diminuer
        if modularity > previous_modularity:
            previous_modularity = modularity
            optimal_num = step
        else:
            break  # Sortir dès que la modularité diminue

    return optimal_num

def apply_girvan_newman_to_optimal(G, optimal_communities):
    communities_generator = girvan_newman(G)
    for _ in range(optimal_communities - 1):
        next(communities_generator)  # Continuer jusqu'à l'avant-dernière scission
    final_communities = next(communities_generator)  # Obtenez les communautés à l'étape optimale

    return final_communities

def plot_communities(G, communities):
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
    


# Charger le graphe et appliquer la fonction
G = nx.read_gml("LR_graph_Macrophages_Tcells.gml", label ='id')
#G = nx.karate_club_graph()
optimal_number_of_communities = optimal_communities_girvan_newman(G)
print("Nombre optimal de communautés :", optimal_number_of_communities)


final_communities = apply_girvan_newman_to_optimal(G, optimal_number_of_communities)
print("Communautés finales obtenues :")
for i, community in enumerate(final_communities, 1):
    print(f"Communauté {i}: {community}")
    
#plot_communities(G, final_communities)


def girvan_newman_persistent_color_communities(G, optimal_steps):
    # Copier le graphe lu pour rester sur le même graphe
    copied_graph = G.copy()
    communities_generator = girvan_newman(copied_graph)
    steps = 0
    #Les couleurs que j'ai choisi pour le graph "LR_graph_Macrophages_Tcells"
    color_map = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3', '#FF1493', '#1E90FF', '#32CD32']

    community_color_map = {}
    next_color_index = 0

    pos = nx.spring_layout(G)  
    graph_init(G, pos)
    for communities in communities_generator:
        steps += 1
        if steps > optimal_steps:
            break  # Arrêter quand on touche l'étape optimale

        #Apres chaque étape, on recalcule la centralité intermédiaires pour les arrêtes restants
        betweenness = nx.edge_betweenness_centrality(copied_graph)

        # Supprimer l'arrêt ayant le plus grand centralité intermédiaires
        edge_to_remove = max(betweenness, key=betweenness.get)
        copied_graph.remove_edge(*edge_to_remove)

        # Mettre à jour les couleurs si une autre communauté trouvée 
        new_community_map = {frozenset(community): i for i, community in enumerate(communities)}
        for community in communities:
            community_frozen = frozenset(community)
            if community_frozen not in community_color_map:
                community_color_map[community_frozen] = color_map[next_color_index % len(color_map)]
                next_color_index += 1

        node_colors = {}
        for community in communities:
            community_color = community_color_map[frozenset(community)]
            for node in community:
                node_colors[node] = community_color

        #Afficher le graphe
        plt.figure(figsize=(10, 10))
        nx.draw_networkx_nodes(G, pos, node_color=[node_colors[node] for node in G.nodes()])
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        nx.draw_networkx_labels(G, pos)
        plt.title(f'Étape {steps}: Communaute après avoir supprimé sommet {edge_to_remove}')
        plt.show()
        
#plot_communities(G, final_communities)
girvan_newman_persistent_color_communities(G, optimal_number_of_communities)
    


