import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import MATCH, Input, Output, State, callback, ctx, dcc, html

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles

# ruff: noqa: D103  #TODO remove this line when finalizing this module


def get_loaded_data():
    return [
        {"Number": 1, "sampling_frequency": 100},
        {"Number": 2, "sampling_frequency": 50},
        {"Number": 3, "sampling_frequency": 250},
    ]


# this callback runs when the page is loaded (the title of the preprocessing is created)
# and loads the data in the resampling card and in the dataset selection menu
@callback(
    [Output(ids.RESAMPLING_CARD, "children"), Output(ids.DATASET_SELECTION_CHECKBOX, "options")],
    Input(ids.PREPROCESING_TITLE, "children"),
)
def load_datasets(title):
    dummy_data = get_loaded_data()

    row = [dbc.Row([dbc.Col([html.H6("Sequence")]), dbc.Col([html.H6("Sampling frequency")])]), html.P()]

    row += [
        dbc.Row([dbc.Col(f'Sequence {data["Number"]}'), dbc.Col(f'{data["sampling_frequency"]} Hz'), html.P()])
        for data in dummy_data
    ]

    options = [{"label": f'Sequence {data["Number"]}', "value": str(i)} for i, data in enumerate(dummy_data)]

    return row, options


# apply resampling
@callback(
    [
        Output(ids.OPEN_SYNCH_BUTTON, "disabled"),
        Output(ids.OPEN_SELECT_PERIODS_BUTTON, "disabled"),
        Output(ids.OPEN_FILTER_DATA_BUTTON, "disabled"),
        Output(ids.SUMMARY_COLUMN, "children"),
    ],
    Input(ids.CONFIRM_RESAMPLING_BUTTON, "n_clicks"),
    [State(ids.SUMMARY_COLUMN, "children"), State(ids.RESAMPLING_FREQUENCY_INPUT, "value")],
    prevent_initial_call=True,
)
def apply_resampling(apply_click, summary, frequency):
    summary = [dbc.Row([html.Div(f"Resampled dataset at {frequency}Hz", style=styles.SUMMARY_ELEMENT)])]
    return False, False, False, summary


# open/close modal dialog for data synchronization
@callback(
    Output(ids.SYNCHRONIZATION_POPUP, "is_open"),
    [Input(ids.OPEN_SYNCH_BUTTON, "n_clicks"), Input(ids.SYNCHRONIZATION_CONFIRM_BUTTON, "n_clicks")],
    prevent_initial_call=True,
)
def open_synch_modal(open_click, confirm_click) -> bool:
    trigger = ctx.triggered_id

    if trigger == ids.OPEN_SYNCH_BUTTON:
        return True

    return False


# open/close modal dialog for periods selection
@callback(
    Output(ids.PERIODS_SELECTION_POPUP, "is_open"),
    [Input(ids.OPEN_SELECT_PERIODS_BUTTON, "n_clicks"), Input(ids.PERIODS_CONFIRM_BUTTON, "n_clicks")],
    prevent_initial_call=True,
)
def open_periods_modal(open_click, confirm_click) -> bool:
    trigger = ctx.triggered_id

    if trigger == ids.OPEN_SELECT_PERIODS_BUTTON:
        return True

    return False


# Show dataset
@callback(
    Output(ids.SYNC_DATA_PREVIEW_CONTAINER, "children"),
    Input(ids.DATASET_SELECTION_CHECKBOX, "value"),
    State(ids.SYNC_DATA_PREVIEW_CONTAINER, "children"),
    prevent_initial_call=True,
)
def show_data(selected_dataset, current_content):
    x = np.linspace(-2 * np.pi, 2 * np.pi, 201)
    sample_data = np.sin(x)

    fig = go.Figure(data=[go.Scatter(y=sample_data)])

    return [
        dcc.Graph(figure=fig, id={"type": ids.SYNC_DATA_PREVIEW_GRAPH, "index": selected})
        for selected in selected_dataset
    ]


# mark clicked data points
@callback(
    Output({"type": ids.SYNC_DATA_PREVIEW_GRAPH, "index": MATCH}, "figure"),
    Input({"type": ids.SYNC_DATA_PREVIEW_GRAPH, "index": MATCH}, "clickData"),
    State({"type": ids.SYNC_DATA_PREVIEW_GRAPH, "index": MATCH}, "figure"),
    prevent_initial_call=True,
)
def mark_selected_point(selected_point, figure):
    fig = go.Figure(figure)

    x = selected_point["points"][0]["x"]

    fig.add_vline(x=x, line_width=3, line_dash="dash", line_color="green")
    return fig
