"""
 fichier permetant de chargé le fichier de modèle et de mettre à jour le metadata donnée
"""
from dash import *
import dask.dataframe as dd
import datetime
import psycopg2
from psycopg2.extras import Json, DictCursor
import json
import pandas as pd
import io
import base64
from Explanable.backend.server import app
import os
import sys
from pathlib import Path
current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)
from Explanable.log_app.log import log

file = "explain/Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
print('the log file is ', logfile)
print('the current directory is', current_dir)
logger = log()
log = logger.log(logfile)

# variable accessible à d'autre module
modèle = None
def parse_fichier(contents, filename): # fichier pkl juste pris en charge
    """
    fonction récupérant le contenu du fichier chargés

    :param contents: contenu du fichier chargé
    :param filename: nom du fichier chargé

    :return: [nom_modèle, modèle_paramètre, base64encode] 
    un dictionaire du contenu charge des données
    """
    content_type, content_string = contents.split(',')
    print(content_type)
    decoded = base64.b64decode(content_string)
    try:
        if 'pkl' in filename:
            # pour les fichiers de type pkl
            log.info('le fichier à un format pickle')
            try:
                model = pd.read_pickle(io.BytesIO(decoded)) # to implement joblib we need to review the code
            except Exception as e:
                log.info('something went wrong with model loading')
                log.error(e)
            try:
                model_name = type(model).__name__
            except Exception as e:
                log.info('something went wrong with getting the name \
                         of the model')
                log.error(e)
            return model_name, model.get_params(), content_string

    except Exception as e:
        log.error(e)

def connection_à_la_base_de_donnée():
    """
    fonction permettant de se connecté à la base de pur les données chargé 
    sur la platforme

    :return: connection [objet] (objet de connection à la base de donnée)
    """
    try:
        log.info('connection avec le serveur postgres')
        connection= psycopg2.connect(
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port='5432'
        )
    except Exception as e:
        log.error(e)
    
    return connection
        

def excution_de_la_requète_de_la_base_de_donnée(objet_de_connection,requete,valeurs_de_la_requete):
    """
    fonction permetant d'exécuté une requete sur une base de donnée à partir 
    d'un objet de connexion à cette base de donnée

    :param objet_de_connection: objet de connection à la base de donnée [objet]
    :param requete: requete SQL sur la base de donnée [string]
    :param valeurs_de_la_requete: valeurs à insérer dans la requete pour la 
    base de donnée

    return: None
    """

    curseur_de_la_base_donnée = objet_de_connection.cursor()

    log.info('lancement du query')
    curseur_de_la_base_donnée.execute(requete,valeurs_de_la_requete)

    log.info('Arret du curseur de la base de donnée')
    curseur_de_la_base_donnée.close()


def validation_et_feméture_de_la_base_de_donnée(objet_de_connection):
    """
    fonction permetant de validté des requetes de la base de donnée et 
    aussi de fermé la base de donnée

    :param objet_de_connection: objet de connection à la base de donnée

    return: None
    """
    log.info('query commité')
    objet_de_connection.commit()

    log.info('ferméture de la connexion à la base de donnée')
    objet_de_connection.close()


def insertion_des_données_dans_base_de_donnée(objet_de_connection,date_stocké,fichier_modèle,parametre_modèle,\
                                              base64contenu_modèle,table):
    """
    fonction permetant d'inséré les données dans la base de données

    :param objet_de_connection: objet de connection à la base de donnée
    :param date_stocké: date de stockage de la donnée
    :param fichier_modèle: nom du fichier modèele chargé sur la platforme
    :param parametre_modèle: hyperparamètre du modèle
    :param base64contenu_modèle: contenu du modèle encodé
    :param table: nom de la table ou stocké la donnée

    return: None
    """
    modèle_table_schema = '(date,fichier,model,hyperparametre,contenu)'
    valeurs = '(%s,%s,%s,%s,%s)'

    requete = f"INSERT INTO {table} {modèle_table_schema} VALUES {valeurs};"
    valeurs_de_la_requete = (date_stocké,fichier_modèle, modèle, parametre_modèle, base64contenu_modèle)

    excution_de_la_requète_de_la_base_de_donnée(objet_de_connection,requete,valeurs_de_la_requete)    

    validation_et_feméture_de_la_base_de_donnée(objet_de_connection)


def mise_à_jour_des_metadata_de_la_base_de_donnée_pour_modèle(fichier_modèle,date,table,modèle,\
                                                              parametre_modèle,contenu):
    """
    fonction mettant à jour la table précisé

    :param filename: le nom du fichier
    :param date: la date d'aujourd'hui avec format (année , mois, jours, heure, minute)
    :param table: le nom de la table

    :return: None
    """

    resultat = connection_à_la_base_de_donnée()



def information_sur_le_modèle_chargé():
    """
    fonction montrant l'information sur les module chargé 

    :param module: information sur le module chargé [objet]
    """
    log.info('mise à jours de table modèle')
    log.info('chargement du contenu du modèle')


def update_app(contenu_du_modèle, nom_du_fichier_du_modèle):
    """
    fonction mettant à jour une table de la base de donnée et récupère le 
    contenu du modèle
    :param contents_modèle: contenu fichier modèle
    :param filename_modèle: cnom du fichier modèle
    :return: None
    """
    date_daujourdhui = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) 
    information_sur_le_modèle_chargé()
    modèle,hyperparametre,contenu = parse_fichier(contenu_du_modèle, nom_du_fichier_du_modèle)
    hyperparametre = str(hyperparametre)
    mise_à_jour_des_metadata_de_la_base_de_donnée_pour_modèle(nom_du_fichier_du_modèle, date_daujourdhui, \
                                                              'metadata_modèle',modèle,hyperparametre,contenu) 