from __future__ import annotations

from typing import TYPE_CHECKING, List

import plotly.graph_objects as go

if TYPE_CHECKING:
    from eitprocessing.sequence import Sequence


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


def create_slider_figure(
    dataset: Sequence,
    eit_variants: list[str] | None = None,
    continuous_data: list[str] | None = None,
    clickable_legend: bool = False,
) -> go.Figure:
    """Create the figure for the selection of range.

    Args:
        dataset: Sequence object containing the selected dataset
        eit_variants: list of the eit variants to be plotted
        continuous_data: list of the continuous data signals to be plotted
        clickable_legend: if True, the user can hide a signal by clicking on the legend
    """
    figure = go.Figure()
    params = dict()
    y_position = 0

    if continuous_data is None:
        continuous_data = []
    if eit_variants is None:
        eit_variants = ["raw"]

    for eit_variant in eit_variants:
        figure.add_trace(
            go.Scatter(
                x=dataset.eit_data[eit_variant].time,
                y=dataset.eit_data[eit_variant].global_impedance,
                name=eit_variant,
            )
        )

    for n, cont_signal in enumerate(continuous_data):
        figure.add_trace(
            go.Scatter(
                x=dataset.continuous_data[cont_signal].time,
                y=dataset.continuous_data[cont_signal].values,
                name=cont_signal,
                opacity=0.5,
                yaxis=f"y{n + 2}",
            ),
        )
        # decide whether to put the axis left or right
        if (n % 2) == 0:
            side = "right"
        else:
            side = "left"

        y_position += 0.1
        new_y = dict(
            title=cont_signal,
            anchor="free",
            overlaying="y",
            side=side,
            autoshift=True,
        )

        # layout parameters for multiple y axis
        param_name = f"yaxis{n + 2}"
        params.update({param_name: new_y})

    for event in dataset.eit_data[eit_variants[0]].events:
        annotation = {"text": f"{event.text}", "textangle": -90}
        figure.add_vline(
            x=event.time,
            line_width=3,
            line_dash="dash",
            line_color="green",
            annotation=annotation,
        )

    figure.update_layout(
        xaxis={"rangeslider": {"visible": True}},
        margin={"t": 0, "l": 0, "b": 0, "r": 0},
        **params,
    )

    # itemclick is a toggable element, so it can only be deactivated, and it is not possible
    # to set it to True
    if not clickable_legend:
        figure.update_layout(legend={"itemclick": False, "itemdoubleclick": False})

    return figure


def mark_selected_periods(
    original_figure: go.Figure | dict, periods: List[Sequence], period_index: int
) -> go.Figure:
    """
    Create the figure for the selection of range.

    Args:
        original_figure: figure to update
        periods: list of Sequence object containing the selected dataset.
        These ranges, the signal is plotted in black
        period_index: index of the selected period
    """
    for period in periods:
        for eit_variant in period.eit_data:
            selected_impedance = go.Scatter(
                x=period.eit_data[eit_variant].time,
                y=period.eit_data[eit_variant].global_impedance,
                name=eit_variant,
                meta={"uid": period_index},
                line={"color": "black"},
                showlegend=False,
            ).to_plotly_json()

            if type(original_figure) == go.Figure:
                original_figure.add_trace(selected_impedance)
            else:
                original_figure["data"].append(selected_impedance)

        for n, cont_signal in enumerate(period.continuous_data):
            selected_signal = go.Scatter(
                x=period.continuous_data[cont_signal].time,
                y=period.continuous_data[cont_signal].values,
                name=cont_signal,
                meta={"uid": period_index},
                opacity=0.5,
                yaxis=f"y{n + 2}",
                line={"color": "black"},
                showlegend=False,
            ).to_plotly_json()

            if type(original_figure) == go.Figure:
                original_figure.add_trace(selected_signal)
            else:
                original_figure["data"].append(selected_signal)

    return original_figure


def get_signal_options(
    dataset: Sequence, show_eit: bool = False
) -> list[dict[str, int | str]]:
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


def get_selections_slidebar(slidebar_stat: dict) -> tuple:
    """Given the layout data of a graph slidebar, it returns the first
    and the last sample selected.

    Args:
        slidebar_stat: Layout data of a graph slidebar.
    Returns:
        A tuple where the first value is the starting sample and the second value is the
        end sample. If a sample cannot be determined, None is returned.
    """

    if "xaxis.range" in slidebar_stat:
        start_sample = slidebar_stat["xaxis.range"][0]
        stop_sample = slidebar_stat["xaxis.range"][1]
    elif ("xaxis.range[0]" in slidebar_stat) and ("xaxis.range[1]" in slidebar_stat):
        start_sample = slidebar_stat["xaxis.range[0]"]
        stop_sample = slidebar_stat["xaxis.range[1]"]
    else:
        start_sample = stop_sample = None

    return start_sample, stop_sample
