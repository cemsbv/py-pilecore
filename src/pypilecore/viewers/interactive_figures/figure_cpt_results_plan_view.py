from __future__ import annotations  # noqa: F404

from typing import Hashable, List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pypilecore.results.cases_multi_cpt_results import CasesMultiCPTBearingResults
from pypilecore.results.result_definitions import CPTResultDefinitions
from pypilecore.viewers.interactive_figures.utils import get_continuous_color


class FigureCPTResultsPlanView:
    """
    Interactive figure to show the CPT results of the bearing capacity calculations
    in plan view for a fixed pile tip level (PTL).

    The layout of the figure is:
        - X axis: X coordinate.
        - Y axis: Y coordinate.
        - Each point represents a different CPT, but the same pile tip level.

    The figure has a method to switch between case, result and pile tip level.
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
                width=1200,
                title="CPT Results in Plan View<br>Case: , Pile tip level [m NAP]: <br>Result: ",
                legend_title="CPT",
                colorway=px.colors.qualitative.Plotly,
                xaxis=go.layout.XAxis(
                    title="X [m]",
                    title_font_size=18,
                ),
                yaxis=go.layout.YAxis(
                    title="Y [m]",
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
    def pile_tip_levels_nap(self) -> List[float]:
        """The pile tip levels w.r.t. NAP of all the MultiCPTBearingResults."""
        return self.results.pile_tip_levels_nap

    @property
    def figure(self) -> go.FigureWidget:
        """The figure widget."""
        return self._figure

    def get_visible_test_ids(self) -> List[str]:
        """Returns the visible `test_id` (s) in the figure widget."""
        return [trace.name for trace in self.figure.data if trace.visible is True]

    def show_case_result_and_ptl(
        self, case_name: Hashable, result_name: str, pile_tip_level_nap: float
    ) -> None:
        """Shows the results for all CPTs for the requested `case_name`, `result_name` and `pile_tip_level`.

        Parameters
        ----------
        case_name : str
            The name of the case to show.
        result_name : str
            The name of the result to show.
        pile_tip_level_nap : float
            The pile tip level w.r.t. NAP to show.


        Raises
        ------
        TypeError
            If the `pile_tip_level_nap` is not of type 'float'.
        ValueError
            If the `case_name` is not found in the cases.
            If the `result_name` is not found in the CPTResultDefinitions.
            If the `pile_tip_level_nap` is not found in the pile tip levels.
        """
        # Check that case name is in cases.
        if case_name not in self.cases:
            raise ValueError(f"Case name '{case_name}' not found in cases.")

        # Get the result definition that corresponds to the result name.
        result_definition = CPTResultDefinitions.get(result_name)

        # Check that pile tip level NAP is in pile tip levels.
        if not isinstance(pile_tip_level_nap, (int, float)):
            raise TypeError(
                f"Expected type 'float' for 'pile_tip_level_nap', but got {type(pile_tip_level_nap)}"
            )
        if not any(
            np.isclose(pile_tip_level_nap, self.pile_tip_levels_nap, rtol=0, atol=1e-4)
        ):
            raise ValueError(
                f"Pile tip level NAP '{pile_tip_level_nap}' not found in pile tip levels NAP."
            )

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
        mask_pile_tip_level = np.isclose(
            pile_tip_level_nap,
            self.data["pile_tip_level_nap"].to_numpy(),
            rtol=0,
            atol=1e-4,
        )
        selected_data = self.data.loc[
            (mask_case_name)
            & (self.data["result_name"] == result_definition.name)
            & (mask_pile_tip_level)
        ]

        # Get the min and max result values for the color scale.
        result_max = selected_data["result"].max()
        result_min = selected_data["result"].min()
        colorscale = px.colors.get_colorscale("picnic")

        traces = []
        for test_id in self.test_ids:
            df = selected_data.loc[selected_data["test_id"] == test_id]
            result = round(df["result"].values[0], 1)
            color = get_continuous_color(
                colorscale=colorscale,
                intermed=(result - result_min) / (result_max - result_min),
            )
            traces.append(
                go.Scatter(
                    x=df["x"],
                    y=df["y"],
                    text=f"CPT {test_id}<br>{result}",
                    mode="markers+text",
                    name=test_id,
                    marker=dict(
                        size=8,
                        color=color,
                        line=dict(
                            width=0.5,
                            color="black",
                        ),
                    ),
                    textposition="top center",
                    hoverinfo="none",
                )
            )

        # Add the colorbar
        traces.append(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                name="__colorbar__",
                marker=dict(
                    colorscale=colorscale,
                    showscale=True,
                    cmin=result_min,
                    cmax=result_max,
                    colorbar=dict(
                        thickness=16,
                        orientation="h",
                        x=0.75,
                        y=1.0,
                        len=0.5,
                        title=f"{result_definition.value.html} [{result_definition.value.unit}]",
                        title_font_size=14,
                    ),
                ),
                hoverinfo="none",
                showlegend=False,
            )
        )

        with self.figure.batch_update():
            # Empty traces
            self.figure.data = []

            # Apply changes
            self.figure.add_traces(traces)

            self.figure.update_layout(
                title=f"CPT Results in Plan View<br>Case: {case_name}, "
                + f"Pile tip level [m NAP]: {pile_tip_level_nap}<br>"
                + f"Result: {result_definition.value.html} [{result_definition.value.unit}]"
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

            self.figure.update_traces(
                selector=lambda x: x.name == "__colorbar__",
                patch=dict(
                    visible=True,
                    showlegend=False,
                ),
            )
