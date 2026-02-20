from typing import Any, Callable, Literal, Tuple

import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from pypilecore.common.piles.geometry.components.common import instantiate_axes


def plot_side_view(
    get_component_bounds_nap: Callable[[float | int, float | int], Tuple[float, float]],
    width_offset: float,
    width: float,
    bottom_boundary_nap: float | Literal["pile_tip"] = "pile_tip",
    top_boundary_nap: float | Literal["pile_head"] = "pile_head",
    pile_tip_level_nap: float | int = -10,
    pile_head_level_nap: float | int = 0,
    figsize: Tuple[float, float] = (6.0, 6.0),
    facecolor: Tuple[float, float, float] | str | None = None,
    axes: Axes | None = None,
    axis_arg: bool | str | Tuple[float, float, float, float] | None = "scaled",
    show: bool = True,
    **kwargs: Any,
) -> Axes:
    """
    Plot the side view of the component at a specified depth.

    Parameters
    ----------
    get_component_bounds_nap : Callable[[float | int, float | int], Tuple[float, float]]
        A function that takes the pile tip and head levels in m w.r.t. NAP and returns the component head and tip levels in m w.r.t. NAP.
    width_offset : float
        The horizontal offset of the component from the y-axis in the plot, in meters.
    width : float
        The width of the component in meters.
    bottom_boundary_nap : float or str, optional
        The bottom boundary level of the plot, in m w.r.t. NAP. Default = "pile_tip".
    top_boundary_nap : float or str, optional
        The top boundary level of the plot, in m w.r.t. NAP. Default = "pile_head".
    pile_tip_level_nap : float, optional
        The pile tip level in m w.r.t. NAP. Default = -10.
    pile_head_level_nap : float, optional
        The pile head level in m w.r.t. NAP. Default = 0.
    figsize : tuple, optional
        The figure size (width, height) in inches, by default (6.0, 6.0).
    facecolor : tuple or str, optional
        The face color of the pile cross-section, by default None.
    axes : Axes
        The axes object to plot the cross-section on.
    axis_arg : bool or str or tuple, optional
        The axis argument to pass to the `axes.axis()` function, by default "auto".
    show : bool, optional
        Whether to display the plot, by default True.

    Returns
    -------
    Axes
        The axes object to plot the cross-section on.
    """
    axes = instantiate_axes(
        figsize=figsize,
        axes=axes,
        **kwargs,
    )

    if top_boundary_nap == "pile_head":
        top_boundary_nap = pile_head_level_nap

    if bottom_boundary_nap == "pile_tip":
        bottom_boundary_nap = pile_tip_level_nap

    (
        component_head_level_nap,
        component_tip_level_nap,
    ) = get_component_bounds_nap(pile_tip_level_nap, pile_head_level_nap)

    if (
        top_boundary_nap >= component_tip_level_nap
        and bottom_boundary_nap <= component_head_level_nap
    ):
        # If the component is at least partially within the plot boundaries, plot the component

        z_offset = component_tip_level_nap
        height = component_head_level_nap - max(
            component_tip_level_nap, bottom_boundary_nap
        )

        if np.isclose(height, 0):
            # Visualise baseplate (height = 0) as a black line
            height = 0.1
            facecolor = "black"

        axes.add_patch(
            patches.Rectangle(
                (width_offset, z_offset),
                width,
                height,
                facecolor=facecolor,
                edgecolor="black",
            )
        )

    if axis_arg:
        axes.axis(axis_arg)
    if show:
        plt.show()
    return axes
