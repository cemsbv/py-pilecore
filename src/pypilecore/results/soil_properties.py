from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

from ..plot_utils import validate_axes_array
from ..utils import depth_to_nap, nap_to_depth

Number = Union[float, int]

SOIL_COLOR_DIC_intern = {
    "G": "#708090",
    "Z": "#DBAD4B",
    "L": "#0078C1",
    "K": "#578E57",
    "V": "#a76b29",
}

ENG_MAIN_COMPONENT_NAME_DIC = {
    "G": "Gravel",
    "Z": "Sand",
    "L": "Loam",
    "V": "Peat",
    "K": "Clay",
}

SOIL_COLOR_DIC = {
    value: SOIL_COLOR_DIC_intern[key]
    for key, value in ENG_MAIN_COMPONENT_NAME_DIC.items()
}


def get_soil_layer_handles() -> List[Patch]:
    return [Patch(color=clr, label=key) for (key, clr) in SOIL_COLOR_DIC.items()]


class SoilProperties:
    """
    A class for soil properties.
    """

    def __init__(
        self,
        cpt_data: pd.DataFrame | Dict[str, Sequence[float]],
        layer_table: pd.DataFrame | Dict[str, Sequence[float]],
        ref_height: float,
        surface_level_ref: float,
        groundwater_level_ref: float,
        test_id: str | None = None,
    ):
        """
        Parameters
        ----------
        cpt_data: pandas.DataFrame
            DataFrame with CPT data

            Required columns
                depth_nap: number
                    Depth below service level [m]
                qc: number
                    Cone resistance [Mpa]
                qc1: number
                qc2: number
                qc_chamfered: number
                qc_original: number

            Optional columns
                fs: number
                    Sleeve friction resistance [MPa]
        layer_table: pandas.DataFrame
            DataFrame containing the soil-layers and engineering parameters.

            Required columns
                depth_btm: number
                    Depth of the the layer edge (top/bottom) [m] (w.r.t. service level)
                thickness: number
                    Thickness of the layer[m]
                soil_code: str
                    The code used to describe the soil layers of the boreholes. Main components are specified
                    with capital letters and are the following:
                        - G = gravel (Grind)
                        - Z = sand (Zand)
                        - L = loam (Leem)
                        - K = clay (Klei)
                        - V = peat (Veen)
                    Second components are specified with lowercase letter and follow the main component.

                    Example: Vk1 "Peat, slightly clayey" (Veen, zwak kleiig)
                gamma: number
                    Dry unit weight [kN/m^3 or MN/m^3]
                gamma_sat: number
                    Saturated unit weight [kN/m^3 or MN/m^3]
                C_p: number
                    Koppejan consolidation factor C_p [-]
                C_s: number
                    Koppejan consolidation factor C_s [-]
                phi: number
                    Internal friction [degree/rad]

            Examples
                - The layer_table from the gef-model (https://crux-nuclei.com/swagger/gef-model) can be used as input with no
                  need of modifications.
                - Another example can be found in `tests/files/layer_table.csv`
        test_id:
            Identifier of the CPT
        """
        if isinstance(cpt_data, pd.DataFrame):
            self._cpt_data = cpt_data
        else:
            self._cpt_data = pd.DataFrame(cpt_data)
        if "qc_original" in self._cpt_data.columns and "fs" in self._cpt_data.columns:
            self._cpt_data["friction_ratio"] = (
                self._cpt_data["fs"] / self._cpt_data["qc_original"] * 100
            )

        if isinstance(layer_table, pd.DataFrame):
            self._layer_table = layer_table
        else:
            self._layer_table = pd.DataFrame(layer_table)

        self._ref_height = ref_height
        self._test_id = test_id
        self._groundwater_level_ref = groundwater_level_ref
        self._surface_level_ref = surface_level_ref

    @property
    def cpt_data(self) -> pd.DataFrame:
        """
        DataFrame with CPT data

        Always available columns
            depth_nap: number
                Depth below service level [m]
            qc: number
                Cone resistance [Mpa]
            qc1: number
            qc2: number
            qc_chamfered: number
            qc_original: number
        Possibly available columns
            fs: number
        """
        return self._cpt_data

    @property
    def layer_table(self) -> pd.DataFrame:
        """
        DataFrame containing the soil-layers and engineering parameters.

            Always available columns
                depth_btm: number
                    Depth of the the layer edge (top/bottom) [m] (w.r.t. service level)
                thickness: number
                    Thickness of the layer[m]
                soil_code: str
                    The code used to describe the soil layers of the boreholes. Main components are specified
                    with capital letters and are the following:
                        - G = gravel (Grind)
                        - Z = sand (Zand)
                        - L = loam (Leem)
                        - K = clay (Klei)
                        - V = peat (Veen)
                    Second components are specified with lowercase letter and follow the main component.

                    Example: Vk1 "Peat, slightly clayey" (Veen, zwak kleiig)
                gamma: number
                    Dry unit weight [MN/m^3]. If all values > 1.0 we assume [kN/m^3].
                gamma_sat: number
                    Saturated unit weight [MN/m^3]. If all values > 1.0 we assume [kN/m^3].
                C_p: number
                    Koppejan consolidation factor C_p [-]
                C_s: number
                    Koppejan consolidation factor C_s [-]
                phi: number
                    Internal friction [degree/rad]
                index: number
        """
        return self._layer_table

    @property
    def x(self) -> float | None:
        return None

    @property
    def y(self) -> float | None:
        return None

    @property
    def test_id(self) -> str | None:
        return self._test_id

    @property
    def ref_height(self) -> float:
        return self._ref_height

    @property
    def groundwater_level_ref(self) -> float:
        return self._groundwater_level_ref

    @property
    def surface_level_ref(self) -> float:
        return self._surface_level_ref

    def plot_cpt(
        self,
        axes: Optional[Tuple[Optional[plt.Axes], Optional[plt.Axes]]] = None,
        figsize: Tuple[float, float] = (10, 12),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Tuple[Optional[plt.Axes], Optional[plt.Axes]]:
        """
        Plots the CPT data on the provided `plt.Axes`.

        If the "friction_number" is present in the merged-soilproperties, this list
        contains two `Axes` objects: the second one being the twin of the first,
        containing the friction-number plot in the same location (see
        `pyplot.Axes.twiny()`)

        Parameters
        ----------
        axes:
            Optional tuple with two `plt.Axes` objects where the qc-data and Rf-data can
            be plotted on. If not provided, a new `plt.Figure` will be activated and the
            `plt.Axes` objects will be created and returned.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        add_legend:
            Add a legend to the second axes object (default = True).
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes_qc:
            The `Axes` object where the qc-data was plotted on
        axes_rf:
            The `Axes` object where the Rf-data was plotted on.
        """

        # Create or validate axes objects
        if axes is not None:
            validate_axes_array(axes, shape=2)
            ax_qc, ax_rf = axes

        else:
            kwargs_subplot = {
                "figsize": figsize,
                "tight_layout": True,
            }

            kwargs_subplot.update(kwargs)

            _, ax_qc = plt.subplots(
                **kwargs_subplot,
            )
            ax_rf = ax_qc.twiny()

        if ax_qc is not None:
            # Plot horizontal lines
            ax_qc.axhline(
                y=self.groundwater_level_ref,
                color="tab:blue",
                linestyle="--",
                label="Groundwater level",
            )

            ax_qc.axhline(
                y=self.surface_level_ref,
                color="tab:brown",
                linestyle="--",
                label="Surface level",
            )

            # Plot Base qc subplot
            if "qc_chamfered" in self.cpt_data.columns:
                ax_qc.plot(
                    self.cpt_data["qc_chamfered"],
                    self.cpt_data["depth_nap"].to_numpy(),
                    label="$q_{c;a}$",
                    color="orange",
                    linestyle=":",
                )

            if not np.array_equal(
                self.cpt_data["qc"],
                self.cpt_data["qc_original"],
            ):
                ax_qc.plot(
                    self.cpt_data["qc_original"],
                    self.cpt_data["depth_nap"],
                    label="$q_{c;original}$",
                    linestyle="-",
                    color="darkblue",
                )
                ax_qc.plot(
                    self.cpt_data["qc"],
                    self.cpt_data["depth_nap"],
                    label="$q_{c;reduced}$",
                    linestyle="-",
                    color="orange",
                )

            else:
                ax_qc.plot(
                    self.cpt_data["qc"],
                    self.cpt_data["depth_nap"],
                    label="$q_c$",
                    linestyle="-",
                    color="darkblue",
                )

            ax_qc.set_xlim((0, 40))
            ax_qc.set_ylabel("Depth [m NAP]")
            ax_qc.set_xlabel("$q_c$ [MPa]")
            ax_qc.xaxis.label.set_color("darkblue")

            # add grid
            ax_qc.grid()

        if ax_rf is not None:
            # add friction number subplot
            if "friction_ratio" in self.cpt_data.columns:
                ax_rf.plot(
                    self.cpt_data["friction_ratio"],
                    self.cpt_data["depth_nap"],
                    label="Rf",
                    color="darkgray",
                )
                ax_rf.spines["top"].set_position(("outward", 0))
                ax_rf.set_xlabel("Friction ratio [%]")
                ax_rf.xaxis.label.set_color("lightgray")

            ax_rf.set_xlim(0, 20)

        if add_legend:
            ax_qc_legend_handles_list = (
                ax_qc.get_legend_handles_labels()[0] if ax_qc is not None else []
            )

            ax_rf_legend_handles_list = (
                ax_rf.get_legend_handles_labels()[0] if ax_rf is not None else []
            )

            handles_list = [
                *ax_qc_legend_handles_list,
                *ax_rf_legend_handles_list,
            ]

            ax_legend = None
            if ax_qc is not None:
                ax_legend = ax_qc
            elif ax_rf is not None:
                ax_legend = ax_rf

            if ax_legend is not None:
                ax_legend.legend(
                    handles=handles_list,
                    loc="upper left",
                    bbox_to_anchor=(1, 1),
                    title="name: " + self.test_id
                    if self.test_id is not None
                    else "name: unknown",
                )

        return ax_qc, ax_rf

    def plot_layers(
        self,
        axes: Optional[plt.Axes] = None,
        hide_excavated: bool = False,
        figsize: Tuple[float, float] = (3, 10),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> plt.Axes:
        """
        Plots the soil layers on the provided `plt.Axes`.

        Parameters
        ----------
        axes:
            Optional `plt.Axes` object where the soil-layer data can be plotted on. If
            not provided, a new `plt.Figure` will be activated and the `plt.Axes` object
            will be created and returned.
        hide_excavated:
            Hide the layers under the excavation level.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        add_legend:
            Add a legend to the second axes object
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The `Axes` object where the soil layers were plotted on
        """

        # Create axes objects if not provided
        if axes is None:
            kwargs_subplot = {
                "figsize": figsize,
                "tight_layout": True,
            }

            kwargs_subplot.update(kwargs)

            _, axes = plt.subplots(
                **kwargs_subplot,
            )

        elif not isinstance(axes, plt.Axes):
            raise ValueError(
                "'axes' argument to plot_layers() must be a `pyplot.Axes` object or None."
            )

        ax_layers = axes

        # add soil layers subplot
        for depth_btm, delta_z, main_component in zip(
            self.layer_table["depth_btm"],
            self.layer_table["thickness"],
            self.layer_table["soil_code"],
        ):
            if hide_excavated:
                if depth_btm < self.surface_level_ref:
                    continue
                if depth_btm - delta_z < nap_to_depth(
                    self.surface_level_ref, self.ref_height
                ):
                    delta_z = depth_btm - nap_to_depth(
                        self.surface_level_ref, self.ref_height
                    )

            if main_component[0] not in list(SOIL_COLOR_DIC_intern.keys()):
                raise ValueError(
                    "Cannot plot Soil Properties, update SOIL_COLOR_DIC"
                    "to match soil_code of the layer table"
                )
            ax_layers.fill_between(
                [0, 1],
                y1=depth_to_nap(depth_btm, self.ref_height) + delta_z,
                y2=depth_to_nap(depth_btm, self.ref_height),
                color=SOIL_COLOR_DIC_intern[main_component[0]],
            )
        ax_layers.get_xaxis().set_visible(False)

        if add_legend:
            ax_layers.legend(
                handles=get_soil_layer_handles(),
                loc="upper left",
                bbox_to_anchor=(1, 1),
                title="name: " + self.test_id
                if self.test_id is not None
                else "name: unknown",
            )

        return ax_layers

    def plot_overview(
        self,
        axes: Optional[
            Tuple[Optional[plt.Axes], Optional[plt.Axes], Optional[plt.Axes]]
        ] = None,
        figsize: Tuple[float, float] = (10.0, 12.0),
        width_ratios: Tuple[float, float] = (1.0, 0.1),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Tuple[Optional[plt.Axes], Optional[plt.Axes], Optional[plt.Axes]]:
        """
        Plots the CPT and soil table data on the provided axes.

        Parameters
        ----------
        axes:
            Optional tuple with three `plt.Axes` objects where the qc-data, Rf-data and
            soil-layer data can be plotted on. If not provided, a new `plt.Figure` will
            be activated and the`plt.Axes` objects will be created and returned.
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
        axes_qc:
            The `Axes` object where the qc-data was plotted on
        axes_rf:
            The `Axes` object where the Rf-data was plotted on.
        axes_layers:
            The `Axes` object where the soil-layers were plotted on.
        """

        # Create or validate axes objects
        if axes is not None:
            validate_axes_array(axes, shape=3)
            ax_qc, ax_rf, ax_layers = axes

        else:
            kwargs_subplot = {
                "gridspec_kw": {"width_ratios": width_ratios},
                "sharey": "row",
                "figsize": figsize,
                "tight_layout": True,
            }

            kwargs_subplot.update(kwargs)

            _, axes_new = plt.subplots(
                1,
                2,
                **kwargs_subplot,
            )

            ax_qc, ax_layers = axes_new
            ax_rf = ax_qc.twiny()

        # Plot the cpt data
        self.plot_cpt(axes=(ax_qc, ax_rf), add_legend=False)

        if ax_layers is not None:
            # Plot the soil layers
            self.plot_layers(axes=ax_layers, add_legend=False)

        # Add a legend if required
        if add_legend:
            ax_qc_legend_handles_list = (
                ax_qc.get_legend_handles_labels()[0] if ax_qc is not None else []
            )

            ax_rf_legend_handles_list = (
                ax_rf.get_legend_handles_labels()[0] if ax_rf is not None else []
            )

            soil_layer_legend_handles_list = (
                get_soil_layer_handles() if ax_layers is not None else []
            )

            handles_list = [
                *ax_qc_legend_handles_list,
                *ax_rf_legend_handles_list,
                *soil_layer_legend_handles_list,
            ]

            ax_legend = None
            if ax_layers is not None:
                ax_legend = ax_layers
            elif ax_qc is not None:
                ax_legend = ax_qc
            elif ax_rf is not None:
                ax_legend = ax_rf

            if ax_legend is not None:
                ax_legend.legend(
                    handles=handles_list,
                    loc="upper left",
                    bbox_to_anchor=(1, 1),
                    title="name: " + self.test_id
                    if self.test_id is not None
                    else "name: unknown",
                )

        return (ax_qc, ax_rf, ax_layers)
