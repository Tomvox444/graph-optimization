import sys
import time
import os

# Import des modules depuis le dossier src
# Assure-toi d'avoir un fichier vide __init__.py dans le dossier src
from src.graph import Graph
from src.io_manager import read_graph, write_flow
from src.algorithm import edmonds_karp, theorem_menger, analyse_spectrale
from src.visualizer import visualiser_flot
from src.affichage import start_interface

def main():
   # 1. Interface Utilisateur pour les paramètres d'entrée
   _, _, _, source, puits, input_file = start_interface()

   input_file = os.path.join("data", input_file)
   
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

   try:
      visualiser_flot(g, source, puits, file_name="initial_graph.html")
   except Exception as e:
      print(f"[!] Erreur lors de la visualisation : {e}")

   # 3. Vérification du graphe
   sommets = g.get_all_vertices()
   if not sommets:
      print("[!] Le graphe est vide.")
      sys.exit(1)


   
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
      visualiser_flot(g, source, puits, file_name="flow_solution.html")
   except Exception as e:
      print(f"[!] Erreur lors de la visualisation : {e}")

if __name__ == "__main__":
   main()