class pile:



    def __init__(self):
        self.pile = []
    


    def ajout_pile(self, page_courante):
        if page_courante not in self.pile:
            print(page_courante, self.pile)
            self.pile.append(page_courante)
            self.pile[-1].etat = False
            self.pile[-1].affichage = []



    def vider_pile(self):
        self.pile = []
    


    def deplacer_centre(self, x, y):
        for v in self.pile:
            v.x -= x
            v.y -= - y
        
        

    def retour_arriere(self, obj):
        self.pile = self.pile[:self.pile.index(obj)]



    def affiche_pile(self, page):
        for i in range(len(self.pile)):
            page.ajout_voisin(self.pile[len(self.pile)-1-i])