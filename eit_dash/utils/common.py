from eit_dash.definitions.option_lists import SignalSelections
from eitprocessing.sequence import Sequence
from typing import List, Dict

import plotly.graph_objects as go


def create_slider_figure(
    dataset: Sequence,
    eit_variants: List[str] = ["raw"],
    continuous_data: List[str] = [],
) -> go.Figure:
    """
    Create the figure for the selection of range.

    Args:
        dataset: Sequence object containing the selected dataset
        eit_variants: list of the eit variants to be plotted
        continuous_data: list of the continuous data signals to be plotted
    """
    traces = []

    for eit_variant in eit_variants:
        # TODO: This is a patch! Needs to be changed
        if eit_variant == "raw":
            try:
                impedance = dataset.eit_data.variants[eit_variant].global_impedance
            except KeyError:
                impedance = dataset.eit_data.variants[None].global_impedance
        traces.append(
            {
                "x": dataset.eit_data.time,
                "y": impedance,
                "type": "scatter",
                "mode": "lines",
                "name": "a_level",
            }
        )

    for cont_signal in continuous_data:
        traces.append(
            {
                "x": dataset.continuous_data[cont_signal].time,
                "y": dataset.continuous_data[cont_signal].variants["raw"].values,
                "type": "scatter",
                "mode": "lines",
                "name": "a_level",
            }
        )

    figure = go.Figure(
        data=traces,
        layout=go.Layout(
            xaxis={"rangeslider": {"visible": True}},
            margin={"t": 0, "l": 0, "b": 0, "r": 0},
        ),
    )
    for event in dataset.eit_data.events:
        annotation = dict(text=f"{event.text}", textangle=-90)
        figure.add_vline(
            x=event.time,
            line_width=3,
            line_dash="dash",
            line_color="green",
            annotation=annotation,
        )

    return figure


def get_signal_options(
    dataset: Sequence, show_eit: bool = False
) -> List[Dict[str, int | str]]:
    """
    Get the options for signal selection to be shown in the signal selection section.

    Args:
        dataset: Sequence object containing the selected dataset
        show_eit: include eit data in the option if True. Default false
    Returns:
        A list of label - value options for populating the options list
    """
    options = []
    if show_eit:
        # iterate over eit data
        for variant in dataset.eit_data.variants:
            # TODO: the None check is just a temporary fix.
            #  The select_by_index should be adjusted instead.

            if variant == "raw" or variant is None:
                label = SignalSelections.raw.name
                value = SignalSelections.raw.value
            else:
                label = variant
                value = max(len(SignalSelections), len(options) + 1)
            options.append({"label": label, "value": value})

    if dataset.continuous_data:
        for cont in dataset.continuous_data:
            # if cont == "airway pressure":
            #     label = SignalSelections.airway_pressure.name
            #     value = SignalSelections.airway_pressure.value
            # elif cont == "flow":
            #     label = SignalSelections.flow.name
            #     value = SignalSelections.flow.value
            # elif cont == "esophageal pressure":
            #     label = SignalSelections.esophageal_pressure.name
            #     value = SignalSelections.esophageal_pressure.value
            # elif cont == "volume":
            #     label = SignalSelections.volume.name
            #     value = SignalSelections.volume.value
            # elif cont == "CO2":
            #     label = SignalSelections.CO2.name
            #     value = SignalSelections.CO2.value
            # else:
            # label = cont
            # value = max(len(SignalSelections), len(options) + 1)
            options.append({"label": cont, "value": len(options)})

    return options
