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


# css style
style_header = {
    'backgroundColor': '#96B9C4',
    'color': '#F3FBFB',
    'fontWeight': 'bold'
}

style_data = {
    'color': 'black',
    'backgroundColor': 'white',
    'whiteSpace': 'normal',
    'height': 'auto',
    'lineHeight': '40px'
}

style_cell={
    'font-family': 'Overpass'
}

style_cell_conditional = [
    {
    'if': {'column_id': 'fichier'},
        'textAlign': 'center'
    },
    {
        'if': {'column_id': 'date'},
        'textAlign': 'center'
    }
]

style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#EEEFF1',
    }
]

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
sql = "SELECT date, fichier FROM metadata_donnée_v2;"
log.info('recuperation des données de la base')
df = pd.read_sql(sql,conn)
print(df)

# layout
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




