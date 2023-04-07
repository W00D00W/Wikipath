import wikipediaapi

wiki = wikipediaapi.Wikipedia('fr')

def tri_lien(voisins, page): ## optimiser !!
    a = wiki.page(page).links
    b = []
    for el in voisins:
        if a[el].ns == 0:
            b.append(el)
    return b
        

def liens_rec(page, n, nbr):
    """
    retourne un dictionnaire contenant nbr voisins sur n niveau de profondeur
    """
    voisins = tri_lien([el for el in wiki.page(page).links.keys()], page)
    voisins = voisins[:min(nbr, len(voisins))]
    if n < 1:
        return {page: voisins}
    dico = {}
    for element in [liens_rec(el, n-1, nbr) for el in voisins]:
        dico = {**dico, **element}
    return {**{page: voisins}, **dico}


print(liens_rec('Lune', 2, 10))