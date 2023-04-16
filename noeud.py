#importation librairies
from tkinter import *



class bulle:
    def __init__(self, val, pos = (0,0)):
        self.val = val
        self.x = pos[0]
        self.y = pos[1]
        self.affichage = []
        self.largeur = None
        self.hauteur = None
        self.etat = True
        self.passage = 0



    def affichage_noeud(self, it, page): ### permet l'affichage du noeud
        """
        ne prend rien en parametre 
        crée un objet sur le canvas pour afficher le noeud
        ne renvoie rien
        """
        self.calcul(it) ## permet de connaitre taille du texte et place

        if self.etat == True:
            ### gestion des collisions 
            test = [True]
            while True in test:  
                test = []
                test.append(self.collision(page))
                for v in page.voisins:
                    if v.hauteur != None:
                        test.append(self.collision(v))

        bbox = (self.x, self.y, self.x+self.largeur, self.y+self.hauteur) ## redefinition de la taille 
        radius = 20 # rayon des coins arrondis
        padding = 10 # espace de rembourrage entre le texte et le bord du rectangle
        if self.etat != True: 
            couleur = '#bebfc2'
        else : 
            couleur = '#F2F3F5'
        if len(self.affichage) > 2:
            self.affichage = []
        self.affichage.append(it.graphe.create_rounded_rectangle(it.canvas, *bbox, radius=radius, fill=couleur, outline="#4E5058", width=2, tag='graphe'))
        self.affichage.append(it.canvas.create_text(self.x+self.largeur/2, self.y+self.hauteur/2, text=self.val, width=bbox[2]-bbox[0]-2*padding, justify=CENTER, fill="black", tag='graphe'))



    def ajout_lien(self, it, obj): ### rajoute le tracé du lien dans la variable qui stocke l'affichage
        
        couleur = '#4E5058'
        if self.etat != True: 
            if obj.voisins[obj.voisins.index(self)+1].etat == False:
                obj = obj.voisins[obj.voisins.index(self)+1]
        self.affichage.append(it.canvas.create_line(obj.x+obj.largeur/2, obj.y+obj.hauteur/2, self.x+self.largeur/2, self.y+self.hauteur/2, fill=couleur, tag='graphe', width=1.5))



    def calcul(self, it): ### permet de trouver la largeur du rectangle
        """
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


    
    def __init__(self, val, voisins, pos=(0,0)):
        super().__init__(val, pos)
        self.voisins = voisins



    def affichage_noeud(self, it, obj):
        """
        permet d'afficher le noeud ainsi que tout les voisins
        ne prend rien en parametre
        ne renvoie rien
        """
        super().affichage_noeud(it, obj)
        
        if self.etat == True:
            [v.affichage_noeud(it, obj) for v in self.voisins] ## affiche tout les voisins
            [v.ajout_lien(it, self) for v in self.voisins] ## affiche tout les liens

            for i in range(2):
                it.canvas.tag_raise(self.affichage[i])
            for v in self.voisins:
                for i in range(2):
                    it.canvas.tag_raise(v.affichage[i])



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
            


