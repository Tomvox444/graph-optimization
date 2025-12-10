from pyvis.network import Network
from math import log
import sys

def get_color_and_width(flow, capacity):
    """Calcule la couleur et l'épaisseur de l'arête en fonction du taux de saturation."""
    if flow > 0:
        flow_magnitude = flow
    else:
        flow_magnitude = 0
    
    if capacity <= 0:
        # Arcs fantômes ou sans capacité réelle
        return "#AAAAAA", 0.5, 0.0
        
    saturation = flow / capacity
    
    # Largeur basée sur le log pour ne pas avoir des lignes trop épaisses
    width = max(1, log(flow_magnitude + 1) * 2)
        
    # Détermination de la couleur (Arc-en-ciel progressif)
    # Saturation 0% -> Bleu (Hue ~240)
    # Saturation 100% -> Rouge (Hue 0)
    
    # On clamp la saturation entre 0 et 1 pour le calcul de couleur
    sat_clamped = max(0.0, min(1.0, saturation))
    
    # Interpolation linéaire inversée : 0 -> 240 (Bleu), 1 -> 0 (Rouge)
    hue = int(240 * (1 - sat_clamped))
    
    # Conversion HSL vers Hex string simple
    # On utilise une saturation de couleur de 100% et une luminosité de 50%
    color = f"hsl({hue}, 100%, 50%)"
            
    return color, width, saturation

def visualiser_flot(graph_obj, source, puit, file_name="flow_solution.html"):
    """
    Génère une visualisation HTML interactive du réseau de flot final (PyVis).
    Optimisé pour tenter de contourner les problèmes de rendu local.
    """
    
    # 1. Configuration de PyVis
    net = Network(height="750px", width="100%", 
                  bgcolor="#222222", 
                  font_color="white", 
                  directed=True)
    
    # On ajoute des options de stabilisation pour que le graphe ne s'échappe pas
    # hors de l'écran, ce qui donne l'effet "écran noir".
    # net.set_options(...)
    # net.set_options(...)
    net.set_options("""
    {
      "nodes": {
        "size": 10
      },
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08,
          "damping": 0.4,
          "avoidOverlap": 0.5
        },
        "maxVelocity": 50,
        "minVelocity": 0.1,
        "timestep": 0.35,
        "stabilization": {
          "enabled": true,
          "iterations": 1000,
          "updateInterval": 25,
          "onlyDynamicEdges": false,
          "fit": true
        }
      },
      "configure": {
        "enabled": false
      }
    }
    """)
    # 2. Traitement des arcs et nœuds
    
    # Pré-chargement de tous les noeuds pour éviter l'erreur "non existent node"
    all_nodes = set()
    for u in graph_obj.adj:
        all_nodes.add(u)
        for v in graph_obj.adj[u]:
            all_nodes.add(v)
            


    for n in all_nodes:
        # Par défaut
        color_node = "#97C2FC" # Bleu clair par défaut de PyVis
        size_node = 10
        label_node = f"{n}"

        if n == source:
            color_node = "#00FF00" # Vert
            size_node = 25
            label_node = f"Source ({n})"
        elif n == puit:
            color_node = "#FF0000" # Rouge
            size_node = 25
            label_node = f"Puits ({n})"

        net.add_node(n, label=label_node, title=f"Noeud {n}", color=color_node, size=size_node)

    for u in graph_obj.adj:
        for v, data in graph_obj.adj[u].items():
            cap, flow = data
            if file_name == "initial_graph.html":
                flow = 1 # Pour la visualisation initiale, on met le flot à 100% de la capacité
            
            # FILTRE : On n'affiche que les arcs qui avaient une capacité réelle OU qui transportent du flux.
            if cap > 0 and flow > 0: 
                
                # Récupération des attributs de style
                color, width, _ = get_color_and_width(flow, cap)
                
                # --- Ne dessiner que si la saturation n'est pas 0 (pour ne pas surcharger) ---
                if width > 0.5:
                    
                    # Label pour l'interactivité (survol)
                    if cap > 0:
                        label_text = f"{flow}/{cap} ({flow/cap:.0%})"
                    else:
                         # Si cap=0 mais flow > 0, on affiche juste le flow net
                        label_text = f"Flot net: {flow}" 

                    # Ajout de l'arête
                    net.add_edge(u, v, 
                                 title=label_text, 
                                 value=width, # 'value' est utilisé par PyVis pour la taille/épaisseur
                                 color=color,
                                 font={'color': 'white'}
                                )
    try:
        # Si le graphe est trop grand, la stabilisation prend beaucoup de temps
        # Nous allons forcer le fit pour qu'il apparaisse à l'écran
        net.save_graph(file_name)
        print(f" Visualisation interactive générée : {file_name}")
        print(" NOTE: Si l'écran est noir, attendez quelques secondes pour que la physique se stabilise, ou ouvrez le fichier avec Firefox.")
        
    except Exception as e:
        print(f"Erreur lors de la génération du HTML : {e}")

if __name__ == "__main__":
    print("Ce module est une librairie et doit être appelé par main.py.")
    sys.exit(0)