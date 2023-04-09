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
    
    def affichage_noeud(self):
        global canvas
        self.affichage = canvas.create_oval(self.x, self.y, self.x+20, self.y+20,fill='red')

class noeud(bulle):
    def __init__(self, val, voisins, pos=(0,0)):
        super().__init__(val, pos)
        self.voisins = voisins
        self.affichage = None



def recuperation_page(page, nbr=40):
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



def graphe(obj):
    position = [300,300]
    obj.x, obj.y = position[0], position[1]


    print(len(obj.voisins))
    lst_cercle = nbr_cercle(obj.voisins)
    for i in range(len(lst_cercle)):
        print(len(lst_cercle[i]))
        for j in range(len(lst_cercle[i])):
            lst_angle = [el*(360 / len(lst_cercle[i])) for el in range(len(lst_cercle[i]))]
            lst_cercle[i][j].x = obj.x + 50*(1+i) * math.cos(lst_angle[j]*math.pi / 180)
            lst_cercle[i][j].y = obj.y + 50*(1+i) * math.sin(lst_angle[j]*math.pi / 180)
            lst_cercle[i][j].affichage_noeud()
    obj.affichage_noeud()
    



graphe(recuperation_page('Catégorie:Histoire'))









#Creation  d'un bouton "Quitter":
Bouton_Quitter=Button(tk, text ='Quitter', command = tk.destroy)
#On ajoute l'affichage du bouton dans la fenêtre tk:
Bouton_Quitter.pack()


tk.mainloop()






