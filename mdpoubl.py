#importation librairies
import sqlite3
import customtkinter

#importation des autres fichiers du projet
from  bdd import *
from page import *
from pageconn import *
from bdd import *


class oubl:
    bdd = sqlite3.connect("bdd_user.db")
    curseur = bdd.cursor()

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
        self.confirmer = customtkinter.CTkButton(self.button_frame, text="Confirmer", command=lambda : mdpoublie(id, self.mdp_entry.get(), self.mdp_entry2.get();*, obj))
        self.confirmer.pack(side="left", padx=10, pady=20)
    
