class Graph:
    """
    Classe représentant un réseau de transport pour le calcul de Flot Maximal.
    Implémentation par liste d'adjacence (Dictionnaire de Dictionnaires).
    """

    def __init__(self):
        # Structure principale : self.adj[u][v] = [Capacité, Flot]
        # u : Sommet de départ
        # v : Sommet d'arrivée
        # [0] : Capacité Maximale (C)
        # [1] : Flot Actuel (F)
        self.adj = {}

    def add_vertex(self, u):
        """Ajoute un sommet au graphe s'il n'existe pas encore."""
        if u not in self.adj:
            self.adj[u] = {}

    def add_edge(self, u, v, capacity):
        """
        Ajoute un arc orienté u -> v avec une capacité donnée.
        Gère automatiquement la création de l'arc retour (v -> u) pour le graphe résiduel.
        """
        # 1. On s'assure que les sommets existent dans le dictionnaire
        self.add_vertex(u)
        self.add_vertex(v)

        # 2. Ajout de l'arc ALLER (u -> v) - Le "Vrai" tuyau
        # Si l'arc existait déjà (ex: créé comme arc retour par un autre ajout),
        # on met à jour sa capacité réelle.
        if v in self.adj[u]:
            self.adj[u][v][0] = capacity
        else:
            self.adj[u][v] = [capacity, 0]  # [Capacité, Flot initial]

        # 3. Ajout de l'arc RETOUR (v -> u) - L'arc "Fantôme"
        # Nécessaire pour l'algorithme d'Edmonds-Karp (pour "annuler" du flux).
        # Sa capacité est 0 car il n'existe pas physiquement.
        # On ne le crée que s'il n'existe pas déjà (pour ne pas écraser un vrai arc v->u).
        if u not in self.adj[v]:
            self.adj[v][u] = [0, 0]

    def get_residual_capacity(self, u, v):
        """
        Renvoie la capacité résiduelle d'un arc u -> v.
        C'est la quantité de flux qu'on peut ENCORE pousser.
        Formule : Capacité Max - Flot Actuel
        """
        if u in self.adj and v in self.adj[u]:
            cap, flow = self.adj[u][v]
            return cap - flow
        return 0

    def augment_flow(self, u, v, amount):
        """
        Met à jour le flot sur l'arc u -> v et son inverse v -> u.
        C'est le cœur de la mise à jour du graphe résiduel.
        """
        # On ajoute du flux dans le sens u -> v
        self.adj[u][v][1] += amount
        
        # On retire du flux dans le sens v -> u 
        # Cela permet à l'algorithme de "voir" qu'on peut annuler ce flux plus tard.
        self.adj[v][u][1] -= amount

    def get_neighbors(self, u):
        """Renvoie la liste des voisins de u (clés du dictionnaire)."""
        if u in self.adj:
            return list(self.adj[u].keys())
        return []

    def get_all_vertices(self):
        """Renvoie tous les sommets du graphe."""
        return list(self.adj.keys())

    def __str__(self):
        """Affichage propre pour le débogage."""
        res = "--- État du Graphe ---\n"
        for u in self.adj:
            for v, data in self.adj[u].items():
                cap, flow = data
                # On n'affiche que les arcs qui ont une capacité réelle ou un flux actif
                if cap > 0 or flow > 0:
                    res += f"{u} -> {v} : Flux {flow} / Cap {cap}\n"
        return res
