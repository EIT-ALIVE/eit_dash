import dash_bootstrap_components as dbc
from dash import html, register_page

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles

register_page(__name__, path='/preprocessing')

resampling_card = dbc.Card([
    dbc.CardHeader('Resampling'),
    dbc.CardBody(id=ids.RESAMPLING_CARD),
    dbc.CardFooter([
        dbc.Button('Apply', id=ids.CONFIRM_RESAMPLING_BUTTON)
    ],
        style=styles.CARD_FOOTER)
])

summary = dbc.Col([
    html.H2('Summary', style=styles.COLUMN_TITLE),
],
    id=ids.SUMMARY_COLUMN)

actions = dbc.Col([
    html.H2('Pre-processing steps', id=ids.PREPROCESING_TITLE, style=styles.COLUMN_TITLE),
    resampling_card,
    html.P(),
    dbc.Row(dbc.Button('Synchronize data', id=ids.OPEN_SYNCH_BUTTON, disabled=True)),
    html.P(),
    dbc.Row(dbc.Button('Select data range(s)', id=ids.OPEN_SELECT_RANGE_BUTTON, disabled=True)),
    html.P(),
    dbc.Row(dbc.Button('Filter data', id=ids.OPEN_FILTER_DATA_BUTTON, disabled=True)),
])

results = dbc.Col([
    html.H2('Results', style=styles.COLUMN_TITLE)
],
    id=ids.PREPROCESING_RESULTS_CONTAINER)


modal_synchronization = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Close"), close_button=True),
                dbc.ModalBody(),
                dbc.ModalFooter(
                    dbc.Button(
                        "Confirm",
                        id=ids.SYNCHRONIZATION_CONFIRM_BUTTON,
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id=ids.SYNCHRONIZATION_POPUP,
            centered=True,
            is_open=False,
            backdrop=False,
            scrollable=True
        ),
    ]
)


layout = dbc.Row([
    html.H1('PRE-PROCESSING', style=styles.COLUMN_TITLE),
    summary,
    actions,
    results,
    modal_synchronization
])
