#importation librairies
from tkinter import *
import customtkinter

#importation des autres fichiers du projet
from page import *
from bdd import *


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


