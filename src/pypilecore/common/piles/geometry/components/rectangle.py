from __future__ import annotations

import math
from typing import Any, Literal, Tuple

import matplotlib.patches as patches
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import NDArray

from pypilecore.common.piles.geometry.components.common import (
    PrimaryPileComponentDimension,
    _BasePileGeometryComponent,
    get_area_vs_depth,
    get_circum_vs_depth,
    get_component_bounds_nap,
    instantiate_axes,
)


def calculate_equiv_tip_diameter(dim1: float, dim2: float | None = None) -> float:
    """
    Calculate the equivalent tip diameter of a rectangular pile.

    Parameters
    ----------
    dim1, dim2 : float
        The dimension of the rectangular pile (in any unit).

    Returns
    -------
    float
        The equivalent tip diameter of the rectangular pile (in the same unit as `dim1` and `dim2`).

    Notes
    -----
    The equivalent tip diameter is calculated based on the dimensions of a rectangular pile. If the maximum dimension
    (`b_max`) is greater than 1.5 times the minimum dimension (`a_min`), the equivalent tip diameter is equal to the
    minimum dimension (`a_min`). Otherwise, it is calculated using the formula: 1.13 * `a_min` * sqrt(`b_max` / `a_min`).

    Examples
    --------
    >>> calculate_equiv_tip_diameter(2.0, 3.0)
    2.0

    >>> calculate_equiv_tip_diameter(2.0, 4.0)
    2.26
    """
    if dim2 is None:
        dim2 = dim1

    b_max = max(dim1, dim2)
    a_min = min(dim1, dim2)

    if b_max > (1.5 * a_min):
        return a_min
    return float(1.13 * a_min * math.sqrt(b_max / (a_min + 1e-12)))


class RectPileGeometryComponent(_BasePileGeometryComponent):
    """The RectPileGeometryComponent class represents a rectangular pile-geometry component."""

    def __init__(
        self,
        secondary_dimension: float,
        primary_dimension: PrimaryPileComponentDimension,
        tertiary_dimension: float | None = None,
        inner_component: _BasePileGeometryComponent | None = None,
        material: str | None = None,
    ):
        """
        Represents a rectangular pile-geometry component.

        Parameters:
        -----------
        secondary_dimension : float
            The secondary dimension [m] of the pile-geometry component, which is the largest cross-sectional dimension.
        primary_dimension : PrimaryPileComponentDimension
            The primary dimension [m] of the pile-geometry component, which is measured along the primary axis of the pile.
        tertiary_dimension : float, optional
            The tertiary dimension [m] of the pile-geometry component, which is the smallest cross-sectional dimension.
        inner_component : RoundPileGeometryComponent | RectPileGeometryComponent | None, optional
            The component on the inside of the pile-geometry component, by default None.
        material : str, optional
            The material name of the pile-geometry component, by default None.
        """
        self._secondary_dimension = secondary_dimension
        self._tertiary_dimension = tertiary_dimension
        self._primary_dimension = primary_dimension
        self._inner_component = inner_component
        self._material = material

    @classmethod
    def from_api_response(
        cls,
        component: dict,
        inner_component: _BasePileGeometryComponent | None = None,
    ) -> RectPileGeometryComponent:
        """
        Instantiates a RectPileGeometryComponent from a component object in the API
        response payload.

        Parameters:
        -----------
        component: dict
            A dictionary that is retrieved from the API response payload at "/pile_properties/geometry/components/[i]".
            The component dictionary should have the following schema:

            {
                "secondary_dimension": float,
                "tertiary_dimension": float,
                "primary_dimension": {
                    "length": float,
                    "width": float
                },
                "material": str
            }

            - secondary_dimension (float): The secondary dimension of the rectangular pile component.
              This dimension represents the dimension perpendicular to the primary dimension.
            - tertiary_dimension (float): The tertiary dimension of the rectangular pile component.
              This dimension represents the dimension perpendicular to both the primary and secondary dimensions.
            - primary_dimension (dict): The primary dimension of the rectangular pile component.
                - length (float): The length of the rectangular pile component.
                  This dimension represents the length of the pile along its primary axis.
                - width (float): The width of the rectangular pile component.
                  This dimension represents the width of the pile along its secondary axis.
            - material (str): The material of the rectangular pile component.

        inner_component: RectPileGeometryComponent | RoundPileGeometryComponent | None, optional
            The component on the inside of the pile-geometry component, by default None.

        Returns:
        --------
        RectPileGeometryComponent
            A rectangular pile-geometry component.

        Example:
        --------
        >>> component = {
        ...     "secondary_dimension": 10,
        ...     "tertiary_dimension": 5,
        ...     "primary_dimension": {
        ...         "length": 20,
        ...         "width": 15
        ...     },
        ...     "material": "concrete"
        ... }
        >>> inner_component = None
        >>> result = RectPileGeometryComponent.from_api_response(component, inner_component)
        """
        return cls(
            secondary_dimension=component["secondary_dimension"],
            tertiary_dimension=component["tertiary_dimension"],
            primary_dimension=PrimaryPileComponentDimension.from_api_response(
                component["primary_dimension"]
            ),
            inner_component=inner_component,
            material=component["material"],
        )

    @property
    def inner_component(
        self,
    ) -> _BasePileGeometryComponent | None:
        """The component on the inside of the pile-geometry component"""
        return self._inner_component

    @property
    def outer_shape(self) -> Literal["rectangle"]:
        """The outer shape of the pile-geometry component"""
        return "rectangle"

    @property
    def material(self) -> str | None:
        """The material name of the pile-geometry component"""
        return self._material

    @property
    def primary_dimension(self) -> PrimaryPileComponentDimension:
        """
        The primary dimension [m] of the pile-geometry component, which is measured along the primary axis of the pile.
        """
        return self._primary_dimension

    @property
    def secondary_dimension(self) -> float:
        """
        The secondary dimension [m] of the pile-geometry component, which is the largest cross-sectional dimension.
        """
        return self._secondary_dimension

    @property
    def tertiary_dimension(self) -> float:
        """
        The tertiary dimension [m] of the pile-geometry component, which is the smallest cross-sectional dimension.
        """
        if self._tertiary_dimension is not None:
            return self._tertiary_dimension
        return self.secondary_dimension

    @property
    def cross_section_bounds(self) -> Tuple[float, float, float, float]:
        """Alias of the diameter [m] of the pile-geometry component"""
        return (
            -self.secondary_dimension / 2,
            self.secondary_dimension / 2,
            -self.tertiary_dimension / 2,
            self.tertiary_dimension / 2,
        )

    @property
    def circumference(self) -> float:
        """The outer-circumference [m] of the pile-geometry component"""
        return 2 * (self.secondary_dimension + self.tertiary_dimension)

    @property
    def equiv_tip_diameter(self) -> float:
        """
        Equivalent outer-diameter [m] of the component at the tip-level.
        According to NEN-9997-1+C2_2017 paragraphs 1.5.2.106a and 7.6.2.3.(10)(e).

        Specifically: returns self.tertiary_dimension
        if self.primary_dimension > (1,5 * self.tertiary_dimension)
        """
        return calculate_equiv_tip_diameter(
            self.tertiary_dimension, self.secondary_dimension
        )

    @property
    def area_full(self) -> float:
        """The full outer-area [m²] of the pile-geometry component, including any potential inner-components"""
        return self.secondary_dimension * self.tertiary_dimension

    def serialize_payload(self) -> dict:
        """
        Serialize the rectangular pile-geometry component to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the outer shape, secondary dimension, tertiary dimension (if set), material, and primary dimension (if set).
        """
        payload = {
            "outer_shape": self.outer_shape,
            "primary_dimension": self.primary_dimension.serialize_payload(),
            "secondary_dimension": self.secondary_dimension,
            "material": self.material,
        }
        if self.tertiary_dimension is not None:
            payload["tertiary_dimension"] = self.tertiary_dimension

        return payload

    def get_component_bounds_nap(
        self,
        pile_tip_level_nap: float | int,
        pile_head_level_nap: float | int,
    ) -> Tuple[float, float]:
        """
        Returns component head and tip level in NAP.

        Parameters
        ----------
        pile_tip_level_nap : float
            pile tip level in [m] w.r.t. NAP.
        pile_head_level_nap : float
            pile head level in [m] w.r.t. NAP.

        Returns
        -------
        tuple
            Tuple with component head and tip level in [m] w.r.t. NAP.
        """
        return get_component_bounds_nap(
            pile_tip_level_nap=pile_tip_level_nap,
            pile_head_level_nap=pile_head_level_nap,
            component_primary_length=self.primary_dimension.length,
        )

    def get_circum_vs_depth(
        self,
        depth_nap: NDArray[np.floating],
        pile_tip_level_nap: float | int,
        pile_head_level_nap: float | int,
    ) -> NDArray[np.floating]:
        """
        Returns component circumferences at requested depths.

        Parameters
        ----------
        depth_nap : np.array
            Array with depths in [m] w.r.t. NAP.
        pile_tip_level_nap : float
            pile tip level in [m] w.r.t. NAP.
        pile_head_level_nap : float
            pile head level in [m] w.r.t. NAP.

        Returns
        -------
        np.array
            Array with component circumferences at the depths in the depth parameter.
        """
        return get_circum_vs_depth(
            depth_nap=depth_nap,
            pile_tip_level_nap=pile_tip_level_nap,
            pile_head_level_nap=pile_head_level_nap,
            length=self.primary_dimension.length,
            circumference=self.circumference,
        )

    def get_inner_area_vs_depth(
        self,
        depth_nap: NDArray[np.floating],
        pile_tip_level_nap: float | int,
        pile_head_level_nap: float | int,
    ) -> NDArray[np.floating]:
        """
        Returns inner component areas at requested depths.

        Parameters
        ----------
        depth_nap : np.array
            Array with depths in [m] w.r.t. NAP.
        pile_tip_level_nap : float
            pile tip level in [m] w.r.t. NAP.
        pile_head_level_nap : float
            pile head level in [m] w.r.t. NAP.

        Returns
        -------
        np.array
            Array with inner component areas at the depths in the depth parameter.
        """
        if self.inner_component is None:
            return np.zeros_like(depth_nap)

        return self.inner_component.get_area_vs_depth(
            depth_nap=depth_nap,
            pile_tip_level_nap=pile_tip_level_nap,
            pile_head_level_nap=pile_head_level_nap,
        )

    def get_area_vs_depth(
        self,
        depth_nap: NDArray[np.floating],
        pile_tip_level_nap: float | int,
        pile_head_level_nap: float | int,
    ) -> NDArray[np.floating]:
        """
        Returns component areas at requested depths.

        Parameters
        ----------
        depth_nap : np.array
            Array with depths in [m] w.r.t. NAP.
        pile_tip_level_nap : float
            pile tip level in [m] w.r.t. NAP.
        pile_head_level_nap : float
            pile head level in [m] w.r.t. NAP.

        Returns
        -------
        np.array
            Array with component areas at the depths in the depth parameter.
        """

        (
            component_head_level_nap,
            component_tip_level_nap,
        ) = self.get_component_bounds_nap(pile_tip_level_nap, pile_head_level_nap)

        inner_area = self.get_inner_area_vs_depth(
            depth_nap=depth_nap,
            pile_tip_level_nap=pile_tip_level_nap,
            pile_head_level_nap=pile_head_level_nap,
        )

        return get_area_vs_depth(
            depth_nap=depth_nap,
            area_full=self.area_full,
            component_head_level_nap=component_head_level_nap,
            component_tip_level_nap=component_tip_level_nap,
            inner_area=inner_area,
        )

    def plot_cross_section_exterior(
        self,
        figsize: Tuple[float, float] = (6.0, 6.0),
        facecolor: Tuple[float, float, float] | str | None = None,
        axes: Axes | None = None,
        axis_arg: bool | str | Tuple[float, float, float, float] | None = "auto",
        show: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plot the cross-section of the pile at a specified depth.

        Parameters
        ----------
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
        **kwargs
            Additional keyword arguments to pass to the `plt.subplots()` function.
        """
        axes = instantiate_axes(
            figsize=figsize,
            axes=axes,
            **kwargs,
        )

        x_offset = -self.secondary_dimension / 2
        y_offset = -self.tertiary_dimension / 2

        axes.add_patch(
            patches.Rectangle(
                (x_offset, y_offset),
                self.secondary_dimension,
                self.tertiary_dimension,
                facecolor=facecolor,
                edgecolor="black",
            )
        )
        if axis_arg:
            axes.axis(axis_arg)
        if show:
            plt.show()
        return axes

    def plot_side_view(
        self,
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
        **kwargs
            Additional keyword arguments to pass to the `plt

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
        ) = self.get_component_bounds_nap(pile_tip_level_nap, pile_head_level_nap)

        if (
            top_boundary_nap > component_tip_level_nap
            and bottom_boundary_nap < component_head_level_nap
        ):
            z_offset = component_head_level_nap
            height = (
                max(component_tip_level_nap, bottom_boundary_nap)
                - component_head_level_nap
            )

            axes.add_patch(
                patches.Rectangle(
                    (self.cross_section_bounds[0], z_offset),
                    self.secondary_dimension,
                    height,
                    facecolor=facecolor,
                )
            )

        if axis_arg:
            axes.axis(axis_arg)
        if show:
            plt.show()
        return axes
