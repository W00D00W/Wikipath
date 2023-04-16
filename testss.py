from tkinter import *
from PIL import ImageTk, Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup


def recuperation_image(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")

    obj = soup.find('div', class_='thumbinner')
    soup = obj.findAll('img')
    print(soup)



recuperation_image("https://fr.wikipedia.org/wiki/Wikipedia_Zero")