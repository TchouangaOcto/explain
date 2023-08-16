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
current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)
from Explanable.log_app.log import log

# instance de log
file = "explain/Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)


# css style
style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    }

style_header2 = {
    'backgroundColor': '#96B9C4',
    'color': '#F3FBFB',
    'fontWeight': 'bold'
}
style_cell={
    'font-family': 'Overpass',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'maxWidth': 0,
}

style_cell2={
    'padding': '5px',
    'font-family': 'Overpass'
}

style_cell_conditional = [
    {
        'textAlign': 'center'
    }
]

style_data = {
    'color': 'black',
    'backgroundColor': 'white',
    'whiteSpace': 'normal',
    'height': 'auto',
    'lineHeight': '40px'
}

style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#EEEFF1',
    }
]

# connection à la base de donnée
try:
    log.info('connection avec le serveur postgres')
    conn = psycopg2.connect(
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        #host=os.getenv('DB_HOST'),
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

# layout
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