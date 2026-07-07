import numpy as np
import pytest
from nuclei.client.utils import serialize_jsonifyable_object
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from requests import Request

from pypilecore.input import create_grouper_payload_from_bearing_results
from pypilecore.results import (
    CustomBearingResults,
    CustomCptBearingResult,
    GrouperBearingResultsLike,
)
from pypilecore.results.soil_properties import SoilProperties


@pytest.fixture()
def headers() -> dict:
    return {"Content-Type": "application/json"}


def _record(test_id: str, x: float, y: float, **overrides) -> CustomCptBearingResult:
    data = dict(
        test_id=test_id,
        x=x,
        y=y,
        pile_tip_level_nap=[-10.0, -11.0, -12.0],
        R_b_cal=[100.0, 110.0, 120.0],
        R_s_cal=[50.0, 55.0, 60.0],
        F_nk_d=[10.0, 10.0, 10.0],
        R_c_d_net=[120.0, 130.0, 140.0],
    )
    data.update(overrides)
    return CustomCptBearingResult(**data)


@pytest.fixture()
def custom_bearing_results() -> CustomBearingResults:
    return CustomBearingResults(
        [_record("CPT-1", 0.0, 0.0), _record("CPT-2", 5.0, 5.0)]
    )


def test_custom_bearing_results_satisfies_protocol(
    custom_bearing_results: CustomBearingResults,
) -> None:
    assert isinstance(custom_bearing_results, GrouperBearingResultsLike)
    assert custom_bearing_results.cpt_names == ["CPT-1", "CPT-2"]
    assert custom_bearing_results.pile_tip_levels_nap == [-10.0, -11.0, -12.0]


def test_custom_bearing_results_payload_validates_against_openapi(
    custom_bearing_results: CustomBearingResults,
    pc_openapi,
    headers: dict,
) -> None:
    payload = create_grouper_payload_from_bearing_results(custom_bearing_results)

    request = Request(
        method="POST",
        headers=headers,
        url="http://grouper/group-cpts",
        json=serialize_jsonifyable_object(payload),
    )
    pc_openapi.request_validator.validate(RequestsOpenAPIRequest(request))


def test_base_max_bearing_results_builds_coordinate_only_baseline(
    custom_bearing_results: CustomBearingResults,
) -> None:
    base = custom_bearing_results.base_max_bearing_results()

    assert set(base.test_ids) == {"CPT-1", "CPT-2"}

    result = base["CPT-1"]
    # pile_head_level_nap is dropped from the custom API -> None on the baseline.
    assert result.pile_head_level_nap is None
    # origin is a per-PTL Sequence[str].
    assert list(result.table.origin) == ["CPT:CPT-1", "CPT:CPT-1", "CPT:CPT-1"]
    # No soil trace supplied -> synthesized coordinate-only SoilProperties.
    assert result.soil_properties.cpt_table is None
    assert result.soil_properties.layer_table is None
    assert result.soil_properties.test_id == "CPT-1"
    assert result.soil_properties.x == 0.0
    assert result.soil_properties.y == 0.0
    np.testing.assert_array_equal(
        result.table.R_c_d_net, np.array([120.0, 130.0, 140.0])
    )


def test_dict_like_access(custom_bearing_results: CustomBearingResults) -> None:
    assert custom_bearing_results["CPT-1"].test_id == "CPT-1"
    assert set(custom_bearing_results.results_dict.keys()) == {"CPT-1", "CPT-2"}
    assert len(custom_bearing_results.results) == 2
    with pytest.raises(ValueError):
        _ = custom_bearing_results["does-not-exist"]


def test_rejects_nan() -> None:
    with pytest.raises(ValueError, match="NaN"):
        _record("CPT-1", 0.0, 0.0, R_b_cal=[np.nan, 110.0, 120.0])


def test_rejects_mismatched_array_lengths() -> None:
    with pytest.raises(ValueError, match="same length"):
        _record("CPT-1", 0.0, 0.0, R_s_cal=[50.0, 55.0])


def test_rejects_missing_coordinates() -> None:
    with pytest.raises(ValueError, match="x and a y"):
        _record("CPT-1", None, 0.0)


def test_rejects_soil_properties_disagreement() -> None:
    mismatched = SoilProperties(test_id="OTHER", x=0.0, y=0.0)
    with pytest.raises(ValueError, match="does not match"):
        _record("CPT-1", 0.0, 0.0, soil_properties=mismatched)


def test_accepts_matching_soil_properties() -> None:
    matching = SoilProperties(test_id="CPT-1", x=0.0, y=0.0)
    record = _record("CPT-1", 0.0, 0.0, soil_properties=matching)
    assert record.soil_properties is matching


def test_rejects_duplicate_test_ids() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        CustomBearingResults([_record("CPT-1", 0.0, 0.0), _record("CPT-1", 5.0, 5.0)])


def test_rejects_differing_pile_tip_level_grids() -> None:
    with pytest.raises(ValueError, match="same pile-tip-level grid"):
        CustomBearingResults(
            [
                _record("CPT-1", 0.0, 0.0),
                _record(
                    "CPT-2", 5.0, 5.0, pile_tip_level_nap=[-10.0, -11.0, -99.0]
                ),
            ]
        )
