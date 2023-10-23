import json
import os
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, html, ALL
from dash.exceptions import PreventUpdate

import eit_dash.definitions.element_ids as ids
from eit_dash.definitions.option_lists import InputFiletypes, SignalSelections
from eitprocessing.binreader.sequence import Sequence

file_data = None


# managing the file selection
@callback(
    Output(ids.CHOOSE_DATA_POPUP, 'is_open'),
    Output(ids.NFILES_PLACEHOLDER, 'children'),
    Output(ids.ALERT_LOAD, 'is_open'),
    Input(ids.SELECT_FILES_BUTTON, 'n_clicks'),
    Input(ids.LOAD_CONFIRM_BUTTON, 'n_clicks'),
    State(ids.STORED_CWD, 'data'),
    State(ids.INPUT_TYPE_SELECTOR, 'value'),
    prevent_initial_call=True
)
def open_modal(open_btn, close_btn, file_path, file_type):  # pylint: disable=unused-argument
    open_modal = True
    data = None
    show_alert = False
    read_data_flag = False

    trigger = ctx.triggered_id

    # if the callback has not been triggered by the select files button,
    # get the information on the selected file and try to read it
    if trigger != ids.SELECT_FILES_BUTTON:
        path = Path(file_path)
        extension = path.suffix if not path.name.startswith('.') else path.name

        # check if the file extension is compatible with the file type selected
        if (int(file_type)) == InputFiletypes.Draeger.value:
            if extension == '.bin':
                read_data_flag = True

        # if the type check is ok, then close the file selector and read the data
        if read_data_flag:
            data = file_path
            open_modal = False

        # if it's not ok, then show an alert
        else:
            show_alert = True

    return open_modal, data, show_alert


@callback(
    Output(ids.DATA_SELECTOR_OPTIONS, 'hidden'),
    Output(ids.CHECKBOX_SIGNALS, 'options'),
    Output(ids.FILE_LENGTH_SLIDER, 'min'),
    Output(ids.FILE_LENGTH_SLIDER, 'max'),
    Input(ids.NFILES_PLACEHOLDER, 'children'),
    State(ids.INPUT_TYPE_SELECTOR, 'value'),
    prevent_initial_call=True)
def open_data_selector(data, file_type):
    options = []
    min_slider = 0
    max_slider = 0

    if not data:
        return True, options, min_slider, max_slider

    global file_data

    path = Path(data)
    file_data = Sequence.from_path(path, vendor=InputFiletypes(int(file_type)).name)
    min_slider=file_data.time[0]
    max_slider=file_data.time[-1]

    for frameset in file_data.framesets:
        if frameset == 'raw':
            label = 'raw'
            value = 3

        options.append({'label': label, 'value': value})

    return False, options, min_slider, max_slider


# @callback(
#     Output(ids.DATASET_CONTAINER, 'children'),
#     Input(ids.LOAD_CONFIRM_BUTTON, 'n_clicks'),
#     State(ids.NFILES_PLACEHOLDER, 'children'),
#     State(ids.DATASET_CONTAINER, 'children'),
#     State(ids.INPUT_TYPE_SELECTOR, 'value'),
#     prevent_initial_call=True,
# )
# def show_info(btn_click, loaded_data, container_state, filetype):
#     # TODO read data from file
#     # TODO read secondary input parameters from input selection
#
#     if file_data:
#         name = file_data.path.name
#         nframes = file_data.nframes
#         vendor = file_data.vendor
#         path = str(file_data.path)
#
#         info_data = {
#                    'Name': name,
#                    'n_frames': nframes,
#                    'vendor': vendor,
#                    'path': path
#                }
#
#         card_list = [
#             html.H4(f'Dataset ', className="card-title"),
#             html.H6(InputFiletypes(int(filetype)).name, className="card-subtitle"),
#         ]
#         card_list += [dbc.Row(f'{data}: {value}', style={'margin-left': 10}) for data, value in
#                       info_data.items()]
#
#         card = dbc.Card(
#             dbc.CardBody(card_list),
#             id='card-1'
#         )
#
#         if container_state:
#             container_state += [card]
#         else:
#             container_state = [card]
#
#     return container_state


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
