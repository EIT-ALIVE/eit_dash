from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.definitions.option_lists import InputFiletypes

register_page(__name__, path="/analyze")

summary = dbc.Col([html.H2("Summary", style=styles.COLUMN_TITLE)])

results = dbc.Col(
    [
        html.H2("Results", id=ids.ANALYZE_RESULTS_TITLE, style=styles.COLUMN_TITLE),
        html.Div(id=ids.DATASET_CONTAINER, style=styles.LOAD_RESULTS),
    ],
)

actions = dbc.Col(
    [
        html.H2("Data analysis", style=styles.COLUMN_TITLE),
    ],
)

layout = dbc.Row(
    [
        html.H1("ANALYZE DATA", style=styles.COLUMN_TITLE),
        summary,
        actions,
        results,
    ],
)
