"""
Integration tests for the full Grouper pipeline driven by a CustomBearingResults
(bring-your-own bearing numbers), plus the equivalence guarantee against the PileCore
path.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from nuclei.client.utils import serialize_jsonifyable_object
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from requests import Request

from pypilecore.input import (
    create_grouper_payload_from_bearing_results,
    create_grouper_report_payload,
)
from pypilecore.results import (
    CustomBearingResults,
    GrouperResults,
    MultiCPTCompressionBearingResults,
)
from pypilecore.results.cases_grouper_results import CasesGrouperResults
from pypilecore.viewers.viewer_grouper_results_per_cpt_table import (
    ViewerGrouperResultsPerCptTable,
)


def test_custom_path_equivalent_to_pilecore_path(
    mock_group_cpts_response: dict,
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
    mock_custom_bearing_results: CustomBearingResults,
) -> None:
    """
    Same numbers -> equivalent grouper payload AND equivalent folded cpt_results on both
    the PileCore and the custom path. This proves the seam is source-agnostic.
    """
    multi_cpt_bearing_results = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_group_multi_cpt_bearing_response,
        cpt_input=mock_group_results_passover,
    )
    custom = mock_custom_bearing_results

    # Equivalent payload.
    assert create_grouper_payload_from_bearing_results(
        custom
    ) == create_grouper_payload_from_bearing_results(multi_cpt_bearing_results)

    # Equivalent folded cpt_results.
    grouper_reference = GrouperResults.from_grouper_response(
        mock_group_cpts_response, 100, multi_cpt_bearing_results
    )
    grouper_custom = GrouperResults.from_grouper_response(
        mock_group_cpts_response, 100, custom
    )

    assert grouper_custom.cpt_results.test_ids == grouper_reference.cpt_results.test_ids
    for test_id in grouper_reference.cpt_results.test_ids:
        reference_table = grouper_reference.cpt_results[test_id].table
        custom_table = grouper_custom.cpt_results[test_id].table
        np.testing.assert_allclose(
            custom_table.pile_tip_level_nap,
            reference_table.pile_tip_level_nap,
            equal_nan=True,
        )
        np.testing.assert_allclose(
            custom_table.R_c_d_net, reference_table.R_c_d_net, equal_nan=True
        )
        np.testing.assert_allclose(
            custom_table.F_nk_d, reference_table.F_nk_d, equal_nan=True
        )
        np.testing.assert_array_equal(custom_table.origin, reference_table.origin)


def test_custom_path_full_pipeline(
    mock_group_cpts_response: dict,
    mock_custom_bearing_results: CustomBearingResults,
    mock_cases_grouper_results_custom: dict,
    pc_openapi,
) -> None:
    """Drive the whole Grouper flow from a CustomBearingResults using mocked responses."""
    custom = mock_custom_bearing_results

    # 1. Payload -> validates against the Grouper endpoint schema.
    payload = create_grouper_payload_from_bearing_results(custom)
    request = Request(
        method="POST",
        headers={"Content-Type": "application/json"},
        url="http://grouper/group-cpts",
        json=serialize_jsonifyable_object(payload),
    )
    pc_openapi.request_validator.validate(RequestsOpenAPIRequest(request))

    # 2. Wrap the (mocked) API response.
    grouper_results = GrouperResults.from_grouper_response(
        mock_group_cpts_response, 100, custom
    )

    # 3. Fold + scatter (plot) + plan (map) viewers.
    max_bearing_results = grouper_results.cpt_results
    assert isinstance(max_bearing_results.plot(), plt.Figure)
    plt.close("all")
    assert isinstance(max_bearing_results.map(pile_tip_level_nap=-15), plt.Figure)
    plt.close("all")
    assert isinstance(grouper_results.plot(), plt.Figure)
    plt.close("all")
    assert isinstance(grouper_results.map(), plt.Figure)
    plt.close("all")

    # 4. Cases + table viewer on the custom path.
    cases = CasesGrouperResults(**mock_cases_grouper_results_custom)
    assert isinstance(cases.cpt_results_table.to_pandas(), pd.DataFrame)
    table_viewer = ViewerGrouperResultsPerCptTable(cases)
    assert isinstance(table_viewer.to_pandas(), pd.DataFrame)

    # 5. Report payload needs nothing from bearing results beyond payload + response.
    report_payload = create_grouper_report_payload(
        grouper_payload=payload,
        grouper_response=mock_group_cpts_response,
        project_name="Custom project",
        project_id="CUSTOM-1",
        author="Tester",
    )
    assert "sub_groups" in report_payload
    assert "cpt_objects" not in report_payload
