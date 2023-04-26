import tkinter as tk
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO

# Créer une fenêtre Tkinter
root = tk.Tk()


def afficher_image(url):
    try:
        # Ouvrir l'URL et charger l'image
        with urllib.request.urlopen(url) as u:
            image_data = u.read()
        image = Image.open(BytesIO(image_data))
        
        # Convertir l'image en PhotoImage pour l'afficher dans un widget Label
        image = ImageTk.PhotoImage(image)
        
        # Mettre à jour l'affichage de l'image
        label_image.config(image=image)
        label_image.image = image
    except Exception as e:
        print("Erreur : ", e)



label_image = tk.Label(root)
label_image.pack()

root.mainloop()