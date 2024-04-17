from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.definitions.option_lists import InputFiletypes

register_page(__name__, path="/analyze")

summary = dbc.Col(
    [
        html.H2("Summary", style=styles.COLUMN_TITLE),
        html.Div([], id=ids.SUMMARY_COLUMN_ANALYZE, style=styles.LOAD_RESULTS),
    ]
)

results = dbc.Col(
    [
        html.H2("Results", id=ids.ANALYZE_RESULTS_TITLE, style=styles.COLUMN_TITLE),
        html.Div(id=ids.DATASET_CONTAINER, style=styles.LOAD_RESULTS),
    ],
)

actions = dbc.Col(
    [
        html.H2("Data analysis", id=ids.ANALYZE_TITLE, style=styles.COLUMN_TITLE),
        html.P(),
        html.Div(
            dbc.Row(
                dbc.Button("Apply EELI", id=ids.EELI_APPLY, disabled=False),
            ),
            hidden=False,
        ),
        html.P(),
        html.Div(
            [
                dbc.Row(dbc.Select(id=ids.ANALYZE_SELECT_PERIOD_VIEW)),
                dbc.Row(
                    dcc.Graph(id=ids.EELI_RESULTS_GRAPH, style=styles.EMPTY_ELEMENT),
                ),
            ],
            id=ids.EELI_RESULTS_GRAPH_DIV,
            hidden=True,
        ),
        html.P(),
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
