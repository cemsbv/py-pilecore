from __future__ import annotations

from typing import Any, Dict, List, Mapping, Tuple

import numpy as np
import pandas as pd
from pygef.cpt import CPTData
from tqdm import tqdm

# Create input_table
results_passover = {}
soil_properties_list = []


def create_soil_properties_payload(
    cptdata_objects: List[CPTData],
    layer_tables: Dict[str, pd.DataFrame],
    groundwater_level_nap: float,
    friction_range_strategy: str,
    excavation_depth_nap: float | None = None,
    individual_negative_friction_range_nap: Mapping[Any, Tuple[float, str]]
    | None = None,
    individual_positive_friction_range_nap: Mapping[Any, Tuple[float, str]]
    | None = None,
) -> Tuple[List[dict], Dict[str, dict]]:
    """
    Creates a dictionary with the `soil_properties` payload content for the PileCore
    endpoints.

    Note that
    the dictionary should be converted to a jsonifyable message before it can be passed
    to a `requests` call directly, for instance with
    `nuclei.client.utils.python_types_to_message()`.

    Parameters
    ----------
    cptdata_objects:
        A list of pygef.CPTData objects
    layer_tables:
        A dictionary, mapping `CPTData.alias` values to pandas Dataframes with soil-layer
        information, containing the following columns:
            (index):
                Unique integer for soil-layer, starting at 0 for the top layer.
            depth_top (float):
                Depth w.r.t. surface level [m];
            thickness (float):
                Thickness of the layer [m];
            gamma (float):
                Dry volumetric weight [kN/m^3];
            gamma_sat (float):
                Saturated volumetric weight [kN/m^3];
            phi (float):
                Internal friction angle [rad];
            soil_code (str):
                Main components are specified with capital letters and are the following:
                    - G: gravel (Grind)
                    - Z: sand (Zand)
                    - L: loam (Leem)
                    - K: clay (Klei)
                    - V: peat (Veen)
            thickness (float):
                The layer thickness [m]
    groundwater_level_nap:
        The ground water level. Unit: [m] w.r.t. NAP.
    friction_range_strategy:
        Sets the method to determine the sleeve friction zones on the pile. The soil
        friction in the positive zone contributes to the bearing capacity, while the
        negative zone adds an extra load on the pile. Accepted values: "manual",
        "lower_bound" or "settlement_driven".
    excavation_depth_nap:
        Soil excavation depth after the CPT was taken. Unit: [m] w.r.t. NAP.
    individual_negative_friction_range_nap:
        A dictionary, mapping `CPTData.alias` values to fixed negative-friction ranges.
        For a specification of the values, see `fixed_negative_friction_range_nap`
    individual_positive_friction_range_nap:
        A dictionary, mapping `CPTData.alias` values to fixed positive-friction ranges.
        For a specification of the values, see `fixed_positive_friction_range_nap`

    Returns
    -------
    soil_properties_list:
        The `list_soil_properties` payload content of the PileCore-API multi-cpt
        endpoints.
    results_kwargs:
        Dictionary with keyword arguments for the `pilecore.MultiCPTBearingResults`
        object.
    """
    for cpt in tqdm(cptdata_objects):
        # Construct the cpt_data payload
        cpt_data = dict(
            depth=np.array(cpt.data["depth"], dtype=float),
            qc=np.array(cpt.data["coneResistance"], dtype=float).clip(0),
        )

        # Optionally add pore-pressure data to 'cpt_data'.
        if "porePressure" in cpt.data.columns:
            cpt_data["u"] = np.array(cpt.data["porePressure"])

        # Get the layer_table for this cpt from the layer-table dictionary
        layer_table = layer_tables[cpt.alias]

        # Construct the layer_table_data payload
        layer_table_data = dict(
            depth_btm=np.array(layer_table["depth_top"] + layer_table["thickness"]),
            gamma=np.array(layer_table["gamma"]),
            gamma_sat=np.array(layer_table["gamma_sat"]),
            index=np.array(layer_table.index),
            phi=np.array(layer_table["phi"]),
            soil_code=np.array(layer_table["soil_code"]),
            thickness=np.array(layer_table["thickness"]),
        )
        # Optionally add consolidation parameters to 'layer_table_data'.
        if "C_p" in layer_table.columns:
            layer_table_data["C_p"] = np.array(layer_table["C_p"])
        if "C_s" in layer_table.columns:
            layer_table_data["C_s"] = np.array(layer_table["C_s"])

        # Create the Soil-Properties payload
        soil_properties = dict(
            cpt_data=cpt_data,
            layer_table_data=layer_table_data,
            ref_height=cpt.delivered_vertical_position_offset,
            test_id=cpt.alias,
            groundwater_level_nap=groundwater_level_nap
            if groundwater_level_nap is not None
            else cpt.delivered_vertical_position_offset - 1,
            coordinates=dict(x=cpt.delivered_location.x, y=cpt.delivered_location.y),
        )
        # Optionally add cpt-specific friction-range parameters
        if friction_range_strategy == "manual":
            if (
                individual_negative_friction_range_nap is not None
                and cpt.alias in individual_negative_friction_range_nap.keys()
            ):
                soil_properties[
                    "fixed_negative_friction_range_nap"
                ] = individual_negative_friction_range_nap[cpt.alias]
            if (
                individual_positive_friction_range_nap is not None
                and cpt.alias in individual_positive_friction_range_nap.keys()
            ):
                soil_properties[
                    "fixed_positive_friction_range_nap"
                ] = individual_positive_friction_range_nap[cpt.alias]

        soil_properties_list.append(soil_properties)
        results_passover[cpt.alias] = {
            "ref_height": cpt.delivered_vertical_position_offset,
            "surface_level_nap": excavation_depth_nap
            if excavation_depth_nap is not None
            else cpt.delivered_vertical_position_offset,
        }

    return soil_properties_list, results_passover
