import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, html

import eit_dash.definitions.element_ids as ids
from eit_dash.definitions.option_lists import InputFiletypes


@callback(
    [Output(ids.CHOOSE_DATA_POPUP, 'is_open'), Output(ids.NFILES_PLACEHOLDER, 'children')],
    [Input(ids.ADD_DATA_BUTTON, 'n_clicks'), Input(ids.SELECT_FILES_BUTTON, 'n_clicks')],
    prevent_initial_call=True
)
def open_modal(add_data_click, select_files_click): # pylint: disable=unused-argument
    flag = False

    trigger = ctx.triggered_id
    if trigger == ids.SELECT_FILES_BUTTON:
        flag = True

    return True, flag


@callback(
    Output(ids.DATA_SELECTOR_OPTIONS, 'hidden'),
    Input(ids.NFILES_PLACEHOLDER, 'children'),
    prevent_initial_call=True,
)
def load_file(flag):
    if flag:
        return False
    return True

@callback(
    Output(ids.DATASET_CONTAINER, 'children'),
    Input(ids.LOAD_CONFIRM_BUTTON, 'n_clicks'),
    State(ids.DATASET_CONTAINER, 'children'),
    State(ids.INPUT_TYPE_SELECTOR, 'value'),
    prevent_initial_call=True,
)
def show_info(confirm_click, container_state, filetype):
    #TODO read data from file
    #TODO read secondary input parameters from input selection

    dummy_data = {
        'N_signals': 3,
        'duration': 12,
        'n_frames': 234,
        'filename': 'file.bin',
        'etc': 'etc',
    }
    
    card_list = [
            html.H4(f'Dataset {confirm_click}', className="card-title"),
            html.H6(InputFiletypes(int(filetype)).name, className="card-subtitle"),
        ]
    card_list += [dbc.Row(f'{data}: {value}', style={'margin-left': 10}) for data, value in dummy_data.items()]
    
    card = dbc.Card(
        dbc.CardBody(card_list),
    )
    if container_state:
        container_state += [card] 
    else:
        container_state = [card]

    return container_state
    
    