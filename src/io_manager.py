def read_graph(file_path, graph_obj):
   with open(file_path, 'r') as f:
      lines = f.readlines()

   line_count = 0
   for line in lines:
      line_count += 1
      parts = line.strip().split()
      
      # Ignorer les lignes vides ou les commentaires
      if not parts or parts[0].startswith('#'):
         continue
         
      if len(parts) != 3:
         raise ValueError(f"Ligne {line_count} invalide : format attendu 'u v cap'")
         
      try:
         # On tente de convertir en entiers, mais on garde des strings si besoin
         # Si tes sommets sont des lettres "A", "B", retire les int() pour u et v
         u = int(parts[0]) 
         v = int(parts[1])
         cap = int(parts[2])
         
         if cap < 0:
            raise ValueError(f"Capacité négative à la ligne {line_count}")
            
         graph_obj.add_edge(u, v, cap)
         
      except ValueError as e:
         raise ValueError(f"Erreur de données ligne {line_count}: {e}")

def write_flow(file_path, graph):
   with open(file_path, 'w') as file:
      for u in graph.get_all_vertices():
         for v in graph.get_neighbors(u):
            cap, flow = graph.adj[u][v]
            if cap > 0 and flow>=0:  # On n'écrit que les arcs avec une capacité positive et un flow >= 0
               file.write(f"{u} {v} {flow}\n")
