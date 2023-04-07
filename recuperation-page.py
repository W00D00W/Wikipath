import wikipediaapi

wiki = wikipediaapi.Wikipedia('fr')

def liens_rec(page, n, nbr):
    """
    retourne un dictionnaire contenant nbr voisins sur n niveau de profondeur
    """
    voisins = [el for el in wiki.page(page).links.keys()][:min(nbr, len(wiki.page(page).links.keys()))]
    ## implementer fonction tri
    if n < 1:
        return {page: voisins}
    dico = {}
    for element in [liens_rec(el, n-1, nbr) for el in voisins]:
        dico = {**dico, **element}
    return {**{page: voisins}, **dico}


print(liens_rec('Lune', 1, 10))