from ipywidgets import Layout

layouts = dict(
    text=Layout(width="80%"),
    numeric=Layout(width="120px"),
    dropdown=Layout(width="60%"),
)
styles = dict(
    project_information={"description_width": "90px"},
    pile_tip_levels={"description_width": "50px"},
    pile_specification={"description_width": "110px"},
)

formatting = dict(
    pile_specification=dict(
        numeric=dict(layout=Layout(width="120px"), style={"description_width": "70px"})
    )
)
