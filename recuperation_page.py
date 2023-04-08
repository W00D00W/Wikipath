import wikipediaapi
import requests
from bs4 import BeautifulSoup

wiki = wikipediaapi.Wikipedia('fr')
        
####
# recuperation des voisins de la page entré en parametre
####
def liens_rec(page, n, nbr=0):
    """
    retourne un dictionnaire contenant nbr voisins sur n niveau de profondeur, principalement pour des pages 
    """
    if nbr == 0: nbr = min(30, len(wiki.page(page).links)) ## si nbr n'est pas défini
    filtre_lien = lambda v : [el for el in v if el.ns == 0 or el.ns == 14] ## defini la fonction de tri des liens
    if type(page) == type('str'): ## condition de départ 
        voisins = filtre_lien([el for el in wiki.page(page).links.values()]) ## recupere une liste filtrée  
    else:
        voisins = filtre_lien([el for el in wiki.page(page.title).links.values()]) ## recupere une liste filtrée
    voisins = voisins[:min(nbr, len(voisins))] ## réduit la liste au nombre d'élement demandé
    if n < 1:
        return {page: voisins}
    dico = {}
    for element in [liens_rec(el, n-1, nbr) for el in voisins]:
        dico = {**dico, **element}
    return {**{page: voisins}, **dico}

####
# recuperation des voisins lié a une matiere entré en parametre
####
def recuperation_categorie(matiere, n, nbr=0):
    """
    retourne un dictionnaire contenant nbr voisins sur n niveau de profondeur, principalement pour des matieres
    """
    categorie = lambda cat: [el for el in cat.categorymembers.values() if el.ns == 0 or el.ns == 14]

    if type(matiere) == type('str'): ## pour condition de lancement
        if nbr == 0: nbr = min(40, len(wiki.page(matiere).links))
        lst_domaine = categorie(wiki.page(matiere))

    elif matiere.ns == 14:
        if nbr == 0: nbr = min(40, len(wiki.page(matiere.title).links))
        lst_domaine = categorie(wiki.page(matiere.title)) ## si categorie
    else: 
        return liens_rec(matiere, n, nbr) ## si page 
    
    print(len(lst_domaine))

    lst_domaine = lst_domaine[:min(nbr, len(lst_domaine))] ## réduit la liste au nombre d'élement demandé
    if n < 1:
        return {matiere: lst_domaine}
    dico = {}
    for element in [recuperation_categorie(el, n-1, nbr) for el in lst_domaine]:
        dico = {**dico, **element}
    return {**{matiere: lst_domaine}, **dico}


### fonction pour rechercher matiere et liens en même temps
def recuperation_page(page, n, nbr=0):
    if type(page) == type('str'): 
        if page.count('Catégorie') > 0:
            if nbr == 0: nbr = min(40, len(wiki.page(page).links))
            lst_domaine = [el for el in wiki.page(page).categorymembers.values() if el.ns == 0 or el.ns == 14]
        else:
            lst_domaine = [el for el in wiki.page(page).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée     elif page.ns == 14:
            if nbr == 0: nbr = min(40, len(wiki.page(page).links))
    elif page.ns == 14:
        if nbr == 0: nbr = min(40, len(wiki.page(page).links))
        lst_domaine = [el for el in wiki.page(page.title).categorymembers.values() if el.ns == 0 or el.ns == 14]
    else:
        if nbr == 0: nbr = min(40, len(wiki.page(page.title).links))
        lst_domaine = [el for el in wiki.page(page.title).links.values() if el.ns == 0 or el.ns == 14] ## recupere une liste filtrée
    lst_domaine = lst_domaine[:min(nbr, len(lst_domaine))] ## réduit la liste au nombre d'élement demandé
    if n < 1:
        return {page: lst_domaine}
    dico = {}
    for element in [recuperation_page(el, n-1, nbr) for el in lst_domaine]:
        dico = {**dico, **element}
    return {**{page: lst_domaine}, **dico}

####
# recherche a partir d'un lien ou d'un nom 
####
def recherche(mot):
    if mot.count('/') > 0:
        soup = BeautifulSoup(requests.get(mot).text, "html.parser")
        obj = soup.find('title').text
        print(obj[:obj.index('— Wikipédia')])
        return recuperation_page(obj[:obj.index('— Wikipédia')], 2)


print(recuperation_page('Catégorie:Histoire', 1))