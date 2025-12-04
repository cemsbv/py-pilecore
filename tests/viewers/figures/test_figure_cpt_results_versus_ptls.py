import plotly.graph_objects as go
import pytest

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTResultDefinition
from pypilecore.viewers.interactive_figures.figure_cpt_results_versus_ptls import (
    FigureCPTResultsVersusPtls,
)


def test_init_valid_input(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the initialization of the FigureCPTResultsVersusPtls with valid input.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTResultsVersusPtls(
        cases_multi_results=cases_multi_results,
    )

    assert figure.results == cases_multi_results
    assert figure.data.equals(cases_multi_results.cpt_results_table.to_pandas())
    assert figure.cases == cases_multi_results.cases
    assert figure.test_ids == cases_multi_results.test_ids
    assert isinstance(figure.figure, go.FigureWidget)


def test_init_invalid_input() -> None:
    """
    Tests the initialization of the FigureCPTResultsVersusPtls with invalid input
    returns the expected errors.
    """
    with pytest.raises(TypeError, match="'cases_multi_results'"):
        FigureCPTResultsVersusPtls(cases_multi_results="invalid")


def test_get_visible_test_ids(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `_get_visible_test_ids` method of the FigureCPTResultsVersusPtls.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTResultsVersusPtls(
        cases_multi_results=cases_multi_results,
    )

    # Test that initially no test_ids are visible
    assert len(figure.get_visible_test_ids()) == 0

    # Test that after showing a case and result, all the test_ids are visible
    figure.show_case_and_result(case_name="case_1", result_name="R_c_d_net")
    assert figure.get_visible_test_ids() == cases_multi_results.test_ids


def test_show_case_and_result(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `show_case_and_result` method of the FigureCPTResultsVersusPtls.
    """

    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTResultsVersusPtls(
        cases_multi_results=cases_multi_results,
    )

    # Invalid case
    with pytest.raises(ValueError, match="Case"):
        figure.show_case_and_result(case_name="invalid", result_name="R_c_d_net")

    # Invalid result name
    with pytest.raises(ValueError, match="Result"):
        figure.show_case_and_result(case_name="case_1", result_name="invalid")

    # Valid cases and results
    figure.show_case_and_result(case_name="case_2", result_name="R_c_d_net")
    assert "case_2" in figure.figure.layout.title.text
    assert CPTResultDefinition.R_c_d_net.value.html in figure.figure.layout.title.text

    figure.show_case_and_result(case_name="case_1", result_name="s_b")
    assert "case_1" in figure.figure.layout.title.text
    assert CPTResultDefinition.s_b.value.html in figure.figure.layout.title.text
