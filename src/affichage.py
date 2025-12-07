import tkinter as tk
from tkinter import messagebox, filedialog
import os 
from src.graph_generator import generate_graph 

# --- La fenêtre principale ---
def start_interface():
   # Dictionnaire pour stocker les résultats
   results = {"x": None, "y": None, "z": None,"source":None,"puit":None, "file_name": None}

   window = tk.Tk()
   window.title("Générateur de Graphe")
   window.geometry("800x800") 
   window.config(bg="#17b4db")

   # Variable pour le mode (Générer ou Charger)
   mode_var = tk.IntVar(value=0) # 0 = Générer, 1 = Charger

   def toggle_mode():
      if mode_var.get() == 1:
         # Mode Charger : Désactiver les champs de génération
         entry_nodes.config(state='disabled')
         entry_edges.config(state='disabled')
         entry_flow.config(state='disabled')
         btn_generate.config(text="Charger le Graphe")
      else:
         # Mode Générer : Activer les champs
         entry_nodes.config(state='normal')
         entry_edges.config(state='normal')
         entry_flow.config(state='normal')
         btn_generate.config(text="Générer le Graphe")

   # --- Actions et boutons ---
   def process_action():
      try:
         file_name = entry_filename.get()
         if not file_name.endswith(".txt"):
            file_name += ".txt"
         
         complete_path = os.path.join("data", file_name)

         # On récupère Source et Puits ici pour qu'ils soient disponibles dans les deux modes
         source = int(entry_source.get())
         puit_input = int(entry_puit.get())

         if mode_var.get() == 1: # Mode Charger
            if not os.path.exists(complete_path):
               messagebox.showerror("Erreur", f"Le fichier '{file_name}' n'existe pas dans le dossier data.")
               return
            
            # On considère que le chargement est un succès
            messagebox.showinfo("Succès", f"Fichier '{file_name}' sélectionné.\nSource: {source}, Puits: {puit_input}")
            
            results["file_name"] = file_name
            results["source"] = source
            results["puit"] = puit_input
            # x, y, z restent à None car on charge un fichier existant
            
            window.destroy()

         else: # Mode Générer
            x = int(entry_nodes.get())
            y = int(entry_edges.get())
            z = int(entry_flow.get())
            # source et puit_input sont déjà récupérés plus haut

            os.makedirs("data", exist_ok=True)

            sucess, message = generate_graph(complete_path, x, y, z)

            if sucess:
               messagebox.showinfo("Succès", message)
               # Stocker les valeurs dans le dictionnaire de résultats
               results["x"] = x
               results["y"] = y
               results["z"] = z
               results["source"] = source
               results["puit"] = puit_input
               results["file_name"] = file_name
               # Fermer la fenêtre pour continuer l'exécution et retourner les valeurs
               window.destroy()
            else: 
               messagebox.showinfo("Erreur, lors de la génération", message)

      except ValueError as e: 
         messagebox.showwarning("Attention", f"Vérifiez vos entrées (nombres entiers requis).\nErreur: {str(e)}")
      
      except Exception as e: 
         messagebox.showerror("Erreur Technique", f"Une erreur est survenue :\n{e}")

   # --- Champs et Textes ---

   # Titre
   lbl_title = tk.Label(window, text="Générateur du Graphe", font=("Arial", 14, "bold"), bg="#17b4db")
   lbl_title.pack(pady=10)

   # Checkbox Mode
   chk_mode = tk.Checkbutton(window, text="Utiliser un fichier existant", variable=mode_var, command=toggle_mode, bg="#17b4db", activebackground="#17b4db")
   chk_mode.pack(pady=5)

   # Nombre de Sommets 
   frame_x = tk.Frame(window, bg="#0d738c")
   frame_x.pack(pady=5)
   tk.Label(frame_x, text="Nombre de Sommets:", width=20, anchor='e', bg="#0d738c").pack(side=tk.LEFT)
   entry_nodes = tk.Entry(frame_x)
   entry_nodes.insert(0,"10")
   entry_nodes.pack(side=tk.LEFT)

   # Nombre d'Arêtes
   frame_y = tk.Frame(window, bg="#0d738c")
   frame_y.pack(pady=5)
   tk.Label(frame_y, text="Nombre d'Arêtes:", width=20, anchor='e', bg="#0d738c").pack(side=tk.LEFT)
   entry_edges = tk.Entry(frame_y)
   entry_edges.insert(0,"20")
   entry_edges.pack(side=tk.LEFT)

   # Capacité Maximale
   frame_z = tk.Frame(window, bg="#0d738c")
   frame_z.pack(pady=5)
   tk.Label(frame_z, text="Capacité Maximale:", width=20, anchor='e', bg="#0d738c").pack(side=tk.LEFT)
   entry_flow = tk.Entry(frame_z)
   entry_flow.insert(0,"20")
   entry_flow.pack(side=tk.LEFT)

   # Source et Puits
   frame_sp = tk.Frame(window, bg="#0d738c")
   frame_sp.pack(pady=5)
   tk.Label(frame_sp, text="Source (par défaut 0):", width=20, anchor='e', bg="#0d738c").pack(side=tk.LEFT)
   entry_source = tk.Entry(frame_sp)
   entry_source.insert(0,"0")
   entry_source.pack(side=tk.LEFT)

   frame_p = tk.Frame(window, bg="#0d738c")
   frame_p.pack(pady=5)
   tk.Label(frame_p, text="Puits (par défaut dernier sommet):", width=25, anchor='e', bg="#0d738c").pack(side=tk.LEFT)
   entry_puit = tk.Entry(frame_p)
   entry_puit.insert(0,"9")
   entry_puit.pack(side=tk.LEFT)
   # Nom du Fichier 
   frame_file = tk.Frame(window, bg="#0d738c")
   frame_file.pack(pady=5)
   tk.Label(frame_file, text="Nom du Fichier (data/):", width=20, anchor='e', bg="#0d738c").pack(side=tk.LEFT)
   entry_filename = tk.Entry(frame_file)
   entry_filename.insert(0,"graph.txt")
   entry_filename.pack(side=tk.LEFT)

   # Sources/Puits
   lbl_info = tk.Label(window, text="Note: Source = 0, Puits = Dernier Sommet", fg="gray", bg="#17b4db", font=("Arial", 9, "italic"))
   lbl_info.pack(pady=5)

   # Bouton 
   btn_generate = tk.Button(window, text="Générer le Graphe", command=process_action, bg="#0d738c", fg="white", font=("Arial", 11, "bold"))
   btn_generate.pack(pady=20, ipadx=10)

   window.mainloop()
   
   # Retourner les valeurs après la fermeture de la fenêtre
   return results["x"], results["y"], results["z"], results["source"], results["puit"], results["file_name"]


if __name__ == "__main__":
   # Correction ici : récupération des 6 valeurs retournées
   x, y, z, source, puit, file_name = start_interface()
   
   if file_name is not None:
       if x is not None:
           print(f"Graphe généré: {x} sommets, {y} arêtes, flux max {z}, fichier {file_name}")
           print(f"Source: {source}, Puits: {puit}")
       else:
           print(f"Fichier existant sélectionné: {file_name}")
           print(f"Source définie manuellement: {source}, Puits défini manuellement: {puit}")
