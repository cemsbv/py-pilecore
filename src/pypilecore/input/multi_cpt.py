from __future__ import annotations

import datetime
from copy import deepcopy
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import pandas as pd
from pygef.cpt import CPTData

from .pile_properties import create_pile_properties_payload
from .soil_properties import create_soil_properties_payload


def create_multi_cpt_payload(
    pile_tip_levels_nap: Sequence[float],
    cptdata_objects: List[CPTData],
    layer_tables: Dict[str, pd.DataFrame],
    groundwater_level: float,
    friction_range_strategy: str,
    pile_type: str,
    specification: str,
    installation: str,
    pile_shape: str,
    stiff_construction: bool | None = None,
    cpts_group: bool | None = None,
    use_almere_rules: bool | None = None,
    soil_load_sls: float | None = None,
    overrule_xi: float | None = None,
    gamma_f_nk: float | None = None,
    gamma_r_s: float | None = None,
    gamma_r_b: float | None = None,
    fixed_negative_friction_range_nap: Tuple[float, float] | None = None,
    fixed_positive_friction_range_nap: Tuple[float, str | float] | None = None,
    negative_shaft_friction: float | None = None,
    apply_qc3_reduction: bool | None = None,
    relative_pile_load: float | None = None,
    pile_load_sls: float | None = None,
    pile_head_level_nap: float | str | None = None,
    excavation_depth_nap: float | None = None,
    excavation_param_t: float | None = None,
    set_negative_friction_range_nap: Mapping[Any, Tuple[float, str]] | None = None,
    set_positive_friction_range_nap: Mapping[Any, Tuple[float, str]] | None = None,
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
) -> Tuple[dict, Dict[str, dict]]:
    soil_properties_list, results_passover = create_soil_properties_payload(
        cptdata_objects=cptdata_objects,
        layer_tables=layer_tables,
        groundwater_level=groundwater_level,
        friction_range_strategy=friction_range_strategy,
        excavation_depth_nap=excavation_depth_nap,
        set_negative_friction_range_nap=set_negative_friction_range_nap,
        set_positive_friction_range_nap=set_positive_friction_range_nap,
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
    )

    # Add optional properties
    if excavation_depth_nap is not None:
        multi_cpt_payload["excavation_depth_nap"] = excavation_depth_nap
    if excavation_param_t is not None:
        multi_cpt_payload["excavation_param_t"] = excavation_param_t
    if pile_head_level_nap is not None:
        multi_cpt_payload["pile_head_level_nap"] = pile_head_level_nap
    if pile_load_sls is not None:
        multi_cpt_payload["pile_load"] = pile_load_sls
    if relative_pile_load is not None:
        multi_cpt_payload["rel_pile_load"] = relative_pile_load
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
    if gamma_f_nk is not None:
        multi_cpt_payload["gamma_f_nk"] = gamma_f_nk
    if gamma_r_s is not None:
        multi_cpt_payload["gamma_r_s"] = gamma_r_s
    if gamma_r_b is not None:
        multi_cpt_payload["gamma_r_b"] = gamma_r_b
    if overrule_xi is not None:
        multi_cpt_payload["overrule_xi"] = overrule_xi
    if soil_load_sls is not None:
        multi_cpt_payload["soil_load"] = soil_load_sls
    if use_almere_rules is not None:
        multi_cpt_payload["use_almere_rules"] = use_almere_rules
    if cpts_group is not None:
        multi_cpt_payload["cpts_group"] = cpts_group
    if friction_range_strategy is not None:
        multi_cpt_payload["friction_range_strategy"] = friction_range_strategy
    if stiff_construction is not None:
        multi_cpt_payload["stiff_construction"] = stiff_construction

    return multi_cpt_payload, results_passover


def create_multi_cpt_report_payload(
    multi_cpt_payload: dict,
    project_name: str,
    project_id: str,
    author: str,
    date: str | None = None,
    group_results_content: bool | None = None,
    individual_cpt_results_content: bool | None = None,
    result_summary_content: bool | None = None,
) -> dict:
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
