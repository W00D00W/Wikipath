#importation librairies
import webbrowser
import customtkinter

#importation des autres fichiers du projet
from noeud import *
from page import *
from image import *
from bdd import *


class interface:
    def efface(self):
        self.liste = self.tk.winfo_children()
        for element in self.liste:
            element.destroy()

    def affichage_bouton(self, values):
        self.graphe.pile.vider_pile()
        self.profondeur = 48
        # self.change_compteur(0)
        if values == 'prédefinie':
            self.recherche_page_entry.grid_forget()
            self.recherche_page_ok.grid_forget()
            self.predefini()
        else:
            self.page.page_courante = bulle('Wikipedia')
            self.recherche_page_entry.grid(row=0, column=1)
            self.recherche_page_ok.grid(row=0, column=2)
            self.page.regeneration_page(self, self.profondeur)

    def definition_taille(self):
        if self.largeur != self.tk.winfo_width() or self.hauteur != self.tk.winfo_height():
            if self.page_actuelle == 0:
                self.largeur = self.tk.winfo_width()
                self.hauteur = self.tk.winfo_height()

                ### menu
                self.barre_menu.configure(width=self.largeur, height=30)
                self.tk.update()

                hauteur_barre_menu = self.barre_menu.winfo_height()

                ### canvas
                self.canvas.configure(width=self.largeur*3/4, height=self.hauteur-hauteur_barre_menu-65)
                self.tk.update()

                ### zone droite
                hauteur_canvas = self.canvas.winfo_height()

                largeur_zone_droite = (self.largeur/4)*95/100

                self.zone_droite.configure(width=largeur_zone_droite, height=hauteur_canvas)
                self.tk.update()

                largeur_frame = self.zone_droite.winfo_width()

                self.texte[2].configure(width=largeur_frame-largeur_frame/4, height= hauteur_canvas/2.5)
                self.tk.update()

            if self.co > 0:
                if self.image_wiki != None:
                    self.texte[1].configure(width=largeur_frame, height = hauteur_canvas/4)
                    self.tk.update()

                    hpercent = (self.texte[1].winfo_height()/float(self.image_wiki.size[0]))
                    wsize = int((float(self.image_wiki.size[0])*float(hpercent)))

                    redimension = self.image_wiki.resize((wsize, self.image_wiki.size[1]), Image.Resampling.LANCZOS)
                    self.texte[1].delete('all')
                    self.img = ImageTk.PhotoImage(redimension)

                    self.image_page = self.texte[1].create_image(self.texte[1].winfo_width()/2, self.texte[1].winfo_height()/2, image=self.img)
                    self.tk.update()

                    self.texte[1].configure(height=self.image_wiki.size[1])    
                    self.tk.update()



        elif self.page_actuelle == 1 or self.page_actuelle == 2:
            self.barre_menu.configure(width=self.largeur, height=30)
            self.tk.update()     
                
    def __init__(self):
        self.page = page()
        self.arbre = None
        self.tk = customtkinter.CTk()
        self.graphe = graphe()
        self.profondeur = 48
        self.item = None
        self.pos = [0,0]
        self.co = 0
        self.largeur = 0
        self.hauteur = 0
        self.page_conn = None
        self.page_actuelle = 0
        self.image_page = None

        customtkinter.set_appearance_mode("Dark")
        self.tk.geometry(str(self.tk.winfo_screenwidth())+'x'+str(self.tk.winfo_screenheight()))
        self.tk.update()
        self.tk.grid_propagate(False)

        self.tk.grid_columnconfigure(3, weight=1)

        ### affichage canvas
        self.canvas = Canvas(self.tk, bg="white")
        self.canvas.grid(row=1, column=0)
        self.canvas.grid_propagate(False)

        self.menu() ### creation du menu 

        ### zone droite
        self.zone_droite = Frame(self.tk, bg='#bebfc2')
        self.zone_droite.grid(row=1, column=3)

        self.zone_droite.rowconfigure(0, weight=1)
        self.zone_droite.rowconfigure(1, weight=1)
        self.zone_droite.rowconfigure(2, weight=1)
        self.zone_droite.rowconfigure(3, weight=1)
        self.zone_droite.columnconfigure(0, weight=1)
        self.zone_droite.columnconfigure(1, weight=1)

        self.zone_droite.grid_propagate(False)

        ### creation du texte dans la zone droite
        self.btn_fav = customtkinter.CTkButton(self.zone_droite, text ='', image=customtkinter.CTkImage(Image.open("image/coeur_vide.png")), width=20, height=20)
        self.btn_fav.grid(row=0, column=1, padx=20)

        self.texte = [None, None, None, None, None]
        self.texte[0] = customtkinter.CTkLabel(self.zone_droite, text = '', text_color='black')
        self.texte[0].grid(row=0, column=0, columnspan=1, pady=10, sticky='snew')

        self.texte[1] = Canvas(self.zone_droite, bg='#bebfc2', bd=0, highlightbackground='#bebfc2')

        self.texte[2] = customtkinter.CTkTextbox(self.zone_droite, fg_color='transparent', text_color='black')
        self.texte[2].grid(row=2, column=0, columnspan=2)

        self.texte[3] = customtkinter.CTkButton(self.zone_droite, text = 'Aller a la page', command=lambda : webbrowser.open_new(''))
        self.texte[3].grid(row=3, column=0, columnspan=2, pady=10, sticky='S')

        self.texte[4] = customtkinter.CTkButton(self.zone_droite, text='recharger les liens', command = lambda : self.page.regeneration_page(self, self.profondeur))
        self.texte[4].grid(row=4, column=0, columnspan=2, pady=10)

        ### assignations
        self.canvas.bind('<Button-1>', self.actu_pos)
        self.canvas.bind('<Double-Button-1>', self.clic)
        self.canvas.bind('<B1-Motion>', self.item_bouge)
        self.canvas.bind('<ButtonRelease-1>', self.item_remove)
        self.tk.bind('<Button-1>', self.actu_fenetre)

        self.definition_taille()

    def menu(self):
        self.barre_menu = customtkinter.CTkFrame(master = self.tk)
        self.barre_menu.grid(row=0, column=0, columnspan=4)

        for i in range(3):
            self.barre_menu.columnconfigure(i, weight=1)

        self.barre_menu.grid_propagate(False)

        ### creation des boutons propres au menu
        if self.page_conn != None:
            text = self.page_conn.user
        text = "Se connecter / S'inscrire"
        self.login_button = customtkinter.CTkButton(self.barre_menu, text=text, command=lambda : conn(self))
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

    def affichage_page(self, page):
        self.co += 1
        page = self.page.wiki.page(page.val)
        
        sum = page.summary

        lst = sum.split(' ')

        chaine = ""
        cpt = 0
        while len(lst) > 0:
            if cpt+len(lst[0]) < 50 or len(lst[0]) > 50:
                cpt += len(lst[0]) + 1
                chaine += lst.pop(0) + ' '
            else:
                cpt = 0
                chaine += '\n'

        sum = chaine
    
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
        self.image_wiki = recuperation_image(page.title)
        if self.image_wiki != None:
            self.zone_droite.grid_columnconfigure(1, weight=1)
            self.texte[1].grid(row=1, column=0, columnspan=1)
            self.texte[1].update()
            self.texte[1].delete('all')

#####################
            hpercent = (self.texte[1].winfo_height()/float(self.image_wiki.size[0]))
            wsize = int((float(self.image_wiki.size[0])*float(hpercent)))

            redimension = self.image_wiki.resize((wsize, self.image_wiki.size[1]), Image.Resampling.LANCZOS)
            self.texte[1].delete('all')
            self.img = ImageTk.PhotoImage(redimension)

            self.image_page = self.texte[1].create_image(self.texte[1].winfo_width()/2, self.texte[1].winfo_height()/2, image=self.img)
            self.tk.update()

            self.texte[1].configure(height=self.image_wiki.size[1])    
            self.tk.update()
#######################
        else:
            self.texte[1].grid_forget()
            self.zone_droite.grid_columnconfigure(1, weight=0)
        self.texte[2].configure(state='normal')
        self.texte[2].delete(0.0, END)
        self.texte[2].insert("0.0", sum)
        self.texte[2].configure(state='disabled')
        self.texte[3].configure(command= lambda : webbrowser.open_new(page.fullurl))

    def predefini(self):
        self.canvas.delete('graphe')
        self.page.page_courante = noeud('Wikipedia', [bulle('Catégorie: Littérature'), bulle('Catégorie: histoire'), bulle('Catégorie: musique'), bulle('Catégorie: mode'), 
                            bulle('Catégorie: art'), bulle('Catégorie: culture'), bulle('Catégorie: géographie'), bulle('Catégorie: géopolitique'), 
                            bulle('Catégorie: politique'), bulle('Catégorie: culture pop'), bulle('Catégorie: philosophie'), bulle('Catégorie: mathématiques'),
                            bulle('Catégorie: Informatique'), bulle('Catégorie: nature'), bulle('Catégorie: sport')])
        self.graphe.graphe(self, self.page.page_courante)

    def genere_graphe(self):
        self.arbre = self.graphe.graphe(self, self.page.page_courante)

    ### actions
    def actu_fenetre(self, event):
        self.definition_taille()

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


### page connexion
class page_conn:
    def __init__(self, obj, user):
        self.tk = obj.tk
        self.user = user
        obj.efface()
        obj.page_actuelle = 2

        obj.menu()
        obj.definition_taille()

        self.title_label = customtkinter.CTkLabel(self.tk, text="Espace membre : bienvenue "+user)
        self.title_label.grid(row=1, column=0, padx=30, pady=15)

        text = "Vous n'avez aucune page en favori"
        if len(chercher_captures(self.user)) > 0:
            text = "Pages en favori"
        self.recherche_page = customtkinter.CTkLabel(self.tk, text=text)
        self.recherche_page.grid(row=2, column=0, padx=0, pady=50)

        if len(chercher_captures(self.user)) > 0:
            scrollable_frame = customtkinter.CTkScrollableFrame(self.tk, label_text="CTkScrollableFrame")
            scrollable_frame.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
            scrollable_frame_switches = []
            cpt = 2
            for element in chercher_captures(self.user):
                switch = customtkinter.CTkButton(master=scrollable_frame, text=element)
                switch.grid(row=cpt, column=0, padx=10, pady=(0, 20))
                scrollable_frame_switches.append(switch)
                cpt += 1

class conn:
    def __init__(self, obj):
        self.tk = obj.tk
        obj.efface()
        obj.page_actuelle = 1
        obj.menu()
        obj.definition_taille()

        # Création du titre
        self.title_label = customtkinter.CTkLabel(self.tk, text="Espace membre")
        self.title_label.grid(row=1, column=0, pady=10, columnspan=4)

        # Création des champs de saisie
        self.id_label = customtkinter.CTkLabel(self.tk, text="Nom d'utilisateur")
        self.id_label.grid(row=2, column=0, columnspan=4)
        self.id_entry = customtkinter.CTkEntry(self.tk)
        self.id_entry.grid(row=3, column=0, pady=5, columnspan=4)

        self.mdp_label = customtkinter.CTkLabel(self.tk, text="Mot de passe")
        self.mdp_label.grid(row=4, column=0, columnspan=4)
        self.mdp_entry = customtkinter.CTkEntry(self.tk, show="*")
        self.mdp_entry.grid(row=5, column=0, pady=5, columnspan=4)

        # Création d'un cadre pour les boutons
        self.button_frame = customtkinter.CTkFrame(self.tk)
        self.button_frame.grid(row=6, column=0, columnspan=4)

        # Création des boutons de connexion / inscription / mdp oublié
        self.login_button = customtkinter.CTkButton(self.button_frame, text="Se connecter", command=lambda : self.connexion(self.id_entry.get(), self.mdp_entry.get(), obj))
        self.login_button.pack(side="left", padx=10, pady=20)
        self.signup_button = customtkinter.CTkButton(self.button_frame, text="S'inscrire", command=lambda : self.inscription(self.id_entry.get(), self.mdp_entry.get(), obj))
        self.signup_button.pack(side="left", padx=10, pady=20)
        self.oublie_button = customtkinter.CTkButton(self.button_frame, text="Mdp oublié ?", command=lambda : oubl(self.id_entry.get(), obj))
        self.oublie_button.pack(side="left", padx=10, pady=20)

    def connexion(self, id, mdp, obj):
        if verif(id, mdp):
            obj.temp = page_conn(obj, id)
    
    def inscription(self, id, mdp, obj):
        if sign_up(id, mdp):
            obj.temp = page_conn(obj, id)

### oublié 
class oubl:

    def __init__(self, id, obj):
        self.tk = obj.tk
        obj.efface()
        obj.page_actuelle = 2
        obj.menu()
        obj.definition_taille()

        # Création du titre
        self.title_label = customtkinter.CTkLabel(self.tk, text="Mdp oublié")
        self.title_label.grid(row=1, column=0, pady=10, columnspan=4)

        # Création des champs de saisie
    

        self.mdp_label = customtkinter.CTkLabel(self.tk, text="Nouveau mot de passe.")
        self.mdp_label.grid(row=4, column=0, columnspan=4)
        self.mdp_entry = customtkinter.CTkEntry(self.tk, show="*")
        self.mdp_entry.grid(row=5, column=0, pady=5, columnspan=4)

        self.mdp_label2 = customtkinter.CTkLabel(self.tk, text="Confirmez votre mot de passe.")
        self.mdp_label2.grid(row=6, column=0, columnspan=4)
        self.mdp_entry2 = customtkinter.CTkEntry(self.tk, show="*")
        self.mdp_entry2.grid(row=7, column=0, pady=5, columnspan=4)

        # Création d'un cadre pour les boutons
        self.button_frame = customtkinter.CTkFrame(self.tk)
        self.button_frame.grid(row=8, column=0, columnspan=4)

        # Création des boutons de connexion / inscription / mdp oublié
        self.confirmer = customtkinter.CTkButton(self.button_frame, text="Confirmer", command=lambda : self.bouton_cliqué(id, self.mdp_entry.get(), self.mdp_entry2.get(), obj))
        self.confirmer.grid(row=9, padx=10, pady=20)
    
    def bouton_cliqué(self, id, mdp1, mdp2, obj):
        mdpoublie(id, mdp1, mdp2)
        obj.temp = page_conn(obj, id)