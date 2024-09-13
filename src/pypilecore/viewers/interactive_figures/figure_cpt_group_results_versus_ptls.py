from __future__ import annotations  # noqa: F404

from typing import Hashable, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from natsort import natsort_keygen

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTGroupResultDefinitions


class FigureCPTGroupResultsVersusPtls:
    """
    Interactive figure to show the CPT grouped results of the bearing capacity calculations
    versus the pile tip levels (PTLs).

    The layout of the figure is:
        - X axis: result values.
        - Y axis: pile tip level w.r.t. NAP.
        - Each trace represents a different case.

    The figure has a method to switch between results.
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
        self._figure = go.FigureWidget(
            layout=go.Layout(
                height=800,
                width=800,
                title="CPT Group Results vs. Pile tip level for all cases<br>Result: ",
                legend_title="Case",
                colorway=px.colors.qualitative.Plotly,
                xaxis_title="",
                yaxis=go.layout.YAxis(
                    title="Pile tip level [m NAP]",
                    title_font_size=18,
                ),
                autosize=False,
            )
        )

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
        return self.results.cpt_group_results_dataframe

    @property
    def cases(self) -> List[Hashable]:
        """The case names of each MultiCPTBearingResults."""
        return self.results.cases

    @property
    def figure(self) -> go.FigureWidget:
        """The figure widget."""
        return self._figure

    def get_visible_cases(self) -> List[Hashable]:
        """
        Returns the visible cases in the figure widget.

        Notes
        -----
            - If there are no traces in the figure, it returns all the case names.
            - If a case is None, then it is represented as "None".
        """
        if len(self.figure.data) == 0:
            # Select all cases if there are no traces in the figure yet.
            cases: List[Hashable] = []
            for case in self.cases:
                if case is None:
                    cases.append("None")
                else:
                    cases.append(case)
            return cases
        return [trace.name for trace in self.figure.data if trace.visible is True]

    def show_result(self, result_name: str) -> None:
        """Shows the group results for all pile tip levels for the requested `result_name`.

        Parameters
        ----------
        result_name : str
            The name of the result to show.

        Raises
        ------
        ValueError
            If the `result_name` is not found in the CPTResultDefinitions.
        """
        # Get the result definition that corresponds to the result name.
        result_definition = CPTGroupResultDefinitions.get(result_name)

        # Get the visible cases
        visible_cases = self.get_visible_cases()

        # Select data for result type
        selected_data = self.data.loc[
            self.data["result_name"] == result_definition.name
        ]

        # Organize data and format depending on result type
        mode = "lines+markers"
        marker_size = 6
        if result_definition in [
            CPTGroupResultDefinitions.cpt_Rc_min,
            CPTGroupResultDefinitions.cpt_Rc_max,
            CPTGroupResultDefinitions.cpt_normative,
            CPTGroupResultDefinitions.use_group_average,
            CPTGroupResultDefinitions.xi_normative,
            CPTGroupResultDefinitions.n_cpts,
        ]:
            selected_data = selected_data.sort_values(by="result", key=natsort_keygen())
            mode = "markers"
            marker_size = 10

        traces = []
        for case in self.cases:
            if case is not None:
                df = selected_data.loc[selected_data["case_name"] == case]
            else:
                df = selected_data.loc[selected_data["case_name"].isna()]

            traces.append(
                go.Scatter(
                    x=df["result"],
                    y=df["pile_tip_level_nap"],
                    mode=mode,
                    name=case if case is not None else "None",
                    marker_size=marker_size,
                )
            )

        with self.figure.batch_update():
            # Empty traces
            self.figure.data = []

            # Apply changes
            self.figure.add_traces(traces)

            self.figure.update_layout(
                title=f"CPT Group Results vs. Pile tip level for all cases<br>Result: {result_definition.value.html}",
                xaxis=go.layout.XAxis(
                    title=f"{result_definition.value.html} [{result_definition.value.unit}]",
                    title_font_size=18,
                ),
                showlegend=True,
            )

            self.figure.update_traces(
                selector=lambda x: x.name in visible_cases,
                patch=dict(
                    visible=True,
                ),
            )

            self.figure.update_traces(
                selector=lambda x: x.name not in visible_cases,
                patch=dict(
                    visible="legendonly",
                ),
            )
