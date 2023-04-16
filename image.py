from tkinter import *
from PIL import ImageTk, Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup


def recuperation_image(nom):
    url = f"https://fr.wikipedia.org/w/index.php?title={nom}&action=info"
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    test = True
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
            if int(soup['data-file-width']) > 50:

                response = requests.get("https:"+str(soup['src']))
                print("https:"+str(soup['src']))

                return Image.open(BytesIO(response.content))



