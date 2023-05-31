from dash import callback, Output, Input
import definitions.element_ids as ids

@callback(
    Output(ids.CHOOSE_DATA_POPUP, 'is_open'),
    Input(ids.ADD_DATA_BUTTON, 'n_clicks'),
    prevent_initial_call=True
)
def update_graph(value):
    return True