import inspect

import pytest
from nuclei.client.utils import serialize_jsonifyable_object
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from requests import Request

from pypilecore.input.grouper_properties import (
    create_grouper_payload,
    create_grouper_payload_from_bearing_results,
)
from pypilecore.results import (
    GrouperBearingResultsLike,
    MultiCPTCompressionBearingResults,
)
from pypilecore.results.compression.multi_cpt_results import (
    SingleCPTCompressionBearingResultsContainer,
)


@pytest.fixture()
def headers() -> dict:
    return {
        "Content-Type": "application/json",
    }


@pytest.fixture()
def grouper_multi_cpt_bearing_results(
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
) -> MultiCPTCompressionBearingResults:
    return MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_group_multi_cpt_bearing_response,
        cpt_input=mock_group_results_passover,
    )


def test_multi_cpt_results_satisfies_grouper_bearing_results_like(
    grouper_multi_cpt_bearing_results: MultiCPTCompressionBearingResults,
) -> None:
    """`MultiCPTCompressionBearingResults` satisfies the `GrouperBearingResultsLike` seam."""
    assert isinstance(grouper_multi_cpt_bearing_results, GrouperBearingResultsLike)


def test_create_grouper_payload_from_bearing_results_equals_dict_path(
    grouper_multi_cpt_bearing_results: MultiCPTCompressionBearingResults,
) -> None:
    """
    The source-agnostic payload builder produces the same payload from a PileCore
    `MultiCPTCompressionBearingResults` as the classic dict-based function.
    """
    payload_dict_path = create_grouper_payload(
        grouper_multi_cpt_bearing_results.cpt_results.cpt_results_dict
    )
    payload_bearing_path = create_grouper_payload_from_bearing_results(
        grouper_multi_cpt_bearing_results
    )

    assert payload_bearing_path == payload_dict_path


def test_create_grouper_payload_from_bearing_results_validates_against_openapi(
    grouper_multi_cpt_bearing_results: MultiCPTCompressionBearingResults,
    pc_openapi,
    headers: dict,
) -> None:
    """The payload built via the seam validates against the Grouper endpoint schema."""
    payload = create_grouper_payload_from_bearing_results(
        grouper_multi_cpt_bearing_results
    )

    request = Request(
        method="POST",
        headers=headers,
        url="http://grouper/group-cpts",
        json=serialize_jsonifyable_object(payload),
    )
    openapi_request = RequestsOpenAPIRequest(request)
    pc_openapi.request_validator.validate(openapi_request)


def test_create_grouper_payload_from_bearing_results_nan_defaults() -> None:
    """
    `create_grouper_payload_from_bearing_results` exposes the same NaN knobs and defaults
    as `create_grouper_payload`.
    """
    signature = inspect.signature(create_grouper_payload_from_bearing_results)
    assert signature.parameters["overrule_nan"].default == 0.0
    assert signature.parameters["skip_nan"].default is False


def test_pile_tip_levels_nap_returns_shared_grid(
    grouper_multi_cpt_bearing_results: MultiCPTCompressionBearingResults,
) -> None:
    """When all CPT grids agree, the adapter returns the shared grid, sorted descending."""
    levels = grouper_multi_cpt_bearing_results.pile_tip_levels_nap

    assert isinstance(levels, list)
    assert len(levels) > 0
    # Sorted descending.
    assert levels == sorted(levels, reverse=True)
    # Matches the pile_tip_level entry of the payload (which is the shared grid).
    payload = create_grouper_payload_from_bearing_results(
        grouper_multi_cpt_bearing_results
    )
    assert [round(level, 2) for level in levels] == [
        round(level, 2) for level in payload["pile_tip_level"]
    ]


def test_pile_tip_levels_nap_raises_when_grids_differ(
    mock_multi_cpt_bearing_response: dict,
    mock_multi_cpt_bearing_response_less_pile_tip_levels: dict,
    mock_results_passover: dict,
) -> None:
    """The PileCore adapter fails loudly when per-CPT pile-tip-level grids differ."""
    mcb_full = MultiCPTCompressionBearingResults.from_api_response(
        mock_multi_cpt_bearing_response, mock_results_passover
    )
    mcb_less = MultiCPTCompressionBearingResults.from_api_response(
        mock_multi_cpt_bearing_response_less_pile_tip_levels, mock_results_passover
    )

    # Mix one CPT from each response so the two per-CPT grids differ.
    mcb_full._cpt_results = SingleCPTCompressionBearingResultsContainer(
        {
            "full": mcb_full.cpt_results.results[0],
            "less": mcb_less.cpt_results.results[0],
        }
    )

    with pytest.raises(ValueError, match="same pile-tip-level grid"):
        _ = mcb_full.pile_tip_levels_nap
