#importation librairies
from tkinter import *
import customtkinter

#importation des autres fichiers du projet
from page import *


class page_conn:
    def __init__(self, obj, user, mdp):
        self.tk = obj.tk
        self.user = user
        self.mdp = mdp
        obj.efface()
        obj.page_actuelle = 2

        self.title_label = customtkinter.CTkLabel(self.tk, text="Espace membre : bienvenue "+user)
        self.title_label.grid(row=0, column=0, padx=30, pady=15)

        self.recherche_page = customtkinter.CTkLabel(self.tk, text="Pages enregistrées")
        self.recherche_page.grid(row=4, column=0, padx=0, pady=50)


