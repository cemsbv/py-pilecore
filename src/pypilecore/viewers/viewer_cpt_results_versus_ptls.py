from __future__ import annotations  # noqa: F404

from typing import Any

from IPython.display import DisplayHandle, display
from ipywidgets import widgets
from natsort import natsorted

from pypilecore.results.typing import CasesMultiCPTResultsLike
from pypilecore.viewers.interactive_figures import FigureCPTResultsVersusPtls


class ViewerCptResults:
    """
    Viewer for the CPT results of the bearing capacity calculations.

    It offers the following layout:
        - Dropdown widgets:
            - Case: to select the case to show.
            - Result: to select the result to show.
        - Figure CPT results vs. pile tip level:
            - X axis: result values
            - Y axis: pile tip level w.r.t. NAP
            - Each trace represents a different CPT.
    """

    def __init__(self, results_cases: CasesMultiCPTResultsLike) -> None:
        """Initialize the viewer.

        Parameters
        ----------
        results_cases : CasesMultiCPTResultsProtocol
            The results of the bearing capacity calculations.
        """

        # Initialize figure CPT resuls vs. pile tip level
        self._figure_plts = FigureCPTResultsVersusPtls(results_cases=results_cases)

        # Set up control widgets
        self._case_dropdown = widgets.Dropdown(
            description="Case:",
            value=self._figure_plts.cases[0],
            options=self._figure_plts.cases,
        )

        # Create a sorted list of unique result names
        _options = natsorted(
            set(
                [
                    result_def.name
                    for result_def in results_cases.cpt_results_table.result_def
                ]
            )
        )
        _initial_option = "R_c_d_net" if "R_c_d_net" in _options else _options[0]
        self._result_dropdown = widgets.Dropdown(
            description="Result:",
            value=_initial_option,
            options=_options,
        )

        # Update plot for initial selection of control widgets
        self._update_case_and_result(None)

        # Set up callbacks
        self._case_dropdown.observe(self._update_case_and_result, "value")
        self._result_dropdown.observe(self._update_case_and_result, "value")

        # Set up layout
        self._control_widgets = widgets.HBox(
            [
                self._case_dropdown,
                self._result_dropdown,
            ]
        )
        self._layout = widgets.VBox(
            [self._control_widgets, self._figure_plts.figure]
        )  # , width=800)

    def _update_case_and_result(self, change: Any) -> None:
        """Private method to update the figure when the case or result name are changed in the control widgets."""

        # Update the figure
        self._figure_plts.show_case_and_result(
            case_name=self._case_dropdown.value,
            result_name=self._result_dropdown.value,
        )

    def display(self) -> DisplayHandle | None:
        """Display the figure."""
        return display(self._layout)
