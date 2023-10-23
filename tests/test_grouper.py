import matplotlib.pyplot as plt
from pypilecore.results.grouper_result import GrouperResults


def test_grouper_results(mock_group_cpts_response):
    """
    Test parsing and plotting in GrouperResults object
    """

    # test parsing of response to dataclass
    result = GrouperResults.from_api_response(mock_group_cpts_response, pile_load_uls=1500)

    # test plotting
    plot = result.plot()
    assert isinstance(plot, plt.Figure)

    figure = result.map()
    assert isinstance(figure, plt.Figure)

    chart = result.clusters[0].plot()
    assert isinstance(chart, plt.Figure)
