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
from backend.app import app
import os
import sys
from pathlib import Path
current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)
from log_app.log import log
file = "Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

# variable accessible à d'autre module
modèle = None
def parse_fichier(contents, filename): # fichier pkl juste pris en charge
    """
    fonction récupérant le contenu du fichier chargés
    :param contents: contenu du fichier chargé
    :param filename: nom du fichier chargé
    :return: un dictionaire du contenu charge des données
    """
    content_type, content_string = contents.split(',')
    print(content_type)
    decoded = base64.b64decode(content_string)
    try:
        if 'pkl' in filename:
            # pour les fichiers de type pkl
            log.info('le fichier à un format pickle')
            try:
                model = pd.read_pickle(io.BytesIO(decoded))
            except Exception as e:
                log.info('something went wrong with model loading')
                log.error(e)
            try:
                model_name = type(model).__name__
            except Exception as e:
                log.info('something went wrong with getting the name of the model')
                log.error(e)
            return model_name, model.get_params(), content_string

    except Exception as e:
        log.error(e)

def update_metadata(filename,date,table,modèle,hyperparametre,contenu):
    """
    fonction mettant à jour la table précisé
    :param filename: le nom du fichier
    :param date: la date d'aujourd'hui avec format (année , mois, jours, heure, minute)
    :param table: le nom de la table
    :return: None
    """
    modèle_table_schema = '(date,fichier,model,hyperparametre,contenu)'
    inputs = '(%s,%s,%s,%s,%s)'
    try:
        # connection à la base de donnée
        log.info('connection avec le serveur postgres')
        conn = psycopg2.connect(
            database="postgres",
            user='postgres',
            password='0000',
            host='localhost',
            port='5432'
        )
    except Exception as e:
        log.error(e)
    cursor = conn.cursor()
    sql = f"INSERT INTO {table} {modèle_table_schema} VALUES {inputs};"
    values = (date,filename,modèle,hyperparametre,contenu)
    log.info('lancement du query')
    cursor.execute(sql,values)
    log.info('Arret du curseur de la base de donnée')
    cursor.close()
    log.info('query commité')
    conn.commit()
    log.info('ferméture de la connexion à la base de donnée')
    conn.close()

def update_app(contents_modèle, filename_modèle):
    """
    fonction mettant à jour une table de la base de donnée et récupère le contenu du modèle
    :param contents_modèle: contenu fichier modèle
    :param filename_modèle: cnom du fichier modèle
    :return: None
    """
    date = str(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))  # bon format de date (année , mois, jours, heure, minute)
    log.info('mise à jours de table modèle')
    log.info('chargement du contenu du modèle')
    modèle,hyperparametre,contenu = parse_fichier(contents_modèle, filename_modèle) # récupération du contenu du fichier modèle
    hyperparametre = str(hyperparametre)
    update_metadata(filename_modèle, date, 'metadata_modèle',modèle,hyperparametre,contenu) # mise à jours de la table metadata_modèle