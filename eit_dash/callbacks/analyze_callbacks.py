import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx

import eit_dash.definitions.element_ids as ids
from eit_dash.app import data_object
from eit_dash.utils.common import (
    create_filter_results_card,
    create_loaded_data_summary,
    create_selected_period_card,
)


@callback(
    Output(ids.SUMMARY_COLUMN_ANALYZE, "children", allow_duplicate=True),
    [
        Input(ids.ANALYZE_RESULTS_TITLE, "children"),
    ],
    [
        State(ids.SUMMARY_COLUMN_ANALYZE, "children"),
    ],
    # this allows duplicate outputs with initial call
    prevent_initial_call="initial_duplicate",
)
def update_summary(_, summary):
    """Updates summary.

    When the page is loaded, it populates the summary column
    with the info about the loaded datasets and the preprocessing steps
    """
    trigger = ctx.triggered_id

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

        summary += [create_filter_results_card(filter_params)]

    return summary
