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

    
    def affichage_noeud(self):
        global canvas
        self.affichage = canvas.create_oval(self.x, self.y, self.x+20, self.y+20,fill='red')


class noeud(bulle):
    def __init__(self, val, voisins, pos=(0,0)):
        super().__init__(val, pos)
        self.voisins = voisins


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

# # définition de la fonction pour créer un rectangle avec des bords arrondis
# def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
#     points = [x1+radius, y1,
#               x1+radius, y1,
#               x2-radius, y1,
#               x2-radius, y1,
#               x2, y1,
#               x2, y1+radius,
#               x2, y1+radius,
#               x2, y2-radius,
#               x2, y2-radius,
#               x2, y2,
#               x2-radius, y2,
#               x2-radius, y2,
#               x1+radius, y2,
#               x1+radius, y2,
#               x1, y2,
#               x1, y2-radius,
#               x1, y2-radius,
#               x1, y1+radius,
#               x1, y1+radius,
#               x1, y1]
#     return canvas.create_polygon(points, smooth=True, **kwargs)

## fonction qui affiche le graphe
def graphe(obj):
    position = [300,300]
    obj.x, obj.y = position[0], position[1]
    lst_angle = [el*(360 / len(obj.voisins)) for el in range(len(obj.voisins))]

    lst_cercle = nbr_cercle(obj.voisins)
    lst_cercle = [[lst_cercle[el]]+[100*(1+el)] for el in range(len(lst_cercle))]
    while len(lst_cercle) > 0:
        j = -1
        for i in range(len(lst_cercle)):
            j += 1
            obj.voisins.append(lst_cercle[j][0].pop(0))
            obj.voisins[-1].x = obj.x + lst_cercle[j][1] * math.cos(lst_angle[0]*math.pi / 180)
            obj.voisins[-1].y = obj.y + lst_cercle[j][1] * math.sin(lst_angle.pop(0)*math.pi / 180)
            obj.voisins[-1].affichage_noeud()
            if lst_cercle[j][0] == []:
                lst_cercle.pop(j)
                j -= 1
    obj.affichage_noeud()

            

    # for i in range(len(lst_cercle)):
    #     print(len(lst_cercle[i]))
    #     for j in range(len(lst_cercle[i])):
    #         lst_angle = [el*(360 / len(lst_cercle[i])) for el in range(len(lst_cercle[i]))]
    #         if i != 0:
    #             lst_angle = [el+(360/len(lst_cercle[i])/2) for el in lst_angle]
    #         lst_cercle[i][j].x = obj.x + 100*(1+i) * math.cos(lst_angle[j]*math.pi / 180)
    #         lst_cercle[i][j].y = obj.y + 100*(1+i) * math.sin(lst_angle[j]*math.pi / 180)
    #         lst_cercle[i][j].affichage_noeud()
    # obj.affichage_noeud()
    



graphe(recuperation_page('Catégorie:Histoire'))









#Creation  d'un bouton "Quitter":
Bouton_Quitter=Button(tk, text ='Quitter', command = tk.destroy)
#On ajoute l'affichage du bouton dans la fenêtre tk:
Bouton_Quitter.pack()


tk.mainloop()






# # ajout du texte à l'intérieur du rectangle
# text = "Ceci est une bulle de carte mentale"
# x, y = 0, 0 # coordonnées du centre du rectangle
# padding = 10 # espace de rembourrage entre le texte et le bord du rectangle
# bbox = canvas.bbox(canvas.create_text(x, y, text=text)) # dimensions du rectangle englobant
# bbox = (bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding) # ajout de rembourrage


# # dessin du rectangle avec des bords arrondis autour du texte
# radius = 20 # rayon des coins arrondis
# rect = create_rounded_rectangle(canvas, *bbox, radius=radius, fill="#3CA6A6", outline="#026773", width=2)

# # création d'une police de caractères en gras

# # ajout du texte centré à l'intérieur du rectangle
# canvas.create_text(x, y, text=text, width=bbox[2]-bbox[0]-2*padding, justify=tk.CENTER, fill="#FFFFFF")

# # lancement de la boucle principale Tkinter
# root.mainloop()