from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from pypilecore.common.piles import PileGridProperties
from pypilecore.results.soil_properties import (
    CPTTable,
    LayerTable,
    SoilProperties,
    get_soil_layer_handles,
)

Number = Union[float, int]


@dataclass(frozen=True)
class CPTTensionResultsTable:
    """Object containing the results of a single CPT."""

    pile_tip_level_nap: NDArray[np.float64]
    """The pile-tip level in [m] w.r.t. the reference."""
    A: NDArray[np.float64]
    """The area of influence of the pile, that is, the area over which
            the stress spreads around a pile within a pile group [m2]."""
    R_t_d_plug: NDArray[np.float64]
    """The root ball weight, excluding the weight of the pile (7.6.3.3 (h) NEN
            9997-1+C2:2017) [kN]."""
    R_t_d: NDArray[np.float64]
    """The design value of the tensile resistance of a pile or pile group
            (7.6.3.3 (a) NEN 9997-1+C2:2017) [kN]."""
    R_t_k: NDArray[np.float64]
    """The characteristic value of the tensile resistance of a pile or pile
            group (7.6.3.3 NEN 9997-1+C2:2017) [kN]."""
    R_t_mob_ratio: NDArray[np.float64]
    """The mobilisation ratio of the shaft bearing capacity [-]."""
    R_t_mob: NDArray[np.float64]
    """The mobilisation of the shaft bearing capacity [kN]."""
    k_v_b: NDArray[np.float64]
    """The 1-dimensional stiffness modulus at pile bottom [kN/mm]."""
    k_v_1: NDArray[np.float64]
    """The 1-dimensional stiffness modulus at pile head [MN/mm]."""
    q_s_max_mean: NDArray[np.float64]
    """The computational value of shaft friction [MPa]."""
    s_e: NDArray[np.float64]
    """The elastic shortening of the pile [mm]."""
    s_b: NDArray[np.float64]
    """The settlement of the pile bottom [mm]."""
    s_1: NDArray[np.float64]
    """The settlement of the pile [mm]."""
    sand_clay_ratio: NDArray[np.float64]
    """Contributions to the bearing capacity from sandy layers [-]."""

    def __post_init__(self) -> None:
        dict_lengths = {}
        for key, value in self.__dict__.items():
            if not np.all(np.isnan(value)):
                dict_lengths[key] = len(value)
        if len(set(dict_lengths.values())) > 1:
            raise ValueError(
                f"Inputs for LayerTable must have same lengths, but got lengths: {dict_lengths}"
            )

    @classmethod
    def from_sequences(
        cls,
        pile_tip_level_nap: Sequence[Number],
        A: Sequence[Number],
        R_t_d_plug: Sequence[Number],
        R_t_d: Sequence[Number],
        R_t_k: Sequence[Number],
        R_t_mob_ratio: Sequence[Number],
        R_t_mob: Sequence[Number],
        k_v_b: Sequence[Number],
        k_v_1: Sequence[Number],
        q_s_max_mean: Sequence[Number],
        s_e: Sequence[Number],
        s_b: Sequence[Number],
        s_1: Sequence[Number],
        sand_clay_ratio: Sequence[Number],
    ) -> CPTTensionResultsTable:
        return cls(
            pile_tip_level_nap=np.array(pile_tip_level_nap).astype(np.float64),
            A=np.array(A).astype(np.float64),
            R_t_d_plug=np.array(R_t_d_plug).astype(np.float64),
            R_t_d=np.array(R_t_d).astype(np.float64),
            R_t_k=np.array(R_t_k).astype(np.float64),
            R_t_mob_ratio=np.array(R_t_mob_ratio).astype(np.float64),
            R_t_mob=np.array(R_t_mob).astype(np.float64),
            k_v_b=np.array(k_v_b).astype(np.float64),
            k_v_1=np.array(k_v_1).astype(np.float64),
            q_s_max_mean=np.array(q_s_max_mean).astype(np.float64),
            s_e=np.array(s_e).astype(np.float64),
            s_b=np.array(s_b).astype(np.float64),
            s_1=np.array(s_1).astype(np.float64),
            sand_clay_ratio=np.array(sand_clay_ratio).astype(np.float64),
        )

    def to_pandas(self) -> pd.DataFrame:
        """Get the pandas.DataFrame representation"""
        return pd.DataFrame(self.__dict__).dropna(axis=0, how="all")


class SingleCPTTensionBearingResults:
    """
    Object that contains the results of a PileCore single-cpt calculation.

    *Not meant to be instantiated by the user.*
    """

    def __init__(
        self,
        soil_properties: SoilProperties,
        pile_head_level_nap: float,
        results_table: CPTTensionResultsTable,
        pile_grid_properties: PileGridProperties,
    ) -> None:
        """
        Parameters
        ----------
        soil_properties
            The object with soil properties
        pile_head_level_nap
            The elevation of the pile-head, in [m] w.r.t. NAP.
        results_table
            The object with CPT results.
        """
        self._sp = soil_properties
        self._pile_head_level_nap = pile_head_level_nap
        self._results_table = results_table
        self._pile_grid_properties = pile_grid_properties

    @classmethod
    def from_api_response(
        cls,
        cpt_results_dict: dict,
        ref_height: float,
        surface_level_ref: float,
        x: float | None = None,
        y: float | None = None,
    ) -> "SingleCPTTensionBearingResults":
        results_table = cpt_results_dict["results_table"]
        return cls(
            soil_properties=SoilProperties(
                cpt_table=CPTTable.from_api_response(
                    cpt_results_dict.get("cpt_chart", {})
                ),
                layer_table=LayerTable.from_api_response(
                    cpt_results_dict["layer_table"]
                ),
                test_id=cpt_results_dict.get("test_id"),
                ref_height=ref_height,
                surface_level_ref=surface_level_ref,
                groundwater_level_ref=cpt_results_dict["groundwater_level_nap"],
                x=x,
                y=y,
            ),
            pile_head_level_nap=cpt_results_dict["pile_head_level_nap"],
            results_table=CPTTensionResultsTable.from_sequences(
                pile_tip_level_nap=results_table["pile_tip_level_nap"],
                k_v_b=results_table["k_v_b"],
                k_v_1=results_table["k_v_1"],
                A=results_table["A"],
                R_t_d_plug=results_table["R_t_d_plug"],
                R_t_d=results_table["R_t_d"],
                R_t_k=results_table["R_t_k"],
                R_t_mob_ratio=results_table["R_s_mob_ratio"],
                R_t_mob=results_table["R_s_mob"],
                q_s_max_mean=results_table["q_s_max_mean"],
                s_e=results_table["s_e"],
                s_b=results_table["s_b"],
                s_1=results_table["s_1"],
                sand_clay_ratio=results_table["sand_clay_ratio"],
            ),
            pile_grid_properties=PileGridProperties.from_api_response(
                cpt_results_dict["pile_grid"]
            ),
        )

    @property
    def soil_properties(self) -> SoilProperties:
        """
        The SoilProperties object.
        """
        return self._sp

    @property
    def pile_grid_properties(self) -> PileGridProperties:
        """
        The PileGridProperties object.
        """
        return self._pile_grid_properties

    @property
    def pile_head_level_nap(self) -> float:
        """
        The elevation of the pile-head in [m] w.r.t. NAP.
        """
        return self._pile_head_level_nap

    @property
    def table(self) -> CPTTensionResultsTable:
        """The object with single-CPT results table traces."""
        return self._results_table

    def plot_bearing_capacities(
        self,
        axes: Optional[Axes] = None,
        figsize: Tuple[float, float] = (8, 10),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plot the bearing calculation results on an `Axes' object.

        Parameters
        ----------
        axes:
            Optional `Axes` object where the bearing capacities can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `Axes`
            object will be created and returned.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        add_legend:
            Add a legend to the second axes object
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The `Axes` object where the bearing capacities were plotted on.
        """

        # Create axes objects if not provided
        if axes is not None:
            if not isinstance(axes, Axes):
                raise ValueError(
                    "'axes' argument to plot_bearing_capacities() must be a `pyplot.axes.Axes` object or None."
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

        # add horizontal lines
        axes.axhline(
            y=self.soil_properties.groundwater_level_ref,
            color="tab:blue",
            linestyle="--",
            label="Groundwater level",
        )
        axes.axhline(
            y=self.soil_properties.surface_level_ref,
            color="tab:brown",
            linestyle="--",
            label="Surface level",
        )

        # add bearing result subplot
        axes.plot(
            np.array(self.table.R_t_d),
            self.table.pile_tip_level_nap,
            color="tab:orange",
            label=r"$R_{t;d}$",
        )
        axes.plot(
            np.array(self.table.R_t_d_plug),
            self.table.pile_tip_level_nap,
            label=r"$R_{t;d;kluit}$",
            lw=3,
            color="tab:blue",
        )
        axes.set_xlabel("Force [kN]")
        axes.set_xlim(
            np.floor(np.nanmin(np.array(self.table.R_t_d) / 10.0)) * 10,
            np.ceil(np.nanmax(np.array(self.table.R_t_d) / 10.0)) * 10,
        )

        # add legend
        if add_legend:
            axes.legend(
                loc="upper left",
                bbox_to_anchor=(1, 1),
            )

        # set grid
        axes.grid()

        return axes

    def plot_bearing_overview(
        self,
        figsize: Tuple[float, float] = (10.0, 12.0),
        width_ratios: Tuple[float, float, float] = (1, 0.1, 2),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Figure:
        """
        Plot an overview of the bearing-capacities, including the .

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
            3,
            **kwargs_subplot,
        )

        ax_qc, ax_layers, ax_bearing = fig.axes
        ax_rf = ax_qc.twiny()
        assert isinstance(ax_rf, Axes)

        # Plot bearing capacities
        self.soil_properties.cpt_table.plot_qc(ax_qc, add_legend=False)
        bounds = ax_qc.get_ylim()
        self.soil_properties.cpt_table.plot_friction_ratio(ax_rf, add_legend=False)
        self.soil_properties.plot_layers(ax_layers, add_legend=False)
        ax_layers.set_ylim(bounds)

        self.plot_bearing_capacities(axes=ax_bearing, add_legend=False)

        if add_legend:
            ax_qc_legend_handles_list = ax_qc.get_legend_handles_labels()[0]
            ax_rf_legend_handles_list = ax_rf.get_legend_handles_labels()[0]
            ax_layers_legend_handles_list = get_soil_layer_handles()

            # Omit last 2 duplicate "bearing" handles
            # (groundwater_level and surface_level):
            ax_bearing_legend_handles_list = ax_bearing.get_legend_handles_labels()[0][
                2:
            ]

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
                title=(
                    "name: " + self.soil_properties.test_id
                    if self.soil_properties.test_id is not None
                    else "name: unknown"
                ),
            )

        return fig
