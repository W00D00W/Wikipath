#importation librairies
import sqlite3
import customtkinter

#importation des autres fichiers du projet
from bddd import verif, sign_up, avant_mdp_oublie
from page import *
from pageconn import *


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

        # Création des boutons de connexion / inscription / mdp oublié
        self.login_button = customtkinter.CTkButton(self.button_frame, text="Se connecter", command=lambda : verif(self.id_entry.get(), self.mdp_entry.get()))
        self.login_button.pack(side="left", padx=10, pady=20)
        self.signup_button = customtkinter.CTkButton(self.button_frame, text="S'inscrire", command=lambda : sign_up(self.id_entry.get(), self.mdp_entry.get()))
        self.signup_button.pack(side="left", padx=10, pady=20)
        self.oublie_button = customtkinter.CTkButton(self.button_frame, text="Mdp oublié ?", command=lambda : avant_mdp_oublie(self.id_entry.get(), obj))
        self.oublie_button.pack(side="left", padx=10, pady=20)

            





