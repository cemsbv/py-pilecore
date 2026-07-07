import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from pygef.common import Location

from pypilecore.results import GrouperResults, MultiCPTCompressionBearingResults
from pypilecore.results.cases_grouper_results import CasesGrouperResults
from pypilecore.results.soil_properties import SoilProperties


def test_grouper_results(
    mock_group_cpts_response: dict,
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
) -> None:
    """
    Test parsing and plotting in GrouperResults object
    """

    multi_cpt_bearing_results = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_group_multi_cpt_bearing_response,
        cpt_input=mock_group_results_passover,
    )

    # test parsing of response to dataclass
    grouper_results = GrouperResults.from_api_response(
        mock_group_cpts_response,
        pile_load_uls=100,
        multi_cpt_bearing_results=multi_cpt_bearing_results,
    )

    # test plotting
    plot = grouper_results.plot()
    assert isinstance(plot, plt.Figure)
    plt.close("all")

    figure = grouper_results.map()
    assert isinstance(figure, plt.Figure)
    plt.close("all")

    chart = grouper_results.clusters[0].plot()
    assert isinstance(chart, plt.Figure)
    plt.close("all")

    result = grouper_results.cpt_results
    scene = result.plot()
    assert isinstance(scene, plt.Figure)
    plt.close("all")

    with pytest.raises(ValueError):
        result.map(pile_tip_level_nap=0)
    _map = result.map(pile_tip_level_nap=-15)
    assert isinstance(_map, plt.Figure)
    plt.close("all")


def test_grouper_results_max_bearing(
    mock_group_cpts_response_3: dict,
    mock_multi_cpt_bearing_response_3,
    mock_results_passover_3,
) -> None:
    mcb = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_multi_cpt_bearing_response_3,
        cpt_input=mock_results_passover_3,
    )

    gr = GrouperResults.from_api_response(
        response_dict=mock_group_cpts_response_3,
        pile_load_uls=700,
        multi_cpt_bearing_results=mcb,
    )

    # Get the max bearing results
    mbr = gr.cpt_results

    # Check that the results per cpt can be fetched for correct column names
    for colname in ["R_c_d_net", "F_nk_d", "origin"]:
        assert isinstance(mbr.get_results_per_cpt(colname), pd.DataFrame)

    # Check that the results per cpt cannot be fetched for incorrect column names
    for colname in ["pile_tip_level_nap", "test_id", "something_else"]:
        with pytest.raises(ValueError):
            mbr.get_results_per_cpt(colname)

    mbr_pd = mbr.to_pandas()
    assert isinstance(mbr_pd, pd.DataFrame)
    assert mbr_pd.columns.to_list() == [
        "pile_tip_level_nap",
        "R_c_d_net",
        "F_nk_d",
        "origin",
        "test_id",
        "x",
        "y",
    ]

    for idx, test_id in enumerate(mbr.test_ids):
        # Make sure that the multiple ways of fetching a result return the same object
        assert mbr[test_id] == mbr.get_cpt_results(test_id)
        assert mbr[test_id] == mbr.results[idx]
        assert mbr.cpt_results_dict[test_id] == mbr.get_cpt_results(test_id)

        mbr1 = mbr.get_cpt_results(test_id)

        assert isinstance(mbr1.soil_properties, SoilProperties)
        assert mbr1.soil_properties.test_id == test_id

        assert isinstance(mbr1.plot_bearing_capacities(), plt.Axes)
        assert isinstance(mbr1.plot_bearing_overview(), plt.Figure)

        plt.close("all")

        for colname in ["pile_tip_level_nap", "R_c_d_net", "F_nk_d", "origin"]:
            assert isinstance(mbr1.table.__getattribute__(colname), np.ndarray)

    # Check that only the last R_c_d_net values of CPT 24 are NaN
    assert np.isnan(mbr["24"].table.R_c_d_net[10:]).all()
    assert ~np.isnan(mbr["24"].table.R_c_d_net[:10]).any()


def test_grouper_results_bearing_results_field_and_deprecated_accessor(
    mock_group_cpts_response: dict,
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
) -> None:
    """
    `bearing_results` is the source of truth; the deprecated `multi_cpt_bearing_results`
    accessor still returns the PileCore object and emits a DeprecationWarning.
    """
    mcb = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_group_multi_cpt_bearing_response,
        cpt_input=mock_group_results_passover,
    )
    grouper_results = GrouperResults.from_api_response(
        mock_group_cpts_response,
        pile_load_uls=100,
        multi_cpt_bearing_results=mcb,
    )

    assert grouper_results.bearing_results is mcb

    with pytest.warns(DeprecationWarning):
        assert grouper_results.multi_cpt_bearing_results is mcb


def test_grouper_results_from_grouper_response_matches_from_api_response(
    mock_group_cpts_response: dict,
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
) -> None:
    """`from_api_response` delegates to `from_grouper_response`: same folded results."""
    mcb = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_group_multi_cpt_bearing_response,
        cpt_input=mock_group_results_passover,
    )
    gr_legacy = GrouperResults.from_api_response(
        mock_group_cpts_response,
        pile_load_uls=100,
        multi_cpt_bearing_results=mcb,
    )
    gr_general = GrouperResults.from_grouper_response(
        mock_group_cpts_response,
        pile_load_uls=100,
        bearing_results=mcb,
    )

    assert gr_general.cpt_results.test_ids == gr_legacy.cpt_results.test_ids
    for test_id in gr_legacy.cpt_results.test_ids:
        np.testing.assert_allclose(
            gr_general.cpt_results[test_id].table.R_c_d_net,
            gr_legacy.cpt_results[test_id].table.R_c_d_net,
            equal_nan=True,
        )
        np.testing.assert_array_equal(
            gr_general.cpt_results[test_id].table.origin,
            gr_legacy.cpt_results[test_id].table.origin,
        )


def test_cases_grouper_results_pilecore_path(
    mock_group_cpts_response: dict,
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
) -> None:
    """CasesGrouperResults rides the source-agnostic protocol on the PileCore path."""
    mcb = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_group_multi_cpt_bearing_response,
        cpt_input=mock_group_results_passover,
    )
    grouper_results = GrouperResults.from_api_response(
        mock_group_cpts_response,
        pile_load_uls=100,
        multi_cpt_bearing_results=mcb,
    )
    cpt_locations = {
        test_id: Location(srs_name="RD", **info["location"])
        for test_id, info in mock_group_results_passover.items()
    }

    cases = CasesGrouperResults(
        results_per_case={"case_1": grouper_results, "case_2": grouper_results},
        cpt_locations=cpt_locations,
    )

    assert cases.cases == ["case_1", "case_2"]
    assert set(cases.test_ids) == set(mcb.cpt_names)
    assert len(cases.pile_tip_levels_nap) > 0
    assert isinstance(cases.cpt_results_table.to_pandas(), pd.DataFrame)


def test_grouper_triangulation(
    mock_group_cpts_response_3: dict,
    mock_multi_cpt_bearing_response_3,
    mock_results_passover_3,
) -> None:
    mcb = MultiCPTCompressionBearingResults.from_api_response(
        response_dict=mock_multi_cpt_bearing_response_3,
        cpt_input=mock_results_passover_3,
    )

    gr = GrouperResults.from_api_response(
        response_dict=mock_group_cpts_response_3,
        pile_load_uls=700,
        multi_cpt_bearing_results=mcb,
    )

    # Get the max bearing results
    mbr = gr.cpt_results

    # alter dict
    _data = {}
    xx = [0, 0, 1, 1]
    yy = [0, 1.1, 0, 1]
    for key, value, x, y in zip(mbr.test_ids[:4], mbr.results[:4], xx, yy):
        value.soil_properties._x = x
        value.soil_properties._y = y
        _data[key] = value
    mbr._cpt_results_dict = _data

    # test tessellation
    assert mbr.triangulation(-18) == [
        {
            "geometry": [[1.0, 0.0], [1.0, 1.0], [0.0, 0.0]],
            "test_id": ["17", "12", "33"],
        },
        {
            "geometry": [[1.0, 1.0], [0.0, 1.1], [0.0, 0.0]],
            "test_id": ["12", "24", "33"],
        },
    ]
