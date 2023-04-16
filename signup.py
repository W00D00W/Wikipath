#importation librairies
import sqlite3
import customtkinter

#importation des autres fichiers du projet
from  bdd import *
from page import *
from pageconn import *
from bdd import *


class conn:
    bdd = sqlite3.connect("bdd_user.db")
    curseur = bdd.cursor()

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

        # Création des boutons de connexion / inscription
        self.login_button = customtkinter.CTkButton(self.button_frame, text="Se connecter / s'inscrire", command=lambda : self.login(obj))
        self.login_button.grid(row=7, column=0, columnspan=4)

    # Fonction pour se connecter
    def login(self, obj):
        if self.mdp_entry.get() !=" " and self.id_entry.get() != " " and len(self.mdp_entry.get())>7:
            if existe(self.id_entry.get()):
                if verif(self.id_entry.get(), self.mdp_entry.get()):
                    obj.page_conn = page_conn(obj, self.id_entry.get())
            else:
                sign_up(self.id_entry.get(), self.mdp_entry.get())
                obj.page_conn = page_conn(obj, self.id_entry.get())
            





