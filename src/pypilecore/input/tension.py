from __future__ import annotations

import datetime
from copy import deepcopy
from typing import Any, Dict, List, Literal, Mapping, Sequence, Tuple

from pygef.cpt import CPTData

from pypilecore.common.piles import PileGridProperties, PileProperties
from pypilecore.input.soil_properties import create_soil_properties_payload


def create_multi_cpt_payload(
    pile_tip_levels_nap: Sequence[float],
    cptdata_objects: List[CPTData],
    classify_tables: Dict[str, dict],
    groundwater_level_nap: float,
    pile: PileProperties,
    pile_grid: PileGridProperties | None,
    stiff_construction: bool = False,
    ocr: float | None = None,
    soil_load_sls: float = 0.0,
    pile_head_level_nap: float | Literal["surface"] = "surface",
    excavation_depth_nap: float | None = None,
    top_of_tension_zone_nap: float | None = None,
    individual_top_of_tension_zone_nap: Mapping[Any, float] | None = None,
    excavation_param_t: float = 1.0,
    individual_ocr: Mapping[str, float] | None = None,
    overrule_xi: float | None = None,
    gamma_f_nk: float = 1.0,
    gamma_r_s: float = 1.2,
    gamma_r_b: float = 1.2,
    void_ratio_max: float = 0.8,
    void_ratio_min: float = 0.4,
    pile_load_sls_max: float = 1,
    pile_load_sls_min: float = 0,
    gamma_s_t: float = 1.35,
    gamma_gamma: float = 1.1,
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
    stiff_construction:
        Set to True if it's a stiff costruction. This will have influence on the xi factor
        if you don't overrule it. Default = False.
    ocr:
        The Over-Consolidation-Ratio [-] of the foundation layer.
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
    void_ratio_max:
        Maximum void ratio of the soil (the loosest packing). The influence of this
        parameter is limited and therefore it is typically sufficient to provide a
        global estimation. For normally consolidated sands in The Netherlands, an
        emax = 0.80 can be used in most cases.
        Default = 0.8
    void_ratio_min:
        Minimum void ratio of the soil (the densest packing). The influence of this parameter
        is limited and therefore it is typically sufficient to provide a global estimation.
        For normally consolidated sands in The Netherlands, an emin = 0.40 can be used in most cases.
        Default = 0.4
    pile_load_sls_max:
        Maximum tension force on pile Ft;max;k. Note that only positive values (tension force)
        are accepted. unit: kN
        Default = 1
    pile_load_sls_min:
        Minimum tension force (or maximum compression force) on pile -Ft;min;k (tension > 0). Positive
        values (tension force), negative values (compression force) and 0.0 are accepted. Note that
        the positive must be <= pile_load_sls_max. unit: kN
        Default = 0
    gamma_s_t:
        Pile resistance factor gamma_s;t used to compute the design cone resistance values
        qc;z;d as prescribed in NEN 9997-1+C2_2017 7.6.3.3(d).
        Default = 1.35
    gamma_gamma:
        Partial factor for volumetric weight NEN 9997-1+C2:2017 A.3.2
        Default = 1.1
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
        - If both `relative_pile_load` and `pile_load_sls` are None.
    """
    # Input validation
    if excavation_depth_nap is not None and excavation_param_t is None:
        raise ValueError(
            "`excavation_param_t` cannot be None when `excavation_depth_nap` is not None."
        )

    soil_properties_list, results_kwargs = create_soil_properties_payload(
        cptdata_objects=cptdata_objects,
        classify_tables=classify_tables,
        groundwater_level_nap=groundwater_level_nap,
        friction_range_strategy="manual",
        excavation_depth_nap=excavation_depth_nap,
        master_ocr=ocr,
        individual_negative_friction_range_nap=None,
        individual_positive_friction_range_nap=None,
        individual_ocr=individual_ocr,
        master_top_of_tension_zone_nap=top_of_tension_zone_nap,
        individual_top_of_tension_zone_nap=individual_top_of_tension_zone_nap,
    )
    multi_cpt_payload: dict = dict(
        pile_tip_levels_nap=list(pile_tip_levels_nap),
        list_soil_properties=soil_properties_list,
        pile_properties=pile.serialize_payload(),
        pile_head_level_nap=pile_head_level_nap,
        stiff_construction=stiff_construction,
        soil_load=soil_load_sls if soil_load_sls is not None else 0.0,
        excavation_param_t=excavation_param_t,
        gamma_f_nk=gamma_f_nk,
        gamma_r_b=gamma_r_b,
        gamma_r_s=gamma_r_s,
        void_ratio_max=void_ratio_max,
        void_ratio_min=void_ratio_min,
        pile_load_sls_max=pile_load_sls_max,
        pile_load_sls_min=pile_load_sls_min,
        gamma_s_t=gamma_s_t,
        gamma_gamma=gamma_gamma,
    )

    # Add optional properties
    if excavation_depth_nap is not None:
        multi_cpt_payload["excavation_depth_nap"] = excavation_depth_nap
    if overrule_xi is not None:
        multi_cpt_payload["overrule_xi"] = overrule_xi
    if pile_grid is not None:
        multi_cpt_payload["pile_grid"] = pile_grid.serialize_payload()

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
                date=(
                    date if date is None else datetime.date.today().strftime("%d-%m-%y")
                ),
            ),
        )
    )
    return report_payload
