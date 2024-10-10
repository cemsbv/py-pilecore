import pytest
from nuclei.client.utils import serialize_jsonifyable_object
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from requests import Request

from pypilecore.common.piles import PileProperties
from pypilecore.common.piles.geometry import PileGeometry
from pypilecore.common.piles.geometry.components import RoundPileGeometryComponent
from pypilecore.common.piles.geometry.components.common import (
    PrimaryPileComponentDimension,
)
from pypilecore.common.piles.type import PileType
from pypilecore.input.multi_cpt import create_multi_cpt_payload


@pytest.fixture()
def headers() -> dict:
    # admin@cemsbv.io
    # Allowed pilecore+report & pilecore+calculate
    nuclei_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiUGlsZUNvcmUgVGVzdCIsImV4cGlyZXMiOjE5NTU5MTk2MDAsInVuaXF1ZV9rZXkiOiJlOTNiZDBjNC0yYmZhLTQ5MGUtYjI0Yy03OGMwOThkOWYyOWYiLCJ1c2VyX2lkIjoiYXV0aDB8NjU0YzlmNjk4YjA4Yzc3ZTQ4NjA3OGFjIiwicGVybWlzc2lvbnMiOlsicmVhZDpwaWxlY29yZStjYWxjdWxhdGUiLCJyZWFkOnBpbGVjb3JlK3JlcG9ydCJdfQ.KpVmh4rbzCFIO-9fJrsz8pXbs2ITxGHuv5_WQNJGPJg"

    return {
        # "Authorization": "Bearer {}".format(nuclei_token),
        "Content-Type": "application/json",
    }


@pytest.fixture
def round_pile() -> PileProperties:
    return PileProperties(
        geometry=PileGeometry(
            components=[
                RoundPileGeometryComponent(
                    diameter=0.5,
                    primary_dimension=PrimaryPileComponentDimension(length=None),
                )
            ]
        ),
        pile_type=PileType(
            standard_pile={
                "main_type": "concrete",
                "specification": "1",
            },
        ),
    )


def test_create_multi_cpt_payload(pc_openapi, cpt, round_pile, headers):
    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[-10.0, -20.0],
        cptdata_objects=[cpt],
        classify_tables={
            cpt.alias: {
                "geotechnicalSoilName": ["Sand"],
                "lowerBoundary": [1.0],
                "upperBoundary": [0.0],
                "color": ["#000000"],
                "mainComponent": ["sand"],
                "cohesion": [0.0],
                "gamma_sat": [20],
                "gamma_unsat": [18],
                "phi": [30],
                "undrainedShearStrength": [0.0],
            }
        },
        groundwater_level_nap=-10.0,
        pile=round_pile,
    )

    request = Request(
        method="POST",
        headers=headers,
        url="http://compression/multiple-cpts/results",
        json=serialize_jsonifyable_object(payload),
    )

    openapi_request = RequestsOpenAPIRequest(request)

    pc_openapi.request_validator.validate(openapi_request)


def test_create_multi_cpt_payload_no_coords(
    pc_openapi, cpt_no_coords, round_pile, headers
):
    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[-10.0, -20.0],
        cptdata_objects=[cpt_no_coords],
        classify_tables={
            cpt_no_coords.alias: {
                "geotechnicalSoilName": ["Sand"],
                "lowerBoundary": [1.0],
                "upperBoundary": [0.0],
                "color": ["#000000"],
                "mainComponent": ["sand"],
                "cohesion": [0.0],
                "gamma_sat": [20],
                "gamma_unsat": [18],
                "phi": [30],
                "undrainedShearStrength": [0.0],
            }
        },
        groundwater_level_nap=-10.0,
        pile=round_pile,
    )

    request = Request(
        method="POST",
        headers=headers,
        url="http://compression/multiple-cpts/results",
        json=serialize_jsonifyable_object(payload),
    )

    openapi_request = RequestsOpenAPIRequest(request)

    pc_openapi.request_validator.validate(openapi_request)


@pytest.mark.parametrize(
    ("stress_reduction_method", "excavation_width", "excavation_edge_distance"),
    [
        ("constant", None, None),
        ("begemann", 10.0, 0.0),
        ("begemann", 10.0, 5.0),
    ],
)
def test_create_multi_cpt_payload_excavation_settings_valid(
    pc_openapi,
    cpt,
    round_pile,
    headers,
    stress_reduction_method,
    excavation_width,
    excavation_edge_distance,
):
    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[-10.0, -20.0],
        cptdata_objects=[cpt],
        classify_tables={
            cpt.alias: {
                "geotechnicalSoilName": ["Sand"],
                "lowerBoundary": [1.0],
                "upperBoundary": [0.0],
                "color": ["#000000"],
                "mainComponent": ["sand"],
                "cohesion": [0.0],
                "gamma_sat": [20],
                "gamma_unsat": [18],
                "phi": [30],
                "undrainedShearStrength": [0.0],
            }
        },
        excavation_stress_reduction_method=stress_reduction_method,
        excavation_width=excavation_width,
        excavation_edge_distance=excavation_edge_distance,
        groundwater_level_nap=-10.0,
        pile=round_pile,
    )

    request = Request(
        method="POST",
        headers=headers,
        url="http://compression/multiple-cpts/results",
        json=serialize_jsonifyable_object(payload),
    )

    openapi_request = RequestsOpenAPIRequest(request)

    pc_openapi.request_validator.validate(openapi_request)


@pytest.mark.parametrize(
    (
        "stress_reduction_method",
        "excavation_width",
        "excavation_edge_distance",
        "expected_error",
        "message_matching",
    ),
    [
        (None, None, None, ValueError, "excavation_stress_reduction_method"),
        ("begemann", None, 0.0, ValueError, "excavation_width"),
        ("begemann", 10.0, None, ValueError, "excavation_edge_distance"),
    ],
)
def test_create_multi_cpt_payload_excavation_settings_invalid(
    cpt,
    round_pile,
    stress_reduction_method,
    excavation_width,
    excavation_edge_distance,
    expected_error,
    message_matching,
):
    with pytest.raises(expected_error, match=message_matching):
        create_multi_cpt_payload(
            pile_tip_levels_nap=[-10.0, -20.0],
            cptdata_objects=[cpt],
            classify_tables={
                cpt.alias: {
                    "geotechnicalSoilName": ["Sand"],
                    "lowerBoundary": [1.0],
                    "upperBoundary": [0.0],
                    "color": ["#000000"],
                    "mainComponent": ["sand"],
                    "cohesion": [0.0],
                    "gamma_sat": [20],
                    "gamma_unsat": [18],
                    "phi": [30],
                    "undrainedShearStrength": [0.0],
                }
            },
            excavation_stress_reduction_method=stress_reduction_method,
            excavation_width=excavation_width,
            excavation_edge_distance=excavation_edge_distance,
            groundwater_level_nap=-10.0,
            pile=round_pile,
        )
