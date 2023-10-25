import json

import pytest


@pytest.fixture
def mock_group_cpts_response() -> dict:
    with open("tests/response/group_cpts_response.json", "r") as file:
        data = json.load(file)
    return data
