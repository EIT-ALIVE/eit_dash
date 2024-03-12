from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go

if TYPE_CHECKING:
    from eitprocessing.sequence import Sequence


def create_slider_figure(
    dataset: Sequence,
    eit_variants: list[str] | None = None,
    continuous_data: list[str] | None = None,
) -> go.Figure:
    """Create the figure for the selection of range.

    Args:
        dataset: Sequence object containing the selected dataset
        eit_variants: list of the eit variants to be plotted
        continuous_data: list of the continuous data signals to be plotted
    """
    if continuous_data is None:
        continuous_data = []
    if eit_variants is None:
        eit_variants = ["raw"]

    traces = [{
                "x": dataset.eit_data[eit_variant].time,
                "y": dataset.eit_data[eit_variant].global_impedance,
                "type": "scatter",
                "mode": "lines",
                "name": "a_level",
            } for eit_variant in eit_variants]

    for cont_signal in continuous_data:
        traces.append(  # noqa: PERF401
            {
                "x": dataset.continuous_data[cont_signal].time,
                "y": dataset.continuous_data[cont_signal].values,  # noqa: PD011
                "type": "scatter",
                "mode": "lines",
                "name": "a_level",
            },
        )

    figure = go.Figure(
        data=traces,
        layout=go.Layout(
            xaxis={"rangeslider": {"visible": True}},
            margin={"t": 0, "l": 0, "b": 0, "r": 0},
        ),
    )

    for event in dataset.eit_data[eit_variants[0]].events:
        annotation = {"text": f"{event.text}", "textangle": -90}
        figure.add_vline(
            x=event.time,
            line_width=3,
            line_dash="dash",
            line_color="green",
            annotation=annotation,
        )

    return figure


def get_signal_options(dataset: Sequence, show_eit: bool = False) -> list[dict[str, int | str]]:
    """Get the options for signal selection to be shown in the signal selection section.

    Args:
        dataset: Sequence object containing the selected dataset
        show_eit: include eit data in the option if True. Default false
    Returns:
        A list of label - value options for populating the options list
    """
    options = []
    if show_eit:
        # iterate over eit data
        for eit in dataset.eit_data:
            options.append({"label": eit, "value": len(options)})

    if dataset.continuous_data:
        # iterate over continuous data
        for cont in dataset.continuous_data:
            options.append({"label": cont, "value": len(options)})

    return options
