from __future__ import annotations


def create_pile_properties_payload(
    pile_type: str,
    specification: str,
    installation: str,
    pile_shape: str,
    diameter_base: float | None = None,
    diameter_shaft: float | None = None,
    width_base_large: float | None = None,
    width_base_small: float | None = None,
    width_shaft_large: float | None = None,
    width_shaft_small: float | None = None,
    height_base: float | None = None,
    settlement_curve: float | None = None,
    adhesion: float | None = None,
    alpha_p: float | None = None,
    alpha_s_clay: float | None = None,
    alpha_s_sand: float | None = None,
    beta_p: float | None = None,
    pile_tip_factor_s: float | None = None,
    elastic_modulus: float | None = None,
    is_auger: float | None = None,
    is_low_vibrating: float | None = None,
    negative_fr_delta_factor: float | None = None,
) -> dict:
    pile_properties: dict = dict(
        props=dict(
            pile_type_specification=dict(
                pile_type=pile_type,
                specification=specification,
                installation=installation,
            )
        ),
        type=pile_shape,
    )

    if pile_shape == "round":
        if diameter_base is None:
            raise ValueError(
                'A value for `diameter_base` is required for pile_shape=="round"'
            )

        pile_properties["props"]["diameter_base"] = diameter_base

        if diameter_shaft is None:
            pile_properties["props"]["diameter_shaft"] = diameter_shaft

    elif pile_shape == "rect":
        if width_base_large is None:
            raise ValueError(
                'A value for `width_base_large` is required for pile_shape=="rect"'
            )
        pile_properties["props"]["width_base_large"] = width_base_large

        if width_base_small is not None:
            pile_properties["props"]["width_base_small"] = width_base_small

        if width_shaft_large is not None:
            pile_properties["props"]["width_shaft_large"] = width_shaft_large

        if width_shaft_small is not None:
            pile_properties["props"]["width_shaft_small"] = width_shaft_small

    else:
        raise ValueError('pile_shape should be one of ["round", "rect"]')

    if height_base is not None:
        pile_properties["props"]["height_base"] = height_base

    if settlement_curve is not None:
        pile_properties["props"]["settlement_curve"] = settlement_curve

    if adhesion is not None:
        pile_properties["props"]["adhesion"] = adhesion

    if alpha_p is not None:
        pile_properties["props"]["alpha_p"] = alpha_p

    if alpha_s_clay is not None:
        pile_properties["props"]["alpha_s_clay"] = alpha_s_clay

    if alpha_s_sand is not None:
        pile_properties["props"]["alpha_s_sand"] = alpha_s_sand

    if beta_p is not None:
        pile_properties["props"]["beta_p"] = beta_p

    if pile_tip_factor_s is not None:
        pile_properties["props"]["pile_tip_factor_s"] = pile_tip_factor_s

    if elastic_modulus is not None:
        pile_properties["props"]["elastic_modulus"] = elastic_modulus

    if is_auger is not None:
        pile_properties["props"]["is_auger"] = is_auger

    if is_low_vibrating is not None:
        pile_properties["props"]["is_low_vibrating"] = is_low_vibrating

    if negative_fr_delta_factor is not None:
        pile_properties["props"]["negative_fr_delta_factor"] = negative_fr_delta_factor

    return pile_properties
