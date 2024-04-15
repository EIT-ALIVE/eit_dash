from dash import Input, Output, State, callback, ctx

import eit_dash.definitions.element_ids as ids


@callback(
    [Output(ids.SUMMARY_COLUMN, "children", allow_duplicate=True)],
    [
        Input(ids.ANALYZE_RESULTS_TITLE, "children"),
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
    with the info about the loaded datasets and the preprocessing steps
    """
    trigger = ctx.triggered_id

    results = []

    if trigger is None:
        data = []
        summary += data

    return results
