from __future__ import annotations  # noqa: F404

from typing import Any

from IPython.display import DisplayHandle, display
from ipywidgets import widgets
from natsort import natsorted

from pypilecore.results.cases_grouper_results import CasesGrouperResults
from pypilecore.viewers.interactive_figures.figure_cpt_results_plan_view import (
    FigureCPTResultsPlanView,
)


class ViewerGroupResultsPlanView:
    """
    Viewer for the Grouper results in plan view for a fixed pile tip level (PTL).

    It offers the following layout:
        - Dropdown widgets:
            - Case: to select the case to show.
            - Result: to select the result to show.
            - Pile tip level: to select the pile tip level to show.
        - Figure Grouper results vs. pile tip level:
            - X axis: X coordinate.
            - Y axis: Y coordinate.
            - Each point represents a different cluster, but the same pile tip level.
    """

    def __init__(self, cases_grouper_results: CasesGrouperResults) -> None:
        """Initialize the viewer.

        Parameters
        ----------
        cases_grouper_results : CasesGrouperResults
            The results of the grouper calculations.

        Raises
        ------
        TypeError
            If 'cases_grouper_results' are not of type 'CasesGrouperResults'.
        """
        self._figure_plan_view = FigureCPTResultsPlanView(
            cases_multi_results=cases_grouper_results
        )

        self._case_dropdown = widgets.Dropdown(
            description="Case:",
            value=self._figure_plan_view.cases[0],
            options=self._figure_plan_view.cases,
        )
        # Create a sorted list of unique result names
        result_options = natsorted(
            set(
                [
                    result_def.name
                    for result_def in cases_grouper_results.cpt_results_table.result_def
                ]
            )
        )
        self._result_dropdown = widgets.Dropdown(
            description="Result:",
            value=result_options[0],
            options=result_options,
        )
        self._pile_tip_level_dropdown = widgets.Dropdown(
            description="Pile tip level NAP:",
            value=self._figure_plan_view.pile_tip_levels_nap[-1],
            options=self._figure_plan_view.pile_tip_levels_nap,
        )

        self._update_case_result_and_ptl(None)

        self._case_dropdown.observe(self._update_case_result_and_ptl, "value")
        self._result_dropdown.observe(self._update_case_result_and_ptl, "value")
        self._pile_tip_level_dropdown.observe(self._update_case_result_and_ptl, "value")

        self._control_widgets = widgets.HBox(
            [
                self._case_dropdown,
                self._result_dropdown,
                self._pile_tip_level_dropdown,
            ]
        )
        self._layout = widgets.VBox(
            [self._control_widgets, self._figure_plan_view.figure]
        )

    def _update_case_result_and_ptl(self, change: Any) -> None:
        """Update the figure when the controls change."""
        self._figure_plan_view.show_case_result_and_ptl(
            case_name=self._case_dropdown.value,
            result_name=self._result_dropdown.value,
            pile_tip_level_nap=self._pile_tip_level_dropdown.value,
        )

    def display(self) -> DisplayHandle | None:
        """Display the figure."""
        return display(self._layout)
