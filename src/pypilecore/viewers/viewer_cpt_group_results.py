from __future__ import annotations  # noqa: F404

from typing import Any

from IPython.display import DisplayHandle, display
from ipywidgets import widgets
from natsort import natsorted

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.viewers.interactive_figures import FigureCPTGroupResultsVersusPtls


class ViewerCptGroupResults:
    """
    Viewer for the CPT group results of the bearing capacity calculations.

    It offers the following layout:
        - Dropdown widgets:
            - Result: to select the result to show.
        - Figure CPT group results vs. pile tip level:
            - X axis: result values
            - Y axis: pile tip level w.r.t. NAP
            - Each trace represents a different case.
    """

    def __init__(self, cases_multi_results: CasesMultiCPTBearingResults) -> None:
        """Initialize the viewer.

        Parameters
        ----------
        cases_multi_results : CasesMultiCPTBearingResults
            The results of the bearing capacity calculations.

        Raises
        ------
        TypeError
            If 'cases_multi_results' are not of type 'CasesMultiCPTBearingResults'.
        """
        # Initialize figure CPT group resuls vs. pile tip level
        self._figure_plts = FigureCPTGroupResultsVersusPtls(
            cases_multi_results=cases_multi_results
        )

        # Set up control widgets

        # Create a sorted list of unique result names
        result_options = natsorted(
            set(
                [
                    result_def.name
                    for result_def in cases_multi_results.cpt_results_table.result_def
                ]
            )
        )
        self._result_dropdown = widgets.Dropdown(
            description="Result:",
            value=result_options[0],
            options=result_options,
        )

        # Update plot for initial selection of control widgets
        self._update_result(None)

        # Set up callbacks
        self._result_dropdown.observe(self._update_result, "value")

        # Set up layout
        self._control_widgets = widgets.HBox(
            [
                self._result_dropdown,
            ]
        )
        self._layout = widgets.VBox([self._control_widgets, self._figure_plts.figure])

    def _update_result(self, change: Any) -> None:
        """Private method to update the figure when the result name is changed in the result dropdown."""

        # Update the figure
        self._figure_plts.show_result(
            result_name=self._result_dropdown.value,
        )

    def display(self) -> DisplayHandle | None:
        """Display the figure."""
        return display(self._layout)
