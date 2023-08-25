# explain

Ce projet contient les différentes possibilité de pouvoir évaluer la transparence 
d'un modèle de deep learning et machine learning à parti di jeu de donnée charger

Dockerfile : fichier contenant les paramètres de configuration du conteneur du projet.

app.py : le fichier de lancement de la platforme, associé avec la commande 'python app.py'

docker_compose.yml: fichier contenant l'infrastructure de déploiement du projet 

requirements.txt : contient les différents librairie pour propre fonctionement de l'applicaiton

explanable : contient tous ce qui concern le backend et le frontend de l'applciation

# important docker commands for composing services

- docker compose down #to destroy all what has been created
- docker-compose up --build #to buid up from scratch 
