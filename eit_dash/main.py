from dash import html, page_container
import dash_bootstrap_components as dbc
from app import app
import callbacks.load_callbacks # noqa


app.layout = html.Div([
    html.H1(children='EIT-ALIVE dashboard', style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col(dbc.NavLink('Load', href='/load')),
        dbc.Col(dbc.NavLink('Sync', href='/dummy')),
        dbc.Col(dbc.NavLink('Select', href='/dummy')),
        dbc.Col(dbc.NavLink('Filter', href='/dummy')),
        dbc.Col(dbc.NavLink('Analyze', href='/dummy')),
        dbc.Col(dbc.NavLink('Summarize', href='/dummy')),
    ],
        style={'textAlign':'center'}),
    page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)
