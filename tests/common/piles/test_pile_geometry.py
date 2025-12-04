import math

import numpy as np
from matplotlib.axes import Axes

from pypilecore.common.piles.geometry.components.common import (
    PrimaryPileComponentDimension,
)
from pypilecore.common.piles.geometry.components.rectangle import (
    RectPileGeometryComponent,
    calculate_equiv_tip_diameter,
)
from pypilecore.common.piles.geometry.components.round import RoundPileGeometryComponent


def test_calculate_equiv_tip_diameter():
    # Test case where b_max is greater than 1.5 times a_min
    a_min = 2.0
    b_max = 4.0
    expected_result = 2.0
    assert math.isclose(
        calculate_equiv_tip_diameter(a_min, b_max), expected_result, rel_tol=1e-3
    )

    # Test case where b_max is less than 1.5 times a_min
    a_min = 2.0
    b_max = 3.0
    expected_result = 2.768
    assert math.isclose(
        calculate_equiv_tip_diameter(a_min, b_max), expected_result, rel_tol=1e-3
    )

    # Test case where b_max is equal to 1.5 times a_min
    a_min = 2.0
    b_max = 3.0
    expected_result = 2.768
    assert math.isclose(
        calculate_equiv_tip_diameter(a_min, b_max), expected_result, rel_tol=1e-3
    )

    # Test case where a_min is zero
    a_min = 0.0
    b_max = 4.0
    expected_result = 0.0
    assert math.isclose(
        calculate_equiv_tip_diameter(a_min, b_max), expected_result, rel_tol=1e-6
    )

    # Test case where a_min and b_max are zero
    a_min = 0.0
    b_max = 0.0
    expected_result = 0.0
    assert math.isclose(
        calculate_equiv_tip_diameter(a_min, b_max), expected_result, rel_tol=1e-6
    )


def test_rect_pile_component_core(rect_pile_component_core):
    component = rect_pile_component_core

    assert isinstance(component.primary_dimension, PrimaryPileComponentDimension)
    assert component.primary_dimension.length is None
    assert component.secondary_dimension == 0.35
    assert component.tertiary_dimension == 0.30
    assert component.inner_component is None
    assert component.material == "concrete"
    assert component.outer_shape == "rectangle"

    assert np.allclose(component.cross_section_bounds, (-0.175, 0.175, -0.15, 0.15))
    assert np.isclose(component.circumference, 1.3)
    assert np.isclose(component.equiv_tip_diameter, 0.366, rtol=1e-3)
    assert np.isclose(component.area_full, 0.105)

    payload = component.serialize_payload()
    assert payload == dict(
           outer_shape="rectangle",
           secondary_dimension=0.35,
           tertiary_dimension=0.30,
           material="concrete",
    )

    assert np.allclose(component.get_component_bounds_nap(-10, 0), (0, -10))


def test_rect_pile_component_shell(rect_pile_component_shell):
    component = rect_pile_component_shell

    assert isinstance(component.primary_dimension, PrimaryPileComponentDimension)
    assert component.primary_dimension.length == 1.0
    assert component.secondary_dimension == 0.45
    assert component.tertiary_dimension == 0.40
    assert isinstance(component.inner_component, RectPileGeometryComponent)
    assert component.material == "concrete"
    assert component.outer_shape == "rectangle"

    assert np.allclose(component.cross_section_bounds, (-0.225, 0.225, -0.2, 0.2))
    assert np.isclose(component.circumference, 1.7)
    assert np.isclose(component.equiv_tip_diameter, 0.479, rtol=1e-3)
    assert np.isclose(component.area_full, 0.18)

    payload = component.serialize_payload()
    assert payload == dict(
        outer_shape="rectangle",
        primary_dimension=dict(length=1),
        secondary_dimension=0.45,
        tertiary_dimension=0.40,
        material="concrete",
    )

    assert np.allclose(component.get_component_bounds_nap(-10, 0), (-9, -10))


def test_round_pile_component_core(round_pile_component_core):
    component = round_pile_component_core

    assert isinstance(component.primary_dimension, PrimaryPileComponentDimension)
    assert component.primary_dimension.length is None
    assert component.diameter == 0.35
    assert component.inner_component is None
    assert component.material == "concrete"
    assert component.outer_shape == "round"

    assert np.allclose(component.cross_section_bounds, (-0.175, 0.175, -0.175, 0.175))
    assert np.isclose(component.circumference, math.pi * 0.35)
    assert np.isclose(component.equiv_tip_diameter, 0.35, rtol=1e-3)
    assert np.isclose(component.area_full, math.pi * (0.35 / 2) ** 2)

    payload = component.serialize_payload()
    assert payload == dict(
           outer_shape="round",
           diameter=0.35,
           material="concrete",
    )

    assert np.allclose(component.get_component_bounds_nap(-10, 0), (0, -10))


def test_round_pile_component_shell(round_pile_component_shell):
    component = round_pile_component_shell

    assert isinstance(component.primary_dimension, PrimaryPileComponentDimension)
    assert component.primary_dimension.length == 1.0
    assert component.diameter == 0.45
    assert isinstance(component.inner_component, RoundPileGeometryComponent)
    assert component.material == "concrete"
    assert component.outer_shape == "round"

    assert np.allclose(component.cross_section_bounds, (-0.225, 0.225, -0.225, 0.225))
    assert np.isclose(component.circumference, math.pi * 0.45)
    assert np.isclose(component.equiv_tip_diameter, 0.45, rtol=1e-3)
    assert np.isclose(component.area_full, math.pi * (0.45 / 2) ** 2)

    payload = component.serialize_payload()
    assert payload == dict(
        outer_shape="round",
        primary_dimension=dict(length=1),
        diameter=0.45,
        material="concrete",
    )

    assert np.allclose(component.get_component_bounds_nap(-10, 0), (-9, -10))


def test_rect_widened_base_geometry(rect_widened_base_geometry):
    geometry = rect_widened_base_geometry

    assert isinstance(geometry.components, list)
    for component in geometry.components:
        assert isinstance(component, RectPileGeometryComponent)

    assert geometry.materials == []
    assert geometry.materials_dict == {}
    assert geometry.pile_tip_factor_s is None
    assert np.isclose(geometry.beta_p, 0.8)
    assert geometry.equiv_diameter_pile_tip == geometry.components[1].equiv_tip_diameter
    assert geometry.circumference_pile_tip == geometry.components[1].circumference
    assert geometry.area_pile_tip == geometry.components[1].area_full

    assert geometry.serialize_payload() == dict(
        components=[
            dict(
                   outer_shape="rectangle",
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
        custom_properties=dict(beta_p=0.8),
    )

    assert np.allclose(
        geometry.get_circum_vs_depth(
            pile_tip_level_nap=-5,
            pile_head_level_nap=-1,
            depth_nap=np.arange(-0.5, -6.5, -1.0),
        ),
        np.array([0, 1.3, 1.3, 1.3, 1.7, 0]),
    )

    assert np.allclose(
        geometry.get_area_vs_depth(
            pile_tip_level_nap=-5,
            pile_head_level_nap=-1,
            depth_nap=np.arange(-0.5, -6.5, -1.0),
        ),
        np.array(
            [
                0,
                0.35 * 0.3,
                0.35 * 0.3,
                0.35 * 0.3,
                0.45 * 0.4,
                0,
            ]
        ),
    )

    axes = geometry.plot(pile_tip_level_nap=-5, pile_head_level_nap=-1, show=False)
    assert isinstance(axes, np.ndarray)
    for ax in axes:
        assert isinstance(ax, Axes)


def test_round_widened_base_geometry(round_widened_base_geometry):
    geometry = round_widened_base_geometry

    assert isinstance(geometry.components, list)
    for component in geometry.components:
        assert isinstance(component, RoundPileGeometryComponent)

    assert geometry.materials == []
    assert geometry.materials_dict == {}
    assert geometry.pile_tip_factor_s is None
    assert np.isclose(geometry.beta_p, 0.9)
    assert geometry.equiv_diameter_pile_tip == geometry.components[1].equiv_tip_diameter
    assert geometry.circumference_pile_tip == geometry.components[1].circumference
    assert geometry.area_pile_tip == geometry.components[1].area_full

    assert geometry.serialize_payload() == dict(
        components=[
            dict(
                   outer_shape="round",
                   diameter=0.35,
                   material="concrete",
            ),
            dict(
                outer_shape="round",
                diameter=0.45,
                primary_dimension=dict(length=1.0),
                material="concrete",
            ),
        ],
        custom_properties=dict(beta_p=0.9),
    )

    assert np.allclose(
        geometry.get_circum_vs_depth(
            pile_tip_level_nap=-5,
            pile_head_level_nap=-1,
            depth_nap=np.arange(-0.5, -6.5, -1.0),
        ),
        np.array(
            [0, math.pi * 0.35, math.pi * 0.35, math.pi * 0.35, math.pi * 0.45, 0]
        ),
    )

    assert np.allclose(
        geometry.get_area_vs_depth(
            pile_tip_level_nap=-5,
            pile_head_level_nap=-1,
            depth_nap=np.arange(-0.5, -6.5, -1.0),
        ),
        np.array(
            [
                0,
                math.pi * (0.35 / 2) ** 2,
                math.pi * (0.35 / 2) ** 2,
                math.pi * (0.35 / 2) ** 2,
                math.pi * (0.45 / 2) ** 2,
                0,
            ]
        ),
    )

    axes = geometry.plot(pile_tip_level_nap=-5, pile_head_level_nap=-1, show=False)
    assert isinstance(axes, np.ndarray)
    for ax in axes:
        assert isinstance(ax, Axes)
