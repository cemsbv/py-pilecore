import json

import pygef
import pytest
from pygef.cpt import CPTData


@pytest.fixture
def mock_group_cpts_response() -> dict:
    with open("tests/response/group_cpts_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def mock_multi_cpt_bearing_response() -> dict:
    with open("tests/response/multi_cpt_bearing_response.json", "r") as file:
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
    }


@pytest.fixture
def mock_classify_response() -> dict:
    with open("tests/response/classify_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def cpt() -> CPTData:
    return pygef.read_cpt("tests/data/cpt.gef")
