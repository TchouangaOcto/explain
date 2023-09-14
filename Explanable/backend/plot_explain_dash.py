from dash import *
import os
import sys
from pathlib import Path
import dash_bootstrap_components as dbc
from Explanable.backend.server import app
from Explanable.backend.explain import *
import psycopg2
import pandas as pd
import io
import base64
from Explanable.backend.assets.style_plot_explain import *
from Explanable.backend.assets.style_app import texte_style

current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)

from Explanable.log_app.log import log
file = "explain/Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)


card_content = [
    dbc.CardBody(
        [
            html.Div(id='graph_globale1'),
        ]
    ),
]

card_content2 = [
    dbc.CardBody(
        [
            html.Div(id='graph_globale2'),
        ]
    ),
]

row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content, color="primary", outline=True,style=card_unique_style),width=10),
        dbc.Col(dbc.Card(card_content2, color="secondary", outline=True,style=card_unique_style),width=10),
    ],style=card_style,
    className="mb-4",
)

cards = html.Div([row_1])

def lancé_le_module_dalex(modèle, dataset, variable_à_predire):
    """
    fonction permetant de lancé le module dalex

    :param modèle: objet de connection à la base de donnée [objet]
    :param dataset: le jeu de donnée [objet]
    :param variable_à_predire: variable à expliqué du jeu de donnée [string]

    :return: dalex [objet] (objet du module dalex)
    """
    module = dalex(modèle, dataset, variable_à_predire)
    return module


def connection_à_la_base_de_donnée():
    """
    fonction permetant la connexion à la base de donnée

    :return: connection [objet] (objet de connection à la base de donnée)
    """
    try:
        # connection à la base de donnée
        log.info('connection avec le serveur postgres')
        connection= psycopg2.connect(
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'), 
            host=os.getenv('POSTGRES_HOST'),
            port='5432'
        )
    except Exception as e:
        log.error(e)

    return connection


def recupéré_les_donnée(connection, requete_sql):
    """
    fonction mettant à jour la table précisé dans la base de donnée

    :param connection: objet de connection à la base de donnée [objet]
    :param requete_sql: commande sql [string]

    :return: resultat_attendu [list] liste de valeur retourner
    """
    curseur = connection.cursor()
    curseur.execute(requete_sql)
    valeurs = curseur.fetchall()
    curseur.close()
    log.info('ferméture de la connexion à la base de donnée')
    connection.close()

    return valeurs # change this to a correct name


def chargement_du_modèle_et_du_jeu_donnée(contenu_crypté_de_modèle, contenu_crypté_du_dataset):
    """
    fonction chargent les contenu du jeu de donnée chargé sur la platforme 
    et le modèle aussi

    :param contenu_crypté_de_modèle: contenu cryté du jeu de modèle [string]
    :param contenu_crypté_du_dataset: contenu cryté du jeu de donnée [string]

    :return: 
        - modèle: contenu chargé du modèlé à partir de la base de donnée [objet]
        - dataset: jeu de donnée chargé à partir de la base de donnée [objet]
    """
    contenu_décrypté_de_modèle = base64.b64decode(contenu_crypté_de_modèle)
    contenu_décrypté_du_dataset = base64.b64decode(contenu_crypté_du_dataset)
    modèle = pd.read_pickle(io.BytesIO(contenu_décrypté_de_modèle))
    dataset = pd.read_csv(io.StringIO(contenu_décrypté_du_dataset.decode('utf-8')))

    return modèle, dataset

def information_sur_explicabilité_chargé(module):
    """
    fonction montrant l'information sur les module chargé 

    :param module: information sur le module chargé [objet]
    """
    log.info(f'le module est: {module}')


def information_sur_les_variables_explicatifs(variable_explicatif):
    """
    fonction montrant l'information sur les explicatifs choisi

    :param module: information sur le module chargé [objet]
    """

    log.info(f'le(s) variables explicatifs sont/est {variable_explicatif}')


def requete_pour_obtenir_les_donnée_et_le_modèle_chargé_le_plus_récent():
    """
    fonction permettant d'avoir l'information ma plus récente sur la table 
    contenant les jeu de données chargé et aussi les modèles

    :return: resultat (une requete sql) [string]
    """
    
    table_information_sur_les_donnée_chargé ='metadata_donnée_v2'
    table_information_sur_les_modèle_chargé ='metadata_modèle'

    resultat =  f"select {table_information_sur_les_donnée_chargé}.contenu as data, \
                        {table_information_sur_les_modèle_chargé}.fichier as model, \
                        {table_information_sur_les_modèle_chargé}.contenu as contenu, \
                 max({table_information_sur_les_donnée_chargé}.date) as date \
                 from {table_information_sur_les_donnée_chargé} \
                 left join {table_information_sur_les_modèle_chargé} \
                 on {table_information_sur_les_donnée_chargé}.date = {table_information_sur_les_modèle_chargé}.date \
                 where {table_information_sur_les_modèle_chargé}.fichier is not null group by data,\
                 {table_information_sur_les_modèle_chargé}.fichier, {table_information_sur_les_modèle_chargé}.contenu \
                order by date desc limit 1;"
    
    return resultat 

def figure_explicatif_du_module_chargé(module, variable_explicatif_du_jeu_de_donnée):
    """
    fonction affichant les différent graphique dépendant du module choisi

    :param module: module précis d'explicabilité choisi [objet]
    :param variable_explicatif_du_jeu_de_donnée:list de variables 
    explicatif [list]

    :return: resultat [string] (une requete sql)
    """
    # predict_profile = module.predict_profile(variable_explicatif_du_jeu_de_donnée).\
    #    update_traces(marker=dict(color="#89D9D7"), hoverlabel=dict(bgcolor="#F79034"),selector=dict(type="line"))
    # predict_profile = predict_profile.update_layout(font=dict(color='#013E50'))
    
    #log.info('construction du graphique predict profile')

    variable_importance = module.feature_importance().update_traces(marker=dict(color="#89D9D7"),\
                                                                    hoverlabel=dict(bgcolor= "#F79034"),\
                                                                    selector=dict(type="bar"))
    variable_importance = variable_importance.update_layout(font=dict(color='#013E50'),annotations=dict(dict(text='')))

    log.info('construction du graphique variable importance')

    return None, variable_importance

@app.callback(
    Output('graph_globale1', 'children'),
    Output('graph_globale2', 'children'),
    Input('checklist_explain', 'value'),
    Input('Explanabilité_methdode', 'value'),
    Input('variable_à_expliqué', 'value'),
    Input('variable_explicatif', 'value')
)

def update_card(checkbox_valeur,dropdown_valeur,variable_predire, variable_explicatif):
    
    if  'dalex' in dropdown_valeur  and 'Explanabilité :' in checkbox_valeur:

        requete = requete_pour_obtenir_les_donnée_et_le_modèle_chargé_le_plus_récent()

        #contenu_crypté_du_dataset, modèle, contenu_crypté_de_modèle, _ = mettre_à_jour_les_tables(requete)

        resultat = connection_à_la_base_de_donnée()

        resultat_requete = recupéré_les_donnée(resultat, requete)
        
        if len(resultat_requete) == 0:
            log.info('pas de modèle chargé')

            return dbc.Alert("Aucun modèle à été chargé", style=texte_style), no_update
        
        else:
            
            contenu_crypté_du_dataset, modèle, contenu_crypté_de_modèle, _ = resultat_requete[0]

            modèle, dataset = chargement_du_modèle_et_du_jeu_donnée(contenu_crypté_de_modèle, \
                                                                    contenu_crypté_du_dataset)

            resultat = lancé_le_module_dalex(modèle,dataset, variable_predire)

            information_sur_explicabilité_chargé(resultat)

            information_sur_les_variables_explicatifs(variable_explicatif)
            #dalex_explain.feature_importance().update_traces(marker=dict(color="# 89D9D7")
            # ,hoverlabel=dict(bgcolor= "#F79034"),selector=dict(type="bar"))
            #dalex_explain.feature_importance().data[0].hoverlabel.bgcolor =
            #log.info(f'graph info: {resultat.predict_profile(variable_explicatif)}')
            
            resultat1, resultat2 = figure_explicatif_du_module_chargé(resultat, variable_explicatif)

            return dcc.Graph(figure=resultat2), no_update