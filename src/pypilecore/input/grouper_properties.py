from __future__ import annotations

from copy import deepcopy
from typing import Dict, List, Literal

from shapely.geometry import Polygon, mapping

from ..results import SingleCPTBearingResults


def create_grouper_payload(
    cpt_results_dict: Dict[str, SingleCPTBearingResults],
    pile_load_uls: float,
    building_polygon: Polygon | None = None,
    cpt_grid_rotation: float = 0.0,
    gamma_bottom: float = 1.2,
    gamma_shaft: float = 1.2,
    include_centre_to_centre_check: bool = False,
    stiff_construction: bool = False,
    optimize_result_by: List[
        Literal[
            "minimum_pile_level",
            "number_of_cpts",
            "number_of_consecutive_pile_levels",
            "centre_to_centre_check",
        ]
    ]
    | None = [
        "minimum_pile_level",
        "number_of_cpts",
        "number_of_consecutive_pile_levels",
    ],
    resolution: float = 0.5,
) -> dict:
    """
    Creates a dictionary with the payload content for the PileCore endpoint
    "/grouper/group_cpts"


    Notes
    ------
    The grouper uses pile bearing capacity results calculated by PileCore or other software to
    form  subgroups of the total group of CPT’s belonging to this project.
    Valid subgroups have three characteristics:
        - a maximum variation coefficient of 12% at one or more pile-tip levels. (Variation check
        NEN9997-1 A.3.3.3)
        - a minimum design pile bearing capacity based on the given pile load ULS at one or more
        pile-tip levels. (Bearing check)
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
        Dictionary with key as CPT name and value a SingleCPTBearingResults class
    pile_load_uls
        ULS load in kN. Used to determine if a grouping configuration is valid.
    stiff_construction
        Default is False
        Attribute use to get the xi3 and xi4 value. True if it is a stiff construction
    optimize_result_by
        Default is "minimum_pile_level", "number_of_cpts", "number_of_consecutive_pile_levels"
        Attribute that states how to sort the result and find groups.
        Based on the filter method, a selection of valid subgroups are included in the report. The following
        filters are available:
            - Number_of_cpts: the grouper adds filters to make the group as big as possible to try and get a
            uniform pile tip level for most CPT’s.
            - Number_of_consecutive_pile_levels; the grouper adds filters to get groups that contain consecutive
            pile tip levels to ensure a consistent soil layer is used.
            - Minimum_pile_level; the grouper adds filters to return groups that optimize pile length to try and
            optimize or reduce material use.
            - Centre_to_centre_check; the grouper adds filters to favour groups that are valid according to the
            centre to centre rules of the NEN9997-1 3.2.3.
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

    Raises
    ------
    ValueError:
        - if NaN values are present in negative friction, bottom or shaft bearing_capacity
        - if x or y coordinate is None
        - if pile tip levels don't macht for all SingleCPTBearingResults

    Returns
    -------
    payload:
        Dictionary with the payload content for the PileCore endpoint
        "/grouper/group_cpts"
    """
    # create default payload object
    payload = {
        "cpt_grid_rotation": cpt_grid_rotation,
        "gamma_bottom": gamma_bottom,
        "gamma_shaft": gamma_shaft,
        "include_centre_to_centre_check": include_centre_to_centre_check,
        "pile_load_uls": pile_load_uls,
        "stiff_construction": stiff_construction,
        "resolution": resolution,
        "optimize_result_by": optimize_result_by,
    }

    # set source building polygon in payload
    if building_polygon is not None:
        payload["building_polygon"] = mapping(building_polygon)

    # set bearing capacity in payload
    cpt_objects = []
    pile_tip_level_object = {}
    for name, cpt_result in cpt_results_dict.items():
        # check if coordinate are set
        if cpt_result.soil_properties.x is None:
            raise ValueError(f" CPT {name} does not have a x-coordinate")
        if cpt_result.soil_properties.y is None:
            raise ValueError(f"CPT {name} does not have a y-coordinate")

        for item in ["R_b_cal", "F_nk_cal", "R_s_cal"]:
            if cpt_result.results_df[item].isnull().values.any():
                raise ValueError(
                    f"CPT {name} has NaN values are present in column {item}."
                )

        # map pile tip levels to object
        pile_tip_level_object[name] = cpt_result.results_df[
            "pile_tip_level_nap"
        ].tolist()

        # add bearing capacity result to object
        cpt_objects.append(
            {
                "bottom_bearing_capacity": cpt_result.results_df["R_b_cal"].tolist(),
                "negative_friction": cpt_result.results_df["F_nk_cal"].tolist(),
                "shaft_bearing_capacity": cpt_result.results_df["R_s_cal"].tolist(),
                "name": name,
                "coordinates": {
                    "x": cpt_result.soil_properties.x,
                    "y": cpt_result.soil_properties.y,
                },
            }
        )
    payload["cpt_objects"] = cpt_objects

    # validate pile tip levels
    raw_lengths = [frozenset(values) for values in pile_tip_level_object.values()]
    if len(list(set(raw_lengths))) > 1:
        msg = "For the grouper payload must all CPT's have a valid bearing capacity for all pile tip levels. \n"
        for name, pile_tip_level in pile_tip_level_object.items():
            msg += f"Pile tip levels are not similar for CPT {name} with length {len(pile_tip_level)}. \n"
        raise ValueError(msg)
    payload["pile_tip_level"] = list(raw_lengths[0])

    return payload


def create_grouper_report_payload(
    grouper_payload: dict,
    grouper_response: dict,
    project_name: str,
    project_id: str,
    author: str,
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
            sub_groups=grouper_response,
            author=author,
            project_id=project_id,
            project_name=project_name,
        ),
    )
    _ = report_payload.pop("pile_tip_level")
    return report_payload