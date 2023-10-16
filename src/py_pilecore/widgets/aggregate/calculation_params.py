from ipywidgets import HBox, Label, Layout, Stack, VBox

from ..components import (
    groundwater_level_from_cpt,
    groundwater_level_numeric,
    groundwater_level_reference,
)

but_and_stack = Stack([Label("or else"), Label("but")], selected_index=0)
groundwater_numeric_label_stack = Stack(
    [Label("[m]"), Label("[m] w.r.t. NAP")], selected_index=0
)

groundwater_level_from_cpt.layout = Layout(width="80px")
groundwater_level_reference.layout = Layout(width="140px")
groundwater_level_numeric.layout = Layout(width="50px")


def handle_groundwater_level_from_cpt_change(change: dict) -> None:
    if change["new"] == "Try to":
        but_and_stack.selected_index = 0
    else:
        but_and_stack.selected_index = 1


groundwater_level_from_cpt.observe(
    handle_groundwater_level_from_cpt_change, names="value"
)

calculation_params_widget = VBox(
    [
        HBox(
            [
                groundwater_level_from_cpt,
                Label("use the groundwater level from the CPT source,"),
            ]
        ),
        HBox(
            [
                but_and_stack,
                Label("set the value at"),
                groundwater_level_numeric,
                Label("[m] w.r.t."),
                groundwater_level_reference,
                Label("."),
            ]
        ),
    ]
)
