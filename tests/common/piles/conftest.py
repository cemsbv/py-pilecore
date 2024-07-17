import pytest

from pypilecore.common.piles.geometry.components import (
    PrimaryPileComponentDimension,
    RectPileGeometryComponent,
    RoundPileGeometryComponent,
)
from pypilecore.common.piles.geometry.main import PileGeometry


@pytest.fixture
def rect_pile_component_core():
    return RectPileGeometryComponent.from_api_response(
        dict(
            secondary_dimension=0.35,
            primary_dimension=dict(length=None),
            tertiary_dimension=0.30,
            material="concrete",
        ),
        inner_component=None,
    )


@pytest.fixture
def rect_pile_component_shell(rect_pile_component_core):
    return RectPileGeometryComponent.from_api_response(
        dict(
            secondary_dimension=0.45,
            primary_dimension=dict(length=1.0),
            tertiary_dimension=0.4,
            material="concrete",
        ),
        inner_component=rect_pile_component_core,
    )


@pytest.fixture
def round_pile_component_core():
    return RoundPileGeometryComponent.from_api_response(
        dict(
            diameter=0.35,
            primary_dimension=dict(length=None),
            material="concrete",
        ),
        inner_component=None,
    )


@pytest.fixture
def round_pile_component_shell(round_pile_component_core):
    return RoundPileGeometryComponent.from_api_response(
        dict(
            diameter=0.45,
            primary_dimension=dict(length=1.0),
            material="concrete",
        ),
        inner_component=round_pile_component_core,
    )


@pytest.fixture
def rect_widened_base_geometry():
    return PileGeometry.from_api_response(
        dict(
            components=[
                dict(
                    outer_shape="rectangle",
                    primary_dimension=dict(length=None),
                    secondary_dimension=0.35,
                    tertiary_dimension=0.30,
                    material="concrete",
                ),
                dict(
                    outer_shape="rectangle",
                    primary_dimension=dict(length=1.0),
                    secondary_dimension=0.45,
                    tertiary_dimension=0.40,
                    material="concrete",
                ),
            ],
            properties=dict(beta_p=0.8),
        )
    )


@pytest.fixture
def round_widened_base_geometry():
    return PileGeometry.from_api_response(
        dict(
            components=[
                dict(
                    outer_shape="round",
                    diameter=0.35,
                    primary_dimension=dict(length=None),
                    material="concrete",
                ),
                dict(
                    outer_shape="round",
                    diameter=0.45,
                    primary_dimension=dict(length=1.0),
                    material="concrete",
                ),
            ],
            properties=dict(beta_p=0.9),
        )
    )
