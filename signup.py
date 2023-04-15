#importation librairies
import sqlite3
import customtkinter

#importation des autres fichiers du projet
from  bdd import *
from page import *



bdd = sqlite3.connect("bdd_user.db")
curseur = bdd.cursor()


# définition de la fonction pour créer un rectangle avec des bords arrondis


# Fonction pour se connecter
def login():
    id = id_entry.get()
    mdp = mdp_entry.get()
    print(verif(id, mdp))

# Fonction pour s'inscrire
def signup():
    id = id_entry.get()
    mdp = mdp_entry.get()
    sign_up(id, mdp)

# Création de la fenêtre
tk = Tk()
tk.attributes('-fullscreen', True)
tk.update()

# Création du titre
title_label = customtkinter.CTkLabel(tk, text="Espace membre")
title_label.pack(pady=10)

# Création des champs de saisie
id_label = customtkinter.CTkLabel(tk, text="Nom d'utilisateur")
id_label.pack()
id_entry = customtkinter.CTkEntry(tk)
id_entry.pack(pady=5)

mdp_label = customtkinter.CTkLabel(tk, text="Mot de passe")
mdp_label.pack()
mdp_entry = customtkinter.CTkEntry(tk, show="*")
mdp_entry.pack(pady=5)

# Création d'un cadre pour les boutons
button_frame = customtkinter.CTkFrame(tk)
button_frame.pack()

# Création des boutons de connexion / inscription
login_button = customtkinter.CTkButton(button_frame, text="Se connecter", command=login)
login_button.pack(side="left", padx=10, pady=20)

signup_button = customtkinter.CTkButton(button_frame, text="S'inscrire", command=signup)
signup_button.pack(side="left", padx=10, pady=20)

# Lancement de la boucle principale
tk.mainloop()

# requete="""
# SELECT * 
# FROM user;
# """
# curseur.execute(requete)
# a = curseur.fetchall()
# print(a)
