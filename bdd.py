#importation librairies
import sqlite3



bdd = sqlite3.connect("bdd_user.db")
curseur = bdd.cursor()



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



#fonction pour qu'un client S'inscrive au site 
def sign_up(id, mdp):
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
    requete = """
    SELECT *
    FROM user
    WHERE id = ? AND mdp = ?;
    """
    curseur.execute(requete, (id, mdp))
    resultat = curseur.fetchall()
    if resultat == []:
        return False
    elif str(resultat[0][1]) != mdp:
        return False
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
    a = curseur.fetchall()
    return a 

