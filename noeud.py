#importation librairies
from tkinter import *



class bulle:
    """
    un objet represantant un noeud sur le canvas
    """
    def __init__(self, val, pos = (0,0)):
        self.val = val ## la valeur du noeud
        self.x = pos[0] ## la position x sur le canvas
        self.y = pos[1] ## la position y sur le canvas
        self.affichage = [] ## stocke les widget relatifs a l'affichage du noeud
        self.largeur = None 
        self.hauteur = None
        self.etat = True ## si il fait parti des voisins direct ou si il fait parti des page deja visités / True : voisins direct

        self.x_initial = 0 ## sauvegarde de la position
        self.y_initial = 0 ## sauvegarde de la position
        self.centre = False ## permet de distinguer un voisin du noeud principal

    def affichage_noeud(self, it, page, co = True):
        """
        it : l'objet interface
        page : le noeud principal avec ces voisins
        co : collision / permet de savoir si il faut calculer les collisions avant d'afficher le noeud
        crée un objet sur le canvas pour afficher le noeud
        ne renvoie rien
        """
        self.calcul(it) ## permet de connaitre taille du texte et place
        if co == True: ## calcul les positions car le noeud n'a jamais été placé sur le canvas
            if self.etat == True:
                ### gestion des collisions 
                test = [True]
                while True in test:  
                    test = []
                    test.append(self.collision(page))
                    for v in page.voisins:
                        if v.hauteur != None:
                            test.append(self.collision(v))

        else: ## si on reconstruit un graphe a partir d'un noeud ou les positions ont deja été calculé
            if self.centre == True:
                self.x, self.y = 500, 480 
            else:
                self.x, self.y = self.x_initial, self.y_initial 

        bbox = (self.x, self.y, self.x+self.largeur, self.y+self.hauteur) ## redefinition de la taille 
        radius = 20 # rayon des coins arrondis
        padding = 10 # espace de rembourrage entre le texte et le bord du rectangle

        ## couleurs
        if self.etat != True: ## ancien noeud / dans la pile
            couleur = '#bebfc2'
        elif self.centre == True: ## noeud principal
            couleur = '#EBD6EA'
        else :  ## voisin
            couleur = '#F2F3F5'
        if len(self.affichage) > 2: ## vide la liste qui stocke les elements a afficher
            self.affichage = []
        self.affichage.append(it.graphe.rectangle_bord_rond(*bbox, radius=radius, fill=couleur, outline="#4E5058", width=2, tag='graphe')) ## affiche le rectangle
        self.affichage.append(it.canvas.create_text(self.x+self.largeur/2, self.y+self.hauteur/2, text=self.val, width=bbox[2]-bbox[0]-2*padding, justify=CENTER, fill="black", tag='graphe')) ## affiche le texte

        if co == True:
            self.x_initial, self.y_initial = self.x, self.y ## sauvegarde de la position
        elif self.centre != True: ## si on recréé un noeud a partir d'un graphe deja existant
            self.x, self.y = self.x_initial, self.y_initial 

    def ajout_lien(self, it, obj):
        """
        it : objet interface
        obj : un noeud 
        trace un trait entre le noeud et le voisin
        """
        couleur = '#4E5058'
        if self.etat != True: ## si appartient a la pile (noeud visité precedement)
            if obj.voisins[obj.voisins.index(self)+1].etat == False: ## si le prochain voisin appartient egalement a la pile (noeud visité precedement)
                obj = obj.voisins[obj.voisins.index(self)+1] ## obj devient l'obj suivant au lieu d'etre le noeud du milieu
        self.affichage.append(it.canvas.create_line(obj.x+obj.largeur/2, obj.y+obj.hauteur/2, self.x+self.largeur/2, self.y+self.hauteur/2, fill=couleur, tag='graphe', width=1.5)) ## affiche le tracé

    def calcul(self, it):
        """
        it : objet interface
        calcul la largeur du rectangle et attribue aux variables x, y, largeur et hauteur les valeurs correspondantes
        ne renvoie rien
        """
        padding = 10 # espace de rembourrage entre le texte et le bord du rectangle
        affiche = it.canvas.create_text(self.x, self.y, text=self.val)
        bbox = it.canvas.bbox(affiche) # dimensions du rectangle englobant
        bbox = (bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding) # ajout de rembourrage
        it.canvas.delete(affiche)

        self.x = bbox[0]
        self.y = bbox[1]
        self.largeur = bbox[2] - bbox[0]
        self.hauteur = bbox[3] - bbox[1]


    ### actualise le x et le y en fonction du x et y du canvas
    def actualisation(self, it): 
        """
        attribue les coordonées x et y du canvas pour l'objet au x et y de l'objet
        """
        if len(self.affichage) > 0:
            self.x = it.canvas.coords(self.affichage[1])[0]-self.largeur/2
            self.y = it.canvas.coords(self.affichage[1])[1]-self.hauteur/2


    ### verifie si l'objet est affiché par dessus un autre, si oui le déplace
    def collision(self, obj):  
        """
        obj, un obj bulle ou noeud differend de l'objet actuel
        déplace l'objet jusqu'a ce qu'il ne se supperpose plus a aucun autre
        renvoie True si l'objet a été déplacé, False sinon
        """
        global it
        stop = False
        dep = False
        while stop == False:
            if self.x > obj.x and self.x < obj.x+obj.largeur and self.y < obj.y and self.y +self.hauteur > obj.y: ## +
                self.x += 15
                self.y += 5
                dep = True
            elif self.x > obj.x and self.x < obj.x+obj.largeur and self.y > obj.y and self.y < obj.y+obj.hauteur:
                self.x += 15
                self.y += 5
                dep = True
            elif self.x > obj.x and self.x < obj.x+obj.largeur and self.y == obj.y:
                self.x += 15
                dep = True
            elif self.x < obj.x and self.x+self.largeur > obj.x and self.y < obj.y and self.y +self.hauteur > obj.y:
                self.x += 15
                self.y += 5
                dep = True
            elif self.x < obj.x and self.x+self.largeur > obj.x and self.y > obj.y and self.y < obj.y+obj.hauteur:
                self.x += 15
                self.y += 5
                dep = True
            elif self.x < obj.x and self.x+self.largeur > obj.x and self.y == obj.y:
                self.x += 15
                dep = True
            else:
                stop = True
        return dep
    
    

    def contient(self, x, y):
        """
        x, y : floats; renvoie une True si la position x y est comprise dans la hitbox de l'objet, False sinon
        """
        if self.x < x and self.x+self.largeur > x and self.y < y and self.y+self.hauteur > y:
            return True
        return False
    


class noeud(bulle):
    """
    objet definissant le noeud central du graphe (hérite de la classe bulle)
    """

    def __init__(self, val, voisins, pos=(0,0)):
        super().__init__(val, pos) ## appelle init de la classe bulle
        self.voisins = voisins

    def affichage_noeud(self, it, obj, val=True):

        """
        it : objet interface
        obj : noeud correspondant au noeud du milieu
        permet d'afficher le noeud ainsi que tout les voisins
        ne renvoie rien
        """
        if self.etat == True: self.centre = True  ## defini le noeud comme noeud central

        super().affichage_noeud(it, obj, val) ## affiche le noeud

        if self.etat == True: ## si noeud correspond au noeud central
            
            [v.affichage_noeud(it, obj, val) for v in self.voisins] ## affiche tout les voisins
            [v.ajout_lien(it, self) for v in self.voisins] ## affiche tout les liens

            for i in range(2):
                it.canvas.tag_raise(self.affichage[i]) ## fait passer le rectangle et le texte devant le trait
            for v in self.voisins:
                for i in range(2):
                    it.canvas.tag_raise(v.affichage[i]) ## fait passer le rectangle et le texte devant le trait

        



    def ajout_voisin(self, voisin):
        if voisin not in self.voisins:
            self.voisins.insert(0, voisin)
    


    def trouve_item(self, item):
        """
        item : int ou un objet du canva
        renvoie l'objet qui possede l'objet du canvas
        """
        for v in self.voisins:
            if item[0] in v.affichage:
                return v
            


