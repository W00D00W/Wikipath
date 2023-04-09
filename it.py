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

class noeud(bulle):
    def __init__(self, val, voisins, pos=(0,0)):
        super().__init__(val, pos)
        self.voisins = voisins
        self.affichage = None

    def affichage_noeud(self):
        global canvas
        self.affichage = canvas.create_oval(self.x, self.y, self.x+20, self.x+20,fill='red')

def recuperation_page(page, nbr=40):
    if type(page) == type('str'): 
        page = wiki.page(page)
    if page.title.count('Catégorie:')>=1:
            voisins = [bulle(el.title) for el in wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
    else:
        voisins = [bulle(el.title) for el in wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
    voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
    return noeud(page.title, voisins)



def graphe(obj):
    position = [50,50]
    obj.x, obj.y = position[0], position[1]
    if len(obj.voisins)<8:
        lst_angle = [el*(360 / len(obj.voisins)) for el in range(len(obj.voisins))]
    for i in range(len(obj.voisins)):
        obj.voisins[i].x = obj.x + 8 * math.cos(lst_angle[i]*math.pi / 180)
        obj.voisins[i].y + 8 * math.sin(lst_angle[i]*math.pi / 180)



# graphe(recuperation_page('Catégorie:Histoire'))









# #Creation  d'un bouton "Quitter":
# Bouton_Quitter=Button(tk, text ='Quitter', command = tk.destroy)
# #On ajoute l'affichage du bouton dans la fenêtre tk:
# Bouton_Quitter.pack()

# balle = noeud('a', [], (40,40))
# balle.affichage_noeud()




# tk.mainloop()






