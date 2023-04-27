import customtkinter
import webbrowser
from PySide6 import QtGui

from page import *
from noeud import *
from bdd import *
from image import *

class gestion_page:
    """
    permet de connecter toute les pages entres elles / changer de page
    """
    def __init__(self):
        self.tk = customtkinter.CTk()
        self.largeur = 0 # largeur de la fenetre 
        self.hauteur = 0 # hauteur de la fenetre
        self.utilisateur = '' # garde en mémoire l'utilisateur connecté
        self.page_dico = {'page_interface' : interface(self), 'page_connexion' : conn(self), 'page_compte' : page_conn(self), 'mdp_oubli':mdp_oubli(self)} ## contient l'ensemble des pages
        self.page_actuelle = self.page_dico['page_interface'] ## correspond a l'objet de la page actuelle
        self.menu = menu(self) # crée l'objet qui permet d'afficher le menu

        self.tk.title("Wikipath")
        self.tk.iconbitmap("image\livre.ico")

        ### pour recuperer le ratio de la fenetre / initialise tout les parametres au lancement
        self.echelle = QtGui.QGuiApplication([]).screens()[0].devicePixelRatio()

        ### propre a l'affichage de la page 
        customtkinter.set_appearance_mode("Dark") ## la fenetre est en mode sombre
        self.tk.geometry(str(self.tk.winfo_screenwidth())+'x'+str(self.tk.winfo_screenheight())) ## défini la taille de la fenetre a la taille de l'ecran
        self.tk.update()
        self.tk.grid_propagate(False) ## la fenetre ne s'adapte pas a la taille des widget / pour que la fenetre conserve sa taille initiale
        self.page_actuelle.affichage() ## affiche la page de référence
        self.menu.affiche() ## affiche le menu
        self.taille() ## met a jour la taille des widget


    def taille(self):
        """
        ne prend rien en parametre
        redimensionne la taille des widgets present en fonction de la taille de la fenetre
        """
        self.largeur = self.tk.winfo_width() ## recupere largeur
        self.hauteur = self.tk.winfo_height() ## recupere hauteur
        self.menu.taille() ## adapte taille du menu
        self.page_actuelle.taille() ## adapte taille de la fenetre
        self.tk.update()
        
    def changement_page(self, page):
        """
        page : une chaine de caractere correspondant a une clé du dictionnaire page_dico
        change la page affiché par celle donné en parametre
        """
        [self.tk.rowconfigure(i, weight=0) for i in range(10)] ## réinitialise les parametre de la grille

        self.page_actuelle.efface() ## cache tout les widget affiché
        self.menu.affiche() ## affiche le menu a nouveau
        self.page_actuelle = self.page_dico[page] ## change la page de référence
        self.page_actuelle.affichage() ## affiche la nouvelle page
        self.taille() ## met a jour la taille des widget

class page_tkinter:
    """
    base commune a toute les pages
    """
    def __init__(self, objet):
        self.tk = objet.tk ## l'objet tkinter ou sont placé tout les widgets
        self.parent = objet  ## correspond a la classe dans laquelle le nouvel objet a été crée (correspond majoritairement à une instance de l'objet "gestion_page")

    def affichage(self):
        pass

    def efface(self):
        """
        ne renvoie rien
        enleve tout les widget de la grille / les enleve de l'ecran
        """
        for element in self.tk.winfo_children(): ## recupere la liste de widget
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
                         'bouton_quitter':   customtkinter.CTkButton(self.elements['barre_menu'], text="Quitter", command= lambda : self.parent.tk.destroy()),
                         'recherche':        customtkinter.CTkFrame(self.elements['barre_menu'])}}
        self.elements = {**self.elements,**{
                         'valeurs':          customtkinter.CTkSegmentedButton(self.elements['recherche'], values=['prédefinie', 'rechercher'], command= lambda e: self.parent.page_dico['page_interface'].affichage_bouton(e)),
                         'valeurs_entre':    customtkinter.CTkEntry(self.elements['recherche']),
                         'recherche_valide': customtkinter.CTkButton(self.elements['recherche'], text='ok', width = 20, command=lambda: self.change_page())}}

    def affiche(self):
        """
        affiche tout les items présents dans la classe
        """
        [self.elements['barre_menu'].columnconfigure(i, weight=1) for i in range(3)]

        ###  regarde si utilisateur connecté ou non
        self.elements['bouton_connexion'].configure(text='se connecter')
        if self.parent.utilisateur != '':
            self.elements['bouton_connexion'].configure(text=self.parent.utilisateur)

        self.elements['barre_menu'].grid(row=0, column=0, columnspan=4)
        self.elements['barre_menu'].grid_propagate(False)
        self.elements['bouton_connexion'].grid(row=0, column=0, sticky='W', padx=10)
        self.elements['bouton_quitter'].grid(row=0, column=2, sticky='E', padx=10)
        
        if self.elements['valeurs'].get() != 'prédefinie':
            self.elements['recherche'].grid(row=0, column=1)

            # ## réinitialise la valeur deja cliqué
            self.elements['valeurs'].destroy()
            self.elements['valeurs'] = customtkinter.CTkSegmentedButton(self.elements['recherche'], values=['prédefinie', 'rechercher'], command= lambda e: self.parent.page_dico['page_interface'].affichage_bouton(e))
            self.elements['valeurs'].grid(row=0, column=0)

            self.elements['valeurs_entre'].grid(row=0, column=1)
            self.elements['recherche_valide'].grid(row=0, column=5)

    def change_page(self):
        """
        permet de charger le graphe pour une recherche d'un utilisateur 
        """
        if self.elements['valeurs_entre'].get() != '': ## si la valeur n'est pas vide
            self.parent.page_dico['page_interface'].gen_page(self.elements['valeurs_entre'].get()) ## generere la page avec la nouvelle valeure
            self.parent.changement_page('page_interface') ## change de page pour afficher le nouveau graphe

    def taille(self):
        """
        adapte la taille du menu a la taille de la fenetre
        """
        self.elements['barre_menu'].configure(width=self.parent.largeur/self.parent.echelle, height=38/self.parent.echelle)
        self.tk.update()

class zone_droite:
    """
    zone de texte a droite du canvas sur la page principale (page interface)
    """
    def __init__(self, obj):
        self.longeur_boite_texte = 0
        self.parent = obj
        self.tk = obj.tk
        self.elements = {'zone_droite' : customtkinter.CTkFrame(self.tk)}
        self.elements = {**self.elements, **{'bouton_favori' : customtkinter.CTkButton(self.elements['zone_droite'], text ='', image=customtkinter.CTkImage(Image.open("image/coeur_vide.png")), width=20, height=20),
                                        'texte': [customtkinter.CTkLabel(self.elements['zone_droite'], text = '', text_color='white'), 
                                                Label(self.elements['zone_droite'], bg='#bebfc2', bd=0, highlightbackground='#bebfc2'),
                                                customtkinter.CTkTextbox(self.elements['zone_droite'], fg_color='transparent', text_color='white'),
                                                customtkinter.CTkButton(self.elements['zone_droite'], text = 'Aller a la page'),
                                                customtkinter.CTkButton(self.elements['zone_droite'], text='recharger les liens', command = lambda : self.parent.regenerer_page())]}}
        
    def affiche(self):
        """
        affiche tout les elements contenus dans le dictionnaire elements
        """
        self.elements['zone_droite'].grid(row=1, column=3)

        [self.elements['zone_droite'].rowconfigure(i, weight=1) for i in range(4)]
        [self.elements['zone_droite'].columnconfigure(i, weight=1) for i in range(2)]
        self.elements['zone_droite'].grid_propagate(False)

        if self.parent.parent.utilisateur != '':
            self.elements['bouton_favori'].grid(row=0, column=1, padx=20)
            self.elements['texte'][0].grid(row=0, column=0, columnspan=1, pady=10, sticky='snew')
        else:
            self.elements['texte'][0].grid(row=0, column=0, columnspan=2, pady=10, sticky='snew')
        
        self.elements['texte'][1].grid(row=1, column=0, columnspan=2)
        self.elements['texte'][2].grid(row=2, column=0, columnspan=2)

        self.elements['texte'][3].grid(row=3, column=0, columnspan=2, pady=10, sticky='S')
        self.elements['texte'][4].grid(row=4, column=0, columnspan=2, pady=10)
        
    def bouton_favoris(self, titre):
        """
        titre : une chaine de caractere correspondant au titre d'une page wikipédia
        ajoute ou suprime des favoris de l'utilisateur la page relatif a la variable titre
        """
        if titre in [el[0] for el in chercher_captures(self.parent.parent.utilisateur)]: ## si titre est dans la liste des titres contenu dans les favoris de l'utilisateur
            self.elements['bouton_favori'].configure(image = customtkinter.CTkImage(Image.open("image/coeur_vide.png"))) ## change image pour coeur vide
            suprimer_capture(titre, self.parent.parent.utilisateur) ## suprime de la bdd
        else:
            self.elements['bouton_favori'].configure(image = customtkinter.CTkImage(Image.open("image/coeur_plein.png"))) ## change image pour coeur plein
            insert_capture(titre, self.parent.parent.utilisateur) ## ajoute a la bdd

    def affichage_page(self, page_objet):
        """
        page_objet : un objet noeud
        configure les widget pour afficher les informations relatifs a la page donnée
        """
        page = self.parent.page.wiki.page(page_objet.val) ## recupere l'objet wiki a partir du nom du noeud
        self.texte = page.summary ## recupere le résumé de la page
        titre = page.title ## recupere le titre de la page

        if self.parent.parent.utilisateur != '': ## si un utilisateur est connecté
            if titre in [el[0] for el in chercher_captures(self.parent.parent.utilisateur)]:
                self.elements['bouton_favori'].configure(command = lambda : self.bouton_favoris(titre), image=customtkinter.CTkImage(Image.open("image/coeur_plein.png")))
            else:
                self.elements['bouton_favori'].configure(command = lambda : self.bouton_favoris(titre), image = customtkinter.CTkImage(Image.open("image/coeur_vide.png")))

        self.elements['texte'][0].configure(text= titre) ## affiche le titre

        ## page.title
        self.image = recuperation_image(self.parent.page.page_courante.val) ## recupere l'image de la page wiki

        self.elements['texte'][1].config(image=self.image) ## attribue l'image a un widget label
        if self.image == None: ## si il y a eu une erreur
            self.elements['texte'][1].grid_forget() ## n'affiche pas le label
        else:
            self.elements['texte'][1].grid(row=1, column=0, columnspan=2) ## affiche le label
        
        ## bouton changement de page
        self.elements['texte'][3].configure(command= lambda : webbrowser.open_new(page.fullurl)) ## envoi sur la page web de la page wiki

    def formatage_texte(self):
        """
        adapte le texte a la largeur du widget pour ne pas couper les mots en plein milieu
        """
        longeur = self.elements['texte'][2].winfo_width() // 9
        if self.elements['texte'][2].get('1.0', '1.end').split(' ')[1:6] != self.texte.split(' ')[:5] or longeur != self.longeur_boite_texte:
            self.longeur_boite_texte = longeur
            texte = self.texte.split(' ')
            cpt = 0
            chaine = ''
            while texte != []:
                if cpt+len(texte[0]) < longeur:
                    cpt += len(str(texte[0]))
                    chaine += str(texte.pop(0))+' '
                elif cpt == 0 and len(texte[0]) > longeur:
                    chaine += str(texte.pop(0))
                else:
                    cpt = 0
                    chaine += '\n'
            self.elements['texte'][2].configure(state='normal') ## réactive la boite de texte
            self.elements['texte'][2].delete(0.0, END) ## efface tout le contenu
            self.elements['texte'][2].insert("0.0", chaine) ## réecrit avec le texte formaté
            self.elements['texte'][2].configure(state='disabled') ## désactive la boite de texte pour que l'utilisateur ne puisse pas la modifier
    
    def taille(self):
        """
        adapte les widget a la taille de la fenetre
        """
        hauteur = self.elements['zone_droite'].winfo_height() - round(self.elements['texte'][1].winfo_height()) - round(self.elements['texte'][3].winfo_height()) - round(self.elements['texte'][4].winfo_height()) - round(self.elements['texte'][0].winfo_height()) - 100
        if hauteur > self.elements['texte'][2].winfo_height()+10 or hauteur < self.elements['texte'][2].winfo_height()-10:
            self.elements['texte'][2].configure(height=round(hauteur/self.parent.parent.echelle))      

class interface(page_tkinter):
    """
    page d'acceuil
    """
    def __init__(self, tk_objet):
        super().__init__(tk_objet)
        self.page = page() ### correspond a l'objet qui stocke les données sur wikipédia
        self.graphe = graphe(self) ### correspond a l'objet qui permet l'affichage du graphe

        self.item = None 
        self.pos = [0,0]
        self.image_page = None
        self.zone_droite = zone_droite(self)
        self.changement_texte = None

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
        """
        affiche les elements nécessaires
        """
        self.canvas.grid(row=1, column=0) ## affiche le canvas
        self.zone_droite.affiche() ## affiche la zone de texte a droite
        self.graphe.graphe(self.page.page_courante) ## affiche le graphe contenu dans le canvas
        
    def taille(self):
        """
        adapte la taille des widgets a la fenetre
        """
        hauteur_barre_menu = self.parent.menu.elements['barre_menu'].winfo_height() ## recupere la hauteur du menu

        ### canvas
        self.canvas.configure(width=self.parent.largeur*3/4, height=self.parent.hauteur-hauteur_barre_menu) ## ajuste la taille du canvas
        self.tk.update()

        ### zone droite
        hauteur_canvas = self.canvas.winfo_height() ## recupere la hauteur du canvas

        self.zone_droite.elements['zone_droite'].configure(width=((self.parent.largeur/4)/self.parent.echelle)*95/100, height=hauteur_canvas/self.parent.echelle*98/100) ## configure la hauteur et la largeur du frame
        self.tk.update()

        largeur_frame = self.zone_droite.elements['zone_droite'].winfo_width() ## recupere la largeur du frame

        self.zone_droite.elements['texte'][2].configure(width=largeur_frame-largeur_frame/4) ## correspond au widget de texte
        self.tk.update()

        if self.page.page_courante.val != self.changement_texte:
            self.zone_droite.formatage_texte() ## met a jour l'affichage du texte
            self.changement_texte = self.page.page_courante.val
        self.zone_droite.taille() ## met a jour les widget dans l'objet zone_droite

    def affichage_bouton(self, values):
        """
        permet de changer de page entre prédefinie et recherche
        """
        self.graphe.pile.vider_pile() ## remet la navigation a zéro
        self.canvas.delete('all')  ## suprime tout ce qui est affiché dans le canvas
        if values == 'prédefinie':
            self.parent.menu.elements['valeurs_entre'].grid_forget() ## efface la barre de recherche dans le menu
            self.parent.menu.elements['recherche_valide'].grid_forget() ## efface le bouton 'ok'
            self.predefini() ## lance la fonction pour generer le graphe prédéfini
        else:
            self.page.page_courante = bulle('Wikipedia') ## relance la page depuis wikipedia
            self.page.regeneration_page()  ### a modifier a voir plus tard 
            self.parent.menu.elements['valeurs_entre'].grid(row=0, column=1) ## affiche la barre de recherche dans le menu
            self.parent.menu.elements['recherche_valide'].grid(row=0, column=2) ## affiche le bouton 'ok'
        self.parent.changement_page('page_interface') ## change la page pour afficher le graphe

    def predefini(self):
        """
        permet de generer le graphe prédéfini
        """
        self.page.page_courante = noeud('Wikipedia', [bulle('Catégorie: Littérature'), bulle('Catégorie: histoire'), bulle('Catégorie: musique'), bulle('Catégorie: mode'), 
                            bulle('Catégorie: art'), bulle('Catégorie: culture'), bulle('Catégorie: géographie'), bulle('Catégorie: géopolitique'), 
                            bulle('Catégorie: politique'), bulle('Catégorie: culture pop'), bulle('Catégorie: philosophie'), bulle('Catégorie: mathématiques'),
                            bulle('Catégorie: Informatique'), bulle('Catégorie: nature'), bulle('Catégorie: sport')])

    def gen_page(self, page):
        """
        page : chaine de caractere correspondant au titre d'une page wiki
        permet de modifier la page courante et de vider la liste de navigation
        """
        self.canvas.delete('all') ## efface tout
        self.graphe.pile.vider_pile() 
        self.page.page_courante = self.page.recuperation_page(page) ## recupere un objet noeud de la page

    def regenerer_page(self):
        """
        permet de regenerer la page et prendre de nouveau voisins
        """
        self.canvas.delete('all') ## efface tout
        self.page.page_courante = self.page.recuperation_page(self.page.page_courante.val) ## recupere la valeur de la page actuelle
        self.graphe.graphe(self.page.page_courante) ## affiche le nouveau graphe


    """
    ACTIONS 
    """
    def actu_fenetre(self, event):
        """
        actualise la taille de la fenetre
        """
        self.parent.taille()

    def actu_pos(self, event):
        """
        actualise pos a chaque clic / permet de deplacer les items dans le canvas
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
                    self.canvas.delete('all')
                    self.graphe.pile.retour_arriere(v)
                    self.graphe.pile.deplacer_centre(v.x, v.y)
                    v.etat = True
                    self.page.page_courante = v
                    self.graphe.graphe(v, False)
                else:
                    self.canvas.delete('graphe')
                    self.page.page_courante.centre = False
                    self.graphe.pile.ajout_pile(self.page.page_courante)
                    self.graphe.pile.deplacer_centre(x, y)
                    self.page.page_courante = self.page.recuperation_page(v.val)
                    if self.page.page_courante.val in [v.val for v in self.graphe.pile.pile]:
                        self.graphe.pile.pile[:-2]
                    self.graphe.graphe(self.page.page_courante)
                [self.parent.taille() for i in range(2)]
                break ## ahahaha on l'a laissé pour la blague
    
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
    """
    page de gestion de compte : lorsque utilisateur connecté
    """
    def __init__(self, objet):
        super().__init__(objet)

        self.zone_gauche = customtkinter.CTkFrame(self.tk) ## crée une frame
        self.zone_droite = customtkinter.CTkFrame(self.tk) ## crée une frame
        
        self.bienvenue = customtkinter.CTkLabel(self.zone_gauche) 

        text = "Vous n'avez aucune page en favori"
        if len(chercher_captures(self.parent.utilisateur)) > 0:
            text = "Pages en favori"
        self.recherche_page = customtkinter.CTkLabel(self.zone_gauche, text=text)
        self.image_avatar = None 
        self.description = customtkinter.CTkLabel(self.zone_droite, text='votre avatar sur wikipath')
        self.scrollable_frame = None
        self.nouvel_avatar = customtkinter.CTkButton(self.zone_droite, text='générer un nouvel avatar', command=self.regeneration_avatar)

    def affichage(self):
        """
        permet d'afficher la page
        """
        ### zone gauche 
        self.bienvenue.configure(text=f"Espace membre : bienvenue {self.parent.utilisateur}")
        
        self.zone_gauche.grid(row=1, column=0)
        self.bienvenue.grid(row=0, column=0, padx=30, pady=15)
        self.recherche_page.grid(row=1, column=0, padx=0, pady=50)

        self.zone_droite.columnconfigure(0, weight=1)
        [self.zone_droite.rowconfigure(i, weight=1) for i in range(2)]

        ## si l'utilisateur à enregistré des noeuds
        if len(chercher_captures(self.parent.utilisateur)) > 0:
            self.recherche_page.grid_forget()
            self.scrollable_frame = customtkinter.CTkScrollableFrame(self.zone_gauche, label_text="vos page en favoris")
            self.scrollable_frame.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(0, weight=1)
            scrollable_frame_switches = []
            cpt = 2
            nom_page = []
            for element in chercher_captures(self.parent.utilisateur):
                nom_page.append(element)
                switch = customtkinter.CTkButton(master=self.scrollable_frame, text=element, command= lambda el = element: self.load(el))
                switch.grid(row=cpt, column=0, padx=10, pady=(0, 20))
                scrollable_frame_switches.append(switch)
                cpt += 1

        ### zone droite
        self.zone_droite.grid(row=1, column=1)
        ## creation de l'image
        if self.image_avatar == None:
            self.avatar_chemin = Image.open(chemin_avatar(self.parent.utilisateur))
            self.image_finale = ImageTk.PhotoImage(self.avatar_chemin)
            self.image_avatar = Label(self.zone_droite, image=self.image_finale)     

        self.image_avatar.grid(row=0, rowspan=1, column=0, columnspan=1)
        self.description.grid(row=1, column=0)
        self.nouvel_avatar.grid(row=2, column=0)

    def taille(self):
        """
        permet de redimensioner les widget pour s'adapter a la taille de la fenetre
        """
        self.zone_gauche.grid_propagate(False)
        self.zone_droite.grid_propagate(False)

        self.zone_gauche.configure(width=self.parent.largeur/4*2/self.parent.echelle-100, height=self.parent.hauteur/self.parent.echelle-100)

        self.zone_droite.configure(width=((self.parent.largeur/4)*2)/self.parent.echelle-100, height=self.parent.hauteur/self.parent.echelle-100)

        self.tk.rowconfigure(0, weight=1)
        self.tk.rowconfigure(1, weight=1)
        self.tk.rowconfigure(2, weight=0)
        self.tk.rowconfigure(3, weight=0)

        if self.scrollable_frame != None:
            self.scrollable_frame.configure(width= self.parent.largeur/4*2/self.parent.echelle-150, height=self.parent.hauteur/self.parent.echelle-300)
        
        if self.image_avatar != None:
            largeur = int(round(self.parent.hauteur//1.5 * self.image_avatar.winfo_width() / self.image_avatar.winfo_height()))
            self.avatar_chemin = self.avatar_chemin.resize((largeur, int(self.parent.hauteur//1.5)), resample=Image.Resampling.LANCZOS)
            self.image_finale = ImageTk.PhotoImage(self.avatar_chemin)
            self.image_avatar.configure(image=self.image_finale)
            self.image_avatar.update()

            
    def load(self, page):
        """
        permet d'afficher un lien capturé par l'utilisateur
        """
        self.parent.page_dico['page_interface'].gen_page(page[0])
        self.parent.changement_page('page_interface')

    def regeneration_avatar(self):
        aleatoire = random.randint(1,13) ## choisi un nombre aléatoire
        changer_avatar(self.parent.utilisateur, str('avatar/'+str(aleatoire)+'.jpg')) ## change dans la base de donnée
        self.image_avatar = None ## réinitialise pour prendre la nouvelle valeur
        self.parent.changement_page('page_compte') ## recharge la page de compte

class conn(page_tkinter):
    """
    page de connexion
    """
    def __init__(self, objet):
        super().__init__(objet)

        # Création du titre
        self.title_label = customtkinter.CTkLabel(self.tk, text="Espace membre")
        
        # Création du widget de recuperation de texte
        self.id_label = customtkinter.CTkLabel(self.tk, text="Nom d'utilisateur")
        
        self.id_entry = customtkinter.CTkEntry(self.tk)
        
        self.mdp_label = customtkinter.CTkLabel(self.tk, text="Mot de passe")
        
        self.mdp_entry = customtkinter.CTkEntry(self.tk, show="*")

        # Création du frame
        self.button_frame = customtkinter.CTkFrame(self.tk)

        # Création des boutons de connexion / inscription / mdp oublié
        self.login_button = customtkinter.CTkButton(self.button_frame, text="Se connecter", command=lambda : self.connexion(self.id_entry.get(), self.mdp_entry.get()))
        
        self.signup_button = customtkinter.CTkButton(self.button_frame, text="S'inscrire", command=lambda : self.inscription(self.id_entry.get(), self.mdp_entry.get()))
        
        self.oublie_button = customtkinter.CTkButton(self.button_frame, text="Mdp oublié ?", command=lambda : self.parent.changement_page('mdp_oubli'))
        
    def affichage(self):
        """
        permet d'afficher tout les widget de la page
        """
        if self.parent.utilisateur != '': ## si l'utilisateur est deja connecté alors bascule sur la page de connexion
            self.parent.changement_page('page_compte')
        else:
            self.title_label.grid(row=1, column=0, pady=10, columnspan=4)
            self.id_label.grid(row=2, column=0, columnspan=4)
            self.id_entry.grid(row=3, column=0, pady=5, columnspan=4)
            self.mdp_label.grid(row=4, column=0, columnspan=4)
            self.mdp_entry.grid(row=5, column=0, pady=5, columnspan=4)
            self.button_frame.grid(row=6, column=0, columnspan=4)

            self.login_button.pack(side="left", padx=10, pady=20)
            self.signup_button.pack(side="left", padx=10, pady=20)
            self.oublie_button.pack(side="left", padx=10, pady=20)

    def connexion(self, id, mdp):
        """
        verifie si un utilisateur existe et si son mot de passe est bon / si oui change de page et amene sur la page de compte
        """
        if verif(id, mdp):
            self.parent.utilisateur = str(id)
            self.parent.changement_page('page_compte')
    
    def inscription(self, id, mdp):
        """
        inscrit un nouvel utilisateur dans la bdd et change la page pour la page de compte
        """
        if sign_up(id, mdp, str('avatar/'+str(random.randint(1, 13))+'.jpg')):
            self.parent.utilisateur = str(id)
            self.parent.changement_page('page_compte')

class mdp_oubli(page_tkinter):
    """
    page de changement de mot de passe
    """
    def __init__(self, objet):
        super().__init__(objet)

        # Création du titre
        self.title_label = customtkinter.CTkLabel(self.tk, text="Mdp oublié")
        
        self.mdp_label = customtkinter.CTkLabel(self.tk, text="Nouveau mot de passe.")
        self.mdp_entry = customtkinter.CTkEntry(self.tk, show="*")
        self.mdp_label2 = customtkinter.CTkLabel(self.tk, text="Confirmez votre mot de passe.")
        self.mdp_entry2 = customtkinter.CTkEntry(self.tk, show="*")
        
        # Création du frame
        self.button_frame = customtkinter.CTkFrame(self.tk)

        # Création des boutons de connexion / inscription / mdp oublié
        self.confirmer = customtkinter.CTkButton(self.button_frame, text="Confirmer", command=lambda : self.bouton_clic(self.parent.utilisateur, self.mdp_entry.get(), self.mdp_entry2.get()))
        
    
    def affichage(self):
        """
        affiche tout les elements
        """
        self.title_label.grid(row=1, column=0, pady=10, columnspan=4)
        self.mdp_label.grid(row=4, column=0, columnspan=4)
        self.mdp_entry.grid(row=5, column=0, pady=5, columnspan=4)
        self.mdp_label2.grid(row=6, column=0, columnspan=4)
        self.mdp_entry2.grid(row=7, column=0, pady=5, columnspan=4)
        self.button_frame.grid(row=8, column=0, columnspan=4)
        self.confirmer.grid(row=9, padx=10, pady=20)

    def bouton_clic(self, id, mdp1, mdp2):
        """
        verifie si les deux mots de passe correspondent et change le mot de passe
        """
        mdpoublie(id, mdp1, mdp2)
        self.parent.changement_page('page_connexion')

if __name__ == '__main__':   
    page_actuelle = gestion_page()

    page_actuelle.tk.mainloop()