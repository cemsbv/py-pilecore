from __future__ import annotations

from typing import Any, Dict, List, Literal, Mapping, Tuple

import numpy as np
from pygef.cpt import CPTData
from tqdm import tqdm

transform = {
    "rocks": "G",
    "gravel": "G",
    "sand": "Z",
    "silt": "L",
    "clay": "K",
    "peat": "V",
}


def create_soil_properties_payload(
    cptdata_objects: List[CPTData],
    classify_tables: Dict[str, dict],
    groundwater_level_nap: float,
    friction_range_strategy: Literal["manual", "lower_bound", "settlement_driven"],
    excavation_depth_nap: float | None = None,
    master_ocr: float | None = None,
    individual_negative_friction_range_nap: Mapping[Any, Tuple[float, float]]
    | None = None,
    individual_positive_friction_range_nap: Mapping[
        Any, Tuple[float, Literal["ptl"] | float]
    ]
    | None = None,
    individual_ocr: Mapping[Any, float] | None = None,
    verbose: bool = False,
) -> Tuple[List[dict], Dict[str, dict]]:
    """
    Creates a dictionary with the `soil_properties` payload content for the PileCore
    endpoints.

    Note
    ------
    the dictionary should be converted to a jsonifyable message before it can be passed
    to a `requests` call directly, for instance with
    `nuclei.client.utils.python_types_to_message()`.

    Parameters
    ----------
    cptdata_objects:
        A list of pygef.CPTData objects
    classify_tables:
        A dictionary, mapping `CPTData.alias` values to dictionary with the resulting response
        of a call to CPTCore `classify/*` information, containing the following keys:
            geotechnicalSoilName: Sequence[str]
                geotechnical Soil Name related to the ISO
            lowerBoundary: Sequence[float]
                lower boundary of the layer [m]
            upperBoundary: Sequence[float]
                upper boundary of the layer [m]
            color: Sequence[str]
                hex color code
            mainComponent: Sequence[Literal["rocks", "gravel", "sand", "silt", "clay", "peat"]]
                main soil component
            cohesion: Sequence[float]
                cohesion of the layer [kPa]
            gamma_sat: Sequence[float]
                Saturated unit weight [kN/m^3]
            gamma_unsat: Sequence[float]
                unsaturated unit weight [kN/m^3]
            phi: Sequence[float]
                phi [degrees]
            undrainedShearStrength: Sequence[float]
                undrained shear strength [kPa]
    groundwater_level_nap:
        The groundwater level. Unit: [m] w.r.t. NAP.
    friction_range_strategy:
        Sets the method to determine the sleeve friction zones on the pile. The soil
        friction in the positive zone contributes to the bearing capacity, while the
        negative zone adds an extra load on the pile. Accepted values: "manual",
        "lower_bound" or "settlement_driven".
    excavation_depth_nap:
        Soil excavation depth after the CPT was taken. Unit: [m] w.r.t. NAP.
    ocr:
        The Over-Consolidation-Ratio [-] of the foundation layer.
    individual_negative_friction_range_nap:
        A dictionary, mapping `CPTData.alias` values to fixed negative-friction ranges.
        For a specification of the values, see `fixed_negative_friction_range_nap`
    individual_positive_friction_range_nap:
        A dictionary, mapping `CPTData.alias` values to fixed positive-friction ranges.
        For a specification of the values, see `fixed_positive_friction_range_nap`
    individual_ocr:
        A dictionary, mapping ``CPTData.alias`` values to Over-Consolidation-Ratio [-]
        values of the foundation layer. This will overrule the general `ocr` setting for
        these specific CPTs only.
    verbose:
        If True, show progress bars and status messages in stdout.

    Returns
    -------
    soil_properties_list:
        The `list_soil_properties` payload content of the PileCore-API multi-cpt
        endpoints.
    results_kwargs:
        Dictionary with keyword arguments for the `pilecore.MultiCPTBearingResults`
        object.
    """
    # Initialize outputs
    results_passover = {}
    soil_properties_list = []

    pbar = None
    if verbose:
        pbar = tqdm(total=len(cptdata_objects))
    for cpt in cptdata_objects:
        # Push verbose message
        if pbar:
            pbar.update()
            pbar.set_description(f"Create soil properties payload for CPT: {cpt.alias}")

        # Construct the cpt_data payload
        cpt_data = dict(
            depth=np.array(cpt.data["depth"], dtype=float),
            qc=np.array(cpt.data["coneResistance"], dtype=float).clip(0),
        )

        # Optionally add pore-pressure data to 'cpt_data'.
        if "porePressure" in cpt.data.columns:
            cpt_data["u"] = np.array(cpt.data["porePressure"])

        # Get the layer_table for this cpt from the layer-table dictionary
        if cpt.alias not in classify_tables.keys():
            raise ValueError(f"{cpt.alias} not in `classify_tables`")
        layer_table = classify_tables[cpt.alias]

        # Construct the layer_table_data payload
        layer_table_data = dict(
            depth_btm=layer_table["lowerBoundary"],
            gamma=layer_table["gamma_unsat"],
            gamma_sat=layer_table["gamma_sat"],
            index=list(range(0, len(layer_table["gamma_sat"]))),
            phi=layer_table["phi"],
            soil_code=[transform[soil] for soil in layer_table["mainComponent"]],
            thickness=(
                np.array(layer_table["lowerBoundary"])
                - np.array(layer_table["upperBoundary"])
            ).tolist(),
        )
        # Optionally add consolidation parameters to 'layer_table_data'.
        if "C_p" in layer_table.keys():
            layer_table_data["C_p"] = layer_table["C_p"]
        if "C_s" in layer_table.keys():
            layer_table_data["C_s"] = layer_table["C_s"]

        # Create the Soil-Properties payload
        soil_properties = dict(
            cpt_data=cpt_data,
            layer_table_data=layer_table_data,
            ref_height=cpt.delivered_vertical_position_offset,
            test_id=cpt.alias,
            groundwater_level_nap=groundwater_level_nap
            if groundwater_level_nap is not None
            else cpt.delivered_vertical_position_offset - 1,
        )

        # Optionally add coordinates
        if (
            cpt.delivered_location is not None
            and cpt.delivered_location.x is not None
            and cpt.delivered_location.y is not None
        ):
            soil_properties["coordinates"] = {
                "x": cpt.delivered_location.x,
                "y": cpt.delivered_location.y,
            }

        # Optionally add cpt-specific friction-range parameters
        if (
            individual_negative_friction_range_nap is not None
            and cpt.alias in individual_negative_friction_range_nap.keys()
        ):
            soil_properties[
                "fixed_negative_friction_range_nap"
            ] = individual_negative_friction_range_nap[cpt.alias]
            soil_properties["friction_range_strategy"] = "manual"
        if (
            individual_positive_friction_range_nap is not None
            and cpt.alias in individual_positive_friction_range_nap.keys()
        ):
            soil_properties[
                "fixed_positive_friction_range_nap"
            ] = individual_positive_friction_range_nap[cpt.alias]
            soil_properties["friction_range_strategy"] = "manual"

        # Optionally add OCR parameter
        if individual_ocr is not None and cpt.alias in individual_ocr.keys():
            ocr: float | None = individual_ocr[cpt.alias]
        else:
            ocr = master_ocr
        if ocr is not None:
            soil_properties["ocr"] = ocr

        soil_properties_list.append(soil_properties)
        results_passover[cpt.alias] = {
            "ref_height": cpt.delivered_vertical_position_offset,
            "surface_level_nap": excavation_depth_nap
            if excavation_depth_nap is not None
            else cpt.delivered_vertical_position_offset,
            "location": {"x": cpt.delivered_location.x, "y": cpt.delivered_location.y},
        }

    return soil_properties_list, results_passover
