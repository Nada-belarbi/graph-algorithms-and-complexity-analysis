import random
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import heapq
import time
from tabulate import tabulate
from termcolor import colored
class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self.adj_list = {i: [] for i in range(num_vertices)}

    def add_edge(self, u, v, weight):
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices and u != v:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight

            self.adj_list[u].append((v, weight))
            self.adj_list[v].append((u, weight))
    def remove_edge(self, u, v):
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.adj_matrix[u][v] = 0
            self.adj_matrix[v][u] = 0

            self.adj_list[u] = [(vertex, w) for vertex, w in self.adj_list[u] if vertex != v]
            self.adj_list[v] = [(vertex, w) for vertex, w in self.adj_list[v] if vertex != u]

    def add_vertex(self):
        self.num_vertices += 1

        for row in self.adj_matrix:
            row.append(0)
        self.adj_matrix.append([0] * self.num_vertices)

        self.adj_list[self.num_vertices - 1] = []

    def remove_vertex(self, vertex):
        if 0 <= vertex < self.num_vertices:
            self.adj_matrix.pop(vertex)
            for row in self.adj_matrix:
                row.pop(vertex)

            self.adj_list.pop(vertex, None)
            for v, neighbors in self.adj_list.items():
                self.adj_list[v] = [(u, w) for u, w in neighbors if u != vertex]

            self.num_vertices -= 1
            
    def display_internal_representation(self):
        # Display the adjacency matrix
        print("\nMatrice d'adjacence:")
        headers = [f"S{x}" for x in range(self.num_vertices)]
        styled_headers = [colored(h, 'cyan', attrs=['bold']) for h in headers]  # Color headers
        styled_matrix = [[colored(row[j], 'yellow') if j == 0 else row[j] for j in range(len(row))] for i, row in enumerate(self.adj_matrix)]
        print(tabulate(styled_matrix, headers=styled_headers, showindex="always", tablefmt="fancy_grid"))

        # Display the adjacency list
        print("\nListe d'adjacence:")
        formatted_adj_list = [f"Γ({key}) = [{', '.join([f'({v}, {w})' for v, w in values])}]" for key, values in self.adj_list.items()]
        print(tabulate([[item] for item in formatted_adj_list], headers=["Adjacency List"], tablefmt="fancy_grid"))

    def display_A_S_lists(self):
        # Generate A (list of edges with weights)
        A = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.adj_matrix[i][j] != 0:
                    A.append((i, j, self.adj_matrix[i][j]))
        
        # Generate S (list of vertices)
        S = list(self.adj_list.keys())

        # Display formatted A and S
        print("\nA = {", ", ".join([f"({x[0]}, {x[1]}, {x[2]})" for x in A]), "}")
        print("S = {", ", ".join(map(str, S)), "}")

    def display_degrees(self):
        # Calculate degrees
        degrees = {i: len(neighbors) for i, neighbors in self.adj_list.items()}

        # Display the degree table
        print("\nTableau des degrés :")
        degree_table = [[f"Sommet {vertex}", degree] for vertex, degree in degrees.items()]
        print(tabulate(degree_table, headers=["Sommet", "Degré"], tablefmt="fancy_grid"))

    def draw(self):
        G = nx.Graph()

        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.adj_matrix[i][j] != 0:
                    G.add_edge(i, j, weight=self.adj_matrix[i][j])

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
        plt.title("Représentation Graphique du Graphe", fontsize=14)
        plt.show()

def generate_and_display_graph(num_vertices, num_edges, weight_range, is_connected):
    # Vérifier si des poids négatifs sont inclus
    if weight_range[0] < 0:
        print("❌ Erreur : Les poids négatifs ne sont pas compatibles avec l'algorithme de Dijkstra.")
        print("🔹 Veuillez choisir un intervalle de poids positif.")
        return None

    # Calculer le nombre maximal d'arêtes (y compris les boucles)
    max_edges = (num_vertices * (num_vertices + 1)) // 2

    # Vérification que le nombre d'arêtes demandé ne dépasse pas la capacité maximale
    if num_edges > max_edges:
        print(f"❌ Erreur : Le nombre d'arêtes demandé ({num_edges}) dépasse la limite maximale ({max_edges}) pour {num_vertices} sommets.")
        return None

    graph = Graph(num_vertices)
    edges = set()  # Ensemble des arêtes ajoutées (pour éviter les doublons)

    # Si un graphe connexe est requis, on ajoute une structure en chaîne pour garantir la connexion
    if is_connected:
        for i in range(num_vertices - 1):
            weight = random.randint(*weight_range)
            graph.add_edge(i, i + 1, weight)
            edges.add((i, i + 1))

    # Ajouter des arêtes aléatoires (y compris les boucles) jusqu'à atteindre `num_edges`
    while len(edges) < num_edges:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)  # Les boucles sont possibles car u peut être égal à v

        edge = (min(u, v), max(u, v))  # Normalisation pour éviter les doublons
        if edge not in edges:
            weight = random.randint(*weight_range)
            graph.add_edge(u, v, weight)
            edges.add(edge)

    # Affichage des représentations internes
    graph.display_internal_representation()
    graph.display_A_S_lists()
    graph.display_degrees()

    # Dessiner le graphe si le nombre d'arêtes est raisonnable
    if num_edges <= 100:
        graph.draw()
    else:
        print("🔹 La visualisation est désactivée pour les graphes trop denses.")

    return graph

def compare_algorithms(graph, start, dijkstra_naive, dijkstra_optimized):
    # Vérifiez si le graphe est valide
    if graph is None or not isinstance(graph, Graph):
        print("❌ Erreur : Le graphe fourni n'est pas valide. Impossible de comparer les algorithmes.")
        return None, None

    # Vérifier si le sommet `start` existe dans le graphe
    if start not in graph.adj_list:
        print(f"❌ Erreur : Le sommet de départ {start} n'existe pas dans la liste d'adjacence.")
        return None, None

    # Exécution de Dijkstra Naïf
    try:
        start_time = time.perf_counter()
        distances_naive = dijkstra_naive(graph, start)
        naive_time = time.perf_counter() - start_time
    except Exception as e:
        print(f"Erreur dans Dijkstra Naïf : {e}")
        distances_naive, naive_time = None, None

    # Exécution de Dijkstra Optimisé
    try:
        start_time = time.perf_counter()
        distances_optimized = dijkstra_optimized(graph, start)
        optimized_time = time.perf_counter() - start_time
    except Exception as e:
        print(f"Erreur dans Dijkstra Optimisé : {e}")
        distances_optimized, optimized_time = None, None

    # Affichage des résultats
    print("\n🔹 **Comparaison des Algorithmes de Dijkstra**")
    print(f"🔵 Dijkstra Naïf : {naive_time:.6f} secondes")
    print(f"🟢 Dijkstra Optimisé (Tas) : {optimized_time:.6f} secondes")

    if naive_time is not None and optimized_time is not None:
        if naive_time > optimized_time:
            print("✅ L'algorithme optimisé est plus rapide.")
        elif naive_time < optimized_time:
            print("⚡ L'algorithme naïf est plus rapide (peu probable sur des graphes denses).")
        else:
            print("🔄 Les deux algorithmes ont des performances identiques.")

    return naive_time, optimized_time

def compare_algorithms_with_density(dijkstra_naive, dijkstra_optimized, orders, densities, repetitions):
    """
    Compare les performances des deux versions de Dijkstra sur plusieurs graphes de différentes densités.
    
    Parameters:
    - dijkstra_naive: Fonction de l'algorithme de Dijkstra naïf
    - dijkstra_optimized: Fonction de l'algorithme optimisé
    - orders: Liste des ordres (nombre de sommets) des graphes à tester
    - densities: Liste des densités (ratio entre nombre d'arêtes et maximum possible) à tester
    - repetitions: Nombre de graphes à tester pour chaque combinaison ordre-densité

    Returns:
    - Un dictionnaire contenant les temps moyens pour chaque combinaison.
    """
    results = {}

    for order in orders:
        results[order] = {}
        for density in densities:
            naive_times = []
            optimized_times = []

            for _ in range(repetitions):
                # Calcul du nombre maximal d'arêtes
                max_edges = (order * (order - 1)) // 2
                num_edges = int(density * max_edges)

                # Générer un graphe aléatoire
                graph = Graph(order)
                edges = set()
                while len(edges) < num_edges:
                    u = random.randint(0, order - 1)
                    v = random.randint(0, order - 1)
                    if u != v:
                        edge = (min(u, v), max(u, v))
                        if edge not in edges:
                            weight = random.randint(1, 10)  # Poids entre 1 et 10
                            graph.add_edge(u, v, weight)
                            edges.add(edge)

                # Choisir un sommet de départ aléatoire
                start = random.randint(0, order - 1)

                # Mesurer le temps d'exécution de Dijkstra naïf
                start_time = time.perf_counter()
                dijkstra_naive(graph, start)
                naive_times.append(time.perf_counter() - start_time)

                # Mesurer le temps d'exécution de Dijkstra optimisé
                start_time = time.perf_counter()
                dijkstra_optimized(graph, start)
                optimized_times.append(time.perf_counter() - start_time)

            # Calculer les temps moyens pour cette densité
            results[order][density] = {
                "naive": sum(naive_times) / len(naive_times),
                "optimized": sum(optimized_times) / len(optimized_times)
            }

    # Générer des graphiques alignés horizontalement
    fig, axes = plt.subplots(1, len(orders), figsize=(5 * len(orders), 5), constrained_layout=True)

    for idx, order in enumerate(orders):
        ax = axes[idx]
        densities = sorted(results[order].keys())
        naive_times = [results[order][density]["naive"] for density in densities]
        optimized_times = [results[order][density]["optimized"] for density in densities]

        ax.plot(densities, naive_times, label="Naïf", marker='o')
        ax.plot(densities, optimized_times, label="Optimisé (Tas)", marker='o')
        ax.set_title(f"Ordre du Graphe : {order} Sommets")
        ax.set_xlabel("Densité du Graphe")
        ax.set_ylabel("Temps d'exécution (secondes)")
        ax.legend()
        ax.grid()

    plt.suptitle("Comparaison des Algorithmes de Dijkstra pour Différentes Densités", fontsize=16)
    plt.show()

    return results
