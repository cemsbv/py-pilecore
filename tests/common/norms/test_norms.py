import pytest

from pypilecore.common import norms as norms


def test_nen99971_defaults():
	norm = norms.Nen99971()
	# default version should be V2025
	assert norm.version == norms.NEN99971_version.V2025 == "2025"
	# string representation should include the version value
	assert str(norm) == "NEN9997-1 (2025)"


def test_cur236_defaults():
	norm = norms.Cur236()
	assert norm.version == norms.CUR236_version.V2024 == "2024"
	assert str(norm) == "CUR236 (2024)"


def test_norms_serialize_defaults():
	norm = norms.Norms()
	payload = norm.serialize_payload()

	# payload should contain the enum members for the versions
	assert "NEN99971_version" in payload
	assert "CUR236_version" in payload
	assert payload["NEN99971_version"] == norms.NEN99971_version.V2025 == "2025"
	assert payload["CUR236_version"] == norms.CUR236_version.V2024 == "2024"

def test_norms_accept_custom_versions():
	norm = norms.Norms(
		nen_9997_1=norms.NEN99971_version.V2017,
		cur_236=norms.CUR236_version.V2024,
	)
	payload = norm.serialize_payload()
	assert payload["NEN99971_version"] == norms.NEN99971_version.V2017 == "2017"
	assert payload["CUR236_version"] == norms.CUR236_version.V2024 == "2024"

def test_norms_invalid_inputs():
	# Passing invalid values (years not defined in the enums) to Norms should raise ValueError
	with pytest.raises(ValueError):
		norms.Norms(nen_9997_1="2001")

	with pytest.raises(ValueError):
		norms.Norms(cur_236="1998")
