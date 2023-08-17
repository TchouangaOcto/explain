import dash
import flask
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True
