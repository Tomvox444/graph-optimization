import random 

def generate_graph(filename, nb_nodes, nb_edges, flow_max):
   """
   Génère un graphe aléatoire et le sauvegarde dans un fichier.
   filename : nom du fichier de sortie
   nb_nodes : nombre total de sommets 
   nb_edges : nombre d'arêtes à créer
   flow_max : capacité maximale d'une arête
   """
   max_edges = nb_nodes * (nb_nodes -1)
   if nb_edges > max_edges:
      raise ValueError(f"Trop d'arêtes! Le maximum est {max_edges}.")
      nb_edges = max_edges

   exist_edges = set()
   edges = []
      
   count = 0 
   while count < nb_edges: 
      u = random.randint (0, nb_nodes -1)
      v = random.randint (0, nb_nodes -1)
         
      if u != v and (u,v) not in exist_edges: 
         capacity = random.randint (1, flow_max)

         exist_edges.add((u, v))
         edges.append(f"{u} {v} {capacity}\n")
         count += 1 

   try:
      with open(filename, "w") as f: 
         f.writelines(edges)
      return True, f"Graphe généré avec succès : {filename}"
   except Exception as e: 
      return False, str(e)