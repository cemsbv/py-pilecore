from __future__ import annotations

import math
from typing import Any, Dict, Literal, Tuple

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


class RoundPileGeometryComponent(_BasePileGeometryComponent):
    """The RoundPileGeometryComponent class represents a round pile-geometry component."""

    def __init__(
        self,
        diameter: float,
        primary_dimension: PrimaryPileComponentDimension,
        inner_component: _BasePileGeometryComponent | None = None,
        material: str | None = None,
    ):
        """
        Represents a round pile-geometry component.

        Parameters:
        -----------
        diameter : float
            The outer-diameter [m] of the pile-geometry component.
        primary_dimension : PrimaryPileComponentDimension
            The primary dimension [m] of the pile-geometry component, which is measured along the primary axis of the pile.
        inner_component : RoundPileGeometryComponent | RectPileGeometryComponent | None, optional
            The component on the inside of the pile-geometry component, by default None.
        material : str, optional
            The material name of the pile-geometry component, by default None.
        """
        self._diameter = diameter
        self._primary_dimension = primary_dimension
        self._inner_component = inner_component
        self._material = material

    @classmethod
    def from_api_response(
        cls,
        component: dict,
        inner_component: _BasePileGeometryComponent | None = None,
    ) -> RoundPileGeometryComponent:
        """
        Instantiates a RoundPileGeometryComponent from a component object in the API
        response payload.

        Parameters:
        -----------
        component: dict
            A dictionary that represents the component object retrieved from the API response payload.
            The dictionary should have the following schema:
            {
                "diameter": float,  # The diameter of the round pile component.
                "primary_dimension": {
                    "length": float,  # The length of the primary dimension of the round pile component.
                },
                "material": str  # The material of the round pile component.
            }
        inner_component: RoundPileGeometryComponent | RectPileGeometryComponent | None, optional
            The component on the inside of the pile-geometry component, by default None.

        Returns:
        --------
        RoundPileGeometryComponent
            A round pile-geometry component.

        Example:
        --------
        >>> component = {
        ...     "diameter": 10,
        ...     "primary_dimension": {
        ...         "length": 20,
        ...         "width": 30
        ...     },
        ...     "material": "concrete"
        ... }
        >>> inner_component = RectPileGeometryComponent(...)
        >>> round_component = RoundPileGeometryComponent.from_api_response(component, inner_component)
        """
        return cls(
            diameter=component["diameter"],
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
    def outer_shape(self) -> Literal["round"]:
        """The outer shape of the pile-geometry component"""
        return "round"

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
    def cross_section_bounds(self) -> Tuple[float, float, float, float]:
        """Alias of the diameter [m] of the pile-geometry component"""
        return (
            -self.diameter / 2,
            self.diameter / 2,
            -self.diameter / 2,
            self.diameter / 2,
        )

    @property
    def diameter(self) -> float:
        """The outer-diameter [m] of the pile-geometry component"""
        return self._diameter

    @property
    def radius(self) -> float:
        """The outer-radius [m] of the pile-geometry component"""
        return self.diameter / 2

    @property
    def circumference(self) -> float:
        """The outer-circumference [m] of the pile-geometry component"""
        return self.diameter * math.pi

    @property
    def equiv_tip_diameter(self) -> float:
        """
        Equivalent diameter [m] of the component at tip-level.
        """
        return self.diameter

    @property
    def area_full(self) -> float:
        """The full outer-area [m²] of the pile-geometry component, including any potential inner-components"""
        return (self.diameter / 2) ** 2 * math.pi

    def serialize_payload(
        self,
    ) -> Dict[str, str | float | Dict[str, float | None] | None]:
        """
        Serialize the round pile-geometry component to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the outer shape, diameter, material, and primary dimension (if set).
        """
        return {
            "outer_shape": self.outer_shape,
            "primary_dimension": self.primary_dimension.serialize_payload(),
            "diameter": self.diameter,
            "material": self.material,
        }

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
        Plot the cross-section of the component at a specified depth.

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
        axes.add_patch(
            patches.Circle((0, 0), self.radius, facecolor=facecolor, edgecolor="black")
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
                    self.diameter,
                    height,
                    facecolor=facecolor,
                )
            )

        if axis_arg:
            axes.axis(axis_arg)
        if show:
            plt.show()
        return axes
