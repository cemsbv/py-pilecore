import plotly.graph_objects as go
import pytest

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTResultDefinition
from pypilecore.viewers.interactive_figures.figure_cpt_group_results_versus_ptls import (
    FigureCPTGroupResultsVersusPtls,
)


def test_init_valid_input(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the initialization of the FigureCPTGroupResultsVersusPtls with valid input.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTGroupResultsVersusPtls(
        cases_multi_results=cases_multi_results,
    )

    assert figure.results == cases_multi_results
    assert figure.data.equals(cases_multi_results.cpt_group_results_dataframe)
    assert figure.cases == cases_multi_results.cases

    assert isinstance(figure.figure, go.FigureWidget)


def test_init_invalid_input() -> None:
    """
    Tests the initialization of the FigureCPTGroupResultsVersusPtls with invalid input
    returns the expected errors.
    """
    with pytest.raises(TypeError, match="'cases_multi_results'"):
        FigureCPTGroupResultsVersusPtls(cases_multi_results="invalid")


def test_get_visible_cases(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `_get_visible_cases` method of the FigureCPTGroupResultsVersusPtls.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTGroupResultsVersusPtls(
        cases_multi_results=cases_multi_results,
    )

    # Test that initially, all the cases are returned
    assert figure.get_visible_cases() == cases_multi_results.cases

    # Test that after showing a result, all the cases are visible
    figure.show_result(result_name="R_c_d_net")
    assert figure.get_visible_cases() == cases_multi_results.cases


def test_show_result(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `show_result` method of the FigureCPTGroupResultsVersusPtls.
    """

    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTGroupResultsVersusPtls(
        cases_multi_results=cases_multi_results,
    )

    # Invalid result name
    with pytest.raises(ValueError, match="Result"):
        figure.show_result(result_name="invalid")

    # Valid result name
    figure.show_result(result_name="s_b")
    assert CPTResultDefinition.s_b.value.html in figure.figure.layout.title.text
