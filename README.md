# Projet_9_OC

# Clonage du projet
git clone https://github.com/hgxv/Projet_9_OC NomDuDossier

# On se déplace dans le projet
cd NomDuDossier

# Création de l'environnement virtuel
py -m venv env

# Activation de l'environnement virtuel
      # Pour windows:
      env\scripts\activate
      
      #Pour Linux:
      source bin/env/activate

# Installation des dépendances
py -m pip install -r requirements.txt

# On se déplace dans l'application
cd LITReview

# Lancement du serveur virtuel
py manage.py runserver
