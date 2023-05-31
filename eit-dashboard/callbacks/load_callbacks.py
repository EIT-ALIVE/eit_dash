from dash import callback, Output, Input, ctx
import definitions.element_ids as ids


@callback(
    [Output(ids.CHOOSE_DATA_POPUP, 'is_open'), Output(ids.NFILES_PLACEHOLDER, 'children')],
    [Input(ids.ADD_DATA_BUTTON, 'n_clicks'), Input(ids.SELECT_FILES_BUTTON, 'n_clicks')],
    prevent_initial_call=True
)
def open_modal(add_data_click, select_files_click):
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

