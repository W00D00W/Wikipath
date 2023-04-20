from page import *
from noeud import *
import customtkinter

from bdd import *

from image import *
import webbrowser

class gestion_page:
    """
    permet de connecter toute les pages entres elles
    """
    def __init__(self):
        self.tk = customtkinter.CTk()
        self.largeur = 0 # largeur de la fenetre 
        self.hauteur = 0 # hauteur de la fenetre
        self.utilisateur = ''
        self.page_dico = {'page_interface' : interface(self), 'page_connexion' : conn(self), 'page_compte' : page_conn(self)}
        self.page_actuelle = self.page_dico['page_interface'] ## correspond a l'objet de la page actuelle
        self.menu = menu(self)
    
    def fenetre_affiche(self): ### une seule fois au lancement
        ### propre a l'affichage de la page
        customtkinter.set_appearance_mode("Dark")
        self.tk.geometry(str(self.tk.winfo_screenwidth())+'x'+str(self.tk.winfo_screenheight()))
        self.tk.update()
        self.tk.grid_propagate(False)
        self.page_actuelle.affichage()
        self.menu.affiche()
        self.taille()

    def taille(self):
        self.largeur = self.tk.winfo_width()
        self.hauteur = self.tk.winfo_height()
        self.tk.update()
        self.menu.taille()
        self.tk.update()
        self.page_actuelle.taille()
        
    def changement_page(self, page):
        self.page_actuelle.efface()
        self.menu.affiche()
        self.page_actuelle = self.page_dico[page]
        self.page_actuelle.affichage()
        self.taille()

class page_tkinter:
    """
    base commune a toute les pages
    """
    def __init__(self, objet):
        self.tk = objet.tk
        self.parent = objet

    def affichage(self):
        pass

    def efface(self):
        self.liste = self.tk.winfo_children()
        for element in self.liste:
            element.grid_forget()

    def taille(self):
        pass

class menu:
    """
    menu de la page d'acceuil
    """
    def __init__(self, page):
        self.parent = page
        self.tk = page.tk
        self.elements = {'barre_menu':       customtkinter.CTkFrame(master = self.tk)}
        self.elements = {**self.elements,**{
                         'bouton_connexion': customtkinter.CTkButton(self.elements['barre_menu'], command = lambda : self.parent.changement_page('page_connexion')),
                         'bouton_quitter':   customtkinter.CTkButton(self.elements['barre_menu'], text="Quitter"),
                         'recherche':        customtkinter.CTkFrame(self.elements['barre_menu'])}}
        self.elements = {**self.elements,**{
                         'valeurs':          customtkinter.CTkSegmentedButton(self.elements['recherche'], values=['prédefinie', 'rechercher'], command= lambda e: self.parent.page_dico['page_interface'].affichage_bouton(e)),
                         'valeurs_entre':    customtkinter.CTkEntry(self.elements['recherche']),
                         'recherche_valide': customtkinter.CTkButton(self.elements['recherche'], text='ok', width = 20)}}

    def affiche(self):
        """
        affiche tout les items présents dans la classe
        """
        [self.elements['barre_menu'].columnconfigure(i, weight=1) for i in range(3)]
        
        self.elements['barre_menu'].grid(row=0, column=0, columnspan=4)
        self.elements['barre_menu'].grid_propagate(False)
        self.elements['bouton_connexion'].grid(row=0, column=0, sticky='W', padx=10)
        self.elements['bouton_quitter'].grid(row=0, column=2, sticky='E', padx=10)
        self.elements['recherche'].grid(row=0, column=1)
        self.elements['valeurs'].grid(row=0, column=0)
        self.elements['valeurs_entre'].grid(row=0, column=1)
        self.elements['recherche_valide'].grid(row=0, column=5)

    def taille(self):
        self.elements['barre_menu'].configure(width=self.parent.largeur*100/125, height=30)
        self.tk.update()

class zone_droite:
    """
    zone de texte a droite du canvas sur la page principale
    """
    def __init__(self, obj):
        self.parent = obj
        self.tk = obj.tk
        self.elements = {'zone_droite' : Frame(self.tk, bg='#bebfc2')}
        self.elements = {**self.elements, **{'bouton_favori' : customtkinter.CTkButton(self.elements['zone_droite'], text ='', image=customtkinter.CTkImage(Image.open("image/coeur_vide.png")), width=20, height=20),
                                        'texte': [customtkinter.CTkLabel(self.elements['zone_droite'], text = '', text_color='black'), 
                                                Canvas(self.elements['zone_droite'], bg='#bebfc2', bd=0, highlightbackground='#bebfc2'),
                                                customtkinter.CTkTextbox(self.elements['zone_droite'], fg_color='transparent', text_color='black'),
                                                customtkinter.CTkButton(self.elements['zone_droite'], text = 'Aller a la page'),
                                                customtkinter.CTkButton(self.elements['zone_droite'], text='recharger les liens')]}}
    def affiche(self):
        """
        affiche tout les elements contenus dans le dictionnaire elements
        """
        self.elements['zone_droite'].grid(row=1, column=3)

        [self.elements['zone_droite'].rowconfigure(i, weight=1) for i in range(4)]
        [self.elements['zone_droite'].columnconfigure(i, weight=1) for i in range(2)]
        self.elements['zone_droite'].grid_propagate(False)

        self.elements['bouton_favori'].grid(row=0, column=1, padx=20)

        self.elements['texte'][0].grid(row=0, column=0, columnspan=1, pady=10, sticky='snew')
        self.elements['texte'][2].grid(row=2, column=0, columnspan=2)
        self.elements['texte'][3].grid(row=3, column=0, columnspan=2, pady=10, sticky='S')
        self.elements['texte'][4].grid(row=4, column=0, columnspan=2, pady=10)

    def affichage_page(self, page_objet):
        page = self.parent.page.wiki.page(page_objet.val)
        sum = page.summary

        titre = page.title
        
        self.elements['texte'][0].configure(text= titre)
        self.elements['image_wiki'] = recuperation_image(page.title)

        ## configuration des éléments
        ## texte résumé de wikipédia
        self.elements['texte'][2].configure(state='normal')
        self.elements['texte'][2].delete(0.0, END)
        self.elements['texte'][2].insert("0.0", sum)
        self.elements['texte'][2].configure(state='disabled')
        ## bouton changement de page
        self.elements['texte'][3].configure(command= lambda : webbrowser.open_new(page.fullurl))

class interface(page_tkinter):
    """
    page d'acceuil
    """
    def __init__(self, tk_objet):
        super().__init__(tk_objet)
        self.page = page() ### objets liés a d'autre page / correspond a l'objet qui stocke les données sur wikipédia
        self.graphe = graphe() ### objets liés a d'autre page / correspond a l'objet qui permet l'affichage du graphe

        self.item = None # variable locale / utile pour la gestion du canvas
        self.pos = [0,0]
        self.co = 0
        self.image_page = None
        self.zone_droite = zone_droite(self)

        ### canvas
        self.canvas = Canvas(self.tk, bg="white")
        self.canvas.grid_propagate(False)
        ### assignations
        self.canvas.bind('<Button-1>', self.actu_pos)
        self.canvas.bind('<Double-Button-1>', self.clic)
        self.canvas.bind('<B1-Motion>', self.item_bouge)
        self.canvas.bind('<ButtonRelease-1>', self.item_remove)
        self.tk.bind('<Button-1>', self.actu_fenetre)
    
    def affichage(self):
        super().affichage()
        self.canvas.grid(row=1, column=0)
        self.zone_droite.affiche()
        self.graphe.graphe(self, self.page.page_courante)
        

    def taille(self):
        hauteur_barre_menu = self.parent.menu.elements['barre_menu'].winfo_height()

        print(hauteur_barre_menu)

        ### canvas
        self.canvas.configure(width=self.parent.largeur*3/4, height=self.parent.hauteur-hauteur_barre_menu)
        self.tk.update()

        ### zone droite
        hauteur_canvas = self.canvas.winfo_height()

        self.zone_droite.elements['zone_droite'].configure(width=(self.parent.largeur/4)*95/100, height=hauteur_canvas)
        self.tk.update()

        largeur_frame = self.zone_droite.elements['zone_droite'].winfo_width()

        self.zone_droite.elements['texte'][2].configure(width=largeur_frame-largeur_frame/4, height= hauteur_canvas/2.5)
        self.tk.update()

    def affichage_bouton(self, values):
        """
        permet de changer de page entre prédefinie et recherche
        """
        self.graphe.pile.vider_pile()
        self.profondeur = 48
        self.canvas.delete('all')
        if values == 'prédefinie':
            self.parent.menu.elements['valeurs_entre'].grid_forget()
            self.parent.menu.elements['recherche_valide'].grid_forget()
            self.predefini()
        else:
            self.page.page_courante = bulle('Wikipedia')
            self.page.regeneration_page()
            self.parent.menu.elements['valeurs_entre'].grid(row=0, column=1)
            self.parent.menu.elements['recherche_valide'].grid(row=0, column=2)
        self.parent.changement_page('page_interface')

    def predefini(self):
        """
        permet de generer le graphe prédéfini
        """
        self.canvas.delete('graphe')
        self.page.page_courante = noeud('Wikipedia', [bulle('Catégorie: Littérature'), bulle('Catégorie: histoire'), bulle('Catégorie: musique'), bulle('Catégorie: mode'), 
                            bulle('Catégorie: art'), bulle('Catégorie: culture'), bulle('Catégorie: géographie'), bulle('Catégorie: géopolitique'), 
                            bulle('Catégorie: politique'), bulle('Catégorie: culture pop'), bulle('Catégorie: philosophie'), bulle('Catégorie: mathématiques'),
                            bulle('Catégorie: Informatique'), bulle('Catégorie: nature'), bulle('Catégorie: sport')])

    ### actions
    def actu_fenetre(self, event):
        """
        actualise la taille de la fenetre
        """
        self.parent.taille()

    def actu_pos(self, event):
        """
        actualise pos a chaque clic
        """
        self.pos[0], self.pos[1] = event.x, event.y
    
        if self.item == None:
            self.item = self.page.page_courante.trouve_item(self.canvas.find_closest(event.x, event.y))
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
            x, y = event.x-self.item.largeur/2, event.y-self.item.hauteur/2
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
        self.item =  None    
        self.page.page_courante.actualisation(self)
        for element in self.page.page_courante.voisins:
            element.actualisation(self)

class page_conn(page_tkinter):
    def __init__(self, objet):
        super().__init__(objet)

        self.title_label = customtkinter.CTkLabel(self.tk, text="Espace membre : bienvenue ")
        

        text = "Vous n'avez aucune page en favori"
        # if len(chercher_captures(self.parent.utilisateur)) > 0:
        #     text = "Pages en favori"
        self.recherche_page = customtkinter.CTkLabel(self.tk, text=text)
        
        # if len(chercher_captures(self.user)) > 0:
        #     scrollable_frame = customtkinter.CTkScrollableFrame(self.tk, label_text="CTkScrollableFrame")
        #     scrollable_frame.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #     scrollable_frame_switches = []
        #     cpt = 2
        #     for element in chercher_captures(self.user):
        #         switch = customtkinter.CTkButton(master=scrollable_frame, text=element)
        #         switch.grid(row=cpt, column=0, padx=10, pady=(0, 20))
        #         scrollable_frame_switches.append(switch)
        #         cpt += 1

    def affichage(self):
        self.title_label.grid(row=1, column=0, padx=30, pady=15)
        self.recherche_page.grid(row=2, column=0, padx=0, pady=50)
    
    def taille(self):
        pass

class conn(page_tkinter):
    def __init__(self, objet):
        super().__init__(objet)

        # Création du titre
        self.title_label = customtkinter.CTkLabel(self.tk, text="Espace membre")
        
        # Création des champs de saisie
        self.id_label = customtkinter.CTkLabel(self.tk, text="Nom d'utilisateur")
        
        self.id_entry = customtkinter.CTkEntry(self.tk)
        
        self.mdp_label = customtkinter.CTkLabel(self.tk, text="Mot de passe")
        
        self.mdp_entry = customtkinter.CTkEntry(self.tk, show="*")

        # Création d'un cadre pour les boutons
        self.button_frame = customtkinter.CTkFrame(self.tk)

        # Création des boutons de connexion / inscription / mdp oublié
        self.login_button = customtkinter.CTkButton(self.button_frame, text="Se connecter", command=lambda : self.connexion(self.id_entry.get(), self.mdp_entry.get(), obj))
        
        self.signup_button = customtkinter.CTkButton(self.button_frame, text="S'inscrire", command=lambda : self.inscription(self.id_entry.get(), self.mdp_entry.get(), obj))
        
        self.oublie_button = customtkinter.CTkButton(self.button_frame, text="Mdp oublié ?", command=lambda : oubl(self.id_entry.get(), obj))
        
    def affichage(self):
        self.title_label.grid(row=1, column=0, pady=10, columnspan=4)
        self.id_label.grid(row=2, column=0, columnspan=4)
        self.id_entry.grid(row=3, column=0, pady=5, columnspan=4)
        self.mdp_label.grid(row=4, column=0, columnspan=4)
        self.mdp_entry.grid(row=5, column=0, pady=5, columnspan=4)
        self.button_frame.grid(row=6, column=0, columnspan=4)

        self.login_button.pack(side="left", padx=10, pady=20)
        self.signup_button.pack(side="left", padx=10, pady=20)
        self.oublie_button.pack(side="left", padx=10, pady=20)

    # def connexion(self, id, mdp, obj):
    #     if verif(id, mdp):
    #         obj.temp = page_conn(obj, id)
    
    # def inscription(self, id, mdp, obj):
    #     if sign_up(id, mdp):
    #         obj.temp = page_conn(obj, id)

    
page_actuelle = gestion_page()
page_actuelle.fenetre_affiche()

page_actuelle.tk.mainloop()