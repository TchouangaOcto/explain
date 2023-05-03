""" fichier contenant l’interface du logicielle et différent fonctionnalité et connexion
au module backend pour le fonctionnement de l’interface.
(dépendence: load_donnée, load_modèle, tab_historique_data, tab_historique_modèle)
"""
from dash import *
import dash_bootstrap_components as dbc
from backend.app import app
from backend import load_donnée, load_modèle, tab_historique_donnée, tab_historique_modèle, plot_explain_dash
import os
import sys
import base64
from pathlib import Path
current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
print(current_dir)
from log_app.log import log
file = "Explanable/log_app/frontend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

# variable globale et intérageable avec d'autre module
outils_xai = ['shapash', 'dalex']
choix_xai = ['Explanabilité :', 'Interprétabilité :']

# css style de la page
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'textAlign': 'center',
    'font-size': '90%',
    'font-family': 'Overpass'
}

btn_style = {
    "height": "30px",
    "margin":"10px",
    'font-family': 'Overpass',
    'border-radius': '3px'

}

texte_style= {
    'textAlign': 'center',
    'font-family': 'Overpass',
    'font-weight':'normal',
    'font-size': '150%'}

radio_btn_style= {
    'font-family': 'Overpass',
    "margin":"20px",
    'font-family': 'Overpass',
    "display": "inline-block"}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#10b1ae',
    'color': 'white',
    'padding': '6px'
}

div_btn_style = {
    "display": "inline-flex",
    "verticalAlign": "middle",
    "font-family": "Overpass"
}

div_dropdown_style = {
    "width": "130px",
    "height": "40px",
    "margin-left": "30px",
    "verticalAlign": "middle",
    "font-family": "Overpass",
    "display": "inline-block",
    "float": "right"
}
div_dropdown_style2 = {
    "width": "220px",
    "height": "40px",
    "margin-top": "10px",
    "verticalAlign": "middle",
    "font-family": "Overpass",
    "display": "inline-block",
    'background-color': '#10b1ae'
}

div_xai = {
    "color":'#10b1ae'
}

img_style = {
 "display": "block",
 "margin-left":"auto",
 "margin-right":"auto"
}

page_style={
"flex-wrap": "wrap"
}


# obtention du contenu du logo
log.info('obtention du contenu du logo')
fichier_image = 'Explanable/logo.png'
repertiore_image = os.path.join(current_dir, fichier_image)
try:
    encoded_image = base64.b64encode(open(repertiore_image, 'rb').read()).decode('ascii')
except Exception as e:
    log.error(e)

# App Layout
log.info('chargement de la page acceuille web')
app.layout = html.Div([

    #html.H1(children='Make AI Explanable', style={'textAlign': 'center',"font-family": "Overpass"}), # header (title)

    # le logo de l'application
    html.Img(src='data:image/png;base64,{}'.format(encoded_image),height=300, style=img_style),
    html.Div([
        # button chargement de donnée
        html.Div(children=[
            dcc.Upload(id='donnée', children=html.Div(
                [dbc.Button('charger les données', style=btn_style,
                            size='lg', className="btn", id='donnée_button', n_clicks=0)])),], style=div_btn_style),
        # button chargement de modèle
        html.Div(children=[
            dcc.Upload(id='modèle', children=html.Div([dbc.Button('charger le modèle',
                                                                   style=btn_style,
                                                                   size='lg', className="btn",
                                                                   id='modèle_button', n_clicks=0)], ))], style=div_btn_style),

        # checkbox pour l'explanabilité
        dcc.Checklist([choix_xai[0]],style=radio_btn_style, inline=True,id='checklist_explain'),

        # dropdown pour l'explanabilté
        html.Div(children=[
                    dcc.Dropdown(outils_xai,multi=True,placeholder="outil", searchable=False, id='Explanabilité_methdode')
                ],style=div_dropdown_style2, className="custom-dropdown"),

        # checkbox pour l'interprétabilité
        dcc.Checklist([choix_xai[1]], style=radio_btn_style, inline=True, id='checklist_interprete'),

        # dropdown pour les méthodes d'interprétabilité
        html.Div(children=[
            dcc.Dropdown(outils_xai,multi=True,placeholder="outil", searchable=False, id='Interprétabilité_methdode',className="custom-dropdown")
        ], style=div_dropdown_style2),

        # dropdown pour le choix de la variable à prédire
        html.Div(children=['variable à expliqué:',
            dcc.Dropdown(placeholder="variable", id='variable_à_expliqué')
        ], style=div_dropdown_style),
        # dropdown pour le choix de la variable a expliqué
        html.Div(children=['variable explicatif:',
            dcc.Dropdown(placeholder="variable", maxHeight=50, id='variable_explicatif')
        ], style=div_dropdown_style)
    ], style={
        "margin-left": "100px",
        "flex-wrap": "wrap",
    }, className="custom-flex"),
    html.Br(),
    # les différents tab de la page
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


    # descriptive analysis content
    html.Div(id="analyse_descriptive"),

    html.Br(),
    # contenu XAI
    html.Div(id="xai",style=div_xai)



],style=page_style)


id_dropdown = 'variable_à_expliqué'
state = True
status_explicatif = True
log.info('activation de callback pour le management des tabs')
# callback pour le management des tabs
@app.callback(
                (
                  Output("tab_content", "children"), # sortie pour le contenu du tab
                  Output(id_dropdown, 'options'), # sortie pour le contenu du drop down pour la variable à expliqué
                  Output('variable_explicatif', 'options'), # sortie pour le contenu du drop down pour la variable explicatif
                  Output('variable_explicatif', 'value')
                ),
              [
                  Input('variable_à_expliqué', 'value'),
                  Input("tabs-styled-with-inline", "value"),
                  Input('donnée', 'contents'),
                  Input('modèle', 'contents'),
                  State('modèle', 'filename'),
                  State('donnée', 'filename')
              ]
              )

def render_content(contenu_dropdown_variable_explicatif,tab,contenu_donnée,contenu_modèle,filename_modèle,filename_donnée):
    '''
    Fonction gérant la mise à jour du contenu des tabs
    :param tab: le tab spécifique sur lequel l'utilisateur a cliqué
    :param contenu_donnée: le contenu des données chargé
    :param contenu_modèle: le contenu du modèle chargé
    :param filename_modèle: le nom du fichier du modèle chargé
    :return: un data table des données chargé, l'historique des données chargé, l'historique des modèles chargé.
    Par défaut du texte
    '''
    global state
    global status_explicatif
    try:
        log.info(f'valeur dropdown explicatif: {contenu_dropdown_variable_explicatif}')
        log.info(f'contenu modèle: {contenu_modèle}')
        if status_explicatif and contenu_dropdown_variable_explicatif is not None:
            log.info('tab pour variable explicatif')
            log.info('explicatif avec succes')
            colonnes_explicatif_to_list = list(load_donnée.parse_fichier(contenu_donnée, filename_donnée)[1])
            colonnes_explicatif_to_list.remove(contenu_dropdown_variable_explicatif)
            log.info(f'statue charge  variable avant : {status_explicatif}')
            status_explicatif = False
            log.info(f'statue charge  variable après : {status_explicatif}')
            return no_update, no_update, colonnes_explicatif_to_list, colonnes_explicatif_to_list[0]

        elif contenu_modèle is not None and state: # si le contenu du modèle existe
            load_modèle.update_app(contenu_modèle,filename_modèle) # chargé et mettre à jour les metadata modèle
            log.info(f'statue charge modèle avant : {state}')
            state = False
            log.info(f'state charge modèle après : {state}')
            return no_update, no_update, no_update, no_update # définir les mises à jour

        elif tab == "tab-1": # tab concernant la disposition du dataframe
            log.info('verification du premier tab')
            if contenu_donnée is not None:# si le contenu des données existe
                if contenu_dropdown_variable_explicatif is not None:
                    return load_donnée.layout, no_update, no_update, no_update
                else:
                    colonnes = load_donnée.parse_fichier(contenu_donnée, filename_donnée)[1]
                    state = True
                    status_explicatif = True
                    return load_donnée.layout, colonnes, no_update, no_update# crée le data table et retourner la liste des colonnes

            else:
                log.info('texte contenant le message de bienvenue')
                return html.Div([
                    html.H4('Bienvenue sur explainable AI octopeek, charge ton fichier de donnée et modèle',
                            style=texte_style)]), no_update, no_update, no_update # sinon renvoyer du texte

        elif tab == "tab-2": # si le tab 2 est cliqué
            log.info('verification du deuxième tab')#  mettre à jour l'historique des données chargé
            return tab_historique_donnée.layout,no_update, no_update, no_update
            #return html.Div([
             #   html.H4('Ceci sera visible quand vous allez chargé les données',
              #          style=texte_style)
            #])
        elif tab == "tab-3": # si le tab 3 est cliqué
            log.info('verification du troisième tab') # mettre à jour l'historique des modèles chargé
            return tab_historique_modèle.layout, no_update, no_update, no_update
            #return html.Div([
            #    html.H4('Ceci sera visible quand vous allez chargé les différents modèles',
            #           style=texte_style)
            #])


    except Exception as e:
        log.error(e)


@app.callback(


                  Output("xai", "children"),
                  #Output("confirm-danger","displayed")


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
#        elif isinstance(checklist_explain,str) or isinstance(Explanabilité_methdode,str):
#            return no_update, no_update
#        else:
 #           return no_update, True
 #   else:
 #       return no_update, no_update





log.info('lancement du serveur dash')
if __name__ == '__main__':
    try:
        app.run_server(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        log.error(e)