import random

from corps import wiki
from objet import bulle
from objet import noeud




def recuperation_page(page, nbr=48):
    """
    page : objet wikipedia ou chaine de caractere, n : un entier positif
    renvoie un objet noeud avec n voisins
    """
    global page_sauvegarde
    print(page_sauvegarde)
    if type(page) == type('str'): 
        page = wiki.page(page)
    if page.exists() != True:
        print('non existe')
        page = page_sauvegarde
    if page.title.count('Catégorie:')>=1:
        voisins = [bulle(el.title) for el in wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
    else:
        voisins = [bulle(el.title) for el in wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
    random.shuffle(voisins)
    voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
    page_sauvegarde = page
    return noeud(page.title, voisins)