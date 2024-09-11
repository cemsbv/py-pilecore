from __future__ import annotations  # noqa: F404

from typing import Dict, Hashable, List

import pandas as pd
from natsort import natsorted
from pygef.common import Location

from pypilecore.results.multi_cpt_results import MultiCPTBearingResults
from pypilecore.results.result_definitions import (
    CPTGroupResultDefinitions,
    CPTResultDefinitions,
)


class CasesMultiCPTBearingResults:
    """
    Container class for the results of multiple cases of MultiCPTBearingResults.
    It expects that all MultiCPTBearingResults objects have the same pile tip levels and same test ids.
    """

    def __init__(
        self,
        results_per_case: Dict[Hashable, MultiCPTBearingResults],
        cpt_locations: Dict[str, Location],
    ) -> None:
        """
        Initialize the class with the results of multiple cases of MultiCPTBearingResults.

        Parameters
        ----------
        results_per_case : Dict[Hashable, MultiCPTBearingResults]
            A dictionary with the results of multiple cases of MultiCPTBearingResults.
            The keys of the dictionary are the case names.
            All MultiCPTBearingResults objects must have the same pile tip levels and same test ids.
        cpt_locations : Dict[str, Location]
            The mapping between `test_id` (key) and the `location` (value) of the cpt.
            The keys must contain all the `test_id` (s) used in the MultiCPTBearingResults objects.

        Raises
        ------
        TypeError
            If `results_per_case` is not of the expected type.
            If `cpt_locations` is not of the expected type.
        ValueError
            If `results_per_case` is an empty dictionary.
            If not all MultiCPTBearingResults objects have the same pile tip levels and test ids.
            If not all the `test_id` (s) used in the MultiCPTBearingResults objects are in the keys of `cpt_locations`.
        """
        # Validate results cases
        _validate_results_per_case(results_per_case)

        # Initialize private variables
        self._cases = natsorted(list(results_per_case.keys()))
        self._multicpt_bearing_results = [results_per_case[c] for c in self.cases]
        self._test_ids = natsorted(
            results_per_case[list(results_per_case.keys())[0]].cpt_results.test_ids
        )
        self._pile_tip_levels_nap = sorted(
            list(
                results_per_case[list(results_per_case.keys())[0]]
                .cpt_results.to_pandas()
                .pile_tip_level_nap.unique()
            ),
            reverse=True,
        )
        self._set_cpt_locations(cpt_locations)

        # Create cpt_results_dataframe and cpt_group_results_dataframe
        self._set_cpt_results_dataframe(results_per_case)
        self._set_cpt_group_results_dataframe(results_per_case)

    def _set_cpt_results_dataframe(
        self, results_per_case: Dict[Hashable, MultiCPTBearingResults]
    ) -> None:
        """Private method to create and set the property `cpt_results_dataframe`."""
        records = []
        for case_name, case_results in results_per_case.items():
            for result_definition in CPTResultDefinitions:
                df = case_results.cpt_results.get_results_per_cpt(
                    column_name=result_definition.name
                )
                for idx_row, row in df.iterrows():
                    for test_id, result in row.items():
                        records.append(
                            dict(
                                case_name=case_name,
                                result_name=result_definition.name,
                                test_id=test_id,
                                x=self.cpt_locations[test_id].x,
                                y=self.cpt_locations[test_id].y,
                                pile_tip_level_nap=idx_row,
                                result=result,
                                result_unit=result_definition.value.unit,
                            )
                        )
        self._cpt_results_dataframe = pd.DataFrame.from_records(records)

    def _set_cpt_group_results_dataframe(
        self, result_cases: Dict[Hashable, MultiCPTBearingResults]
    ) -> None:
        """Private method to create and set the property `cpt_group_results_dataframe`."""
        records = []
        for case_name, case_results in result_cases.items():
            df = case_results.group_results_table.to_pandas()
            for result_definition in CPTGroupResultDefinitions:
                for _, row in df.iterrows():
                    records.append(
                        dict(
                            case_name=case_name,
                            result_name=result_definition.name,
                            pile_tip_level_nap=row["pile_tip_level_nap"],
                            result=row[result_definition.value.name],
                            result_unit=result_definition.value.unit,
                        )
                    )
        self._cpt_group_results_dataframe = pd.DataFrame.from_records(records)

    def _set_cpt_locations(self, value: Dict[str, Location]) -> None:
        """Private setter for `cpt_locations`."""
        # Check data types
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected type 'List[CPTData]' for 'cpt_locations', but got {type(value)}"
            )

        if not all(isinstance(k, str) for k in value.keys()):
            raise TypeError(
                f"Expected type 'str' for keys of 'cpt_locations', but got {(type(k) for k in value.keys())}"
            )

        if not all(isinstance(v, Location) for v in value.values()):
            raise TypeError(
                f"Expected type 'Location' for values of 'cpt_locations', but got {(type(v) for v in value.values())}"
            )

        # Check that all the `test_id`s used in the MultiCPTBearingResults objects are in the keys.
        if not all(test_id in value.keys() for test_id in self.test_ids):
            missing_test_ids = [
                test_id for test_id in self.test_ids if test_id not in value.keys()
            ]
            raise ValueError(
                "Not all `test_id`s used in the MultiCPTBearingResults objects are in the keys of `cpt_locations`. "
                + f"The following `test_id`s are missing: {missing_test_ids}"
            )

        self._cpt_locations = value

    @property
    def cases(self) -> List[Hashable]:
        """The case names."""
        return self._cases

    @property
    def multicpt_bearing_results(self) -> List[MultiCPTBearingResults]:
        """The MultiCPTBearingResults objects."""
        return self._multicpt_bearing_results

    @property
    def test_ids(self) -> List[str]:
        """The test ids of all MultiCPTBearingResults objects."""
        return self._test_ids

    @property
    def pile_tip_levels_nap(self) -> List[float]:
        """The pile tip levels NAP of all MultiCPTBearingResults objects."""
        return self._pile_tip_levels_nap

    @property
    def cpt_locations(self) -> Dict[str, Location]:
        """The mapping between `test_id` (key) and the `location` (value) of the cpt."""
        return self._cpt_locations

    @property
    def cpt_results_dataframe(self) -> pd.DataFrame:
        """
        The dataframe with all the CPT results.
        Available columns: case_name, result_name, test_id, x, y, pile_tip_level_nap, result, result_unit.
        """
        return self._cpt_results_dataframe

    @property
    def cpt_group_results_dataframe(self) -> pd.DataFrame:
        """
        The dataframe with CPT group results.
        Available columns: case_name, result_name, pile_tip_level_nap, result, result_unit.
        """
        return self._cpt_group_results_dataframe


def _validate_results_per_case(
    results_per_case: Dict[Hashable, MultiCPTBearingResults]
) -> None:
    """
    Private method to validate the results_per_case dictionary.

    Parameters
    ----------
    results_per_case : Dict[Hashable, MultiCPTBearingResults]
        A dictionary with the results of multiple cases of MultiCPTBearingResults.
        The keys of the dictionary are the case names.
        All MultiCPTBearingResults objects must have the same pile tip levels and same test ids.

    Raises
    ------
    TypeError
        If `results_per_case` is not of the expected type.
    ValueError
        If `results_per_case` is an empty dictionary.
        If not all MultiCPTBearingResults objects have the same pile tip levels and test ids.
    """
    if not isinstance(results_per_case, dict):
        raise TypeError(
            f"Expected type 'Dict[Hashable, MultiCPTBearingResults]' for 'results_per_case', but got {type(results_per_case)}"
        )

    if len(results_per_case) == 0:
        raise ValueError("Empty dictionary 'results_per_case' is not allowed.")

    for val in results_per_case.values():
        if not isinstance(val, MultiCPTBearingResults):
            raise TypeError(
                f"Expected type 'MultiCPTBearingResults' for items in 'results_per_case', but got {type(val)}"
            )

    test_ids = results_per_case[list(results_per_case.keys())[0]].cpt_results.test_ids
    pile_tip_levels_nap = list(
        results_per_case[list(results_per_case.keys())[0]]
        .cpt_results.to_pandas()
        .pile_tip_level_nap.unique()
    )
    for results in results_per_case.values():
        if results.cpt_results.test_ids != test_ids:
            raise ValueError(
                "All MultiCPTBearingResults objects must have the same test ids."
            )

        if (
            list(results.cpt_results.to_pandas().pile_tip_level_nap.unique())
            != pile_tip_levels_nap
        ):
            raise ValueError(
                "All MultiCPTBearingResults objects must have the same pile tip levels."
            )
