import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import MATCH, Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate
from eitprocessing.continuous_data import ContinuousData
from eitprocessing.data_collection import DataCollection
from eitprocessing.eit_data import EITData
from eitprocessing.sequence import Sequence

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.app import data_object
from eit_dash.definitions.option_lists import PeriodsSelectMethods
from eit_dash.utils.common import (
    create_slider_figure,
    get_signal_options,
    mark_selected_period,
)

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


def create_loaded_data_summary():
    loaded = []

    loaded_data = data_object.get_all_sequences()

    for dataset in loaded_data:
        loaded.append(
            dbc.Row([html.Div(f"Loaded {dataset.label}", style={"textAlign": "left"})]),
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
                },
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
            data_object.get_sequence_at(int(dataset)), show_eit=True,
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


# make visible the div containing the graphs and the buttons
@callback(
    Output(ids.PERIODS_SELECTION_DIV, "hidden"),
    Input(ids.PREPROCESING_SIGNALS_CHECKBOX, "value"),
    prevent_initial_call=True,
)
def show_selection_div(signals):  # pylint: disable=unused-argument
    if signals:
        return False

    return True


@callback(
    [
        Output(ids.PREPROCESING_PERIODS_GRAPH, "figure", allow_duplicate=True),
        Output(ids.PREPROCESING_PERIODS_GRAPH, "style", allow_duplicate=True),
    ],
    [
        Input(ids.PREPROCESING_DATASET_SELECT, "value"),
    ],
    prevent_initial_call=True,
)
def initialize_figure(
    dataset,
):
    """When the dataset is selected, the figure is initialized."""
    # the callback is run also when populating the dataset options.
    # In this case we don't want to run it
    if not dataset:
        raise PreventUpdate

    data = data_object.get_sequence_at(int(dataset))

    style = styles.EMPTY_ELEMENT

    figure = create_slider_figure(
            data,
            ["raw"],
            [continuous_datum for continuous_datum in data.continuous_data],
        )
    current_figure = figure

    return current_figure, style


@callback(
    [
        Output(ids.PREPROCESING_PERIODS_GRAPH, "figure", allow_duplicate=True),
        Output(ids.PREPROCESING_RESULTS_CONTAINER, "children"),
    ],
    [

        Input(ids.PREPROCESING_SELECT_BTN, "n_clicks"),
    ],
    [
        State(ids.PREPROCESING_SIGNALS_CHECKBOX, "value"),
        State(ids.PREPROCESING_SIGNALS_CHECKBOX, "options"),
        State(ids.PREPROCESING_DATASET_SELECT, "value"),
        State(ids.PREPROCESING_PERIODS_GRAPH, "relayoutData"),
        State(ids.PREPROCESING_PERIODS_GRAPH, "figure"),
        State(ids.PREPROCESING_RESULTS_CONTAINER, "children"),
    ],
    prevent_initial_call=True,
)
def select_period(
    select_periods,
    signals,
    options,
    dataset,
    slidebar_stat,
    current_figure,
    current_summary,
):
    """Mark the selected period in the graph and save it."""
    data = data_object.get_sequence_at(int(dataset))

    if slidebar_stat is not None:
        if "xaxis.range" in slidebar_stat:
            start_sample = slidebar_stat["xaxis.range"][0]
            stop_sample = slidebar_stat["xaxis.range"][1]
        elif ("xaxis.range[0]" in slidebar_stat) and ("xaxis.range[1]" in slidebar_stat):
            start_sample = slidebar_stat["xaxis.range[0]"]
            stop_sample = slidebar_stat["xaxis.range[1]"]
        else:
            start_sample = data.time[0]
            stop_sample = data.time[-1]
    else:
        start_sample = data.time[0]
        stop_sample = data.time[-1]

    content = [
        dbc.Row(
            [html.Div(f"Selected new period from {start_sample} to {stop_sample}")],
        ),
    ]

    # TODO: refactor to avoid duplications

    # cut the eit data and the continuous data and add them to a new DataCollections

    eit_data_cut = DataCollection(data_type=EITData)
    continuous_data_cut = DataCollection(data_type=ContinuousData)

    for data_type in (eit := data.eit_data):
        eit_data_cut.add(eit[data_type].select_by_time(start_sample, stop_sample))

    for data_type in (cont := data.continuous_data):
        # add just the selected signals
        if data_type in cont:
            continuous_data_cut.add(cont[data_type].select_by_time(start_sample, stop_sample))

    cut_data = Sequence(
        label="whatever",
        eit_data=eit_data_cut,
        continuous_data=continuous_data_cut,
    )
    # TODO: explore Patch https://dash.plotly.com/partial-properties
    current_figure = mark_selected_period(current_figure, cut_data)

    # TODO: refactor to avoid duplications
    ok = [options[s]["label"] for s in signals]
    for s in current_figure["data"]:
        if s["name"] in ok:
            s["visible"] = True
        else:
            s["visible"] = False

    current_summary += content

    return current_figure, current_summary


@callback(
    [
        Output(ids.PREPROCESING_PERIODS_GRAPH, "figure", allow_duplicate=True),
        Output(ids.PREPROCESING_PERIODS_GRAPH, "style", allow_duplicate=True),
    ],
    [
        Input(ids.PREPROCESING_SIGNALS_CHECKBOX, "value"),
    ],
    [
        State(ids.PREPROCESING_SIGNALS_CHECKBOX, "options"),
        State(ids.PREPROCESING_PERIODS_GRAPH, "figure"),
    ],
    prevent_initial_call=True,
)
def select_signals(
    signals,
    options,
    current_figure,
):
    """React to ticking a signal. The function updates the figure by showing the ticked signals
    and hiding the unticked ones.
    """
    # the callback is run also when populating the signals options (no figure created).
    # In this case we don't want to run it
    if not current_figure:
        raise PreventUpdate

    signals = signals or []
    selected = [options[s]["label"] for s in signals]

    for s in current_figure["data"]:
        if s["name"] in selected:
            s["visible"] = True
        else:
            s["visible"] = False

    style = styles.GRAPH

    return current_figure, style


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
