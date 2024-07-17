from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Tuple

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import NDArray


def get_component_bounds_nap(
    pile_tip_level_nap: float | int,
    pile_head_level_nap: float | int,
    component_primary_length: float | int | None,
) -> Tuple[float, float]:
    """
    Returns component head and tip level in NAP.

    Parameters
    ----------
    pile_tip_level_nap : float
        pile tip level in [m] w.r.t. NAP.
    pile_head_level_nap : float
        pile head level in [m] w.r.t. NAP.
    component_primary_length : float, optional
        The length of the pile-geometry component.

    Returns
    -------
    tuple
        Tuple with component head and tip level in [m] w.r.t. NAP.
    """
    # Component tip level is always the pile tip level
    component_tip_level_nap = pile_tip_level_nap

    # Component head level is the pile head level if the length is not set
    if component_primary_length is not None:
        component_head_level_nap = pile_tip_level_nap + component_primary_length
    else:
        component_head_level_nap = pile_head_level_nap

    return float(component_head_level_nap), float(component_tip_level_nap)


def get_circum_vs_depth(
    depth_nap: NDArray[np.floating],
    pile_tip_level_nap: float | int,
    pile_head_level_nap: float | int,
    length: float | None,
    circumference: float,
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
    length : float, optional
        The length of the pile-geometry component, by default None.
    circumference : float
        The circumference of the pile-geometry component.

    Returns
    -------
    np.array
        Array with component circumferences at the depths in the depth parameter.
    """
    circum_vs_depth = np.zeros_like(depth_nap)

    # Component tip level is always the pile tip level
    component_tip_level_nap = pile_tip_level_nap

    # Component head level is the pile head level if the length is not set
    if length is not None:
        component_head_level_nap = pile_tip_level_nap + length
    else:
        component_head_level_nap = pile_head_level_nap

    # Fill the circumference between component tip and head level
    circum_vs_depth[
        (depth_nap <= component_head_level_nap) & (depth_nap >= component_tip_level_nap)
    ] = circumference

    return circum_vs_depth


def get_area_vs_depth(
    depth_nap: NDArray[np.floating],
    area_full: float | int,
    component_head_level_nap: float | int,
    component_tip_level_nap: float | int,
    inner_area: NDArray[np.floating],
) -> NDArray[np.floating]:
    """
    Returns component areas at requested depths.

    Parameters
    ----------
    depth_nap : np.array
        Array with depths in [m] w.r.t. NAP.
    area_full : float
        The full outer-area [m²] of the pile-geometry component, including any potential inner-components.
    pile_tip_level_nap : float
        pile tip level in [m] w.r.t. NAP.
    pile_head_level_nap : float
        pile head level in [m] w.r.t. NAP.
    component_head_level_nap : float
        Component head level in [m] w.r.t. NAP.
    component_tip_level_nap : float
        Component tip level in [m] w.r.t. NAP.
    inner_area : np.array
        Array with inner areas at the depths in the depth parameter.

    Returns
    -------
    np.array
        Array with component areas at the depths in the depth parameter.
    """
    area_vs_depth = np.zeros_like(depth_nap, dtype=np.floating)

    # Mask the depths between the component tip and head level
    mask_depths = (depth_nap <= component_head_level_nap) & (
        depth_nap >= component_tip_level_nap
    )

    # Fill the area between component tip and head level, subtracting the inner area
    area_vs_depth[mask_depths] = float(area_full) - inner_area[mask_depths]

    return area_vs_depth


def instantiate_axes(
    figsize: Tuple[float, float] = (6.0, 6.0),
    axes: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """
    Validate axes objects if provided, otherwise create a new axes object.

    Parameters
    ----------
    figsize : tuple, optional
        The figure size (width, height) in inches, by default (6.0, 6.0).
    axes : Axes, optional
        The axes object to plot the cross-section on.
    **kwargs
        Additional keyword arguments to pass to the `plt.subplots()` function.

    Returns
    -------
    Axes
        The axes object to plot the cross-section on.
    """
    # Create axes objects if not provided
    if axes is not None:
        if not isinstance(axes, Axes):
            raise ValueError(
                "'axes' argument must be a `pyplot.axes.Axes` object or None."
            )

    else:
        kwargs_subplot = {
            "figsize": figsize,
            "tight_layout": True,
        }

        kwargs_subplot.update(kwargs)

        _, axes = plt.subplots(
            1,
            1,
            **kwargs_subplot,
        )

        if not isinstance(axes, Axes):
            raise ValueError(
                "Could not create Axes objects. This is probably due to invalid matplotlib keyword arguments. "
            )

    return axes


class _BasePileGeometryComponent(ABC):
    """
    The _BasePileGeometryComponent class is an abstract base class for pile-geometry components.
    """

    @classmethod
    @abstractmethod
    def from_api_response(
        cls,
        component: dict,
        inner_component: _BasePileGeometryComponent | None = None,
    ) -> _BasePileGeometryComponent:
        """
        Instantiates a pile-geometry component from a component object in the API response payload.

        Parameters:
        -----------
        component: dict
            A dictionary that is retrieved from the API response payload at "/pile_properties/geometry/components/[i]".
        inner_component: _BasePileGeometryComponent | None, optional
            The component on the inside of the pile-geometry component, by default None.

        Returns:
        --------
        _BasePileGeometryComponent
            A pile-geometry component.
        """
        ...

    @property
    @abstractmethod
    def inner_component(
        self,
    ) -> _BasePileGeometryComponent | None:
        """The component on the inside of the pile-geometry component"""
        ...

    @property
    @abstractmethod
    def outer_shape(self) -> str:
        """The outer shape of the pile-geometry component"""
        ...

    @property
    @abstractmethod
    def material(self) -> str | None:
        """The material name of the pile-geometry component"""
        ...

    @property
    @abstractmethod
    def primary_dimension(self) -> PrimaryPileComponentDimension:
        """
        The primary dimension [m] of the pile-geometry component, which is measured along the primary axis of the pile.
        """
        ...

    @property
    @abstractmethod
    def circumference(self) -> float:
        """The outer-circumference [m] of the pile-geometry component"""
        ...

    @property
    @abstractmethod
    def equiv_tip_diameter(self) -> float:
        """
        Equivalent outer-diameter [m] of the component at the tip-level.
        """
        ...

    @property
    @abstractmethod
    def area_full(self) -> float:
        """The full outer-area [m²] of the pile-geometry component, including any potential inner-components"""
        ...

    @abstractmethod
    def serialize_payload(self) -> dict:
        """
        Serialize the pile-geometry component to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the geometry properties.
        """

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
            The face color of the cross-section, by default None.
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
        ...

    @abstractmethod
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
        Plot the side view of the cross-section at a specified depth.

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
            Additional keyword arguments to pass to the `plt
        """
        ...


class PrimaryPileComponentDimension:
    """
    The PrimaryPileComponentDimension class represents the primary dimension of a pile-geometry component,
    which is measured along the primary axis of the pile. It contains the length, top level, and bottom level
    of the pile-geometry component.
    """

    def __init__(
        self,
        length: float | None = None,
    ):
        """
        Represents the primary dimension of a pile-geometry component, which is measured
        along the primary axis of the pile.

        Args:
            length: The length [m] of the pile-geometry component (along the primary axis).
        """
        self._length = length

    @classmethod
    def from_api_response(cls, primary_dim: dict) -> PrimaryPileComponentDimension:
        """
        Instantiates a PrimaryPileComponentDimension from a primary dimension object in the API response payload.

        Args:
            primary_dim: A dictionary that is retrieved from the API response payload at "/pile_properties/geometry/components/[i]/primary_dimension".
        """
        return cls(
            length=primary_dim.get("length"),
        )

    @property
    def length(self) -> float | None:
        """The length [m] of the pile-geometry component"""
        return self._length

    def serialize_payload(self) -> Dict[str, float | None] | None:
        """
        Serialize the primary dimension to a dictionary payload for the API.

        Only contains the length, since this is the only accepted value by the API.
        Returns None if the length is not set.

        Returns:
            A dictionary payload containing the length of the primary dimension.
        """
        if self.length is not None:
            return {"length": self.length}
        return None
