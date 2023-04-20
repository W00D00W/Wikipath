# Wikipath

Une appli qui vous permet d'utiliser au maximum la puissance de [Wikipédia](https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal) !

## Caractéristiques

### Visualisation des pages du site comme un graphe.

- Chaque page de Wikipédia peut être vu comme un nœud qui est lié à ses voisins (les pages voisines) par des liens hypertextes, qui sont donc dans notre graphe les arcs.
- Le graphe affiché correspond à un seul niveau, c'est à dire à une page et toutes ses voisines.
- Les pages ont un nombre variable de voisines, nous avons décidé de limiter l'affichage à 50 pour une meilleure lisibilité.
- Les données relatives au site Wikipédia sont les données du site en temps réel, car elle sont directement demandées par l'API de Wikipédia. Il n'y a donc pas de problème de mise à jour ou de données obsolètes.

### Utilisation / stockage des données

- Les données des clients sont stockées dans une base de donnée relationnelle, gérée avec le language SQL. Elle comprend le nom d'utilisateur de chaque client, son mots de passe, sa photo de profil et les nœuds qu'il enregistre au fur et à mesure de son parcours sur l'application.
- Les comptes ne sont pas très sécurisé car il est possible de changer le mot de passe à partir du nom d'utilisateur.

 ### Interface Utilisateur

- Interface graphique Customtkinter
- Design de l'interface sobre et minimaliste pour privilégier la lisibilité et la rendre la plus intuitive possible

#### Partie client

Nous avons voulu rendre la partie base de données la plus solide possible en gérant les erreurs potentielles.
- Possibilité de se connecter, ou de se créer un compte (bouton "S'inscrire / Se connecter" en haut de la page).
- Gestion des oublis de mots de passes à l'aide du bouton "mdp oublié"
- Possibilité pour l'utilisateur de se rendre sur son compte une fois connecté, où se trouve ses informations personnelles 
- L'utilisateur peut enregistrer un nœud sur le graphe en cliquant sur le bouton dans l'espace à droite du canvas, pour le retrouver ultérieurement sur son espace personnel

#### Affichage du graphe

L'affichage du graphe est géré avec un wiget `canvas` du module `Tkinter`.
- Il est possible de bouger les points en maintenant le clic gauche dessus
- Il est possible de se déplacer dans le canvas en maintenant le clic gauche à un endroit où il n'y a pas de nœuds
- Pour se déplacer dans le graphe, il faut double cliquer sur une bulle affichée dans le graphe.

#### Déplacement dans le graphe

- Quand vous arrivez sur l'appli, pour commencer à explorer vous avez le choix entre quatre points de départ: 
  - La page "Wikipédia", et toutes ses voisines, qui se présente directement devant vous au lancement
  - Cliquer sur "Prédéfini" pour avoir notre sélection personnelle de Catégories
  - Cliquer sur "Rechercher" et entrer le nom d'une page, puis cliquer sur "ok"
  - Aller sur votre espace personnel et partir d'une page qui a au préalable été enregistrée
 
#### Encadré décrivant la page centrale du graphe

A droite de l’application se trouve un encadré décrivant la page « courante » du graphe.
- Affichage du titre, du résumé (Wikipédia met à disposition des résumés de ses pages) et si c'est pertinent d'une image de la page qui est au centre du graphe.
- deux boutons:
  - "Aller à la page" qui ouvre la page concernée dans un navigateur web
  - "Recharger les liens" qui propose une autre sélection de liens de la même page, et qui peut aussi servir à recentrer le graphe si l'on se perd dans le canvas 

 
## Installation

.exe ?

## Utilisation
