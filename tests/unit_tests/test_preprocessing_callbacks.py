import dash_bootstrap_components as dbc
import eit_dash.definitions.element_ids as ids
import eit_dash.definitions.layout_styles as styles
import numpy as np
import plotly.graph_objs as go
import pytest

from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash import dcc, html
from eit_dash.callbacks.preprocessing_callbacks import (
    apply_resampling,
    load_datasets,
    mark_selected_point,
    open_periods_modal,
    open_synch_modal,
    show_data,
)
from unittest.mock import MagicMock


mock_series = np.sin(np.linspace(-2 * np.pi, 2 * np.pi, 201))
mock_fig = go.Figure(data=[go.Scatter(y=mock_series)])


def test_load_datasets_callback():
    mock_get_loaded_data = MagicMock()
    mock_get_loaded_data.return_value = [{"Number": 1, "sampling_frequency": 10}]

    with pytest.MonkeyPatch.context() as m:
        m.setattr("eit_dash.callbacks.preprocessing_callbacks.get_loaded_data", mock_get_loaded_data)

        mock_data_row = [
            dbc.Row([dbc.Col([html.H6("Sequence")]), dbc.Col([html.H6("Sampling frequency")])]),
            html.P(),
            dbc.Row([dbc.Col("Sequence 1"), dbc.Col("10 Hz"), html.P()]),
        ]

        mock_options = [{"label": "Sequence 1", "value": "0"}]

        mock_return = (mock_data_row, mock_options)

        output = load_datasets(["Test"])

        # Assessing for the equivalence of the objects directly will fail
        assert str(output) == str(mock_return)


def test_apply_resampling_callback():
    test_frequency = 10

    output = apply_resampling(0, [], test_frequency)

    added_row = [dbc.Row([html.Div(f"Resampled dataset at {test_frequency}Hz", style=styles.SUMMARY_ELEMENT)])]

    assert output[0] is False
    assert output[1] is False
    assert output[2] is False
    assert str(output[3]) == str(added_row)


def test_open_synch_modal_callback():
    context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": f"{ids.OPEN_SYNCH_BUTTON}.n_clicks"}]}))

    output = open_synch_modal(1, 1)

    expected_output = True

    # verify that a different input produces a different output
    context_value.set(
        AttributeDict(**{"triggered_inputs": [{"prop_id": f"{ids.SYNCHRONIZATION_CONFIRM_BUTTON}.n_clicks"}]})
    )

    output_new_params = open_synch_modal(1, 1)

    assert output == expected_output
    assert output_new_params != expected_output


def test_open_periods_modal_callback():
    context_value.set(
        AttributeDict(**{"triggered_inputs": [{"prop_id": f"{ids.OPEN_SELECT_PERIODS_BUTTON}.n_clicks"}]})
    )

    output = open_periods_modal(1, 1)

    expected_output = True

    # verify that a different input produces a different output
    context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": f"{ids.PERIODS_CONFIRM_BUTTON}.n_clicks"}]}))

    output_new_params = open_periods_modal(1, 1)

    assert output == expected_output
    assert output_new_params != expected_output


def test_show_data_callback():
    dataset = 1

    expected_output = [dcc.Graph(figure=mock_fig, id={"type": ids.SYNC_DATA_PREVIEW_GRAPH, "index": dataset})]

    output = show_data([dataset], [])

    assert str(expected_output) == str(output)


def test_mark_selected_point_callback():
    x_selected = 10
    mock_selected_point = {"points": [{"x": x_selected}]}

    output = mark_selected_point(mock_selected_point, mock_fig)

    mock_fig_vline = mock_fig.add_vline(x=x_selected, line_width=3, line_dash="dash", line_color="green")

    assert str(mock_fig_vline) == str(output)
