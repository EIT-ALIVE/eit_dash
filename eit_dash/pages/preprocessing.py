import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.definitions.option_lists import (
    FilterTypes,
    PeriodsSelectMethods,
    SynchMethods,
)

register_page(__name__, path="/preprocessing")

resampling_card = html.Div(
    dbc.Card(
        [
            dbc.CardHeader("Resampling"),
            dbc.CardBody(id=ids.RESAMPLING_CARD_BODY),
            dbc.CardFooter(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Input(
                                        type="number",
                                        placeholder="Resampling frequency",
                                        value=100,
                                        id=ids.RESAMPLING_FREQUENCY_INPUT,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                [dbc.Button("Apply", id=ids.CONFIRM_RESAMPLING_BUTTON)],
                            ),
                        ],
                    ),
                ],
                style=styles.CARD_FOOTER,
            ),
        ],
    ),
    id=ids.RESAMPLING_CARD,
)

summary = dbc.Col(
    [
        html.H2("Summary", style=styles.COLUMN_TITLE),
    ],
    id=ids.SUMMARY_COLUMN,
)

actions = dbc.Col(
    [
        html.H2(
            "Pre-processing steps",
            id=ids.PREPROCESING_TITLE,
            style=styles.COLUMN_TITLE,
        ),
        resampling_card,
        html.P(),
        html.Div(
            dbc.Row(
                dbc.Button("Synchronize data", id=ids.OPEN_SYNCH_BUTTON, disabled=True),
            ),
            hidden=True,
        ),
        html.P(),
        dbc.Row(
            dbc.Button(
                "Select periods",
                id=ids.OPEN_SELECT_PERIODS_BUTTON,
                disabled=False,
            ),
        ),
        html.P(),
        dbc.Row(
            dbc.Button("Filter data", id=ids.OPEN_FILTER_DATA_BUTTON, disabled=True),
        ),
    ],
)

results = dbc.Col(
    [
        html.H2("Results", style=styles.COLUMN_TITLE),
        html.Div(id=ids.PREPROCESING_RESULTS_CONTAINER, style=styles.LOAD_RESULTS),
    ],
)

# popup for data synchronization
modal_synchronization = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Data synchronization"),
                    close_button=True,
                ),
                dbc.ModalBody(
                    [
                        dbc.Select(
                            id=ids.SYNC_METHOD_SELECTOR,
                            options=[{"label": method.name, "value": method.value} for method in SynchMethods],
                            value=str(SynchMethods.manual.value),
                        ),
                        html.P(),
                        dbc.Row(dbc.Checklist(id=ids.DATASET_SELECTION_CHECKBOX)),
                        html.P(),
                        dbc.Row(id=ids.SYNC_DATA_PREVIEW_CONTAINER),
                        dbc.Button("SYNCH PREVIEW", id=ids.CONFIRM_SYNCH_BUTTON),
                    ],
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id=ids.SYNCHRONIZATION_CONFIRM_BUTTON,
                        className="ms-auto",
                        n_clicks=0,
                    ),
                ),
            ],
            id=ids.SYNCHRONIZATION_POPUP,
            centered=True,
            is_open=False,
            backdrop=False,
            scrollable=True,
            size="xl",
        ),
    ],
)

modal_selection_body = html.Div(
    [
        dbc.Row(id=ids.PERIODS_SELECTION_SELECT_DATASET),
        html.P(),
        dbc.Row(id=ids.PREPROCESING_SIGNALS_CHECKBOX_ROW),
        html.P(),
        dcc.Loading(
            html.Div(
                [
                    dbc.Row(
                        [
                            dcc.Graph(
                                id=ids.PREPROCESING_PERIODS_GRAPH,
                                style=styles.EMPTY_ELEMENT,
                            ),
                        ],
                    ),
                    html.P(),
                    dbc.Row(
                        [
                            dbc.Button(
                                "Add selection",
                                id=ids.PREPROCESING_SELECT_BTN,
                            ),
                        ],
                        style=styles.BUTTONS_ROW,
                    ),
                ],
                id=ids.PERIODS_SELECTION_DIV,
                hidden=True,
            ),
        ),
    ],
    id=ids.PERIODS_SELECTION_BODY,
)

modal_selection = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Periods selection"), close_button=True),
                dbc.ModalBody(
                    [
                        html.H6("Periods selection method"),
                        dbc.Select(
                            id=ids.PERIODS_METHOD_SELECTOR,
                            options=[{"label": method.name, "value": method.value} for method in PeriodsSelectMethods],
                            value=str(PeriodsSelectMethods.Manual.value),
                        ),
                        modal_selection_body,
                    ],
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Confirm",
                        id=ids.PERIODS_CONFIRM_BUTTON,
                        className="ms-auto",
                        n_clicks=0,
                    ),
                ),
            ],
            id=ids.PERIODS_SELECTION_POPUP,
            centered=True,
            is_open=False,
            backdrop=False,
            scrollable=True,
            size="xl",
        ),
    ],
)

alert_filter = dbc.Alert(
    [],
    id=ids.ALERT_FILTER,
    color="danger",
    dismissable=True,
    is_open=False,
    duration=3000,
)

alert_saved_results = dbc.Alert(
    [],
    id=ids.ALERT_SAVED_RESULTS,
    color="success",
    dismissable=True,
    is_open=False,
    duration=3000,
)

filter_params = html.Div(
    [
        dbc.Row(alert_filter),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Filter Order"),
                        dbc.Input(id=ids.FILTER_ORDER, type="number", min=0),
                    ],
                ),
                dbc.Col(
                    [
                        html.P("Cut off frequency low"),
                        dbc.Input(id=ids.FILTER_CUTOFF_LOW, type="number", min=0),
                    ],
                ),
                dbc.Col(
                    [
                        html.P("Cut off frequency high"),
                        dbc.Input(id=ids.FILTER_CUTOFF_HIGH, type="number", min=0),
                    ],
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Apply",
                            id=ids.FILTER_APPLY,
                            disabled=True,
                        ),
                    ],
                ),
            ],
            style=styles.BUTTONS_ROW,
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        html.H6("Select a period to view the results"),
                        dbc.Select(id=ids.FILTERING_SELECT_PERIOD_VIEW),
                        dcc.Graph(
                            id=ids.FILTERING_RESULTS_GRAPH,
                            style=styles.EMPTY_ELEMENT,
                        ),
                    ],
                    id=ids.FILTERING_RESULTS_DIV,
                    hidden=True,
                ),
            ],
            style=styles.BUTTONS_ROW,
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.Button("Confirm", id=ids.FILTERING_CONFIRM_BUTTON),
                    ],
                    id=ids.FILTERING_CONFIRM_DIV,
                    hidden=True,
                ),
            ],
            style=styles.BUTTONS_ROW,
        ),
    ],
    id=ids.FILTER_PARAMS,
    hidden=True,
)

modal_filtering = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Filter"), close_button=True),
                dbc.ModalBody(
                    [
                        alert_saved_results,
                        html.H6("Select a filter"),
                        dbc.Select(
                            id=ids.FILTER_SELECTOR,
                            options=[{"label": filt.name, "value": filt.value} for filt in FilterTypes],
                        ),
                        html.P(),
                        filter_params,
                    ],
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id=ids.FILTERING_CLOSE_BUTTON,
                        className="ms-auto",
                        n_clicks=0,
                    ),
                ),
                html.Div(id=ids.UPDATE_FILTER_RESULTS, hidden=True),
            ],
            id=ids.FILTERING_SELECTION_POPUP,
            centered=True,
            is_open=False,
            backdrop=False,
            scrollable=True,
            size="xl",
        ),
    ],
)

layout = dbc.Row(
    [
        html.H1("PRE-PROCESSING", style=styles.COLUMN_TITLE),
        summary,
        actions,
        results,
        modal_synchronization,
        modal_selection,
        modal_filtering,
        html.Div(
            [
                dbc.NavLink(
                    html.Div(
                        [
                            dbc.Button(
                                className="fa fa-arrow-circle-right",
                                id=ids.NEXT_PAGE_BUTTON_PREP,
                                style=styles.NEXT_PAGE_BUTTON,
                            ),
                        ],
                    ),
                    href="/analyze",
                    id=ids.NEXT_PAGE_LINK_PREP,
                ),
                html.Div(
                    "NEXT PAGE",
                    style=styles.NEXT_PAGE_SECTION,
                ),
            ],
        ),
        html.Div(
            [
                dbc.NavLink(
                    dbc.Button(
                        className="fa fa-arrow-circle-left",
                        id=ids.PREV_PAGE_BUTTON_PREP,
                        style=styles.PREV_PAGE_BUTTON,
                        disabled=False,
                    ),
                    href="/",
                    id=ids.PREV_PAGE_LINK_PREP,
                ),
                html.Div(
                    "PREVIOUS PAGE",
                    style=styles.PREV_PAGE_SECTION,
                ),
            ],
        ),
    ],
)
