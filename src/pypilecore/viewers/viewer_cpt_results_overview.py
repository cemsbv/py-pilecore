from __future__ import annotations  # noqa: F404

from typing import Any

import numpy as np
import pandas as pd
from IPython.display import DisplayHandle, clear_output, display
from ipywidgets import widgets
from matplotlib import pyplot as plt
from natsort import natsorted

from pypilecore.results.typing import CasesMultiCPTResultsLike


class ViewerCptResultsOverview:
    """
    Viewer for the CPT bearing results overview.

    It offers the following layout:
        - Dropdown widgets:
            - Case: to select the case to show.
            - CPT: to select the CPT to show.
        - Figure Bearing Overview (non-interactive):
    """

    def __init__(self, results_cases: CasesMultiCPTResultsLike) -> None:
        """Initialize the viewer.

        Parameters
        ----------
        results_cases : CasesMultiCPTResultsLike
            The results of the bearing capacity calculations.

        Raises
        ------
        TypeError
            If 'cases_multi_results' are not of type 'CasesMultiCPTResultsLike'.
        """

        # Initialize figure CPT resuls vs. pile tip level
        self.results_cases = results_cases

        # Set up control widgets
        self._case_dropdown = widgets.Dropdown(
            description="Case:",
            value=self.results_cases.cases[0],
            options=self.results_cases.cases,
        )

        _options = natsorted(pd.unique(np.array(self.results_cases.test_ids)))
        self._cpt_dropdown = widgets.Dropdown(
            description="CPT:",
            value=_options[0],
            options=_options,
        )

        # Initiate matplotlib figure as Output widget
        self.plot_widget = widgets.Output()
        self._update_case_and_result(None)  # Initial plot

        # Set up callbacks
        self._case_dropdown.observe(self._update_case_and_result, "value")
        self._cpt_dropdown.observe(self._update_case_and_result, "value")

        # Set up layout
        self._control_widgets = widgets.HBox(
            [
                self._case_dropdown,
                self._cpt_dropdown,
            ]
        )
        self._layout = widgets.VBox(
            [self._control_widgets, self.plot_widget]
        )  # , width=800)

    def _update_case_and_result(self, change: Any) -> None:
        """Private method to update the figure when the case or result name are changed in the control widgets."""

        with self.plot_widget:
            clear_output(wait=True)
            plt.ioff()  # Turn interactive plotting off
            fig = (
                self.results_cases.results_per_case[self._case_dropdown.value]
                .cpt_results[self._cpt_dropdown.value]
                .plot_bearing_overview()
            )
            plt.ion()  # Turn interactive plotting back on
            display(fig)
            plt.close(fig)  # Close the figure to prevent accumulation

    def display(self) -> DisplayHandle | None:
        """Display the figure."""
        return display(self._layout)
