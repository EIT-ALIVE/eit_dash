import dash_bootstrap_components as dbc
from dash import html, page_container

import eit_dash.callbacks.load_callbacks  # noqa
from eit_dash.app import app

app.layout = html.Div([
    html.H1(id='test-id',children='EIT-ALIVE dashboard', style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col(dbc.NavLink('Load', href='/load')),
        dbc.Col(dbc.NavLink('Pre-processing', href='/preprocessing')),
        dbc.Col(dbc.NavLink('Analyze', href='/dummy')),
        dbc.Col(dbc.NavLink('Summarize', href='/dummy')),
    ],
        style={'textAlign':'center'}),
    page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)
