from dash import register_page, html
import dash_bootstrap_components as dbc
# from app import app

register_page(__name__, path='/load')

summary = dbc.Col('summary')


actions = dbc.Col([
    dbc.Row(dbc.Button('Add dataset', id='add-data-button')),
    dbc.Row(dbc.Label('label', id='test-label'))
])


results = dbc.Col('results')


layout = dbc.Row([
    html.H1('this is the loading page'),
    summary,
    actions,
    results,
])

