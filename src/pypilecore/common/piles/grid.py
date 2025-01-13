from __future__ import annotations

from typing import Any, List, Tuple

import matplotlib.patches as patches
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from shapely.geometry import MultiPolygon, shape
from shapely.plotting import plot_polygon


class PileGridProperties:
    def __init__(
        self,
        points: List[Tuple[float, float]],
        index_location: int,
        geometry: MultiPolygon | None = None,
        _validate: bool = True,
    ):
        """
        Class that holds the information of the pile placement.
        The structure of the grid effects the effective area of the
        pile.

        Parameters
        ----------
        points: List of tuple
            List of tuple with xy coordinates.
        index_location: int
            selected index of the points list as pile location
        geometry: MultiPolygon, optional
            A;eff as polygon
        _validate: bool, optional
            flag that overrules validation of the parameters

        """
        if len(points) < 2 and _validate:
            raise ValueError("Provide at least two points to the pile grid.")

        if len(points) != len(set(points)):
            raise ValueError("All points of the pile grid must be unique.")
        if len(points) - 1 < index_location > 0:
            raise IndexError(
                f"Index out of range, must be between 0 and {len(points) - 1} got {index_location}."
            )

        self._points = points
        self._index_location = index_location
        self._geometry = geometry

    @classmethod
    def regular(cls, ctc: float, index_location: int) -> "PileGridProperties":
        """
        Create a regular grid with a centre to centre distance provided by the user.
        The regular grid contains 9 points. Numbering start in the lower left corner.
        So for the
            - center pile `index_location= 4`
            - middle pile `index_location= 1 or 3 or 4 or 5 or 7`
            - corner pile `index_location= 0 or 2 or 6 or 8`

        x --- x --- x
        |     |     |
        x --- x --- x
        |     |     |
        x --- x --- x   with --- == | == ctc

        Parameters
        ----------
        ctc: float
            Centre to centre distance of regular grid [m]
        index_location: int
            Location of the pile to calculate
        Returns
        -------
        PileGrid
        """
        xx, yy = np.meshgrid(np.arange(0, 3) * ctc, np.arange(0, 3) * ctc)

        return cls(
            points=list(zip(xx.flatten(), yy.flatten())), index_location=index_location
        )

    @classmethod
    def from_api_response(cls, payload: dict) -> PileGridProperties:
        """
        Instantiates a PileGeometry from a geometry object in the API response payload.

        Parameters:
        -----------
        geometry: dict
            A dictionary that is retrieved from the API response payload at "/pile_properties/geometry".

        Returns:
        --------
        PileGeometry
            A pile geometry.
        """
        # make list type hashable
        points = [(point[0], point[1]) for point in payload["points"]]
        return cls(
            points=points,
            index_location=payload["index_location"],
            geometry=shape(payload["geometry"]),
            _validate=False,
        )

    def serialize_payload(self) -> dict:
        return {
            "locations": self._points,
            "pile_index": self._index_location,
        }

    def plot_overview(
        self,
        figsize: Tuple[float, float] = (6.0, 6.0),
        axes: Axes | None = None,
        add_ticks: bool = False,
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plot the Bird's-eye view of the pile grid. When provided the effect area of
        the pile influence zone is add to the figure.

        Parameters
        ----------
        figsize : tuple, optional
            The figure size (width, height) in inches, by default (6.0, 6.0).
        axes : Axes
            The axes object to plot the cross-section on.
        add_ticks : bool
            Add ticks to figure, by default False
        add_legend : bool
            Add legend to figure, by default True
        **kwargs
            Additional keyword arguments to pass to the `plt
        """

        # Create axes objects if not provided
        if axes is not None:
            if not isinstance(axes, Axes):
                raise ValueError(
                    "'axes' argument to plot_overview() must be a `pyplot.axes.Axes` object or None."
                )
        else:
            kwargs_subplot = {
                "figsize": figsize,
                "tight_layout": True,
            }

            kwargs_subplot.update(kwargs)

            _, axes = plt.subplots(1, 1, **kwargs_subplot)

            if not isinstance(axes, Axes):
                raise ValueError(
                    "Could not create Axes objects. This is probably due to invalid matplotlib keyword arguments. "
                )
        handles = [
            Line2D(
                [0],
                [0],
                label="Selected pile",
                marker=".",
                color="None",
                markerfacecolor="tab:orange",
                markeredgecolor="None",
                ls="",
            ),
        ]

        if len(self._points) >= 2:
            handles.append(
                Line2D(
                    [0],
                    [0],
                    color="None",
                    label="Other piles",
                    marker=".",
                    markerfacecolor="gray",
                    markeredgecolor="None",
                    ls="",
                )
            )
        # add the effective area of the pile with the pile grid
        if self._geometry is not None:
            plot_polygon(self._geometry, ax=axes, add_points=False, color="tab:blue")
            handles.append(
                patches.Patch(
                    facecolor="tab:blue",
                    alpha=0.3,
                    label=r"$A_{eff}$" + rf" {self._geometry.area:.1f} $m^2$",
                    edgecolor="tab:blue",
                )
            )

        # plot points
        colors = ["gray"] * len(self._points)
        colors[self._index_location] = "tab:orange"
        axes.scatter(*zip(*self._points), color=colors, marker=".")

        # add labels to points
        for x, y, label in zip(*zip(*self._points), range(len(self._points))):
            axes.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

        axes.ticklabel_format(useOffset=False, style="plain")
        axes.set_aspect("equal", adjustable="box")
        if add_ticks:
            axes.xaxis.set_major_locator(ticker.NullLocator())
            axes.yaxis.set_major_locator(ticker.NullLocator())

        if add_legend:
            axes.legend(
                title="Pile grid configuration",
                bbox_to_anchor=(1.04, 1),
                loc="upper left",
                handles=handles,
            )
        return axes
