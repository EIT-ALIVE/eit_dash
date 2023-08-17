from dash import html, Input, Output, State, callback, ctx
from eit_dash.definitions.option_lists import SynchMethods

import dash_bootstrap_components as dbc
import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles

dummy_data = [
    dict(Number=1, sampling_frequency=100),
    dict(Number=2, sampling_frequency=50),
    dict(Number=3, sampling_frequency=250),
]


# this callback runs when the page is loaded (the title of the preprocessing is created)
# and loads the data in the resampling card and in the dataset selrction menu
@callback(
    [Output(ids.RESAMPLING_CARD, 'children'), Output(ids.DATASET_SELECTION_CHECKBOX, 'options')],
    Input(ids.PREPROCESING_TITLE, 'children')
)
def load_datasets(title):  # pylint: disable=unused-argument

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

    options = [{'label': f'Dateset {data["Number"]}', 'value': str(i)}
               for i, data in enumerate(dummy_data)]

    return row, options


# apply resampling
@callback(
    [Output(ids.OPEN_SYNCH_BUTTON, 'disabled'),
     Output(ids.OPEN_SELECT_RANGE_BUTTON, 'disabled'),
     Output(ids.OPEN_FILTER_DATA_BUTTON, 'disabled'),
     Output(ids.SUMMARY_COLUMN, 'children')],
    Input(ids.CONFIRM_RESAMPLING_BUTTON, 'n_clicks'),
    State(ids.SUMMARY_COLUMN, 'children'),
    prevent_initial_call=True
)
def apply_resampling(apply_click, summary):  # pylint: disable=unused-argument
    summary += [
        dbc.Row([html.Div('Resampled dataset at 100Hz', style=styles.SUMMARY_ELEMENT)])
    ]
    return False, False, False, summary


# open/close modal dialog for data synchronization
@callback(
    Output(ids.SYNCHRONIZATION_POPUP, 'is_open'),
    [Input(ids.OPEN_SYNCH_BUTTON, 'n_clicks'),
     Input(ids.SYNCHRONIZATION_CONFIRM_BUTTON, 'n_clicks')],
    prevent_initial_call=True
)
def open_synch_modal(open_click, confirm_click):  # pylint: disable=unused-argument

    trigger = ctx.triggered_id

    if trigger == ids.OPEN_SYNCH_BUTTON:
        return True
    elif trigger == ids.SYNCHRONIZATION_CONFIRM_BUTTON:
        return False
