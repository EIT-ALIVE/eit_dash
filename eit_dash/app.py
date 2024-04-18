import logging

import dash_bootstrap_components as dbc
from dash import Dash

from .utils import data_singleton

# this avoids the printing of warning errors in the console
logging.getLogger("werkzeug").setLevel(logging.ERROR)

# this is a shared object to use the data through different pages
# it is initialized here, and imported by the callbacks pages when needed
data_object = data_singleton.get_singleton()
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.13.0/css/all.css"
external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME]
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
