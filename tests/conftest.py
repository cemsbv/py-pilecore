import json

import pygef
import pytest
from openapi_core import Config, OpenAPI, V30RequestValidator
from pygef.common import Location
from pygef.cpt import CPTData

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.compression.multi_cpt_results import (
    MultiCPTCompressionBearingResults,
)


@pytest.fixture
def mock_group_cpts_response() -> dict:
    with open("tests/response/group_cpts_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_group_multi_cpt_bearing_response() -> dict:
    with open("tests/response/group_multi_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_group_results_passover() -> dict:
    with open("tests/response/group_passover_dump.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_multi_cpt_tension_response() -> dict:
    with open("tests/response/multi_cpt_tension_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_multi_cpt_bearing_response() -> dict:
    with open("tests/response/multi_cpt_bearing_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_multi_cpt_bearing_response_less_cpts() -> dict:
    with open("tests/response/multi_cpt_bearing_response_less_cpts.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_multi_cpt_bearing_response_less_pile_tip_levels() -> dict:
    with open(
        "tests/response/multi_cpt_bearing_response_less_pile_tip_levels.json", "r"
    ) as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_results_passover() -> dict:
    return {
        "9": {
            "ref_height": 11.41,
            "surface_level_nap": 11.41,
            "location": {"x": 0, "y": 0},
        },
        "7": {
            "ref_height": 10.98,
            "surface_level_nap": 10.98,
            "location": {"x": 2, "y": 1},
        },
        "5": {
            "ref_height": 10.96,
            "surface_level_nap": 10.96,
            "location": {"x": 2, "y": 2},
        },
        "12": {
            "ref_height": 11.56,
            "surface_level_nap": 11.56,
            "location": {"x": 3, "y": 3},
        },
        "17A": {
            "ref_height": 11.44,
            "surface_level_nap": 11.44,
            "location": {"x": 4, "y": 4},
        },
    }


@pytest.fixture
def mock_group_cpts_response_3() -> dict:
    with open("tests/response/group_cpts_response_3.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_multi_cpt_bearing_response_2() -> dict:
    with open("tests/response/multi_cpt_bearing_response_2.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_multi_cpt_bearing_response_3() -> dict:
    with open("tests/response/multi_cpt_bearing_response_3.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_results_passover_2() -> dict:
    with open("tests/response/results_passover_dump.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_results_passover_3() -> dict:
    with open("tests/response/results_passover_dump_3.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_classify_response() -> dict:
    with open("tests/response/classify_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def cpt() -> CPTData:
    return pygef.read_cpt("tests/data/cpt.gef")


@pytest.fixture
def cpt_no_coords() -> CPTData:
    return pygef.read_cpt("tests/data/cpt_no_coordinates.GEF")


@pytest.fixture
def mock_cases_multi_cpt_bearing_results_valid_data(
    mock_multi_cpt_bearing_response: dict, mock_results_passover: dict
) -> dict:
    cptgroupresults = MultiCPTCompressionBearingResults.from_api_response(
        mock_multi_cpt_bearing_response, mock_results_passover
    )

    cpt_locations = {
        cpt_id: Location(srs_name="RD", **cpt["location"])
        for cpt_id, cpt in mock_results_passover.items()
    }

    results_per_case = {
        "case_1": cptgroupresults,
        "case_2": cptgroupresults,
    }

    return {
        "results_per_case": results_per_case,
        "cpt_locations": cpt_locations,
    }


@pytest.fixture
def mock_cases_multi_cpt_bearing_results_different_cpts(
    mock_multi_cpt_bearing_response: dict,
    mock_multi_cpt_bearing_response_less_cpts: dict,
    mock_results_passover: dict,
) -> dict:
    cptgroupresults = MultiCPTCompressionBearingResults.from_api_response(
        mock_multi_cpt_bearing_response, mock_results_passover
    )

    cptgroupresults_less_cpts = MultiCPTCompressionBearingResults.from_api_response(
        mock_multi_cpt_bearing_response_less_cpts, mock_results_passover
    )

    cpt_locations = {
        cpt_id: Location(srs_name="RD", **cpt["location"])
        for cpt_id, cpt in mock_results_passover.items()
    }

    results_per_case = {
        "case_1": cptgroupresults,
        "case_2": cptgroupresults_less_cpts,
    }

    return {
        "results_per_case": results_per_case,
        "cpt_locations": cpt_locations,
    }


@pytest.fixture
def mock_cases_multi_cpt_bearing_results_different_pile_tip_levels(
    mock_multi_cpt_bearing_response: dict,
    mock_multi_cpt_bearing_response_less_pile_tip_levels: dict,
    mock_results_passover: dict,
) -> dict:
    cptgroupresults = MultiCPTCompressionBearingResults.from_api_response(
        mock_multi_cpt_bearing_response, mock_results_passover
    )

    cptgroupresults_less_pile_tip_levels = (
        MultiCPTCompressionBearingResults.from_api_response(
            mock_multi_cpt_bearing_response_less_pile_tip_levels, mock_results_passover
        )
    )

    cpt_locations = {
        cpt_id: Location(srs_name="RD", **cpt["location"])
        for cpt_id, cpt in mock_results_passover.items()
    }

    results_per_case = {
        "case_1": cptgroupresults,
        "case_2": cptgroupresults_less_pile_tip_levels,
    }

    return {
        "results_per_case": results_per_case,
        "cpt_locations": cpt_locations,
    }


@pytest.fixture
def mock_cases_multi_cpt_bearing_results(
    mock_cases_multi_cpt_bearing_results_valid_data: dict,
) -> CasesMultiCPTBearingResults:
    return CasesMultiCPTBearingResults(
        **mock_cases_multi_cpt_bearing_results_valid_data
    )


@pytest.fixture
def pc_openapi() -> OpenAPI:
    return OpenAPI.from_file_path(
        "tests/openapi/openapi.yaml",
        config=Config(
            spec_validator_cls=None,
            request_validator_cls=V30RequestValidator,
        ),
    )
