from dash import register_page, html, dcc
import dash_bootstrap_components as dbc
import definitions.element_ids as ids
from definitions.option_lists import InputFiletypes, SignalSelections
import definitions.layout_styles as styles
# from app import app

register_page(__name__, path='/load')

summary = dbc.Col('summary')


actions = dbc.Col([
    html.H2('Load datasets', style=styles.COLUMN_TITLE),
    dbc.Row(dbc.Button('Add dataset', id=ids.ADD_DATA_BUTTON)),
])


results = dbc.Col([
    html.H2('Results', style=styles.COLUMN_TITLE)
])


input_type_selector = html.Div([
    dbc.Select(
        id =ids.INPUT_TYPE_SELECTOR,
        options = [{'label': filetype.name, "value": filetype.value} for filetype in InputFiletypes],
        value = str(InputFiletypes.Draeger.value),
    ),
    html.P(),
    dbc.Row(dbc.Button('Select files', id=ids.SELECT_FILES_BUTTON)),
    dbc.Row(dbc.Label(id=ids.METADATA)),    
])

max_slider_length = 100
add_data_selector = html.Div(
    id=ids.DATA_SELECTOR_OPTIONS,
    hidden = True,
    children = [
        html.P(),
        html.H5('Signal selections'),
        dbc.Row(dbc.Checklist(id=ids.CHECKBOX, 
            options = [{'label': signal.name, "value": signal.value} for signal in SignalSelections],
            # value = [signal.value for signal in SignalSelections],
            )),
        html.P(),
        html.H5('Pre selection'),
        dcc.RangeSlider(0,max_slider_length,1,
            value = [10,50],
            id = ids.FILE_LENGTH_SLIDER,
            marks = {n: str(n) for n in range(0, max_slider_length, max_slider_length//10)},
            tooltip = {"placement": "bottom", "always_visible": True},
            allowCross = False,
        ),
    ],
)


modal_dialog = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Close"), close_button=True),
                dbc.ModalBody([input_type_selector, add_data_selector]),
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


placeholder_nfiles = html.Div(
    hidden=True,
    id = ids.NFILES_PLACEHOLDER,
    children=0,
)


layout = dbc.Row([
    html.H1('this is the loading page'),
    summary,
    actions,
    results,
    modal_dialog,
    placeholder_nfiles
])


