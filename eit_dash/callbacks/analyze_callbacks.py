from dash import Input, Output, State, callback, ctx
from matplotlib import pyplot as plt

from eitprocessing.parameters.eeli import EELI

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.definitions.constants import FILTERED_EIT_LABEL
from eit_dash.app import data_object
from eit_dash.utils.common import (
    create_filter_results_card,
    create_loaded_data_summary,
    create_selected_period_card,
)

import plotly.graph_objects as go

eeli = []


@callback(
    Output(ids.SUMMARY_COLUMN_ANALYZE, "children", allow_duplicate=True),
    Output(ids.ANALYZE_SELECT_PERIOD_VIEW, "options"),
    [
        Input(ids.ANALYZE_RESULTS_TITLE, "children"),
    ],
    [
        State(ids.SUMMARY_COLUMN_ANALYZE, "children"),
    ],
    # this allows duplicate outputs with initial call
    prevent_initial_call="initial_duplicate",
)
def page_setup(_, summary):
    """Setups the page elements when it starts up.

    When the page is loaded, it populates the summary column
    with the info about the loaded datasets and the preprocessing steps.
    Populates the periods selections element with the loaded periods.
    """
    trigger = ctx.triggered_id
    options = []

    if trigger is None:
        loaded_data = create_loaded_data_summary()
        summary += loaded_data

        filter_params = {}

        for period in data_object.get_all_stable_periods():
            if not filter_params:
                filter_params = (
                    period.get_data()
                    .continuous_data.data["global_impedance_filtered"]
                    .parameters
                )

            summary += [
                create_selected_period_card(
                    period.get_data(),
                    period.get_dataset_index(),
                    period.get_period_index(),
                    False,
                )
            ]

            # populate period selection
            options.append(
                {
                    "label": f"Period {period.get_period_index()}",
                    "value": period.get_period_index(),
                }
            )

        summary += [create_filter_results_card(filter_params)]

    return summary, options


@callback(
    Output(ids.EELI_RESULTS_GRAPH_DIV, "hidden"),
    Input(ids.EELI_APPLY, "n_clicks"),
    prevent_initial_call=True,
)
def apply_eeli(_):
    """Apply EELI and store results"""

    global eeli

    eeli.clear()

    periods = data_object.get_all_stable_periods()

    for period in periods:
        sequence = period.get_data()
        eeli_result_filtered = EELI().compute_parameter(sequence, FILTERED_EIT_LABEL)

        # TODO: the results should be stored in the sequence object
        eeli_result_filtered["index"] = period.get_period_index()

        eeli.append(eeli_result_filtered)

    return False


@callback(
    [
        Output(ids.EELI_RESULTS_GRAPH, "figure"),
        Output(ids.EELI_RESULTS_GRAPH, "style"),
    ],
    Input(ids.ANALYZE_SELECT_PERIOD_VIEW, "value"),
    prevent_initial_call=True,
)
def show_eeli(selected):
    """
    Show the results of the EELI for the selected period.
    """
    figure = go.Figure()

    sequence = data_object.get_stable_period(int(selected)).get_data()
    for e in eeli:
        if e["index"] == int(selected):
            result = e

    figure.add_trace(
        go.Scatter(
            x=sequence.continuous_data[FILTERED_EIT_LABEL].time,
            y=sequence.continuous_data[FILTERED_EIT_LABEL].values,
            name=FILTERED_EIT_LABEL,
        )
    )

    figure.add_hline(y=result["mean"], line_color="red", name="Mean")
    figure.add_hline(y=result["median"], line_color="red", name="Median")

    figure.add_scatter(
        x=sequence.continuous_data[FILTERED_EIT_LABEL].time[result["indices"]],
        y=result["values"],
        line_color="black",
        name="EELIs",
        mode="markers",
    )

    sd_upper = result["mean"] + result["standard deviation"]
    sd_lower = result["mean"] - result["standard deviation"]

    figure.add_trace(
        go.Scatter(
            x=sequence.continuous_data[FILTERED_EIT_LABEL].time,
            y=[sd_upper] * len(sequence.continuous_data[FILTERED_EIT_LABEL].time),
            fill=None,
            mode="lines",
            line_color="rgba(0,0,255,0)",  # Set to transparent blue
            name="Standard deviation",
        )
    )

    # Add the lower bound line
    figure.add_trace(
        go.Scatter(
            x=sequence.continuous_data[FILTERED_EIT_LABEL].time,
            y=[sd_lower] * len(sequence.continuous_data[FILTERED_EIT_LABEL].time),
            fill="tonexty",  # Fill area below this line
            mode="lines",
            line_color="rgba(0,0,255,0.3)",  # Set to semi-transparent blue
            name="Standard deviation",
        )
    )

    return figure, styles.GRAPH
