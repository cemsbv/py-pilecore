import pytest
from ipywidgets import widgets

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTResultDefinition
from pypilecore.viewers.interactive_figures.figure_cpt_group_results_versus_ptls import (
    FigureCPTGroupResultsVersusPtls,
)
from pypilecore.viewers.viewer_cpt_group_results import ViewerCptGroupResults


def test_init_valid_input(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the initialization of the ViewerCptGroupResults with valid input.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    viewer = ViewerCptGroupResults(
        cases_multi_results=cases_multi_results,
    )

    assert isinstance(viewer._figure_plts, FigureCPTGroupResultsVersusPtls)
    assert isinstance(viewer._result_dropdown, widgets.Dropdown)
    assert isinstance(viewer._control_widgets, widgets.HBox)
    assert isinstance(viewer._layout, widgets.VBox)


def test_init_invalid_input() -> None:
    """
    Tests the initialization of the ViewerCptGroupResults with invalid input
    returns the expected errors.
    """
    with pytest.raises(TypeError, match="'cases_multi_results'"):
        ViewerCptGroupResults(cases_multi_results="invalid")


def test_update_result(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `_update_result` method of the ViewerCptGroupResults
    is called and works correclty when the case and result dropdown
    values are changed.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    viewer = ViewerCptGroupResults(
        cases_multi_results=cases_multi_results,
    )

    # Test that the figure is updated when the result is changed
    viewer._result_dropdown.value = "s_b"
    assert (
        CPTResultDefinition.s_b.value.html
        in viewer._figure_plts.figure.layout.title.text
    )


def test_display(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `display` method of the ViewerCptGroupResults.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    viewer = ViewerCptGroupResults(
        cases_multi_results=cases_multi_results,
    )

    assert viewer.display() is None
