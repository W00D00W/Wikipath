#importation librairies
from tkinter import *
import customtkinter

#importation des autres fichiers du projet
from page import *



tk = Tk()
tk.attributes('-fullscreen', True)
tk.update()


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    """
    renvoie un objet canva rectangle avec les bords arrondis
    """
    points = page.arrondi(x1, y1, x2, y2, radius)
    return canvas.create_polygon(points, smooth=True, **kwargs)


title_label = customtkinter.CTkLabel(tk, text="Espace membre")
title_label.grid(row=0, column=0, padx=30, pady=15)

recherche_page = customtkinter.CTkLabel(tk, text="Pages enregistrées")
recherche_page.grid(row=4, column=0, padx=0, pady=50)

for i in range(10):
    btn = customtkinter.CTkButton(tk, text="bulle enregistrée n°%s"% i)
    btn.grid(row=i+9, column=0, pady= 3)

tk.mainloop()


# customtkinter.CTkButton(self.barre_menu, text="Se connecter / S'inscrire")