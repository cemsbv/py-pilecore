import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from pypilecore.results import GrouperResults, MultiCPTBearingResults
from pypilecore.results.soil_properties import SoilProperties


def test_grouper_results(
    mock_group_cpts_response: dict,
    mock_group_multi_cpt_bearing_response: dict,
    mock_group_results_passover: dict,
) -> None:
    """
    Test parsing and plotting in GrouperResults object
    """

    multi_cpt_bearing_results = MultiCPTBearingResults.from_api_response(
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

    figure = grouper_results.map()
    assert isinstance(figure, plt.Figure)

    chart = grouper_results.clusters[0].plot()
    assert isinstance(chart, plt.Figure)

    result = grouper_results.max_bearing_results
    scene = result.plot()
    assert isinstance(scene, plt.Figure)


def test_grouper_results_max_bearing(
    mock_group_cpts_response_3: dict,
    mock_multi_cpt_bearing_response_3,
    mock_results_passover_3,
) -> None:
    mcb = MultiCPTBearingResults.from_api_response(
        response_dict=mock_multi_cpt_bearing_response_3,
        cpt_input=mock_results_passover_3,
    )

    gr = GrouperResults.from_api_response(
        response_dict=mock_group_cpts_response_3,
        pile_load_uls=700,
        multi_cpt_bearing_results=mcb,
    )

    # Get the max bearing results
    mbr = gr.max_bearing_results

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

        for colname in ["pile_tip_level_nap", "R_c_d_net", "F_nk_d", "origin"]:
            assert isinstance(mbr1.table.__getattribute__(colname), np.ndarray)

    # Check that only the last R_c_d_net values of CPT 24 are NaN
    assert np.isnan(mbr["24"].table.R_c_d_net[10:]).all()
    assert ~np.isnan(mbr["24"].table.R_c_d_net[:10]).any()
