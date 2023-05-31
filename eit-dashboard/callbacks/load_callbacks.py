from dash import callback, Output, Input
import definitions.element_ids as ids


@callback(
    [Output(ids.CHOOSE_DATA_POPUP, 'is_open'), Output(ids.NFILES_PLACEHOLDER, 'children')],
    [Input(ids.ADD_DATA_BUTTON, 'n_clicks'), Input(ids.SELECT_FILES_BUTTON, 'n_clicks')],
    prevent_initial_call=True
)
def open_modal(add_data_click, select_files_click):
    n_files = 0
    if select_files_click == None:
        select_files_click = 0

    n_files = n_files + select_files_click

    return True, select_files_click


@callback(
    Output(ids.DATA_SELECTOR_OPTIONS, 'hidden'),
    Input(ids.NFILES_PLACEHOLDER, 'children'),
    prevent_initial_call=True,
)
def load_file(n_files):
    # TODO: check number of loaded files, if 0 then hide DATA_SELECTOR_OPTIONS
    print(n_files)
    if n_files > 0:
        return False

