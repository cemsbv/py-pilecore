from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Dict, List, Sequence, Tuple

import natsort
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import NDArray
from shapely import MultiPoint

from pypilecore.results.multi_cpt_results import MultiCPTBearingResults
from pypilecore.results.post_processing import (
    MaxBearingResult,
    MaxBearingResults,
    MaxBearingTable,
)


class SingleClusterData:
    """
    Data for a single CPT subgroup
    *Not meant to be instantiated by the user.*
    """

    def __init__(
        self,
        characteristic_bearing_capacity: Sequence[float],
        design_bearing_capacity: Sequence[float],
        design_negative_friction: Sequence[float],
        group_centre_to_centre_validation: Sequence[bool],
        group_centre_to_centre_validation_15: Sequence[bool],
        group_centre_to_centre_validation_20: Sequence[bool],
        group_centre_to_centre_validation_25: Sequence[bool],
        mean_calculated_bearing_capacity: Sequence[float],
        min_calculated_bearing_capacity: Sequence[float],
        net_design_bearing_capacity: Sequence[float],
        nominal_cpt: Sequence[str],
        pile_tip_level: Sequence[float],
        variation_coefficient: Sequence[float],
        xi_factor: Sequence[str],
        xi_values: Sequence[float],
    ):
        """
        Parameters
        ----------
        characteristic_bearing_capacity:
            characteristic bearing capacity [kN]
        design_bearing_capacity:
            design bearing capacity [kN]
        design_negative_friction:
            design negative friction [kN]
        group_centre_to_centre_validation:
            group centre to centre validation
        group_centre_to_centre_validation_15:
            group centre to centre validation 15 meter
        group_centre_to_centre_validation_20:
            group centre to centre validation 20 meter
        group_centre_to_centre_validation_25:
            group centre to centre validation 25 meter
        mean_calculated_bearing_capacity:
            mean calculated bearing capacity [kN]
        min_calculated_bearing_capacity:
            min calculated bearing capacity [kN]
        net_design_bearing_capacity:
            net design bearing capacity [kN]
        nominal_cpt:
            nominal cpt
        pile_tip_level:
            pile tip level [m w.r.t NAP]
        variation_coefficient:
            variation coefficient [-]
        xi_factor:
            xi factor
        xi_values:
            xi values [-]
        """
        self._characteristic_bearing_capacity = characteristic_bearing_capacity
        self._design_bearing_capacity = design_bearing_capacity
        self._design_negative_friction = design_negative_friction
        self._group_centre_to_centre_validation = group_centre_to_centre_validation
        self._group_centre_to_centre_validation_15 = (
            group_centre_to_centre_validation_15
        )
        self._group_centre_to_centre_validation_20 = (
            group_centre_to_centre_validation_20
        )
        self._group_centre_to_centre_validation_25 = (
            group_centre_to_centre_validation_25
        )
        self._mean_calculated_bearing_capacity = mean_calculated_bearing_capacity
        self._min_calculated_bearing_capacity = min_calculated_bearing_capacity
        self._net_design_bearing_capacity = net_design_bearing_capacity
        self._nominal_cpt = nominal_cpt
        self._pile_tip_level = pile_tip_level
        self._variation_coefficient = variation_coefficient
        self._xi_factor = xi_factor
        self._xi_values = xi_values

        raw_lengths = [len(values) for values in self.__dict__.values()]
        if len(list(set(raw_lengths))) > 1:
            raise ValueError("All values in this dataclass must have the same length.")

    @property
    def characteristic_bearing_capacity(self) -> NDArray[np.float64]:
        """Characteristic bearing capacity [kN]"""
        return np.array(self._characteristic_bearing_capacity).astype(np.float64)

    @property
    def design_bearing_capacity(self) -> NDArray[np.float64]:
        """Design bearing capacity [kN]"""
        return np.array(self._design_bearing_capacity).astype(np.float64)

    @property
    def design_negative_friction(self) -> NDArray[np.float64]:
        """Design negative friction [kN]"""
        return np.array(self._design_negative_friction).astype(np.float64)

    @property
    def group_centre_to_centre_validation(self) -> NDArray[np.bool_]:
        """Group centre to centre validation"""
        return np.array(self._group_centre_to_centre_validation).astype(np.bool_)

    @property
    def group_centre_to_centre_validation_15(self) -> NDArray[np.bool_]:
        """Group centre to centre validation 15 meter"""
        return np.array(self._group_centre_to_centre_validation_15).astype(np.bool_)

    @property
    def group_centre_to_centre_validation_20(self) -> NDArray[np.bool_]:
        """Group centre to centre validation 20 meter"""
        return np.array(self._group_centre_to_centre_validation_20).astype(np.bool_)

    @property
    def group_centre_to_centre_validation_25(self) -> NDArray[np.bool_]:
        """Group centre to centre validation 25 meter"""
        return np.array(self._group_centre_to_centre_validation_25).astype(np.bool_)

    @property
    def mean_calculated_bearing_capacity(self) -> NDArray[np.float64]:
        """Mean calculated bearing capacity [kN]"""
        return np.array(self._mean_calculated_bearing_capacity).astype(np.float64)

    @property
    def min_calculated_bearing_capacity(self) -> NDArray[np.float64]:
        """Min calculated bearing capacity [kN]"""
        return np.array(self._min_calculated_bearing_capacity).astype(np.float64)

    @property
    def net_design_bearing_capacity(self) -> NDArray[np.float64]:
        """Net design bearing capacity [kN]"""
        return np.array(self._net_design_bearing_capacity).astype(np.float64)

    @property
    def nominal_cpt(self) -> NDArray[np.str_]:
        """Nominal cpt"""
        return np.array(self._nominal_cpt).astype(str)

    @property
    def pile_tip_level(self) -> NDArray[np.float64]:
        """Pile tip level [m w.r.t NAP]"""
        return np.array(self._pile_tip_level).astype(np.float64)

    @property
    def variation_coefficient(self) -> NDArray[np.float64]:
        """Variation coefficient [-]"""
        return np.array(self._variation_coefficient).astype(np.float64)

    @property
    def xi_factor(self) -> NDArray[np.str_]:
        """Xi factor"""
        return np.array(self._xi_factor).astype(str)

    @property
    def xi_values(self) -> NDArray[np.float64]:
        """Xi values [-]"""
        return np.array(self._xi_values).astype(np.float64)

    @cached_property
    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self.__dict__)

    def plot_variation_coefficient(
        self, axes: Axes | None = None, **kwargs: Any
    ) -> None:
        """
        Plot the bearing capacity and variation coefficient in a subplot

        Parameters
        ----------
        axes:
            `plt.Axes` object where the data can be plotted on.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.
        """
        if axes is None:
            _, axes = plt.subplots(**kwargs)

        # create variation coefficient plot
        axes.plot(self.variation_coefficient, self.pile_tip_level, "o-")
        axes.axvline(x=0.12, color="black", linestyle="--")
        axes.grid()
        axes.set_xlabel("Variation coefficient [-]")

    def plot_bearing_capacity(
        self, axes: Axes | None = None, pile_load_uls: float = 0.0, **kwargs: Any
    ) -> None:
        """
        Plot the bearing capacity and variation coefficient in a subplot

        Note
        ------
        For the `Net bearing capacity` subplot there are two colors plotted:
         - orange:  conservative bearing capacity
         - blue:    net bearing capacity

        Parameters
        ----------
        axes:
            `plt.Axes` object where the data can be plotted on.
        pile_load_uls:
            Default is 0.0
            ULS load in kN.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.
        """
        if axes is None:
            _, axes = plt.subplots(**kwargs)

        # add net bearing capacity to plot
        axes.scatter(
            self.net_design_bearing_capacity,
            self.pile_tip_level,
            color=list(
                map(
                    lambda x: "tab:blue" if x <= 0.12 else "tab:orange",
                    self.variation_coefficient,
                )
            ),
        )
        axes.axvline(x=pile_load_uls, color="black", linestyle="--")
        axes.grid()
        axes.set_xlabel("Net bearing capacity [kN]")

    def plot_group_centre_to_centre_validation(
        self, axes: plt.Axes | None = None, **kwargs: Any
    ) -> None:
        """
        Plot the spacing checks in a subplot

        Note
        ------
        For the `spacing` subplot there are two colors plotted:
         - red:     invalid spacing
         - green:   valid spacing

        Parameters
        ----------
        axes:
            `plt.Axes` object where the data can be plotted on.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.
        """
        if axes is None:
            _, axes = plt.subplots(**kwargs)

        axes.scatter(
            [0] * len(self.pile_tip_level),
            self.pile_tip_level,
            marker="o",
            color=list(
                map(
                    lambda x: "tab:green" if x else "tab:red",
                    self.group_centre_to_centre_validation_25,
                )
            ),
        )
        axes.scatter(
            [1] * len(self.pile_tip_level),
            self.pile_tip_level,
            marker="s",
            color=list(
                map(
                    lambda x: "tab:green" if x else "tab:red",
                    self.group_centre_to_centre_validation_20,
                )
            ),
        )
        axes.scatter(
            [2] * len(self.pile_tip_level),
            self.pile_tip_level,
            marker="D",
            color=list(
                map(
                    lambda x: "tab:green" if x else "tab:red",
                    self.group_centre_to_centre_validation_15,
                )
            ),
        )
        axes.grid()
        axes.set_xticks([0, 1, 2], ["25", "20", "15"])
        axes.set_xlabel("CPT ctc [m]")

    def plot_xi(self, axes: plt.Axes | None = None, **kwargs: Any) -> None:
        """
        Plot the xi factor in a subplot

        Note
        ------
        For the `xi factor` subplot there are two colors plotted:
         - olive:   xi3
         - cyan:    xi4

        Parameters
        ----------
        axes:
            `plt.Axes` object where the data can be plotted on.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.
        """
        if axes is None:
            _, axes = plt.subplots(**kwargs)

        axes.scatter(
            self.xi_values,
            self.pile_tip_level,
            color=list(
                map(
                    lambda i: "tab:cyan" if i == "\u03BE4" else "tab:olive",
                    self.xi_factor,
                )
            ),
        )
        axes.grid()
        axes.set_xlabel("xi value [-]")


@dataclass(frozen=True)
class SingleClusterResult:
    """
    *Not meant to be instantiated by the user.*

    Attributes:
    ------------
    cpt_names: List[str]
        List of cpt names present in this cluster
    coordinates: List[Tuple[float, float]]
        List of coordinates present in this cluster
    pile_load_uls
        ULS load in kN. Used to determine if a grouping configuration is valid.
    maximum_pile_level: float
        maximum pile level [m w.r.t NAP]
    minimum_pile_level: float
        minimum pile level [m w.r.t NAP]
    number_of_consecutive_pile_levels: int
        number of consecutive pile levels
    pile_load_check: bool
        True if a minimum design pile bearing capacity based on the given pile load ULS at one or more
        pile-tip levels.
    spatial_check: bool
        True if cluster is spatially coherent, which means there are no other CPTs in between the members
        of the subgroup.
    variation_check: bool
        True if a maximum variation coefficient of 12% at one or more pile-tip levels.
    centre_to_centre_check: bool
        True if one of the conditions stated in NEN9997-1 3.2.3 is met at one or more pile-tip levels.
    data: SingleClusterData
        single cluster dataclass
    """

    cpt_names: List[str]
    coordinates: List[Tuple[float, float]]
    pile_load_uls: float
    maximum_pile_level: float
    minimum_pile_level: float
    number_of_consecutive_pile_levels: int
    pile_load_check: bool
    spatial_check: bool
    variation_check: bool
    centre_to_centre_check: bool
    data: SingleClusterData

    @classmethod
    def from_api_response(
        cls, response_dict: dict, pile_load_uls: float
    ) -> "SingleClusterResult":
        try:
            table = response_dict["table"]
            return cls(
                cpt_names=response_dict["names"],
                coordinates=response_dict["coordinates"],
                pile_load_uls=pile_load_uls,
                maximum_pile_level=response_dict["maximum_pile_level"],
                minimum_pile_level=response_dict["minimum_pile_level"],
                number_of_consecutive_pile_levels=response_dict[
                    "number_of_consecutive_pile_levels"
                ],
                pile_load_check=response_dict["pile_load_check"],
                spatial_check=response_dict["spatial_check"],
                variation_check=response_dict["variation_check"],
                centre_to_centre_check=response_dict["centre_to_centre_check"],
                data=SingleClusterData(
                    characteristic_bearing_capacity=table[
                        "characteristic_bearing_capacity"
                    ],
                    design_bearing_capacity=table["design_bearing_capacity"],
                    design_negative_friction=table["design_negative_friction"],
                    group_centre_to_centre_validation=table[
                        "group_centre_to_centre_validation"
                    ],
                    group_centre_to_centre_validation_15=table[
                        "group_centre_to_centre_validation_15"
                    ],
                    group_centre_to_centre_validation_20=table[
                        "group_centre_to_centre_validation_20"
                    ],
                    group_centre_to_centre_validation_25=table[
                        "group_centre_to_centre_validation_25"
                    ],
                    mean_calculated_bearing_capacity=table[
                        "mean_calculated_bearing_capacity"
                    ],
                    min_calculated_bearing_capacity=table[
                        "min_calculated_bearing_capacity"
                    ],
                    net_design_bearing_capacity=table["net_design_bearing_capacity"],
                    nominal_cpt=table["nominal_cpt"],
                    pile_tip_level=[round(elem, 2) for elem in table["pile_tip_level"]],
                    variation_coefficient=table["variation_coefficient"],
                    xi_factor=table["xi_factor"],
                    xi_values=table["xi_values"],
                ),
            )
        except KeyError as e:
            raise KeyError(
                "Response dictionary is missing an expected key.\n" rf"Traceback: {e}"
            )
        except ValueError as e:
            raise ValueError(
                f"Could not create `SingleClusterResult` class with the following cpts: {response_dict.get('names')} \n"
                rf"Traceback: {e}"
            )

    def map(
        self,
        figsize: Tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> plt.Figure:
        """
        Plot a map of the cpt locations

        Parameters
        ----------
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The `Axes` object where the data was plotted on.
        """

        # Create axes objects if not provided
        kwargs_subplot = {
            "figsize": figsize,
            "tight_layout": True,
        }

        kwargs_subplot.update(kwargs)

        fig, axes = plt.subplots(
            **kwargs_subplot,
        )

        # plot cpt
        xy = list(zip(*self.coordinates))
        axes = axes.scatter(x=xy[0], y=xy[1], color="grey")

        # add labels (cpt names) to map
        for x, y, label in zip(xy[0], xy[1], self.cpt_names):
            axes.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
        axes.ticklabel_format(useOffset=False, style="plain")
        return fig

    def plot(
        self,
        figsize: Tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> plt.Figure:
        """
        Plot contains the:
            - bearing capacity
            - variation coefficient
            - xi factor
            - centre to centre validation

        Note
        ------
        For the `Net bearing capacity` subplot there are two colors plotted:
         - orange:  conservative bearing capacity
         - blue:    net bearing capacity

        For the `xi factor` subplot there are two colors plotted:
         - olive:   xi3
         - cyan:    xi4

        For the `spacing` subplot there are two colors plotted:
         - red:     invalid spacing
         - green:   valid spacing

        Parameters
        ----------
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        figure:
            `plt.Figure` object.
        """

        kwargs_subplot = {
            "sharey": "row",
            "sharex": "col",
            "figsize": figsize,
        }

        kwargs_subplot.update(kwargs)

        fig, axes = plt.subplots(
            1,
            4,
            **kwargs_subplot,
        )
        # add plot variation coefficient
        self.data.plot_variation_coefficient(axes[0])

        # add plot bearing capacity
        self.data.plot_bearing_capacity(axes[1], self.pile_load_uls)

        # add xi table
        self.data.plot_xi(axes[2])

        # add centre to centre
        self.data.plot_group_centre_to_centre_validation(axes[3])

        return fig


@dataclass(frozen=True)
class GrouperResults:
    """
    *Not meant to be instantiated by the user.*

    Use the `from_api_response` method to instantiate the class.

    Attributes:
    ------------
    clusters: List[SingleClusterResult]
    """

    clusters: List[SingleClusterResult]
    multi_cpt_bearing_results: MultiCPTBearingResults

    def __post_init__(self) -> None:
        for cluster in self.clusters:
            for cpt_name in cluster.cpt_names:
                # check if the cpt names in the SingleClusterResults are also present
                # in the MultiCPTBearingResults
                if (
                    cpt_name
                    not in self.multi_cpt_bearing_results.cpt_results.cpt_results_dict.keys()
                ):
                    raise ValueError(
                        "CPT names dont match between MultiCPTBearingResults object and GrouperResults. "
                        "Make sure that you use the same MultiCPTBearingResults as you generated "
                        "the subgroups/clusters with."
                    )

                # Check that all the pile tip levels in the SingleClusterResults are
                # also present in the MultiCPTBearingResults
                for pile_tip_level in cluster.data.pile_tip_level:
                    if not np.isclose(
                        pile_tip_level,
                        self.multi_cpt_bearing_results.cpt_results.cpt_results_dict[
                            cpt_name
                        ].table.pile_tip_level_nap,
                        rtol=1e-2,
                    ).any():
                        raise ValueError(
                            "Pile tip levels dont match between MultiCPTBearingResults object and GrouperResults. "
                            "Make sure that you use the same MultiCPTBearingResults as you generated "
                            "the subgroups/clusters with."
                        )

    @classmethod
    def from_api_response(
        cls,
        response_dict: dict,
        pile_load_uls: float,
        multi_cpt_bearing_results: MultiCPTBearingResults,
    ) -> "GrouperResults":
        """
        Stores the response of the PileCore endpoint
        "/grouper/group_cpts"

        Parameters
        ----------
        response_dict:
           The resulting response of a call to `get_groups_api_result()`
        pile_load_uls:
            ULS load in kN. Used to determine if a grouping configuration is valid.
        multi_cpt_bearing_results:
           The container that holds multiple SingleCPTBearingResults objects
        """
        results = [
            SingleClusterResult.from_api_response(item, pile_load_uls)
            for item in response_dict["sub_groups"]
        ]
        return cls(
            clusters=results, multi_cpt_bearing_results=multi_cpt_bearing_results
        )

    @cached_property
    def max_bearing_results(self) -> "MaxBearingResults":
        """
        Get the results of the maximum net design bearing capacity (R_c_d_net) for every CPT.
        """
        max_bearing: Dict[str, Any] = {}

        # iterate over single cpt result
        for (
            cpt_name,
            _single_cpt_result,
        ) in self.multi_cpt_bearing_results.cpt_results.cpt_results_dict.items():
            single_cpt_result = deepcopy(_single_cpt_result)
            max_bearing[cpt_name] = dict(
                pile_head_level_nap=single_cpt_result.pile_head_level_nap,
                soil_properties=single_cpt_result.soil_properties,
                results_table=dict(
                    pile_tip_level_nap=single_cpt_result.table.pile_tip_level_nap,
                    R_c_d_net=single_cpt_result.table.R_c_d_net,
                    F_nk_d=single_cpt_result.table.F_nk_d,
                    origin=[f"CPT:{cpt_name}"]
                    * len(single_cpt_result.table.pile_tip_level_nap),
                ),
            )

        # iterate over subgroups result
        for cluster_idx, cluster in enumerate(self.clusters):
            # iterate over cpts in subgroup
            for cpt_name in cluster.cpt_names:
                # iterate over pile tip levels in the cluster results for the cpt
                for cluster_ptl_idx, ptl in enumerate(cluster.data.pile_tip_level):
                    # find corresponding pile tip level index in the max_bearing results
                    max_bearing_ptl_idx = np.abs(
                        max_bearing[cpt_name]["results_table"]["pile_tip_level_nap"]
                        - ptl
                    ).argmin()

                    # check bearing capacity
                    if cluster.data.net_design_bearing_capacity[
                        cluster_ptl_idx
                    ] > np.nan_to_num(
                        max_bearing[cpt_name]["results_table"]["R_c_d_net"][
                            max_bearing_ptl_idx
                        ]
                    ):
                        # replace data
                        max_bearing[cpt_name]["results_table"]["R_c_d_net"][
                            max_bearing_ptl_idx
                        ] = cluster.data.net_design_bearing_capacity[cluster_ptl_idx]
                        max_bearing[cpt_name]["results_table"]["F_nk_d"][
                            max_bearing_ptl_idx
                        ] = cluster.data.design_negative_friction[cluster_ptl_idx]
                        max_bearing[cpt_name]["results_table"]["origin"][
                            max_bearing_ptl_idx
                        ] = f"Group:{cluster_idx}"

        return MaxBearingResults(
            cpt_results_dict={
                cpt_name: MaxBearingResult(
                    pile_head_level_nap=data["pile_head_level_nap"],
                    soil_properties=data["soil_properties"],
                    table=MaxBearingTable(
                        pile_tip_level_nap=data["results_table"]["pile_tip_level_nap"],
                        R_c_d_net=data["results_table"]["R_c_d_net"],
                        F_nk_d=data["results_table"]["F_nk_d"],
                        origin=data["results_table"]["origin"],
                    ),
                )
                for cpt_name, data in max_bearing.items()
            }
        )

    def map(
        self,
        distance: float = 25.0,
        add_tags: bool = True,
        figsize: Tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> plt.Figure:
        """
        Plot a map of the valid subgroups.
        Plot contains the:

            - convex_hull of the subgroup with buffer distance
            - All CPT's with tag

        Parameters
        ----------
        distance : float, optional
            Default is 25.
            The buffer around the convex_hull of the subgroup
        add_tags : bool, optional
            default is True
            Show the CTP names as tags on the map
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        figure:
            The `Figure` object where the data was plotted on.
        """

        kwargs_subplot = {
            "figsize": figsize,
            "tight_layout": True,
        }

        kwargs_subplot.update(kwargs)

        figure, axes = plt.subplots(
            **kwargs_subplot,
        )

        for group_id, cluster in enumerate(self.clusters):
            # add cpts to plot
            xy = list(zip(*cluster.coordinates))
            axes.scatter(xy[0], xy[1], color="grey")

            if add_tags:
                for x, y, label in zip(xy[0], xy[1], cluster.cpt_names):
                    axes.annotate(
                        label, xy=(x, y), xytext=(3, 3), textcoords="offset points"
                    )

            # add group convex hull
            polygon = (
                MultiPoint(cluster.coordinates)
                .convex_hull.buffer(distance=distance)
                .exterior
            )
            axes.plot(polygon.xy[0], polygon.xy[1], label=f"Group {group_id}")

        axes.legend(bbox_to_anchor=(1, 1), loc="upper left")
        axes.ticklabel_format(useOffset=False, style="plain")

        return figure

    def plot(
        self,
        figsize: Tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> plt.Figure:
        """
        Plot a summary of the valid subgroups.

        Note
        -----
        Plot contains the:

            - cpts within a subgroup
                - green:
                    There are no other CPTs in between the members of the subgroup. The
                    group is also compliant with the NEN9997-1 3.2.3 centre to centre
                    validation.
                - orange:
                    There are no other CPTs in between the members of the subgroup. The
                    centre-to-centre check failed and so the group does not follow the
                    NEN9997-1 3.2.3 centre to centre validation.
                - red:
                    There are other CPTs in between the members of the subgroup.
            - valid depth of the subgroup

        Parameters
        ----------
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        figure:
            the `plt.Figure` object.
        """
        kwargs_subplot = {
            "sharex": "row",
            "figsize": figsize,
            "tight_layout": True,
        }

        kwargs_subplot.update(kwargs)

        figure, axes = plt.subplots(
            1,
            2,
            **kwargs_subplot,
        )

        # place holds needed to sort for plot
        group_id_list_sort = []
        cpt_names_list: List[str] = []
        color_list = []
        group_id_list = []

        for group_id, cluster in enumerate(self.clusters):
            group_id_list_sort.extend([group_id] * len(cluster.cpt_names))
            cpt_names_list.extend(cluster.cpt_names)
            color_list.extend(
                [
                    "tab:green"
                    if cluster.spatial_check and cluster.centre_to_centre_check
                    else "tab:orange"
                    if cluster.spatial_check and ~cluster.centre_to_centre_check
                    else "tab:red"
                ]
                * len(cluster.cpt_names)
            )
            valid_pile_level = np.array(cluster.data.pile_tip_level)[
                np.array(cluster.data.net_design_bearing_capacity)
                >= cluster.pile_load_uls
            ]
            axes[1].scatter([group_id] * len(valid_pile_level), valid_pile_level)
            group_id_list.append(group_id)

            data = pd.DataFrame(
                {
                    "group_id": group_id_list_sort,
                    "cpt_names": cpt_names_list,
                    "colors": color_list,
                }
            ).sort_values("cpt_names", ascending=False, key=natsort.natsort_keygen())
            axes[0].scatter(x="group_id", y="cpt_names", color="colors", data=data)
            axes[0].set_xlabel("Group ID")
            axes[0].set_xticks(group_id_list)
            axes[0].set_ylabel("CPT name")
            axes[0].grid(which="major", axis="both", alpha=0.1)

        axes[1].set_xlabel("Group ID")
        axes[1].set_ylabel("Depth [m NAP]")
        axes[1].grid(which="major", axis="both", alpha=0.1)

        return figure
