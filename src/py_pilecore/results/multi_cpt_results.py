from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..exceptions import UserError
from .load_settlement import get_load_settlement_plot
from .pile_properties import PileProperties, create_pile_properties_from_api_response
from .single_cpt_results import SingleCPTBearingResults
from .soil_properties import SoilProperties

Number = Union[float, int]


class MultiCPTBearingResults:
    def __init__(
        self,
        cpt_results_dict: Dict[str, SingleCPTBearingResults],
        group_results: pd.DataFrame | Dict[str, Sequence[float | str]],
        pile_properties: PileProperties,
        gamma_f_nk: float,
        gamma_r_b: float,
        gamma_r_s: float,
        soil_load: float,
    ) -> None:
        self._pp = pile_properties
        self._gamma_f_nk = gamma_f_nk
        self._gamma_r_b = gamma_r_b
        self._gamma_r_s = gamma_r_s
        self._soil_load = soil_load

        self._cpt_results_dict = cpt_results_dict

        df_list: List[pd.DataFrame] = []
        for test_id in self.cpt_results_dict:
            df = self.cpt_results_dict[test_id].results_df
            df = df.assign(test_id=test_id)
            df_list.append(df)
        self._cpt_results_df = pd.concat(df_list)
        self._cpt_results_df = self._cpt_results_df.assign(
            pile_tip_level_nap=self._cpt_results_df.pile_tip_level_nap.round(1)
        )
        self._cpts_group = list(self.cpt_results_dict.keys())

        if isinstance(group_results, pd.DataFrame):
            self._group_results_df = group_results
        else:
            self._group_results_df = pd.DataFrame(group_results)

    @property
    def pile_properties(self) -> PileProperties:
        """
        The PileProperties object.
        """
        return self._pp

    @property
    def cpt_results_dict(self) -> Dict[str, SingleCPTBearingResults]:
        return self._cpt_results_dict

    @property
    def cpts_group(self) -> List[str]:
        return self._cpts_group

    @cpts_group.setter
    def cpts_group(self, value: List[str]) -> None:
        if not (isinstance(value, (list, tuple, np.ndarray)) and len(value) > 0):
            raise UserError("cpts_group should be a list with length > 0.")
        for cpt in value:
            if cpt not in self.cpt_results_dict.keys():
                raise UserError(
                    f"""Unknown CPT name in cpts_group: {cpt}. Make sure to add this CPT
                    to the MultiCPTBearingCalculation input_table argument before
                    regenerating the results."""
                )
        self._cpts_group = value

    @property
    def cpt_results_df(self) -> pd.DataFrame:
        """
        A dataframe with the calculation results of all individual CPTs.

        Columns:
            test_id: str
                The CPT identifier.
            pile_tip_level_nap: float
                The pile-tip level in [m] w.r.t. NAP.
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
        return self._cpt_results_df

    @property
    def group_summary_df(self) -> pd.DataFrame:
        """
        A dataframe with a summary of group calculation results.

        Columns:
            pile_tip_level_nap: float
                The pile-tip level [m] w.r.t. NAP.
            var_coef: float
                The variation coefficient [%] of the calculated bearing capacities in the
                group.
            n_cpts
                The number of CPTs [-] that have been taken into account to establish the
                :math:`Xi` value.
            xi_normative
                The normative :math:`Xi` (either :math:`Xi_3` or :math:`Xi_4`)
            xi_value
                The :math:`Xi` value [-] that was applied to calculate the characteristic
                value of the total bearing capacity.
            cpt_normative
                The normative CPT. Can be "group average" if that was found to be the
                normative scenario.
            R_s_k
                The characteristic value of the shaft bearingcapacity [kN].
            R_b_k
                The characteristic value of the bottom bearingcapacity [kN].
            R_c_k
                The characteristic value of the total compressive bearingcapacity [kN].
            R_c_d
                The design value of the total bearingcapacity [kN].
            R_c_d_net
                The net design value of the total bearingcapacity [kN] (netto =
                excluding design negative friction force.).
            F_c_k_tot
                The characteristic value of the total compressive pile load [kN]
                (building-load + neg. friction force).
            F_nk_d
                The design value of the negative friction force [kN].
            s_b
                The settlement of the pile bottom [mm].
            s_e
                The elastic shortening of the pile due to elastic strain [mm].
            k_v_b
                The 1-dimensional stiffness modulus at pile bottom [kN/m].
            k_v_1
                The 1-dimensional stiffness modulus at pile head [MN/mm].
        """
        return self.group_results_df.loc[
            :,
            [
                "pile_tip_level_nap",
                "var_coef",
                "n_cpts",
                "xi_normative",
                "xi_value",
                "cpt_normative",
                "R_s_k",
                "R_b_k",
                "R_c_k",
                "R_c_d",
                "R_c_d_net",
                "F_c_k_tot",
                "F_nk_d",
                "s_b",
                "s_e",
                "k_v_b",
                "k_v_1",
            ],
        ]

    def get_results_per_cpt(self, column_name: str) -> pd.DataFrame:
        if column_name not in self.cpt_results_df.columns or column_name in [
            "pile_tip_level_nap",
            "test_id",
        ]:
            raise ValueError("Invalid column_name provided.")

        results = pd.pivot_table(
            self.cpt_results_df,
            values=column_name,
            index="pile_tip_level_nap",
            columns="test_id",
        )
        return results.sort_values("pile_tip_level_nap", ascending=False)

    @property
    def group_results_df(self) -> pd.DataFrame:
        return self._group_results_df

    @classmethod
    def from_api_response(
        cls, response_dict: dict, cpt_input: dict
    ) -> "MultiCPTBearingResults":
        cpt_results_dict: Dict[str, SingleCPTBearingResults] = {
            cpt_results["test_id"]: SingleCPTBearingResults(
                soil_properties=SoilProperties(
                    cpt_data=cpt_results["cpt_chart"],
                    layer_table=cpt_results["layer_table"],
                    ref_height=cpt_input[cpt_results["test_id"]]["ref_height"],
                    surface_level_ref=cpt_input[cpt_results["test_id"]][
                        "surface_level_nap"
                    ],
                    groundwater_level_ref=cpt_results["groundwater_level_nap"],
                ),
                pile_head_level_nap=cpt_results["annotations"]["pile_head_level_nap"],
                results=cpt_results["results_table"],
            )
            for cpt_results in response_dict["cpts"]
        }

        return cls(
            cpt_results_dict=cpt_results_dict,
            pile_properties=create_pile_properties_from_api_response(
                response_dict["pile_properties"]
            ),
            group_results=response_dict["group_results"],
            gamma_f_nk=response_dict["calculation_params"]["gamma_f_nk"],
            gamma_r_b=response_dict["calculation_params"]["gamma_r_b"],
            gamma_r_s=response_dict["calculation_params"]["gamma_r_s"],
            soil_load=response_dict["calculation_params"]["soil_load"],
        )

    def get_cpt_results(self, test_id: str) -> SingleCPTBearingResults:
        """
        Returns the `SingleCPTBearingResults` object for the provided test_id.
        """

        if test_id not in self.cpt_results_dict.keys():
            raise ValueError(
                "No Cpt-results were calculated for this test-id. "
                "Please check the spelling or run a new calculation for this CPT."
            )

        return self.cpt_results_dict[test_id]

    def plot_group_bearing_capacities(
        self,
        axes: Optional[plt.Axes] = None,
        figsize: Tuple[int, int] = (8, 10),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> plt.Axes:
        """
        Plots the design value of the bearing capacity Rcd, based on a group of CPTs.

        Parameters
        ----------
        axes:
            Optional `plt.Axes` object where the bearing capacity data can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `plt.Axes`
            object will be created and returned.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        add_legend:
            Add a legend to the `Axes` object
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

        axes.plot(
            self.group_summary_df["R_c_d"],
            self.group_summary_df["pile_tip_level_nap"],
            "-",
            label=r"$R_{c;d}$",
        )
        axes.plot(
            self.group_summary_df["F_nk_d"],
            self.group_summary_df["pile_tip_level_nap"],
            ":",
            label=r"$F_{s;d}$ ",
        )
        axes.set_xlabel("[kN]")
        axes.set_ylabel("[m] w.r.t. NAP")

        # set grid
        axes.grid()

        # Add legend
        if add_legend:
            axes.legend(
                loc="upper left",
                bbox_to_anchor=(1, 1),
            )
        return axes

    def plot_load_settlement(
        self,
        pile_tip_level_nap: float,
        axes: Optional[plt.Axes] = None,
        figsize: Tuple[float, float] = (6.0, 6.0),
        sb_max: float = 25,
        **kwargs: Any,
    ) -> plt.Axes:
        """
        Plot load settlement curve.

        Parameters
        ----------
        pile_tip_level_nap:
            Pile tip level  in [m NAP] for which to calculate and plot the
            load-settlement behavior.
        axes:
            Optional `plt.Axes` object where the load-settlement data can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `plt.Axes`
            object will be created and returned.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        sb_max:
            Default: 25
            Maximum value for settlement at pile-tip level.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The `Axes` object where the settlement curves were plotted on
        """

        # Validate axes
        if (axes is not None) and (not isinstance(axes, plt.Axes)):
            raise ValueError(
                "'axes' argument to plot_load_settlement() must be a `pyplot.Axes` object or None."
            )

        # Get ptl index
        idx = np.argmin(
            abs(self.group_summary_df.pile_tip_level_nap - pile_tip_level_nap)
        )
        if (
            abs(self.group_summary_df.pile_tip_level_nap.loc[idx] - pile_tip_level_nap)
            > 0.01
        ):
            raise UserError(
                """No results have been calculated for the requested pile-tip-level.
                Please include this level in the pile-tip range parameter of the
                calculation."""
            )

        return get_load_settlement_plot(
            settlement_curve=self._pp.settlement_curve,
            d_eq=self._pp.equiv_base_diameter,
            s_b=self.group_summary_df.loc[idx, "s_b"],
            f_c_k=self.group_results_df.loc[idx, "F_c_k"],
            f_nk_k=self.group_results_df.loc[idx, "F_nk_k"],
            r_b_k=self.group_results_df.loc[idx, "R_b_k"],
            r_s_k=self.group_results_df.loc[idx, "R_s_k"],
            rs_mob_ratio=self.group_results_df.loc[idx, "R_s_mob_ratio"],
            rb_mob_ratio=self.group_results_df.loc[idx, "R_b_mob_ratio"],
            sb_max=sb_max,
            axes=axes,
            figsize=figsize,
            **kwargs,
        )
