from __future__ import annotations

import datetime
from copy import deepcopy
from typing import Dict, List, Literal, Mapping, Sequence, Tuple

from pygef.cpt import CPTData

from pypilecore.input.pile_properties import create_pile_properties_payload
from pypilecore.input.soil_properties import create_soil_properties_payload


def create_multi_cpt_payload(
    pile_tip_levels_nap: Sequence[float],
    cptdata_objects: List[CPTData],
    classify_tables: Dict[str, dict],
    groundwater_level_nap: float,
    pile_type: Literal["concrete", "steel", "micro", "wood"],
    specification: Literal["1", "2", "3", "4", "5", "6", "7"],
    installation: Literal["A", "B", "C", "D", "E", "F", "G"],
    pile_shape: Literal["round", "rect"],
    friction_range_strategy: Literal[
        "manual", "lower_bound", "settlement_driven"
    ] = "lower_bound",
    stiff_construction: bool = False,
    cpts_group: List[str] | None = None,
    ocr: float | None = None,
    fixed_negative_friction_range_nap: Tuple[float, float] | None = None,
    fixed_positive_friction_range_nap: Tuple[float, Literal["ptl"] | float]
    | None = None,
    negative_shaft_friction: float | None = None,
    apply_qc3_reduction: bool | None = None,
    relative_pile_load: float | None = 0.7,
    pile_load_sls: float | None = None,
    soil_load_sls: float = 0.0,
    pile_head_level_nap: float | Literal["surface"] = "surface",
    excavation_depth_nap: float | None = None,
    excavation_param_t: float = 1.0,
    individual_negative_friction_range_nap: Mapping[str, Tuple[float, float]]
    | None = None,
    individual_positive_friction_range_nap: Mapping[
        str, Tuple[float, Literal["ptl"] | float]
    ]
    | None = None,
    individual_ocr: Mapping[str, float] | None = None,
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
    use_almere_rules: bool = False,
    overrule_xi: float | None = None,
    gamma_f_nk: float = 1.0,
    gamma_r_s: float = 1.2,
    gamma_r_b: float = 1.2,
) -> Tuple[dict, Dict[str, dict]]:
    """
    Creates a dictionary with the payload content for the PileCore endpoint
    "/compression/multi-cpt/results"

    This dictionary can be passed directly to `nuclei.client.call_endpoint()`.

    Note
    ----
    The result should be converted to a jsonifyable message before it can be passed to a
    `requests` call directly, for instance with
    `nuclei.client.utils.python_types_to_message()`.

    Parameters
    ----------
    pile_tip_levels_nap:
        Range of values for which the pile resistance is calculated.
    cptdata_objects:
        A list of pygef.CPTData objects
    classify_tables:
        A dictionary, mapping `CPTData.alias` values to dictionary with the resulting response
        of a call to CPTCore `classify/*` information, containing the following keys:

            - geotechnicalSoilName: Sequence[str]
                Geotechnical Soil Name related to the ISO
            - lowerBoundary: Sequence[float]
                Lower boundary of the layer [m]
            - upperBoundary: Sequence[float]
                Upper boundary of the layer [m]
            - color: Sequence[str]
                Hex color code
            - mainComponent: Sequence[Literal["rocks", "gravel", "sand", "silt", "clay", "peat"]]
                Main soil component
            - cohesion: Sequence[float]
                Cohesion of the layer [kPa]
            - gamma_sat: Sequence[float]
                Saturated unit weight [kN/m^3]
            - gamma_unsat: Sequence[float]
                Unsaturated unit weight [kN/m^3]
            - phi: Sequence[float]
                Phi [degrees]
            - undrainedShearStrength: Sequence[float]
                Undrained shear strength [kPa]

    groundwater_level_nap:
        The groundwater level. Unit: [m] w.r.t. NAP.
    pile_type:
        The equaly named entry in the "pile_type_specification" settings.
    friction_range_strategy:
        Sets the method to determine the sleeve friction zones on the pile. The soil
        friction in the positive zone contributes to the bearing capacity, while the
        negative zone adds an extra load on the pile. Accepted values: "manual",
        "lower_bound" (default) or "settlement_driven".
    specification:
        The equaly named entry in the "pile_type_specification" settings.
    installation:
        The equaly named entry in the "pile_type_specification" settings.
    pile_shape:
        The shape of the pile.
    stiff_construction:
        Set to True if it's a stiff costruction. This will have influence on the xi factor
        if you don't overrule it. Default = False.
    cpts_group:
        CPTs that are considered one group. Items must relate to the alias of the CPTData
        objects in `cptdata_objects`.
    ocr:
        The Over-Consolidation-Ratio [-] of the foundation layer.
    fixed_negative_friction_range_nap:
        Optionally sets the fixed depth range between which the negative sleeve friction
        is calculated. If an array of format [top, bottom], the range is set between top
        and bottom where top and bottom are floating values.
        Unit: [m] w.r.t. NAP
    fixed_positive_friction_range_nap:
        Optionally sets the fixed depth range between which the positive sleeve friction
        is calculated. If an array of format (top, bottom), the range is set between top
        and bottom where top and bottom are floating point values. If bottom == "ptl",
        the pile tip level of the calculation is used as value for bottom.
        Unit: [m] w.r.t. NAP
    negative_shaft_friction:
        Sets a fixed value for the negative friction force. If provided, the
        fixed_negative_friction_range_nap parameter will be ignored.
        Unit: [kN]
    apply_qc3_reduction:
        Determines if the reduction on the qc;III trajectory for auger piles should be
        applied conform 7.6.2.3(e) of NEN 9997-1. If omitted (or null: default), the
        value is inferred from the pile type: only True for auger piles (when
        pile_properties.is_auger == True). If a boolean is provided, the qc3 reduction
        is/isn't applied, regardless of the pile type.
    relative_pile_load:
        The fraction of the maximum bearing capacity that is used as pilehead force in
        the settlement calculations. The input value can range between 0.0 and 1.0,
        where 1.0 translates to a pile load of 100% of the maximum bearing capacity.
        When the pile_load_sls parameter is provided, rel_pile_load will be ignored.

        When multiple pile-tip levels are considered, the applied pile load will vary
        with each pile-tip level, depending on the bearing capacity.

        Default = 0.7
    pile_load_sls:
        Force on pile in SLS [kN]. Used to determine settlement of pile w.r.t. soil.
    soil_load_sls:
        Load on soil surface [kPa], used to calculate soil settlement. This is only required
        with the settlement-driven friction-range strategy.
        Default = 0.0
    pile_head_level_nap:
        The level of the pile head. Can be:

            - float;
                This is interpreted as an absolute level in [m w.r.t. NAP];
            - Literal["surface"] (default).
                In this case, the soil_properties.service_level
                property is used.
    excavation_depth_nap:
        Soil excavation depth after the CPT was taken. Unit: [m] w.r.t. NAP.
    excavation_param_t:
        Excavation parameter depending on pile installation method and/or phasing.
            - Use 1.0 (default) for post-excavation installation with vibration (i.e. hammering).
            - Use 0.5 for reduced-vibration installation, or pile installation prior to
              excavation method.

        See for more info NEN 9997-1+C2:2017 7.6.2.3.(10)(k)
    individual_negative_friction_range_nap:
        A dictionary, mapping ``CPTData.alias`` values to fixed negative-friction ranges.
        For a specification of the values, see ``fixed_negative_friction_range_nap``
    individual_positive_friction_range_nap:
        A dictionary, mapping ``CPTData.alias`` values to fixed positive-friction ranges.
        For a specification of the values, see ``fixed_positive_friction_range_nap``
    individual_ocr:
        A dictionary, mapping ``CPTData.alias`` values to Over-Consolidation-Ratio [-]
        values of the foundation layer. This will overrule the general `ocr` setting for
        these specific CPTs only.
    diameter_base:
        Pile base diameter [m].
        Only relevant if ``pile_shape`` = "round".
    diameter_shaft:
        Pile shaft diameter [m].
        Only relevant if ``pile_shape`` = "round".
    width_base_large:
        Largest dimension of the pile base [m].
        Only relevant if ``pile_shape`` = "rect".
    width_base_small:
        Smallest dimension of the pile base [m].
        Only relevant if ``pile_shape`` = "rect".
    width_shaft_large:
        Largest dimension of the pile shaft [m].
        Only relevant if ``pile_shape`` = "rect".
    width_shaft_small:
        Smallest dimension of the pile shaft [m].
        Only relevant if ``pile_shape`` = "rect".
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
    use_almere_rules:
        If set to True the contribution, produced by the positive shaft friction, to the
        total bearing capacity is limited to at most 75% the contribution provided by
        the pile tip. ref: https://www.almere.nl/fileadmin/user_upload/Richtlijnen_Constructie_Gem._Almere_vanaf_01-01-2017_versie_3.0a.pdf
    overrule_xi:
        Set a fixed value for xi in all calculations. Use with caution. This will
        overrule the calculation of xi-values based on the group-size, variation-
        coefficient and construction stiffness.
    gamma_f_nk:
        Safety factor for design-values of the negative sleeve friction force.
        Default = 1.0
    gamma_r_s:
        Safety factor, used to obtain design-values of the pile-tip bearingcapacity.
        Default = 1.2
    gamma_r_b:
        Safety factor, used to obtain design-values of the sleeve bearingcapacity.
        Default = 1.2

    Returns
    -------
    multi_cpt_payload:
        Dictionary with the payload content for the PileCore endpoint
        "/compression/multi-cpt/results"
    results_kwargs:
        Dictionary with keyword arguments for the `pilecore.MultiCPTBearingResults`
        object.

    Raises
    ------
    ValueError:
        - if `pile_shape`=="round" & `diameter_base` is None
        - if `pile_shape`=="rect" & `width_base_large` is None
        - if `pile_shape` not in ["rect", "round"]
    """
    # Input validation
    if excavation_depth_nap is not None and excavation_param_t is None:
        raise ValueError(
            "`excavation_param_t` cannot be None when `excavation_depth_nap` is not None."
        )
    if relative_pile_load is None and pile_load_sls is None:
        raise ValueError(
            "Need at least a value for one of: [`relative_pile_load`, `pile_load_sls`]"
        )

    soil_properties_list, results_kwargs = create_soil_properties_payload(
        cptdata_objects=cptdata_objects,
        classify_tables=classify_tables,
        groundwater_level_nap=groundwater_level_nap,
        friction_range_strategy=friction_range_strategy,
        excavation_depth_nap=excavation_depth_nap,
        master_ocr=ocr,
        individual_negative_friction_range_nap=individual_negative_friction_range_nap,
        individual_positive_friction_range_nap=individual_positive_friction_range_nap,
        individual_ocr=individual_ocr,
    )
    pile_properties = create_pile_properties_payload(
        pile_type=pile_type,
        specification=specification,
        installation=installation,
        pile_shape=pile_shape,
        diameter_base=diameter_base,
        diameter_shaft=diameter_shaft,
        width_base_large=width_base_large,
        width_base_small=width_base_small,
        width_shaft_large=width_shaft_large,
        width_shaft_small=width_shaft_small,
        height_base=height_base,
        settlement_curve=settlement_curve,
        adhesion=adhesion,
        alpha_p=alpha_p,
        alpha_s_clay=alpha_s_clay,
        alpha_s_sand=alpha_s_sand,
        beta_p=beta_p,
        pile_tip_factor_s=pile_tip_factor_s,
        elastic_modulus=elastic_modulus,
        is_auger=is_auger,
        is_low_vibrating=is_low_vibrating,
        negative_fr_delta_factor=negative_fr_delta_factor,
    )
    multi_cpt_payload: dict = dict(
        pile_tip_levels_nap=list(pile_tip_levels_nap),
        list_soil_properties=soil_properties_list,
        pile_properties=pile_properties,
        friction_range_strategy=friction_range_strategy,
        pile_head_level_nap=pile_head_level_nap,
        stiff_construction=stiff_construction,
        rel_pile_load=relative_pile_load,
        soil_load=soil_load_sls,
        excavation_param_t=excavation_param_t,
        use_almere_rules=use_almere_rules,
        gamma_f_nk=gamma_f_nk,
        gamma_r_b=gamma_r_b,
        gamma_r_s=gamma_r_s,
    )

    # Add optional properties
    if excavation_depth_nap is not None:
        multi_cpt_payload["excavation_depth_nap"] = excavation_depth_nap
    if pile_load_sls is not None:
        multi_cpt_payload["pile_load"] = pile_load_sls
    if apply_qc3_reduction is not None:
        multi_cpt_payload["apply_qc3_reduction"] = apply_qc3_reduction
    if negative_shaft_friction is not None:
        multi_cpt_payload["f_nk"] = negative_shaft_friction
    if fixed_negative_friction_range_nap is not None:
        multi_cpt_payload[
            "fixed_negative_friction_range_nap"
        ] = fixed_negative_friction_range_nap
    if fixed_positive_friction_range_nap is not None:
        multi_cpt_payload[
            "fixed_positive_friction_range_nap"
        ] = fixed_positive_friction_range_nap
    if overrule_xi is not None:
        multi_cpt_payload["overrule_xi"] = overrule_xi
    if cpts_group is not None:
        multi_cpt_payload["cpts_group"] = cpts_group

    return multi_cpt_payload, results_kwargs


def create_multi_cpt_report_payload(
    multi_cpt_payload: dict,
    project_name: str,
    project_id: str,
    author: str,
    date: str | None = None,
    group_results_content: bool = True,
    individual_cpt_results_content: bool = True,
    result_summary_content: bool = True,
) -> dict:
    """
    Creates a dictionary with the payload content for the PileCore endpoint
    "/compression/multi-cpt/report"

    This dictionary can be passed directly to `nuclei.client.call_endpoint()`. Note that
    it should be converted to a jsonifyable message before it can be passed to a
    `requests` call directly, for instance with
    `nuclei.client.utils.python_types_to_message()`.

    Parameters
    ----------
    multi_cpt_payload:
        Index 0 of the resulting tuple of a call to `create_multi_cpt_payload()`
    project_name:
        The name of the project.
    project_id:
        The identifier (code) of the project.
    author:
        The author of the report.
    date:
        The date of the report. If None, the current date will be used.
    group_results_content:
        Whether or not to add the group-results section to the report. Default = True
    individual_cpt_results_content:
        Whether or not to add the individual-cpt-results section to the report.
        Default = True
    result_summary_content:
        Whether or not to add the result-summary section to the report. Default = True

    Returns
    -------
    report_payload:
        Dictionary with the payload content for the PileCore endpoint
        "/compression/multi-cpt/report"
    """
    report_payload = deepcopy(multi_cpt_payload)
    report_payload.update(
        dict(
            content=dict(
                group_results=group_results_content,
                individual_cpt_results=individual_cpt_results_content,
                result_summary=result_summary_content,
            ),
            general=dict(
                author=author,
                project_id=project_id,
                project_name=project_name,
                date=date
                if date is None
                else datetime.date.today().strftime("%d-%m-%y"),
            ),
        )
    )
    return report_payload
