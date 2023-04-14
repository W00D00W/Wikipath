#importation librairies
import webbrowser
import customtkinter

#importation des autres fichiers du projet
from noeud import *
from page import *



class interface:
    def affichage_bouton(self, values):
        self.graphe.pile.vider_pile()
        self.profondeur = 48
        self.change_compteur(0)
        if values == 'prédefinie':
            self.recherche_page_entry.grid_forget()
            self.recherche_page_ok.grid_forget()
            self.predefini()
        else:
            self.page.page_courante = bulle('Wikipedia')
            self.recherche_page_entry.grid(row=0, column=1)
            self.recherche_page_ok.grid(row=0, column=2)
            self.page.regeneration_page(self, self.profondeur)
            
                
    def __init__(self):
        self.page = page()
        self.arbre = None
        self.tk = customtkinter.CTk()
        self.graphe = graphe()
        self.profondeur = 48
        self.item = None
        self.pos = [0,0]
        self.co = 0

        customtkinter.set_appearance_mode("Dark")
        self.tk.geometry(str(self.tk.winfo_screenwidth())+'x'+str(self.tk.winfo_screenheight()))
        self.tk.update()

        largeur = self.tk.winfo_width()
        hauteur = self.tk.winfo_height()

        ### affichage canva
        self.canvas = Canvas(self.tk,width = (largeur/4)*3-30, height = hauteur-160 , bd=0, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=3,rowspan=3, padx=15)

        self.tk.grid_columnconfigure(3, weight = 1)

        #### affichage menu

        self.barre_menu = customtkinter.CTkFrame(master = self.tk, width = largeur, height= 30)
        self.barre_menu.grid(row=0, column=0, columnspan=4, pady=10)

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

        self.recherche_page_ok = customtkinter.CTkButton(self.recherche, text='ok', width = 20, command= lambda : self.page.changement_page(self, self.recherche_page_entry.get()))
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

        self.texte[3] = customtkinter.CTkButton(self.zone_droite, text='recharger les liens', command = lambda : self.page.regeneration_page(self, self.profondeur))
        self.texte[3].grid(row=3, column=0, columnspan=1, pady=10)
        
        ### bind action
        self.canvas.bind('<Button-1>', self.actu_pos)
        self.canvas.bind('<Double-Button-1>', self.clic)
        self.canvas.bind('<B1-Motion>', self.item_bouge)
        self.canvas.bind('<ButtonRelease-1>', self.item_remove)

        ### bouton
        self.nb_n = customtkinter.CTkFrame(self.canvas, 100, 30)

        self.bouton_plus = customtkinter.CTkButton(self.nb_n, 20, 15, text='+', command=lambda : self.change_compteur(+1))
        self.bouton_plus.grid(row=0, column=1)

        self.bouton_moins = customtkinter.CTkButton(self.nb_n, 20, 15, text='-', command=lambda : self.change_compteur(-1))
        self.bouton_moins.grid(row=1, column=1)

        self.bouton_valide = customtkinter.CTkButton(self.nb_n, 20, 30, text='ok', command=lambda : self.page.regeneration_page(self,self.profondeur))
        self.bouton_valide.grid(row=0, column=2, rowspan = 2)

        self.compteur = customtkinter.CTkLabel(self.nb_n, 40, 30, text=self.profondeur)
        self.compteur.grid(row=0, column=0, rowspan=2)

        self.canvas.create_window((largeur/4)*3-100, hauteur-200, window=self.nb_n)

    def change_compteur(self, x):
        self.profondeur += x
        self.compteur.configure(text=self.profondeur)


    def affichage_page(self, page):
        page = self.page.wiki.page(page.val)
        
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
        self.canvas.delete('graphe')
        self.page.page_courante = noeud('Wikipedia', [bulle('Catégorie:Littérature'), bulle('Catégorie:histoire'), bulle('Catégorie:musique'), bulle('Catégorie:mode'), 
                            bulle('Catégorie:art'), bulle('Catégorie:culture'), bulle('Catégorie:géographie'), bulle('Catégorie:géopolitique'), 
                            bulle('Catégorie:politique'), bulle('Catégorie:culture pop'), bulle('Catégorie:philosophie'), bulle('Catégorie:mathématiques'),
                            bulle('Catégorie:Informatique'), bulle('Catégorie:nature'), bulle('Catégorie:sport')])
        self.graphe.graphe(self, self.page.page_courante)

    def genere_graphe(self):
        self.arbre = self.graphe.graphe(self, self.page.page_courante)


    ### actions
    def actu_pos(self, event):
        """
        actualise pos a chaque clic
        """
        self.pos[0], self.pos[1] = event.x, event.y
    
        if self.item == None:
            self.item = self.page.page_courante.trouve_item(it.canvas.find_closest(event.x, event.y))
            if self.item != None:
                if self.item.contient(event.x, event.y) != True:
                    self.item = None

    def clic(self, event):
        """
        regenere un graphe a chaque double clic
        """
        x = event.x
        y = event.y
        
        for v in self.page.page_courante.voisins:
            if x > v.x and x < v.x + v.largeur  and  y > v.y and y < v.y+v.hauteur:    
                if v.etat == False:
                    self.canvas.delete('graphe')
                    v.etat = True
                    self.graphe.pile.retour_arriere(v)
                    self.page.page_courante = v
                    self.graphe.graphe(self, v)
                else:
                    self.canvas.delete('graphe')
                    self.graphe.pile.ajout_pile(self.page.page_courante)
                    self.graphe.pile.deplacer_centre(v.x, v.y)
                    self.page.page_courante = self.page.recuperation_page(v.val)
                    self.graphe.graphe(self, self.page.page_courante)
                break

    def item_bouge(self, event):
        """
        bouge l'ensemble ou un item en fonction de la souris
        """
        if self.item is not None:
            x, y = event.x-item.largeur/2, event.y-self.item.hauteur/2
            bbox = self.graphe.arrondi(x, y, x+self.item.largeur, y+self.item.hauteur, 20)
            self.canvas.coords(self.item.affichage[0], *bbox)
            self.canvas.coords(self.item.affichage[1], x+self.item.largeur/2, y+self.item.hauteur/2)
            self.pos = self.canvas.coords(self.item.affichage[2])
            if self.item.etat == False:
                if self.page.page_courante.voisins[self.page.page_courante.voisins.index(self.item)+1].etat == False:
                    self.pos[0] = self.page.page_courante.voisins[self.page.page_courante.voisins.index(self.item)+1].x+self.item.largeur/2
                    self.pos[1] = self.page.page_courante.voisins[self.page.page_courante.voisins.index(self.item)+1].y+self.item.hauteur/2 
                if self.page.page_courante.voisins[self.page.page_courante.voisins.index(self.item)-1].etat == False:
                    self.item2 = self.page.page_courante.voisins[self.page.page_courante.voisins.index(self.item)-1]
                    self.canvas.coords(self.item2.affichage[2], self.item2.x+self.item2.largeur/2, self.item2.y+self.item2.hauteur/2, self.item.x+self.item.largeur/2, self.item.y+self.item.hauteur/2)
                    self.item2.actualisation(self)
            self.canvas.coords(self.item.affichage[2], self.pos[0], self.pos[1], x+self.item.largeur/2, y+self.item.hauteur/2)
            
            self.item.actualisation(self)
            
        else:
            self.canvas.move('graphe', event.x-self.pos[0], event.y - self.pos[1])
            self.pos[0], self.pos[1] = event.x, event.y
        

    def item_remove(self, event):
        """
        réinitialise la variable item lorsque le clic de souris est relaché
        """
        global item
        item =  None    
        self.page.page_courante.actualisation(self)
        for element in self.page.page_courante.voisins:
            element.actualisation(self)