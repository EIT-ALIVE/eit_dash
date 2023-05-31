from dash import Dash, html, dcc, callback, Output, Input, page_container
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from app import app
import callbacks.load_callbacks

app.layout = html.Div([
    html.H1(children='EIT-ALIVE dashboard', style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col(dbc.NavLink('Left', href='/left')),
        dbc.Col(dbc.NavLink('Load', href='/load')),
        dbc.Col(dbc.NavLink('Right', href='/right')),
    ],
        style={'textAlign':'center'}),
    page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)
