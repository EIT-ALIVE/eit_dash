import os
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, html, ALL
from dash.exceptions import PreventUpdate

import eit_dash.definitions.element_ids as ids
from eit_dash.app import data_object
from eit_dash.definitions.option_lists import InputFiletypes, SignalSelections
from eitprocessing.binreader.sequence import Sequence

file_data: Sequence | None = None


def create_info_card(dataset: Sequence, file_type: int) -> dbc.Card:
    """
    Create the card with the information on the loaded dataset
    to be displayed in the Results section

    Args:
        dataset: Sequence object containing the selected dataset
        file_type: index of the selected type of selected
    """

    info_data = {
        'Name': dataset.path.name,
        'n_frames': dataset.nframes,
        'start_time': dataset.time[0],
        'end_time': dataset.time[-1],
        'vendor': dataset.vendor,
        'path': str(dataset.path)
    }

    dataset_n = data_object.get_list_length()

    card_list = [
        html.H4(f'Dataset {dataset_n}', className="card-title"),
        html.H6(InputFiletypes(file_type).name, className="card-subtitle"),
    ]
    card_list += [dbc.Row(f'{data}: {value}', style={'margin-left': 10}) for data, value in
                  info_data.items()]

    card = dbc.Card(
        dbc.CardBody(card_list),
        id='card-1'
    )

    return card


# managing the file selection. Confirm button clicked
@callback(
    Output(ids.CHOOSE_DATA_POPUP, 'is_open'),
    Output(ids.NFILES_PLACEHOLDER, 'children'),
    Output(ids.ALERT_LOAD, 'is_open'),
    Input(ids.SELECT_FILES_BUTTON, 'n_clicks'),
    Input(ids.SELECT_CONFIRM_BUTTON, 'n_clicks'),
    State(ids.STORED_CWD, 'data'),
    State(ids.INPUT_TYPE_SELECTOR, 'value'),
    prevent_initial_call=True
)
# load the information selected from the file (e.g., signals, time span)
def load_selected_data(select_file, confirm_select, file_path,
                       file_type):  # pylint: disable=unused-argument
    open_modal = True
    data = None
    show_alert = False
    read_data_flag = False

    global file_data

    trigger = ctx.triggered_id

    # when the button for selecting the file has been clicked
    if trigger == ids.SELECT_FILES_BUTTON:
        # if a file has been loaded already, the data should not be cancelled,
        # unless a new file is loaded. if `data` is None, the selection is cancelled
        data = file_path if file_data else None

    # if the callback has not been triggered by the select files button,
    # get the information on the selected file and try to read it
    if trigger == ids.SELECT_CONFIRM_BUTTON:
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
    Output(ids.FILE_LENGTH_SLIDER, 'value'),
    Input(ids.NFILES_PLACEHOLDER, 'children'),
    Input(ids.LOAD_CANCEL_BUTTON, 'n_clicks'),
    State(ids.INPUT_TYPE_SELECTOR, 'value'),
    prevent_initial_call=True)
# read the file selected in the file selector
def open_data_selector(data, cancel_load, file_type):
    options = []
    min_slider = 0
    max_slider = 10
    selcted_range = [0, 10]

    global file_data

    trigger = ctx.triggered_id

    # cancelled selection. Reset the data and turn of the data selector
    if trigger == ids.LOAD_CANCEL_BUTTON:
        data = None
        file_data = None

    if not data:
        return True, options, min_slider, max_slider, selcted_range

    path = Path(data)
    file_data = Sequence.from_path(path, vendor=InputFiletypes(int(file_type)).name)
    min_slider = file_data.time[0]
    max_slider = file_data.time[-1]
    selcted_range = [min_slider, max_slider]

    for frameset in file_data.framesets:
        if frameset == 'raw':
            label = 'raw'
            value = 3
        else:
            label = frameset
            value = 5
        options.append({'label': label, 'value': value})

    return False, options, min_slider, max_slider, selcted_range


@callback(
    Output(ids.DATASET_CONTAINER, 'children'),
    Input(ids.LOAD_CONFIRM_BUTTON, 'n_clicks'),
    State(ids.NFILES_PLACEHOLDER, 'children'),
    State(ids.DATASET_CONTAINER, 'children'),
    State(ids.INPUT_TYPE_SELECTOR, 'value'),
    State(ids.FILE_LENGTH_SLIDER, 'value'),
    State(ids.CHECKBOX_SIGNALS, 'value'),
    prevent_initial_call=True,
)
def show_info(btn_click, loaded_data, container_state, filetype, selected_range, selected_signals):
    global file_data

    if file_data and selected_signals is not None:

        cut_data = file_data.select_by_time(selected_range[0], selected_range[1])

        # save the selected data in the singleton
        data_object.add_sequence(cut_data)

        # create the info summary card
        card = create_info_card(cut_data, int(filetype))

        # add the card to the current results
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
