from __future__ import annotations

from functools import lru_cache
from typing import Any, List, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from numpy.typing import NDArray

from pypilecore.utils import depth_to_nap, nap_to_depth

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


class LayerTable:
    """
    Object that contains the Soil-layer data-traces.
    """

    def __init__(
        self,
        index: Sequence[int],
        thickness: Sequence[float],
        depth_btm: Sequence[float],
        C_s: Sequence[float] | None,
        C_p: Sequence[float] | None,
        gamma: Sequence[float],
        gamma_sat: Sequence[float],
        phi: Sequence[float],
        soil_code: Sequence[str],
    ):
        self.index = np.array(index).astype(np.float64)
        """Layer index"""
        self.thickness = np.array(thickness).astype(np.float64)
        """The layer thickness [m]"""
        self.depth_btm = np.array(depth_btm).astype(np.float64)
        """The depth of the layer bottom (below service level) [m]."""
        self.C_s = np.array(C_s).astype(np.float64)
        """Koppejan parameters for secondary compression."""
        self.C_p = np.array(C_p).astype(np.float64)
        """Koppejan parameters for primary compression."""
        self.gamma = np.array(gamma).astype(np.float64)
        """The dry unit weights [MPa]."""
        self.gamma_sat = np.array(gamma_sat).astype(np.float64)
        """The saturated unit weights [MPa]."""
        self.phi = np.array(phi).astype(np.float64)
        """Internal friction angle. [rad]"""
        self.soil_code = np.array(soil_code).astype(np.str_)
        """
        The code used to describe the soil layers of the boreholes. Main components are
        specified with capital letters and are the following:

            - G: gravel (Grind)
            - Z: sand (Zand)
            - L: loam (Leem)
            - K: clay (Klei)
            - V: peat (Veen)
        """

        dict_lengths = {}
        for key, value in self.__dict__.items():
            if not np.all(pd.isnull(value)):
                dict_lengths[key] = len(value)
        if len(set(dict_lengths.values())) > 1:
            raise ValueError(
                f"Inputs for LayerTable must have same lengths, but got lengths: {dict_lengths}"
            )

        self.__dict__.update({"depth_top": self.depth_top})

    @classmethod
    def from_api_response(cls, layer_table_dict: dict) -> "LayerTable":
        """
        Instantiates the LayerTable object from the "layer_table" object, which is returned in
        the response of a "compression/multiple-cpts/results" endpoint call.
        """
        return cls(
            index=layer_table_dict["index"],
            thickness=layer_table_dict["thickness"],
            depth_btm=layer_table_dict["depth_btm"],
            C_s=layer_table_dict.get("C_s"),
            C_p=layer_table_dict.get("C_p"),
            gamma=layer_table_dict["gamma"],
            gamma_sat=layer_table_dict["gamma_sat"],
            phi=layer_table_dict["phi"],
            soil_code=layer_table_dict["soil_code"],
        )

    @property
    def depth_top(self) -> NDArray[np.float64]:
        return self.depth_btm - self.thickness

    @lru_cache
    def to_pandas(self) -> pd.DataFrame:
        """The pandas.DataFrame representation"""
        return pd.DataFrame(self.__dict__).dropna(axis=0, how="all")


class CPTTable:
    """
    Object that contains the CPT-related data-traces of a bearing calculation. These
    can be either raw input data, corrected data or intermediate results.
    """

    def __init__(
        self,
        depth_nap: Sequence[float] | None,
        qc: Sequence[float] | None,
        qc_original: Sequence[float] | None,
        qc_chamfered: Sequence[float] | None,
        qc1: Sequence[float] | None,
        qc2: Sequence[float] | None,
        fs: Sequence[float] | None,
    ):
        if depth_nap is None:
            self.depth_nap = np.array([depth_nap]).astype(np.float64)
        else:
            self.depth_nap = np.array(depth_nap).astype(np.float64).round(decimals=2)

        """The depth [m] w.r.t. NAP"""
        self.qc = np.array(qc).astype(np.float64)
        """The cone resistance signal from the CPT [MPa], possibly corrected for excavation
        or OCR."""
        self.qc_original = np.array(qc_original).astype(np.float64)
        """The original cone resistance signal from the CPT [MPa]."""
        self.qc_chamfered = np.array(qc_chamfered).astype(np.float64)
        """The chamfered-qc signal, used for the positive friction range [MPa]."""
        self.qc1 = np.array(qc1).astype(np.float64)
        """The Koppejan-qc1 trajectory [MPa]."""
        self.qc2 = np.array(qc2).astype(np.float64)
        """The Koppejan-qc2 trajectory [MPa]."""
        self.fs = np.array(fs).astype(np.float64)
        """The original fs signal from the CPT [MPa]."""

        dict_lengths = {}
        for key, value in self.__dict__.items():
            if not np.all(np.isnan(value)):
                dict_lengths[key] = len(value)
        if len(set(dict_lengths.values())) > 1:
            raise ValueError(
                f"Inputs for CPTTable must have same lengths, but got lengths: {dict_lengths}"
            )

        self.__dict__.update({"friction_ratio": self.friction_ratio})

    @classmethod
    def from_api_response(cls, cpt_chart_dict: dict) -> "CPTTable":
        """
        Instantiates the CPTTable object from the "cpt_chart" object, which is returned in
        the response of a "compression/multiple-cpts/results" endpoint call.
        """
        return cls(
            depth_nap=cpt_chart_dict.get("depth_nap"),
            qc=cpt_chart_dict.get("qc"),
            qc_original=cpt_chart_dict.get("qc_original"),
            qc_chamfered=cpt_chart_dict.get("qc_chamfered"),
            qc1=cpt_chart_dict.get("qc1"),
            qc2=cpt_chart_dict.get("qc2"),
            fs=cpt_chart_dict.get("fs"),
        )

    @property
    def friction_ratio(self) -> NDArray[np.float64]:
        return np.array(self.fs / self.qc * 100)

    @property
    def qc_has_been_chamfered(self) -> bool:
        """Returns False if `qc_chamfered` contains the same data as `qc`."""
        return not np.allclose(self.qc, self.qc_chamfered)

    @property
    def qc_has_been_reduced(self) -> bool:
        """Returns False if `qc` contains the same data as `qc_original`."""
        return not np.allclose(self.qc_original, self.qc)

    @lru_cache
    def to_pandas(self) -> pd.DataFrame:
        """The pandas.DataFrame representation"""
        return pd.DataFrame(self.__dict__).dropna(axis=0, how="all")

    def plot_qc(
        self,
        axes: Axes | None = None,
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plots the qc data on the provided `Axes`.

        Parameters
        ----------
        axes:
            Optional Axes to plot on.
        add_legend:
            Add a legend (default = True).
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The matplotlib Axes object
        """

        if axes is not None:
            if not isinstance(axes, Axes):
                raise TypeError(
                    f"`axes` input for CPTTable.plot_qc() should be a `matplotlib.axes.Axes` object or None, but got: {type(axes)}."
                )
        else:
            kwargs_subplot = {
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

        if np.all(np.isnan(self.qc)):
            qc = np.ones_like(self.depth_nap) * np.nan
        else:
            qc = self.qc

        # Plot Base qc subplot
        if self.qc_has_been_chamfered is True:
            axes.plot(
                self.qc_chamfered,
                self.depth_nap,
                label="$q_{c;a}$",
                color="orange",
                linestyle=":",
            )

        if self.qc_has_been_reduced is True:
            axes.plot(
                self.qc_original,
                self.depth_nap,
                label="$q_{c;original}$",
                linestyle="-",
                color="darkblue",
            )
            axes.plot(
                qc,
                self.depth_nap,
                label="$q_{c;reduced}$",
                linestyle="-",
                color="orange",
            )

        else:
            axes.plot(
                qc,
                self.depth_nap,
                label="$q_c$",
                linestyle="-",
                color="darkblue",
            )

        axes.set_xlim((0, 40))
        axes.set_ylabel("Depth [m NAP]")
        axes.set_xlabel("$q_c$ [MPa]")
        axes.xaxis.label.set_color("darkblue")

        # add grid
        axes.grid()

        if add_legend:
            axes.legend(
                loc="upper left",
                bbox_to_anchor=(1, 1),
            )

        return axes

    def plot_friction_ratio(
        self,
        axes: Axes | None = None,
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plots the friction-ratio data on the provided `Axes`.

        Parameters
        ----------
        axes:
            Optional Axes to plot on.
        add_legend:
            Add a legend (default = True).
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The matplotlib Axes object
        """

        if axes is not None:
            if not isinstance(axes, Axes):
                raise TypeError(
                    f"`axes` input for CPTTable.plot_rf() should be a `matplotlib.axes.Axes` object or None, but got: {type(axes)}."
                )
        else:
            kwargs_subplot = {
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

        if np.all(np.isnan(self.friction_ratio)):
            friction_ratio = np.ones_like(self.depth_nap) * np.nan
        else:
            friction_ratio = self.friction_ratio

        # add friction number subplot
        axes.plot(
            friction_ratio,
            self.depth_nap,
            label="Rf",
            color="darkgray",
        )
        axes.spines["top"].set_position(("outward", 0))
        axes.set_xlabel("Friction ratio [%]")
        axes.xaxis.label.set_color("lightgray")

        axes.set_xlim(0, 20)

        if add_legend:
            axes.legend(
                loc="upper left",
                bbox_to_anchor=(1, 1),
            )

        return axes


class SoilProperties:
    """
    A class for soil properties.
    """

    def __init__(
        self,
        cpt_table: CPTTable,
        layer_table: LayerTable,
        ref_height: float,
        surface_level_ref: float,
        groundwater_level_ref: float,
        test_id: str | None = None,
        x: float | None = None,
        y: float | None = None,
    ):
        """
        Parameters
        ----------
        cpt_table:
            The CPTTable object
        layer_table:
            The LayerTable object.
        ref_height:
            The vertical reference [m].
        surface_level_ref:
            The elevation of the surface w.r.t. the vertical reference [m]. This could
            be the level post-excavation.
        groundwater_level_ref:
            The elevation of the groundwater w.r.t. the vertical reference [m].
        test_id:
            Identifier of the CPT
        x:
            x coordinate of CPT
        y:
            y coordinate of CPT
        """
        self._cpt_table = cpt_table
        self._layer_table = layer_table
        self._ref_height = ref_height
        self._test_id = test_id
        self._groundwater_level_ref = groundwater_level_ref
        self._surface_level_ref = surface_level_ref
        self._x = x
        self._y = y

    @property
    def cpt_table(self) -> CPTTable:
        """The CPTTable object"""
        return self._cpt_table

    @property
    def layer_table(self) -> LayerTable:
        """The LayerTable object"""
        return self._layer_table

    @property
    def x(self) -> float | None:
        """x-coordinate of the CPT"""
        return self._x

    @property
    def y(self) -> float | None:
        """y-coordinate of the CPT"""
        return self._y

    @property
    def test_id(self) -> str | None:
        """Identifier of the CPT"""
        return self._test_id

    @property
    def ref_height(self) -> float:
        """The vertical reference [m]."""
        return self._ref_height

    @property
    def groundwater_level_ref(self) -> float:
        """The elevation of the groundwater w.r.t. the vertical reference [m]."""
        return self._groundwater_level_ref

    @property
    def surface_level_ref(self) -> float:
        """The elevation of the surface w.r.t. the vertical reference [m]. This could
        be the level post-excavation."""
        return self._surface_level_ref

    def plot_layers(
        self,
        axes: Axes | None = None,
        hide_excavated: bool = False,
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plots the soil layers on the provided `Axes`.

        Parameters
        ----------
        axes:
            Optional `Axes` object where the soil-layer data can be plotted on. If
            not provided, a new `plt.Figure` will be activated and the `Axes` object
            will be created and returned.
        hide_excavated:
            Hide the layers under the excavation level.
        add_legend:
            Add a legend to the axes object
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The `Axes` object where the soil layers were plotted on
        """
        if axes is not None:
            if not isinstance(axes, Axes):
                raise TypeError(
                    f"`axes` input for CPTTable.plot_qc() should be a `matplotlib.axes.Axes` object or None, but got: {type(axes)}."
                )
        else:
            kwargs_subplot = {
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

        # add soil layers subplot
        for depth_btm, delta_z, main_component in zip(
            self.layer_table.depth_btm,
            self.layer_table.thickness,
            self.layer_table.soil_code,
        ):
            if hide_excavated:
                if depth_btm < nap_to_depth(self.surface_level_ref, self.ref_height):
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
            axes.fill_between(
                [0, 1],
                y1=depth_to_nap(depth_btm, self.ref_height) + delta_z,
                y2=depth_to_nap(depth_btm, self.ref_height),
                color=SOIL_COLOR_DIC_intern[main_component[0]],
            )
        axes.get_xaxis().set_visible(False)

        if add_legend:
            axes.legend(
                handles=get_soil_layer_handles(),
                loc="upper left",
                bbox_to_anchor=(1, 1),
                title="name: " + self.test_id
                if self.test_id is not None
                else "name: unknown",
            )

        return axes

    def plot(
        self,
        figsize: Tuple[float, float] = (10.0, 12.0),
        width_ratios: Tuple[float, float] = (1.0, 0.1),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Figure:
        """
        Plots the CPT and soil table data.

        Parameters
        ----------
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
            2,
            **kwargs_subplot,
        )

        ax_qc, ax_layers = fig.axes

        ax_rf = ax_qc.twiny()
        assert isinstance(ax_rf, Axes)

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

        self.cpt_table.plot_qc(ax_qc, add_legend=False)
        self.cpt_table.plot_friction_ratio(ax_rf, add_legend=False)
        self.plot_layers(axes=ax_layers, add_legend=False)

        if add_legend:
            ax_qc_legend_handles_list = ax_qc.get_legend_handles_labels()[0]

            ax_rf_legend_handles_list = ax_rf.get_legend_handles_labels()[0]

            handles_list = [
                *ax_qc_legend_handles_list,
                *ax_rf_legend_handles_list,
            ]

            ax_qc.legend(
                handles=handles_list,
                loc="upper left",
                bbox_to_anchor=(1, 1),
                title="name: " + self.test_id
                if self.test_id is not None
                else "name: unknown",
            )

        # Add a legend if required
        if add_legend:
            ax_qc_legend_handles_list = ax_qc.get_legend_handles_labels()[0]

            ax_rf_legend_handles_list = ax_rf.get_legend_handles_labels()[0]

            soil_layer_legend_handles_list = get_soil_layer_handles()

            handles_list = [
                *ax_qc_legend_handles_list,
                *ax_rf_legend_handles_list,
                *soil_layer_legend_handles_list,
            ]

            ax_layers.legend(
                handles=handles_list,
                loc="upper left",
                bbox_to_anchor=(1, 1),
                title="name: " + self.test_id
                if self.test_id is not None
                else "name: unknown",
            )

        return fig
