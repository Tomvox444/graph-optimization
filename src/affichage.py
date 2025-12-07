import tkinter as tk
from tkinter import messagebox, filedialog
import os 
from graph_generator import generate_graph 

# --- La fenêtre principale ---
def start_interface():

   window = tk.Tk()
   window.title("Générateur de Graphe")
   window.geometry("400x350")
   window.config(bg="#17b4db")

   # --- Actions et boutons ---
   def generate():
      try:
         x = int(entry_nodes.get())
         y = int(entry_edges.get())
         z = int(entry_flow.get())
         file_name = entry_filename.get()

         if not file_name.endswith(".txt"):
            file_name += ".txt"

         complete_path = os.path.join("data", file_name)
         os.makedirs("data", exist_ok=True)

         sucess, message = generate_graph(complete_path, x, y, z)

         if sucess:
            messagebox.showinfo("Succès", message)
         else: 
            messagebox.showinfo("Erreur, lors de la génération", message)

      except ValueError as e: 
         messagebox.showwarning("Attention", str(e))
      
      except Exception as e: 
         messagebox.showerror("Erreur Technique", f"Une erreur est survenue :\n{e}")

   # --- Champs et Textes ---

   # Titre
   lbl_title = tk.Label(window, text="Générateur du Graphe", font=("Arial", 14, "bold"), bg="#17b4db")
   lbl_title.pack(pady=10)

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

   # Nom du Fichier 
   frame_file = tk.Frame(window, bg="#0d738c")
   frame_file.pack(pady=5)
   tk.Label(frame_file, text="Nom du Fichier:", width=20, anchor='e', bg="#0d738c").pack(side=tk.LEFT)
   entry_filename = tk.Entry(frame_file)
   entry_filename.insert(0,"graph.txt")
   entry_filename.pack(side=tk.LEFT)

   # Sources/Puits
   lbl_info = tk.Label(window, text="Note: Source = 0, Puits = Dernier Sommet", fg="gray", bg="#17b4db", font=("Arial", 9, "italic"))
   lbl_info.pack(pady=5)

   # Bouton 
   btn_generate = tk.Button(window, text="Générer le Graphe", command=generate, bg="#0d738c", fg="white", font=("Arial", 11, "bold"))
   btn_generate.pack(pady=20, ipadx=10)

   window.mainloop()

if __name__ == "__main__":
   start_interface()
