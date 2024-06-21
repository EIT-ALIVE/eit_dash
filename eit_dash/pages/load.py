from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.definitions.option_lists import InputFiletypes

register_page(__name__, path="/")

summary = dbc.Col([html.H2("Summary", style=styles.COLUMN_TITLE)])

results = dbc.Col(
    [
        html.H2("Results", style=styles.COLUMN_TITLE, id=ids.LOAD_RESULTS_TITLE),
        html.Div(id=ids.DATASET_CONTAINER, style=styles.LOAD_RESULTS),
    ],
)

input_type_selector = html.Div(
    [
        dbc.Select(
            id=ids.INPUT_TYPE_SELECTOR,
            options=[{"label": filetype.name, "value": filetype.value} for filetype in InputFiletypes],
            value=str(InputFiletypes.Sentec.value),
        ),
        html.P(),
        dbc.Row(dbc.Button("Select files", id=ids.SELECT_FILES_BUTTON)),
        dbc.Row(dbc.Label(id=ids.METADATA)),
    ],
)

max_slider_length = 100
add_data_selector = dcc.Loading(
    html.Div(
        id=ids.DATA_SELECTOR_OPTIONS,
        hidden=True,
        children=[
            html.P(),
            html.H5("Signal selections", style=styles.SECTION_TITLE),
            dbc.Row(
                dcc.Checklist(
                    id=ids.CHECKBOX_SIGNALS,
                    inputStyle=styles.CHECKBOX_INPUT,
                ),
            ),
            html.H5("Pre selection", style=styles.SECTION_TITLE),
            dcc.Graph(id=ids.FILE_LENGTH_SLIDER),
            html.Div(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button(
                                "Cancel",
                                id=ids.LOAD_CANCEL_BUTTON,
                                className="ms-auto",
                                color="danger",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Confirm",
                                id=ids.LOAD_CONFIRM_BUTTON,
                                className="ms-auto",
                                color="success",
                                n_clicks=0,
                            ),
                        ],
                    ),
                ],
                style=styles.BUTTONS_ROW,
            ),
        ],
    ),
)

actions = dbc.Col(
    [
        html.H2("Load datasets", style=styles.COLUMN_TITLE),
        html.P(),
        input_type_selector,
        html.P(),
        add_data_selector,
    ],
)

placeholder_nfiles = html.Div(
    hidden=True,
    id=ids.NFILES_PLACEHOLDER,
    children=0,
)

file_browser = html.Div(
    [
        dbc.Row(
            [
                dcc.Store(id=ids.STORED_CWD, data=str(Path.cwd())),
                html.H5(
                    html.B(html.A("⬆️ Parent directory", href="#", id=ids.PARENT_DIR)),
                ),
                html.H3([html.Code(str(Path.cwd()), id=ids.CWD)]),
                html.Br(),
                html.Br(),
                html.Div(id=ids.CWD_FILES, style=styles.FILE_BROWSER),
            ],
        ),
    ],
)

alert_load = dbc.Alert(
    "The selected file cannot be loaded",
    id=ids.ALERT_LOAD,
    color="primary",
    dismissable=True,
    is_open=False,
    duration=3000,
)

modal_dialog = html.Div(
    [
        dcc.Loading(
            [
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle("Select a file"),
                            close_button=True,
                        ),
                        dbc.ModalBody([alert_load, file_browser]),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Confirm",
                                id=ids.SELECT_CONFIRM_BUTTON,
                                className="ms-auto",
                                n_clicks=0,
                            ),
                        ),
                    ],
                    id=ids.CHOOSE_DATA_POPUP,
                    centered=True,
                    is_open=False,
                    backdrop=False,
                    scrollable=True,
                ),
            ],
        ),
    ],
)

# This is a placeholder for triggering repopulating of data when page is reloaded
populate_loaded_data = html.Div(id=ids.POPULATE_DATA)

layout = dbc.Row(
    [
        html.H1("LOAD DATA", style=styles.COLUMN_TITLE),
        summary,
        actions,
        results,
        placeholder_nfiles,
        modal_dialog,
        populate_loaded_data,
        # TODO: the following is duplicated in multiple pages. To be refactored
        html.Div(
            [
                dbc.NavLink(
                    dbc.Button(
                        className="fa fa-arrow-circle-right",
                        id=ids.NEXT_PAGE_BUTTON_LOAD,
                        style=styles.NEXT_PAGE_BUTTON,
                    ),
                    href="/preprocessing",
                    id=ids.NEXT_PAGE_LINK_LOAD,
                ),
                html.Div(
                    "NEXT PAGE",
                    style=styles.NEXT_PAGE_SECTION,
                ),
            ],
        ),
    ],
)
