import plotly.graph_objects as go
import pytest

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTResultDefinition
from pypilecore.viewers.interactive_figures.figure_cpt_results_plan_view import (
    FigureCPTResultsPlanView,
)


def test_init_valid_input(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the initialization of the FigureCPTResultsPlanView with valid input.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTResultsPlanView(
        results_cases=cases_multi_results,
    )

    assert figure.results == cases_multi_results
    assert figure.data.equals(cases_multi_results.cpt_results_table.to_pandas())
    assert figure.cases == cases_multi_results.cases
    assert figure.test_ids == cases_multi_results.test_ids
    assert figure.pile_tip_levels_nap == cases_multi_results.pile_tip_levels_nap
    assert isinstance(figure.figure, go.FigureWidget)


def test_init_invalid_input() -> None:
    """
    Tests the initialization of the FigureCPTResultsPlanView with invalid input
    returns the expected errors.
    """
    with pytest.raises(TypeError, match="'cases_multi_results'"):
        FigureCPTResultsPlanView(results_cases="invalid")


def test_get_visible_test_ids(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `_get_visible_test_ids` method of the FigureCPTResultsPlanView.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTResultsPlanView(
        results_cases=cases_multi_results,
    )

    # Test that initially no test_ids are visible
    assert len(figure.get_visible_test_ids()) == 0

    # Test that after showing a case and result, all the test_ids are visible
    figure.show_case_result_and_ptl(
        case_name="case_1", result_name="R_c_d_net", pile_tip_level_nap=0.0
    )
    assert figure.get_visible_test_ids() == cases_multi_results.test_ids + [
        "__colorbar__"
    ]


def test_show_case_and_result(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `show_case_and_result` method of the FigureCPTResultsPlanView.
    """

    cases_multi_results = mock_cases_multi_cpt_bearing_results

    figure = FigureCPTResultsPlanView(
        results_cases=cases_multi_results,
    )

    # Invalid case
    with pytest.raises(ValueError, match="Case"):
        figure.show_case_result_and_ptl(
            case_name="invalid", result_name="R_c_d_net", pile_tip_level_nap=0.0
        )

    # Invalid result name
    with pytest.raises(ValueError, match="Result"):
        figure.show_case_result_and_ptl(
            case_name="case_1", result_name="invalid", pile_tip_level_nap=0.0
        )

    # Invalid pile tip level
    with pytest.raises(TypeError, match="'pile_tip_level_nap'"):
        figure.show_case_result_and_ptl(
            case_name="case_1",
            result_name="R_c_d_net",
            pile_tip_level_nap="not a float",
        )

    with pytest.raises(ValueError, match="Pile tip level"):
        figure.show_case_result_and_ptl(
            case_name="case_1", result_name="R_c_d_net", pile_tip_level_nap=100.0
        )

    # Valid cases, results and pile tip levels
    figure.show_case_result_and_ptl(
        case_name="case_2", result_name="R_c_d_net", pile_tip_level_nap=0.0
    )
    assert "case_2" in figure.figure.layout.title.text
    assert CPTResultDefinition.R_c_d_net.value.html in figure.figure.layout.title.text
    assert "0.0" in figure.figure.layout.title.text

    figure.show_case_result_and_ptl(
        case_name="case_1", result_name="s_b", pile_tip_level_nap=1.0
    )
    assert "case_1" in figure.figure.layout.title.text
    assert CPTResultDefinition.s_b.value.html in figure.figure.layout.title.text
    assert "1.0" in figure.figure.layout.title.text
