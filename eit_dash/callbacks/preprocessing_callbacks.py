from dash import html, Input, Output, State, callback, ctx, dcc, MATCH
from eit_dash.app import data_object
from eit_dash.definitions.option_lists import PeriodsSelectMethods
from eit_dash.utils.common import create_slider_figure, get_signal_options
from eitprocessing.sequence import Sequence

import dash_bootstrap_components as dbc
import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
import numpy as np
import plotly.graph_objs as go


def check_continuous_data_loaded() -> bool:
    """
    Checks if continuous data have been loaded.

    Return: True if continuous data are present, False otherwise
    """
    loaded_data = data_object.get_all_sequences()
    for dataset in loaded_data:
        if dataset.continuous_data:
            return True

    return False


def create_resampling_card(loaded_data):
    row = [
        dbc.Row(
            [dbc.Col([html.H6("Dataset")]), dbc.Col([html.H6("Sampling frequency")])]
        ),
        html.P(),
    ]

    row += [
        dbc.Row(
            [
                dbc.Col(f'{data["Name"]}'),
                dbc.Col(f'{data["Sampling frequency"]} Hz'),
                html.P(),
            ]
        )
        for data in loaded_data
    ]

    options = [
        {"label": f'{data["Name"]}', "value": str(i)}
        for i, data in enumerate(loaded_data)
    ]

    return row, options


def create_loaded_data_summary():
    loaded = []

    loaded_data = data_object.get_all_sequences()

    for dataset in loaded_data:
        loaded.append(
            dbc.Row([html.Div(f"Loaded {dataset.label}", style={"textAlign": "left"})])
        )

    return loaded


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
                }
            )

    return data


def get_suggested_resampling(loaded_data):
    resampling_freq = 0
    for data in loaded_data:
        if data["Data type"] != "EIT":
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
    # loaded_data = get_loaded_data()
    # continuous_data_loaded = check_continuous_data_loaded()
    #
    # if not continuous_data_loaded:
    #     return [], [], [], None
    #
    # suggested_resampling = get_suggested_resampling(loaded_data)
    #
    # row, options = create_resampling_card(loaded_data)
    #
    # return row, options, suggested_resampling

    # TODO: uncomment lines above for resampling

    return [], [], [], None


# apply resampling
@callback(
    [
        Output(ids.OPEN_SYNCH_BUTTON, "disabled"),
        Output(ids.OPEN_SELECT_PERIODS_BUTTON, "disabled"),
        Output(ids.OPEN_FILTER_DATA_BUTTON, "disabled"),
        Output(ids.SUMMARY_COLUMN, "children"),
    ],
    [
        Input(ids.PREPROCESING_TITLE, "children"),
    ],
    [
        State(ids.SUMMARY_COLUMN, "children"),
    ],
    prevent_initial_call=False,
)
def update_summary(start, summary):  # pylint: disable=unused-argument
    trigger = ctx.triggered_id

    if trigger is None:
        data = create_loaded_data_summary()
        summary += data

    return False, False, False, summary


# open/close modal dialog for data synchronization
@callback(
    Output(ids.SYNCHRONIZATION_POPUP, "is_open"),
    [
        Input(ids.OPEN_SYNCH_BUTTON, "n_clicks"),
        Input(ids.SYNCHRONIZATION_CONFIRM_BUTTON, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def open_synch_modal(open_click, confirm_click):  # pylint: disable=unused-argument
    trigger = ctx.triggered_id

    if trigger == ids.OPEN_SYNCH_BUTTON:
        return True

    return False


# open/close modal dialog for periods selection
@callback(
    Output(ids.PERIODS_SELECTION_POPUP, "is_open"),
    [
        Input(ids.OPEN_SELECT_PERIODS_BUTTON, "n_clicks"),
        Input(ids.PERIODS_CONFIRM_BUTTON, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def open_periods_modal(open_click, confirm_click):  # pylint: disable=unused-argument
    trigger = ctx.triggered_id

    if trigger == ids.OPEN_SELECT_PERIODS_BUTTON:
        return True

    return False


# populate modal body according to the selected method
@callback(
    Output(ids.PERIODS_SELECTION_SELECT_DATASET, "children"),
    Input(ids.PERIODS_METHOD_SELECTOR, "value"),
    prevent_initial_call=True,
)
def populate_periods_selection_datasets(method):  # pylint: disable=unused-argument
    int_value = int(method)

    if int_value == PeriodsSelectMethods.Manual.value:
        signals = data_object.get_all_sequences()
        options = [
            {"label": sequence.label, "value": index}
            for index, sequence in enumerate(signals)
        ]

        body = [
            html.H6("Select one dataset"),
            dbc.Select(
                id=ids.PREPROCESING_DATASET_SELECT,
                options=options,
            ),
        ]
    else:
        body = []

    return body


# populate signals selection in the manual selection case
@callback(
    Output(ids.PREPROCESING_SIGNALS_CHECKBOX_ROW, "children"),
    Input(ids.PREPROCESING_DATASET_SELECT, "value"),
    prevent_initial_call=True,
)
def populate_periods_selection_datasets(dataset):  # pylint: disable=unused-argument
    if dataset:
        options = get_signal_options(
            data_object.get_sequence_at(int(dataset)), show_eit=True
        )
        body = [
            html.H6("Select the signals to be displayed"),
            dcc.Checklist(
                id=ids.PREPROCESING_SIGNALS_CHECKBOX,
                inputStyle=styles.CHECKBOX_INPUT,
                options=options,
            ),
        ]

        return body


# show the selected signals
@callback(
    Output(ids.PREPROCESING_PERIODS_GRAPH, "figure"),
    Input(ids.PREPROCESING_SIGNALS_CHECKBOX, "value"),
    [
        State(ids.PREPROCESING_SIGNALS_CHECKBOX, "options"),
        State(ids.PREPROCESING_DATASET_SELECT, "value"),
    ],
    prevent_initial_call=True,
)
def plot_signal(signals, options, dataset):  # pylint: disable=unused-argument
    data = data_object.get_sequence_at(int(dataset))
    cont_data = []
    eit_variants = []
    for sig in signals:
        if sig == 0:
            eit_variants.append("raw")
        else:
            cont_data.append(options[sig]["label"])

    figure = create_slider_figure(data, eit_variants, cont_data)

    return figure


# Show dataset
@callback(
    Output(ids.SYNC_DATA_PREVIEW_CONTAINER, "children"),
    Input(ids.DATASET_SELECTION_CHECKBOX, "value"),
    State(ids.SYNC_DATA_PREVIEW_CONTAINER, "children"),
    prevent_initial_call=True,
)
def show_data(selected_dataset, current_content):  # pylint: disable=unused-argument
    x = np.linspace(-2 * np.pi, 2 * np.pi, 201)
    sample_data = np.sin(x)

    fig = go.Figure(data=[go.Scatter(y=sample_data)])

    content = [
        dcc.Graph(
            figure=fig, id={"type": ids.SYNC_DATA_PREVIEW_GRAPH, "index": selected}
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
