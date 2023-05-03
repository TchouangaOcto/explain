from dash import *
import dash_bootstrap_components as dbc
from Explanable.backend.app import app
from Explanable.backend.explain import *
import psycopg2
import pandas as pd
import io
import base64
import configparser
import shap

config = configparser.ConfigParser()
current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())
sys.path.append(os.path.join(current_dir, 'log'))
from log import log
file = "Explanable/log_app/backend.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

# variable clé pour lancer le modèle explicable de dalex

card_style = {
    "display": "inline-flex",
    "padding": "2px 16px",
    "position": "center",
    "verticalAlign": "middle",
    "flex-wrap": "wrap"
}

card_unique_style = {
    "box-shadow": "2px 4px 8px 3px rgba(0,0,0,0.2)",
    "margin":"10px",
    "width":"950px",
    "verticalAlign": "middle"
}

card_content = [
    dbc.CardBody(
        [
            html.H2(f"Explicabilité dalex", className="card-title"),
            html.Div(id='graph_globale1'),
        ]
    ),
]

card_content2 = [
    dbc.CardBody(
        [
            html.H2(f"Explicabilité dalex", className="card-title"),
            html.Div(id='graph_globale2'),
        ]
    ),
]

card_content3 = [
    dbc.CardBody(
        [
            html.H2(f"Explicabilité shap", className="card-title"),
            html.Div(id='graph_globale3'),
        ]
    ),
]

row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content, color="primary", outline=True,style=card_unique_style),width=10),
        dbc.Col(dbc.Card(card_content2, color="secondary", outline=True,style=card_unique_style),width=10),
        dbc.Col(dbc.Card(card_content3, color="secondary", outline=True,style=card_unique_style),width=10),

    ],style=card_style,
    className="cards",
)

cards = html.Div([row_1])

def load_explain(modèle,dataset, variable_predire,outil,type='Tree'):
    if outil=='dalex':
        dalex_explain = dalex(modèle, dataset, variable_predire)
        return  dalex_explain
    if outil=='shap':
        shp_explain = SHAP(modèle, dataset, variable_predire,)

    return dalex_explain # retourne objet dalex

def request(sql):
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
    cursor.execute(sql)
    valeurs = cursor.fetchall()
    cursor.close()
    log.info('ferméture de la connexion à la base de donnée')
    conn.close()

    return valeurs[0]
@app.callback(

    Output('graph_globale1', 'children'),
    Output('graph_globale2', 'children'),
    Output('graph_globale3', 'children'),
    Input('checklist_explain', 'value'),
    Input('Explanabilité_methdode', 'value'),
    Input('variable_à_expliqué', 'value'),
    Input('variable_explicatif', 'value')
)

def update_card(checkbox_valeur,dropdown_valeur,variable_predire, variable_explicatif):

    table1 = 'metadata_donnée_v2'
    table2 = 'metadata_modèle'
    sql = f"select {table1}.contenu as data, {table2}.fichier as model, {table2}.contenu as contenu , max({table1}.date) as date from {table1}" \
          f" left join {table2} on {table1}.date = {table2}.date where {table2}.fichier is not null group by data, " \
          f"{table2}.fichier, {table2}.contenu order by date desc limit 1;"

    # obtention du contenu du modèle et des données
    log.info("obtention du contenu du modèle et les données")
    dataset_contenu, modèle, modèle_contenu, _ = request(sql)
    modèle_decoded = base64.b64decode(modèle_contenu)
    dataset_decoded = base64.b64decode(dataset_contenu)
    modèle = pd.read_pickle(io.BytesIO(modèle_decoded))
    dataset = pd.read_csv(io.StringIO(dataset_decoded.decode('utf-8')))

    log.info(f"chargement de l'outil dalex")
    dalex_explain = load_explain(modèle, dataset, variable_predire,)

    log.info("chargement de l'outil shap")
    explainer = shap.TreeExplainer(modèle)
    shap_values = explainer(dataset)

    log.info(f'graph info: {dalex_explain.predict_profile(variable_explicatif)}')
    fig1 = dalex_explain.predict_profile(variable_explicatif).update_traces(marker=dict(color="#89D9D7"),
                                                              hoverlabel=dict(bgcolor="#F79034"),
                                                                            selector=dict(type="line"))
    fig1 = fig1.update_layout(font=dict(color='#013E50'))
    fig2 = dalex_explain.feature_importance().update_traces(marker=dict(color="#89D9D7"),
                                                            hoverlabel=dict(bgcolor="#F79034"),
                                                            selector=dict(type="bar"))
    fig2 = fig2.update_layout(font=dict(color='#013E50'), annotations=dict(dict(text='')))
    #shap.initjs()

    #fig3 = dalex_explain.feature_importance_positif_negatif(dataset)
    #fig3 = shap.summary_plot(shap_values, dataset, show=False)
    #fig3 = shap.plots.waterfall(explainer.base_values[0], shap_values[0][0], dataset[0])
    #fig3 = shap.force_plot(explainer.expected_value, shap_values, dataset, matplotlib=False)

    if 'shap' and 'dalex' in dropdown_valeur  and 'Explanabilité :' in checkbox_valeur:

        #log.info(f'shapely graph {dalex_explain.feature_importance_positif_negatif(dataset)}')
        #log.info(f'info of shap graph {fig3}')
        return dcc.Graph(figure=fig2), \
            dcc.Graph(figure=fig1), dalex_explain.feature_importance_shap(dataset)


    if 'dalex' in dropdown_valeur  and 'Explanabilité :' in checkbox_valeur:
        #dalex_explain.feature_importance().update_traces(marker=dict(color="# 89D9D7"),hoverlabel=dict(bgcolor= "#F79034"),selector=dict(type="bar"))
        #dalex_explain.feature_importance().data[0].hoverlabel.bgcolor =
        return dcc.Graph(figure=fig2), \
            dcc.Graph(figure=fig1), no_update




