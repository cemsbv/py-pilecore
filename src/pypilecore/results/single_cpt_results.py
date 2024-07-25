from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from pypilecore.results.soil_properties import (
    CPTTable,
    LayerTable,
    SoilProperties,
    get_soil_layer_handles,
)

Number = Union[float, int]


@dataclass(frozen=True)
class CPTResultsTable:
    """Object containing the results of a single CPT."""

    pile_tip_level_nap: NDArray[np.float64]
    """The pile-tip level in [m] w.r.t. the reference."""
    F_nk_cal: NDArray[np.float64]
    """The calculated value of the negative shaft friction force [kN]."""
    F_nk_k: NDArray[np.float64]
    """The characteristic value of the negative shaft friction force [kN]."""
    F_nk_d: NDArray[np.float64]
    """The design value of the negative shaft friction force [kN]."""
    R_b_cal: NDArray[np.float64]
    """The calculated value of the bottom bearingcapacity [kN]."""
    R_b_k: NDArray[np.float64]
    """The characteristic value of the bottom bearingcapacity [kN]."""
    R_b_d: NDArray[np.float64]
    """The design value of the bottom bearingcapacity [kN]."""
    R_s_cal: NDArray[np.float64]
    """The calculated value of the shaft bearingcapacity [kN]."""
    R_s_k: NDArray[np.float64]
    """The characteristic value of the shaft bearingcapacity [kN]."""
    R_s_d: NDArray[np.float64]
    """The design value of the shaft bearingcapacity [kN]."""
    R_c_cal: NDArray[np.float64]
    """The calculated value of the total compressive bearingcapacity [kN]."""
    R_c_k: NDArray[np.float64]
    """The characteristic value of the total compressive bearingcapacity [kN]."""
    R_c_d: NDArray[np.float64]
    """The design value of the total compressive bearingcapacity [kN]."""
    R_c_d_net: NDArray[np.float64]
    """The net design value of the total bearingcapacity [kN] (netto =excluding design negative friction force.)."""
    F_c_k: NDArray[np.float64]
    """The compressive force on the pile-head [kN]."""
    F_c_k_tot: NDArray[np.float64]
    """The characteristic value of the total compressive pile load [kN](building-load + neg. friction force)."""
    negative_friction_range_nap_top: NDArray[np.float64]
    """The top boundary of the negative friction interval [m] w.r.t. NAP.
    Can be None when the friction force was provided directly."""
    negative_friction_range_nap_btm: NDArray[np.float64]
    """The bottom boundary of the negative friction interval [m] w.r.t. NAP.
    Can be None when the friction force was provided directly."""
    positive_friction_range_nap_top: NDArray[np.float64]
    """The top boundary of the positive friction interval [m] w.r.t. NAP."""
    positive_friction_range_nap_btm: NDArray[np.float64]
    """The bottom boundary of the positive friction interval [m] w.r.t. NAP."""
    q_b_max: NDArray[np.float64]
    """The maximum bottom bearing resistance [MPa]."""
    q_s_max_mean: NDArray[np.float64]
    """The maximum shaft bearing resistance [MPa]."""
    qc1: NDArray[np.float64]
    """The average friction resistance in Koppejan trajectory I, :math:`q_{c;I;gem}` [MPa] ."""
    qc2: NDArray[np.float64]
    """The average friction resistance in Koppejan trajectory II, :math:`q_{c;II;gem}` [MPa] ."""
    qc3: NDArray[np.float64]
    """The average friction resistance in Koppejan trajectory III, :math:`q_{c;III;gem}` [MPa] ."""
    s_b: NDArray[np.float64]
    """The settlement of the pile bottom [mm]."""
    s_el: NDArray[np.float64]
    """The elastic shortening of the pile due to elastic strain [mm]."""
    k_v_b: NDArray[np.float64]
    """The 1-dimensional stiffness modulus at pile bottom [kN/m]."""
    k_v_1: NDArray[np.float64]
    """The 1-dimensional stiffness modulus at pile head [MN/mm]."""

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
        F_nk_cal: Sequence[Number],
        F_nk_k: Sequence[Number],
        F_nk_d: Sequence[Number],
        R_b_cal: Sequence[Number],
        R_b_k: Sequence[Number],
        R_b_d: Sequence[Number],
        R_s_cal: Sequence[Number],
        R_s_k: Sequence[Number],
        R_s_d: Sequence[Number],
        R_c_cal: Sequence[Number],
        R_c_k: Sequence[Number],
        R_c_d: Sequence[Number],
        R_c_d_net: Sequence[Number],
        F_c_k: Sequence[Number],
        F_c_k_tot: Sequence[Number],
        negative_friction_range_nap_top: Sequence[Number],
        negative_friction_range_nap_btm: Sequence[Number],
        positive_friction_range_nap_top: Sequence[Number],
        positive_friction_range_nap_btm: Sequence[Number],
        q_b_max: Sequence[Number],
        q_s_max_mean: Sequence[Number],
        qc1: Sequence[Number],
        qc2: Sequence[Number],
        qc3: Sequence[Number],
        s_b: Sequence[Number],
        s_el: Sequence[Number],
        k_v_b: Sequence[Number],
        k_v_1: Sequence[Number],
    ) -> CPTResultsTable:
        return cls(
            pile_tip_level_nap=np.array(pile_tip_level_nap).astype(np.float64),
            F_nk_cal=np.array(F_nk_cal).astype(np.float64),
            F_nk_k=np.array(F_nk_k).astype(np.float64),
            F_nk_d=np.array(F_nk_d).astype(np.float64),
            R_b_cal=np.array(R_b_cal).astype(np.float64),
            R_b_k=np.array(R_b_k).astype(np.float64),
            R_b_d=np.array(R_b_d).astype(np.float64),
            R_s_cal=np.array(R_s_cal).astype(np.float64),
            R_s_k=np.array(R_s_k).astype(np.float64),
            R_s_d=np.array(R_s_d).astype(np.float64),
            R_c_cal=np.array(R_c_cal).astype(np.float64),
            R_c_k=np.array(R_c_k).astype(np.float64),
            R_c_d=np.array(R_c_d).astype(np.float64),
            R_c_d_net=np.array(R_c_d_net).astype(np.float64),
            F_c_k=np.array(F_c_k).astype(np.float64),
            F_c_k_tot=np.array(F_c_k_tot).astype(np.float64),
            negative_friction_range_nap_top=np.array(
                negative_friction_range_nap_top
            ).astype(np.float64),
            negative_friction_range_nap_btm=np.array(
                negative_friction_range_nap_btm
            ).astype(np.float64),
            positive_friction_range_nap_top=np.array(
                positive_friction_range_nap_top
            ).astype(np.float64),
            positive_friction_range_nap_btm=np.array(
                positive_friction_range_nap_btm
            ).astype(np.float64),
            q_b_max=np.array(q_b_max).astype(np.float64),
            q_s_max_mean=np.array(q_s_max_mean).astype(np.float64),
            qc1=np.array(qc1).astype(np.float64),
            qc2=np.array(qc2).astype(np.float64),
            qc3=np.array(qc3).astype(np.float64),
            s_b=np.array(s_b).astype(np.float64),
            s_el=np.array(s_el).astype(np.float64),
            k_v_b=np.array(k_v_b).astype(np.float64),
            k_v_1=np.array(k_v_1).astype(np.float64),
        )

    def to_pandas(self) -> pd.DataFrame:
        """Get the pandas.DataFrame representation"""
        return pd.DataFrame(self.__dict__).dropna(axis=0, how="all")


class SingleCPTBearingResults:
    """
    Object that contains the results of a PileCore single-cpt calculation.

    *Not meant to be instantiated by the user.*
    """

    def __init__(
        self,
        soil_properties: SoilProperties,
        pile_head_level_nap: float,
        results_table: CPTResultsTable,
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

    @classmethod
    def from_api_response(
        cls,
        cpt_results_dict: dict,
        ref_height: float,
        surface_level_ref: float,
        x: float | None = None,
        y: float | None = None,
    ) -> "SingleCPTBearingResults":
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
            pile_head_level_nap=cpt_results_dict["annotations"]["pile_head_level_nap"],
            results_table=CPTResultsTable.from_sequences(
                pile_tip_level_nap=results_table["pile_tip_level_nap"],
                F_nk_cal=results_table["F_nk_cal"],
                F_nk_k=results_table["F_nk_k"],
                F_nk_d=results_table["F_nk_d"],
                R_b_cal=results_table["R_b_cal"],
                R_b_k=results_table["R_b_k"],
                R_b_d=results_table["R_b_d"],
                R_s_cal=results_table["R_s_cal"],
                R_s_k=results_table["R_s_k"],
                R_s_d=results_table["R_s_d"],
                R_c_cal=results_table["R_c_cal"],
                R_c_k=results_table["R_c_k"],
                R_c_d=results_table["R_c_d"],
                R_c_d_net=results_table["R_c_d_net"],
                F_c_k=results_table["F_c_k"],
                F_c_k_tot=results_table["F_c_k_tot"],
                negative_friction_range_nap_top=results_table[
                    "negative_friction_range_nap_top"
                ],
                negative_friction_range_nap_btm=results_table[
                    "negative_friction_range_nap_btm"
                ],
                positive_friction_range_nap_top=results_table[
                    "positive_friction_range_nap_top"
                ],
                positive_friction_range_nap_btm=results_table[
                    "positive_friction_range_nap_btm"
                ],
                q_b_max=results_table["q_b_max"],
                q_s_max_mean=results_table["q_s_max_mean"],
                qc1=results_table["qc1"],
                qc2=results_table["qc2"],
                qc3=results_table["qc3"],
                s_b=results_table["s_b"],
                s_el=results_table["s_el"],
                k_v_b=results_table["k_v_b"],
                k_v_1=results_table["k_v_1"],
            ),
        )

    @property
    def soil_properties(self) -> SoilProperties:
        """
        The SoilProperties object.
        """
        return self._sp

    @property
    def pile_head_level_nap(self) -> float:
        """
        The elevation of the pile-head in [m] w.r.t. NAP.
        """
        return self._pile_head_level_nap

    @property
    def table(self) -> CPTResultsTable:
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
            np.array(self.table.F_nk_d),
            self.table.pile_tip_level_nap,
            color="tab:orange",
            label="Fnk;d",
        )
        axes.plot(
            np.array(self.table.R_s_cal),
            self.table.pile_tip_level_nap,
            color="lightgreen",
            label="Rs;cal;max",
        )
        axes.plot(
            np.array(self.table.R_b_cal),
            self.table.pile_tip_level_nap,
            color="darkgreen",
            label="Rb;cal;max",
        )
        axes.plot(
            np.array(self.table.R_c_d_net),
            self.table.pile_tip_level_nap,
            label=r"Rc;net;d",
            lw=3,
            color="tab:blue",
        )
        axes.set_xlabel("Force [kN]")

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
        self.soil_properties.cpt_table.plot_friction_ratio(ax_rf, add_legend=False)
        self.soil_properties.plot_layers(ax_layers, add_legend=False)
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
                title="name: " + self.soil_properties.test_id
                if self.soil_properties.test_id is not None
                else "name: unknown",
            )

        return fig
