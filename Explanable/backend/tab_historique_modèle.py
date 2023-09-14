"""
fichier gérant l’historique des fichiers de chargé
"""
from dash import *
import psycopg2
import dask.dataframe as dd
import pandas as pd
import os
import sys
from pathlib import Path
from Explanable.backend.assets.style_app import texte_style
from Explanable.backend.assets.style_historique_modèle import *


current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)
from Explanable.log_app.log import log

# instance de log
file = "explain/Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

# connection à la base de donnée
try:
    log.info('connection avec le serveur postgres')
    conn = psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'), 
        host=os.getenv('POSTGRES_HOST'),
        port='5432'
    )
except Exception as e:
    log.error(e)
sql = "SELECT date,fichier, model, hyperparametre FROM metadata_modèle;"
log.info('recuperation des données de la base')
try:
    df = pd.read_sql(sql,conn)
except Exception as e:
    log.error(e)

try:
    if df.empty: # ce qui se passe si elle est vide
        layout = html.H4('Pas de donnée historique disponible !', style=texte_style)

    else: #  dans le cas ou la base de donnée n'est pas vide
        layout = html.Div([dash_table.DataTable(
            data=df.to_dict('records'),
            style_as_list_view=True,
            style_cell=style_cell,
            style_header=style_header2,
            style_data=style_data,
            style_data_conditional=style_data_conditional,
            style_cell_conditional=style_cell_conditional,
            page_size= 7,
            tooltip_duration=None
        ) ,])

except Exception as e:
    log.error(e)