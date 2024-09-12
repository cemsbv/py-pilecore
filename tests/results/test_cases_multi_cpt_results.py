from typing import Any, Type

import pytest
from pygef.common import Location

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults


def test_cases_multi_cpt_results_init_valid_input(
    mock_cases_multi_cpt_bearing_results_valid_data: dict,
) -> None:
    """Tests the initialization of the CasesMultiCPTBearingResults class with valid input."""
    cases_multicpt_results = CasesMultiCPTBearingResults(
        **mock_cases_multi_cpt_bearing_results_valid_data
    )

    cptgroupresults = mock_cases_multi_cpt_bearing_results_valid_data[
        "results_per_case"
    ]["case_1"]

    assert cases_multicpt_results.cases == ["case_1", "case_2"]
    assert cases_multicpt_results.multicpt_bearing_results == [
        cptgroupresults,
        cptgroupresults,
    ]
    assert all(
        cpt_name in cases_multicpt_results.test_ids
        for cpt_name in cptgroupresults.cpt_names
    )
    assert all(
        pile_tip_level_nap in cases_multicpt_results.pile_tip_levels_nap
        for pile_tip_level_nap in cptgroupresults.cpt_results.to_pandas().pile_tip_level_nap.unique()
    )

    assert cases_multicpt_results.cpt_results_dataframe.columns.to_list() == [
        "case_name",
        "result_name",
        "test_id",
        "x",
        "y",
        "pile_tip_level_nap",
        "result",
        "result_unit",
    ]
    assert cases_multicpt_results.cpt_group_results_dataframe.columns.to_list() == [
        "case_name",
        "result_name",
        "pile_tip_level_nap",
        "result",
        "result_unit",
    ]


@pytest.mark.parametrize(
    "results_per_case,cpt_locations,expected_error,expected_message",
    [
        # Wrong type for results_per_case
        ("not a dict", "valid", TypeError, "'results_per_case'"),
        # Empty dict for result_cases
        ({}, "valid", ValueError, "'results_per_case'"),
        # Wrong type in results_per_case.values()
        ({"case_1": 1}, "valid", TypeError, "'results_per_case'"),
        # Not all MultiCPTBearingResults with same test_ids
        ("different_cpts", "different_cpts", ValueError, "same test ids"),
        # Not all MultiCPTBearingResults with same pile_tip_levels_nap
        (
            "different_pile_tip_levels",
            "different_pile_tip_levels",
            ValueError,
            "same pile tip levels",
        ),
        # Wrong type for cpt_locations
        ("valid", "not a dict", TypeError, "'cpt_locations'"),
        # Wrong type in cpt_locations.keys()
        ("valid", {1: Location("RD", 0.0, 0.0)}, TypeError, "'cpt_locations'"),
        # Wrong type in cpt_locations.values()
        ("valid", {"cpt_1": 1}, TypeError, "'cpt_locations'"),
        # Not all test_ids in cpt_locations
        ("valid", {"5": Location("RD", 0.0, 0.0)}, ValueError, "Not all `test_id`s"),
    ],
)
def test_cases_multi_cpt_results_init_invalid_input(
    results_per_case: Any,
    cpt_locations: Any,
    expected_error: Type[Exception],
    expected_message: str,
    mock_cases_multi_cpt_bearing_results_valid_data: dict,
    mock_cases_multi_cpt_bearing_results_different_cpts: dict,
    mock_cases_multi_cpt_bearing_results_different_pile_tip_levels: dict,
) -> None:
    """
    Tests the initialization of the CasesMultiCPTBearingResults with invalid input returns the
    expected errors. Note that his also tests the private setters.
    """
    if results_per_case == "valid":
        results_per_case = mock_cases_multi_cpt_bearing_results_valid_data[
            "results_per_case"
        ]
    elif results_per_case == "different_cpts":
        results_per_case = mock_cases_multi_cpt_bearing_results_different_cpts[
            "results_per_case"
        ]
    elif results_per_case == "different_pile_tip_levels":
        results_per_case = (
            mock_cases_multi_cpt_bearing_results_different_pile_tip_levels[
                "results_per_case"
            ]
        )

    if cpt_locations == "valid":
        cpt_locations = mock_cases_multi_cpt_bearing_results_valid_data["cpt_locations"]
    elif cpt_locations == "different_cpts":
        cpt_locations = mock_cases_multi_cpt_bearing_results_different_cpts[
            "cpt_locations"
        ]
    elif cpt_locations == "different_pile_tip_levels":
        cpt_locations = mock_cases_multi_cpt_bearing_results_different_pile_tip_levels[
            "cpt_locations"
        ]

    with pytest.raises(expected_error, match=expected_message):
        CasesMultiCPTBearingResults(
            results_per_case=results_per_case,
            cpt_locations=cpt_locations,
        )
