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
    """
    Creates a dictionary with the `pile_properties` payload content for the PileCore
    endpoints.

    Note that
    the dictionary should be converted to a jsonifyable message before it can be passed
    to a `requests` call directly, for instance with
    `nuclei.client.utils.python_types_to_message()`.

    Parameters
    ----------
    pile_type:
        The equaly named entry in the "pile_type_specification" settings.
        Accepted values are: ["A","B","C""D","E","F","G"]
    specification:
        The equaly named entry in the "pile_type_specification" settings.
        Accepted values are: ["concrete","steel","micro","wood"]
    installation:
        The equaly named entry in the "pile_type_specification" settings.
        Accepted values are: ["1","2","3","4","5","6","7"]
    pile_shape:
        The shape of the pile.
        Accepted values are: ["round", "rect"]
    diameter_base:
        Pile base diameter [m].
        Only relevant if `shape`="round".
    diameter_shaft:
        Pile shaft diameter [m].
        Only relevant if `shape`="round".
    width_base_large:
        Largest dimension of the pile base [m].
        Only relevant if `shape`="rect".
    width_base_small:
        Smallest dimension of the pile base [m].
        Only relevant if `shape`="rect".
    width_shaft_large:
        Largest dimension of the pile shaft [m].
        Only relevant if `shape`="rect".
    width_shaft_small:
        Smallest dimension of the pile shaft [m].
        Only relevant if `shape`="rect".
    height_base:
        Height of pile base [m]. If None, a pile with constant dimension is inferred.
        Cannot be None if diameter_base and diameter_shaft are unequal.
    settlement_curve:
        Settlement lines for figures 7.n and 7.o of NEN-9997-1 As defined in table 7.c
        of NEN-9997-1. The value is inferred from the pile_type_specifications, but can
        be overwritten.
    adhesion:
        Optional adhesion value [kPa], use it if the pile shaft has undergone a special
        treatment. Examples: - adhesion = 50 kN/m2 for synthetic coating - adhesion = 20
        kN/m2 for bentonite - adhesion = 10 kN/m2 for bitumen coating See 7.3.2.2(d) of
        NEN 9997-1 for examples.
    alpha_p:
        Alpha p factor used in pile tip resistance calculation. The value is inferred
        from the pile_type_specifications, but can be overwritten.
    alpha_s_clay:
        Alpha s factor for soft layers used in the positive friction calculation. If
        None the factor is determined as specified in table 7.d of NEN 9997-1.
    alpha_s_sand:
        Alpha s factor for coarse layers used in the positive friction calculation. The
        value is inferred from the pile_type_specifications, but can be overwritten.
    beta_p:
        Factor s used in pile tip resistance calculation as per NEN 9997-1 7.6.2.3 (h).
        The value is inferred from the pile dimension properties, but can be overwritten.
    pile_tip_factor_s:
        Factor s used in pile tip resistance calculation as per NEN 9997-1 7.6.2.3 (h).
        The value is inferred from the pile dimension properties, but can be overwritten.
    elastic_modulus:
        Modulus of elasticity of the pile [Mpa]. The value is inferred from the
        pile_type_specifications, but can be overwritten.
    is_auger:
        Determines weather the pile the pile is an auger pile or not. The value is
        inferred from the pile_type_specifications, but can be overwritten.
    is_low_vibrating:
        Determines weather the pile has an installation type with low vibration. The
        value is inferred from the pile_type_specifications, but can be overwritten.
    negative_fr_delta_factor:
        factor * φ = δ. This parameter will be multiplied with phi to get the delta
        parameter used in negative friction calculation according to NEN-9997-1 7.3.2.2
        (e). Typically values are 1.0 for piles cast in place, and 0.75 for other pile
        types. The value is inferred from the pile_type_specifications, but can be
        overwritten.

    Returns
    -------
    pile_properties:
        The `pile_properties` payload content of the PileCore-API endpoints.

    Raises
    ------
    ValueError:
        - if `pile_shape`=="round" & `diameter_base` is None
        - if `pile_shape`=="rect" & `width_base_large` is None
        - if `pile_shape` not in ["rect", "round"]
    """
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
                'A value for `diameter_base` is required for `pile_shape`=="round"'
            )

        pile_properties["props"]["diameter_base"] = diameter_base

        if diameter_shaft is not None:
            if height_base is None:
                raise ValueError(
                    "A value for `height_base` is required when the base and shaft dimensions are unequal"
                )

            pile_properties["props"]["diameter_shaft"] = diameter_shaft

    elif pile_shape == "rect":
        if width_base_large is None:
            raise ValueError(
                'A value for `width_base_large` is required for `pile_shape`=="rect"'
            )
        pile_properties["props"]["width_base_large"] = width_base_large

        if width_base_small is not None:
            pile_properties["props"]["width_base_small"] = width_base_small

        if (
            width_shaft_large is not None or width_shaft_small is not None
        ) and height_base is None:
            raise ValueError(
                "A value for `height_base` is required when the base and shaft dimensions are unequal"
            )
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
