#importation librairies
import wikipediaapi
import random
import math

#importation des autres fichiers du projet
from noeud import *
from pile import *



class page:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia('fr')
        self.page_courante = self.recuperation_page('Wikipedia')
        self.page_sauvegarde = self.wiki.page('Wikipedia')



    def recuperation_page(self, page = None, nbr=48):
        """
        n : un entier positif
        renvoie un objet noeud avec n voisins
        """
        if page == None:
            page = self.wiki.page(self.page_courante.val)
        if type(page) == type('str'): 
            page = self.wiki.page(page)
        print(page)
        if page.exists() != True:
            page = self.page_sauvegarde
        if page.title.count('Catégorie:')>=1:
            voisins = [bulle(el.title) for el in self.wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
        else:
            voisins = [bulle(el.title) for el in self.wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
        random.shuffle(voisins)
        voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
        self.page_sauvegarde = page
        return noeud(page.title, voisins)



    def regeneration_page(self, it, n=0):
        it.canvas.delete('graphe')
        if n == 0: n = 48
        self.page_courante = self.recuperation_page(self.wiki.page(self.page_courante.val), n)
        it.graphe.graphe(it, self.page_courante)



    def changement_page(self,it,  v):
        it.canvas.delete('graphe')
        self.page_courante = self.recuperation_page(v)
        it.graphe.graphe(it, self.page_courante)



class graphe:



    def __init__(self):
        self.pile = pile()



    def nbr_cercle(self, lst):
        """
        lst : une liste de voisins
        renvoie plusieurs liste possedant les elements de lst séparé en fonction du nombre de cercle
        """
        lst_remplace = []
        i = 0
        while len(lst)> 0:
            i += 1
            lst_remplace.append([lst.pop(0) for el in lst[:i*8]])
        return lst_remplace



    def arrondi(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]
        return points


    # définition de la fonction pour créer un rectangle avec des bords arrondis
    def create_rounded_rectangle(self, it, x1, y1, x2, y2, radius, **kwargs):
        """
        renvoie un objet canva rectangle avec les bords arrondis
        """
        points = self.arrondi(x1, y1, x2, y2, radius)
        return it.create_polygon(points, smooth=True, **kwargs)



    def graphe(self, it, obj):
        """
        obj : un noeud contenant une page wikipedia ainsi que ses voisins
        """

        position = [450,380]
        obj.x, obj.y = position[0], position[1]
        lst_angle = [el*(360 / len(obj.voisins)) for el in range(len(obj.voisins))]

        lst_cercle = self.nbr_cercle(obj.voisins)
        lst_cercle = [[lst_cercle[el]]+[100*(1+el)] for el in range(len(lst_cercle))]

        while len(lst_cercle[0][0]) > 0: ### max de rep possible 
            for i in range(len(lst_cercle)):
                for j in range(1+i):
                    if lst_cercle[i][0] != []:
                        obj.voisins.append(lst_cercle[i][0].pop(0))
                        obj.voisins[-1].x = obj.x + lst_cercle[i][1] * math.cos(lst_angle[0]*math.pi / 180)
                        obj.voisins[-1].y = obj.y + lst_cercle[i][1] * math.sin(lst_angle.pop(0)*math.pi / 180)

        it.affichage_page(obj)
        self.pile.affiche_pile(obj)
        obj.affichage_noeud(it, obj)