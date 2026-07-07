"""
Tier-2 enrichment: attaching a raw CPT trace + soil layers (a full SoilProperties) to a
CustomCptBearingResult unlocks the per-CPT bearing-overview plots, while Tier-1 (numbers +
coordinates only) still works everywhere else.
"""

import matplotlib.pyplot as plt
import pytest
from pygef.common import Location

from pypilecore.exceptions import UserError
from pypilecore.input import create_grouper_payload_from_bearing_results
from pypilecore.results import (
    CustomBearingResults,
    CustomCptBearingResult,
    GrouperResults,
    MultiCPTCompressionBearingResults,
)
from pypilecore.results.cases_grouper_results import CasesGrouperResults
from pypilecore.results.soil_properties import SoilProperties
from pypilecore.viewers.viewer_cpt_results_overview import ViewerCptResultsOverview


def _tier2_custom_from_multi_cpt(
    multi_cpt_bearing_results: MultiCPTCompressionBearingResults,
) -> CustomBearingResults:
    """CustomBearingResults with the full SoilProperties trace attached to each CPT."""
    records = []
    for name, result in multi_cpt_bearing_results.cpt_results.cpt_results_dict.items():
        soil_properties = result.soil_properties
        records.append(
            CustomCptBearingResult(
                test_id=name,
                x=soil_properties.x,
                y=soil_properties.y,
                pile_tip_level_nap=result.table.pile_tip_level_nap,
                R_b_cal=result.table.R_b_cal,
                R_s_cal=result.table.R_s_cal,
                F_nk_d=result.table.F_nk_d,
                R_c_d_net=result.table.R_c_d_net,
                soil_properties=soil_properties,
            )
        )
    return CustomBearingResults(records)


def test_tier2_attached_trace_unlocks_overview_plots(
    mock_group_cpts_response: dict,
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
) -> None:
    """A CPT with an attached full SoilProperties produces the overview plot / viewer."""
    multi_cpt_bearing_results = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_group_multi_cpt_bearing_response,
        cpt_input=mock_group_results_passover,
    )
    custom = _tier2_custom_from_multi_cpt(multi_cpt_bearing_results)

    grouper_results = GrouperResults.from_grouper_response(
        mock_group_cpts_response, 100, custom
    )

    test_id = grouper_results.cpt_results.test_ids[0]
    overview = grouper_results.cpt_results[test_id].plot_bearing_overview()
    assert isinstance(overview, plt.Figure)
    plt.close("all")

    # The overview viewer (which plots the first CPT on construction) also works.
    cpt_locations = {
        cpt_id: Location(srs_name="RD", **info["location"])
        for cpt_id, info in mock_group_results_passover.items()
    }
    cases = CasesGrouperResults(
        results_per_case={"case_1": grouper_results},
        cpt_locations=cpt_locations,
    )
    viewer = ViewerCptResultsOverview(cases)
    assert viewer._layout is not None
    plt.close("all")


def test_tier1_overview_raises_but_tier1_flow_succeeds(
    mock_group_cpts_response: dict,
    mock_custom_bearing_results: CustomBearingResults,
) -> None:
    """
    Without soil data, the overview plot raises the clear 'requires soil data' error,
    while the Tier-1 payload and scatter plot still succeed.
    """
    custom = mock_custom_bearing_results  # Tier-1: no soil trace attached
    grouper_results = GrouperResults.from_grouper_response(
        mock_group_cpts_response, 100, custom
    )

    test_id = grouper_results.cpt_results.test_ids[0]
    with pytest.raises(UserError, match="requires soil data"):
        grouper_results.cpt_results[test_id].plot_bearing_overview()

    # Tier-1 still works: payload builds and the scatter plot renders.
    assert isinstance(create_grouper_payload_from_bearing_results(custom), dict)
    assert isinstance(grouper_results.cpt_results.plot(), plt.Figure)
    plt.close("all")


def test_tier2_soil_properties_disagreement_fails_loud() -> None:
    """
    Regression (from the Tier-2 angle): a SoilProperties whose test_id/x/y disagree with
    the declared params is rejected at construction.
    """
    mismatched = SoilProperties(test_id="WRONG", x=0.0, y=0.0)
    with pytest.raises(ValueError, match="does not match"):
        CustomCptBearingResult(
            test_id="CPT-1",
            x=0.0,
            y=0.0,
            pile_tip_level_nap=[-10.0, -11.0],
            R_b_cal=[100.0, 110.0],
            R_s_cal=[50.0, 55.0],
            F_nk_d=[10.0, 10.0],
            R_c_d_net=[120.0, 130.0],
            soil_properties=mismatched,
        )
