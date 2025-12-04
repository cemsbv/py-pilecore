import pytest
from ipywidgets import widgets

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTResultDefinition
from pypilecore.viewers.interactive_figures.figure_cpt_results_plan_view import (
    FigureCPTResultsPlanView,
)
from pypilecore.viewers.viewer_cpt_results_plan_view import ViewerCptResultsPlanView


def test_init_valid_input(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the initialization of the ViewerCptResultsPlanView with valid input.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    viewer = ViewerCptResultsPlanView(
        cases_multi_results=cases_multi_results,
    )

    assert isinstance(viewer._figure_plan_view, FigureCPTResultsPlanView)
    assert isinstance(viewer._case_dropdown, widgets.Dropdown)
    assert isinstance(viewer._result_dropdown, widgets.Dropdown)
    assert isinstance(viewer._control_widgets, widgets.HBox)
    assert isinstance(viewer._layout, widgets.VBox)


def test_init_invalid_input() -> None:
    """
    Tests the initialization of the VieweCptResultsPlanView with invalid input
    returns the expected errors.
    """
    with pytest.raises(TypeError, match="'cases_multi_results'"):
        ViewerCptResultsPlanView(cases_multi_results="invalid")


def test_update_case_result_and_ptl(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `_update_case_result_and_ptl` method of the VieweCptResultsPlanView
    is called and works correclty when the case and result dropdown
    values are changed.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    viewer = ViewerCptResultsPlanView(
        cases_multi_results=cases_multi_results,
    )

    # Test that the figure is updated when the case is changed
    # (a callback to the method _update_case_result_and_ptl is done)
    viewer._case_dropdown.value = "case_2"
    assert "case_2" in viewer._figure_plan_view.figure.layout.title.text
    assert (
        CPTResultDefinition.F_c_k.value.html
        in viewer._figure_plan_view.figure.layout.title.text
    )
    assert "-0.5" in viewer._figure_plan_view.figure.layout.title.text

    # Test that the figure is updated when the result is changed
    viewer._result_dropdown.value = "s_b"
    assert "case_2" in viewer._figure_plan_view.figure.layout.title.text
    assert (
        CPTResultDefinition.s_b.value.html
        in viewer._figure_plan_view.figure.layout.title.text
    )
    assert "-0.5" in viewer._figure_plan_view.figure.layout.title.text

    # Test that the figure is updated when the pile tip level is changed
    viewer._pile_tip_level_dropdown.value = 1.0
    assert "case_2" in viewer._figure_plan_view.figure.layout.title.text
    assert (
        CPTResultDefinition.s_b.value.html
        in viewer._figure_plan_view.figure.layout.title.text
    )
    assert "1.0" in viewer._figure_plan_view.figure.layout.title.text


def test_display(
    mock_cases_multi_cpt_bearing_results: CasesMultiCPTBearingResults,
) -> None:
    """
    Tests the `display` method of the VieweCptResultsPlanView.
    """
    cases_multi_results = mock_cases_multi_cpt_bearing_results

    viewer = ViewerCptResultsPlanView(
        cases_multi_results=cases_multi_results,
    )

    assert viewer.display() is None
