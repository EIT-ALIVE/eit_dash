from dash import Input, Output, callback

import eit_dash.definitions.element_ids as ids


@callback(
    [Output(ids.OPEN_SYNCH_BUTTON, 'disabled'),
     Output(ids.OPEN_SELECT_RANGE_BUTTON, 'disabled'),
     Output(ids.OPEN_FILTER_DATA_BUTTON, 'disabled')],
    Input(ids.CONFIRM_RESAMPLING_BUTTON, 'n_clicks'),
    prevent_initial_call=True
)
def apply_resampling(apply_click): # pylint: disable=unused-argument

    return False, False, False
