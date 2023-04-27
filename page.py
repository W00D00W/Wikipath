import wikipediaapi
import random
import math 

from noeud import *
from pile import *

class page:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia('fr') ## defini l'objet wiki avec la langue français : ne prend que les pages référencé sur le wikipédia français
        self.page_courante = self.recuperation_page('Wikipedia') ## recupere un noeud et tout ses voisins de la page wikipedia
        self.page_sauvegarde = self.wiki.page('Wikipedia') ## garde en mémoire l'objet wikipedia

    def recuperation_page(self, page = None, nbr=48):
        """
        n : un entier positif
        renvoie un objet noeud avec n voisins
        """
        if page == None:
            page = self.wiki.page(self.page_courante.val) ## si la valeur rentré en parametre est nulle prend l'ancienne valeure
        if type(page) == type('str'): 
            page = self.wiki.page(page) ## recupere un objet wiki
        if page.exists() != True:
            page = self.page_sauvegarde ## remet l'ancienne page si la nouvelle est inexistante
        ## recupere une liste filtrée
        if page.title.count('Catégorie:')>=1: 
            voisins = [bulle(el.title) for el in self.wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14] ## recherche dans les liens relatifs au page de categorie
        else:
            voisins = [bulle(el.title) for el in self.wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recherche dans les liens relatifs au page basiques
        random.shuffle(voisins)
        voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
        self.page_sauvegarde = page ## défini la page de sauvegarde sur la page courante
        return noeud(page.title, voisins) ## renvoie un noeud avec tout ses voisins

    def regeneration_page(self):
        """
        recupere un nouvel objet noeud a partir de la même valeur / recupere aléatoirement de nouveau voisins
        """
        self.page_courante = self.recuperation_page(self.wiki.page(self.page_courante.val))

    def changement_page(self,it,  v):
        """
        it : interface (fait reference a l'objet ou est stocké le canvas)
        v : nouvelle page a generer (correspondnant a un voisin de la page initiale)
        change la page courante par la nouvelle valeure et affiche le graphe
        """
        it.canvas.delete('graphe')
        self.page_courante = self.recuperation_page(v)
        it.graphe.graphe(it, self.page_courante)

class graphe:
    def __init__(self, objet):
        self.pile = pile() ## objet pile
        self.parent = objet

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
    def rectangle_bord_rond(self, x1, y1, x2, y2, radius, **kwargs):
        """
        renvoie un objet canva rectangle avec les bords arrondis
        """
        points = self.arrondi(x1, y1, x2, y2, radius)
        return self.parent.canvas.create_polygon(points, smooth=True, **kwargs)

    def graphe(self, obj, co = True):
        """
        obj : un noeud contenant une page wikipedia ainsi que ses voisins
        calcul la position de chaque elements
        """
        if co == True: ## regarde si besoin de recalculer les positions ou non
            position = [500,480]
            obj.x, obj.y = position[0], position[1] ## objet repositionne au milieu
            lst_angle = [el*(360 / len(obj.voisins)) for el in range(len(obj.voisins))] ##

            lst_cercle = self.nbr_cercle(obj.voisins) ## separe la liste en nombre de cercle voulu
            lst_cercle = [[lst_cercle[el]]+[100*(1+el)] for el in range(len(lst_cercle))] ## creation d'une liste avec la liste d'element et son rayon

            ## determine la position de chaque elements sur le canvas en les disposant autour de l'element au centre
            while len(lst_cercle[0][0]) > 0: ## tant qu'il y a des elements dans le premier cercle
                for i in range(len(lst_cercle)):
                    for j in range(1+i):
                        if lst_cercle[i][0] != []:
                            obj.voisins.append(lst_cercle[i][0].pop(0))
                            obj.voisins[-1].x = obj.x + lst_cercle[i][1] * math.cos(lst_angle[0]*math.pi / 180)
                            obj.voisins[-1].y = obj.y + lst_cercle[i][1] * math.sin(lst_angle.pop(0)*math.pi / 180)
          
        self.parent.zone_droite.affichage_page(obj) ## modifie l'affichage du widget avec les parametres du nouveau noeud
        self.pile.affiche_pile(obj) ## affiche les anciens noeud ou l'utilisateur a cliqué
        obj.affichage_noeud(self.parent, obj, co) ## affiche le noeud courant sur le graphe
    
        