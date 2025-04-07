# Generic Imports
import datetime
import io
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

import numpy as np
import pandas as pd

# Specific libraries
import pygef
from matplotlib import pyplot as plt
from nuclei.client import NucleiClient
from tqdm import tqdm  # progress bar

from pypilecore import api, create_basic_pile
from pypilecore.common.piles.grid import PileGridProperties
from pypilecore.input.tension import create_multi_cpt_payload
from pypilecore.results import (
    CasesMultiCPTBearingResults,
    MultiCPTTensionBearingResults,
)
from pypilecore.viewers import (
    ViewerCptGroupResults,
    ViewerCptResults,
    ViewerCptResultsPlanView,
)

# Additional Setup
pd.set_option("display.max_columns", None)
logging.getLogger().setLevel(logging.INFO)
# Initialize CEMS API client

client = NucleiClient()
client.routing["PileCore"]["v3"] = "http://staging.crux-nuclei.com/api/pilecore"

def main_test():
    """cpt info"""
    cpt_path = r"notebooks/87362_DKM148.gef"
    cpt = [pygef.read_cpt(cpt_path)]

    """ pile info """

    # create pile
    pile = create_basic_pile(
        pile_name="PREFAB 250X250 mm",
        main_type="concrete",
        specification="1",
        installation=None,
        pile_shape="rectangle",
        height_base=None,
        core_secondary_dimension=0.25,
        core_tertiary_dimension=0.25,
        base_secondary_dimension=None,
        base_tertiary_dimension=None,
        pile_material="concrete",
        settlement_curve=1,
        adhesion=None,
        alpha_t_sand=0.007,
        alpha_t_clay=0.014,
        beta_p=None,
        pile_tip_factor_s=None,
        is_auger=None,
        is_low_vibrating=False,
        negative_fr_delta_factor=None,
    )

    pile_head_level_nap = "surface"  # The level of the pile-head [m] w.r.t. NAP.# Must be a number, or the string "surface".

    """ excavation """
    excavation_depth_nap = None  # The depth [m w.r.t. NAP] of the surface-level after excavation. Has to be a number or None.
    # ** excavation_param_t:
    # Required when providing an excavation_depth. The values can be:
    # - 1.0: if installation is not low in vibration (niet-trillingsarm) and piles are installed after excavating
    # - 0.5: (wortel-methode) if piles have been installed before excavation or installation is low-vibrating
    excavation_param_t = 1.0

    """ constructie """
    stiff_construction = True  # Accepted values: [True, False]

    # Maximum tension force on pile Ft;max;k (positive value).
    pile_load_sls_max = 100

    # Positive values (tension force), negative values (compression force) and 0.0 are accepted. Note that the
    # positive must be <= `pile_load_sls_max`
    pile_load_sls_min = -100

    soil_load_sls = 0.0  # The overburden-pressure/surcharge at surface-level [kPa]. Can be None, then defaults to 0.0.

    """ schachtwrijving """
    # Generic for all cpts. Level w.r.t. NAP or None, then pile_head_level_nap is used

    # Please note that chaging the top_of_tension_zone_nap have in impact on the
    # pile settelement calculation. All values above this level will be ignored resulting in a lower pile displacement.
    # PileCore will correct for remarks regarding L;a for CUR236 6.1.1.
    top_of_tension_zone_nap = 0.85

    # If desired, you can also specify top_of_tension_zone_nap values per CPT
    # The values provided below will overwrite the top_of_tension_zone_nap for those specific CPTs.

    # dictionary with key cpt name and top_of_tension_zone_nap value
    # e.g.: {"S03": 1.5}
    # individual_top_of_tension_zone_nap: Mapping[Any, float] = {}
    individual_top_of_tension_zone_nap: Mapping[Any, Tuple[float, str]] = {
        "DKM147": -5.3
    }

    """ OCR """
    ocr = None  # None defaults to 1.0
    individual_ocr: Mapping[
        Any, float
    ] = {}  # OCR for specific cpts; # e.g.: {"S03": 1.5}

    """ Veiligheidsfactoren """
    gamma_gamma = (
        1.1  # Partial factor for volumetric soil weight. A.3.2 NEN 9997-1+C2 (nl)
    )

    gamma_r_b = 1.2  # Safety factor on the pile-tip bearing capacity

    gamma_r_s = 1.2  # Safety factor on the sleeve-friction bearing capacity

    gamma_f_nk = 1.0  # Safety factor on the negative friction

    gamma_s_t = 1.35  # Pile resistance factor gamma_s;t used to compute the

    overrule_xi = 1.39

    """ specific trekmodule input"""
    # Maximum void ratio of the soil (the loosest packing). For normally consolidated
    # sands in The Netherlands, an emax = 0.80 can be used in most cases.
    void_ratio_max = 0.8

    # Minimum void ratio of the soil (the densest packing). For normally consolidated
    # sands in The Netherlands, an emin = 0.40 can be used in most cases.
    void_ratio_min = 0.4

    # if None pile is calculated as a single pile
    center_to_center_distance = 1.3

    # - center pile `pile_location= 4`
    # - middle pile `pile_location= 1 or 3 or 4 or 5 or 7`
    # - corner pile `pile_location= 0 or 2 or 6 or 8`

    #     6 --- 7 --- 8
    #     |     |     |
    #     3 --- 4 --- 5
    #     |     |     |
    #     0 --- 1 --- 2   with --- is | is center_to_center_distance
    pile_location = 4

    if center_to_center_distance:
        pile_grid = PileGridProperties.regular(
            ctc=center_to_center_distance, index_location=pile_location
        )
        pile_grid.plot_overview()
    else:
        pile_grid = None

    classify_method = "cur"
    apply_qc3_reduction = None

    """ custom material """
    # ** custom_material
    # By placing info other than None here, you are overriding the existing material.
    # A custom material definition. Assign the "name" property as `pile_material` to use it.
    # example:
    # custom_material = {
    #     "name": "custom_material",
    #     "elastic_modulus": 15e3,    # [MPa]
    #     "color": "#ff0000",        # Hexadecimal color
    # }
    custom_material = None

    standard = "NEN9997-1"

    """ CALCULATION """

    # create output list
    cems_result_divisions = []

    # loop over different cpt groups

    # get classify tables
    classify_tables = get_classify_tables(cpt, classify_method)
    for classify_table in classify_tables.values():
        # Dump to json
        with open(r"notebooks/classify_table.json", "w") as f:
            json.dump(classify_table, f, indent=4)

    # Get results
    multi_cpt_payload, results_passover = create_multi_cpt_payload(
        cptdata_objects=cpt,
        classify_tables=classify_tables,
        groundwater_level_nap=+1.8,
        excavation_depth_nap=excavation_depth_nap,
        pile=pile,
        excavation_param_t=excavation_param_t,
        pile_head_level_nap=pile_head_level_nap,
        pile_tip_levels_nap=[-8.0, -13.5, -14.0, -15.0, -15.5, -20.0],
        gamma_f_nk=gamma_f_nk,
        gamma_r_b=gamma_r_b,
        gamma_r_s=gamma_r_s,
        gamma_s_t=gamma_s_t,
        overrule_xi=overrule_xi,
        void_ratio_max=0.8,
        void_ratio_min=0.4,
        pile_load_sls_max=pile_load_sls_max,
        pile_load_sls_min=pile_load_sls_min,
        soil_load_sls=soil_load_sls,
        stiff_construction=stiff_construction,
        ocr=ocr,
        individual_ocr=individual_ocr,
        pile_grid=pile_grid,
        top_of_tension_zone_nap=top_of_tension_zone_nap,
        individual_top_of_tension_zone_nap=individual_top_of_tension_zone_nap,
        construction_sequence="cpt-pile",
    )

    api_response = api.get_multi_cpt_api_result_tension(
        client=client, payload=multi_cpt_payload, standard=standard
    )

    multi_bearing_results = MultiCPTTensionBearingResults.from_api_response(
        response_dict=api_response,
        cpt_input=results_passover,
    )

    cems_result_divisions.append(multi_bearing_results)

    # create output
    from pypilecore.input.multi_cpt import create_multi_cpt_report_payload

    individual_cpt_results_content = True  # [True, False]
    result_summary_content = True  # [True, False]
    group_results_content = False
    # Close all open plots to save memory
    plt.close("All")

    multi_cpt_report_payload = create_multi_cpt_report_payload(
        multi_cpt_payload=multi_cpt_payload,
        project_name=f"test tension",
        project_id=str(000),
        author="me myself and I",
        date=datetime.date.today().strftime("%d-%m-%y"),
        group_results_content=group_results_content,
        individual_cpt_results_content=individual_cpt_results_content,
        result_summary_content=result_summary_content,
    )

    report = api.get_multi_cpt_api_report_tension(
        client=client, payload=multi_cpt_report_payload
    )

    with open(r"notebooks/issue_guido_abt.pdf", "wb") as f:
        f.write(report)


def get_classify_tables(cptdata_objects, classify_method):
    classify_tables: Dict[str, dict] = {}

    for i, cpt in tqdm(enumerate(cptdata_objects), desc="Classify CPT's"):
        # remove nan data
        data = cpt.data.drop_nulls()
        # classify CPT with CPTCore
        payload = {
            "aggregateLayersPenalty": 500,
            "minimumSegmentLength": 50,
            "data": {
                "coneResistance": data.get_column("coneResistance")
                .clip(0, 50)
                .to_list(),
                "correctedPenetrationLength": data.get_column("depth").to_list(),
                "localFriction": data.get_column("localFriction").clip(0, 50).to_list(),
            },
            "verticalPositionOffset": cpt.delivered_vertical_position_offset,
            "x": cpt.delivered_location.x,
            "y": cpt.delivered_location.y,
        }
        if "porePressureU2" in data.columns:
            payload["data"]["porePressureU2"] = (
                data.get_column("porePressureU2").clip(0, 50).to_list(),
            )[0]

        response = client.session.post(
            f"https://crux-nuclei.com/api/cptcore/v1/classify/{classify_method}",
            json=payload,
        )
        if not response.ok:
            cptdata_objects.pop(i)
            print(
                f"RuntimeError: {cpt.alias} could not be classified. \n Statuse code: {response.status_code} and {response.text}"
            )
            continue

        classify_tables[cpt.alias] = response.json()
        return classify_tables


if __name__ == "__main__":
    # initialise project

    project = main_test()
