import wikipediaapi


wiki = wikipediaapi.Wikipedia('fr')

def liens_rec(page, n, nbr):
    voisins = [el for el in wiki.page(page).links.keys()][:nbr]
    if n == 1:
        return [[page, voisins]]
    return [[page, voisins]] + [liens_rec(el, n-1, nbr) for el in voisins]

print(liens_rec('Python (langage)', 2, 10))