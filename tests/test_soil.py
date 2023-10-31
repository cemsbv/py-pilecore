from pygef.cpt import CPTData

from pypilecore.input import create_soil_properties_payload


def test_soil_properties(cpt: CPTData, mock_classify_response: dict) -> None:
    """
    Test parsing and plotting in GrouperResults object
    """

    # test parsing of response to dataclass
    payload, passover = create_soil_properties_payload(
        cptdata_objects=[cpt],
        classify_tables={cpt.alias: mock_classify_response},
        groundwater_level_nap=-2.5,
        friction_range_strategy="manual",
    )

    assert isinstance(payload, list)
    assert isinstance(passover, dict)
