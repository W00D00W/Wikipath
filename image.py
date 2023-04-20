from tkinter import *
from PIL import ImageTk, Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import customtkinter


def recuperation_image(nom):
    url = f"https://fr.wikipedia.org/w/index.php?title={nom}&action=info"

    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")

    try : 
        obj = soup.find('table')
        soup = obj.findAll('img')
    except:
        return None

    try : 
        if len(soup) > 0:
            print('ok')
            max = None
            for el in soup:
                if str(el).count('data-file-width'):
                    if max == None:
                        max = el
                    if int(el['data-file-width']) > int(max['data-file-width']):
                        max = el
            soup = max
            print(soup)
            if soup != None:
                response = requests.get("https:"+str(soup['src']))

                return customtkinter.CTkImage(Image.open(BytesIO(response.content)))
    except:
        return None

def configuration_image(objet, image):
    ### definition taille fenetre
    if image != None:
        hpercent = (objet.texte[1].winfo_height()/float(objet.image.size[0]))
        wsize = int((float(objet.image.size[0])*float(hpercent)))

        ### redimensionne l'objet
        redimension = objet.image.resize((wsize, objet.image.size[1]), Image.Resampling.LANCZOS)
        objet.elements['texte'][1].delete('all') ## on suprime tout ce qui à été affiché
        objet.img = ImageTk.PhotoImage(redimension) ## crée une instance de l'image

        ## mise a jour des éléments
        objet.elements['image_wiki'] = objet.texte[1].create_image(objet.texte[1].winfo_width()/2, objet.texte[1].winfo_height()/2, image=objet.img)
        objet.tk.update()

        objet.elements['texte'][1].configure(height=objet.elements['image_wiki'].size[1])    
        objet.tk.update()
    else:
        ## on oublie le canvas / a modifier pour afficher une image prédéfinie
        objet.elements['texte'][1].grid_forget()