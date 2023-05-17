import dash
import flask
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True
