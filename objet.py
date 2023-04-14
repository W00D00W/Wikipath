from tkinter import *
import customtkinter
import webbrowser

from interface import *
from corps import wiki
from corps import page_courante



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
        self.etat = True

    def affichage_noeud(self):
        """
        permet d'afficher le noeud ainsi que tout les voisins
        ne prend rien en parametre
        ne renvoie rien
        """
        super().affichage_noeud()
        if self.etat == True:
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


### pile
class pile:
    def __init__(self):
        self.pile = []
    
    def ajout_pile(self, x):
        self.pile.append(page_courante)
        self.pile[-1].etat = False
    
    def retirer_pile(self):
        return self.pile.pop(-1)
    
    def deplacer_centre(self, x, y):
        self.pile[-1].x = self.pile[-1].x - x
        self.pile[-1].y = self.pile[-1].y - y
        print(self.pile[-1].x, self.pile[-1].y)

    def affiche_pile(self):
        global it
        print(len(self.pile))
        for element in self.pile:
            element.affichage_noeud()



