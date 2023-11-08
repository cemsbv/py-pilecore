import logging
from typing import List

import numpy as np
import pytest
from pygef.cpt import CPTData

from pypilecore.input import (
    create_grouper_payload,
    create_pile_properties_payload,
    create_soil_properties_payload,
)
from pypilecore.results import MultiCPTBearingResults

LOGGER = logging.getLogger(__name__)


def test_create_soil_properties_payload(
    cpt: CPTData, mock_classify_response: dict
) -> None:
    """
    Test creating the soil-properties payload with the `create_soil_properties_payload`
    function.
    """

    # test creating the soil_properties payload
    payload, passover = create_soil_properties_payload(
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: mock_classify_response},
        groundwater_level_nap=-2.5,
        friction_range_strategy="manual",
    )

    assert isinstance(payload, list)
    assert isinstance(passover, dict)


def test_create_pile_properties_payload_green_path() -> None:
    """
    Test creating the soil-properties payload with the `create_soil_properties_payload`
    function.
    """

    def validate_pile_properties_payload(
        payload: dict, shape: str, props: List[str]
    ) -> None:
        # Check that the payload is a dictionary
        assert isinstance(payload, dict), type(payload)

        # Check that the main keys are present
        for key in ["props", "type"]:
            assert key in payload.keys()

        # Check that the pile shape is correct
        assert payload["type"] == shape

        # Check that the props key contains a dictionary
        assert isinstance(payload["props"], dict), type(payload["props"])

        # Check that the expected keys are present under "props"
        for key in ["pile_type_specification", *props]:
            assert key in payload["props"].keys()
            # Delete the key from the dict
            del payload["props"][key]

        # Check that no unexpected keys were present in the dictionary
        assert len(payload["props"]) == 0

    # test green path for round piles with minimal input
    payload = create_pile_properties_payload(
        pile_type="A",
        specification="concrete",
        installation="1",
        pile_shape="round",
        diameter_base=0.5,
    )

    validate_pile_properties_payload(payload, "round", ["diameter_base"])

    # test green path for round piles with extended input
    payload = create_pile_properties_payload(
        pile_type="A",
        specification="concrete",
        installation="1",
        pile_shape="round",
        diameter_base=0.5,
        diameter_shaft=0.4,
        height_base=1,
    )

    validate_pile_properties_payload(
        payload, "round", ["diameter_base", "diameter_shaft", "height_base"]
    )

    # test green path for round piles with extended input
    payload = create_pile_properties_payload(
        pile_type="A",
        specification="concrete",
        installation="1",
        pile_shape="round",
        diameter_base=0.5,
        diameter_shaft=0.4,
        height_base=1.0,
        settlement_curve=1,
        adhesion=50,
        alpha_p=1,
        alpha_s_clay=0.1,
        alpha_s_sand=0.1,
        beta_p=1,
        pile_tip_factor_s=1,
        elastic_modulus=1e3,
        is_auger=True,
        is_low_vibrating=True,
        negative_fr_delta_factor=1.2,
    )

    validate_pile_properties_payload(
        payload,
        "round",
        [
            "diameter_base",
            "diameter_shaft",
            "height_base",
            "settlement_curve",
            "adhesion",
            "alpha_p",
            "alpha_s_clay",
            "alpha_s_sand",
            "beta_p",
            "pile_tip_factor_s",
            "elastic_modulus",
            "is_auger",
            "is_low_vibrating",
            "negative_fr_delta_factor",
        ],
    )

    # test green path for rect piles
    payload = create_pile_properties_payload(
        pile_type="A",
        specification="concrete",
        installation="1",
        pile_shape="rect",
        width_base_large=0.5,
    )

    validate_pile_properties_payload(payload, "rect", ["width_base_large"])

    # test green path for rect piles with extended input
    payload = create_pile_properties_payload(
        pile_type="A",
        specification="concrete",
        installation="1",
        pile_shape="rect",
        width_base_large=0.5,
        width_base_small=0.4,
    )

    validate_pile_properties_payload(
        payload, "rect", ["width_base_large", "width_base_small"]
    )

    # test green path for rect piles with extended input
    payload = create_pile_properties_payload(
        pile_type="A",
        specification="concrete",
        installation="1",
        pile_shape="rect",
        width_base_large=0.5,
        width_base_small=0.4,
        width_shaft_large=0.4,
        width_shaft_small=0.3,
        height_base=1,
    )

    validate_pile_properties_payload(
        payload,
        "rect",
        [
            "width_base_large",
            "width_base_small",
            "width_shaft_large",
            "width_shaft_small",
            "height_base",
        ],
    )

    # test green path for round piles with extended input
    payload = create_pile_properties_payload(
        pile_type="A",
        specification="concrete",
        installation="1",
        pile_shape="rect",
        width_base_large=0.5,
        width_base_small=0.4,
        width_shaft_large=0.4,
        width_shaft_small=0.3,
        height_base=1,
        settlement_curve=1,
        adhesion=50,
        alpha_p=1,
        alpha_s_clay=0.1,
        alpha_s_sand=0.1,
        beta_p=1,
        pile_tip_factor_s=1,
        elastic_modulus=1e3,
        is_auger=True,
        is_low_vibrating=True,
        negative_fr_delta_factor=1.2,
    )

    validate_pile_properties_payload(
        payload,
        "rect",
        [
            "width_base_large",
            "width_base_small",
            "width_shaft_large",
            "width_shaft_small",
            "height_base",
            "settlement_curve",
            "adhesion",
            "alpha_p",
            "alpha_s_clay",
            "alpha_s_sand",
            "beta_p",
            "pile_tip_factor_s",
            "elastic_modulus",
            "is_auger",
            "is_low_vibrating",
            "negative_fr_delta_factor",
        ],
    )

    # Raise ValueError for unrecognized pile_shape
    with pytest.raises(ValueError):
        create_pile_properties_payload(
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="square",
            width_base_large=0.5,
        )

    # Raise ValueError for missing round geometry
    with pytest.raises(ValueError):
        create_pile_properties_payload(
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="round",
        )

    # Raise ValueErrror for missing base height round pile
    with pytest.raises(ValueError):
        create_pile_properties_payload(
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="round",
            diameter_base=0.5,
            diameter_shaft=0.4,
        )

    # Raise ValueErrror for missing base height rect pile
    with pytest.raises(ValueError):
        payload = create_pile_properties_payload(
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="rect",
            width_base_large=0.5,
            width_base_small=0.4,
            width_shaft_large=0.4,
            width_shaft_small=0.3,
        )

    # Raise ValueError when providing rect geometry for round pile shape
    with pytest.raises(ValueError):
        create_pile_properties_payload(
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="round",
            width_base_large=0.5,
        )

    # Raise ValueError for missing rect geometry
    with pytest.raises(ValueError):
        create_pile_properties_payload(
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="rect",
        )

    # Raise ValueError when providing round geometry for rect pile shape
    with pytest.raises(ValueError):
        create_pile_properties_payload(
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="rect",
            diameter_base=0.5,
        )


def test_create_grouper_payload(
    caplog, mock_multi_cpt_bearing_response, mock_results_passover
) -> None:
    cptgroupresults = MultiCPTBearingResults.from_api_response(
        mock_multi_cpt_bearing_response, mock_results_passover
    )

    create_grouper_payload(
        cptgroupresults.cpt_results.cpt_results_dict, pile_load_uls=100
    )

    # test value error
    single_cpt_results = cptgroupresults.cpt_results.cpt_results_dict["9"]
    with pytest.raises(ValueError):
        single_cpt_results.soil_properties.__setattr__("_x", None)
        create_grouper_payload(
            cptgroupresults.cpt_results.cpt_results_dict, pile_load_uls=100
        )
    single_cpt_results.soil_properties.__setattr__("_x", 0)

    arr = single_cpt_results.table.__getattribute__("R_b_cal")
    arr[-1] = np.nan
    with caplog.at_level(logging.WARNING):
        single_cpt_results.table.__setattr__("R_b_cal", arr)
        create_grouper_payload(
            cptgroupresults.cpt_results.cpt_results_dict, pile_load_uls=100
        )

        assert "CPT 9 has NaN values are present in column R_b_cal. " in caplog.text

    arr = single_cpt_results.table.__getattribute__("pile_tip_level_nap")
    single_cpt_results.table.__setattr__("pile_tip_level_nap", arr[:-1])
    with pytest.raises(ValueError):
        create_grouper_payload(
            cptgroupresults.cpt_results.cpt_results_dict, pile_load_uls=100
        )
