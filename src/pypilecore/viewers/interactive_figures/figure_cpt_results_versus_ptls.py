from __future__ import annotations  # noqa: F404

from typing import Hashable, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTResultDefinitions


class FigureCPTResultsVersusPtls:
    """
    Interactive figure to show the CPT results of the bearing capacity calculations
    versus the pile tip levels (PTLs).

    The layout of the figure is:
        - X axis: result values.
        - Y axis: pile tip level w.r.t. NAP.
        - Each trace represents a different CPT.

    The figure has a method to switch between cases and results.
    """

    def __init__(self, cases_multi_results: CasesMultiCPTBearingResults) -> None:
        """
        Initializes the figure.

        Parameters
        ----------
        cases_multi_results : CasesMultiCPTBearingResults
            The results of the bearing capacity calculations.

        Raises
        ------
        TypeError
            If `cases_multi_results` are not of type 'CasesMultiCPTBearingResults'.
        """
        # Validate the data
        self._set_results(cases_multi_results)

        # Initialize the figure
        self._figure = go.FigureWidget()

    def _set_results(self, value: CasesMultiCPTBearingResults) -> None:
        """Private setter for the results."""
        if not isinstance(value, CasesMultiCPTBearingResults):
            raise TypeError(
                f"Expected type 'CasesMultiCPTBearingResults' for 'cases_multi_results', but got {type(value)}"
            )
        self._results = value

    @property
    def results(self) -> CasesMultiCPTBearingResults:
        """The results of the bearing capacity calculations."""
        return self._results

    @property
    def data(self) -> pd.DataFrame:
        """The dataframe used to plot the results."""
        return self.results.cpt_results_dataframe

    @property
    def cases(self) -> List[Hashable]:
        """The case names of each MultiCPTBearingResults."""
        return self.results.cases

    @property
    def test_ids(self) -> List[str]:
        """The test_ids (cpt names) of all the MultiCPTBearingResults."""
        return self.results.test_ids

    @property
    def figure(self) -> go.FigureWidget:
        """The figure widget."""
        return self._figure

    def get_visible_test_ids(self) -> List[go.Scatter]:
        """Returns the visible `test_id` (s) in the figure widget."""
        return [trace.name for trace in self.figure.data if trace.visible is True]

    def show_case_and_result(self, case_name: Hashable, result_name: str) -> None:
        """Shows the results for all CPTs and pile tip levels for the requested `case_name` and `result_name`.

        Parameters
        ----------
        case_name : str
            The name of the case to show.
        result_name : str
            The name of the result to show.

        Raises
        ------
        ValueError
            If the `case_name` is not found in the cases.
            If the `result_name` is not found in the CPTResultDefinitions.
        """
        # Check that case name is in cases.
        if case_name not in self.cases:
            raise ValueError(f"Case name '{case_name}' not found in cases.")

        # Get the result definition that corresponds to the result name.
        result_definition = CPTResultDefinitions.get(result_name)

        # Get the visible test_ids
        if len(self.figure.data) == 0:
            # Select all test_ids if there are no traces in the figure yet.
            visible_test_ids = self.test_ids
        else:
            visible_test_ids = self.get_visible_test_ids()

        # Select data for case name and result name.
        mask_case_name = (
            self.data["case_name"] == case_name
            if case_name is not None
            else self.data["case_name"].isna()
        )
        selected_data = self.data.loc[
            (mask_case_name) & (self.data["result_name"] == result_definition.name)
        ]
        traces = []
        for test_id in self.test_ids:
            df = selected_data.loc[selected_data["test_id"] == test_id]
            traces.append(
                go.Scatter(
                    x=df["result"],
                    y=df["pile_tip_level_nap"],
                    mode="lines+markers",
                    name=test_id,
                )
            )

        with self.figure.batch_update():
            # Empty traces
            self.figure.data = []

            # Apply changes
            self.figure.add_traces(traces)

            self.figure.update_layout(
                title=f"CPT Results vs. Pile tip level<br>Case: {case_name}, Result: {result_definition.value.html}",
                xaxis=go.layout.XAxis(
                    title=f"{result_definition.value.html} [{result_definition.value.unit}]",
                    title_font_size=18,
                ),
                showlegend=True,
                # The following parameters shouldn't be necessary to update
                # (and therefore could be assigned on initialization of self.figure),
                # but they are needed to avoid a bug in plotly since dash > 3.0.
                height=800,
                width=800,
                legend_title="CPT",
                colorway=px.colors.qualitative.Plotly,
                yaxis=go.layout.YAxis(
                    title="Pile tip level [m NAP]",
                    title_font_size=18,
                ),
                autosize=False,
            )

            self.figure.update_traces(
                selector=lambda x: x.name in visible_test_ids,
                patch=dict(
                    visible=True,
                ),
            )

            self.figure.update_traces(
                selector=lambda x: x.name not in visible_test_ids,
                patch=dict(
                    visible="legendonly",
                ),
            )
