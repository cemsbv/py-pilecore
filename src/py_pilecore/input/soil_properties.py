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
    groundwater_level: float,
    friction_range_strategy: str,
    excavation_depth_nap: float | None = None,
    set_negative_friction_range_nap: Mapping[Any, Tuple[float, str]] | None = None,
    set_positive_friction_range_nap: Mapping[Any, Tuple[float, str]] | None = None,
) -> Tuple[List[dict], Dict[str, dict]]:
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
            groundwater_level_nap=groundwater_level
            if groundwater_level is not None
            else cpt.delivered_vertical_position_offset - 1,
            coordinates=dict(x=cpt.delivered_location.x, y=cpt.delivered_location.y),
        )
        # Optionally add cpt-specific friction-range parameters
        if friction_range_strategy == "manual":
            if (
                set_negative_friction_range_nap is not None
                and cpt.alias in set_negative_friction_range_nap.keys()
            ):
                soil_properties[
                    "fixed_negative_friction_range_nap"
                ] = set_negative_friction_range_nap[cpt.alias]
            if (
                set_positive_friction_range_nap is not None
                and cpt.alias in set_positive_friction_range_nap.keys()
            ):
                soil_properties[
                    "fixed_positive_friction_range_nap"
                ] = set_positive_friction_range_nap[cpt.alias]

        soil_properties_list.append(soil_properties)
        results_passover[cpt.alias] = {
            "ref_height": cpt.delivered_vertical_position_offset,
            "surface_level_nap": excavation_depth_nap
            if excavation_depth_nap is not None
            else cpt.delivered_vertical_position_offset,
        }

    return soil_properties_list, results_passover
