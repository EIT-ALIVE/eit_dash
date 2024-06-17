from unittest.mock import patch

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pytest
from dash import html
from dash._callback_context import context_value
from dash._utils import AttributeDict
from eitprocessing.datahandling.eitdata import Vendor
from eitprocessing.datahandling.sequence import Sequence

import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
from eit_dash.callbacks.load_callbacks import load_selected_data, show_info
from eit_dash.definitions.option_lists import InputFiletypes
from tests.conftest import data_path

EXPECTED_CONTINUOUS_DATA = [
    {"label": "airway pressure", "value": 0},
    {"label": "flow", "value": 1},
    {"label": "volume", "value": 2},
    {"label": "CO2", "value": 3},
]

FIRST_SAMPLE = 100
LAST_SAMPLE = 1000

CUT_FILE_LENGTH = LAST_SAMPLE - FIRST_SAMPLE


@pytest.fixture(scope="session")
def expected_cut_info_data(file_data: Sequence):
    return {
        "Name": "Draeger_Test3.bin",
        "n_frames": CUT_FILE_LENGTH,
        "start_time": file_data.time[FIRST_SAMPLE],
        "end_time": file_data.time[LAST_SAMPLE - 1],
        "vendor": Vendor.DRAEGER,
        "continuous signals": [
            "airway pressure",
            "flow",
            "volume",
            "CO2",
            "global_impedance_(raw)",
        ],
        "path": str(data_path),
    }


def test_load_selected_data_callback(file_data: Sequence, expected_cut_info_data: dict):
    cancel_load = 0
    sig = []
    file_type = InputFiletypes.Draeger.value
    fig = go.Figure()

    # cancel data button input
    context_value.set(
        AttributeDict(
            triggered_inputs=[{"prop_id": f"{ids.LOAD_CANCEL_BUTTON}.n_clicks"}],
        ),
    )
    output = load_selected_data(data_path, cancel_load, sig, file_type, fig)

    assert output == (True, [], [], go.Figure())

    # file selected input
    context_value.set(
        AttributeDict(
            triggered_inputs=[{"prop_id": f"{ids.NFILES_PLACEHOLDER}.n_clicks"}],
        ),
    )

    # run the callback
    output = load_selected_data(data_path, cancel_load, sig, file_type, fig)

    # the output of this function is a figure that uses the loaded data
    # we can check the data in the figure to verify the correct data loading
    fig_data = output[3].data[0]["x"]

    assert len(fig_data) == len(file_data.time)

    # we can check that also the other continuous data has been detected and displayed as options

    assert output[1] == EXPECTED_CONTINUOUS_DATA


def test_show_info_callback(file_data: Sequence, expected_cut_info_data: dict):
    # run the callback
    with patch("eit_dash.callbacks.load_callbacks.file_data", new=file_data):
        output = show_info(
            btn_click=1,
            loaded_data=data_path,
            container_state=None,
            filetype="1",
            slidebar_stat={
                "xaxis.range": [
                    file_data.time[FIRST_SAMPLE],
                    file_data.time[LAST_SAMPLE],
                ],
            },
            selected_signals=[0, 1, 2, 3],
            signals_options=EXPECTED_CONTINUOUS_DATA,
        )

    # the output is a card containing the information about the selected signal.
    # We have to check that the information is the expected one to verify the correct slicing

    card_list = [
        html.H4("Dataset 0", className="card-title"),
        html.H6(Vendor.DRAEGER, className="card-subtitle"),
    ]
    card_list += [dbc.Row(f"{data}: {value}", style=styles.INFO_CARD) for data, value in expected_cut_info_data.items()]
    mock_data_card = [dbc.Card(dbc.CardBody(card_list), id="card-1")]

    # Assessing the string converted objects, to check that the properties are the same.
    # Assessing for the equivalence of the objects directly will fail
    assert str(output) == str(mock_data_card)
