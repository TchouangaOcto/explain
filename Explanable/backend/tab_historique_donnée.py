"""
fichier gérant l’historique des fichiers de jeu de donnée chargé
"""
from dash import *
import psycopg2
import pandas as pd
import os
from pathlib import Path
import dash_html_components as html

current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print("chargement de l'histotique des données")


# instance de log
from Explanable.log_app.log import log
file = "explain/Explanable/log_app/backend.log"
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
        database=os.getenv('DB_DATABASE'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port='5432'
    )
except Exception as e:
    log.error(e)
sql = "SELECT date, fichier FROM metadata_donnée_v2;"
log.info('recuperation des données de la base')
try:
    df = pd.read_sql(sql,conn)
except Exception as e:
    log.error(e)

# layout
message = 'en cliquant dessus vous lancez le chargement du fichier'

layout = html.Div([dash_table.DataTable(
    data=df.to_dict('records'),
    tooltip_data=[
        {
            column: {'value': message, 'type': 'markdown'}
            for column, value in row.items() if column == 'fichier'
        } for row in df.to_dict('records')
    ],
    css=[{
        'selector': '.dash-table-tooltip',
        'rule': 'background-color: #EEEFF1; font-family: monospace; color: black'
    }],
    tooltip_delay=0,
    tooltip_duration=None,
    style_as_list_view=True,
    style_cell=style_cell,
    style_header=style_header,
    style_data=style_data,
    style_data_conditional=style_data_conditional,
    style_cell_conditional=style_cell_conditional,
    page_size= 10,
    virtualization=True
) ,])




