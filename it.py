from tkinter import *
import wikipediaapi
import requests
from bs4 import BeautifulSoup
import math

wiki = wikipediaapi.Wikipedia('fr')

tk = Tk()
canvas = Canvas(tk,width = 1000, height = 1000 , bd=0, bg="white")
canvas.pack(padx=10,pady=10)

class noeud():
    def __init__(self, val, voisins, pos=(0,0)):
        self.val = val
        self.voisins = voisins
        self.x = pos[0]
        self.y = pos[1]
        self.affichage = None

    def affichage_noeud(self):
        global canvas
        self.affichage = canvas.create_oval(self.x, self.y, self.x+20, self.x+20,fill='red')

def recuperation_page(page, nbr=40):
    if type(page) == type('str'): 
        page = wiki.page(page)
    if page.title.count('Catégorie:')>=1:
            voisins = [el for el in wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
    else:
        voisins = [el for el in wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
    voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
    return noeud(page.title, voisins)



def graphe(dico):
    position = [50,50]
    val = [el.val for el in dico.values()]
    print(val)
    for val in dico.values():
        val.x, val.y = position[0], position[1]
        if len(val.voisins)<8:
            angle = 360 / len(val.voisins)
            lst_angle = [el*angle for el in range(len(val.voisins))]
        for i in range(len(val.voisins)):
            dico[val.voisins[i]].x = val.x + 8 * math.cos(lst_angle[i]*math.pi / 180)
            dico[val.voisins[i]].y = val.y + 8 * math.sin(lst_angle[i]*math.pi / 180)


    


# graphe(recuperation_page('Catégorie:Histoire'))









# #Creation  d'un bouton "Quitter":
# Bouton_Quitter=Button(tk, text ='Quitter', command = tk.destroy)
# #On ajoute l'affichage du bouton dans la fenêtre tk:
# Bouton_Quitter.pack()

# balle = noeud('a', [], (40,40))
# balle.affichage_noeud()




# tk.mainloop()






