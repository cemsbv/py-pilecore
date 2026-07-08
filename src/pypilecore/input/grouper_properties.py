from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any, Dict, List

import numpy as np
from shapely.geometry import Polygon, mapping

from pypilecore.results import SingleCPTCompressionBearingResults
from pypilecore.results.typing import GrouperBearingResultsLike, GrouperCptInput


def create_grouper_payload(
    cpt_results_dict: Dict[str, SingleCPTCompressionBearingResults],
    building_polygon: Polygon | None = None,
    cpt_grid_rotation: float = 0.0,
    gamma_bottom: float = 1.2,
    gamma_shaft: float = 1.2,
    include_centre_to_centre_check: bool = False,
    stiff_construction: bool = False,
    resolution: float = 0.5,
    overrule_nan: float = 0.0,
    skip_nan: bool = False,
) -> dict:
    """
    Creates a dictionary with the payload content for the PileCore endpoint
    "/grouper/group_cpts"


    Note
    ------
    The grouper uses pile bearing capacity results calculated by PileCore or other software to
    form  subgroups of the total group of CPT’s belonging to this project.
    Valid subgroups have the characteristics:

        - a maximum variation coefficient of 12% at one or more pile-tip levels. (Variation check
          NEN9997-1 A.3.3.3)
        - is spatially coherent, which means there are no other CPTs in between the members
          of the subgroup. (Spatial check)

    Additionally, centre to centre validation (include_centre_to_centre_check; NEN9997-1 3.2.3) can be
    added to the cluster method. This check adds restrictions to the maximum allowable R;c;cal outliers
    and makes sure that the suitable data density requirements for the subgroup are met, by checking the
    centre-to-centre (CTC) distance of the cpts in a regular square grid:

        - A maximum CTC distance of 25 m, if no R;c;cal outliers greater than 30% off the average;
        - A maximum CTC distance of 20 m, if no R;c;cal outliers greater than 40% off the average;
        - A maximum CTC distance of 15 m, if no R;c;cal outliers greater than 50% off the average;
        - All subgroups with R;c;cal outliers greater than 50% of the average are considered invalid.

    The CTC check is performed by drawing a square around each CPT with the CTC dimensions according to the
    outlier criterion and verifying that there is no empty space between squares. The rotation of the squares
    can be provided with the `cpt_grid_rotation` argument. Note that this rotation is assigned to all CPT's and
    therefore should represent the main orientation of the building.

    Parameters
    ----------
    cpt_results_dict:
        Dictionary with key as CPT name and value a SingleCPTBearingResults class.
        Should contain at least 2 entries.
    stiff_construction
        Default is False
        Attribute use to get the xi3 and xi4 value. True if it is a stiff construction
    gamma_shaft
        Default is 1.2
        Safety factor shaft design bearing capacity
    gamma_bottom
        Default is 1.2
        Safety factor bottom design bearing capacity
    include_centre_to_centre_check:
        Default is False
        Flag that indicates if the cluster algorithm performs a centre to centre validation of the CPT’s of the
        generated subgroups or not according to NEN9997-1 3.2.3. If the group doesn’t comply to the check, the
        result of the group is deleted from the result.
    building_polygon:
        Default is None
        Polygon of the contour of the building. If None the building Polygon in generated based on the
        convex_hull of the CPT points.
    cpt_grid_rotation:
        Default is 0.0.
        Rotation of the squares used in the centre to centre validation [degrees]
    resolution:
        Default is 0.5
        The resolution of clusters algorithm. If resolution is 1 the cluster boundary conditions can be met
        (number clusters is number CPTs). Depending on the number of CPTs this can take some time.
    overrule_nan:
        Default is 0.0
        The default behavior is to replace NaN with zero, for one of the following
        attributes ["R_b_cal", "F_nk_d", "R_s_cal"].
    skip_nan:
        Default is False
        If True the CPTs are skipped that have NaN values in one of the following
        attributes ["R_b_cal", "F_nk_d", "R_s_cal"], this means that they are not used in the grouper method.

    Raises
    ------
    ValueError:
        - if NaN values are present in negative friction, bottom or shaft bearing_capacity

        - if x or y coordinate is None

        - if pile tip levels don't macht for all SingleCPTBearingResults

        - if less than 2 valid CPTs are provided


    Returns
    -------
    payload:
        Dictionary with the payload content for the PileCore endpoint
        "/grouper/group_cpts"
    """
    # Adapt the PileCore-shaped dict onto the source-agnostic payload seam and build the
    # payload through the shared core. Kept for backwards compatibility; prefer
    # `create_grouper_payload_from_bearing_results`.
    cpt_inputs = [
        GrouperCptInput(
            name=name,
            x=cpt_result.soil_properties.x,
            y=cpt_result.soil_properties.y,
            pile_tip_level_nap=cpt_result.table.pile_tip_level_nap,
            R_b_cal=cpt_result.table.R_b_cal,
            R_s_cal=cpt_result.table.R_s_cal,
            F_nk_d=cpt_result.table.F_nk_d,
        )
        for name, cpt_result in cpt_results_dict.items()
    ]
    return _build_grouper_payload(
        cpt_inputs,
        building_polygon=building_polygon,
        cpt_grid_rotation=cpt_grid_rotation,
        gamma_bottom=gamma_bottom,
        gamma_shaft=gamma_shaft,
        include_centre_to_centre_check=include_centre_to_centre_check,
        stiff_construction=stiff_construction,
        resolution=resolution,
        overrule_nan=overrule_nan,
        skip_nan=skip_nan,
    )


def create_grouper_payload_from_bearing_results(
    bearing: GrouperBearingResultsLike,
    building_polygon: Polygon | None = None,
    cpt_grid_rotation: float = 0.0,
    gamma_bottom: float = 1.2,
    gamma_shaft: float = 1.2,
    include_centre_to_centre_check: bool = False,
    stiff_construction: bool = False,
    resolution: float = 0.5,
    overrule_nan: float = 0.0,
    skip_nan: bool = False,
) -> dict:
    """
    Creates a dictionary with the payload content for the PileCore endpoint
    "/grouper/group_cpts" from any object that satisfies `GrouperBearingResultsLike`.

    This is the source-agnostic sibling of `create_grouper_payload`: it serves both a
    PileCore `MultiCPTCompressionBearingResults` and a user-built `CustomBearingResults`,
    because both satisfy the `GrouperBearingResultsLike` protocol.

    See `create_grouper_payload` for the meaning of the grouper settings and the
    validation rules.

    Parameters
    ----------
    bearing:
        Any object satisfying `GrouperBearingResultsLike` (e.g. a PileCore
        `MultiCPTCompressionBearingResults` or a `CustomBearingResults`). Should contain
        at least 2 CPTs with valid bearing capacity.
    overrule_nan:
        Default is 0.0.
        The default behavior is to replace NaN with zero, for one of the following
        attributes ["R_b_cal", "F_nk_d", "R_s_cal"].

        Note: inert for a `CustomBearingResults` source, which is NaN-free by construction.
    skip_nan:
        Default is False.
        If True the CPTs are skipped that have NaN values in one of the following
        attributes ["R_b_cal", "F_nk_d", "R_s_cal"].

        Note: inert for a `CustomBearingResults` source, which is NaN-free by construction.

    Returns
    -------
    payload:
        Dictionary with the payload content for the PileCore endpoint
        "/grouper/group_cpts"
    """
    return _build_grouper_payload(
        bearing.grouper_cpt_inputs(),
        building_polygon=building_polygon,
        cpt_grid_rotation=cpt_grid_rotation,
        gamma_bottom=gamma_bottom,
        gamma_shaft=gamma_shaft,
        include_centre_to_centre_check=include_centre_to_centre_check,
        stiff_construction=stiff_construction,
        resolution=resolution,
        overrule_nan=overrule_nan,
        skip_nan=skip_nan,
    )


def _build_grouper_payload(
    cpt_inputs: List[GrouperCptInput],
    *,
    building_polygon: Polygon | None,
    cpt_grid_rotation: float,
    gamma_bottom: float,
    gamma_shaft: float,
    include_centre_to_centre_check: bool,
    stiff_construction: bool,
    resolution: float,
    overrule_nan: float,
    skip_nan: bool,
) -> dict:
    """
    Shared core that builds the "/grouper/group_cpts" payload from a list of neutral
    `GrouperCptInput` records.

    Holds the NaN-handling coercion (`overrule_nan`/`skip_nan`), the equal-pile-tip-level
    validation and the "at least 2 valid CPTs" requirement, so both
    `create_grouper_payload` (PileCore dict) and
    `create_grouper_payload_from_bearing_results` (any `GrouperBearingResultsLike`) share
    exactly the same behaviour.
    """
    # create default payload object
    payload: Dict[str, Any] = {
        "cpt_grid_rotation": cpt_grid_rotation,
        "gamma_bottom": gamma_bottom,
        "gamma_shaft": gamma_shaft,
        "include_centre_to_centre_check": include_centre_to_centre_check,
        "stiff_construction": stiff_construction,
        "resolution": resolution,
    }

    # set source building polygon in payload
    if building_polygon is not None:
        payload["building_polygon"] = mapping(building_polygon)

    # set bearing capacity in payload
    cpt_objects = []
    pile_tip_level_object = {}
    for cpt_input in cpt_inputs:
        name = cpt_input.name
        has_nan = False
        # check if coordinate are set
        if cpt_input.x is None or cpt_input.y is None:
            raise ValueError(
                f" CPT {name} does not have a x-coordinate or y-coordinate"
            )

        for item, values in (
            ("R_b_cal", cpt_input.R_b_cal),
            ("F_nk_d", cpt_input.F_nk_d),
            ("R_s_cal", cpt_input.R_s_cal),
        ):
            if np.isnan(values).any():
                if skip_nan:
                    has_nan = True
                    logging.warning(
                        f"CPT {name} has NaN values are present in column {item}. "
                        f"Not included in grouper payload."
                    )

                    break
                else:
                    logging.warning(
                        f"CPT {name} has NaN values are present in column {item}. "
                        f"Replace NaN with {overrule_nan}."
                    )
        # skip CPT that are not valid.
        if has_nan:
            continue

        # map pile tip levels to object
        pile_tip_level_object[name] = np.asarray(cpt_input.pile_tip_level_nap).tolist()

        # add bearing capacity result to object
        cpt_objects.append(
            {
                "bottom_bearing_capacity": np.nan_to_num(
                    cpt_input.R_b_cal, nan=overrule_nan
                ).tolist(),
                "negative_friction": np.nan_to_num(
                    cpt_input.F_nk_d, nan=overrule_nan
                ).tolist(),
                "shaft_bearing_capacity": np.nan_to_num(
                    cpt_input.R_s_cal, nan=overrule_nan
                ).tolist(),
                "name": name,
                "coordinates": {
                    "x": cpt_input.x,
                    "y": cpt_input.y,
                },
            }
        )

    if not len(cpt_objects) >= 2:
        raise ValueError(
            "The PileCore grouper requires at least 2 CPTs with valid bearing capacity."
        )

    payload["cpt_objects"] = cpt_objects

    # validate pile tip levels
    raw_lengths = [
        frozenset(np.round(values, 2)) for values in pile_tip_level_object.values()
    ]
    if len(list(set(raw_lengths))) > 1:
        msg = "The PileCore grouper requires all CPTs to have a valid bearing capacity for all pile tip levels. \n"
        for name, pile_tip_level in pile_tip_level_object.items():
            msg += (
                f"Pile tip levels are not similar for CPT {name} with length {len(pile_tip_level)}, "
                f"upper boundary: {max(pile_tip_level)}, lower boundary: {min(pile_tip_level)}. \n"
            )
        raise ValueError(msg)
    payload["pile_tip_level"] = sorted(list(raw_lengths[0]), reverse=True)

    return payload


def create_grouper_report_payload(
    grouper_payload: dict,
    grouper_response: dict,
    project_name: str,
    project_id: str,
    author: str,
    project_remark: str | None = None,
) -> dict:
    """
    Creates a dictionary with the payload content for the PileCore endpoint
    "grouper/generate_grouper_report"

    Parameters
    ----------
    grouper_payload:
       The resulting payload of a call to `create_grouper_payload()`
    grouper_response:
       The resulting response of a call to `get_groups_api_result()`
    project_name:
        The name of the project.
    project_id:
        The identifier (code) of the project.
    author:
        The author of the report.

    Returns
    -------
    report_payload:
        Dictionary with the payload content for the PileCore endpoint
        "grouper/generate_grouper_report"
    """
    report_payload = deepcopy(grouper_payload)
    report_payload.update(
        dict(
            sub_groups=grouper_response["sub_groups"],
            author=author,
            project_number=project_id,
            project_name=project_name,
            project_remark=project_remark,
        ),
    )
    # remove not used attributes
    _ = report_payload.pop("pile_tip_level")
    _ = report_payload.pop("cpt_objects")
    return report_payload
