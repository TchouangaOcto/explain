"""
fichier permetant de chargé le fichier de donnée et mettre à jour le metadata donnée
"""
from dash import *
import dask.dataframe as dd
import datetime
import psycopg2
import pandas as pd
import io
import base64
from Explanable.backend.app import app
import os
import sys
from pathlib import Path
current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)
sys.path.append(os.path.join(current_dir, 'log'))
from log import log

# instance de log
file = "Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

filename = ''

# css style
style_header = {
            'backgroundColor': '#96B9C4',
            'color': '#F3FBFB',
            'fontWeight': 'bold'
        }

style_header_conditional = [
            {'if': {'column_id': 'id', },
             'display': 'None', }]

style_cell = {
            'font-family': 'Overpass'
        }

style_data = {
            'color': 'black',
            'backgroundColor': 'white',
            'whiteSpace': 'normal',
            'height': 'auto',

        }

style_table = {'overflowX': 'auto'}

style_data_conditional = [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#EEEFF1',
            },
            {'if': {'column_id': 'id', },
             'display': 'None', }
        ]

style_data_conditional2 = [
            {
                "if": {
                    "state": "active"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            },
            {
                "if": {
                    "state": "selected"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            },
            {'if': {'column_id': 'id', },
             'display': 'None', }
        ]

# layout
layout = html.Div([
                    dash_table.DataTable(
                    id='table',
                    row_selectable='single',
                    page_size= 20,
                    style_cell=style_cell,
                    style_table=style_table,
                    cell_selectable=True,
                    style_header=style_header,
                    style_data=style_data,
                    style_data_conditional=style_data_conditional,
                    style_header_conditional=style_header_conditional,
                    virtualization=True
                             ),])

# connection à la base de donnée
try:
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

def parse_fichier(contents, filename):
        """
        fonction récupérant le contenu du fichier chargés
        :param contents: contenu du fichier chargé
        :param filename: nom du fichier chargé
        :return: un dictionaire du contenu charge si ce sont des données et rien du tout si c'est un modèle
        """
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # pour les fichiers de type csv
                log.info('le fichier à un format csv')
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # pour les fichiers de type xls
                log.info('le fichier à un format xls')
                df = pd.read_excel(io.BytesIO(decoded))
            elif 'xlsx' in filename:
                # pour les fichiers de type xlsx
                log.info('le fichier à un format xlsx')
                df = pd.read_excel(io.BytesIO(decoded))
            elif 'pkl' in filename:
                # pour les fichiers de type pkl
                log.info('le fichier à un format pickle')
                model = pd.read_pickle(io.BytesIO(decoded))
                return no_update
            candidates = ['Unnamed: 0']
            df = df.drop([x for x in candidates if x in df.columns], 1)
            df_table = df.copy()
            df_table['id'] = df_table.index
        except Exception as e:
            log.error(e)
        return df_table.to_dict('records'), df.columns, content_string

def update_metadata(filename,contenu,date,sql):
    """
    fonction mettant à jour la table précisé dans la base de donnée
    :param filename: nom du fichier de donnée chargé
    :param date: date d'aujourd'hui
    :param table: nom de la table
    :return: None
    """
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
    values = (date,filename,contenu)
    log.info('lancement du query')
    cursor.execute(sql,values)
    log.info('Arret du curseur de la base de donnée')
    cursor.close()
    log.info('query commité')
    conn.commit()
    log.info('ferméture de la connexion à la base de donnée')
    conn.close()


log.info('lancement du callback pour la gestion du data table')
@app.callback(

        Output('table', 'data'),
        Input('donnée', 'contents'),
        State('donnée', 'filename'),
    )
def update_app(contents_donnée, filename_donnée):
        """
        fonction mettant à jour une table de la base de donnée et lance le data table layout
        :param contents_donnée:
        :param filename_donnée:
        :return: récupère le contenu du fichier donné et lance le data table layout
        """
        log.info('lancement de la fonction après le callback')
        date = str(datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M"))  # bon format de date (année , mois, jours, heure, minute)
        if contents_donnée is not None:
            log.info('mise à jours de table donnée')
            table = 'metadata_donnée_v2'
            sql = f"INSERT INTO {table} (date,fichier,contenu) VALUES (%s,%s,%s);"
            log.info('chargement du contenu du fichier')
            dict_donnée, _, content_string = parse_fichier(contents_donnée,
                          filename_donnée)
            log.info('création du data table')
            update_metadata(filename_donnée,content_string, date, sql)  # mise à jour de la table metadata_donnée

            return dict_donnée# récuperation du contenu du fichier de donnée et création du data table




