import dash_bootstrap_components as dbc
from dash import html, page_container

from eit_dash.app import app
from eit_dash.callbacks import (  # noqa: F401
    analyze_callbacks,
    load_callbacks,
    preprocessing_callbacks,
)
from eit_dash.definitions import layout_styles as styles
from eit_dash.definitions import element_ids as ids

app.layout = html.Div(
    [
        html.H1(
            id="test-id",
            children="EIT-ALIVE dashboard",
            style={"textAlign": "center"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H2(dbc.NavLink("LOAD", href="/", style=styles.PAGES_LINK)),
                ),
                dbc.Col(
                    html.H2(
                        dbc.NavLink(
                            "PRE-PROCESSING",
                            href="/preprocessing",
                            style=styles.PAGES_LINK,
                        ),
                    ),
                ),
                dbc.Col(
                    html.H2(
                        dbc.NavLink(
                            "ANALYZE",
                            href="/analyze",
                            style=styles.PAGES_LINK,
                        ),
                    ),
                ),
            ],
            style={"textAlign": "center"},
        ),
        page_container,
        html.Div(
            [
                dbc.NavLink(
                    dbc.Button(
                        className="fa fa-arrow-circle-right",
                        id=ids.NEXT_PAGE_BUTTON,
                        style=styles.NEXT_PAGE_BUTTON,
                    ),
                    href="/preprocessing",
                    id=ids.NEXT_PAGE_LINK,
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=False)
