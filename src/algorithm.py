# src/algorithms.py
from collections import deque
import copy
import numpy as np  

# --- 1. OUTILS DE BASE (BFS) ---

def bfs_find_path(graph, source, sink):
    """Cherche un chemin dans le graphe résiduel (capacité > 0)."""
    queue = deque([source])
    parent = {source: None}
    
    while queue:
        u = queue.popleft()
        if u == sink:
            return parent
        
        for v in graph.get_neighbors(u):
            if v not in parent and graph.get_residual_capacity(u, v) > 0:
                parent[v] = u
                queue.append(v)
    return None

# --- 2. ALGORITHME PRINCIPAL (FLOT MAX) ---

def edmonds_karp(graph, source, sink):
    """Implémentation de Ford-Fulkerson avec BFS (Edmonds-Karp)."""
    max_flow = 0
    while True:
        parent_map = bfs_find_path(graph, source, sink)
        if not parent_map:
            break
            
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent_map[v]
            path_flow = min(path_flow, graph.get_residual_capacity(u, v))
            v = u
            
        v = sink
        while v != source:
            u = parent_map[v]
            graph.augment_flow(u, v, path_flow)
            v = u
            
        max_flow += path_flow
    return max_flow

# --- 3. EXTENSION THÉORIQUE (MENGER) ---

def theorem_menger(graph_original, source, sink):
    """
    Calcule le nombre de chemins arête-disjoints (Théorème de Menger).
    Principe : On met toutes les capacités à 1 et on calcule le flot max.
    """
    # On travaille sur une copie pour ne pas détruire le graphe original
    g_copy = copy.deepcopy(graph_original)
    
    # Transformation : Toutes les capacités deviennent 1
    for u in g_copy.adj:
        for v in g_copy.adj[u]:
            if g_copy.adj[u][v][0] > 0: # Si c'est un vrai arc
                g_copy.adj[u][v][0] = 1
                g_copy.adj[u][v][1] = 0 # Reset du flux
                
    return edmonds_karp(g_copy, source, sink)

# --- 4. ANALYSE SPECTRALE  ---

def analyse_spectrale(graph):
    """
    Calcule la connectivité algébrique (Valeur de Fiedler).
    Si numpy n'est pas installé, retourne None.
    """

    vertices = sorted(graph.get_all_vertices())
    n = len(vertices)
    mapping = {v: i for i, v in enumerate(vertices)}
    
    # Construction du Laplacien L = D - A
    L = np.zeros((n, n))
    
    # On remplit d'abord l'adjacence et les degrés
    for u in vertices:
        d_u = 0
        for v in graph.get_neighbors(u):
            # On considère le graphe comme non-orienté pour la robustesse structurelle
            cap, _ = graph.adj[u][v]
            if cap > 0:
                i, j = mapping[u], mapping[v]
                L[i][j] = -1
                d_u += 1
        L[mapping[u]][mapping[u]] = d_u

    # Calcul des valeurs propres
    vals = np.linalg.eigvalsh(L)
    vals.sort()
    # La valeur de Fiedler est la 2ème plus petite valeur propre
    if vals[1] < 1e-10:
        return 0  # Graphes déconnectés ou quasi-déconnectés
    
    
    return vals[1] if len(vals) > 1 else 0