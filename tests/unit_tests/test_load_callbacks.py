import dash_bootstrap_components as dbc
import eit_dash.definitions.element_ids as ids

from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash import html
from eit_dash.callbacks.load_callbacks import open_modal, load_file, show_info


def test_show_info_callback():
    output = show_info(1, None, 0)

    mock_data_card = [dbc.Card(dbc.CardBody([
        html.H4("Dataset 1", className="card-title"),
        html.H6("Timpel", className="card-subtitle"),
        dbc.Row("N_signals: 3", style={'margin-left': 10}),
        dbc.Row("duration: 12", style={'margin-left': 10}),
        dbc.Row("n_frames: 234", style={'margin-left': 10}),
        dbc.Row("filename: file.bin", style={'margin-left': 10}),
        dbc.Row("etc: etc", style={'margin-left': 10})
    ]),
        id='card-1')]

    # Assessing the string converted objects, to check that the properties are the same.
    # Assessing for the equivalence of the objects directly will fail
    assert str(output) == str(mock_data_card)

    # rerun the callback with different inputs and verify that the output is different
    output_new_params = show_info(1, None, 2)

    assert str(output_new_params) != str(mock_data_card)


def test_load_file_callback():
    output = load_file(True)
    assert output is False
    assert output is not True


def test_open_modal_callback():

    context_value.set(AttributeDict(**{"triggered_inputs": [
        {"prop_id": f"{ids.SELECT_FILES_BUTTON}.n_clicks"}
    ]}))

    output = open_modal(1, 1)

    expected_output = (True, True)

    # verify that a different input produces a different output
    context_value.set(AttributeDict(**{"triggered_inputs": [
        {"prop_id": f"{ids.ADD_DATA_BUTTON}.n_clicks"}
    ]}))

    output_new_params = open_modal(1, 1)

    assert output == expected_output
    assert output_new_params != expected_output
