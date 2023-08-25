""" fichier contenant l’interface du logicielle et différent fonctionnalité et connexion
au module backend pour le fonctionnement de l’interface.
(dépendence: load_donnée, load_modèle, tab_historique_data, tab_historique_modèle)
"""
from dash import *
from Explanable.backend.server import app
from Explanable.backend.assets.style_app import *
from Explanable.backend import load_donnée, load_modèle, tab_historique_donnée, tab_historique_modèle, plot_explain_dash
import os
import sys
import base64
import psycopg2
import random
from pathlib import Path
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
sys.path.append(os.path.join(current_dir, 'log'))
from Explanable.log_app.log import log
file = "explain/Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

#setting environment variables
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = '0000'
os.environ['DB_DATABASE'] = 'postgres'
os.environ['DB_HOST'] = 'database'

# variable globale et intérageable avec d'autre module
outils_xai = ['shapash', 'dalex','shap']
choix_xai = ['Explanabilité :', 'Interprétabilité :']

# obtention du contenu du logo
log.info('obtention du contenu du logo')
fichier_image = 'explain/Explanable/logo.png'
repertiore_image = os.path.join(current_dir, fichier_image)
encoded_image = base64.b64encode(open(repertiore_image, 'rb').read()).decode('ascii')

# App Layout
log.info('chargement de la page acceuille web')
app.layout = html.Div([

    #html.H1(children='Make AI Explanable', style={'textAlign': 'center',"font-family": "Overpass"}), # header (title)

    # le logo de l'application
    html.Img(src='data:image/png;base64,{}'.format(encoded_image),height=300, style=img_style),
    html.Div([
        html.Div([
        # button chargement de donnée
        html.Div(children=[
            dcc.Upload(id='donnée', children=html.Div(
                [dbc.Button('charger les données', style=btn_style,
                            size='lg', className="btn", id='donnée_button', n_clicks=0),])),], style=div_btn_style),

        # icon info pour le chargement des fichier données
        html.Div(children=[html.I(className="bi bi-info-circle-fill me-2", id="info_donnée"),
                               dbc.Tooltip('charge les fichiers csv seulement', style=tooltip_style,
                                           target='info_donnée', placement='top')]),

        # button chargement de modèle
        html.Div(
            dcc.Loading(
            type="circle",
            children=[
            dcc.Upload(id='modèle', children=html.Div([dbc.Button('charger le modèle',
                                                                   style=btn_style,
                                                                   size='lg', className="btn",
                                                                   id='modèle_button', n_clicks=0),], ))]), \
                                                                    style=div_btn_style),

        # icon info pour le chargement des fichiers modèle
        html.Div(children=[html.I(className="bi bi-info-circle-fill me-2", id="info_modèle"),
                               dbc.Tooltip('charge les fichiers pkl seulement', style=tooltip_style,
                                           target='info_modèle', placement='top')]),

        # checkbox pour l'explanabilité
        dcc.Checklist([choix_xai[0]],style=radio_btn_style, inline=True,id='checklist_explain'),

        # dropdown pour l'explanabilté
        html.Div(children=[
                    dcc.Dropdown(outils_xai,multi=True,placeholder="outil", searchable=False, \
                                 id='Explanabilité_methdode')
                ],style=div_dropdown_style2, className="custom-dropdown"),

        # checkbox pour l'interprétabilité
        dcc.Checklist([choix_xai[1]], style=radio_btn_style, inline=True, id='checklist_interprete'),

        # dropdown pour les méthodes d'interprétabilité
        html.Div(children=[
            dcc.Dropdown(outils_xai,multi=True,placeholder="outil", searchable=False, id='Interprétabilité_methdode',\
                         className="custom-dropdown")
        ], style=div_dropdown_style2),

        # dropdown pour le choix de la variable à prédire
        html.Div(children=['variable à expliqué:',
            dcc.Dropdown(placeholder="variable", id='variable_à_expliqué')
        ], style=div_dropdown_style),
        # dropdown pour le choix de la variable a expliqué
        html.Div(children=['variable explicatif:',
            dcc.Dropdown(multi=True, placeholder="variable", maxHeight=50, id='variable_explicatif')
        ], style=div_dropdown_style)
    ], style={
        "margin-left": "100px",
        "flex-wrap": "wrap",
    }, className="custom-flex"),],className="btn_drop"),
    html.Br(),

    # les différents tab de la page pour les données
    html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='jeu de donnée', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='historique des données chargé', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='historique de modèle chargé', value='tab-3', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles)

    ],

        className="row tabs_div"
    ),



    dcc.ConfirmDialog(
        id='confirm-danger',
        message="n'oublie pas de choisir la  méthode voulu",
    ),

    # Tab content
    html.Div(id="tab_content"),

    # button chargent les données historiques
    html.Div(children=[
            dbc.Button('utilisation des données historique', style=btn_style,
                        size='lg', className="btn", id='btn_donnée_historique', n_clicks=0), ], \
                            style=div_btn_historique_style),

    # icon info pour le chargement des fichiers de données historiques
    html.Div(children=[html.I(className="bi bi-info-circle-fill me-2", id="info_historique", style={'float':'right'}),
                       dbc.Tooltip("charge les dernier fichier dans l'historique des données", style=tooltip_style,
                                   target='info_historique', placement='left')]),

    # les différents tab de la page pour les tableaux de bord
    # html.Div([
    #     dcc.Tabs(id="tabs-styled-with-inline_", value='tabexplain-1', children=[
    #         dcc.Tab(label='Dalex', value='tabexplain-1', style=tab_style, selected_style=tab_selected_style),
    #         dcc.Tab(label='Shapash', value='tabexplain-2', style=tab_style,
    #                 selected_style=tab_selected_style),
    #         dcc.Tab(label='other', value='tabexplain-3', style=tab_style,
    #                 selected_style=tab_selected_style),
    #     ], style=tabs_styles)
    #
    # ],
    #
    #     className="row tabs_div_"
    # ),
    # descriptive analysis content
    html.Div(id="analyse_descriptive"),

    html.Br(),
    # contenu XAI
    html.Div(id="xai",style=div_xai)



],style=page_style)


id_dropdown = 'variable_à_expliqué' #id du design du drop down pour le choix de la variable a expliqué
state = True
status_explicatif =  True # vérifie si les colonnes du jeu de donnée ont été correctement chargé
log.info('activation de callback pour le management des tabs')
# callback pour le management des tabs
@app.callback(
                (
                  Output("tab_content", "children"), # sortie pour le contenu du tab
                  Output(id_dropdown, 'options'), # sortie pour le contenu du drop down pour la variable à expliqué
                  Output('variable_explicatif', 'options'), # sortie pour le contenu du drop down pour la variable explicatif
                  Output('variable_explicatif', 'value') # variable explicatives du modèle
                ),
              [
                  Input('variable_à_expliqué', 'value'), # valuer de la variable à expliqué
                  Input("tabs-styled-with-inline", "value"), # information sur lequel l'utilisateur se trouve
                  Input('donnée', 'contents'), # information concernant le nom du fichier du modèle chargé
                  Input('modèle', 'contents'), # information concernant le contenu du fichier de modèle chargé
                  Input('btn_donnée_historique', 'n_clicks'),
                  State('modèle', 'filename'), # information concernant le nom du fichier du modèle chargé
                  State('donnée', 'filename') # information concernant le nom du fichier de donnée chargé
              ]
              )

def render_content(contenu_dropdown_variable_explicatif,tab,contenu_donnée,contenu_modèle,btn,filename_modèle,filename_donnée):
    '''
    Fonction gérant la mise à jour du contenu des tabs
    :param tab: le tab spécifique sur lequel l'utilisateur a cliqué
    :param contenu_donnée: le contenu des données chargé
    :param contenu_modèle: le contenu du modèle chargé
    :param filename_modèle: le nom du fichier du modèle chargé
    :return: un data table des données chargé, l'historique des données chargé, l'historique des modèles chargé.
    Par défaut du texte
    '''
    # battery of test here
    global state #
    global status_explicatif # vérifie si les colonnes du jeu de donnée ont été correctement chargé
    try: 
        log.info(f'valeur dropdown explicatif: {contenu_dropdown_variable_explicatif}')
        if status_explicatif and contenu_dropdown_variable_explicatif is not None: # # vérifie si les colonnes du jeu de donnée ont été correctement chargé
            log.info('variable explicatives chargé avec success')
            try:
                log.info('collecte des variables explicatives')
                colonnes_explicatif_to_list = list(load_donnée.parse_fichier(contenu_donnée, filename_donnée)[1])
            except Exception as e:
                log.error(e)
            try:
                log.info('suppression de la variable à prédire de la liste des variables explicatives')
                colonnes_explicatif_to_list.remove(contenu_dropdown_variable_explicatif)
            except Exception as e:
                log.error(e)
            log.info(f'statue charge  variable avant : {status_explicatif}')
            status_explicatif = False
            log.info(f'statue charge  variable après : {status_explicatif}')
            return no_update, no_update, colonnes_explicatif_to_list, colonnes_explicatif_to_list[0]

        # cas d'usage  mise à jour automatique des metadonnée du modèle chargé
        elif contenu_modèle is not None and state: # si le contenu du modèle existe
            log.info('contenu du modèle bien chargé')
            try:
                load_modèle.update_app(contenu_modèle,filename_modèle) # chargé et mettre à jour les metadata modèle
            except Exception as e:
                log.error(e)
            log.info(f'statue charge modèle avant : {state}')
            state = False
            log.info(f'state charge modèle après : {state}')

            # cas d'usage ou le fichier csv n'est pas un fichier de donnée
            if contenu_donnée is not None:
                variables = load_modèle.parse_fichier(contenu_modèle, filename_modèle)[-1]
                colonnesFichierDonnée = load_donnée.parse_fichier(contenu_donnée, filename_donnée)[1]
                variablesNombre = len(variables)
                colonnesFichierDonnéeNombre = len(colonnesFichierDonnée)
                colonnesFichierDonnéeAjusté = []
                for variable in  colonnesFichierDonnée:
                    colonnesFichierDonnéeAjusté.append(variable.split(":")[0])
                # nombre de variables utilisé dans le modèle est equivalent à celui de du fichier chargé
                if variablesNombre != colonnesFichierDonnéeNombre and (set(variables) & set(colonnesFichierDonnéeAjusté)) is  None:
                    return html.Div([
                        html.H4("oops le modèle chargé n'est pas cohérant avec le fichier de donnée chargé",
                                style=texte_style)]), no_update, no_update, no_update  # renvoyer le message d'erreur (scénario de test pour pdf,...)

            return no_update, no_update, no_update, no_update # définir les mises à jour

        # cas d'usage faire apparaitre une table par hasard du button historique de donnée
        elif 'btn_donnée_historique' == ctx.triggered_id:
            log.info("cas d'usage faire apparaitre une table par hasard du button historique de donnée")
            query = 'select fichier, contenu from metadata_donnée_v2 order by date desc limit 1;'
            try:
                # connection à la base de donnée
                log.info('connection avec le serveur postgres')
                conn = psycopg2.connect(
                    database=os.getenv('DB_DATABASE'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    host=os.getenv('DB_HOST'),
                    port='5432'
                )
                cursor = conn.cursor()
            except Exception as e:
                log.error(e)
            log.info('lancement du query')
            cursor.execute(query)

            log.info('Arret du curseur de la base de donnée')
            rows = cursor.fetchall()
            row = random.choice(rows)
            filename_donnée = row[0]
            contenu_donnée = row[1]
            cursor.close()

            log.info('query commité')
            log.info('ferméture de la connexion à la base de donnée')
            conn.close()
            return load_donnée.layout, no_update, no_update, no_update

        # cas d'usage le tab 1 est cliqué
        elif tab == "tab-1":
            log.info('CLIQUE sur tab1')

            # case d'usage quand le fichier de donnée est chargé
            if contenu_donnée is not None:
                log.info('il ya du contenu donnée chargé')

                # cas d'usage dans le chargement des variables explicatives dans le drop down
                if contenu_dropdown_variable_explicatif is not None: # verifier si les variables du fichier de donnée ont été correctement chargé
                    log.info('le contenu est chargé malgré le fait que existe des variables explicatives dans le drop down ')
                    return load_donnée.layout, no_update, no_update, no_update #si les colonnes n'ont pas été chargé lancé le chargement du data table du fichier de donnée chargé

                # gestion du cas du usage ou le fichier chargé est de mauvaise qualité
                elif load_donnée.parse_fichier(contenu_donnée, filename_donnée) is None: # si l'extension du fichier chargé n'est pas conforme
                    log.info('le fichier de donnée ne respecte pas les norme de type de ficher accepté')
                    return  html.Div([
                         html.H4('oops charge un fichier xls, csv, xlsx',
                                style=texte_style)]), no_update, no_update, no_update # renvoyer le message d'erreur (scénario de test pour pdf,...)

                else:
                    try:
                        log.info('récupération des colonnes du fichier chargé')
                        colonnes = load_donnée.parse_fichier(contenu_donnée, filename_donnée)[1] # recuperation des colonnes du jeu de donnée
                    except Exception as e:
                        log.error(e)
                    state = True
                    status_explicatif = True # status de chargement des colonnes explicatif deviennent True
                    log.info("renvoie du data table sur l'interface")
                    return load_donnée.layout, colonnes, no_update, no_update# crée le data table et retourner la liste des colonnes

            else:
                log.info('texte contenant le message de bienvenue')
                return html.Div([
                    html.H4('Bienvenue sur explainable AI octopeek, charge ton fichier de donnée et modèle',
                            style=texte_style)]), no_update, no_update, no_update # texte de bienvenue à l'accueille de la platforme

        elif tab == "tab-2": # si le tab 2 est cliqué
            log.info('CLIQUE sur tab2')#  mettre à jour l'historique des données chargé
            return tab_historique_donnée.layout,no_update, no_update, no_update

        elif tab == "tab-3": # si le tab 3 est cliqué
            log.info('CLIQUE sur tab3') # mettre à jour l'historique des modèles chargé
            return tab_historique_modèle.layout, no_update, no_update, no_update
    except Exception as e:
        log.error(e)

@app.callback(

                  Output("xai", "children"),

              [
                  Input("variable_à_expliqué", "value"),
                  Input('checklist_explain', 'value'),
                  Input('Explanabilité_methdode', 'value')
              ]
              )

def render_card(variable_à_prédire,checklist_explain, Explanabilité_methdode):
    log.info("lancement du callabck pour obtenir les graphiques l'explicabilité")
    log.info(f'valeur de méthode {Explanabilité_methdode}')
    log.info(f'valeur de checklist {checklist_explain}')
    log.info(f'valeur à prédire {variable_à_prédire}')
    if isinstance(variable_à_prédire,str):
        if len(checklist_explain)!= 0 and len(Explanabilité_methdode)!= 0:
            log.info("graphique c'est bon")
            return plot_explain_dash.cards


log.info('lancement du serveur dash')
if __name__ == '__main__':
    try:
        app.run_server(host='0.0.0.0', port=80, debug=False)
    except Exception as e:
        log.error(e)