from unittest.mock import patch

import pytest
from dash._callback_context import context_value
from dash._utils import AttributeDict
from eitprocessing.datahandling.sequence import Sequence

import eit_dash.definitions.element_ids as ids
from eit_dash.callbacks.preprocessing_callbacks import (
    apply_filter,
    open_periods_modal,
    open_synch_modal,
)
from eit_dash.definitions.option_lists import FilterTypes
from eit_dash.utils.data_singleton import LoadedData


@pytest.fixture
def mock_data_object(file_data: Sequence):
    """Mocked object to save and retrieve the data."""
    data_object = LoadedData()
    data_object.add_sequence(file_data)
    data_object.add_stable_period(file_data, 0, 0)

    return data_object


@pytest.fixture
def mock_tmp_results():
    """Mocked temporary results object."""
    return LoadedData()


def test_apply_filter_callback(
    mock_data_object: LoadedData,
    mock_tmp_results: LoadedData,
):
    """Test the filtering of stable periods."""
    low_cut = 1
    high_cut = 9
    filter_order = 1

    with patch(
        "eit_dash.callbacks.preprocessing_callbacks.data_object",
        new=mock_data_object,
    ), patch(
        "eit_dash.callbacks.preprocessing_callbacks.tmp_results",
        new=mock_tmp_results,
    ):
        # test error in filter
        with pytest.raises(TypeError):
            _ = apply_filter(
                0,
                co_low=low_cut,
                co_high=high_cut,
                order=filter_order,
                filter_selected=FilterTypes.lowpass.value,
                results=[],
            )

        # test valid filter
        _ = apply_filter(
            0,
            co_low=low_cut,
            co_high=high_cut,
            order=filter_order,
            filter_selected=FilterTypes.bandpass.value,
            results=[],
        )

        # the filtered results are saved in a temporary object before saving them
        # through a different call. We need to verify if the presence of the data
        # in the mocked temporary object.
        assert "global_impedance_(filtered)" in mock_tmp_results.get_stable_period(0).get_data().continuous_data


def test_open_synch_modal_callback():
    """Test opening of synchronization modal."""
    context_value.set(
        AttributeDict(
            triggered_inputs=[{"prop_id": f"{ids.OPEN_SYNCH_BUTTON}.n_clicks"}],
        ),
    )

    output = open_synch_modal(1, 1)

    expected_output = True

    # verify that a different input produces a different output
    context_value.set(
        AttributeDict(
            triggered_inputs=[
                {"prop_id": f"{ids.SYNCHRONIZATION_CONFIRM_BUTTON}.n_clicks"},
            ],
        ),
    )

    output_new_params = open_synch_modal(1, 1)

    assert output == expected_output
    assert output_new_params != expected_output


def test_open_periods_modal_callback():
    """Test opening of the modal for selecting the stable periods."""
    context_value.set(
        AttributeDict(
            triggered_inputs=[
                {"prop_id": f"{ids.OPEN_SELECT_PERIODS_BUTTON}.n_clicks"},
            ],
        ),
    )

    output = open_periods_modal(1, 1)

    expected_output = True

    # verify that a different input produces a different output
    context_value.set(
        AttributeDict(
            triggered_inputs=[{"prop_id": f"{ids.PERIODS_CONFIRM_BUTTON}.n_clicks"}],
        ),
    )

    output_new_params = open_periods_modal(1, 1)

    assert output == expected_output
    assert output_new_params != expected_output
