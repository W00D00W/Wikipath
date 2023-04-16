#importation librairies
import sqlite3
import tkinter as tk
from tkinter import messagebox


bdd = sqlite3.connect("bdd_user.db")
curseur = bdd.cursor()

def erreur(text_erreur):
    """
    prends le texte de l'erreur en param
    affiche une erreur avec le texte passé en param
    ne return rien
    """
    messagebox.showerror("Erreur", text_erreur)



#fonction pour qu'un client S'inscrive au site 
def sign_up(id, mdp):
    
    autorisation = True

    if len(id) < 4:
        erreur("Veuillez renter au moins 4 carractères pour votre nom")
        autorisation = False
    if len(mdp) < 8:
        erreur("Veuillez renter au moins 8 carractères pour votre mdp")
        autorisation = False

    requete = """
    SELECT *
    FROM user
    WHERE id = ?;
    """
    curseur.execute(requete, (id,))
    a = curseur.fetchall()
    print(a)
    if a != []:
        erreur("Il y a déjà un utilisateur enregistré avec ce nom, essayez de vous connecter")
        autorisation = False

    if autorisation != False:
        requete = """
    INSERT INTO user
    VALUES ("%s", "%s");
    """ % (id, mdp)
        curseur.execute(requete)


#Fonction mdp oublié
def mdp_oublie(id, nouv_mdp):
    requete = """
    UPDATE user
    SET mdp = ?
    WHERE id = ?;
    """
    curseur.execute(requete, (nouv_mdp, id))



#vérification des informations lors d'une connection d'un utilisateur
def verif(id, mdp):

    autorisation = True

    requete = """
    SELECT *
    FROM user
    WHERE id = ?;
    """
    curseur.execute(requete, (id,))
    a = curseur.fetchall()
    print(a)


    if a == []:
        erreur("Il n'y a pas de compte avec cet identifiant sur cette appli.")
    else:
        requete = """
        SELECT *
        FROM user
        WHERE id = ? AND mdp = ?;
        """
        curseur.execute(requete, (id, mdp))
        b = curseur.fetchall()
        print(b)
        print("rr")
        if b == []:
            erreur("Ce n'est pas le bon mot de passe.")
        else:
            return True
        
    

    
    


#insérer dans la table "capture"
def insert_capture(noeud, id_user):
    """param: noeud nom du lien STR, id_user STR"""
    requete = """
    INSERT INTO capture
    VALUES (
    ?,
    ?
    );
    """
    curseur.execute(requete, (id_user, noeud))


#appel la fonction d'insertion
def enregistrer_noeud(noeud_obj, id_user ):
    #le param "noeud_obj" est un objet
    insert_capture(noeud_obj.val, id_user)



def chercher_captures(id_user):
    requete = """
    SELECT nom_noeud
    FROM capture
    WHERE id_user = ?;
    """
    curseur.execute(requete, (id_user,))
    return curseur.fetchall()



if __name__ == '__main__':
    requete = """
    DROP TABLE IF EXISTS user; 
    """
    curseur.execute(requete)
    requete = """
    CREATE TABLE user (
    id SRING PRIMARY KEY,
    mdp STRING
    );
    """
    curseur.execute(requete)

    requete = """
    DROP TABLE IF EXISTS capture; 
    """
    curseur.execute(requete)
    requete = """
    CREATE TABLE capture (
    id_user STRING REFERENCES user (id),
    nom_noeud STRING,
    PRIMARY KEY (id_user, nom_noeud));
    """
    curseur.execute(requete)