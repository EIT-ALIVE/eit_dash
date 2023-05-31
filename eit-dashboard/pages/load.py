from dash import register_page, html
import dash_bootstrap_components as dbc
import element_ids as ids
# from app import app

register_page(__name__, path='/load')

summary = dbc.Col('summary')


actions = dbc.Col([
    dbc.Row(dbc.Button('Add dataset', id=ids.ADD_DATA_BUTTON)),
    dbc.Row(dbc.Label('label', id='test-label'))
])


results = dbc.Col('results')


modal_dialog = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Close"), close_button=True),
                dbc.ModalBody(),
                dbc.ModalFooter(
                    dbc.Button(
                        "Confirm",
                        id='CONFIRM_CENTERED',
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
        ),
    ]
)


layout = dbc.Row([
    html.H1('this is the loading page'),
    summary,
    actions,
    results,
    modal_dialog,
])


