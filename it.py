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
import webbrowser

### 
# definition de variables propres a tkinter et tkinter
wiki = wikipediaapi.Wikipedia('fr')

class interface:
    def affichage_bouton(self, values):
            if values == 'prédefinie':
                self.recherche_page_entry.grid_forget()
                self.recherche_page_ok.grid_forget()
                self.predefini()
            else:
                self.recherche_page_entry.grid(row=0, column=1)
                self.recherche_page_ok.grid(row=0, column=2)
                regeneration_page()
                

    def __init__(self):
        self.arbre = None
        self.tk = customtkinter.CTk()

        customtkinter.set_appearance_mode("Dark")
        self.tk.geometry(str(self.tk.winfo_screenwidth())+'x'+str(self.tk.winfo_screenheight()))
        self.tk.update()

        largeur = self.tk.winfo_width()
        hauteur = self.tk.winfo_height()

        ### affichage canva
        self.canvas = Canvas(self.tk,width = (largeur/4)*3, height = hauteur , bd=0, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=3,rowspan=3)

        self.tk.grid_columnconfigure(3, weight = 1)

        #### affichage menu

        self.barre_menu = customtkinter.CTkFrame(master = self.tk, width = largeur, height= 30)
        self.barre_menu.grid(row=0, column=0, columnspan=4)

        for i in range(3):
            self.barre_menu.columnconfigure(i, weight=1)

        self.barre_menu.grid_propagate(False)

        ### creation des boutons propres au menu
        self.login_button = customtkinter.CTkButton(self.barre_menu, text="Se connecter / S'inscrire")
        self.login_button.grid(row=0, column=0, sticky='W', padx=10)

        self.quitter_button = customtkinter.CTkButton(self.barre_menu, text="Quitter")
        self.quitter_button.grid(row=0, column=2, sticky='E', padx=10)

        ### recherche
        self.recherche = customtkinter.CTkFrame(self.barre_menu)
        self.recherche.grid(row=0, column=1)

        self.valeurs = customtkinter.CTkSegmentedButton(self.recherche, values=['prédefinie', 'rechercher'], command = self.affichage_bouton)
        self.valeurs.grid(row=0, column=0)

        self.recherche_page_entry = customtkinter.CTkEntry(self.recherche)
        self.recherche_page_entry.grid(row=0, column=1)

        self.recherche_page_ok = customtkinter.CTkButton(self.recherche, text='ok', width = 20, command= lambda : changement_page(self.recherche_page_entry.get()))
        self.recherche_page_ok.grid(row=0, column=5)

        self.zone_droite = customtkinter.CTkFrame(self.tk, width = (self.tk.winfo_screenwidth()/4)-50, height=self.tk.winfo_screenheight()-120)

        self.zone_droite.grid(row=1, column=3)

        self.zone_droite.rowconfigure(0, weight=1)
        self.zone_droite.rowconfigure(1, weight=1)
        self.zone_droite.rowconfigure(2, weight=1)

        self.zone_droite.grid_propagate(False)

        self.texte = [None, None, None, None]
        self.texte[0] = customtkinter.CTkLabel(self.zone_droite, text = '')
        self.texte[0].grid(row=0, column=0, columnspan=1, pady=10, sticky='snew')

        self.texte[1] = customtkinter.CTkTextbox(self.zone_droite, width= 330, height=600, fg_color='transparent')
        self.texte[1].grid(row=1, column=0, columnspan=1)

        self.texte[2] = customtkinter.CTkButton(self.zone_droite, text = 'Aller a la page', command=lambda : webbrowser.open_new(''))
        self.texte[2].grid(row=2, column=0, columnspan=1, pady=10, sticky='S')

        self.texte[3] = customtkinter.CTkButton(self.zone_droite, text='recharger les liens', command = lambda : regeneration_page())
        self.texte[3].grid(row=3, column=0, columnspan=1, pady=10)
        
        ### appartion ou non du bouton de la barre de recherche

    def affichage_page(self, page):
        page = wiki.page(page.val)
        
        sum = page.summary
    
        titre = page.title
        lst = titre.split(' ')
        cpt = 0
        titre_modif = ''
        while len(lst) > 0:
            if cpt+len(lst[0]) < 20 or len(lst) == 1:
                cpt += len(lst[0])
                titre_modif += lst.pop(0) + ' '
            else:
                cpt = 0
                titre_modif += '\n'
        
        self.texte[0].configure(text= titre_modif)
        self.texte[1].configure(state='normal')
        self.texte[1].delete(0.0, END)
        self.texte[1].insert("0.0", sum)
        self.texte[1].configure(state='disabled')
        self.texte[2].configure(command= lambda : webbrowser.open_new(page.fullurl))

    def predefini(self):
        global page_courante
        self.canvas.delete('all')
        page_courante = noeud('Wikipedia', [bulle('Catégorie:Littérature'), bulle('Catégorie:histoire'), bulle('Catégorie:musique'), bulle('Catégorie:mode'), 
                            bulle('Catégorie:art'), bulle('Catégorie:culture'), bulle('Catégorie:géographie'), bulle('Catégorie:géopolitique'), 
                            bulle('Catégorie:politique'), bulle('Catégorie:culture pop'), bulle('Catégorie:philosophie'), bulle('Catégorie:mathématiques'),
                            bulle('Catégorie:Informatique'), bulle('Catégorie:nature'), bulle('Catégorie:sport')])
        graphe(page_courante)

it = interface()


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
        global it, page_courante

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
        self.affichage.append(create_rounded_rectangle(it.canvas, *bbox, radius=radius, fill="#00FFFF", outline="#026773", width=2))
        self.affichage.append(it.canvas.create_text(self.x+self.largeur/2, self.y+self.hauteur/2, text=self.val, width=bbox[2]-bbox[0]-2*padding, justify=CENTER, fill="black"))

    def ajout_lien(self, obj): ### rajoute le tracé du lien dans la variable qui stocke l'affichage
        self.affichage.append(it.canvas.create_line(obj.x+obj.largeur/2, obj.y+obj.hauteur/2, self.x+self.largeur/2, self.y+self.hauteur/2, fill="#026773"))

    def calcul(self): ### permet de trouver la largeur du rectangle
        """
        calcul la largeur du rectangle et attribue a x, y, largeur et hauteur les valeurs correspondantes
        ne renvoie rien
        """
        global it
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
    def actualisation(self): 
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
            it.canvas.tag_raise(self.affichage[i])
        for v in self.voisins:
            for i in range(2):
                it.canvas.tag_raise(v.affichage[i])
    
    def trouve_item(self, item):
        """
        item : int ou un objet du canva
        renvoie l'objet qui possede l'objet du canvas
        """
        for v in self.voisins:
            if item[0] in v.affichage:
                return v


    

### page
page_sauvegarde = wiki.page('Lune')

def recuperation_page(page, nbr=48):
    """
    page : objet wikipedia ou chaine de caractere, n : un entier positif
    renvoie un objet noeud avec n voisins
    """
    global page_sauvegarde
    print(page_sauvegarde)
    if type(page) == type('str'): 
        page = wiki.page(page)
    if page.exists() != True:
        print('non existe')
        page = page_sauvegarde
    if page.title.count('Catégorie:')>=1:
        voisins = [bulle(el.title) for el in wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
    else:
        voisins = [bulle(el.title) for el in wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
    random.shuffle(voisins)
    voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
    page_sauvegarde = page
    return noeud(page.title, voisins)

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

    it.affichage_page(obj)
    obj.affichage_noeud()


### variables
page_courante = recuperation_page('Wikipedia')
item = None
pos = [0,0]
co = 0
graphe(page_courante)

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
            it.canvas.delete('all')
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


it.canvas.bind('<Button-1>', actu_pos)
it.canvas.bind('<Double-Button-1>', clic)
it.canvas.bind('<B1-Motion>', item_bouge)
it.canvas.bind('<ButtonRelease-1>', item_remove)

it.tk.mainloop()


