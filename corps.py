from tkinter import *
import wikipediaapi
import requests
from bs4 import BeautifulSoup
import copy
import asyncio
import customtkinter 


from objet import interface
from objet import graphe
from algorithmie import recuperation_page
from interface import actu_pos
from interface import clic
from interface import item_bouge
from interface import item_remove


# definition de variables propres a tkinter et tkinter
wiki = wikipediaapi.Wikipedia('fr')
it = interface()
page_sauvegarde = wiki.page('Lune')


### variables
page_courante = recuperation_page('Wikipedia')
item = None
pos = [0,0]
co = 0
graphe(page_courante)



it.canvas.bind('<Button-1>', actu_pos)
it.canvas.bind('<Double-Button-1>', clic)
it.canvas.bind('<B1-Motion>', item_bouge)
it.canvas.bind('<ButtonRelease-1>', item_remove)

it.tk.mainloop()




