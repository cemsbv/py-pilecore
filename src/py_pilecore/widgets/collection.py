from .aggregate.pile import get_pile_tip_range
from .components import (
    adhesion,
    alpha_p,
    alpha_s_clay_check,
    alpha_s_clay_numeric,
    alpha_s_sand,
    diameter,
    diameter_cone,
    groundwater_level_from_cpt,
    groundwater_level_numeric,
    groundwater_level_reference,
    pile_head_dropdown,
    pile_head_level_numeric,
    pile_shape,
    pile_specification,
    pile_specification_dict,
    settlement_curve,
    smooth_pile,
    width_large,
    width_small,
)


def get_calculation_parameters_kwargs() -> dict:
    if groundwater_level_from_cpt.value == "Try to":
        use_cpt_groundwater_level = True
    elif groundwater_level_from_cpt.value == "Never":
        use_cpt_groundwater_level = False
    else:
        raise ValueError()

    if groundwater_level_reference.value == "surface level":
        groundwater_level_wrt_surface = True
    elif groundwater_level_reference.value == "NAP":
        groundwater_level_wrt_surface = False
    else:
        raise ValueError()

    return dict(
        use_cpt_groundwater_level=use_cpt_groundwater_level,
        groundwater_level_wrt_surface=groundwater_level_wrt_surface,
        groundwater_level_numeric=groundwater_level_numeric.value,
    )


def get_pile_properties_kwargs() -> dict:
    if pile_specification.value in pile_specification_dict:
        pile_type = pile_specification_dict[pile_specification.value]["pile_type"]
        specification = pile_specification_dict[pile_specification.value][
            "specification"
        ]
        installation = pile_specification_dict[pile_specification.value]["installation"]
    else:
        pile_type = "concrete"
        specification = "1"
        installation = "A"

    pile_head_level_nap = (
        "surface"
        if pile_head_dropdown.value == "surface"
        else pile_head_level_numeric.value
    )

    adhesion_value = adhesion.value if smooth_pile.value is True else None

    alpha_s_clay_value = (
        alpha_s_clay_numeric.value if alpha_s_clay_check.value == "Constant" else None
    )

    if pile_shape.value == "Rectangluar":
        pile_shape_kwargs = dict(
            pile_shape="rect",
            width_base_large=width_large.value,
            width_base_small=width_small.value,
            height_base=None,
            width_shaft_large=None,
            width_shaft_small=None,
            diameter_base=None,
            diameter_shaft=None,
        )
    elif pile_shape.value == "Round":
        pile_shape_kwargs = dict(
            pile_shape="round",
            diameter_base=diameter.value,
            diameter_shaft=None,
            height_base=None,
            width_base_large=None,
            width_base_small=None,
            width_shaft_large=None,
            width_shaft_small=None,
        )
    elif pile_shape.value == "Round with cone tip":
        pile_shape_kwargs = dict(
            pile_shape="round",
            diameter_base=diameter_cone.value,
            diameter_shaft=diameter.value,
            height_base=0.0,
            width_base_large=None,
            width_base_small=None,
            width_shaft_large=None,
            width_shaft_small=None,
        )

    return dict(
        pile_type=pile_type,
        specification=specification,
        installation=installation,
        pile_tip_levels_nap=get_pile_tip_range(),
        pile_head_level_nap=pile_head_level_nap,
        adhesion=adhesion_value,
        alpha_p=alpha_p.value,
        settlement_curve=int(settlement_curve.value),
        alpha_s_clay=alpha_s_clay_value,
        alpha_s_sand=alpha_s_sand.value,
        **pile_shape_kwargs,
    )


def get_multi_cpt_result_kwargs() -> dict:
    kwargs = {}
    kwargs.update(get_pile_properties_kwargs())
    kwargs.update(get_calculation_parameters_kwargs())
    return kwargs
