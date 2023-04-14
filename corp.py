#importation librairies
from tkinter import *
from bs4 import BeautifulSoup

#importation des autres fichiers du projet
from pile import *
from noeud import *
from page import *
from interface import *



if __name__ == "__main__":
    it = interface()
    it.genere_graphe()



it.tk.mainloop()


