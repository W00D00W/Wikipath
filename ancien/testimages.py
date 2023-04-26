from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import random
import os


# Obtenir le chemin absolu du répertoire de travail actuel
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

# Spécifier le nom du dossier contenant les images
avatar_dirname = 'avatar'

# Combinez le chemin absolu du répertoire de travail avec le nom du dossier "avatar"
avatar_dir = os.path.join(current_dir, avatar_dirname)
print(avatar_dir)

# Obtenir la liste des noms de fichiers d'images dans le dossier "avatar"
image_files = [os.path.join(avatar_dir, file) for file in os.listdir(avatar_dir) if file.endswith('.jpg') or file.endswith('.png')]
print(image_files)

# Choisir une image aléatoire à partir de la liste
random_image_file = random.choice(image_files)

# Ouvrir l'image aléatoire
image = Image.open(random_image_file)

# Redimensionner l'image pour s'adapter à un cercle
image = image.resize((200, 200))
mask = Image.new('L', (200, 200), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 200, 200), fill=255)
image.putalpha(mask)

# Créer une fenêtre Tkinter et afficher l'image
root = tk.Tk()
img = ImageTk.PhotoImage(image)
panel = tk.Label(root, image=img)
panel.pack(side="top", fill="both", expand="yes")
root.mainloop()