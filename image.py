from tkinter import *
from PIL import ImageTk, Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup


def recuperation_image(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    try : 
        obj = soup.find('table')
        soup = obj.findAll('img')
    except:
        return None

    try : 
        if len(soup) > 0:
            max = soup[0]
            for el in soup:
                if int(el['data-file-width']) > int(max['data-file-width']):
                    max = el
            soup = max

            if int(soup['data-file-width']) > 50:

                response = requests.get("https:"+str(soup['src']))


                return ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
    except:
        return None




