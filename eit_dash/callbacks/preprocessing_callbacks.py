from dash import html, Input, Output, State, callback, ctx

import dash_bootstrap_components as dbc
import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles


# this callback runs when the page is loaded (the title of the preprocessing is created)
# and loads the data in the resampling card
@callback(
    Output(ids.RESAMPLING_CARD, 'children'),
    Input(ids.PREPROCESING_TITLE, 'children')
)
def load_datasets(title):  # pylint: disable=unused-argument
    dummy_data = [
        dict(Number=1, sampling_frequency=100),
        dict(Number=2, sampling_frequency=50),
        dict(Number=3, sampling_frequency=250),
    ]

    row = [dbc.Row([
        dbc.Col([html.H6('Dataset')]),
        dbc.Col([html.H6('Sampling frequency')]),
        dbc.Col([html.H6('Resample to')])
    ]),
        html.P()]

    row += [dbc.Row([
        dbc.Col(f'Dataset {data["Number"]}'),
        dbc.Col(f'{data["sampling_frequency"]} Hz'),
        dbc.Col([dbc.Input(
            type="number",
            placeholder="Resampling frequency",
            value=100
        )]),
        html.P()
    ]) for data in dummy_data]

    return row


# apply resampling
@callback(
    [Output(ids.OPEN_SYNCH_BUTTON, 'disabled'),
     Output(ids.OPEN_SELECT_RANGE_BUTTON, 'disabled'),
     Output(ids.OPEN_FILTER_DATA_BUTTON, 'disabled')],
    Input(ids.CONFIRM_RESAMPLING_BUTTON, 'n_clicks'),
    prevent_initial_call=True
)
def apply_resampling(apply_click): # pylint: disable=unused-argument

    return False, False, False
