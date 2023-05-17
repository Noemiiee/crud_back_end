# Crud-back-end
L'applicaiton est une application Back-end qui permet à une entreprise de gérer ses plannings ainsi que ses activités

# Lancer l'application
Pour lancer l'application il sufit d'aller dans le document ./app et de lancer la commande `python -m uvicorn main:app --reload`.
L'application se lancera sur le `http://127.0.0.1:8000/docs`

# Installation de uvicorn
Pour installer uvicorn il faut **requirements:** python3.10 ou plus d'installer
Il faut aussi installer les dépendances `pip install -r requirements.txt`

# Bdd
La base de donnée est initialisé en localhost grâce au fichier `creationbdd.py`
La connexion à la Bdd s'effectue avec le fichier `connexion.py`

