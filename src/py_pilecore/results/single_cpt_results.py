from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from ..plot_utils import validate_axes_array
from .soil_properties import SoilProperties, get_soil_layer_handles

Number = Union[float, int]


class SingleCPTBearingResults:
    """
    Object that is returned by calling get_results() on a SingleCPTBearingCalculation
    object. Carries all result values from the calculation and can generate plots and
    dataframes.

    *Not meant to be instantiated by the user.*
    """

    def __init__(
        self,
        soil_properties: SoilProperties,
        pile_head_level_nap: float,
        results: pd.DataFrame | Dict[str, Sequence[float]],
        # excavation_param_t: Optional[float],
    ) -> None:
        """
        Parameters
        ----------
        calculation:
            The calculation object with input values
        soil_properties
            The object with soil properties
        pile_properties
            The object with pile properties
        pile_head_level_nap
            The elevation of the pile-head, in [m] w.r.t. NAP.
        results_dict_ptl
            A dictionary of PTLResults objects, which carry the pile calculation results
            of the individual pile-tip levels.
        """
        self._sp = soil_properties
        self._pile_head_level_nap = pile_head_level_nap

        if isinstance(results, pd.DataFrame):
            self._results_df = results
        else:
            self._results_df = pd.DataFrame(results)
        self._results_df = self._results_df.sort_values(
            by="pile_tip_level_nap", ascending=False
        )
        self._results_df = self._results_df.reset_index(drop=True)

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
    def results_df(self) -> pd.DataFrame:
        """
        A dataframe with all calculation results.

        Columns:
            pile_tip_level_nap: float
                The pile-tip level in [m] w.r.t. the reference.
            F_nk_cal: float
                The calculated value of the negative shaft friction force [kN].
            F_nk_k: float
                The characteristic value of the negative shaft friction force [kN].
            F_nk_d: float
                The design value of the negative shaft friction force [kN].
            R_s_cal: float
                The calculated value of the shaft bearingcapacity [kN].
            R_s_k: float
                The characteristic value of the shaft bearingcapacity [kN].
            R_s_d: float
                The design value of the shaft bearingcapacity [kN].
            R_b_cal: float
                The calculated value of the bottom bearingcapacity [kN].
            R_b_k: float
                The characteristic value of the bottom bearingcapacity [kN].
            R_b_d: float
                The design value of the bottom bearingcapacity [kN].
            R_c_cal: float
                The calculated value of the total compressive bearingcapacity [kN].
            R_c_k: float
                The characteristic value of the total compressive bearingcapacity [kN].
            R_c_d: float
                The design value of the total compressive bearingcapacity [kN].
            R_c_d_net: float
                The net design value of the total bearingcapacity [kN] (netto =
                excluding design negative friction force.).
            F_c_k: float
                The compressive force on the pile-head [kN].
            F_c_k_tot: float
                The characteristic value of the total compressive pile load [kN]
                (building-load + neg. friction force).
            negative_friction_range_nap_top: Optional[float]
                The top boundary of the negative friction interval [m] w.r.t. NAP.
                Can be None when the friction force was provided directly.
            negative_friction_range_nap_btm: Optional[float]
                The bottom boundary of the negative friction interval [m] w.r.t. NAP.
                Can be None when the friction force was provided directly.
            positive_friction_range_nap_top: float
                The top boundary of the positive friction interval [m] w.r.t. NAP.
            positive_friction_range_nap_btm: float
                The bottom boundary of the positive friction interval [m] w.r.t. NAP.
            q_b_max: float
                The maximum bottom bearing resistance [MPa].
            q_s_max_mean: float
                The maximum shaft bearing resistance [MPa].
            qc1: float
                The average friction resistance in Koppejan trajectory I, :math:`q_{c;I;gem}` [MPa] .
            qc2: float
                The average friction resistance in Koppejan trajectory II, :math:`q_{c;II;gem}` [MPa] .
            qc3: float
                The average friction resistance in Koppejan trajectory III, :math:`q_{c;III;gem}` [MPa] .
            s_b: float
                The settlement of the pile bottom [mm].
            s_el: float
                The elastic shortening of the pile due to elastic strain [mm].
            k_v_b: float
                The 1-dimensional stiffness modulus at pile bottom [kN/m].
            k_v_1: float
                The 1-dimensional stiffness modulus at pile head [MN/mm].
        """
        return self._results_df

    def plot_bearing_capacities(
        self,
        axes: Optional[plt.Axes] = None,
        figsize: Tuple[float, float] = (8, 10),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> plt.Axes:
        """
        Plot the bearing calculation results on an `plt.Axes' object.

        Parameters
        ----------
        axes:
            Optional `plt.Axes` object where the bearing capacities can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `plt.Axes`
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
                "'axes' argument to plot_bearing_capacities() must be a `pyplot.Axes` object or None."
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
            np.array(self._results_df.F_nk_d),
            self._results_df.pile_tip_level_nap,
            color="tab:orange",
            label="Fnk;d",
        )
        axes.plot(
            np.array(self._results_df.R_s_cal),
            self._results_df.pile_tip_level_nap,
            color="lightgreen",
            label="Rs;cal;max",
        )
        axes.plot(
            np.array(self._results_df.R_b_cal),
            self._results_df.pile_tip_level_nap,
            color="darkgreen",
            label="Rb;cal;max",
        )
        axes.plot(
            np.array(self._results_df.R_c_d_net),
            self._results_df.pile_tip_level_nap,
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
        axes: Optional[
            Tuple[
                Optional[plt.Axes],
                Optional[plt.Axes],
                Optional[plt.Axes],
                Optional[plt.Axes],
            ]
        ] = None,
        figsize: Tuple[float, float] = (10.0, 12.0),
        width_ratios: Tuple[float, float, float] = (1, 0.1, 2),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Tuple[
        Optional[plt.Axes], Optional[plt.Axes], Optional[plt.Axes], Optional[plt.Axes]
    ]:
        """
        Plot an overview of the bearing-capacities, including the .

        Parameters
        ----------
        show:
            call plt.show()
        axes:
            Optional tuple with four `plt.Axes` objects where the qc-data, Rf-data,
            soil-layer data and bearing capacities can be plotted on. If not provided, a
            new `plt.Figure` will be activated and the `plt.Axes` objects will be
            created and returned.
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
        axes_bearing:
            The `Axes` object where the bearing_capacities were plotted on.
        """

        # Create axes objects if not provided
        if axes is not None:
            validate_axes_array(axes=axes, shape=4)
            ax_qc, ax_rf, ax_layers, ax_bearing = axes

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
                3,
                **kwargs_subplot,
            )

            ax_qc, ax_layers, ax_bearing = axes_new
            ax_rf = ax_qc.twiny()

        # Plot soil data on first two Axes objects
        self.soil_properties.plot_overview(
            axes=(ax_qc, ax_rf, ax_layers), add_legend=False
        )

        # Plot bearing capacities on third Axes object
        self.plot_bearing_capacities(axes=ax_bearing, add_legend=False)

        if add_legend:
            ax_qc_legend_handles_list = (
                ax_qc.get_legend_handles_labels()[0] if ax_qc is not None else []
            )

            ax_rf_legend_handles_list = (
                ax_rf.get_legend_handles_labels()[0] if ax_rf is not None else []
            )

            ax_layers_legend_handles_list = (
                get_soil_layer_handles() if ax_layers is not None else []
            )

            # Omit last 2 duplicate "bearing" handles
            # (groundwater_level and surface_level):
            ax_bearing_legend_handles_list = (
                ax_bearing.get_legend_handles_labels()[0][2:]
                if ax_bearing is not None
                else []
            )

            handles_list = [
                *ax_qc_legend_handles_list,
                *ax_rf_legend_handles_list,
                *ax_layers_legend_handles_list,
                *ax_bearing_legend_handles_list,
            ]

            ax_legend = None
            if ax_bearing is not None:
                ax_legend = ax_bearing
            elif ax_layers is not None:
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
                    title="name: " + self.soil_properties.test_id
                    if self.soil_properties.test_id is not None
                    else "name: unknown",
                )

        return (ax_qc, ax_rf, ax_layers, ax_bearing)
