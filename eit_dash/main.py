import dash_bootstrap_components as dbc
from dash import html, page_container

from eit_dash.app import app
from eit_dash.callbacks import (
    load_callbacks,
    preprocessing_callbacks,
    analyze_callbacks,
)  # noqa: F401

app.layout = html.Div(
    [
        html.H1(
            id="test-id", children="EIT-ALIVE dashboard", style={"textAlign": "center"}
        ),
        dbc.Row(
            [
                dbc.Col(dbc.NavLink("Load", href="/load")),
                dbc.Col(dbc.NavLink("Pre-processing", href="/preprocessing")),
                dbc.Col(dbc.NavLink("Analyze", href="/analyze")),
                dbc.Col(dbc.NavLink("Summarize", href="/dummy")),
            ],
            style={"textAlign": "center"},
        ),
        page_container,
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
