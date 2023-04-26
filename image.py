from tkinter import *
from PIL import ImageTk, Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import customtkinter
import urllib.request


def recuperation_image(nom):
    url = f"https://fr.wikipedia.org/w/index.php?title={nom}&action=info"

    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")

    try : 
        obj = soup.find('table')
        soup = obj.findAll('img')
    except:
        return None

    if len(soup) > 0:
        max = None
        for el in soup:
            if str(el).count('data-file-width'):
                if max == None:
                    max = el
                if int(el['data-file-width']) > int(max['data-file-width']):
                    max = el
        soup = max
        if soup != None:
            with urllib.request.urlopen("https:"+str(soup['src'])) as u:
                image_data = u.read()
            image = Image.open(BytesIO(image_data))

            return ImageTk.PhotoImage(image)

