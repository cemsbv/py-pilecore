import logging
from typing import List

import numpy as np
import pytest
from pygef.cpt import CPTData

from pypilecore.input import (
    create_grouper_payload,
    create_multi_cpt_payload,
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

    payload = create_grouper_payload(
        cptgroupresults.cpt_results.cpt_results_dict, pile_load_uls=100
    )

    # check if pile tip levels are sorted
    assert payload["pile_tip_level"] == [1.0, 0.5, 0.0, -0.5]

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


def test_create_multi_cpt_payload_defaults(
    cpt: CPTData, mock_classify_response: dict
) -> None:
    """
    Test creating the multi_cpt_results payload with the `create_multi_cpt_payload`
    function with minimal arguments.
    """
    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[0, 1],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: mock_classify_response},
        groundwater_level_nap=-2.5,
        pile_type="concrete",
        specification="1",
        installation="A",
        pile_shape="round",
        diameter_base=0.3,
    )

    # Check the payload content

    # We don't completely check the soil_properties list here
    list_soil_properties = payload.pop("list_soil_properties")
    assert isinstance(list_soil_properties, list)
    assert len(list_soil_properties) == 1

    assert payload.pop("excavation_param_t") == 1.0
    assert payload.pop("pile_head_level_nap") == "surface"
    assert payload.pop("rel_pile_load") == 0.7
    assert payload.pop("friction_range_strategy") == "lower_bound"
    assert np.isclose(payload.pop("gamma_f_nk"), 1.0)
    assert np.isclose(payload.pop("gamma_r_b"), 1.2)
    assert np.isclose(payload.pop("gamma_r_s"), 1.2)
    pile_properties = payload.pop("pile_properties")
    assert pile_properties.get("type") == "round"
    pile_props = pile_properties.get("props")
    assert pile_props.pop("diameter_base") == 0.3

    # Check the pile-type-specification
    assert pile_props.pop("pile_type_specification") == dict(
        installation="A", pile_type="concrete", specification="1"
    )
    # Check that no extra keys are present in the pile_type_specification
    assert len(pile_props.keys()) == 0

    assert payload.pop("pile_tip_levels_nap") == [0, 1]
    assert np.isclose(payload.pop("soil_load"), 0.0)
    assert payload.pop("use_almere_rules") is False
    assert payload.pop("stiff_construction") is False

    # Check that no extra keys are present in the payload
    assert len(payload.keys()) == 0


def test_create_multi_cpt_payload_extended_round_pile(
    cpt: CPTData, mock_classify_response: dict
) -> None:
    """
    Test creating the multi_cpt_results payload with the `create_multi_cpt_payload`
    function with extended arguments for a round pile.
    """

    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[0, 1],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: mock_classify_response},
        groundwater_level_nap=-2.5,
        pile_type="concrete",
        specification="1",
        installation="A",
        pile_shape="round",
        diameter_base=0.3,
        friction_range_strategy="manual",
        stiff_construction=True,
        cpts_group=[cpt.alias],
        fixed_negative_friction_range_nap=(0.0, 5.0),
        fixed_positive_friction_range_nap=(5.0, "ptl"),
        negative_shaft_friction=0.0,
        apply_qc3_reduction=True,
        relative_pile_load=0.8,
        pile_load_sls=0.0,
        soil_load_sls=1.0,
        pile_head_level_nap=5.0,
        excavation_depth_nap=-2.0,
        excavation_param_t=0.5,
        gamma_f_nk=1.2,
        gamma_r_s=1.5,
        gamma_r_b=1.4,
        individual_negative_friction_range_nap={cpt.alias: (0.0, -5.0)},
        individual_positive_friction_range_nap={cpt.alias: (-5.0, "ptl")},
        diameter_shaft=0.25,
        height_base=0.5,
        settlement_curve=2,
        adhesion=0.01,
        alpha_p=0.01,
        alpha_s_clay=0.01,
        alpha_s_sand=0.01,
        beta_p=0.01,
        pile_tip_factor_s=0.01,
        elastic_modulus=0.01,
        is_auger=True,
        is_low_vibrating=True,
        negative_fr_delta_factor=0.01,
    )

    # Check the payload content

    # We don't completely check the soil_properties list here
    assert isinstance(payload.pop("list_soil_properties"), list)

    assert payload.pop("excavation_param_t") == 0.5
    assert payload.pop("pile_head_level_nap") == 5.0
    assert payload.pop("rel_pile_load") == 0.8
    assert payload.pop("friction_range_strategy") == "manual"
    assert np.isclose(payload.pop("gamma_f_nk"), 1.2)
    assert np.isclose(payload.pop("gamma_r_b"), 1.4)
    assert np.isclose(payload.pop("gamma_r_s"), 1.5)
    pile_properties = payload.pop("pile_properties")
    assert pile_properties.get("type") == "round"
    pile_props = pile_properties.get("props")
    assert np.isclose(pile_props.pop("diameter_base"), 0.3)
    assert np.isclose(pile_props.pop("diameter_shaft"), 0.25)
    assert np.isclose(pile_props.pop("height_base"), 0.5)
    assert pile_props.pop("settlement_curve") == 2
    assert np.isclose(pile_props.pop("adhesion"), 0.01)
    assert np.isclose(pile_props.pop("alpha_p"), 0.01)
    assert np.isclose(pile_props.pop("alpha_s_clay"), 0.01)
    assert np.isclose(pile_props.pop("alpha_s_sand"), 0.01)
    assert np.isclose(pile_props.pop("beta_p"), 0.01)
    assert np.isclose(pile_props.pop("pile_tip_factor_s"), 0.01)
    assert np.isclose(pile_props.pop("elastic_modulus"), 0.01)
    assert pile_props.pop("is_auger") is True
    assert pile_props.pop("is_low_vibrating") is True
    assert np.isclose(pile_props.pop("negative_fr_delta_factor"), 0.01)

    # Check the pile-type-specification
    assert pile_props.pop("pile_type_specification") == dict(
        installation="A", pile_type="concrete", specification="1"
    )
    # Check that no extra keys are present in the pile_type_specification
    assert len(pile_props.keys()) == 0

    assert payload.pop("pile_tip_levels_nap") == [0, 1]
    assert np.isclose(payload.pop("soil_load"), 1.0)
    assert payload.pop("use_almere_rules") is False
    assert payload.pop("stiff_construction") is True

    # Check the optional payload keys
    assert payload.pop("cpts_group") == [cpt.alias]
    assert payload.pop("fixed_negative_friction_range_nap") == (0.0, 5.0)
    assert payload.pop("fixed_positive_friction_range_nap") == (5.0, "ptl")
    assert np.isclose(payload.pop("f_nk"), 0.0)
    assert payload.pop("apply_qc3_reduction") is True
    assert np.isclose(payload.pop("pile_load"), 0.0)
    assert np.isclose(payload.pop("excavation_depth_nap"), -2.0)

    # Check that no extra keys are present in the payload
    assert len(payload.keys()) == 0


def test_create_multi_cpt_payload_extended_rect_pile(
    cpt: CPTData, mock_classify_response: dict
) -> None:
    """
    Test creating the multi_cpt_results payload with the `create_multi_cpt_payload`
    function with extended arguments for a rect pile.
    """

    assert isinstance(cpt.alias, str)

    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[0, 1],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: mock_classify_response},
        groundwater_level_nap=-2.5,
        pile_type="concrete",
        specification="1",
        installation="A",
        pile_shape="rect",
        width_base_large=0.3,
        friction_range_strategy="manual",
        stiff_construction=True,
        cpts_group=[cpt.alias],
        fixed_negative_friction_range_nap=(0.0, 5.0),
        fixed_positive_friction_range_nap=(5.0, "ptl"),
        negative_shaft_friction=0.0,
        apply_qc3_reduction=True,
        relative_pile_load=0.8,
        pile_load_sls=0.0,
        soil_load_sls=1.0,
        pile_head_level_nap=5.0,
        excavation_depth_nap=-2.0,
        excavation_param_t=0.5,
        gamma_f_nk=1.2,
        gamma_r_s=1.5,
        gamma_r_b=1.4,
        individual_negative_friction_range_nap={cpt.alias: (0.0, -5.0)},
        individual_positive_friction_range_nap={cpt.alias: (-5.0, "ptl")},
        width_base_small=0.25,
        width_shaft_large=0.3,
        width_shaft_small=0.25,
        height_base=0.5,
        settlement_curve=2,
        adhesion=0.01,
        alpha_p=0.01,
        alpha_s_clay=0.01,
        alpha_s_sand=0.01,
        beta_p=0.01,
        pile_tip_factor_s=0.01,
        elastic_modulus=0.01,
        is_auger=True,
        is_low_vibrating=True,
        negative_fr_delta_factor=0.01,
    )

    # Check the payload content

    # We don't completely check the soil_properties list here
    list_soil_properties = payload.pop("list_soil_properties")
    assert isinstance(list_soil_properties, list)
    assert len(list_soil_properties) == 1

    assert payload.pop("excavation_param_t") == 0.5
    assert payload.pop("pile_head_level_nap") == 5.0
    assert payload.pop("rel_pile_load") == 0.8
    assert payload.pop("friction_range_strategy") == "manual"
    assert np.isclose(payload.pop("gamma_f_nk"), 1.2)
    assert np.isclose(payload.pop("gamma_r_b"), 1.4)
    assert np.isclose(payload.pop("gamma_r_s"), 1.5)
    pile_properties = payload.pop("pile_properties")
    assert pile_properties.get("type") == "rect"
    pile_props = pile_properties.get("props")
    assert np.isclose(pile_props.pop("width_base_large"), 0.3)
    assert np.isclose(pile_props.pop("width_base_small"), 0.25)
    assert np.isclose(pile_props.pop("width_shaft_large"), 0.3)
    assert np.isclose(pile_props.pop("width_shaft_small"), 0.25)
    assert np.isclose(pile_props.pop("height_base"), 0.5)
    assert pile_props.pop("settlement_curve") == 2
    assert np.isclose(pile_props.pop("adhesion"), 0.01)
    assert np.isclose(pile_props.pop("alpha_p"), 0.01)
    assert np.isclose(pile_props.pop("alpha_s_clay"), 0.01)
    assert np.isclose(pile_props.pop("alpha_s_sand"), 0.01)
    assert np.isclose(pile_props.pop("beta_p"), 0.01)
    assert np.isclose(pile_props.pop("pile_tip_factor_s"), 0.01)
    assert np.isclose(pile_props.pop("elastic_modulus"), 0.01)
    assert pile_props.pop("is_auger") is True
    assert pile_props.pop("is_low_vibrating") is True
    assert np.isclose(pile_props.pop("negative_fr_delta_factor"), 0.01)

    # Check the pile-type-specification
    assert pile_props.pop("pile_type_specification") == dict(
        installation="A", pile_type="concrete", specification="1"
    )
    # Check that no extra keys are present in the pile_type_specification
    assert len(pile_props.keys()) == 0

    assert payload.pop("pile_tip_levels_nap") == [0, 1]
    assert np.isclose(payload.pop("soil_load"), 1.0)
    assert payload.pop("use_almere_rules") is False
    assert payload.pop("stiff_construction") is True

    # Check the optional payload keys
    assert payload.pop("cpts_group") == [cpt.alias]
    assert payload.pop("fixed_negative_friction_range_nap") == (0.0, 5.0)
    assert payload.pop("fixed_positive_friction_range_nap") == (5.0, "ptl")
    assert np.isclose(payload.pop("f_nk"), 0.0)
    assert payload.pop("apply_qc3_reduction") is True
    assert np.isclose(payload.pop("pile_load"), 0.0)
    assert np.isclose(payload.pop("excavation_depth_nap"), -2.0)

    # Check that no extra keys are present in the payload
    assert len(payload.keys()) == 0


def test_create_multi_cpt_payload_extended_ocr(
    cpt: CPTData, mock_classify_response: dict
) -> None:
    """
    Test creating the multi_cpt_results payload with the `create_multi_cpt_payload`
    function with extended OCR arguments.
    """

    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[0, 1],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: mock_classify_response},
        groundwater_level_nap=-2.5,
        pile_type="concrete",
        specification="1",
        installation="A",
        pile_shape="round",
        diameter_base=0.3,
        ocr=2.5,
    )

    # Check the payload content

    list_soil_properties = payload.get("list_soil_properties")
    assert isinstance(list_soil_properties, list)
    assert len(list_soil_properties) == 1
    assert "ocr" in list_soil_properties[0].keys()
    assert np.isclose(list_soil_properties[0]["ocr"], 2.5)

    # Case 2: set OCR with individual_ocr parameter

    payload, _ = create_multi_cpt_payload(
        pile_tip_levels_nap=[0, 1],
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: mock_classify_response},
        groundwater_level_nap=-2.5,
        pile_type="concrete",
        specification="1",
        installation="A",
        pile_shape="round",
        diameter_base=0.3,
        ocr=1.0,
        individual_ocr={cpt.alias: 2.0},
    )

    # Check the payload content

    list_soil_properties = payload.pop("list_soil_properties")
    assert isinstance(list_soil_properties, list)
    assert "ocr" in list_soil_properties[0].keys()
    assert np.isclose(list_soil_properties[0]["ocr"], 2.0)


def test_create_multi_cpt_payload_errors(
    cpt: CPTData, mock_classify_response: dict
) -> None:
    """
    Test creating the multi_cpt_results payload with the `create_multi_cpt_payload`
    with erroneous input.
    """

    with pytest.raises(ValueError):
        create_multi_cpt_payload(
            pile_tip_levels_nap=[0, 1],
            cptdata_objects=[cpt],
            classify_tables={cpt.alias: mock_classify_response},
            groundwater_level_nap=-2.5,
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="round",
        )

    with pytest.raises(ValueError):
        create_multi_cpt_payload(
            pile_tip_levels_nap=[0, 1],
            cptdata_objects=[cpt],
            classify_tables={cpt.alias: mock_classify_response},
            groundwater_level_nap=-2.5,
            pile_type="A",
            specification="concrete",
            installation="1",
            pile_shape="rect",
        )
