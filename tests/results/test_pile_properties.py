from typing import Sequence

import numpy as np
import pytest
from numpy.typing import NDArray

from pypilecore.results.pile_properties import RectPileProperties, RoundPileProperties, create_pile_properties_from_api_response


def test_round_pile_properties():
    pile = RoundPileProperties(
        pile_type_specification=dict(
            pile_type="concrete", specification="1", installation="A"
        ),
        diameter_base=0.5,
        diameter_shaft=0.4,
        height_base=1,
        alpha_s_sand=0.01,
        alpha_s_clay=0.01,
        alpha_p=0.01,
        beta_p=1,
        pile_tip_factor_s=1,
        settlement_curve=1,
        elastic_modulus=1e3,
        negative_fr_delta_factor=1.0,
        adhesion=0,
        is_low_vibrating=False,
        is_auger=False,
        name="round_pile",
    )

    # Check properties
    assert isinstance(pile.name, str)
    assert isinstance(pile.alpha_s_clay, float)
    assert isinstance(pile.alpha_s_sand, float)
    assert isinstance(pile.alpha_p, float)
    assert isinstance(pile.elastic_modulus, float)
    assert isinstance(pile.negative_fr_delta_factor, float)
    assert isinstance(pile.is_low_vibrating, bool)
    assert isinstance(pile.is_auger, bool)
    assert isinstance(pile.adhesion, float)
    assert isinstance(pile.shape, str)
    assert isinstance(pile.pile_type, str)
    assert isinstance(pile.installation, str)
    assert isinstance(pile.specification, str)
    assert isinstance(pile.height_base, float)
    assert isinstance(pile.settlement_curve, int)
    assert isinstance(pile.pile_tip_factor_s, float)
    assert isinstance(pile.pile_type_specification, dict)
    assert isinstance(pile.circumference_pile_shaft, float)
    assert isinstance(pile.circumference_pile_base, float)
    assert isinstance(pile.area_pile_tip, float)
    assert isinstance(pile.equiv_base_diameter, float)
    assert isinstance(pile.equiv_shaft_diameter, float)
    assert isinstance(pile.beta_p, float)

    assert isinstance(pile.diameter_base, float)
    assert isinstance(pile.diameter_shaft, float)

    # Check methods
    diameters = pile.get_diameter_vs_depth(
        pile_tip_level=-5, pile_head_level=0, depth=np.array([0, 1, 2, 3, 4])
    )
    assert isinstance(diameters, np.ndarray)

    circums = pile.get_circum_vs_depth(
        pile_tip_level=-5, pile_head_level=0, depth=np.array([0, 1, 2, 3, 4])
    )
    assert isinstance(circums, np.ndarray)

    areas = pile.get_area_vs_depth(
        pile_tip_level=-5, pile_head_level=0, depth=np.array([0, 1, 2, 3, 4])
    )
    assert isinstance(areas, np.ndarray)


def test_rect_pile_properties():
    pile = RectPileProperties(
        pile_type_specification=dict(
            pile_type="concrete", specification="1", installation="A"
        ),
        width_base_large=0.5,
        width_base_small=0.5,
        width_shaft_large=0.4,
        width_shaft_small=0.4,
        height_base=1,
        alpha_s_sand=0.01,
        alpha_s_clay=0.01,
        alpha_p=0.01,
        beta_p=1,
        pile_tip_factor_s=1,
        settlement_curve=1,
        elastic_modulus=1e3,
        negative_fr_delta_factor=1.0,
        adhesion=50,
        is_low_vibrating=True,
        is_auger=True,
    )

    # Check properties
    assert pile.name is None
    assert isinstance(pile.alpha_s_clay, float)
    assert isinstance(pile.alpha_s_sand, float)
    assert isinstance(pile.alpha_p, float)
    assert isinstance(pile.elastic_modulus, float)
    assert isinstance(pile.negative_fr_delta_factor, float)
    assert isinstance(pile.is_low_vibrating, bool)
    assert isinstance(pile.is_auger, bool)
    assert isinstance(pile.adhesion, float)
    assert isinstance(pile.shape, str)
    assert isinstance(pile.pile_type, str)
    assert isinstance(pile.installation, str)
    assert isinstance(pile.specification, str)
    assert isinstance(pile.height_base, float)
    assert isinstance(pile.settlement_curve, int)
    assert isinstance(pile.pile_tip_factor_s, float)
    assert isinstance(pile.pile_type_specification, dict)
    assert isinstance(pile.circumference_pile_shaft, float)
    assert isinstance(pile.circumference_pile_base, float)
    assert isinstance(pile.area_pile_tip, float)
    assert isinstance(pile.equiv_base_diameter, float)
    assert isinstance(pile.equiv_shaft_diameter, float)
    assert isinstance(pile.beta_p, float)

    assert isinstance(pile.width_base_large, float)
    assert isinstance(pile.width_base_small, float)
    assert isinstance(pile.width_shaft_large, float)
    assert isinstance(pile.width_shaft_small, float)

    # Check methods
    with pytest.raises((NotImplementedError, AttributeError)):
        pile.get_diameter_vs_depth(
            pile_tip_level=-5, pile_head_level=0, depth=np.array([0, 1, 2, 3, 4])
        )

    circums = pile.get_circum_vs_depth(
        pile_tip_level=-5, pile_head_level=0, depth=np.array([0, 1, 2, 3, 4])
    )
    assert isinstance(circums, np.ndarray)

    areas = pile.get_area_vs_depth(
        pile_tip_level=-5, pile_head_level=0, depth=np.array([0, 1, 2, 3, 4])
    )
    assert isinstance(areas, np.ndarray)


def test_create_round_pile_properties_from_api_response():
    response = dict(
        type="round",
        props=dict(
            diameter_base=0.5,
            diameter_shaft=0.5,
            height_base=1.0,
            adhesion=0.0,
            alpha_p=0.1,
            alpha_s_clay="from soil-type",
            alpha_s_sand=0.01,
            beta_p=0.9,
            elastic_modulus=1e5,
            is_auger=False,
            is_low_vibrating=True,
            name="round_pile",
            negative_fr_delta_factor=1.0,
            pile_tip_factor_s=1.0,
            pile_type_specification=dict(
                pile_type="concrete", specification="1", installation="A"
            ),
            settlement_curve=3,
        ),
    )

    pile = create_pile_properties_from_api_response(response)
    assert isinstance(pile, RoundPileProperties)

def test_create_rect_pile_properties_from_api_response():
    response = dict(
        type="rect",
        props=dict(
            width_base_large=0.5,
            width_base_small=0.5,
            width_shaft_large=0.5,
            width_shaft_small=0.5,
            height_base=1.0,
            adhesion=0.0,
            alpha_p=0.1,
            alpha_s_clay="from soil-type",
            alpha_s_sand=0.01,
            beta_p=0.9,
            elastic_modulus=1e5,
            is_auger=False,
            is_low_vibrating=True,
            negative_fr_delta_factor=1.0,
            pile_tip_factor_s=1.0,
            pile_type_specification=dict(
                pile_type="concrete", specification="1", installation="A"
            ),
            settlement_curve=3,
        ),
    )

    pile = create_pile_properties_from_api_response(response)
    assert isinstance(pile, RectPileProperties)
