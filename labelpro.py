import networkx as nx
import matplotlib.pyplot as plt
import re
import random
from networkx.algorithms.community import modularity
import time

#-------------------
#   METHODES
#-------------------

def load_graph_from_gml(file_path, ind = 0):
    if(ind == 0):
        G = nx.read_gml(file_path)
    else:
        G = nx.read_gml(file_path, label = None)
        for node in G.nodes():
            if'label' not in G.nodes[node]:
                G.nodes[node]['label']=str(node)
    return G 

def draw_colored_graph(G, node_colors):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=node_colors, with_labels=True)
    plt.show()


def label_propagation(G):
    # Initialiser chaque nœud avec un label unique
    labels = {node: node for node in G.nodes()}

    # Générer des couleurs uniques pour chaque étiquette
    label_colors = {label: "#" + "%06x" % random.randint(0, 0xFFFFFF) for label in set(labels.values())}

    # Convertir les étiquettes en couleurs valides
    node_col = [label_colors[labels[node]] for node in G.nodes()]

    draw_colored_graph(G, node_col)

    # Itération 
    t = 1

    # Répéter jusqu'à ce que tous les nœuds aient convergé
    while True:
        # Mélanger les nœuds dans un ordre aléatoire
        nodes = list(G.nodes())
        random.shuffle(nodes)

        # Pour chaque nœud, mettez à jour son label en fonction de la majorité des labels de ses voisins
        converged = True
        for node in nodes:
            neighbor_labels = [labels[neighbor] for neighbor in G.neighbors(node)]
            if neighbor_labels:
                # Compter les occurrences de chaque label parmi les voisins
                label_counts = {label: neighbor_labels.count(label) for label in set(neighbor_labels)}
                # Trouver le label majoritaire
                majority_label = max(label_counts, key=label_counts.get)
                # Mettre à jour le label du nœud actuel s'il est différent du label majoritaire
                if labels[node] != majority_label:
                    labels[node] = majority_label
                    converged = False

        # Vérifier la convergence
        if converged:
            break

        if(t%5==0):
            # Générer des couleurs uniques pour chaque étiquette
            label_colors = {label: "#" + "%06x" % random.randint(0, 0xFFFFFF) for label in set(labels.values())}

            # Convertir les étiquettes en couleurs valides
            node_col = [label_colors[labels[node]] for node in G.nodes()]

            draw_colored_graph(G, node_col)
        t+=1

    print("itérations = ",t)
    return labels

def aggregate_graph(G, labels):
    # Créer un nouveau graphe agrégé
    aggregated_graph = nx.Graph()

    # Ajouter les nœuds agrégés basés sur les labels
    for label in set(labels.values()):
        nodes_with_label = [node for node, lab in labels.items() if lab == label]
        aggregated_graph.add_node(label, nodes=nodes_with_label)

    # Ajouter des arêtes entre les nœuds agrégés basées sur les arêtes du graphe original
    for node in G.nodes():
        for neighbor in G.neighbors(node):
            label_node = labels[node]
            label_neighbor = labels[neighbor]
            if label_node != label_neighbor:
                aggregated_graph.add_edge(label_node, label_neighbor)

    return aggregated_graph


def calculate_modularity(G, partition):
    return nx.community.modularity(G, partition)

#----------------
#   MAIN
#----------------

G = load_graph_from_gml("corr_distance_Plasma-cells.gml",1)
#G = load_graph_from_gml("corr_distance_Macrophages.gml", 1)
#G = load_graph_from_gml("LR_graph_visu-merged.gml")    
#G = load_graph_from_gml("LR_graph_Macrophages_Tcells.gml")
#G = load_graph_from_gml("corr_distance_Macrophages (1).gml",1)
#G = nx.karate_club_graph()

# Définir le nombre d'itérations de l'algorithme de propagation de libellés

start_t = time.time()
labels = label_propagation(G)
end_t = time.time()

# Générer des couleurs uniques pour chaque étiquette
label_colors = {label: "#" + "%06x" % random.randint(0, 0xFFFFFF) for label in set(labels.values())}

# Convertir les étiquettes en couleurs valides
node_col = [label_colors[labels[node]] for node in G.nodes()]

draw_colored_graph(G, node_col)

# Convertir les étiquettes en partition de graphe
partition = {label: [] for label in set(labels.values())}
for node, label in labels.items():
    partition[label].append(node)

# Calculer la modularité en fonction de la partition obtenue
modularity = calculate_modularity(G, partition.values())

print("Modularité du graphe :", modularity)


# Affiche le temps d'exécution de l'algorithme label propagation
execution_time = end_t - start_t

print("Temps d'exécution:", execution_time, "secondes")
