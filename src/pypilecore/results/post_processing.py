from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple

import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d

from pypilecore.results.soil_properties import SoilProperties, get_soil_layer_handles


class MaxBearingTable:
    """
    Object that contains the results belonging to the maximum net design bearing capacity (R_c_d_net) for a single CPT.

    *Not meant to be instantiated by the user.*
    """

    def __init__(
        self,
        pile_tip_level_nap: Sequence[float],
        R_c_d_net: Sequence[float],
        F_nk_d: Sequence[float],
        origin: Sequence[str],
    ):
        """
        Object that contains the results belonging to the maximum net design bearing capacity (R_c_d_net) for a single CPT.

        Parameters
        ----------
        pile_tip_level_nap
            The elevation of the pile-tip, in [m] w.r.t. NAP.
        R_c_d_net
            The maximum net design bearing capacity, in [kN].
        F_nk_d
            The net design bearing capacity, in [kN].
        origin
            The origin of the CPT data.
        """
        self._pile_tip_level_nap = pile_tip_level_nap
        self._R_c_d_net = R_c_d_net
        self._F_nk_d = F_nk_d
        self._origin = origin

    @property
    def pile_tip_level_nap(self) -> NDArray[np.float64]:
        """The elevation of the pile-tip, in [m] w.r.t. NAP."""
        return np.array(self._pile_tip_level_nap).astype(np.float64)

    @property
    def R_c_d_net(self) -> NDArray[np.float64]:
        """The maximum net design bearing capacity, in [kN]."""
        return np.array(self._R_c_d_net).astype(np.float64)

    @property
    def F_nk_d(self) -> NDArray[np.float64]:
        """The net design bearing capacity, in [kN]."""
        return np.array(self._F_nk_d).astype(np.float64)

    @property
    def origin(self) -> NDArray[np.str_]:
        """The origin of the CPT data."""
        return np.array(self._origin).astype(np.str_)

    @lru_cache
    def to_pandas(self) -> pd.DataFrame:
        """Get the pandas.DataFrame representation"""
        return pd.DataFrame(
            dict(
                pile_tip_level_nap=self.pile_tip_level_nap,
                R_c_d_net=self.R_c_d_net,
                F_nk_d=self.F_nk_d,
                origin=self.origin,
            )
        )


@dataclass(frozen=True)
class MaxBearingResult:
    """
    Object that contains the results of a PileCore single-cpt calculation.

    *Not meant to be instantiated by the user.*

    Attributes
    ----------
    soil_properties
        The object with soil properties
    pile_head_level_nap
        The elevation of the pile-head, in [m] w.r.t. NAP.
    table
        The object with CPT results.
    """

    soil_properties: SoilProperties
    pile_head_level_nap: float
    table: MaxBearingTable

    def to_pandas(self) -> pd.DataFrame:
        """Get the pandas.DataFrame representation"""
        return self.table.to_pandas()

    def plot_bearing_capacities(
        self,
        axes: Optional[Axes] = None,
        figsize: Tuple[float, float] = (8, 10),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Axes:
        """
        Plot the bearing calculation results on an `Axes' object.

        Parameters
        ----------
        axes:
            Optional `Axes` object where the bearing capacities can be plotted on.
            If not provided, a new `plt.Figure` will be activated and the `Axes`
            object will be created and returned.
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        add_legend:
            Add a legend to the second axes object
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        axes:
            The `Axes` object where the bearing capacities were plotted on.
        """

        # Create axes objects if not provided
        if axes is not None:
            if not isinstance(axes, Axes):
                raise ValueError(
                    "'axes' argument to plot_bearing_capacities() must be a `pyplot.axes.Axes` object or None."
                )
        else:
            kwargs_subplot = {
                "figsize": figsize,
                "tight_layout": True,
            }

            kwargs_subplot.update(kwargs)

            _, axes = plt.subplots(1, 1, **kwargs_subplot)

            if not isinstance(axes, Axes):
                raise ValueError(
                    "Could not create Axes objects. This is probably due to invalid matplotlib keyword arguments. "
                )

        # add horizontal lines
        axes.axhline(
            y=self.soil_properties.groundwater_level_ref,
            color="tab:blue",
            linestyle="--",
            label="Groundwater level",
        )
        axes.axhline(
            y=self.soil_properties.surface_level_ref,
            color="tab:brown",
            linestyle="--",
            label="Surface level",
        )

        # add bearing result subplot
        axes.plot(
            np.array(self.table.F_nk_d),
            self.table.pile_tip_level_nap,
            color="tab:orange",
            label="Fnk;d",
        )
        axes.plot(
            np.array(self.table.R_c_d_net),
            self.table.pile_tip_level_nap,
            label=r"Rc;net;d",
            lw=3,
            color="tab:blue",
        )
        axes.set_xlabel("Force [kN]")

        # add legend
        if add_legend:
            axes.legend(
                loc="upper left",
                bbox_to_anchor=(1, 1),
            )

        # set grid
        axes.grid()

        return axes

    def plot_bearing_overview(
        self,
        figsize: Tuple[float, float] = (10.0, 12.0),
        width_ratios: Tuple[float, float, float] = (1, 0.1, 2),
        add_legend: bool = True,
        **kwargs: Any,
    ) -> Figure:
        """
        Plot an overview of the bearing-capacities, including the .

        Parameters
        ----------
        figsize:
            Size of the activate figure, as the `plt.figure()` argument.
        width_ratios:
            Tuple of width-ratios of the subplots, as the `plt.GridSpec` argument.
        add_legend:
            Add a legend to the second axes object
        **kwargs:
            All additional keyword arguments are passed to the `pyplot.subplots()` call.

        Returns
        -------
        fig:
            The matplotlib Figure
        """

        kwargs_subplot = {
            "gridspec_kw": {"width_ratios": width_ratios},
            "sharey": "row",
            "figsize": figsize,
            "tight_layout": True,
        }

        kwargs_subplot.update(kwargs)

        fig, _ = plt.subplots(
            1,
            3,
            **kwargs_subplot,
        )

        ax_qc, ax_layers, ax_bearing = fig.axes
        ax_rf = ax_qc.twiny()
        assert isinstance(ax_rf, Axes)

        # Plot bearing capacities
        self.soil_properties.cpt_table.plot_qc(ax_qc, add_legend=False)
        self.soil_properties.cpt_table.plot_friction_ratio(ax_rf, add_legend=False)
        self.soil_properties.plot_layers(ax_layers, add_legend=False)
        self.plot_bearing_capacities(axes=ax_bearing, add_legend=False)

        if add_legend:
            ax_qc_legend_handles_list = ax_qc.get_legend_handles_labels()[0]
            ax_rf_legend_handles_list = ax_rf.get_legend_handles_labels()[0]
            ax_layers_legend_handles_list = get_soil_layer_handles()

            # Omit last 2 duplicate "bearing" handles
            # (groundwater_level and surface_level):
            ax_bearing_legend_handles_list = ax_bearing.get_legend_handles_labels()[0][
                2:
            ]

            handles_list = [
                *ax_qc_legend_handles_list,
                *ax_rf_legend_handles_list,
                *ax_layers_legend_handles_list,
                *ax_bearing_legend_handles_list,
            ]

            ax_bearing.legend(
                handles=handles_list,
                loc="upper left",
                bbox_to_anchor=(1, 1),
                title="name: " + self.soil_properties.test_id
                if self.soil_properties.test_id is not None
                else "name: unknown",
            )

        return fig


class MaxBearingResults:
    """Object containing the results for the maximum net design bearing capacity (R_c_d_net) for every CPT."""

    def __init__(self, cpt_results_dict: Dict[str, MaxBearingResult]):
        """
        Object containing the results for the maximum net design bearing capacity (R_c_d_net) for every CPT.

        Parameters
        ----------
        cpt_results_dict
            The results for the maximum net design bearing capacity (R_c_d_net) for every CPT.
        """
        self._cpt_results_dict = cpt_results_dict

    def __getitem__(self, test_id: str) -> MaxBearingResult:
        if not isinstance(test_id, str):
            raise TypeError(f"Expected a test-id as a string, but got: {type(test_id)}")

        return self.get_cpt_results(test_id)

    @property
    def cpt_results_dict(self) -> Dict[str, MaxBearingResult]:
        """The dictionary with the MaxBearingResult for each CPT."""
        return self._cpt_results_dict

    @property
    def test_ids(self) -> List[str]:
        """The test-ids of the CPTs."""
        return list(self.cpt_results_dict.keys())

    @property
    def results(self) -> List[MaxBearingResult]:
        """The computed results, as a list of MaxBearingResult objects."""
        return list(self.cpt_results_dict.values())

    def get_cpt_results(self, test_id: str) -> MaxBearingResult:
        """
        Returns the `MaxBearingResult` object for the provided test_id.
        """

        if test_id not in self.cpt_results_dict.keys():
            raise ValueError(
                f"No Cpt-results were calculated for this test-id: {test_id}. "
                "Please check the spelling or run a new calculation for this CPT."
            )

        return self.cpt_results_dict[test_id]

    def get_results_per_cpt(self, column_name: str) -> pd.DataFrame:
        """
        Returns a pandas dataframe with a single result-item, organized per CPT
        (test-id) and pile-tip-level-nap.

        Parameters
        ----------
        column_name:
            The name of the result-item / column name of the single-cpt-results table.
        """
        if column_name not in self.to_pandas().columns or column_name in [
            "pile_tip_level_nap",
            "test_id",
        ]:
            raise ValueError("Invalid column_name provided.")

        results = pd.pivot(
            self.to_pandas(),
            values=column_name,
            index="pile_tip_level_nap",
            columns="test_id",
        )
        return results.sort_values("pile_tip_level_nap", ascending=False)

    @lru_cache
    def to_pandas(self) -> pd.DataFrame:
        """Returns a total overview of all single-cpt results in a pandas.DataFrame representation."""
        df_list: List[pd.DataFrame] = []

        for test_id in self.cpt_results_dict:
            df = self.cpt_results_dict[test_id].table.to_pandas()
            df = df.assign(test_id=test_id)
            df = df.assign(x=self.cpt_results_dict[test_id].soil_properties.x)
            df = df.assign(y=self.cpt_results_dict[test_id].soil_properties.y)
            df_list.append(df)

        cpt_results_df = pd.concat(df_list)
        cpt_results_df = cpt_results_df.assign(
            pile_tip_level_nap=cpt_results_df.pile_tip_level_nap.round(1)
        )

        return cpt_results_df

    @lru_cache()
    def triangulation(self, pile_tip_level_nap: float) -> List[Dict[str, list]]:
        """
        Delaunay tessellation based on the CPT location

        Returns
        -------
        collection: List
            A list of dictionaries containing the tessellation
            geometry and corresponding cpt names:

                - geometry: List[Tuple[float, float]]
                - test_id: List[str]

        """
        _lookup = {
            (point.soil_properties.x, point.soil_properties.y): key
            for key, point in self.cpt_results_dict.items()
        }
        # select point with valid bearing capacity at pile tip level
        _points = (
            self.to_pandas()
            .loc[
                (self.to_pandas()["pile_tip_level_nap"] == pile_tip_level_nap)
                & (~pd.isna(self.to_pandas()["R_c_d_net"])),
                ["x", "y"],
            ]
            .to_numpy()
            .tolist()
        )

        # check if enough points Delaunay
        if len(_points) < 4:
            raise ValueError(
                "Not enough points at this pile tip level to construct "
                "the delaunay tessellation based on the CPT location."
            )
        tri = Delaunay(
            _points,
            incremental=False,
            furthest_site=False,
            qhull_options="Qbb",
        )
        geometries = np.array(_points)[tri.simplices]

        return [
            {
                "geometry": geometry.tolist(),
                "test_id": [_lookup[(xy[0], xy[1])] for xy in geometry],
            }
            for geometry in geometries
        ]

    def plot(
        self,
        projection: Optional[Literal["3d"]] = "3d",
        hue: Literal["colormap", "category"] = "colormap",
        pile_load_uls: float = 100,
        figsize: Tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> plt.Figure:
        """
        Plot a 3D scatterplot of the valid ULS load.

        Parameters
        ----------
        projection
            default is 3d
            The projection type of the subplot. use None to create a 2D plot
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
        axes = fig.add_subplot(projection=projection)
        df = self.to_pandas().dropna()
        # create color list based on hue option
        if hue == "category":
            colors = [
                "red" if var < pile_load_uls else "green" for var in df["R_c_d_net"]
            ]
        else:
            colors = df["R_c_d_net"].tolist()
        # create scatter plot
        if projection == "3d":
            cmap = axes.scatter(
                df["x"],
                df["y"],
                df["pile_tip_level_nap"],
                c=colors,
            )
            axes.set_xlabel("X")
            axes.set_ylabel("Y")
            axes.set_zlabel("Z [m w.r.t NAP]")

            # set cpt names
            for key, result in self.cpt_results_dict.items():
                axes.text(
                    result.soil_properties.x,
                    result.soil_properties.y,
                    result.table.pile_tip_level_nap.max(),
                    key,
                    "z",
                )
        else:
            cmap = axes.scatter(
                df["test_id"],
                df["pile_tip_level_nap"],
                c=colors,
            )
            axes.set_ylabel("Z [m w.r.t NAP]")
            axes.tick_params(axis="x", labelrotation=90)
            axes.grid()

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

    def map(
        self,
        pile_tip_level_nap: float,
        pile_load_uls: float = 100,
        show_delaunay_vertices: bool = True,
        show_voronoi_vertices: bool = False,
        figsize: Tuple[int, int] | None = None,
        **kwargs: Any,
    ) -> plt.Figure:
        """
        Plot a map of the valid ULS load for a given depth.

        Note
        ------
        Based on the Delaunay methode a tessellation is created with
        the location of the CPT's. Each triangle is then colored according to
        the bearing capacity of the CPT its based on. If any of the CPT does
        not meet the required capacity the triangle becomes also invalid.

        Warnings
        --------
        Please note that this map indication of valid ULS zones is intended as a visual aid to help
        the geotechnical engineer. It does not necessarily comply with the NEN 9997-1+C2:2017 since the NEN is open
        to interpretation. It is therefore that the interpretation provided by this methode must be carefully
        validated by a geotechnical engineer.

        Parameters
        ----------
        pile_tip_level_nap:
            Pile tip level to generate map.
        pile_load_uls
            default is 100 kN
            ULS load in kN. Used to determine if a pile tip level configuration is valid.
        show_delaunay_vertices
            default is True
            Add delaunay vertices to the figure
        show_voronoi_vertices
            default is False
            Add voronoi vertices to the figure
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
        fig, axes = plt.subplots(**kwargs_subplot)

        # filter data
        df = (
            self.to_pandas()
            .loc[self.to_pandas()["pile_tip_level_nap"] == pile_tip_level_nap]
            .dropna()
        )

        if df.empty:
            raise ValueError(
                "Pile tip level is not valid pile tip level. "
                "Please select one of the following pile tip level: "
                f"[{(self.to_pandas()['pile_tip_level_nap']).unique()}]"
            )

        df["valid"] = [
            False if var < pile_load_uls else True for var in df["R_c_d_net"]
        ]

        # iterate over geometry
        if show_delaunay_vertices:
            _patches = []
            for tri in self.triangulation(pile_tip_level_nap):
                color = (
                    "green"
                    if all(
                        df.where(df["test_id"].isin(tri["test_id"])).dropna()["valid"]
                    )
                    else "red"
                )
                _patches.append(
                    patches.Polygon(
                        np.array(tri["geometry"]), facecolor=color, edgecolor="grey"
                    )
                )

            collection = PatchCollection(_patches, match_original=True)
            axes.add_collection(collection)

        if show_voronoi_vertices:
            points = [
                (point.soil_properties.x, point.soil_properties.y)
                for point in self.cpt_results_dict.values()
            ]
            vor = Voronoi(points)
            voronoi_plot_2d(
                vor,
                show_vertices=False,
                show_points=False,
                ax=axes,
                line_colors="black",
                line_alpha=0.7,
                line_width=0.1,
                point_size=0.0,
            )

        # add the cpt names
        axes.scatter(
            df["x"],
            df["y"],
            c=["green" if val else "red" for val in df["valid"]],
        )
        for label, x, y in zip(df["test_id"], df["x"], df["y"]):
            axes.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.ticklabel_format(useOffset=False)
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
        axes.set_title(f"Pile tip level at: {pile_tip_level_nap} [m w.r.t NAP]")

        return fig
