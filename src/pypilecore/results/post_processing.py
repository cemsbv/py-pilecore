from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, Literal, Tuple

import matplotlib.patches as patches
import pandas as pd
from matplotlib import pyplot as plt


@dataclass(frozen=False)
class BearingTable:
    """
    *Not meant to be instantiated by the user.*

    Attributes:
    ------------
    x:
        x-coordinate
    y:
        y-coordinate
    pile_tip_level_nap:
        pile tip level [m w.r.t NAP]
    R_c_d_net:
        net design bearing capacity [kN]
    test_id:
        Name of the CPT
    """

    x: float
    y: float
    pile_tip_level_nap: float
    R_c_d_net: float
    test_id: str


@dataclass(frozen=True)
class BearingResults:
    """Object containing the results of the maximum net design bearing capacity (R_c_d_net) for every CPT."""

    data: Dict[FrozenSet[Any], BearingTable]

    def to_pandas(self) -> pd.DataFrame:
        """Get the pandas.DataFrame representation"""
        return pd.DataFrame([var.__dict__ for var in self.data.values()])

    def to_pivot_table(self) -> pd.DataFrame:
        """
        Returns a pandas dataframe, organized per CPT (test-id) and pile-tip-level-nap.
        """
        results = pd.pivot_table(
            self.to_pandas(),
            values="R_c_d_net",
            index="pile_tip_level_nap",
            columns="test_id",
            dropna=False,
        )
        return results.sort_values("pile_tip_level_nap", ascending=False)

    def plot(
        self,
        hue: Literal["colormap", "category"] = "colormap",
        pile_load_uls: float = 100,
        figsize: Tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> plt.Figure:
        """
        Plot a 3D scatterplot of the valid ULS load.

        Parameters
        ----------
        hue
            default is colormap
            The marker colors methode. If colormap is used the colors represent the `R_c_d_net` value.
            The category option sets the colors to valid ULS loads. Please use the pile_load_uls attribute to set
            the required bearing capacity.
        pile_load_uls
            default is 100 kN
            ULS load in kN. Used to determine if a pile tip level configuration is valid.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        figure:
            The `Figure` object where the data was plotted on.
        """
        kwargs_subplot = {
            "figsize": figsize,
            "tight_layout": True,
        }

        kwargs_subplot.update(kwargs)
        fig = plt.figure(**kwargs_subplot)
        axes = fig.add_subplot(projection="3d")
        df = self.to_pandas()
        # create color list based on hue option
        if hue == "category":
            colors = [
                "red" if var < pile_load_uls else "green" for var in df["R_c_d_net"]
            ]
        else:
            colors = df["R_c_d_net"].tolist()
        # create scatter plot
        cmap = axes.scatter(
            df["x"],
            df["y"],
            df["pile_tip_level_nap"],
            c=colors,
        )
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.set_zlabel("Z [m w.r.t NAP]")

        if hue == "category":
            fig.legend(
                title="$R_{c;d;net}$ [kN]",
                title_fontsize=18,
                fontsize=15,
                loc="lower right",
                handles=[
                    patches.Patch(
                        facecolor=color,
                        label=label,
                        alpha=0.9,
                        linewidth=2,
                        edgecolor="black",
                    )
                    for label, color in zip(
                        [f">= {pile_load_uls}", f"< {pile_load_uls}"],
                        ["green", "red"],
                    )
                ],
            )
        else:
            fig.colorbar(cmap, orientation="vertical", label="$R_{c;d;net}$ [kN]")

        return fig
