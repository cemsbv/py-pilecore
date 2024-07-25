from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.patches import Patch

from pypilecore.common.piles import PileProperties
from pypilecore.exceptions import UserError
from pypilecore.results.load_settlement import get_load_settlement_plot
from pypilecore.results.single_cpt_results import SingleCPTBearingResults

Number = Union[float, int]


class CPTGroupResultsTable:
    """
    Dataclass that contains the bearing results of a group of CPTs.
    """

    def __init__(
        self,
        pile_tip_level_nap: Sequence[float],
        R_s_k: Sequence[float],
        R_b_k: Sequence[float],
        R_c_k: Sequence[float],
        R_s_d: Sequence[float],
        R_b_d: Sequence[float],
        R_c_d: Sequence[float],
        F_nk_cal_mean: Sequence[float],
        F_nk_k: Sequence[float],
        F_nk_d: Sequence[float],
        R_c_d_net: Sequence[float],
        F_c_k: Sequence[float],
        F_c_k_tot: Sequence[float],
        s_b: Sequence[float],
        s_e: Sequence[float],
        s_e_mean: Sequence[float],
        R_b_mob_ratio: Sequence[float],
        R_s_mob_ratio: Sequence[float],
        k_v_b: Sequence[float],
        k_v_1: Sequence[float],
        R_c_min: Sequence[float],
        R_c_max: Sequence[float],
        R_c_mean: Sequence[float],
        R_c_std: Sequence[float],
        R_s_mean: Sequence[float],
        R_b_mean: Sequence[float],
        var_coef: Sequence[float],
        n_cpts: Sequence[int],
        use_group_average: Sequence[bool],
        xi_normative: Sequence[str],
        xi_value: Sequence[float],
        cpt_Rc_min: Sequence[str],
        cpt_Rc_max: Sequence[str],
        cpt_normative: Sequence[str],
    ):
        """
        Parameters
        ----------
        pile_tip_level_nap:
            The pile-tip level [m] w.r.t. NAP.
        R_s_k:
            The characteristic value of the shaft bearingcapacity  [kN].
        R_b_k:
            The characteristic value of the bottom bearingcapacity [kN].
        R_c_k:
            The characteristic value of the total compressive bearingcapacity [kN].
        R_s_d:
            The design value of the shaft bearingcapacity  [kN].
        R_b_d:
            The design value of the bottom bearingcapacity [kN].
        R_c_d:
            The design value of the total bearingcapacity [kN].
        F_nk_cal_mean:
            The mean value of the calculated single-CPT negative friction forces [kN].
        F_nk_k:
            The charactertistic value of the negative friction force [kN].
        F_nk_d:
            The design value of the negative friction force [kN].
        R_c_d_net:
            The net design value of the total bearingcapacity [kN] (netto = excluding design negative friction force.).
        F_c_k:
            The characteristic value of the load on the pile head (e.g. building load) [kN]
        F_c_k_tot:
            The characteristic value of the total compressive pile load [kN] (building-load + neg. friction force).
        s_b:
            The settlement of the pile bottom [mm].
        s_e:
            The elastic shortening of the pile [mm].
        s_e_mean:
            The mean of single-CPT results for elastic shortening of the pile [mm].
        R_b_mob_ratio:
            The mobilisation ratio of the bottom bearing capacity [-].
        R_s_mob_ratio:
            The mobilisation ratio of the shaft bearing capacity [-].
        k_v_b:
            The 1-dimensional stiffness modulus at pile bottom [kN/m].
        k_v_1:
            The 1-dimensional stiffness modulus at pile head [kN/m].
        R_c_min:
            The minimum of the single-CPT values for the calculated bearingcapacity [kN].
        R_c_max:
            The maximum of the single-CPT values for the calculated bearingcapacity [kN].
        R_c_mean:
            The mean of the single-CPT values for the calculated bearingcapacity [kN].
        R_c_std:
            The standard-deviation of the single-CPT values for the calculated bearingcapacity [kN].
        R_s_mean:
            The mean of the single-CPT values for the calculated shaft bearingcapacity [kN].
        R_b_mean:
            The mean of the single-CPT values for the calculated bottom bearingcapacity [kN].
        var_coef:
            The variation coefficient [%] of the calculated bearing capacities in the group.
        n_cpts:
            The number of CPTs [-] that have been taken into account to establish the Xi value.
        use_group_average:
            If true, the group average is used for the calculation of characteristic group
            results. If false, the values of the normative CPT are used.
        xi_normative:
            The normative Xi (either Xi_3 or Xi_4)
        xi_value:
            The Xi value [-] that was applied to calculate the characteristic value of the
            total bearing capacity.
        cpt_Rc_min:
            The CPT with the lowest value for R_c_cal.
        cpt_Rc_max:
            The CPT with the highest value for R_c_cal.
        cpt_normative:
            The normative CPT. Can be "group average" if that was found to be the normative scenario.
        """
        self.pile_tip_level_nap = (
            np.array(pile_tip_level_nap).astype(np.float64).round(decimals=2)
        )
        """The pile-tip level [m] w.r.t. NAP."""
        self.R_s_k = np.array(R_s_k).astype(np.float64)
        """The characteristic value of the shaft bearingcapacity  [kN]."""
        self.R_b_k = np.array(R_b_k).astype(np.float64)
        """The characteristic value of the bottom bearingcapacity [kN]."""
        self.R_c_k = np.array(R_c_k).astype(np.float64)
        """The characteristic value of the total compressive bearingcapacity [kN]."""
        self.R_s_d = np.array(R_s_d).astype(np.float64)
        """The design value of the shaft bearingcapacity  [kN]."""
        self.R_b_d = np.array(R_b_d).astype(np.float64)
        """The design value of the bottom bearingcapacity [kN]."""
        self.R_c_d = np.array(R_c_d).astype(np.float64)
        """The design value of the total bearingcapacity [kN]."""
        self.F_nk_cal_mean = np.array(F_nk_cal_mean).astype(np.float64)
        """The mean value of the calculated single-CPT negative friction forces [kN]."""
        self.F_nk_k = np.array(F_nk_k).astype(np.float64)
        """The charactertistic value of the negative friction force [kN]."""
        self.F_nk_d = np.array(F_nk_d).astype(np.float64)
        """The design value of the negative friction force [kN]."""
        self.R_c_d_net = np.array(R_c_d_net).astype(np.float64)
        """The net design value of the total bearingcapacity [kN] (netto = excluding design negative friction force.)."""
        self.F_c_k = np.array(F_c_k).astype(np.float64)
        """The characteristic value of the load on the pile head (e.g. building load) [kN]"""
        self.F_c_k_tot = np.array(F_c_k_tot).astype(np.float64)
        """The characteristic value of the total compressive pile load [kN] (building-load + neg. friction force)."""
        self.s_b = np.array(s_b).astype(np.float64)
        """The settlement of the pile bottom [mm]."""
        self.s_e = np.array(s_e).astype(np.float64)
        """The elastic shortening of the pile [mm]."""
        self.s_e_mean = np.array(s_e_mean).astype(np.float64)
        """The mean of single-CPT results for elastic shortening of the pile [mm]."""
        self.R_b_mob_ratio = np.array(R_b_mob_ratio).astype(np.float64)
        """The mobilisation ratio of the bottom bearing capacity [-]."""
        self.R_s_mob_ratio = np.array(R_s_mob_ratio).astype(np.float64)
        """The mobilisation ratio of the shaft bearing capacity [-]."""
        self.k_v_b = np.array(k_v_b).astype(np.float64)
        """The 1-dimensional stiffness modulus at pile bottom [kN/m]."""
        self.k_v_1 = np.array(k_v_1).astype(np.float64)
        """The 1-dimensional stiffness modulus at pile head [kN/m]."""
        self.R_c_min = np.array(R_c_min).astype(np.float64)
        """The minimum of the single-CPT values for the calculated bearingcapacity [kN]."""
        self.R_c_max = np.array(R_c_max).astype(np.float64)
        """The maximum of the single-CPT values for the calculated bearingcapacity [kN]."""
        self.R_c_mean = np.array(R_c_mean).astype(np.float64)
        """The mean of the single-CPT values for the calculated bearingcapacity [kN]."""
        self.R_c_std = np.array(R_c_std).astype(np.float64)
        """The standard-deviation of the single-CPT values for the calculated bearingcapacity [kN]."""
        self.R_s_mean = np.array(R_s_mean).astype(np.float64)
        """The mean of the single-CPT values for the calculated shaft bearingcapacity [kN]."""
        self.R_b_mean = np.array(R_b_mean).astype(np.float64)
        """The mean of the single-CPT values for the calculated bottom bearingcapacity [kN]."""
        self.var_coef = np.array(var_coef).astype(np.float64)
        """The variation coefficient [%] of the calculated bearing capacities in the group."""
        self.n_cpts = np.array(n_cpts).astype(np.int32)
        """The number of CPTs [-] that have been taken into account to establish the Xi value."""
        self.use_group_average = np.array(use_group_average).astype(np.bool_)
        """If true, the group average is used for the calculation of characteristic group
        results. If false, the values of the normative CPT are used."""
        self.xi_normative = np.array(xi_normative).astype(np.str_)
        """The normative Xi (either Xi_3 or Xi_4)"""
        self.xi_value = np.array(xi_value).astype(np.float64)
        """The Xi value [-] that was applied to calculate the characteristic value of the
        total bearing capacity."""
        self.cpt_Rc_min = np.array(cpt_Rc_min).astype(np.str_)
        """The CPT with the lowest value for R_c_cal."""
        self.cpt_Rc_max = np.array(cpt_Rc_max).astype(np.str_)
        """The CPT with the highest value for R_c_cal."""
        self.cpt_normative = np.array(cpt_normative).astype(np.str_)
        """The normative CPT. Can be "group average" if that was found to be the normative scenario."""

        for value in self.__dict__.values():
            if not len(value) == len(self.pile_tip_level_nap):
                raise ValueError(
                    "Inputs for CPTGroupResults dataclass must have same length."
                )

    @lru_cache
    def to_pandas(self) -> pd.DataFrame:
        """The pandas.DataFrame representation"""
        return pd.DataFrame(self.__dict__).dropna(axis=0, how="all")

    def plot_bearing_capacities(
        self,
        axes: Axes | None = None,
        figsize: Tuple[int, int] = (8, 10),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plots the design value of the bearing capacity Rcd, based on a group of CPTs.

        Parameters
        ----------
        axes:
            Optional `Axes` object where the bearing capacity data can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `Axes`
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
        if axes is not None:
            if not isinstance(axes, Axes):
                raise TypeError(
                    "'axes' argument to plot_bearing_capacities() must be a `pyplot.axes.Axes` object or None."
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

        axes.plot(
            self.R_c_d,
            self.pile_tip_level_nap,
            "-",
            label=r"$R_{c;d}$",
        )
        axes.plot(
            self.F_nk_d,
            self.pile_tip_level_nap,
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


class SingleCPTBearingResultsContainer:
    """A container that holds multiple SingleCPTBearingResults objects"""

    def __init__(self, cpt_results_dict: Dict[str, SingleCPTBearingResults]):
        """
        Parameters
        ----------
        cpt_results_dict:
            A dictionary that maps the cpt-names to SingleCPTBearingResults objects.
        """
        self._cpt_results_dict = cpt_results_dict

    @classmethod
    def from_api_response(
        cls, cpt_results_list: list, cpt_input: dict
    ) -> "SingleCPTBearingResultsContainer":
        """
        Instantiates the SingleCPTBearingResultsContainer object from the "cpts" array,
        which is returned in the response of a "compression/multiple-cpts/results" endpoint call.
        """
        return cls(
            cpt_results_dict={
                cpt_results["test_id"]: SingleCPTBearingResults.from_api_response(
                    cpt_results_dict=cpt_results,
                    ref_height=cpt_input[cpt_results["test_id"]]["ref_height"],
                    surface_level_ref=cpt_input[cpt_results["test_id"]][
                        "surface_level_nap"
                    ],
                    x=cpt_input[cpt_results["test_id"]].get("location", {}).get("x"),
                    y=cpt_input[cpt_results["test_id"]].get("location", {}).get("y"),
                )
                for cpt_results in cpt_results_list
            }
        )

    def __getitem__(self, test_id: str) -> SingleCPTBearingResults:
        if not isinstance(test_id, str):
            raise TypeError(f"Expected a test-id as a string, but got: {type(test_id)}")

        return self.get_cpt_results(test_id)

    @property
    def cpt_results_dict(self) -> Dict[str, SingleCPTBearingResults]:
        """The dictionary that maps the cpt-names to SingleCPTBearingResults objects."""
        return self._cpt_results_dict

    @property
    def test_ids(self) -> List[str]:
        """The test-ids of the CPTs."""
        return list(self.cpt_results_dict.keys())

    @property
    def results(self) -> List[SingleCPTBearingResults]:
        """The computed results, as a list of SingleCPTBearingResults objects."""
        return list(self.cpt_results_dict.values())

    def get_cpt_results(self, test_id: str) -> SingleCPTBearingResults:
        """
        Returns the `SingleCPTBearingResults` object for the provided test_id.
        """

        if test_id not in self.cpt_results_dict.keys():
            raise ValueError(
                f"No Cpt-results were calculated for this test-id: {test_id}. "
                "Please check the spelling or run a new calculation for this CPT."
            )

        return self.cpt_results_dict[test_id]

    def get_results_per_cpt(self, column_name: str) -> pd.DataFrame:
        """
        Returns a pandas dataframe with a single result-item, organized per CPT
        (test-id) and pile-tip-level-nap.

        Parameters
        ----------
        column_name:
            The name of the result-item / column name of the single-cpt-results table.
        """
        if column_name not in self.to_pandas().columns or column_name in [
            "pile_tip_level_nap",
            "test_id",
        ]:
            raise ValueError("Invalid column_name provided.")

        results = pd.pivot_table(
            self.to_pandas(),
            values=column_name,
            index="pile_tip_level_nap",
            columns="test_id",
            dropna=False,
        )
        return results.sort_values("pile_tip_level_nap", ascending=False)

    @lru_cache
    def to_pandas(self) -> pd.DataFrame:
        """Returns a total overview of all single-cpt results in a pandas.DataFrame representation."""
        df_list: List[pd.DataFrame] = []

        for test_id in self.cpt_results_dict:
            df = self.cpt_results_dict[test_id].table.to_pandas()
            df = df.assign(test_id=test_id)
            df_list.append(df)

        cpt_results_df = pd.concat(df_list)
        cpt_results_df = cpt_results_df.assign(
            pile_tip_level_nap=cpt_results_df.pile_tip_level_nap.round(1)
        )

        return cpt_results_df


class MultiCPTBearingResults:
    """
    Object that contains the results of a PileCore multi-cpt calculation.

    *Not meant to be instantiated by the user.*
    """

    def __init__(
        self,
        cpt_results: SingleCPTBearingResultsContainer,
        group_results_table: CPTGroupResultsTable,
        pile_properties: PileProperties,
        gamma_f_nk: float,
        gamma_r_b: float,
        gamma_r_s: float,
        soil_load: float,
    ) -> None:
        """
        Parameters
        ----------
        cpt_results:
            The container object with single-CPT results
        group_results_table:
            The table object with CPT-group-results
        pile_properties:
            The PileProperties object
        gamma_f_nk:
            Safety factor for design-values of the negative sleeve friction force. [-]
        gamma_r_b:
            Safety factor, used to obtain design-values of the pile-tip bearingcapacity. [-]
        gamma_r_s:
            Safety factor, used to obtain design-values of the sleeve bearingcapacity. [-]
        soil_load:
            (Fictive) load on soil used to calculate soil settlement [kPa]. This is
            required and used to determine settlement of pile w.r.t. soil.
        """
        self._pp = pile_properties
        self._gamma_f_nk = gamma_f_nk
        self._gamma_r_b = gamma_r_b
        self._gamma_r_s = gamma_r_s
        self._soil_load = soil_load

        self._cpt_results = cpt_results

        self._group_results_table = group_results_table

    @classmethod
    def from_api_response(
        cls, response_dict: dict, cpt_input: dict
    ) -> "MultiCPTBearingResults":
        """
        Build the object from the response payload of the PileCore endpoint
        "/compression/multi-cpt/results".
        """
        cpt_results_dict = SingleCPTBearingResultsContainer.from_api_response(
            cpt_results_list=response_dict["cpts"], cpt_input=cpt_input
        )
        group_results = response_dict["group_results"]
        return cls(
            cpt_results=cpt_results_dict,
            pile_properties=PileProperties.from_api_response(
                response_dict["pile_properties"]
            ),
            group_results_table=CPTGroupResultsTable(
                pile_tip_level_nap=group_results["pile_tip_level_nap"],
                R_s_k=group_results["R_s_k"],
                R_b_k=group_results["R_b_k"],
                R_c_k=group_results["R_c_k"],
                R_s_d=group_results["R_s_d"]
                if "R_s_d" in group_results
                else np.full_like(
                    group_results["pile_tip_level_nap"], fill_value=np.nan
                ),  # For backwards compatibility with PileCore-API < 2.9.0
                R_b_d=group_results["R_b_d"]
                if "R_b_d" in group_results
                else np.full_like(
                    group_results["pile_tip_level_nap"], fill_value=np.nan
                ),  # For backwards compatibility with PileCore-API < 2.9.0,
                R_c_d=group_results["R_c_d"],
                F_nk_cal_mean=group_results["F_nk_cal_mean"],
                F_nk_k=group_results["F_nk_k"],
                F_nk_d=group_results["F_nk_d"],
                R_c_d_net=group_results["R_c_d_net"],
                F_c_k=group_results["F_c_k"],
                F_c_k_tot=group_results["F_c_k_tot"],
                s_b=group_results["s_b"],
                s_e=group_results["s_e"],
                s_e_mean=group_results["s_e_mean"],
                R_b_mob_ratio=group_results["R_b_mob_ratio"],
                R_s_mob_ratio=group_results["R_s_mob_ratio"],
                k_v_b=group_results["k_v_b"],
                k_v_1=group_results["k_v_1"],
                R_c_min=group_results["R_c_min"],
                R_c_max=group_results["R_c_max"],
                R_c_mean=group_results["R_c_mean"],
                R_c_std=group_results["R_c_std"],
                R_s_mean=group_results["R_s_mean"],
                R_b_mean=group_results["R_b_mean"],
                var_coef=group_results["var_coef"],
                n_cpts=group_results["n_cpts"],
                use_group_average=group_results["use_group_average"],
                xi_normative=group_results["xi_normative"],
                xi_value=group_results["xi_value"],
                cpt_Rc_min=group_results["cpt_Rc_min"],
                cpt_Rc_max=group_results["cpt_Rc_max"],
                cpt_normative=group_results["cpt_normative"],
            ),
            gamma_f_nk=response_dict["calculation_params"]["gamma_f_nk"],
            gamma_r_b=response_dict["calculation_params"]["gamma_r_b"],
            gamma_r_s=response_dict["calculation_params"]["gamma_r_s"],
            soil_load=response_dict["calculation_params"]["soil_load"],
        )

    @property
    def pile_properties(self) -> PileProperties:
        """
        The PileProperties object.
        """
        return self._pp

    @property
    def cpt_results(self) -> SingleCPTBearingResultsContainer:
        """The SingleCPTBearingResultsContainer object."""
        return self._cpt_results

    @property
    def cpt_names(self) -> List[str]:
        """The test-ids of the CPTs."""
        return self.cpt_results.test_ids

    @property
    def group_results_table(self) -> CPTGroupResultsTable:
        """The CPTGroupResultsTable dataclass, containing the group results."""
        return self._group_results_table

    def boxplot(
        self,
        attribute: str,
        axes: Axes | None = None,
        figsize: Tuple[float, float] = (6.0, 6.0),
        show_sqrt: bool = False,
        **kwargs: Any,
    ) -> Axes:
        """
        Plot a box and whisker plot for a given attribute.


        .. code-block:: none

                     MIN      Q1   median  Q3       MAX
                               |-----:-----|
                      |--------|     :     |--------|
                               |-----:-----|

        Parameters
        ----------
        attribute:
            result attribute to create boxplot. Please note that the attribute name must be present in
            the `CPTResultsTable` and `CPTGroupResultsTable` class.
        axes:
            Optional `Axes` object where the boxplot data can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `Axes`
            object will be created and returned.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        show_sqrt:
            Add sqrt(2) bandwidth to figure
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The `Axes` object where the settlement curves were plotted on
        """

        # validate attribute
        if (
            attribute not in self.cpt_results.results[0].table.__dict__.keys()
            or attribute not in self.group_results_table.__dict__.keys()
        ):
            raise ValueError(
                f"""
                {attribute} is not present in CPTResultsTable or CPTGroupResultsTable class.
                Please select on of the following attributes:
                {
                    set(self.cpt_results.results[0].table.__dict__.keys())
                     & set(self.group_results_table.__dict__.keys())
                }
                """
            )

        # Create axes objects if not provided
        if axes is not None:
            if not isinstance(axes, Axes):
                raise ValueError(
                    "'axes' argument to boxplot() must be a `pyplot.axes.Axes` object or None."
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

        # Collect data from single calculation
        data = np.array(
            [
                item.table.__getattribute__(attribute)
                for item in self.cpt_results.results
            ]
        )

        # Draw a box and whisker plot
        axes.boxplot(
            np.flip(data, axis=0),
            tick_labels=np.flip(self.group_results_table.pile_tip_level_nap),
            whis=(0, 100),
            autorange=True,
            vert=False,
            patch_artist=True,
            showmeans=True,
            zorder=0,
        )

        # ad additional bandwidth of sqrt(2) of the mean value
        if show_sqrt:
            axes.scatter(
                np.flip(data.mean(axis=0)) * np.sqrt(2),
                np.flip(
                    np.arange(len(self.group_results_table.pile_tip_level_nap)) + 1
                ),
                marker="^",
                color="tab:purple",
                zorder=1,
            )
            axes.scatter(
                np.flip(data.mean(axis=0)) / np.sqrt(2),
                np.flip(
                    np.arange(len(self.group_results_table.pile_tip_level_nap)) + 1
                ),
                marker="^",
                color="tab:purple",
                zorder=1,
            )

        # Draw group result over single result
        axes.scatter(
            np.flip(self.group_results_table.__getattribute__(attribute)),
            np.flip(np.arange(len(self.group_results_table.pile_tip_level_nap)) + 1),
            marker="o",
            color="tab:red",
            zorder=1,
        )

        # Draw group result over single result
        for i, x in enumerate(data.mean(axis=0)):
            axes.annotate(f"{x.round(2)}", xy=(x, i + 1))

        # add legend to figure
        axes.legend(
            handles=[
                Patch(color=clr, label=key)
                for (key, clr) in {
                    "Single;min:max": "black",
                    "Single;Q25:Q75": "tab:blue",
                    "Single;Q50": "tab:orange",
                    "Single;mean": "tab:green",
                    "Single;mean;sqrt": "tab:purple",
                    "Group;normative": "tab:red",
                }.items()
            ],
            loc="upper left",
            bbox_to_anchor=(1, 1),
            title=f"Bandwidth {attribute}",
        )

        # set label
        axes.set_ylabel("Depth [m NAP]")
        axes.set_xlabel(f"{attribute}")

        return axes

    def plot_load_settlement(
        self,
        pile_tip_level_nap: float,
        axes: Axes | None = None,
        figsize: Tuple[float, float] = (6.0, 6.0),
        sb_max: float = 25,
        **kwargs: Any,
    ) -> Axes:
        """
        Plot load settlement curve.

        Parameters
        ----------
        pile_tip_level_nap:
            Pile tip level  in [m NAP] for which to calculate and plot the
            load-settlement behavior.
        axes:
            Optional `Axes` object where the load-settlement data can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `Axes`
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
        # Validate required properties are present
        if self._pp.pile_type.settlement_curve is None:
            raise ValueError(
                "No settlement curve is defined for the pile-type. "
                "Please define a settlement curve in the pile-type properties."
            )

        # Validate axes
        if (axes is not None) and (not isinstance(axes, Axes)):
            raise ValueError(
                "'axes' argument to plot_load_settlement() must be a `pyplot.axes.Axes` object or None."
            )

        # Get ptl index
        idx = int(
            np.argmin(
                abs(
                    np.array(self.group_results_table.pile_tip_level_nap)
                    - pile_tip_level_nap
                )
            )
        )
        if (
            abs(self.group_results_table.pile_tip_level_nap[idx] - pile_tip_level_nap)
            > 0.01
        ):
            raise UserError(
                """No results have been calculated for the requested pile-tip-level.
                Please include this level in the pile-tip range parameter of the
                calculation."""
            )

        return get_load_settlement_plot(
            settlement_curve=self._pp.pile_type.settlement_curve,
            d_eq=self._pp.geometry.equiv_diameter_pile_tip,
            s_b=self.group_results_table.s_b[idx],
            f_c_k=self.group_results_table.F_c_k[idx],
            f_nk_k=self.group_results_table.F_nk_k[idx],
            r_b_k=self.group_results_table.R_b_k[idx],
            r_s_k=self.group_results_table.R_s_k[idx],
            rs_mob_ratio=self.group_results_table.R_s_mob_ratio[idx],
            rb_mob_ratio=self.group_results_table.R_b_mob_ratio[idx],
            sb_max=sb_max,
            axes=axes,
            figsize=figsize,
            **kwargs,
        )
