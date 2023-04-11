from tkinter import *
import wikipediaapi
import requests
from bs4 import BeautifulSoup
import math
import time
import random
import copy
import asyncio
import customtkinter 

### 
# definition de variables propres a tkinter et tkinter
wiki = wikipediaapi.Wikipedia('fr')


tk = Tk()
tk.attributes('-fullscreen', True)
tk.update()

largeur = tk.winfo_width()
hauteur = tk.winfo_height()

print(largeur, hauteur)

canvas = Canvas(tk,width = (largeur/4)*3, height = hauteur , bd=0, bg="white")
canvas.grid(row=1, column=0, columnspan=3,rowspan=3, pady=10)

####

### classes 

## correspond a un voisin
class bulle:
    def __init__(self, val, pos = (0,0)):
        self.val = val
        self.x = pos[0]
        self.y = pos[1]
        self.affichage = []
        self.largeur = None
        self.hauteur = None

    def affichage_noeud(self): ### permet l'affichage du noeud
        """
        ne prend rien en parametre 
        crée un objet sur le canvas pour afficher le noeud
        ne renvoie rien
        """
        global canvas, page_courante

        self.calcul() ## permet de connaitre taille du texte et place

        ### gestion des collisions 
        test = [True]
        while True in test:  
            test = []
            test.append(self.collision(page_courante))
            for v in page_courante.voisins:
                if v.hauteur != None:
                    test.append(self.collision(v))

        bbox = (self.x, self.y, self.x+self.largeur, self.y+self.hauteur) ## redefinition de la taille 
        radius = 20 # rayon des coins arrondis
        padding = 10 # espace de rembourrage entre le texte et le bord du rectangle
        self.affichage.append(create_rounded_rectangle(canvas, *bbox, radius=radius, fill="#00FFFF", outline="#026773", width=2))
        self.affichage.append(canvas.create_text(self.x+self.largeur/2, self.y+self.hauteur/2, text=self.val, width=bbox[2]-bbox[0]-2*padding, justify=CENTER, fill="black"))

    def ajout_lien(self, obj): ### rajoute le tracé du lien dans la variable qui stocke l'affichage
        self.affichage.append(canvas.create_line(obj.x+obj.largeur/2, obj.y+obj.hauteur/2, self.x+self.largeur/2, self.y+self.hauteur/2, fill="#026773"))

    def calcul(self): ### permet de trouver la largeur du rectangle
        """
        calcul la largeur du rectangle et attribue a x, y, largeur et hauteur les valeurs correspondantes
        ne renvoie rien
        """
        global canvas
        padding = 10 # espace de rembourrage entre le texte et le bord du rectangle
        affiche = canvas.create_text(self.x, self.y, text=self.val)
        bbox = canvas.bbox(affiche) # dimensions du rectangle englobant
        bbox = (bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding) # ajout de rembourrage
        canvas.delete(affiche)

        self.x = bbox[0]
        self.y = bbox[1]
        self.largeur = bbox[2] - bbox[0]
        self.hauteur = bbox[3] - bbox[1]

    ### actualise le x et le y en fonction du x et y du canvas
    def actualisation(self): 
        """
        attribue les coordonées x et y du canvas pour l'objet au x et y de l'objet
        """
        self.x = canvas.coords(self.affichage[1])[0]-self.largeur/2
        self.y = canvas.coords(self.affichage[1])[1]-self.hauteur/2

    ### verifie si l'objet est affiché par dessus un autre, si oui le déplace
    def collision(self, obj):  
        """
        obj, un obj bulle ou noeud differend de l'objet actuel
        déplace l'objet jusqu'a ce qu'il ne se supperpose plus a aucun autre
        renvoie True si l'objet a été déplacé, False sinon
        """
        global canvas
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

    def affichage_noeud(self):
        """
        permet d'afficher le noeud ainsi que tout les voisins
        ne prend rien en parametre
        ne renvoie rien
        """
        super().affichage_noeud()
        
        [v.affichage_noeud() for v in self.voisins] ## affiche tout les voisins
        [v.ajout_lien(self) for v in self.voisins] ## affiche tout les liens

        for i in range(2):
            canvas.tag_raise(self.affichage[i])
        for v in self.voisins:
            for i in range(2):
                canvas.tag_raise(v.affichage[i])
    
    def trouve_item(self, item):
        """
        item : int ou un objet du canva
        renvoie l'objet qui possede l'objet du canvas
        """
        for v in self.voisins:
            if item[0] in v.affichage:
                return v




class file:
    def __init__(self):
        self.tab = []

def recuperation_page(page, nbr=48):
    """
    page : objet wikipedia ou chaine de caractere, n : un entier positif
    renvoie un objet noeud avec n voisins
    """
    global page_sauvegarde
    if type(page) == type('str'): 
        page = wiki.page(page)
    if page.exists() != True:
        page = page_sauvegarde
    if page.title.count('Catégorie:')>=1:
        voisins = [bulle(el.title) for el in wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
    else:
        voisins = [bulle(el.title) for el in wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
    random.shuffle(voisins)
    voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
    page_sauvegarde = page
    return noeud(page.title, voisins)


def nbr_cercle(lst):
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

def arrondi(x1, y1, x2, y2, radius, **kwargs):
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
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    """
    renvoie un objet canva rectangle avec les bords arrondis
    """
    points = arrondi(x1, y1, x2, y2, radius)
    return canvas.create_polygon(points, smooth=True, **kwargs)

texte = [None, None, None]
texte[0] = Label(tk, text = '', font='Arial 20')
texte[0].grid(row=1, column=3, columnspan=1, pady=10)

texte[1] = Label(tk, text='', justify='left', font='Arial 10')
texte[1].grid(row=2, column=3, columnspan=1, pady=10)

texte[2] = Label(tk, text='', justify='left', font='Arial 10')
texte[2].grid(row=3, column=3, columnspan=1, pady=10)


## fonction qui affiche le graphe
def graphe(obj):
    """
    obj : un noeud contenant une page wikipedia ainsi que ses voisins
    """
    position = [400,400]
    obj.x, obj.y = position[0], position[1]
    lst_angle = [el*(360 / len(obj.voisins)) for el in range(len(obj.voisins))]

    lst_cercle = nbr_cercle(obj.voisins)
    lst_cercle = [[lst_cercle[el]]+[100*(1+el)] for el in range(len(lst_cercle))]
    while len(lst_cercle[0][0]) > 0: ### max de rep possible 
        for i in range(len(lst_cercle)):
            for j in range(1+i):
                if lst_cercle[i][0] != []:
                    obj.voisins.append(lst_cercle[i][0].pop(0))
                    obj.voisins[-1].x = obj.x + lst_cercle[i][1] * math.cos(lst_angle[0]*math.pi / 180)
                    obj.voisins[-1].y = obj.y + lst_cercle[i][1] * math.sin(lst_angle.pop(0)*math.pi / 180)
    affichage_page(obj)
    obj.affichage_noeud()




def affichage_page(page):
    global texte
    page = wiki.page(page.val)
    sum = page.summary
    lst = sum.split(' ')
    cpt = 0
    chaine = ''
    while len(lst) > 0:
        if cpt+len(lst[0]) < 55:
            cpt += len(lst[0])
            chaine += lst.pop(0) + ' '
        else:
            cpt = 0
            chaine += '\n'
    
    titre = page.title
    lst = titre.split(' ')
    cpt = 0
    titre_modif = ''
    while len(lst) > 0:
        if cpt+len(lst[0]) < 20:
            cpt += len(lst[0])
            titre_modif += lst.pop(0) + ' '
        else:
            cpt = 0
            titre_modif += '\n'
    
    texte[0].config(text= titre_modif)
    texte[1].config(text=chaine)
    texte[2].config(text=page.fullurl)




### variables
page_courante = recuperation_page('Wikipédia')
page_sauvegarde = page_courante
item = None
pos = [0,0]
graphe(page_courante)



### fonctions tkinter
def actu_pos(event):
    """
    actualise pos a chaque clic
    """
    global page_courante, canvas, item, pos

    pos[0], pos[1] = event.x, event.y

def clic(event):
    """
    regenere un graphe a chaque double clic
    """
    global page_courante, canvas
    x = event.x
    y = event.y
   
    for v in page_courante.voisins:
        if x > v.x and x < v.x + v.largeur  and  y > v.y and y < v.y+v.hauteur:
            canvas.delete('all')
            page_courante = recuperation_page(v.val)
            graphe(page_courante)
            break

def item_bouge(event):
    """
    bouge l'ensemble ou un item en fonction de la souris
    """
    global page_courante, canvas, item, pos
    if item == None:
        item = page_courante.trouve_item(canvas.find_closest(event.x, event.y))
        if item != None:
            if item.contient(event.x, event.y) != True:
                item = None
    if item is not None:
        x, y = event.x-item.largeur/2, event.y-item.hauteur/2
        bbox = arrondi(x, y, x+item.largeur, y+item.hauteur, 20)
        canvas.coords(item.affichage[0], *bbox)
        canvas.coords(item.affichage[1], x+item.largeur/2, y+item.hauteur/2)
        pos = canvas.coords(item.affichage[2])
        canvas.coords(item.affichage[2], pos[0], pos[1], x+item.largeur/2, y+item.hauteur/2)
        item.actualisation()
    else:
        canvas.move('all', event.x-pos[0], event.y - pos[1])
        pos[0], pos[1] = event.x, event.y
        
def item_remove(event):
    """
    réinitialise la variable item lorsque le clic de souris est relaché
    """
    global page_courante, item
    item =  None    
    page_courante.actualisation()
    for element in page_courante.voisins:
        element.actualisation()



tk.bind('<Button-1>', actu_pos)
tk.bind('<Double-Button-1>', clic)
tk.bind('<B1-Motion>', item_bouge)
tk.bind('<ButtonRelease-1>', item_remove)

tk.mainloop()


