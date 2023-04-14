from tkinter import *
from bs4 import BeautifulSoup

from pile import *
from noeud import *
from page import *
from interface import *



if __name__ == "__main__":
    it = interface()
    it.genere_graphe()



#définition des variables
item = None
pos = [0,0]
co = 0



it.tk.mainloop()


