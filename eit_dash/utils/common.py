from eit_dash.definitions.option_lists import SignalSelections
from eitprocessing.sequence import Sequence
from typing import List, Dict

import plotly.graph_objects as go


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


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
    figure = go.Figure()
    params = dict()
    y_position = 0

    for eit_variant in eit_variants:
        # TODO: This is a patch! Needs to be changed
        if eit_variant == "raw":
            try:
                impedance = dataset.eit_data.variants[eit_variant].global_impedance
            except KeyError:
                impedance = dataset.eit_data.variants[None].global_impedance
        figure.add_trace(go.Scatter(x=dataset.eit_data.time, y=impedance, name="eit"))

    for n, cont_signal in enumerate(continuous_data):
        figure.add_trace(
            go.Scatter(
                x=dataset.continuous_data[cont_signal].time,
                y=dataset.continuous_data[cont_signal].variants["raw"].values,
                name=cont_signal,
                opacity=0.5,
                yaxis=f"y{n+2}",
            )
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
        param_name = f"yaxis{n+2}"
        params.update({param_name: new_y})

    for event in dataset.eit_data.events:
        annotation = dict(text=f"{event.text}", textangle=-90)
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
