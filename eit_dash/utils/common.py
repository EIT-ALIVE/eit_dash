from __future__ import annotations

import re
from typing import TYPE_CHECKING

import dash_bootstrap_components as dbc
import plotly.colors
import plotly.graph_objects as go
from dash import html

from eit_dash.definitions import element_ids as ids
from eit_dash.definitions import layout_styles as styles
from eit_dash.definitions.constants import RAW_EIT_LABEL

if TYPE_CHECKING:
    from eitprocessing.datahandling.sequence import Sequence

    from eit_dash.utils.data_singleton import Period


def blank_fig():
    """Create an empty figure."""
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


def create_filter_results_card(parameters: dict) -> dbc.Card:
    """
    Create the card with the information on the parameters used for filtering the data.

    Args:
        parameters: dictionary containing the filter information
    """
    card_list = [
        html.H4("Data filtered", className="card-title"),
    ]
    card_list += [dbc.Row(f"{data}: {value}", style=styles.INFO_CARD) for data, value in parameters.items()]

    return dbc.Card(dbc.CardBody(card_list), id=ids.FILTERING_SAVED_CARD)


def create_info_card(dataset: Sequence, remove_button: bool = False) -> dbc.Card:
    """Create the card with the information on the loaded dataset to be displayed in the Results section.

    Args:
        dataset: Sequence object containing the selected dataset
        remove_button: add the remove button if set to True
    """
    info_data = {
        "Name": dataset.eit_data["raw"].path.name,
        "n_frames": dataset.eit_data["raw"].nframes,
        "start_time": dataset.eit_data["raw"].time[0],
        "end_time": dataset.eit_data["raw"].time[-1],
        "vendor": dataset.eit_data["raw"].vendor,
        "continuous signals": str(list(dataset.continuous_data)),
        "path": str(dataset.eit_data["raw"].path),
    }

    card_list = [
        html.H4(dataset.label, className="card-title"),
        html.H6(dataset.eit_data["raw"].vendor, className="card-subtitle"),
    ]
    card_list += [dbc.Row(f"{data}: {value}", style=styles.INFO_CARD) for data, value in info_data.items()]
    if remove_button:
        card_list += [
            dbc.Button(
                "Remove",
                id={"type": ids.REMOVE_DATA_BUTTON, "index": dataset.label},
            ),
        ]
    return dbc.Card(dbc.CardBody(card_list), id=dataset.label)


def create_selected_period_card(
    period: Sequence,
    dataset: str,
    index: int,
    remove_button: bool = True,
) -> dbc.Card:
    """
    Create the card with the information on the selected period to be displayed in the Results section.

    Args:
        period: Sequence object containing the selected period
        dataset: The original dataset from which the period has been selected
        index: of the period
        remove_button: add the remove button if set to True
    """
    info_data = {
        "n_frames": period.eit_data["raw"].nframes,
        "start_time": period.eit_data["raw"].time[0],
        "end_time": period.eit_data["raw"].time[-1],
        "dataset": dataset,
    }

    card_list = [
        html.H4(period.label, className="card-title"),
    ]
    card_list += [dbc.Row(f"{data}: {value}", style=styles.INFO_CARD) for data, value in info_data.items()]
    if remove_button:
        card_list += [
            dbc.Button(
                "Remove",
                id={"type": ids.REMOVE_PERIOD_BUTTON, "index": str(index)},
            ),
        ]

    return dbc.Card(
        dbc.CardBody(card_list),
        id={"type": ids.PERIOD_CARD, "index": str(index)},
    )


def create_slider_figure(
    dataset: Sequence,
    continuous_data: list[str] | None = None,
    clickable_legend: bool = False,
) -> go.Figure:
    """Create the figure for the selection of range. The raw global impedance is plotted by default.

    Args:
        dataset: Sequence object containing the selected dataset
        continuous_data: list of the continuous data signals to be plotted
        clickable_legend: if True, the user can hide a signal by clicking on the legend
    """
    figure = go.Figure()
    params = {}
    y_position = 0

    if continuous_data is None:
        continuous_data = []

    figure.add_trace(
        go.Scatter(
            x=dataset.continuous_data[RAW_EIT_LABEL].time,
            y=dataset.continuous_data[RAW_EIT_LABEL].values,
            name=RAW_EIT_LABEL,
            line={"color": plotly.colors.DEFAULT_PLOTLY_COLORS[0]},
        ),
    )
    figure.update_yaxes(
        color=plotly.colors.DEFAULT_PLOTLY_COLORS[0],
        title=f"{RAW_EIT_LABEL} {dataset.continuous_data[RAW_EIT_LABEL].unit}",
    )

    for n, cont_signal in enumerate(continuous_data):
        if cont_signal != RAW_EIT_LABEL:
            figure.add_trace(
                go.Scatter(
                    x=dataset.continuous_data[cont_signal].time,
                    y=dataset.continuous_data[cont_signal].values,
                    name=cont_signal,
                    line={"color": plotly.colors.DEFAULT_PLOTLY_COLORS[n + 1]},
                    opacity=0.5,
                    yaxis=f"y{n + 2}",
                ),
            )
            # decide whether to put the axis left or right
            side = "right" if n % 2 == 0 else "left"

            y_position += 0.1
            new_y = {
                "title": f"{cont_signal} {dataset.continuous_data[cont_signal].unit}",
                "anchor": "free",
                "overlaying": "y",
                "side": side,
                "autoshift": True,
                "color": plotly.colors.DEFAULT_PLOTLY_COLORS[n + 1],
            }

            # layout parameters for multiple y axis
            param_name = f"yaxis{n + 2}"
            params.update({param_name: new_y})

    # add events
    if hasattr(dataset, "sparse_data"):
        for key in dataset.sparse_data:
            if re.match("events", key):
                for k, v in enumerate(dataset.sparse_data[key].values):
                    annotation = {"text": f"{v.text}", "textangle": -90}
                    figure.add_vline(
                        x=dataset.sparse_data[key].time[k],
                        line_width=3,
                        line_dash="dash",
                        line_color="green",
                        annotation=annotation,
                    )
                break

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
    original_figure: go.Figure | dict,
    periods: list[Period],
) -> go.Figure:
    """
    Create the figure for the selection of range.

    Args:
        original_figure: figure to update
        periods: list of Sequence object containing the selected dataset.
        These ranges, the signal is plotted in black
    """
    for period in periods:
        seq = period.get_data()

        for n, cont_signal in enumerate(seq.continuous_data):
            params = {
                "x": seq.continuous_data[cont_signal].time,
                "y": seq.continuous_data[cont_signal].values,  # noqa: PD011
                "name": cont_signal,
                "meta": {"uid": period.get_period_index()},
                "line": {"color": "black"},
                "showlegend": False,
            }
            if cont_signal != RAW_EIT_LABEL:
                params.update(
                    {
                        "opacity": 0.5,
                        "yaxis": f"y{n + 2}",
                    },
                )
            selected_signal = go.Scatter(**params).to_plotly_json()

            if isinstance(original_figure, go.Figure):
                original_figure.add_trace(selected_signal)
            else:
                original_figure["data"].append(selected_signal)

    return original_figure


def get_signal_options(
    dataset: Sequence,
    show_eit: bool = False,
) -> list[dict[str, int | str]]:
    """Get the options for signal selection to be shown in the signal selection section.

    Args:
        dataset: Sequence object containing the selected dataset
        show_eit: include eit data in the option if True. Default false
    Returns:
        A list of label - value options for populating the options list
    """
    options = []

    if dataset.continuous_data:
        # iterate over continuous data
        for cont in dataset.continuous_data:
            if (cont == RAW_EIT_LABEL and show_eit) or cont != RAW_EIT_LABEL:
                options.append({"label": cont, "value": len(options)})

    return options


def get_selections_slidebar(slidebar_stat: dict) -> tuple:
    """Given the layout data of a graph slidebar, it returns the first and the last sample selected.

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
