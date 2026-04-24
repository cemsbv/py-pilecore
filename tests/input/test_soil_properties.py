"""
Tests for create_soil_properties_payload friction range payload construction.

Covers the correct construction of per-CPT friction_settings under all combinations
of global (master) and per-CPT (individual) friction range inputs.
"""

from __future__ import annotations

import pygef
import pytest
from pygef.cpt import CPTData

from pypilecore.input.soil_properties import create_soil_properties_payload

CPT_ALIAS = "S-TUN-016-PG"

CLASSIFY_TABLE = {
    CPT_ALIAS: {
        "geotechnicalSoilName": ["Sand"],
        "lowerBoundary": [1.0],
        "upperBoundary": [0.0],
        "color": ["#000000"],
        "mainComponent": ["sand"],
        "cohesion": [0.0],
        "gamma_sat": [20],
        "gamma_unsat": [18],
        "phi": [30],
        "undrainedShearStrength": [0.0],
    }
}


@pytest.fixture
def cpt() -> CPTData:
    return pygef.read_cpt("tests/data/cpt.gef")


def _get_friction_settings(soil_properties_list: list, alias: str) -> dict | None:
    for sp in soil_properties_list:
        if sp.get("test_id") == alias:
            return sp.get("friction_settings")
    return None


class TestNoIndividualOverrides:
    """When no individual overrides are given, no per-CPT friction_settings is created."""

    def test_lower_bound_no_overrides(self, cpt):
        result, _ = create_soil_properties_payload(
            cptdata_objects=[cpt],
            classify_tables=CLASSIFY_TABLE,
            groundwater_level_nap=-1.0,
            friction_range_strategy="lower_bound",
        )
        assert _get_friction_settings(result, CPT_ALIAS) is None

    def test_manual_no_overrides(self, cpt):
        result, _ = create_soil_properties_payload(
            cptdata_objects=[cpt],
            classify_tables=CLASSIFY_TABLE,
            groundwater_level_nap=-1.0,
            friction_range_strategy="manual",
            master_negative_shaft_friction=50.0,
        )
        # No individual range overrides → no per-CPT friction_settings
        assert _get_friction_settings(result, CPT_ALIAS) is None


class TestIndividualPositiveFrictionRange:
    """individual_positive_friction_range_nap triggers per-CPT friction_settings."""

    def test_positive_range_only_no_master_negative(self, cpt):
        """Without master_negative_shaft_friction, negative_friction is absent."""
        result, _ = create_soil_properties_payload(
            cptdata_objects=[cpt],
            classify_tables=CLASSIFY_TABLE,
            groundwater_level_nap=-1.0,
            friction_range_strategy="lower_bound",
            individual_positive_friction_range_nap={CPT_ALIAS: (-5.0, "ptl")},
        )
        fs = _get_friction_settings(result, CPT_ALIAS)
        assert fs is not None
        assert fs["friction_range_strategy"] == "manual"
        assert fs["positive_friction_range_nap"] == (-5.0, "ptl")
        assert "negative_friction" not in fs
        assert "negative_friction_range_nap" not in fs

    def test_positive_range_with_master_negative_shaft_friction(self, cpt):
        """master_negative_shaft_friction is included in per-CPT payload (the bug fix)."""
        result, _ = create_soil_properties_payload(
            cptdata_objects=[cpt],
            classify_tables=CLASSIFY_TABLE,
            groundwater_level_nap=-1.0,
            friction_range_strategy="manual",
            master_negative_shaft_friction=30.0,
            individual_positive_friction_range_nap={CPT_ALIAS: (-5.0, "ptl")},
        )
        fs = _get_friction_settings(result, CPT_ALIAS)
        assert fs is not None
