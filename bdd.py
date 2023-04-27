#importation librairies
import sqlite3
from tkinter import messagebox

bdd = sqlite3.connect("base_de_donne")
curseur = bdd.cursor()

def erreur(text_erreur):
    """
    prends le texte de l'erreur en param
    affiche une erreur avec le texte passé en param
    ne renvoie rien
    """
    messagebox.showerror("Erreur", text_erreur)

#fonction pour qu'un client S'inscrive au site 
def sign_up(id, mdp, avatar):
    
    autorisation = True

    if len(id) < 4:
        erreur("Veuillez renter au moins 4 carractères pour votre nom")
        autorisation = False
    if len(mdp) < 8:
        erreur("Veuillez renter au moins 8 carractères pour votre mdp")
        autorisation = False

    curseur.execute(""" SELECT * FROM user WHERE id = ?; """, (id,))
    if curseur.fetchall() != []:
        erreur("Il y a déjà un utilisateur enregistré avec ce nom, essayez de vous connecter")
        autorisation = False

    if autorisation != False:
        curseur.execute(""" INSERT INTO user VALUES ("%s", "%s", "%s"); """ % (id, mdp, avatar))
        bdd.commit()
    return autorisation

#Fonction mdp oublié
def mdpoublie(id, nouv_mdp, conf_mdp):

    autorise = True

    if nouv_mdp != conf_mdp:
        erreur("Les deux mots de passes sont différents")
        autorise = False

    if autorise:
        curseur.execute(""" UPDATE user SET mdp = ? WHERE id = ?;""", (nouv_mdp, id))

#vérification des informations lors d'une connection d'un utilisateur
def verif(id, mdp):

    requete = """
    SELECT *
    FROM user
    WHERE id = ?;
    """
    curseur.execute(requete, (id,))
    a = curseur.fetchall()

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
        if b == []:
            erreur("Ce n'est pas le bon mot de passe.")
        else:
            return True

def chemin_avatar(utilisateur):
    curseur.execute("SELECT avatar FROM user WHERE id = ?", (utilisateur, ))
    return curseur.fetchone()[0]

#insérer dans la table "capture"
def insert_capture(noeud, id_user):
    re =  """SELECT * FROM capture WHERE id_user = ? AND nom_noeud = ?;"""
    curseur.execute(re, (id_user, noeud))
    if len(curseur.fetchall()) == 0:
        """param: noeud nom du lien STR, id_user STR"""
        requete = """
        INSERT INTO capture
        VALUES (
        ?,
        ?
        );
        """
        curseur.execute(requete, (id_user, noeud))
        bdd.commit()


def suprimer_capture(noeud, id_user):
    curseur.execute('DELETE FROM capture WHERE id_user = ? AND nom_noeud = ?', (id_user, noeud))
    bdd.commit()

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

def changer_avatar(id_user, avatar):
    requete = """
    UPDATE user 
    SET avatar = ?
    WHERE id = ?;
    """
    curseur.execute(requete, (avatar, id_user))
    bdd.commit()

if __name__ == '__main__':
    requete = """
    DROP TABLE IF EXISTS user; 
    """
    curseur.execute(requete)
    requete = """
    CREATE TABLE user (
    id STRING PRIMARY KEY,
    mdp STRING,
    avatar STRING
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


    