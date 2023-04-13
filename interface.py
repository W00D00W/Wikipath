import math
import time

from algorithmie import recuperation_page
from corps import page_sauvegarde
from corps import page_courante
from objet import pile





def regeneration_page():
    global page_courante, it
    it.canvas.delete('all')
    page_courante = recuperation_page(page_courante.val)
    graphe(page_courante)

def changement_page(v):
    global canvas, page_courante
    it.canvas.delete('all')
    print(page_sauvegarde)
    page_courante = recuperation_page(v)
    graphe(page_courante)


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
def create_rounded_rectangle(it, x1, y1, x2, y2, radius, **kwargs):
    """
    renvoie un objet canva rectangle avec les bords arrondis
    """
    points = arrondi(x1, y1, x2, y2, radius)
    return it.create_polygon(points, smooth=True, **kwargs)

pile_page = pile()

## fonction qui affiche le graphe
def graphe(obj):
    """
    obj : un noeud contenant une page wikipedia ainsi que ses voisins
    """

    position = [500,480]
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

    it.affichage_page(obj)
    obj.affichage_noeud()
    pile_page.affiche_pile()



### fonctions tkinter
def actu_pos(event):
    """
    actualise pos a chaque clic
    """
    global page_courante, it, item, pos, co

    pos[0], pos[1] = event.x, event.y
    
    if item == None:
        item = page_courante.trouve_item(it.canvas.find_closest(event.x, event.y))
        if item != None:
            if item.contient(event.x, event.y) != True:
                item = None

def clic(event):
    """
    regenere un graphe a chaque double clic
    """
    global page_courante, it
    x = event.x
    y = event.y
   
    for v in page_courante.voisins:
        if x > v.x and x < v.x + v.largeur  and  y > v.y and y < v.y+v.hauteur:
            it.canvas.move('all', 500, 480)
            page_courante.actualisation()
            time.sleep(1)
            it.canvas.delete('all')
            pile_page.ajout_pile(page_courante)
            pile_page.deplacer_centre(v.x, v.y)
            page_courante = recuperation_page(v.val)
            graphe(page_courante)
            break


def item_bouge(event):
    """
    bouge l'ensemble ou un item en fonction de la souris
    """
    global page_courante, it, item, pos

    if item is not None:
        x, y = event.x-item.largeur/2, event.y-item.hauteur/2
        bbox = arrondi(x, y, x+item.largeur, y+item.hauteur, 20)
        it.canvas.coords(item.affichage[0], *bbox)
        it.canvas.coords(item.affichage[1], x+item.largeur/2, y+item.hauteur/2)
        pos = it.canvas.coords(item.affichage[2])
        it.canvas.coords(item.affichage[2], pos[0], pos[1], x+item.largeur/2, y+item.hauteur/2)
        item.actualisation()
    else:
        it.canvas.move('all', event.x-pos[0], event.y - pos[1])
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



