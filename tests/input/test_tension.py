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
from pypilecore.input.tension import create_multi_cpt_payload

SAFETY_FACTOR_DEFAULTS = {
    "gamma_s_t": 1.35,
}

# Properties that the uplift request schema does not document. They are never sent,
# and their (deprecated) arguments are accepted but ignored. Maps the argument name to
# a sample value and the payload key it used to produce.
DEPRECATED_ARGUMENTS = {
    "gamma_f_nk": (1.0, "gamma_f_nk"),
    "gamma_r_b": (1.2, "gamma_r_b"),
    "gamma_r_s": (1.2, "gamma_r_s"),
    "gamma_gamma": (1.1, "gamma_gamma"),
    "stiff_construction": (True, "stiff_construction"),
    "soil_load_sls": (5.0, "soil_load"),
}

DEPRECATED_PAYLOAD_KEYS = {key for _, key in DEPRECATED_ARGUMENTS.values()}


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
        pile_type=PileType(reference="B1"),
    )


@pytest.fixture
def classify_table() -> dict:
    return {
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


@pytest.mark.parametrize("safety_factor", list(SAFETY_FACTOR_DEFAULTS))
def test_create_multi_cpt_payload_safety_factor_none_is_omitted(
    pc_openapi,
    cpt,
    round_pile,
    classify_table,
    headers,
    safety_factor,
):
    """
    A safety factor of None is omitted from the payload, so that the API applies its own
    default. Passing null would be rejected by the API.
    """
    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[-10.0, -20.0],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: classify_table},
        groundwater_level_nap=-10.0,
        pile=round_pile,
        pile_grid=None,
        **{safety_factor: None},
    )

    assert safety_factor not in payload

    request = Request(
        method="POST",
        headers=headers,
        url="http://uplift/nen/multiple-cpts/results",
        json=serialize_jsonifyable_object(payload),
    )
    pc_openapi.request_validator.validate(RequestsOpenAPIRequest(request))


def test_create_multi_cpt_payload_safety_factor_defaults(
    cpt,
    round_pile,
    classify_table,
):
    """The safety factors are sent with their documented defaults when not overruled."""
    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[-10.0, -20.0],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: classify_table},
        groundwater_level_nap=-10.0,
        pile=round_pile,
        pile_grid=None,
    )

    for name, default in SAFETY_FACTOR_DEFAULTS.items():
        assert payload[name] == default


@pytest.mark.parametrize(
    "argument, value",
    [
        (argument, value)
        for argument, (value, _) in sorted(DEPRECATED_ARGUMENTS.items())
    ],
)
def test_create_multi_cpt_payload_deprecated_arguments_warn(
    cpt,
    round_pile,
    classify_table,
    argument,
    value,
):
    """The uplift endpoints do not accept these properties; passing them is deprecated."""
    with pytest.warns(DeprecationWarning, match=argument):
        payload, _ = create_multi_cpt_payload(
            pile_tip_levels_nap=[-10.0, -20.0],
            cptdata_objects=[cpt],
            classify_tables={cpt.alias: classify_table},
            groundwater_level_nap=-10.0,
            pile=round_pile,
            pile_grid=None,
            **{argument: value},
        )

    assert not DEPRECATED_PAYLOAD_KEYS.intersection(payload)


def test_create_multi_cpt_payload_omits_undocumented_properties(
    cpt,
    round_pile,
    classify_table,
):
    """Properties absent from the uplift request schema are never sent."""
    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[-10.0, -20.0],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: classify_table},
        groundwater_level_nap=-10.0,
        pile=round_pile,
        pile_grid=None,
    )

    assert not DEPRECATED_PAYLOAD_KEYS.intersection(payload)
