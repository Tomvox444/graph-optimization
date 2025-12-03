import sys
import time
import os

# Import des modules depuis le dossier src
# Assure-toi d'avoir un fichier vide __init__.py dans le dossier src
from src.graph import Graph
from src.io_manager import read_graph, write_flow
from src.algorithm import edmonds_karp, theorem_menger, analyse_spectrale
from src.visualizer import visualiser_flot

def main():
   # 1. Gestion des arguments en ligne de commande
   if len(sys.argv) < 2:
      print("Usage: python3 main.py <fichier_entree.txt>")
      print("Exemple: python3 main.py data/input.txt")
      sys.exit(1)

   input_file = sys.argv[1]
   
   # On définit le nom du fichier de sortie (ex: input_sol.txt)
   base_name = os.path.splitext(input_file)[0]
   output_file = f"data/output.txt"

   print(f"--- Projet Théorie des Graphes : Flot Maximal ---")
   print(f"[*] Lecture du fichier : {input_file}")

   # 2. Initialisation et Chargement du Graphe
   g = Graph()
   try:
      read_graph(input_file, g)
   except Exception as e:
      print(f"[!] Erreur critique lors de la lecture : {e}")
      sys.exit(1)

   # 3. Détermination automatique de la Source et du Puits
   # HYPOTHÈSE : Dans ce type de projet, souvent :
   # - La Source (S) est le sommet avec le plus petit ID (souvent 0 ou 1)
   # - Le Puits (T) est le sommet avec le plus grand ID
   # (Tu pourras modifier ça si le sujet précise autre chose)
   sommets = g.get_all_vertices()
   if not sommets:
      print("[!] Le graphe est vide.")
      sys.exit(1)
      
   source = min(sommets)
   puits = max(sommets)
   
   print(f"[*] Graphe chargé : {len(sommets)} sommets.")
   print(f"[*] Configuration détectée -> Source: {source}, Puits: {puits}")

   # 4. Exécution de l'algorithme (avec chronomètre)
   print(f"[*] Lancement de l'algorithme Edmonds-Karp...")
   start_time = time.time()
   
   max_flow_value = edmonds_karp(g, source, puits)
   
   end_time = time.time()
   duree = end_time - start_time

   # 5. Affichage des résultats console
   print(f"--- RÉSULTATS ---")
   print(f"Flot Maximal trouvé : {max_flow_value}")
   print(f"Temps d'exécution   : {duree:.6f} secondes")
   print(f"[*] Analyse de Menger :")
   k = theorem_menger(g, source, puits)
   print(f"   -> Il existe {k} chemins arête-disjoints entre {source} et {puits}.")
   print(f"[*] Analyse Spectrale (Valeur de Fiedler) :")
   fiedler_value = analyse_spectrale(g)
   if fiedler_value is not None:
      print(f"   -> Valeur de Fiedler : {fiedler_value:.6f}")
   else:
      print("   -> numpy non installé, analyse spectrale ignorée.")

   # 6. Écriture du fichier de solution
   try:
      write_flow(output_file, g)
      print(f"[*] Solution sauvegardée dans : {output_file}")
   except Exception as e:
      print(f"[!] Erreur lors de l'écriture du fichier : {e}")
   # 7. Visualisation (optionnelle)
   try:
      visualiser_flot(g, file_name="flow_solution.html")
   except Exception as e:
      print(f"[!] Erreur lors de la visualisation : {e}")

if __name__ == "__main__":
   main()