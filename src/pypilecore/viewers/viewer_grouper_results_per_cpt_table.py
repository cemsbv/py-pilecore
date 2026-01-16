from typing import Any

import pandas as pd
from IPython.display import DisplayHandle, display
from ipywidgets import widgets
from natsort import natsorted

from pypilecore.results.cases_grouper_results import CasesGrouperResults


class ViewerGrouperResultsPerCptTable:
    def __init__(self, group_results_cases: CasesGrouperResults) -> None:
        self.group_results_cases = group_results_cases
        self._df_widget = widgets.Output()

        self._case_dropdown = widgets.Dropdown(
            description="Case:",
            value=group_results_cases.cases[0],
            options=group_results_cases.cases,
        )

        # Create a sorted list of unique result names
        _options = natsorted(
            set(
                [
                    result_def.name
                    for result_def in group_results_cases.cpt_results_table.result_def
                ]
            )
        )
        _initial_option = "R_c_d_net" if "R_c_d_net" in _options else _options[0]
        self._result_dropdown = widgets.Dropdown(
            description="Result:",
            value=_initial_option,
            options=_options,
        )

        # Initialize the dataframe
        self._update_case_result(None)

        # Set up callbacks
        self._case_dropdown.observe(self._update_case_result, "value")
        self._result_dropdown.observe(self._update_case_result, "value")

        # Set up layout
        self._control_widgets = widgets.HBox(
            [
                self._case_dropdown,
                self._result_dropdown,
            ]
        )
        self._layout = widgets.VBox([self._control_widgets, self._df_widget])

    def to_pandas(self) -> pd.DataFrame:
        """Return the currently displayed table as a pandas DataFrame."""
        return self.group_results_cases.results_per_case[
            self._case_dropdown.value
        ].cpt_results.get_results_per_cpt(self._result_dropdown.value)

    def _update_case_result(self, change: Any) -> None:
        """
        Private method to update the figure when the case, result name or pile tip level
        are changed in the control widgets.
        """
        with self._df_widget:
            self._df_widget.clear_output()
            display(self.to_pandas().round(1))

    def display(self) -> DisplayHandle | None:
        """Display the figure."""
        return display(self._layout)
