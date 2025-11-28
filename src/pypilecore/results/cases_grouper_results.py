from __future__ import annotations

from enum import StrEnum
from typing import Dict, Hashable, List

import pandas as pd
from natsort import natsorted
from pygef.common import Location

from pypilecore.results.grouper_result import GrouperResults
from pypilecore.results.result_definitions import GrouperResultsDefinition


class ClusterResultColumn(StrEnum):
    characteristic_bearing_capacity = "characteristic_bearing_capacity"
    design_bearing_capacity = "design_bearing_capacity"
    design_negative_friction = "design_negative_friction"
    group_centre_to_centre_validation = "group_centre_to_centre_validation"
    group_centre_to_centre_validation_15 = "group_centre_to_centre_validation_15"
    group_centre_to_centre_validation_20 = "group_centre_to_centre_validation_20"
    group_centre_to_centre_validation_25 = "group_centre_to_centre_validation_25"
    mean_calculated_bearing_capacity = "mean_calculated_bearing_capacity"
    min_calculated_bearing_capacity = "min_calculated_bearing_capacity"
    net_design_bearing_capacity = "net_design_bearing_capacity"
    nominal_cpt = "nominal_cpt"
    variation_coefficient = "variation_coefficient"
    xi_factor = "xi_factor"
    xi_values = "xi_values"


class Unit(StrEnum):
    kN = "kN"
    NONE = "-"


_CLUSTER_RESULT_UNITS = {
    ClusterResultColumn.characteristic_bearing_capacity.value: Unit.kN,
    ClusterResultColumn.design_bearing_capacity.value: Unit.kN,
    ClusterResultColumn.design_negative_friction.value: Unit.kN,
    ClusterResultColumn.group_centre_to_centre_validation.value: Unit.NONE,
    ClusterResultColumn.group_centre_to_centre_validation_15.value: Unit.NONE,
    ClusterResultColumn.group_centre_to_centre_validation_20.value: Unit.NONE,
    ClusterResultColumn.group_centre_to_centre_validation_25.value: Unit.NONE,
    ClusterResultColumn.mean_calculated_bearing_capacity.value: Unit.kN,
    ClusterResultColumn.min_calculated_bearing_capacity.value: Unit.kN,
    ClusterResultColumn.net_design_bearing_capacity.value: Unit.kN,
    ClusterResultColumn.nominal_cpt.value: Unit.NONE,
    ClusterResultColumn.variation_coefficient.value: Unit.NONE,
    ClusterResultColumn.xi_factor.value: Unit.NONE,
    ClusterResultColumn.xi_values.value: Unit.NONE,
}


class CasesGrouperResults:
    """
    Container class for the results of multiple cases of GrouperResults.
    It expects that all GrouperResults objects are based on MultiCPTBearingResults with the same pile tip levels and test ids.
    """

    def __init__(
        self,
        results_per_case: Dict[Hashable, GrouperResults],
        cpt_locations: Dict[str, Location],
    ) -> None:
        """
        Initialize the class with the results of multiple cases of GrouperResults.

        Parameters
        ----------
        results_per_case : Dict[Hashable, GrouperResults]
            A dictionary with the results of multiple cases of GrouperResults.
            The keys of the dictionary are the case names.
            All GrouperResults objects must be generated with MultiCPTBearingResults objects that have the same pile tip levels and test ids.
        cpt_locations : Dict[str, Location]
            The mapping between `test_id` (key) and the `location` (value) of the cpt.
            The keys must contain all the `test_id` (s) used in the GrouperResults objects.

        Raises
        ------
        TypeError
            If `results_per_case` is not of the expected type.
            If `cpt_locations` is not of the expected type.
        ValueError
            If `results_per_case` is an empty dictionary.
            If not all GrouperResults objects have the same pile tip levels and test ids.
            If not all the `test_id` (s) used in the GrouperResults objects are in the keys of `cpt_locations`.
        """
        _validate_results_per_case(results_per_case)

        self._cases = natsorted(list(results_per_case.keys()))
        self._grouper_results = [results_per_case[c] for c in self.cases]
        first_results = results_per_case[self.cases[0]]
        self._test_ids = natsorted(
            first_results.multi_cpt_bearing_results.cpt_results.test_ids
        )
        self._pile_tip_levels_nap = sorted(
            list(
                first_results.multi_cpt_bearing_results.cpt_results.to_pandas().pile_tip_level_nap.unique()
            ),
            reverse=True,
        )
        self._set_cpt_locations(cpt_locations)

        self._set_cpt_max_results_dataframe(results_per_case)

    def _set_cpt_max_results_dataframe(
        self, results_per_case: dict[Hashable, GrouperResults]
    ) -> None:
        """Private method to set the maximum results dataframe for each case."""
        records = []
        for case_name, case_results in results_per_case.items():
            max_results = case_results.max_bearing_results
            for result_definition in GrouperResultsDefinition:
                if result_definition.name in max_results.to_pandas().columns:
                    df = max_results.get_results_per_cpt(
                        column_name=result_definition.name
                    )
                    for ptl, row in df.iterrows():
                        for test_id, result in row.items():
                            records.append(
                                dict(
                                    case_name=case_name,
                                    result_name=result_definition.name,
                                    test_id=test_id,
                                    x=self.cpt_locations[test_id].x,
                                    y=self.cpt_locations[test_id].y,
                                    pile_tip_level_nap=ptl,
                                    result=result,
                                    result_unit=result_definition.value.unit,
                                )
                            )

        self._max_bearing_results_dataframe = pd.DataFrame.from_records(records)

    def _set_cpt_locations(self, value: Dict[str, Location]) -> None:
        """Private setter for `cpt_locations`."""
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected type 'Dict[str, Location]' for 'cpt_locations', but got {type(value)}"
            )

        if not all(isinstance(k, str) for k in value.keys()):
            raise TypeError(
                f"Expected type 'str' for keys of 'cpt_locations', but got {(type(k) for k in value.keys())}"
            )

        if not all(isinstance(v, Location) for v in value.values()):
            raise TypeError(
                f"Expected type 'Location' for values of 'cpt_locations', but got {(type(v) for v in value.values())}"
            )

        if not all(test_id in value.keys() for test_id in self.test_ids):
            missing_test_ids = [
                test_id for test_id in self.test_ids if test_id not in value.keys()
            ]
            raise ValueError(
                "Not all `test_id`s used in the GrouperResults objects are in the keys of `cpt_locations`. "
                + f"The following `test_id`s are missing: {missing_test_ids}"
            )

        self._cpt_locations = value

    @property
    def cases(self) -> List[Hashable]:
        """The case names."""
        return self._cases

    @property
    def grouper_results(self) -> List[GrouperResults]:
        """The GrouperResults objects."""
        return self._grouper_results

    @property
    def test_ids(self) -> List[str]:
        """The test ids of all GrouperResults objects."""
        return self._test_ids

    @property
    def pile_tip_levels_nap(self) -> List[float]:
        """The pile tip levels NAP of all GrouperResults objects."""
        return self._pile_tip_levels_nap

    @property
    def cpt_locations(self) -> Dict[str, Location]:
        """The mapping between `test_id` (key) and the `location` (value) of the cpt."""
        return self._cpt_locations

    @property
    def cpt_results_dataframe(self) -> pd.DataFrame:
        """DataFrame with the maximum bearing results of all cases."""
        return self._max_bearing_results_dataframe


def _validate_results_per_case(
    results_per_case: Dict[Hashable, GrouperResults],
) -> None:
    """
    Private method to validate the results_per_case dictionary.

    Parameters
    ----------
    results_per_case : Dict[Hashable, GrouperResults]
        A dictionary with the results of multiple cases of GrouperResults.
        The keys of the dictionary are the case names.
        All GrouperResults objects must be generated with MultiCPTBearingResults objects that have the same pile tip levels and test ids.

    Raises
    ------
    TypeError
        If `results_per_case` is not of the expected type.
    ValueError
        If `results_per_case` is an empty dictionary.
        If not all GrouperResults objects have the same pile tip levels and test ids.
    """
    if not isinstance(results_per_case, dict):
        raise TypeError(
            f"Expected type 'Dict[Hashable, GrouperResults]' for 'results_per_case', but got {type(results_per_case)}"
        )

    if len(results_per_case) == 0:
        raise ValueError("Empty dictionary 'results_per_case' is not allowed.")

    for val in results_per_case.values():
        if not isinstance(val, GrouperResults):
            raise TypeError(
                f"Expected type 'GrouperResults' for items in 'results_per_case', but got {type(val)}"
            )

    first_key = list(results_per_case.keys())[0]
    test_ids = results_per_case[
        first_key
    ].multi_cpt_bearing_results.cpt_results.test_ids
    pile_tip_levels_nap = list(
        results_per_case[first_key]
        .multi_cpt_bearing_results.cpt_results.to_pandas()
        .pile_tip_level_nap.unique()
    )
    for results in results_per_case.values():
        if results.multi_cpt_bearing_results.cpt_results.test_ids != test_ids:
            raise ValueError("All GrouperResults objects must have the same test ids.")

        if (
            list(
                results.multi_cpt_bearing_results.cpt_results.to_pandas().pile_tip_level_nap.unique()
            )
            != pile_tip_levels_nap
        ):
            raise ValueError(
                "All GrouperResults objects must have the same pile tip levels."
            )
