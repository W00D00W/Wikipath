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


recuperation_image("Survival horror")