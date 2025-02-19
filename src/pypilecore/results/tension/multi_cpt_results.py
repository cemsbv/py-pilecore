from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from pypilecore.common.piles import PileProperties
from pypilecore.results.tension.single_cpt_results import SingleCPTTensionBearingResults

Number = Union[float, int]


class CPTTensionGroupResultsTable:
    """
    Dataclass that contains the bearing results of a group of CPTs.
    """

    def __init__(
        self,
        pile_tip_level_nap: Sequence[float],
        var_coef: Sequence[float],
        n_cpts: Sequence[float],
        xi_value: Sequence[float],
        xi_normative: Sequence[float],
        cpt_normative: Sequence[float],
        R_t_d_min: Sequence[float],
        R_t_d_mean: Sequence[float],
        R_t_d: Sequence[float],
        R_t_d_plug: Sequence[float],
    ):
        """
        Parameters
        ----------
        pile_tip_level_nap:
            The pile-tip level [m] w.r.t. NAP.
        var_coef:
            The variation coefficient [%] of the calculated bearing capacities in the group.
        n_cpts:
            The number of CPTs [-] that have been taken into account to establish the Xi value.
        xi_normative:
            The normative Xi (either Xi_3 or Xi_4)
        xi_value:
            The Xi value [-] that was applied to calculate the characteristic value of the
            total bearing capacity.
        cpt_normative:
            The normative CPT. Can be "group average" if that was found to be the normative scenario.
        R_t_d_min:
            The minimum of the single-CPT values for the calculated bearingcapacity [kN].
        R_t_d_mean:
            The mean of the single-CPT values for the calculated
                bearingcapacity [kN].
        R_t_d:
            calculation value of the tensile resistance of a pile or pile group
            (7.6.3.3 (a) NEN 9997-1+C2:2017) [kN]
        R_t_d_plug:
            The design value of the total plug weight bearingcapacity [kN].
        """
        self.pile_tip_level_nap = (
            np.array(pile_tip_level_nap).astype(np.float64).round(decimals=2)
        )
        """The pile-tip level [m] w.r.t. NAP."""
        self.var_coef = np.array(var_coef).astype(np.float64)
        """The variation coefficient [%] of the calculated bearing capacities in the group."""
        self.n_cpts = np.array(n_cpts).astype(np.int32)
        """The number of CPTs [-] that have been taken into account to establish the Xi value."""
        self.xi_normative = np.array(xi_normative).astype(np.str_)
        """The normative Xi (either Xi_3 or Xi_4)"""
        self.xi_value = np.array(xi_value).astype(np.float64)
        """The Xi value [-] that was applied to calculate the characteristic value of the
        total bearing capacity."""
        self.cpt_normative = np.array(cpt_normative).astype(np.str_)
        """The normative CPT. Can be "group average" if that was found to be the normative scenario."""
        self.R_t_d_min = np.array(R_t_d_min).astype(np.float64)
        """The minimum of the single-CPT values for the calculated bearingcapacity [kN]."""
        self.R_t_d_mean = np.array(R_t_d_mean).astype(np.float64)
        """The mean of the single-CPT values for the calculated
                bearingcapacity [kN]."""
        self.R_t_d = np.array(R_t_d).astype(np.float64)
        """calculation value of the tensile resistance of a pile or pile group
            (7.6.3.3 (a) NEN 9997-1+C2:2017) [kN]"""
        self.R_t_d_plug = np.array(R_t_d_plug).astype(np.float64)
        """The design value of the total plug weight bearingcapacity [kN]."""

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
            self.R_t_d,
            self.pile_tip_level_nap,
            "-",
            label=r"$R_{t;d}$",
        )
        axes.plot(
            self.R_t_d_plug,
            self.pile_tip_level_nap,
            ":",
            label=r"$R_{t;d;kluit}$",
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


class SingleCPTTensionBearingResultsContainer:
    """A container that holds multiple SingleCPTBearingResults objects"""

    def __init__(self, cpt_results_dict: Dict[str, SingleCPTTensionBearingResults]):
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
    ) -> "SingleCPTTensionBearingResultsContainer":
        """
        Instantiates the SingleCPTBearingResultsContainer object from the "cpts" array,
        which is returned in the response of a "compression/multiple-cpts/results" endpoint call.
        """
        return cls(
            cpt_results_dict={
                cpt_results[
                    "test_id"
                ]: SingleCPTTensionBearingResults.from_api_response(
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

    def __getitem__(self, test_id: str) -> SingleCPTTensionBearingResults:
        if not isinstance(test_id, str):
            raise TypeError(f"Expected a test-id as a string, but got: {type(test_id)}")

        return self.get_cpt_results(test_id)

    @property
    def cpt_results_dict(self) -> Dict[str, SingleCPTTensionBearingResults]:
        """The dictionary that maps the cpt-names to SingleCPTBearingResults objects."""
        return self._cpt_results_dict

    @property
    def test_ids(self) -> List[str]:
        """The test-ids of the CPTs."""
        return list(self.cpt_results_dict.keys())

    @property
    def results(self) -> List[SingleCPTTensionBearingResults]:
        """The computed results, as a list of SingleCPTBearingResults objects."""
        return list(self.cpt_results_dict.values())

    def get_cpt_results(self, test_id: str) -> SingleCPTTensionBearingResults:
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
            raise ValueError(f"Invalid column_name: {column_name} provided.")

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
            pile_tip_level_nap=cpt_results_df.pile_tip_level_nap.round(2)
        )

        return cpt_results_df


class MultiCPTTensionBearingResults:
    """
    Object that contains the results of a PileCore multi-cpt calculation.

    *Not meant to be instantiated by the user.*
    """

    def __init__(
        self,
        cpt_results: SingleCPTTensionBearingResultsContainer,
        group_results_table: CPTTensionGroupResultsTable,
        pile_properties: PileProperties,
        gamma_s_t: float,
        gamma_m_var_qc: float,
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
        gamma_s_t:
            Safety factor γ_s_t. Used to determine the tensile resistance of a pile. [-]
        gamma_m_var_qc:
            partial factor for the influence of load switching; NEN 9997-1+C2:2017 7.6.3.3 (d). [-]
        phi_plug:
            The effective angle of internal friction of the soil layer based on pile type [degrees].
        soil_load:
            (Fictive) load on soil used to calculate soil settlement [kPa]. This is
            required and used to determine settlement of pile w.r.t. soil.
        """
        self._pp = pile_properties
        self._gamma_s_t = gamma_s_t
        self._gamma_m_var_qc = gamma_m_var_qc
        self._soil_load = soil_load

        self._cpt_results = cpt_results

        self._group_results_table = group_results_table

    @classmethod
    def from_api_response(
        cls, response_dict: dict, cpt_input: dict
    ) -> "MultiCPTTensionBearingResults":
        """
        Build the object from the response payload of the PileCore endpoint
        "/compression/multi-cpt/results".
        """
        cpt_results_dict = SingleCPTTensionBearingResultsContainer.from_api_response(
            cpt_results_list=response_dict["cpts"], cpt_input=cpt_input
        )
        group_results = response_dict["group_results"]
        return cls(
            cpt_results=cpt_results_dict,
            pile_properties=PileProperties.from_api_response(
                response_dict["pile_properties"]
            ),
            group_results_table=CPTTensionGroupResultsTable(
                pile_tip_level_nap=group_results["pile_tip_level_nap"],
                var_coef=group_results["var_coef"],
                n_cpts=group_results["n_cpts"],
                xi_value=group_results["xi_value"],
                xi_normative=group_results["xi_normative"],
                cpt_normative=group_results["cpt_normative"],
                R_t_d_min=group_results["R_t_d_min"],
                R_t_d_mean=group_results["R_t_d_mean"],
                R_t_d=group_results["R_t_d"],
                R_t_d_plug=group_results["R_t_d_plug"],
            ),
            gamma_s_t=response_dict["calculation_params"]["gamma_s_t"],
            soil_load=response_dict["calculation_params"]["soil_load"],
            gamma_m_var_qc=response_dict["calculation_params"]["gamma_m_var_qc"],
        )

    @property
    def pile_properties(self) -> PileProperties:
        """
        The PileProperties object.
        """
        return self._pp

    @property
    def cpt_results(self) -> SingleCPTTensionBearingResultsContainer:
        """The SingleCPTBearingResultsContainer object."""
        return self._cpt_results

    @property
    def cpt_names(self) -> List[str]:
        """The test-ids of the CPTs."""
        return self.cpt_results.test_ids

    @property
    def group_results_table(self) -> CPTTensionGroupResultsTable:
        """The CPTGroupResultsTable dataclass, containing the group results."""
        return self._group_results_table
