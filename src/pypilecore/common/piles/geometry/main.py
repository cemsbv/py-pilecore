from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import NDArray

from pypilecore.common.piles.geometry.components import (
    RectPileGeometryComponent,
    RoundPileGeometryComponent,
)
from pypilecore.common.piles.geometry.materials import Color, PileMaterial


class PileGeometry:
    """The PileGeometry class represents the geometry of a pile."""

    def __init__(
        self,
        components: List[RoundPileGeometryComponent | RectPileGeometryComponent],
        materials: List[PileMaterial] | None = None,
        pile_tip_factor_s: float | None = None,
        beta_p: float | None = None,
    ):
        """
        Represents the geometry of a pile.

        Parameters:
        -----------
        components : list
            A list of pile geometry components.
        materials : list, optional
            A list of materials used in the pile geometry, by default None.
        pile_tip_factor_s : float, optional
            The pile tip factor S, by default None.
        beta_p : float, optional
            The beta_p value, by default None.
        """
        self._components = components
        self._materials = materials
        self._pile_tip_factor_s = pile_tip_factor_s
        self._beta_p = beta_p

    @classmethod
    def from_api_response(cls, geometry: dict) -> PileGeometry:
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
        components: List[RoundPileGeometryComponent | RectPileGeometryComponent] = []
        for component in geometry["components"]:
            if component["outer_shape"] == "round":
                components.append(
                    RoundPileGeometryComponent.from_api_response(component)
                )
            else:
                components.append(
                    RectPileGeometryComponent.from_api_response(component)
                )

        materials = []
        if "materials" in geometry:
            for material in geometry["materials"]:
                materials.append(PileMaterial.from_api_response(material))

        return cls(
            components=components,
            materials=materials,
            pile_tip_factor_s=geometry["properties"].get("pile_tip_factor_s"),
            beta_p=geometry["properties"]["beta_p"],
        )

    @property
    def components(
        self,
    ) -> List[RoundPileGeometryComponent | RectPileGeometryComponent]:
        """The components of the pile geometry"""
        return self._components

    @property
    def materials(self) -> List[PileMaterial]:
        """The materials used in the pile geometry"""
        return self._materials if self._materials is not None else []

    @property
    def materials_dict(self) -> Dict[str, PileMaterial]:
        """The materials used in the pile geometry as a dictionary with the material name as key"""
        return {material.name: material for material in self.materials}

    @property
    def pile_tip_factor_s(self) -> float | None:
        """The pile tip factor S of the pile geometry"""
        return self._pile_tip_factor_s

    @property
    def beta_p(self) -> float | None:
        """The beta_p value of the pile geometry"""
        return self._beta_p

    @property
    def equiv_diameter_pile_tip(self) -> float:
        """The equivalent diameter of the pile at the pile tip."""
        return self.components[-1].equiv_tip_diameter

    @property
    def circumference_pile_tip(self) -> float:
        """The outer-circumference of the pile at the pile tip."""
        return self.components[-1].circumference

    @property
    def area_pile_tip(self) -> float:
        """The area of the pile at the pile tip."""
        return self.components[-1].area_full

    def serialize_payload(self) -> Dict[str, list | dict]:
        """
        Serialize the pile geometry to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the components, materials (if set), pile tip factor S (if set), and beta_p (if set).
        """
        components = [component.serialize_payload() for component in self.components]
        payload: Dict[str, Any] = {"components": components}

        if self.materials is not None and len(self.materials) > 0:
            materials = [material.serialize_payload() for material in self.materials]
            payload["materials"] = materials

        custom_geom_properties: Dict[str, float] = {}
        if self.pile_tip_factor_s is not None:
            custom_geom_properties["pile_tip_factor_s"] = self.pile_tip_factor_s

        if self.beta_p is not None:
            custom_geom_properties["beta_p"] = self.beta_p

        if len(custom_geom_properties.keys()) > 0:
            payload["custom_properties"] = custom_geom_properties

        return payload

    def get_circum_vs_depth(
        self,
        pile_tip_level_nap: float | int,
        pile_head_level_nap: float | int,
        depth_nap: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns pile circumferences at requested depths.

        Parameters
        ---------_
        pile_tip_level_nap : float
            Pile tip level in [m] w.r.t. NAP.
        pile_head_level_nap : float
            Pile head level in [m] w.r.t. NAP.
        depth_nap : np.array
            Array with depths in [m] w.r.t. NAP.

        Returns
        -------
        np.array
            Array with pile circumferences at the requested `depth_nap` levels.
        """
        circum_vs_depth = np.zeros_like(depth_nap)

        # Use the maximum circumference of all components at each depth.
        for component in self.components:
            circum_vs_depth = np.maximum(
                circum_vs_depth,
                component.get_circum_vs_depth(
                    pile_tip_level_nap=pile_tip_level_nap,
                    pile_head_level_nap=pile_head_level_nap,
                    depth_nap=depth_nap,
                ),
            )

        return circum_vs_depth

    def get_area_vs_depth(
        self,
        pile_tip_level_nap: float | int,
        pile_head_level_nap: float | int,
        depth_nap: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns cross-sectional area of the pile at requested depths.

        Parameters
        ---------_
        pile_tip_level_nap : float
            Pile tip level in [m] w.r.t. NAP.
        pile_head_level_nap : float
            Pile head level in [m] w.r.t. NAP.
        depth_nap : np.array
            Array with depths in [m] w.r.t. NAP.

        Returns
        -------
        np.array
            Array with pile areas at the requested `depth_nap` levels.
        """
        area_vs_depth = np.zeros_like(depth_nap)

        # Use the maximum area of all components at each depth.
        for component in self.components:
            area_vs_depth = np.maximum(
                area_vs_depth,
                component.get_area_vs_depth(
                    pile_tip_level_nap=pile_tip_level_nap,
                    pile_head_level_nap=pile_head_level_nap,
                    depth_nap=depth_nap,
                ),
            )

        return area_vs_depth

    def plot(
        self,
        pile_tip_level_nap: float | int = -10,
        pile_head_level_nap: float | int = 0,
        figsize: Tuple[float, float] | None = (3, 9),
        show: bool = True,
        **kwargs: Any,
    ) -> List[Axes]:
        """
        Plot the top-view of the pile at a specified depth.

        Parameters
        ----------
        pile_tip_level_nap : float, optional
            The pile tip level in m w.r.t. NAP, by default -10.
        pile_head_level_nap : float, optional
            The pile head level in m w.r.t. NAP, by default 0.
        figsize : tuple, optional
            The figure size (width, height) in inches, by default (6.0, 6.0).
        show : bool, optional
            Whether to display the plot, by default True.
        **kwargs
            Additional keyword arguments to pass to the `plt
        """
        kwargs_subplot = {
            "figsize": figsize,
            "gridspec_kw": {
                "hspace": 0.15,
                "height_ratios": [1, 4],
            },
        }

        kwargs_subplot.update(kwargs)

        height_ratio = (
            kwargs_subplot["gridspec_kw"]["height_ratios"][1]  # type: ignore
            / kwargs_subplot["gridspec_kw"]["height_ratios"][0]  # type: ignore
        )

        _, axes = plt.subplots(
            2,
            1,
            **kwargs_subplot,
        )

        x_ticks = set([0.0])
        y_ticks = set([0.0])

        for component in self.components[::-1]:
            facecolor = "grey"
            if component.material in self.materials_dict:
                material_color = self.materials_dict[component.material].color
                if isinstance(material_color, Color):
                    facecolor = material_color.hex
                elif isinstance(material_color, Color):
                    facecolor = (
                        material_color.red,
                        material_color.green,
                        material_color.blue,
                    )

            component.plot_cross_section_exterior(
                axes=axes[0],
                facecolor=facecolor,
                edgecolor="black",
                axis_arg=None,
                show=False,
            )

            component.plot_side_view(
                pile_tip_level_nap=pile_tip_level_nap,
                pile_head_level_nap=pile_head_level_nap,
                axes=axes[1],
                facecolor=facecolor,
                axis_arg=None,
                show=False,
            )

            x_ticks.add(component.cross_section_bounds[0])
            x_ticks.add(component.cross_section_bounds[1])
            y_ticks.add(component.cross_section_bounds[2])
            y_ticks.add(component.cross_section_bounds[3])
        axes[0].axis("scaled")
        axes[0].set(aspect=1)
        axes[1].axis("auto")
        ax1_aspect = (
            abs(axes[0].axis()[2] - axes[0].axis()[3])
            / abs(axes[1].axis()[2] - axes[1].axis()[3])
            * height_ratio
        )
        axes[1].set(aspect=ax1_aspect)

        axes[0].spines[:].set_visible(False)
        axes[1].spines[:].set_visible(False)

        axes[0].set_xticks(ticks=list(x_ticks))
        axes[0].set_yticks(ticks=list(y_ticks))
        axes[1].set_xticks(ticks=list(x_ticks))
        axes[1].set_yticks(
            ticks=[pile_head_level_nap, pile_tip_level_nap],
            labels=["Pile Head", "Pile Tip"],
        )
        axes[0].tick_params(axis="x", labelrotation=45)
        axes[1].tick_params(axis="x", labelrotation=45)

        if show:
            plt.show()
        return axes
