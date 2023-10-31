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
def mock_classify_response() -> dict:
    with open("tests/response/classify_response.json", "r") as file:
        data = json.load(file)
    return data


@pytest.fixture
def cpt() -> CPTData:
    return pygef.read_cpt("tests/data/cpt.gef")
