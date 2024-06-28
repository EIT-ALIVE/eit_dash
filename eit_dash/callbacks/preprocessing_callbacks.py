from __future__ import annotations

import contextlib
import time
from typing import TYPE_CHECKING

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import ALL, Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate
from eitprocessing.datahandling.continuousdata import ContinuousData
from eitprocessing.filters.butterworth_filters import ButterworthFilter

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.app import data_object
from eit_dash.definitions.constants import FILTERED_EIT_LABEL, RAW_EIT_LABEL
from eit_dash.definitions.option_lists import FilterTypes, PeriodsSelectMethods
from eit_dash.utils.common import (
    create_filter_results_card,
    create_info_card,
    create_selected_period_card,
    create_slider_figure,
    get_selections_slidebar,
    get_signal_options,
    mark_selected_periods,
)
from eit_dash.utils.data_singleton import LoadedData

if TYPE_CHECKING:
    from eitprocessing.datahandling.sequence import Sequence

tmp_results: LoadedData = LoadedData()

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

    options = [{"label": f'{data["Name"]}', "value": str(i)} for i, data in enumerate(loaded_data)]

    return row, options


def get_loaded_data():
    loaded_data = data_object.get_all_sequences()
    data = []
    for dataset in loaded_data:
        name = dataset.label
        if dataset.continuous_data:
            data += [{"Name": name, "Data type": channel} for channel in dataset.continuous_data]
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


@callback(
    [
        Output(ids.RESAMPLING_CARD, "children"),
        Output(ids.RESAMPLING_CARD_BODY, "children"),
        Output(ids.DATASET_SELECTION_CHECKBOX, "options"),
        Output(ids.RESAMPLING_FREQUENCY_INPUT, "value"),
    ],
    Input(ids.PREPROCESING_TITLE, "children"),
)
def load_datasets(title):
    """

    This callback runs when the page is loaded (the title of the preprocessing is created) and loads.

     the data in the resampling card and in the dataset selection menu.
    """
    # ruff: noqa: ERA001
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


@callback(
    [
        Output(ids.OPEN_SYNCH_BUTTON, "disabled"),
        Output(ids.OPEN_SELECT_PERIODS_BUTTON, "disabled"),
        Output(ids.SUMMARY_COLUMN, "children", allow_duplicate=True),
        Output(ids.PREPROCESING_RESULTS_CONTAINER, "children", allow_duplicate=True),
    ],
    [
        Input(ids.PREPROCESING_TITLE, "children"),
    ],
    [
        State(ids.SUMMARY_COLUMN, "children"),
    ],
    # this allows duplicate outputs with initial call
    prevent_initial_call="initial_duplicate",
)
def update_summary(start, summary):
    """Updates summary.

    When the page is loaded, it populates the summary column
    with the info about the loaded datasets. It also checks if periods
    have been already saved and populates the results accordingly.
    """
    trigger = ctx.triggered_id

    results = []

    if trigger is None:
        for d in data_object.get_all_sequences():
            card = create_info_card(d)
            summary += [card]

        for p in data_object.get_all_stable_periods():
            data = p.get_data()
            results.append(
                create_selected_period_card(data, data.label, p.get_period_index()),
            )

    return False, False, summary, results


@callback(
    Output(ids.SYNCHRONIZATION_POPUP, "is_open"),
    [
        Input(ids.OPEN_SYNCH_BUTTON, "n_clicks"),
        Input(ids.SYNCHRONIZATION_CONFIRM_BUTTON, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def open_synch_modal(open_click, confirm_click) -> bool:
    """open/close modal dialog for data synchronization."""
    trigger = ctx.triggered_id

    return trigger == ids.OPEN_SYNCH_BUTTON


@callback(
    Output(ids.PERIODS_SELECTION_POPUP, "is_open"),
    [
        Input(ids.OPEN_SELECT_PERIODS_BUTTON, "n_clicks"),
        Input(ids.PERIODS_CONFIRM_BUTTON, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def open_periods_modal(open_click, confirm_click) -> bool:
    """open/close modal dialog for periods selection."""
    trigger = ctx.triggered_id

    return trigger == ids.OPEN_SELECT_PERIODS_BUTTON


@callback(
    Output(ids.PERIODS_SELECTION_SELECT_DATASET, "children"),
    Input(ids.PERIODS_METHOD_SELECTOR, "value"),
    prevent_initial_call=False,
)
def populate_periods_selection_modal(method):
    """Populate modal body according to the selected method for stable periods selection."""
    int_value = int(method)

    if int_value == PeriodsSelectMethods.Manual.value:
        signals = data_object.get_all_sequences()
        options = [{"label": sequence.label, "value": index} for index, sequence in enumerate(signals)]

        body = (
            [
                html.H6("Select one dataset"),
                dbc.Select(
                    id=ids.PREPROCESING_DATASET_SELECT,
                    options=options,
                    value=str(options[0]["value"]),
                ),
            ]
            if options
            else []
        )
    else:
        body = []

    return body


@callback(
    Output(ids.PERIODS_SELECTION_DIV, "hidden"),
    Input(ids.PREPROCESING_SIGNALS_CHECKBOX, "value"),
    prevent_initial_call=True,
)
def show_selection_div(signals):
    """Make visible the div containing the graphs and the buttons."""
    return not signals


@callback(
    [
        Output(ids.PREPROCESING_PERIODS_GRAPH, "figure", allow_duplicate=True),
        Output(ids.PREPROCESING_PERIODS_GRAPH, "style", allow_duplicate=True),
        Output(ids.PREPROCESING_SIGNALS_CHECKBOX_ROW, "children"),
    ],
    [
        Input(ids.PREPROCESING_DATASET_SELECT, "value"),
    ],
    prevent_initial_call=True,
)
def initialize_figure(
    dataset,
):
    """When the dataset is selected, the figure and the checkbox are initialized."""
    # the callback is run also when populating the dataset options.
    # In this case we don't want to run it
    if not dataset:
        raise PreventUpdate

    data = data_object.get_sequence_at(int(dataset))

    style = styles.EMPTY_ELEMENT

    current_figure = create_slider_figure(
        data,
        list(data.continuous_data),
    )

    # mark the stable periods already selected, if there are any
    if saved_periods := data_object.get_dataset_stable_periods(int(dataset)):
        current_figure = mark_selected_periods(current_figure, saved_periods)

    options = get_signal_options(
        data_object.get_sequence_at(int(dataset)),
        show_eit=True,
    )

    signals_checkbox = [
        html.H6("Select the signals to be displayed"),
        dcc.Checklist(
            id=ids.PREPROCESING_SIGNALS_CHECKBOX,
            inputStyle=styles.CHECKBOX_INPUT,
            options=options,
        ),
    ]

    # THIS IS A TEMPORARY PATCH
    time.sleep(2)

    return current_figure, style, signals_checkbox


@callback(
    [
        Output(ids.PREPROCESING_PERIODS_GRAPH, "figure", allow_duplicate=True),
        Output(ids.PREPROCESING_RESULTS_CONTAINER, "children", allow_duplicate=True),
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
    # get the first and last sample selected in the slidebar
    if slidebar_stat is not None:
        start_sample, stop_sample = get_selections_slidebar(slidebar_stat)

        if not start_sample:
            start_sample = data.time[0]
        if not stop_sample:
            stop_sample = data.time[-1]
    else:
        start_sample = data.time[0]
        stop_sample = data.time[-1]

    period_index = data_object.get_next_period_index()

    cut_data = data.select_by_time(
        start_time=start_sample,
        end_time=stop_sample,
        label=f"Period {period_index}",
    )

    data_object.add_stable_period(cut_data, int(dataset))

    # TODO: explore Patch https://dash.plotly.com/partial-properties
    current_figure = mark_selected_periods(
        current_figure,
        [data_object.get_stable_period(period_index)],
    )

    # TODO: refactor to avoid duplications
    ok = [options[s]["label"] for s in signals]
    for s in current_figure["data"]:
        if s["name"] in ok:
            s["visible"] = True
        else:
            s["visible"] = False

    content = [create_selected_period_card(cut_data, data.label, period_index)]
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
    """React to ticking a signal.

    The function updates the figure by showing the ticked signals and hiding the unticked ones.
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


@callback(
    Output(ids.PREPROCESING_RESULTS_CONTAINER, "children", allow_duplicate=True),
    Output(ids.PREPROCESING_PERIODS_GRAPH, "figure", allow_duplicate=True),
    [
        Input({"type": ids.REMOVE_PERIOD_BUTTON, "index": ALL}, "n_clicks"),
    ],
    [
        State(ids.PREPROCESING_RESULTS_CONTAINER, "children"),
        State(ids.PREPROCESING_PERIODS_GRAPH, "figure"),
    ],
    prevent_initial_call=True,
)
def remove_period(n_clicks, container, figure):
    """React to clicking the remove button of a period.

    Removes the card from the results and the period from the saved selections.
    """
    # at the element creation time, the update should be avoided
    if all(element is None for element in n_clicks):
        raise PreventUpdate

    input_id = int(ctx.triggered_id["index"])

    # remove from the singleton
    data_object.remove_stable_period(input_id)

    # remove from the temp data, if present
    if tmp_results:
        try:
            tmp_results.remove_stable_period(input_id)
        except ValueError:
            contextlib.suppress(Exception)

    # remove from the figure (if the figure exists)
    try:
        figure["data"] = [trace for trace in figure["data"] if "meta" not in trace or trace["meta"]["uid"] != input_id]
    except TypeError:
        contextlib.suppress(Exception)

    results = [card for card in container if f"'index': '{input_id}'" not in str(card)]

    return results, figure


# filters
@callback(
    Output(ids.OPEN_FILTER_DATA_BUTTON, "disabled"),
    Input(ids.PREPROCESING_RESULTS_CONTAINER, "children"),
    prevent_initial_call=True,
)
def enable_filter_button(results):
    """Enable the button for opening the filter modal."""
    return not results


@callback(
    [
        Output(ids.FILTERING_SELECTION_POPUP, "is_open"),
        Output(ids.FILTER_SELECTOR, "value"),
    ],
    [
        Input(ids.OPEN_FILTER_DATA_BUTTON, "n_clicks"),
        Input(ids.FILTERING_CLOSE_BUTTON, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def open_filtering_modal(open_click, confirm_click) -> bool:
    """open/close modal dialog for filtering data."""
    trigger = ctx.triggered_id

    if trigger == ids.OPEN_FILTER_DATA_BUTTON:
        return True, None

    return False, None


@callback(
    [
        Output(ids.FILTER_PARAMS, "hidden"),
        Output(ids.FILTER_CUTOFF_LOW, "disabled"),
        Output(ids.FILTER_CUTOFF_HIGH, "disabled"),
        Output(ids.FILTER_CUTOFF_LOW, "value"),
        Output(ids.FILTER_CUTOFF_HIGH, "value"),
    ],
    Input(ids.FILTER_SELECTOR, "value"),
    prevent_initial_call=True,
)
def show_filters_params(selected):
    """Make visible the div containing the filters params."""
    cutoff_low_enabled = cutoff_high_enabled = filter_params = False
    cutoff_low_val = cutoff_high_val = None

    # if no filter has been selected, hide the params
    if not selected:
        filter_params = True
    elif int(selected) == FilterTypes.lowpass.value:
        cutoff_low_enabled = True
    elif int(selected) == FilterTypes.highpass.value:
        cutoff_high_enabled = True

    return (
        filter_params,
        cutoff_low_enabled,
        cutoff_high_enabled,
        cutoff_low_val,
        cutoff_high_val,
    )


@callback(
    Output(ids.FILTER_APPLY, "disabled"),
    [
        Input(ids.FILTER_CUTOFF_LOW, "value"),
        Input(ids.FILTER_CUTOFF_HIGH, "value"),
        Input(ids.FILTER_ORDER, "value"),
    ],
    [
        State(ids.FILTER_CUTOFF_LOW, "value"),
        State(ids.FILTER_CUTOFF_HIGH, "value"),
        State(ids.FILTER_ORDER, "value"),
        State(ids.FILTER_SELECTOR, "value"),
    ],
    prevent_initial_call=True,
)
def enable_apply_button(
    co_low_in,
    co_high_in,
    order_in,
    co_low,
    co_high,
    order,
    filter_selected,
):
    """Enable the apply button."""
    if not filter_selected:
        return True

    return (
        not (
            (int(filter_selected) == FilterTypes.lowpass.value and co_high and co_high > 0)
            or (int(filter_selected) == FilterTypes.highpass.value and co_low and co_low > 0)
            or (
                int(filter_selected) in [FilterTypes.bandpass.value, FilterTypes.bandstop.value]
                and co_low
                and co_low > 0
                and co_high
                and co_high > 0
            )
        )
        and order
    )


@callback(
    [
        Output(ids.FILTERING_RESULTS_DIV, "hidden", allow_duplicate=True),
        Output(ids.FILTERING_CONFIRM_DIV, "hidden", allow_duplicate=True),
        Output(ids.FILTERING_SELECT_PERIOD_VIEW, "options", allow_duplicate=True),
    ],
    [
        Input(ids.FILTER_APPLY, "disabled"),
    ],
    prevent_initial_call=True,
)
def disable_results(disabled):
    """Hide and disable results if the apply button is disabled."""
    # flag for showing graphs and confirm button
    if not disabled:
        raise PreventUpdate

    hidden_div = True

    options = []

    return hidden_div, hidden_div, options


@callback(
    [
        Output(ids.PREPROCESING_RESULTS_CONTAINER, "children", allow_duplicate=True),
        Output(ids.FILTERING_RESULTS_DIV, "hidden", allow_duplicate=True),
        Output(ids.FILTERING_CONFIRM_DIV, "hidden", allow_duplicate=True),
        Output(ids.FILTERING_SELECT_PERIOD_VIEW, "options", allow_duplicate=True),
        Output(ids.ALERT_FILTER, "is_open"),
        Output(ids.ALERT_FILTER, "children"),
        Output(ids.UPDATE_FILTER_RESULTS, "children"),
    ],
    [
        Input(ids.FILTER_APPLY, "n_clicks"),
    ],
    [
        State(ids.FILTER_CUTOFF_LOW, "value"),
        State(ids.FILTER_CUTOFF_HIGH, "value"),
        State(ids.FILTER_ORDER, "value"),
        State(ids.FILTER_SELECTOR, "value"),
        State(ids.PREPROCESING_RESULTS_CONTAINER, "children"),
    ],
    prevent_initial_call=True,
)
def apply_filter(_, co_low, co_high, order, filter_selected, results):
    """Apply the filter."""
    global tmp_results  # noqa: PLW0602
    # flag for the alert message
    show_alert = False
    # alert message
    alert_msg = ""

    # placeholder to allow results update
    placeholder_div = "updated"

    # flag for showing graphs and confirm button
    hidden_div = False

    # build filter params
    filter_params = get_selected_parameters(co_high, co_low, order, filter_selected)

    options = []

    tmp_results.clear_data()

    # filter all the periods
    try:
        for period in data_object.get_all_stable_periods():
            filtered_data = filter_data(period.get_data(), filter_params)
            data = period.get_data()
            data.continuous_data.add(filtered_data)
            tmp_results.add_stable_period(
                data,
                0,
                period.get_period_index(),
            )

            options.append(
                {
                    "label": f"Period {period.get_period_index()}",
                    "value": period.get_period_index(),
                },
            )
    except ValueError as e:
        show_alert = True
        alert_msg = f"{e}"
        hidden_div = True
        placeholder_div = None

    return (
        results,
        hidden_div,
        hidden_div,
        options,
        show_alert,
        alert_msg,
        placeholder_div,
    )


@callback(
    [
        Output(ids.FILTERING_RESULTS_GRAPH, "figure"),
        Output(ids.FILTERING_RESULTS_GRAPH, "style"),
    ],
    Input(ids.FILTERING_SELECT_PERIOD_VIEW, "value"),
    Input(ids.UPDATE_FILTER_RESULTS, "children"),
    State(ids.FILTERING_SELECT_PERIOD_VIEW, "value"),
    prevent_initial_call=True,
)
def show_filtered_results(_, update, selected):
    """When selecting a period, shows the original and the filtered signal."""
    if not selected or not update:
        raise PreventUpdate

    fig = go.Figure()

    try:
        filtered_data = tmp_results.get_stable_period(int(selected)).get_data()
    except ValueError:
        return fig, styles.EMPTY_ELEMENT

    data = data_object.get_stable_period(int(selected)).get_data()

    fig.add_trace(
        go.Scatter(
            x=data.continuous_data[RAW_EIT_LABEL].time,
            y=data.continuous_data[RAW_EIT_LABEL].values,
            name="Original signal",
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=filtered_data.continuous_data.data[FILTERED_EIT_LABEL].time,
            y=filtered_data.continuous_data.data[FILTERED_EIT_LABEL].values,
            name="Filtered signal",
        ),
    )

    return fig, styles.GRAPH


@callback(
    [
        Output(ids.PREPROCESING_RESULTS_CONTAINER, "children", allow_duplicate=True),
        Output(ids.ALERT_SAVED_RESULTS, "is_open"),
        Output(ids.ALERT_SAVED_RESULTS, "children"),
    ],
    Input(ids.FILTERING_CONFIRM_BUTTON, "n_clicks"),
    State(ids.PREPROCESING_RESULTS_CONTAINER, "children"),
    prevent_initial_call=True,
)
def save_filtered_signal(confirm, results: list):
    """When clocking the confirm button, store the results in the singleton."""
    params = {}

    # save the filtered data
    for res in tmp_results.get_all_stable_periods():
        data = data_object.get_stable_period(res.get_period_index())
        tmp_data = res.get_data()
        data.update_data(tmp_data)

        if not params:
            params = tmp_data.continuous_data.data[FILTERED_EIT_LABEL].parameters

    # show info card
    for element in results:
        if element["props"]["id"] == ids.FILTERING_SAVED_CARD:
            results.remove(element)
    results += [create_filter_results_card(params)]

    return results, True, "Results have been saved"


def get_selected_parameters(co_high, co_low, order, filter_selected) -> dict:
    """Build the parameters dictionary for the filter.

    Args:
        co_high: cut off upper limit
        co_low: cut off lower limit
        order: filter order
        filter_selected: value coming from the filter selection dropbox

    Returns: dictionary containing parameters for the filter
    """
    if co_high is None:
        cutoff_frequency = co_low
    elif co_low is None:
        cutoff_frequency = co_high
    else:
        cutoff_frequency = [co_low, co_high]

    return {
        "filter_type": FilterTypes(int(filter_selected)).name,
        "cutoff_frequency": cutoff_frequency,
        "order": order,
    }


def filter_data(data: Sequence, filter_params: dict) -> ContinuousData | None:
    """Filter the impedance data in a period.

    Args:
        data: sequence containing the data
        filter_params: parameters for the filter

    Returns: the data with the filtered version added
    """
    filter_params["sample_frequency"] = data.eit_data.data["raw"].framerate

    filt = ButterworthFilter(**filter_params)

    gi = data.continuous_data[RAW_EIT_LABEL]

    return ContinuousData(
        FILTERED_EIT_LABEL,
        f"global_impedance filtered with {filter_params['filter_type']}",
        "a.u.",
        "impedance",
        derived_from=[*gi.derived_from, gi],
        parameters=filter_params,
        time=data.continuous_data[RAW_EIT_LABEL].time,
        values=filt.apply_filter(data.continuous_data[RAW_EIT_LABEL].values),
    )
