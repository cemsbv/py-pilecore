import json
from typing import Any

import numpy as np
from ipywidgets import (
    BoundedFloatText,
    Checkbox,
    Dropdown,
    FloatText,
    HBox,
    Label,
    Layout,
    Stack,
    Tab,
    VBox,
    dlink,
)

from .base import BaseCoreWidget
from .style import formatting, layouts, styles

pile_specification_dict = {
    "Prefabricated concrete": {
        "pile_type": "concrete",
        "specification": "1",
        "installation": "A",
        "pile_shape": "Rectangluar",
        "pile_shape_options": [
            "Rectangluar",
        ],
        "alpha_p": 0.7,
        "smooth_pile": False,
        "adhesion": 0.0,
        "alpha_s_clay_check": "Depends on soil-type",
        "alpha_s_sand": 0.01,
        "settlement_curve": "1",
    },
    "Bored pile (drilling mud, uncased borehole)": {
        "pile_type": "concrete",
        "specification": "5",
        "installation": "F",
        "pile_shape": "Round",
        "pile_shape_options": [
            "Round",
        ],
        "alpha_p": 0.35,
        "smooth_pile": False,
        "adhesion": 0.0,
        "alpha_s_clay_check": "Depends on soil-type",
        "alpha_s_sand": 0.006,
        "settlement_curve": "3",
    },
    "Screw pile, cast in place, with grout": {
        "pile_type": "concrete",
        "specification": "3",
        "installation": "D",
        "pile_shape": "Round with cone tip",
        "pile_shape_options": [
            "Round with cone tip",
        ],
        "alpha_p": 0.63,
        "smooth_pile": False,
        "adhesion": 0.0,
        "alpha_s_clay_check": "Depends on soil-type",
        "alpha_s_sand": 0.009,
        "settlement_curve": "1",
    },
    "Driven cast-in-place, tube back by driving": {
        "pile_type": "concrete",
        "specification": "2",
        "installation": "B",
        "pile_shape": "Round with cone tip",
        "pile_shape_options": [
            "Round with cone tip",
        ],
        "alpha_p": 0.7,
        "smooth_pile": False,
        "adhesion": 0.0,
        "alpha_s_clay_check": "Depends on soil-type",
        "alpha_s_sand": 0.014,
        "settlement_curve": "1",
    },
    "Driven cast-in-place, tube back by vibration": {
        "pile_type": "concrete",
        "specification": "2",
        "installation": "C",
        "pile_shape": "Round with cone tip",
        "pile_shape_options": [
            "Round with cone tip",
        ],
        "alpha_p": 0.7,
        "smooth_pile": False,
        "adhesion": 0.0,
        "alpha_s_clay_check": "Depends on soil-type",
        "alpha_s_sand": 0.012,
        "settlement_curve": "1",
    },
    "Continuous flight auger pile": {
        "pile_type": "concrete",
        "specification": "4",
        "installation": "E",
        "pile_shape": "Round",
        "pile_shape_options": [
            "Round",
        ],
        "alpha_p": 0.56,
        "smooth_pile": False,
        "adhesion": 0.0,
        "alpha_s_clay_check": "Depends on soil-type",
        "alpha_s_sand": 0.006,
        "settlement_curve": "2",
    },
}


class PileWidget(BaseCoreWidget):
    name = "pile"

    @property
    def values(self) -> dict:
        return dict()

    def _load_cache(self) -> None:
        with open(self.widget_cache_path, "r") as cache_file:
            values = json.load(cache_file)

    def _init_ipywidget(self) -> VBox:
        self.pile_tip_level_step = BoundedFloatText(
            value=0.5,
            min=0.05,
            max=1e9,
            step=0.05,
            description="Step",
            tooltip="The interval of the Pile-tip levels.",
        )

        self.pile_tip_level_top = BoundedFloatText(
            value=1,
            min=-1,
            step=0.1,
            description="Top",
            tooltip="The highest Pile-tip level.",
        )

        self.pile_tip_level_bottom = BoundedFloatText(
            value=-1,
            max=1,
            min=-1e9,
            step=0.1,
            description="Bottom",
            tooltip="The lowest Pile-tip level.",
        )

        self.pile_head_level_numeric = FloatText(
            value=0.0,
            description="Pile-head level:",
            step=0.1,
            style={"description_width": "160px"},
            tooltip="Specify pile head level.",
        )

        self.pile_head_dropdown = Dropdown(
            options=["surface", "custom level"],
            value="surface",
            description="Pile head level at",
            tooltip="The level of the top of the pile",
        )

        self.pile_specification = Dropdown(
            options=[
                "Prefabricated concrete",
                "Bored pile (drilling mud, uncased borehole)",
                "Screw pile, cast in place, with grout",
                "Driven cast-in-place, tube back by driving",
                "Driven cast-in-place, tube back by vibration",
                "Continuous flight auger pile",
                "Custom",
            ],
            value="Prefabricated concrete",
            description="Pile specification",
            tooltip="Select a pile specification",
        )

        self.pile_type = Dropdown(
            options=["concrete", "steel", "micro", "wood"],
            value="concrete",
            description="Pile type",
        )

        self.pile_shape = Dropdown(
            options=[
                "Round",
                "Rectangluar",
                "Round with cone tip",
            ],
            value="Round with cone tip",
            description="Pile shape",
        )

        self.diameter = FloatText(
            value=0.40,
            min=0.1,
            max=2.0,
            description="Diameter",
            tooltip="Pile diameter",
        )

        self.diameter_cone = BoundedFloatText(
            value=0.40,
            min=0.1,
            max=2.0,
            description="Cone diameter",
            tooltip="Diameter of the cone at pile-tip",
        )

        self.width_large = BoundedFloatText(
            value=0.40,
            min=0.1,
            max=2.0,
            description="Width large",
            tooltip="Largest dimension of the cross-section",
        )

        self.width_small = BoundedFloatText(
            value=0.40,
            min=0.1,
            max=2.0,
            description="Width small",
            tooltip="Smallest dimension of the cross-section",
        )

        self.apply_qc3_reduction = Dropdown(
            options=["Apply", "Don't apply", "Depends on pile-type"],
            value="Depends on pile-type",
            description="qc3 reduction",
            tooltip="Should the qc_III reduction be applied?",
        )

        self.settlement_curve = Dropdown(
            options=["1", "2", "3"],
            value="1",
            description="Settlement curve",
        )

        self.smooth_pile = Checkbox(
            value=False, description="Smoothness treatment", indent=False
        )

        self.adhesion = BoundedFloatText(
            value=0,
            min=0,
            max=1e9,
            description="Adhesion",
            tooltip="Adhesion",
        )

        self.alpha_p = BoundedFloatText(
            value=0.63,
            min=0,
            max=1,
            description="alpha_p",
            tooltip="Alpha p factor used in pile tip resistance calculation",
        )

        self.alpha_s_clay_check = Dropdown(
            options=["Depends on soil-type", "Constant"], description="alpha_s_clay"
        )
        self.alpha_s_clay_numeric = BoundedFloatText(
            value=0,
            max=1,
            description="alpha_s_clay",
            tooltip="Alpha s factor for coarse layers used in the positive friction calculation",
        )

        self.alpha_s_sand = BoundedFloatText(
            value=0,
            min=1,
            max=1,
            description="alpha_s_sand",
            tooltip="Alpha s factor for coarse layers used in the positive friction calculation",
        )

        # Style
        self.pile_specification.layout = layouts["dropdown"]
        self.pile_specification.style = styles["pile_specification"]
        self.pile_type.layout = layouts["dropdown"]
        self.pile_type.style = styles["pile_specification"]
        self.pile_shape.layout = layouts["dropdown"]
        self.pile_shape.style = styles["pile_specification"]
        self.settlement_curve.layout = layouts["dropdown"]
        self.settlement_curve.style = styles["pile_specification"]
        self.smooth_pile.layout = Layout(width="160px")
        self.adhesion.layout = formatting["pile_specification"]["numeric"]["layout"]
        self.adhesion.style = formatting["pile_specification"]["numeric"]["style"]
        self.alpha_p.layout = formatting["pile_specification"]["numeric"]["layout"]
        self.alpha_p.style = formatting["pile_specification"]["numeric"]["style"]
        self.alpha_s_clay_numeric.layout = formatting["pile_specification"]["numeric"][
            "layout"
        ]
        self.alpha_s_clay_numeric.style = formatting["pile_specification"]["numeric"][
            "style"
        ]
        self.alpha_s_sand.layout = formatting["pile_specification"]["numeric"]["layout"]
        self.alpha_s_sand.style = formatting["pile_specification"]["numeric"]["style"]

        self.alpha_s_clay_numeric.description = ""

        self.alpha_s_clay_stack = Stack([self.alpha_s_clay_numeric, Label("")])
        self.adhesion_stack = Stack([HBox([self.adhesion, Label("[kPa]")]), Label("")])
        self.pile_shape_label = Label()
        self.pile_shape_dlink = dlink(
            (self.pile_shape, "value"), (self.pile_shape_label, "value")
        )

        def set_pilespec_to_custom_if_required(name: str, value: Any) -> None:
            """
            Checks if the provided `value` of the widget `name` matches the default value of the
            currently selected default pile-specification. If the values don't match, the
            selected value of the `pile_specification` widget of changed to "Custom".
            """
            custom_pilespec_value = "Custom"

            if self.pile_specification.value in pile_specification_dict:
                default_value = pile_specification_dict[self.pile_specification.value][
                    name
                ]
                if (
                    isinstance(value, bool)
                    and isinstance(default_value, bool)
                    and default_value is not value
                ):
                    self.pile_specification.value = custom_pilespec_value

                elif (
                    isinstance(value, float)
                    and isinstance(default_value, float)
                    and not np.isclose(
                        default_value,
                        value,
                        rtol=0.0,
                        atol=1e-6,
                    )
                ):
                    self.pile_specification.value = custom_pilespec_value

                elif default_value != value:
                    self.pile_specification.value = custom_pilespec_value

        def handle_pile_specification_change(change: dict) -> None:
            if change["new"] in pile_specification_dict:
                self.pile_shape.value = pile_specification_dict[change["new"]][
                    "pile_shape"
                ]
                self.settlement_curve.value = pile_specification_dict[change["new"]][
                    "settlement_curve"
                ]
                self.smooth_pile.value = pile_specification_dict[change["new"]][
                    "smooth_pile"
                ]
                self.adhesion.value = pile_specification_dict[change["new"]]["adhesion"]
                self.alpha_p.value = pile_specification_dict[change["new"]]["alpha_p"]
                self.alpha_s_clay_check.value = pile_specification_dict[change["new"]][
                    "alpha_s_clay_check"
                ]
                self.alpha_s_sand.value = pile_specification_dict[change["new"]][
                    "alpha_s_sand"
                ]

        def handle_smooth_pile_change(change: dict) -> None:
            if change["new"] is True:
                self.adhesion_stack.selected_index = 0
            else:
                self.adhesion_stack.selected_index = 1
            set_pilespec_to_custom_if_required(name="smooth_pile", value=change["new"])

        def handle_alpha_s_clay_check_change(change: dict) -> None:
            if change["new"] == "Constant":
                self.alpha_s_clay_stack.selected_index = 0
            else:
                self.alpha_s_clay_stack.selected_index = 1
            set_pilespec_to_custom_if_required(
                name="alpha_s_clay_check", value=change["new"]
            )

        def handle_pile_shape_change(change: dict) -> None:
            set_pilespec_to_custom_if_required(name="pile_shape", value=change["new"])

        def handle_settlement_curve_change(change: dict) -> None:
            set_pilespec_to_custom_if_required(
                name="settlement_curve", value=change["new"]
            )

        def handle_alpha_p_change(change: dict) -> None:
            set_pilespec_to_custom_if_required(name="alpha_p", value=change["new"])

        def handle_alpha_s_sand_change(change: dict) -> None:
            set_pilespec_to_custom_if_required(name="alpha_s_sand", value=change["new"])

        handle_pile_specification_change({"new": self.pile_specification.value})
        handle_smooth_pile_change({"new": self.smooth_pile.value})
        handle_alpha_s_clay_check_change({"new": self.alpha_s_clay_check.value})

        self.pile_shape.observe(handle_pile_shape_change, names="value")
        self.settlement_curve.observe(handle_settlement_curve_change, names="value")
        self.alpha_s_clay_check.observe(handle_alpha_s_clay_check_change, names="value")
        self.pile_specification.observe(handle_pile_specification_change, names="value")
        self.smooth_pile.observe(handle_smooth_pile_change, names="value")
        self.alpha_p.observe(handle_alpha_p_change, names="value")
        self.alpha_s_sand.observe(handle_alpha_s_sand_change, names="value")

        self.pile_specification_widget = VBox(
            [
                self.pile_specification,
                self.pile_shape,
                self.settlement_curve,
                HBox([self.smooth_pile, self.adhesion_stack]),
                self.alpha_p,
                HBox([self.alpha_s_clay_check, self.alpha_s_clay_stack]),
                self.alpha_s_sand,
            ]
        )

        # Pile cross-section widget

        self.square_box = Checkbox(value=True, description="Square")
        self.width_small.disabled = True

        rect_base_dlink = dlink(
            (self.width_large, "value"), (self.width_small, "value")
        )

        dimension_layout = Layout(width="150px")
        dimension_style = {"description_width": "90px"}
        self.width_large.style = dimension_style
        self.width_large.layout = dimension_layout
        self.width_small.style = dimension_style
        self.width_small.layout = dimension_layout
        self.diameter.style = dimension_style
        self.diameter.layout = dimension_layout
        self.diameter_cone.style = dimension_style
        self.diameter_cone.layout = dimension_layout

        def handle_square_box(change: dict) -> None:
            if change["new"] is True:
                self.width_small.disabled = True
                rect_base_dlink.link()
            else:
                self.width_small.disabled = False
                rect_base_dlink.unlink()

        self.square_box.observe(handle_square_box, names="value")

        rectangular_input = VBox(
            [
                self.square_box,
                HBox([self.width_large, Label("[m]")]),
                HBox([self.width_small, Label("[m]")]),
            ]
        )

        round_input = VBox([HBox([self.diameter, Label("[m]")])])

        round_with_conetip_input = VBox(
            [
                HBox([self.diameter, Label("[m]")]),
                HBox([self.diameter_cone, Label("[m]")]),
            ]
        )

        cross_section_dimensions_stack = Stack(
            [
                round_input,
                rectangular_input,
                round_with_conetip_input,
            ]
        )
        self.cross_sections_dimension_dlink = dlink(
            (self.pile_shape, "index"),
            (cross_section_dimensions_stack, "selected_index"),
        )

        pile_crosssection_widget = VBox(
            [
                HBox([Label("Pile shape: "), self.pile_shape_label]),
                cross_section_dimensions_stack,
            ]
        )

        # Pile levels widget
        def get_pile_tip_range() -> list:
            step = (
                -1 if self.pile_tip_level_step.value > 0 else 1
            ) * self.pile_tip_level_step.value

            return [
                round(value, 2)
                for value in np.arange(
                    start=max(
                        self.pile_tip_level_bottom.value, self.pile_tip_level_top.value
                    ),
                    stop=min(
                        self.pile_tip_level_bottom.value, self.pile_tip_level_top.value
                    )
                    + step,
                    step=step,
                )
            ]

        pile_tip_range_caption = Label(f"PTL: {get_pile_tip_range()}")

        def handle_pile_tip_range_change(change: dict) -> None:
            pile_tip_range_caption.value = f"PTL: {get_pile_tip_range()}"
            self.pile_tip_level_bottom.max = self.pile_tip_level_top.value
            self.pile_tip_level_top.min = self.pile_tip_level_bottom.value

        self.pile_tip_level_bottom.observe(handle_pile_tip_range_change, names="value")
        self.pile_tip_level_top.observe(handle_pile_tip_range_change, names="value")
        self.pile_tip_level_step.observe(handle_pile_tip_range_change, names="value")

        self.pile_tip_level_bottom.layout = layouts["numeric"]
        self.pile_tip_level_bottom.style = styles["pile_tip_levels"]
        self.pile_tip_level_top.layout = layouts["numeric"]
        self.pile_tip_level_top.style = styles["pile_tip_levels"]
        self.pile_tip_level_step.layout = layouts["numeric"]
        self.pile_tip_level_step.style = styles["pile_tip_levels"]
        self.pile_tip_level_step.layout = layouts["numeric"]
        self.pile_head_dropdown.layout = Layout(width="230px")
        self.pile_head_dropdown.style = {"description_width": "120px"}
        self.pile_head_level_numeric.layout = Layout(width="80px")
        self.pile_head_level_numeric.style = {"description_width": "10px"}

        self.pile_head_level_numeric.description = ":  "
        pile_head_level_stack = Stack(
            [Label(""), HBox([self.pile_head_level_numeric, Label("[m] w.r.t. NAP")])],
            selected_index=0,
        )

        def handle_pile_head_dropdown_change(change: dict) -> None:
            if change["new"] == "surface":
                pile_head_level_stack.selected_index = 0
            else:
                pile_head_level_stack.selected_index = 1

        self.pile_head_dropdown.observe(handle_pile_head_dropdown_change, names="value")

        self.pile_levels_widget = VBox(
            [
                Label("Pile Tip Levels:"),
                HBox([self.pile_tip_level_top, Label("[m] w.r.t. NAP")]),
                HBox([self.pile_tip_level_bottom, Label("[m] w.r.t. NAP")]),
                HBox([self.pile_tip_level_step, Label("[m]")]),
                pile_tip_range_caption,
                HBox([self.pile_head_dropdown, pile_head_level_stack]),
            ]
        )

        return Tab(
            children=[
                self.pile_specification_widget,
                pile_crosssection_widget,
                self.pile_levels_widget,
            ],
            titles=["Specification", "Cross-section", "Levels"],
        )
