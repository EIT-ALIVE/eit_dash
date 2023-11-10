import os

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.definitions.option_lists import InputFiletypes

register_page(__name__, path='/load')

summary = dbc.Col([
    html.H2('Summary', style=styles.COLUMN_TITLE)
])

results = dbc.Col([
    html.H2('Results', style=styles.COLUMN_TITLE),
    html.Div(id=ids.DATASET_CONTAINER, style=styles.LOAD_RESULTS)
])

input_type_selector = html.Div([
    dbc.Select(
        id=ids.INPUT_TYPE_SELECTOR,
        options=[{'label': filetype.name, "value": filetype.value} for filetype in InputFiletypes],
        value=str(InputFiletypes.Sentec.value),
    ),
    html.P(),
    dbc.Row(dbc.Button('Select files', id=ids.SELECT_FILES_BUTTON)),
    dbc.Row(dbc.Label(id=ids.METADATA)),
])

max_slider_length = 100
add_data_selector = dcc.Loading(
    html.Div(
        id=ids.DATA_SELECTOR_OPTIONS,
        hidden=True,
        children=[
            html.P(),
            html.H5('Signal selections'),
            dbc.Row(dcc.Checklist(id=ids.CHECKBOX_SIGNALS)),
            html.H5('Pre selection'),
            dcc.Graph(id=ids.FILE_LENGTH_SLIDER),
            html.Div(),
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        "Confirm",
                        id=ids.LOAD_CONFIRM_BUTTON,
                        className="ms-auto",
                        color='success',
                        n_clicks=0,
                    )
                ]),

                dbc.Col([
                    dbc.Button(
                        "Cancel",
                        id=ids.LOAD_CANCEL_BUTTON,
                        className="ms-auto",
                        color='danger',
                        n_clicks=0,
                    )
                ])
            ],
                style={'textAlign': 'center'}),
        ]
    )
)

actions = dbc.Col([
    html.H2('Load datasets', style=styles.COLUMN_TITLE),
    html.P(),
    input_type_selector,
    add_data_selector
])

placeholder_nfiles = html.Div(
    hidden=True,
    id=ids.NFILES_PLACEHOLDER,
    children=0,
)

file_browser = html.Div([
    dbc.Row([

        dcc.Store(id=ids.STORED_CWD, data=os.getcwd()),
        html.H5(html.B(html.A("⬆️ Parent directory", href='#',
                              id=ids.PARENT_DIR))),
        html.H3([html.Code(os.getcwd(), id=ids.CWD)]),
        html.Br(), html.Br(),
        html.Div(id=ids.CWD_FILES,
                 style=styles.FILE_BROWSER),
    ])
])

alert_load = dbc.Alert(
    "The selected file cannot be loaded",
    id=ids.ALERT_LOAD,
    color="primary",
    dismissable=True,
    is_open=False,
    duration=3000
)

modal_dialog = html.Div(
    [
        dcc.Loading([dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Select a file"), close_button=True),
                dbc.ModalBody([alert_load, file_browser]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Confirm",
                        id=ids.SELECT_CONFIRM_BUTTON,
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id=ids.CHOOSE_DATA_POPUP,
            centered=True,
            is_open=False,
            backdrop=False,
            scrollable=True
        )])

    ]
)

layout = dbc.Row([
    html.H1('LOAD DATA', style=styles.COLUMN_TITLE),
    summary,
    actions,
    results,
    placeholder_nfiles,
    modal_dialog
])
