from ipywidgets import BoundedFloatText, Checkbox, Dropdown, FloatText, Text

pile_tip_level_step = BoundedFloatText(
    value=0.5,
    min=0.05,
    max=1e9,
    step=0.05,
    description="Step",
    tooltip="The interval of the Pile-tip levels.",
)

pile_tip_level_top = BoundedFloatText(
    value=1, min=-1, step=0.1, description="Top", tooltip="The highest Pile-tip level."
)

pile_tip_level_bottom = BoundedFloatText(
    value=-1,
    max=1,
    min=-1e9,
    step=0.1,
    description="Bottom",
    tooltip="The lowest Pile-tip level.",
)

pile_head_level_numeric = FloatText(
    value=0.0,
    description="Pile-head level:",
    step=0.1,
    style={"description_width": "160px"},
    tooltip="Specify pile head level.",
)

pile_head_dropdown = Dropdown(
    options=["surface", "custom level"],
    value="surface",
    description="Pile head level at",
    tooltip="The level of the top of the pile",
)

pile_specification = Dropdown(
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

pile_type = Dropdown(
    options=["concrete", "steel", "micro", "wood"],
    value="concrete",
    description="Pile type",
)

pile_shape = Dropdown(
    options=[
        "Round",
        "Rectangluar",
        "Round with cone tip",
    ],
    value="Round with cone tip",
    description="Pile shape",
)

diameter = FloatText(
    value=0.40, min=0.1, max=2.0, description="Diameter", tooltip="Pile diameter"
)

diameter_cone = BoundedFloatText(
    value=0.40,
    min=0.1,
    max=2.0,
    description="Cone diameter",
    tooltip="Diameter of the cone at pile-tip",
)

width_large = BoundedFloatText(
    value=0.40,
    min=0.1,
    max=2.0,
    description="Width large",
    tooltip="Largest dimension of the cross-section",
)

width_small = BoundedFloatText(
    value=0.40,
    min=0.1,
    max=2.0,
    description="Width small",
    tooltip="Smallest dimension of the cross-section",
)

apply_qc3_reduction = Dropdown(
    options=["Apply", "Don't apply", "Depends on pile-type"],
    value="Depends on pile-type",
    description="qc3 reduction",
    tooltip="Should the qc_III reduction be applied?",
)

settlement_curve = Dropdown(
    options=["1", "2", "3"],
    value="1",
    description="Settlement curve",
)

smooth_pile = Checkbox(value=False, description="Smoothness treatment", indent=False)

adhesion = BoundedFloatText(
    value=0,
    min=0,
    max=1e9,
    description="Adhesion",
    tooltip="Adhesion",
)

alpha_p = BoundedFloatText(
    value=0.63,
    min=0,
    max=1,
    description="alpha_p",
    tooltip="Alpha p factor used in pile tip resistance calculation",
)

alpha_s_clay_check = Dropdown(
    options=["Depends on soil-type", "Constant"], description="alpha_s_clay"
)
alpha_s_clay_numeric = BoundedFloatText(
    value=0,
    max=1,
    description="alpha_s_clay",
    tooltip="Alpha s factor for coarse layers used in the positive friction calculation",
)

alpha_s_sand = BoundedFloatText(
    value=0,
    min=1,
    max=1,
    description="alpha_s_sand",
    tooltip="Alpha s factor for coarse layers used in the positive friction calculation",
)

groundwater_level_from_cpt = Dropdown(
    options=["Try to", "Never"],
    value="Try to",
)

groundwater_level_reference = Dropdown(
    options=["surface level", "NAP"], value="surface level"
)

groundwater_level_numeric = FloatText(
    value=-1,
)

cpt_id = Text(value="")
