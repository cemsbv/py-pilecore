import matplotlib.pyplot as plt

from pypilecore.results import GrouperResults, MultiCPTBearingResults


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
