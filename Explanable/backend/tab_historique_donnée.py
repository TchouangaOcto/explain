"""
fichier gérant l’historique des fichiers de jeu de donnée chargé
"""
from dash import *
import psycopg2
import dask.dataframe as dd
import pandas as pd
import os
import sys
from pathlib import Path
from Explanable.backend.assets.style_app import texte_style
from Explanable.backend.assets.style_historique_donnée import * 

current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)
from Explanable.log_app.log import log

# instance de log
file = "explain/Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)


log.info('connection avec le serveur postgres')
print("info : connection avec le serveur postgres")
conn = psycopg2.connect(
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port='5432'
)


sql = "SELECT date, fichier FROM metadata_donnée_v2;"

log.info('recuperation des données de la base')
try:
    df = pd.read_sql(sql,conn)

except Exception as e:
    log.error(e)


if df.empty: # ce qui se passe si elle est vide
    layout = html.H4('Pas de donnée historique disponible !', style=texte_style)

else: #  dans le cas ou la base de donnée n'est pas vide
    layout = html.Div([dash_table.DataTable(
        data=df.to_dict('records'),
        style_as_list_view=True,
        style_cell=style_cell,
        style_header=style_header,
        style_data=style_data,
        style_data_conditional=style_data_conditional,
        style_cell_conditional=style_cell_conditional,
        page_size= 7,
        virtualization=True
    ) ,])






