import numpy as np
import pygef
import pytest
from nuclei.client.utils import serialize_jsonifyable_object
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from requests import Request

from pypilecore.common.friction import FrictionSettings
from pypilecore.common.norms import CUR236_version, NEN99971_version, Norms
from pypilecore.common.piles import PileProperties
from pypilecore.common.piles.geometry import PileGeometry
from pypilecore.common.piles.geometry.components import (
    RectPileGeometryComponent,
    RoundPileGeometryComponent,
)
from pypilecore.common.piles.geometry.components.common import (
    PrimaryPileComponentDimension,
)
from pypilecore.common.piles.type import PileType
from pypilecore.input.multi_cpt import create_multi_cpt_payload
from pypilecore.input.soil_properties import get_cpt_depth


@pytest.fixture()
def headers() -> dict:
    return {
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
            reference="B1",
        ),
    )


@pytest.fixture
def rectangle_pile() -> PileProperties:
    return PileProperties(
        geometry=PileGeometry(
            components=[
                RectPileGeometryComponent(
                    secondary_dimension=0.5,
                    primary_dimension=PrimaryPileComponentDimension(length=0.5),
                )
            ]
        ),
        pile_type=PileType(reference="B1"),
    )


@pytest.fixture
def rectangle_pile_custom() -> PileProperties:
    return PileProperties(
        geometry=PileGeometry(
            components=[
                RectPileGeometryComponent(
                    secondary_dimension=0.6,
                    primary_dimension=PrimaryPileComponentDimension(length=0.4),
                    material="concrete",
                )
            ]
        ),
        pile_type=PileType(
            alpha_s_sand=0.009,
            alpha_s_clay={"use_constant_value": False},
            alpha_p=0.30,
            alpha_t_sand=0.0090,
            alpha_t_clay={"use_constant_value": False},
            negative_fr_delta_factor=1.0,
            is_auger=False,
            installation_method="screwed",
            is_prefab=False,
            is_open_ended=False,
            settlement_curve=1,
            is_low_vibrating=True,
        ),
    )


@pytest.fixture
def default_norm() -> Norms:
    return Norms()


@pytest.fixture
def custom_norm() -> Norms:
    return Norms(nen_9997_1=NEN99971_version.V2017, cur_236=CUR236_version.V2023)

@pytest.fixture
def lower_bound_friction() -> FrictionSettings:
    return FrictionSettings(
        friction_range_strategy="lower_bound"
    )

@pytest.fixture
def manual_friction() -> FrictionSettings:
    return FrictionSettings(
        friction_range_strategy="manual",
        negative_friction_range_nap=(0, -5.0),
        positive_friction_range_nap=(-5.0, "ptl")
    )

@pytest.fixture
def manual_friction_only_positive() -> FrictionSettings:
    return FrictionSettings(
        friction_range_strategy="manual",
        positive_friction_range_nap=(-5.0, "ptl"),
        negative_friction=20.0
    )

@pytest.mark.parametrize(
    "pile_name", ["round_pile", "rectangle_pile", "rectangle_pile_custom"]
)
@pytest.mark.parametrize("norms_name", ["default_norm", "custom_norm"])
@pytest.mark.parametrize("cpt_name", ["cpt", "cpt_no_coords"])
@pytest.mark.parametrize("friction_settings_name", ["lower_bound_friction", "manual_friction", "manual_friction_only_positive"])
def test_create_multi_cpt_payload(
    pc_openapi, cpt_name, pile_name, norms_name, friction_settings_name, request, headers
):
    # resolve fixture by name so we can parametrize over fixture names
    pile = request.getfixturevalue(pile_name)
    norms = request.getfixturevalue(norms_name)
    cpt = request.getfixturevalue(cpt_name)
    friction_settings = request.getfixturevalue(friction_settings_name)

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
        pile=pile,
        norms=norms,
        friction_range_strategy=friction_settings.friction_range_strategy,
        fixed_positive_friction_range_nap=friction_settings.positive_friction_range_nap,
        fixed_negative_friction_range_nap=friction_settings.negative_friction_range_nap,
        negative_shaft_friction=friction_settings.negative_friction
    )

    request = Request(
        method="POST",
        headers=headers,
        url="http://bearing/multiple-cpts/results",
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
        url="http://bearing/multiple-cpts/results",
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


def test_get_cpt_depth(cpt: pygef.cpt.CPTData):
    depth = np.array(cpt.data["depth"])
    penetration_length = np.array(cpt.data["penetrationLength"])

    assert np.array_equal(get_cpt_depth(cpt), depth)

    cpt.data.drop_in_place("depth")
    assert np.array_equal(get_cpt_depth(cpt), penetration_length)
