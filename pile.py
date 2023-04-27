class pile:
    def __init__(self):
        self.pile = []

    def ajout_pile(self, page_courante):
        """
        ajoute un objet noeud dans la pile
        """
        if page_courante.val not in [v.val for v in self.pile]:
            self.pile.append(page_courante)
            self.pile[-1].etat = False
            self.pile[-1].affichage = []

    def vider_pile(self):
        """
        vide la pile
        """
        self.pile = []
    
    def deplacer_centre(self, x, y):
        """
        x, y deux entiers correspondant a des coordonées
        deplace chaque noeud de x et y 
        """
        # self.pile[-1].x, self.pile[-1].y = 200, 500
        for v in self.pile:
            v.x -= v.x - x
            v.y += v.y - y

    def retour_arriere(self, obj):
        """
        obj : un noeud correspondant a un noeud stocké dans la pile
        suprime tout les elements se trouvant apres celui rentré en parametre
        """
        self.pile = self.pile[:self.pile.index(obj)]

    def affiche_pile(self, page):
        """
        page : un objet noeud
        ajoute au voisin de page les elements contenus dans la pile
        """
        for i in range(len(self.pile)):
            page.ajout_voisin(self.pile[len(self.pile)-1-i])