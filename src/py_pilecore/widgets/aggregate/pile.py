from typing import Any

import numpy as np
from ipywidgets import Checkbox, HBox, Label, Layout, Stack, Tab, VBox, dlink

from ..components import (
    adhesion,
    alpha_p,
    alpha_s_clay_check,
    alpha_s_clay_numeric,
    alpha_s_sand,
    diameter,
    diameter_cone,
    pile_head_dropdown,
    pile_head_level_numeric,
    pile_shape,
    pile_specification,
    pile_specification_dict,
    pile_tip_level_bottom,
    pile_tip_level_step,
    pile_tip_level_top,
    pile_type,
    settlement_curve,
    smooth_pile,
    width_large,
    width_small,
)
from ..style import formatting, layouts, styles

# Style
pile_specification.layout = layouts["dropdown"]
pile_specification.style = styles["pile_specification"]
pile_type.layout = layouts["dropdown"]
pile_type.style = styles["pile_specification"]
pile_shape.layout = layouts["dropdown"]
pile_shape.style = styles["pile_specification"]
settlement_curve.layout = layouts["dropdown"]
settlement_curve.style = styles["pile_specification"]
smooth_pile.layout = Layout(width="160px")
adhesion.layout = formatting["pile_specification"]["numeric"]["layout"]
adhesion.style = formatting["pile_specification"]["numeric"]["style"]
alpha_p.layout = formatting["pile_specification"]["numeric"]["layout"]
alpha_p.style = formatting["pile_specification"]["numeric"]["style"]
alpha_s_clay_numeric.layout = formatting["pile_specification"]["numeric"]["layout"]
alpha_s_clay_numeric.style = formatting["pile_specification"]["numeric"]["style"]
alpha_s_sand.layout = formatting["pile_specification"]["numeric"]["layout"]
alpha_s_sand.style = formatting["pile_specification"]["numeric"]["style"]

alpha_s_clay_numeric.description = ""

alpha_s_clay_stack = Stack([alpha_s_clay_numeric, Label("")])
adhesion_stack = Stack([HBox([adhesion, Label("[kPa]")]), Label("")])
pile_shape_label = Label()
pile_shape_dlink = dlink((pile_shape, "value"), (pile_shape_label, "value"))


def set_pilespec_to_custom_if_required(name: str, value: Any) -> None:
    """
    Checks if the provided `value` of the widget `name` matches the default value of the
    currently selected default pile-specification. If the values don't match, the
    selected value of the `pile_specification` widget of changed to "Custom".
    """
    custom_pilespec_value = "Custom"

    if pile_specification.value in pile_specification_dict:
        default_value = pile_specification_dict[pile_specification.value][name]
        if (
            isinstance(value, bool)
            and isinstance(default_value, bool)
            and default_value is not value
        ):
            pile_specification.value = custom_pilespec_value

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
            pile_specification.value = custom_pilespec_value

        elif default_value != value:
            pile_specification.value = custom_pilespec_value


def handle_pile_specification_change(change: dict) -> None:
    if change["new"] in pile_specification_dict:
        pile_shape.value = pile_specification_dict[change["new"]]["pile_shape"]
        settlement_curve.value = pile_specification_dict[change["new"]][
            "settlement_curve"
        ]
        smooth_pile.value = pile_specification_dict[change["new"]]["smooth_pile"]
        adhesion.value = pile_specification_dict[change["new"]]["adhesion"]
        alpha_p.value = pile_specification_dict[change["new"]]["alpha_p"]
        alpha_s_clay_check.value = pile_specification_dict[change["new"]][
            "alpha_s_clay_check"
        ]
        alpha_s_sand.value = pile_specification_dict[change["new"]]["alpha_s_sand"]


def handle_smooth_pile_change(change: dict) -> None:
    if change["new"] is True:
        adhesion_stack.selected_index = 0
    else:
        adhesion_stack.selected_index = 1
    set_pilespec_to_custom_if_required(name="smooth_pile", value=change["new"])


def handle_alpha_s_clay_check_change(change: dict) -> None:
    if change["new"] == "Constant":
        alpha_s_clay_stack.selected_index = 0
    else:
        alpha_s_clay_stack.selected_index = 1
    set_pilespec_to_custom_if_required(name="alpha_s_clay_check", value=change["new"])


def handle_pile_shape_change(change: dict) -> None:
    set_pilespec_to_custom_if_required(name="pile_shape", value=change["new"])


def handle_settlement_curve_change(change: dict) -> None:
    set_pilespec_to_custom_if_required(name="settlement_curve", value=change["new"])


def handle_alpha_p_change(change: dict) -> None:
    set_pilespec_to_custom_if_required(name="alpha_p", value=change["new"])


def handle_alpha_s_sand_change(change: dict) -> None:
    set_pilespec_to_custom_if_required(name="alpha_s_sand", value=change["new"])


handle_pile_specification_change({"new": pile_specification.value})
handle_smooth_pile_change({"new": smooth_pile.value})
handle_alpha_s_clay_check_change({"new": alpha_s_clay_check.value})

pile_shape.observe(handle_pile_shape_change, names="value")
settlement_curve.observe(handle_settlement_curve_change, names="value")
alpha_s_clay_check.observe(handle_alpha_s_clay_check_change, names="value")
pile_specification.observe(handle_pile_specification_change, names="value")
smooth_pile.observe(handle_smooth_pile_change, names="value")
alpha_p.observe(handle_alpha_p_change, names="value")
alpha_s_sand.observe(handle_alpha_s_sand_change, names="value")


pile_specification_widget = VBox(
    [
        pile_specification,
        pile_shape,
        settlement_curve,
        HBox([smooth_pile, adhesion_stack]),
        alpha_p,
        HBox([alpha_s_clay_check, alpha_s_clay_stack]),
        alpha_s_sand,
    ]
)

# Pile cross-section widget

square_box = Checkbox(value=True, description="Square")
width_small.disabled = True

rect_base_dlink = dlink((width_large, "value"), (width_small, "value"))

dimension_layout = Layout(width="150px")
dimension_style = {"description_width": "90px"}
width_large.style = dimension_style
width_large.layout = dimension_layout
width_small.style = dimension_style
width_small.layout = dimension_layout
diameter.style = dimension_style
diameter.layout = dimension_layout
diameter_cone.style = dimension_style
diameter_cone.layout = dimension_layout


def handle_square_box(change: dict) -> None:
    if change["new"] is True:
        width_small.disabled = True
        rect_base_dlink.link()
    else:
        width_small.disabled = False
        rect_base_dlink.unlink()


square_box.observe(handle_square_box, names="value")

rectangular_input = VBox(
    [
        square_box,
        HBox([width_large, Label("[m]")]),
        HBox([width_small, Label("[m]")]),
    ]
)

round_input = VBox([HBox([diameter, Label("[m]")])])

round_with_conetip_input = VBox(
    [
        HBox([diameter, Label("[m]")]),
        HBox([diameter_cone, Label("[m]")]),
    ]
)

cross_section_dimensions_stack = Stack(
    [
        round_input,
        rectangular_input,
        round_with_conetip_input,
    ]
)
cross_sections_dimension_dlink = dlink(
    (pile_shape, "index"), (cross_section_dimensions_stack, "selected_index")
)

pile_crosssection_widget = VBox(
    [HBox([Label("Pile shape: "), pile_shape_label]), cross_section_dimensions_stack]
)


# Pile levels widget
def get_pile_tip_range() -> list:
    step = (-1 if pile_tip_level_step.value > 0 else 1) * pile_tip_level_step.value

    return [
        round(value, 2)
        for value in np.arange(
            start=max(pile_tip_level_bottom.value, pile_tip_level_top.value),
            stop=min(pile_tip_level_bottom.value, pile_tip_level_top.value) + step,
            step=step,
        )
    ]


pile_tip_range_caption = Label(f"PTL: {get_pile_tip_range()}")


def handle_pile_tip_range_change(change: dict) -> None:
    pile_tip_range_caption.value = f"PTL: {get_pile_tip_range()}"
    pile_tip_level_bottom.max = pile_tip_level_top.value
    pile_tip_level_top.min = pile_tip_level_bottom.value


pile_tip_level_bottom.observe(handle_pile_tip_range_change, names="value")
pile_tip_level_top.observe(handle_pile_tip_range_change, names="value")
pile_tip_level_step.observe(handle_pile_tip_range_change, names="value")

pile_tip_level_bottom.layout = layouts["numeric"]
pile_tip_level_bottom.style = styles["pile_tip_levels"]
pile_tip_level_top.layout = layouts["numeric"]
pile_tip_level_top.style = styles["pile_tip_levels"]
pile_tip_level_step.layout = layouts["numeric"]
pile_tip_level_step.style = styles["pile_tip_levels"]
pile_tip_level_step.layout = layouts["numeric"]
pile_head_dropdown.layout = Layout(width="230px")
pile_head_dropdown.style = {"description_width": "120px"}
pile_head_level_numeric.layout = Layout(width="80px")
pile_head_level_numeric.style = {"description_width": "10px"}

pile_head_level_numeric.description = ":  "
pile_head_level_stack = Stack(
    [Label(""), HBox([pile_head_level_numeric, Label("[m] w.r.t. NAP")])],
    selected_index=0,
)


def handle_pile_head_dropdown_change(change: dict) -> None:
    if change["new"] == "surface":
        pile_head_level_stack.selected_index = 0
    else:
        pile_head_level_stack.selected_index = 1


pile_head_dropdown.observe(handle_pile_head_dropdown_change, names="value")


pile_levels_widget = VBox(
    [
        Label("Pile Tip Levels:"),
        HBox([pile_tip_level_top, Label("[m] w.r.t. NAP")]),
        HBox([pile_tip_level_bottom, Label("[m] w.r.t. NAP")]),
        HBox([pile_tip_level_step, Label("[m]")]),
        pile_tip_range_caption,
        HBox([pile_head_dropdown, pile_head_level_stack]),
    ]
)


pile_widget = Tab(
    children=[pile_specification_widget, pile_crosssection_widget, pile_levels_widget],
    titles=["Specification", "Cross-section", "Levels"],
)
