from tkinter import *
import wikipediaapi
import requests
from bs4 import BeautifulSoup
import math


wiki = wikipediaapi.Wikipedia('fr')

tk = Tk()
canvas = Canvas(tk,width = 1000, height = 1000 , bd=0, bg="white")
canvas.pack(padx=10,pady=10)



class bulle:
    def __init__(self, val, pos = (0,0)):
        self.val = val
        self.x = pos[0]
        self.y = pos[1]
        self.affichage = None
        self.affichage_texte = None
        self.largeur = None
        self.hauteur = None

    
    def affichage_noeud(self):
        global canvas
        padding = 10 # espace de rembourrage entre le texte et le bord du rectangle
        bbox = canvas.bbox(canvas.create_text(self.x, self.y, text=self.val)) # dimensions du rectangle englobant
        bbox = (bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding) # ajout de rembourrage
        self.largeur = bbox[2] - bbox[0]
        self.hauteur = bbox[3] - bbox[1]
        radius = 20 # rayon des coins arrondis
        self.affichage = create_rounded_rectangle(canvas, *bbox, radius=radius, fill="#3CA6A6", outline="#026773", width=2)
        self.affichage_texte = canvas.create_text(self.x, self.y, text=self.val, width=bbox[2]-bbox[0]-2*padding, justify=CENTER, fill="#FFFFFF")
        self.x = bbox[0]
        self.y = bbox[1]


class noeud(bulle):
    def __init__(self, val, voisins, pos=(0,0)):
        super().__init__(val, pos)
        self.voisins = voisins


def recuperation_page(page, nbr=48):
    if type(page) == type('str'): 
        page = wiki.page(page)
    if page.title.count('Catégorie:')>=1:
        voisins = [bulle(el.title) for el in wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
    else:
        voisins = [bulle(el.title) for el in wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
    voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
    return noeud(page.title, voisins)


def nbr_cercle(lst):
    lst_remplace = []
    i = 0
    while len(lst)> 0:
        i += 1
        lst_remplace.append([lst.pop(0) for el in lst[:i*8]])
    return lst_remplace

# définition de la fonction pour créer un rectangle avec des bords arrondis
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
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
    return canvas.create_polygon(points, smooth=True, **kwargs)



def arc(obj):
    for bulle in obj.voisins:
        canvas.create_line(obj.x, obj.y, bulle.x, bulle.y, fill="#026773")



## fonction qui affiche le graphe
def graphe(obj):
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
                    obj.voisins[-1].affichage_noeud()
    obj.affichage_noeud()
    arc(obj)
    

### variables
page_courante = recuperation_page('Wikipédia')
graphe(page_courante)

    
def clic(event):
    global page_courante, canvas
    x = event.x
    y = event.y

    
    for v in page_courante.voisins:
        if x > v.x and x < v.x + v.largeur  and  y > v.y and y < v.y+v.hauteur:
            canvas.delete('all')
            page_courante = recuperation_page(v.val)
            graphe(page_courante)
            break















tk.bind('<Button-1>', clic)

tk.mainloop()


