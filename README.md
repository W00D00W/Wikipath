# Wikipath

Une appli qui vous permet d'utiliser au maximum la puissance de [Wikipédia](https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal) !

## Caractéristiques

### Visualisation des pages du site comme un graphe.

- Chaque page de Wikipédia peut être vu comme un noeud qui est lié à ses voisins (les pages voisines) par des liens hypertextes, qui sont donc dans notre ghaphe les arcs.
- Le graphe affiché correspond en tout les cas à un seul niveau, c'est à dire à une page et toutes ses voisines.
- Les pages ont un nombre variable de voisines, nous avons décidé de limiter l'affichage à 50 pour une meilleur lisibilité.
- Pour se déplacer dans le graphe, il faut double cliquer sur une bulle affichée dans le graphe.
- Quand vous arrivez sur l'appli, pour commencer à explorer vous avez le choix entre trois points de départ: 
  - La page "Wikipédia", et toutes ses voisines, qui se présente directement devant vous au lancement
  - Cliquer sur "Prédéfini" pour avoir notre sélection personnelle de Catégories
  - Cliquer sur "Rechercher" et entrer le nom d'un page, puis cliquer sur "ok"
 
 ### Interface Utilisateur

- Options de rendu dans la console (Unix et Windows)
- Interface graphique Customtkinter
- Design de l'interface sobre et minimaliste pour privilégier la lisibilité et la rendre la plus intuitive possible

#### Partie client

Nous avons voulu rendre la partie base de donnée la plus solide possible en gérant les erreurs potentielles.
- Possibilité de se connecter, ou de se créer un compte (bouton "S'inscrire / Se connecter" en haut de la page)
- Gestion des oublis de mots de passes à l'aide du bouton "mdp oublié"
- Possibilité pour l'utilisateur de se rendre sur son compte une fois connecté, où se trouve ses informations personnelles 
- L'utilisateur peut enregister un noeux sur le graphe en cliquant sur le bouton dans l'espace à droite du canva, pour le retrouver ultérieurement sur son espace personnel

#### Affichage du graphe

L'affichage du graphe est géré avec un module `canva`.
- Il est possible de bouger les points en maintenant le clic gauche dessus
- Il est possible de bouger la totalité du graphe en maintenant le clic gauche à un endroit où il n'y a pas de noeuds 

#### Encadré décrivant la page centrale du graphe

Cet encadré se trouve à droite du canva.
- Affichage du titre, du résumé et si c'est pertinent d'un image de la page qui est au centre du graphe.
- deux boutons:
  - "Aller à la page" qui ouvre la page concernée dans un navigateur web
  - "Recharger les liens" qui propose une autre sélection de liens de la même page, et qui peut aussi servie à recentrer le graphe si l'on se perd dans le canva 

 
## Installation

.exe ?

## Utilisation
