from __future__ import annotations

import datetime
from copy import deepcopy
from typing import Dict, List, Literal, Mapping, Sequence, Tuple

from pygef.cpt import CPTData

from pypilecore.common.piles import PileProperties
from pypilecore.input.soil_properties import create_soil_properties_payload


def create_multi_cpt_payload(
    pile_tip_levels_nap: Sequence[float],
    cptdata_objects: List[CPTData],
    classify_tables: Dict[str, dict],
    groundwater_level_nap: float,
    pile: PileProperties,
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
    excavation_stress_reduction_method: Literal["constant", "begemann"] = "constant",
    excavation_width: float | None = None,
    excavation_edge_distance: float | None = None,
    individual_negative_friction_range_nap: Mapping[str, Tuple[float, float]]
    | None = None,
    individual_positive_friction_range_nap: Mapping[
        str, Tuple[float, Literal["ptl"] | float]
    ]
    | None = None,
    individual_ocr: Mapping[str, float] | None = None,
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
    pile:
        A PileProperties object.
    friction_range_strategy:
        Sets the method to determine the sleeve friction zones on the pile. The soil
        friction in the positive zone contributes to the bearing capacity, while the
        negative zone adds an extra load on the pile. Accepted values: "manual",
        "lower_bound" (default) or "settlement_driven".
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
    excavation_stress_reduction_method:
        Method used to calculate the stress reduction due to the excavation applied to the effective and total stresses.
        Only used when `excavation_depth_nap` is different than `None`. It can be:
            - "constant" (default): The stress reduction below the excavation is constant with depth. The stress reduction
            is equal to the original effective stress (i.e. before the excavation) at the excavation depth.
            - "begemann": The stress reduction below the excavation decreases with depth according to the Begemann method.
            This method uses the elastic solution of a strip load acting on a semi-infinite homogeneous soil mass.
            The load has a width equal to the excavation width and a magnitude equal to the original effective stress at
            the excavation depth.
        Regardless the method, the stress reduction applied above the excavation is equal to the original effective stress
        at each corresponding depth.
    excavation_width:
        Width of the excavation [m]. Used to calculate the stress reduction due to the excavation if the Begemann method is selected.
        In this case, it must be provided and it must be > 0.
    excavation_edge_distance:
        Distance from the pile centerline to the excavation edge [m]. Used to calculate the stress reduction due to the excavation if
        the Begemann method is selected. In this case, it must be provided and it must be between 0.0 and 0.5 * excavation_width.

        Note that:
            - 0.0 means that the pile is located at the edge of the excavation.
            - 0.5 * excavation_width means that the pile is at the center of the excavation.
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
        - If `excavation_depth_nap` is not None and `excavation_param_t` is None.
        - If `excavation_stress_reduction_method` is not either 'constant' or 'begemann'.
        - If `excavation_stress_reduction_method` is 'begemann' and `excavation_width` is None.
        - If `excavation_stress_reduction_method` is 'begemann' and `excavation_edge_distance` is None.
        - If both `relative_pile_load` and `pile_load_sls` are None.
    """
    # Input validation
    if excavation_depth_nap is not None and excavation_param_t is None:
        raise ValueError(
            "`excavation_param_t` cannot be None when `excavation_depth_nap` is not None."
        )
    if excavation_stress_reduction_method not in ["constant", "begemann"]:
        raise ValueError(
            "`excavation_stress_reduction_method` must be either 'constant' or 'begemann'."
        )
    if excavation_stress_reduction_method == "begemann" and excavation_width is None:
        raise ValueError(
            "`excavation_width` must be provided when `excavation_stress_reduction_method` is 'begemann'."
        )
    if (
        excavation_stress_reduction_method == "begemann"
        and excavation_edge_distance is None
    ):
        raise ValueError(
            "`excavation_edge_distance` must be provided when `excavation_stress_reduction_method` is 'begemann'"
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
    multi_cpt_payload: dict = dict(
        pile_tip_levels_nap=list(pile_tip_levels_nap),
        list_soil_properties=soil_properties_list,
        pile_properties=pile.serialize_payload(),
        friction_range_strategy=friction_range_strategy,
        pile_head_level_nap=pile_head_level_nap,
        stiff_construction=stiff_construction,
        rel_pile_load=relative_pile_load,
        soil_load=soil_load_sls if soil_load_sls is not None else 0.0,
        excavation_param_t=excavation_param_t,
        use_almere_rules=use_almere_rules,
        gamma_f_nk=gamma_f_nk,
        gamma_r_b=gamma_r_b,
        gamma_r_s=gamma_r_s,
    )

    # Add optional properties
    if excavation_depth_nap is not None:
        multi_cpt_payload["excavation_depth_nap"] = excavation_depth_nap

    if excavation_stress_reduction_method == "constant":
        multi_cpt_payload["excavation_settings"] = dict(
            stress_reduction_method="constant"
        )
    else:
        multi_cpt_payload["excavation_settings"] = dict(
            stress_reductin_method="begemann",
            excavation_width=excavation_width,
            excavation_edge_distance=excavation_edge_distance,
        )

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
