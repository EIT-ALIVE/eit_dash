import os
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, html, ALL
from dash.exceptions import PreventUpdate

import eit_dash.definitions.element_ids as ids
from eit_dash.definitions.option_lists import InputFiletypes


@callback(
    Output(ids.NFILES_PLACEHOLDER, 'children'),
    Output(ids.CHOOSE_DATA_POPUP, 'is_open'),
    Input(ids.SELECT_FILES_BUTTON, 'n_clicks'),
    State(ids.SELECT_FILES_BUTTON, 'filename'),
    State(ids.INPUT_TYPE_SELECTOR, 'value'),
    prevent_initial_call=True
)
def open_modal(contents, name, vendor): # pylint: disable=unused-argument
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
        id=f'card-{confirm_click}'
    )
    if container_state:
        container_state += [card]
    else:
        container_state = [card]

    return container_state


# file browser
@callback(
    Output(ids.CWD, 'children'),
    Input(ids.STORED_CWD, 'data'),
    Input(ids.PARENT_DIR, 'n_clicks'),
    Input(ids.CWD, 'children'),
    prevent_initial_call=True)
def get_parent_directory(stored_cwd, n_clicks, currentdir):
    triggered_id = ctx.triggered_id
    if triggered_id == ids.STORED_CWD:
        return stored_cwd
    parent = Path(currentdir).parent.as_posix()
    return parent


@callback(
    Output(ids.CWD_FILES, 'children'),
    Input(ids.CWD, 'children'))
def list_cwd_files(cwd):
    path = Path(cwd)

    cwd_files = []
    if path.is_dir():
        files = sorted(os.listdir(path), key=str.lower)
        for i, file in enumerate(files):
            filepath = Path(file)
            extension = filepath.suffix if not filepath.name.startswith('.') else filepath.name
            full_path = os.path.join(cwd, filepath.as_posix())

            is_dir = Path(full_path).is_dir()
            link = html.A([
                html.Span(
                    file, id={'type': 'listed_file', 'index': i},
                    title=full_path,
                    style={'fontWeight': 'bold'} if is_dir else {}
                )], href='#')
            prepend = '' if not is_dir else '📂'
            cwd_files.append(prepend)
            cwd_files.append(link)
            cwd_files.append(html.Br())
    return cwd_files

@callback(
    Output(ids.STORED_CWD, 'data'),
    Input({'type': 'listed_file', 'index': ALL}, 'n_clicks'),
    State({'type': 'listed_file', 'index': ALL}, 'title'))
def store_clicked_file(n_clicks, title):
    if not n_clicks or set(n_clicks) == {None}:
        raise PreventUpdate
    index = ctx.triggered_id['index']
    return title[index]

