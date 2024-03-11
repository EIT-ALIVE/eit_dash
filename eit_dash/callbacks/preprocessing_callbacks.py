import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import MATCH, Input, Output, State, callback, ctx, dcc, html

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.app import data_object

# ruff: noqa: D103  #TODO remove this line when finalizing this module


def check_continuous_data_loaded() -> bool:
    """
    Checks if continuous data have been loaded.

    Return: True if continuous data are present, False otherwise
    """
    loaded_data = data_object.get_all_sequences()

    return any(dataset.continuous_data for dataset in loaded_data)


def create_resampling_card(loaded_data):
    row = [
        dbc.Row(
            [dbc.Col([html.H6("Dataset")]), dbc.Col([html.H6("Sampling frequency")])],
        ),
        html.P(),
    ]

    row += [
        dbc.Row(
            [
                dbc.Col(f'{data["Name"]}'),
                dbc.Col(f'{data["Sampling frequency"]} Hz'),
                html.P(),
            ],
        )
        for data in loaded_data
    ]

    options = [
        {"label": f'{data["Name"]}', "value": str(i)}
        for i, data in enumerate(loaded_data)
    ]

    return row, options


def get_loaded_data():
    loaded_data = data_object.get_all_sequences()
    data = []
    for dataset in loaded_data:
        name = dataset.label
        if dataset.continuous_data:
            for channel in dataset.continuous_data:
                data.append({"Name": name, "Data type": channel})
        if dataset.eit_data:
            data.append(
                {
                    "Name": name,
                    "Data type": "EIT",
                    "Sampling frequency": dataset.eit_data.framerate,
                },
            )

    return data


def get_suggested_resampling(loaded_data):
    resampling_freq = 0
    for data in loaded_data:
        if data["Sampling frequency"] != "EIT":
            resampling_freq = min(resampling_freq, data["Sampling frequency"])

    return resampling_freq


# this callback runs when the page is loaded (the title of the preprocessing is created)
# and loads the data in the resampling card and in the dataset selection menu
@callback(
    [
        Output(ids.RESAMPLING_CARD, "children"),
        Output(ids.RESAMPLING_CARD_BODY, "children"),
        Output(ids.DATASET_SELECTION_CHECKBOX, "options"),
        Output(ids.RESAMPLING_FREQUENCY_INPUT, "value"),
    ],
    Input(ids.PREPROCESING_TITLE, "children"),
)
def load_datasets(title):  # pylint: disable=unused-argument
    loaded_data = get_loaded_data()
    continuous_data_loaded = check_continuous_data_loaded()

    if not continuous_data_loaded:
        return [], [], [], None

    suggested_resampling = get_suggested_resampling(loaded_data)

    row, options = create_resampling_card(loaded_data)

    return row, options, suggested_resampling



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

    content = [
        dcc.Graph(
            figure=fig, id={"type": ids.SYNC_DATA_PREVIEW_GRAPH, "index": selected},
        )
        for selected in selected_dataset
    ]

    return content


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
