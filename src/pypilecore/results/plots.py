from typing import Any, Callable, Tuple

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from pypilecore.results.soil_properties import get_soil_layer_handles


def plot_bearing_overview(
    plot_qc: Callable[[Axes | None, bool], Axes],
    plot_friction_ratio: Callable[[Axes | None, bool], Axes],
    plot_layers: Callable[[Axes | None, bool, bool], Axes],
    plot_bearing_capacities: Callable[[Axes | None, Tuple[float, float], bool], Axes],
    test_id: str | None = None,
    figsize: Tuple[float, float] = (10.0, 12.0),
    width_ratios: Tuple[float, float, float] = (1, 0.1, 2),
    add_legend: bool = True,
    **kwargs: Any,
) -> Figure:
    """
    Plot an overview of the bearing-capacities, including the .

    Parameters
    ----------
    plot_qc:
        Function to plot the qc values vs. depth.
    plot_friction_ratio:
        Function to plot the friction ratio vs. depth.
    plot_layers:
        Function to plot the soil layers vs. depth.
    plot_bearing_capacities:
        Function to plot the bearing capacities vs. depth.
    test_id:
        The test ID to display in the legend title.
    figsize:
        Size of the activate figure, as the `plt.figure()` argument.
    width_ratios:
        Tuple of width-ratios of the subplots, as the `plt.GridSpec` argument.
    add_legend:
        Add a legend to the second axes object
    **kwargs:
        All additional keyword arguments are passed to the `pyplot.subplots()` call.

    Returns
    -------
    fig:
        The matplotlib Figure
    """

    kwargs_subplot = {
        "gridspec_kw": {"width_ratios": width_ratios},
        "sharey": "row",
        "figsize": figsize,
        "tight_layout": True,
    }

    kwargs_subplot.update(kwargs)

    fig, _ = plt.subplots(
        1,
        3,
        **kwargs_subplot,
    )

    ax_qc, ax_layers, ax_bearing = fig.axes
    ax_rf = ax_qc.twiny()
    assert isinstance(ax_rf, Axes)

    # Plot bearing capacities
    plot_qc(ax_qc, False)
    plot_friction_ratio(ax_rf, False)
    plot_layers(ax_layers, False, False)

    # Set bounds of layers to qc plot
    bounds = ax_qc.get_ylim()
    ax_layers.set_ylim(bounds)

    plot_bearing_capacities(ax_bearing, figsize, False)

    if add_legend:
        ax_qc_legend_handles_list = ax_qc.get_legend_handles_labels()[0]
        ax_rf_legend_handles_list = ax_rf.get_legend_handles_labels()[0]
        ax_layers_legend_handles_list = get_soil_layer_handles()

        # Omit last 2 duplicate "bearing" handles
        # (groundwater_level and surface_level):
        ax_bearing_legend_handles_list = ax_bearing.get_legend_handles_labels()[0][2:]

        handles_list = [
            *ax_qc_legend_handles_list,
            *ax_rf_legend_handles_list,
            *ax_layers_legend_handles_list,
            *ax_bearing_legend_handles_list,
        ]

        ax_bearing.legend(
            handles=handles_list,
            loc="upper left",
            bbox_to_anchor=(1, 1),
            title=("name: " + test_id if test_id is not None else "name: unknown"),
        )

    return fig
