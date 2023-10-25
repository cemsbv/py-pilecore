from __future__ import annotations

from copy import deepcopy
from typing import Any, Tuple

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import NDArray

# Axis with mobilized capacity as a fracion of maximum.
mob_over_max = np.array(
    [
        0,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
        0.75,
        0.80,
        0.85,
        0.90,
        0.95,
        0.98,
        1.00,
    ]
)

# Axis with s_b/Deq [%] due to pile-tip mobilization for settlement-curve 1
sb_rb_1 = np.array(
    [
        0,
        0.03,
        0.08,
        0.16,
        0.26,
        0.4,
        0.55,
        0.73,
        0.95,
        1.18,
        1.48,
        1.83,
        2.3,
        2.85,
        3.49,
        4.25,
        5.13,
        6.33,
        7.8,
        9,
        10,
    ]
)

# Axis with s_b/Deq [%] due to pile-tip mobilization for settlement-curve 2
sb_rb_2 = np.array(
    [
        0,
        0.15,
        0.3,
        0.5,
        0.75,
        1.06,
        1.41,
        1.79,
        2.2,
        2.71,
        3.29,
        3.99,
        4.81,
        5.8,
        7.04,
        8.57,
        10.46,
        12.76,
        15.62,
        17.95,
        20,
    ]
)

# Axis with s_b/Deq [%] due to pile-tip mobilization for settlement-curve 3
sb_rb_3 = np.array(
    [
        0,
        0.55,
        0.91,
        1.31,
        1.73,
        2.19,
        2.7,
        3.23,
        3.78,
        4.4,
        5.09,
        5.84,
        6.85,
        8.07,
        9.45,
        10.99,
        12.73,
        14.67,
        17.05,
        18.7,
        20,
    ]
)

# Axis with s_b [mm] due to pile-shaft mobilization for settlement-curve 1
sb_rs_1 = np.array(
    [
        0,
        0.05,
        0.1,
        0.17,
        0.29,
        0.45,
        0.65,
        0.87,
        1.12,
        1.39,
        1.69,
        2.02,
        2.38,
        2.78,
        3.3,
        4.04,
        4.96,
        6.22,
        7.87,
        9.16,
        10.3,
    ]
)

# Axis with s_b [mm] due to pile-shaft mobilization for settlement-curve 2
sb_rs_2 = np.array(
    [
        0,
        0.55,
        0.91,
        1.3,
        1.73,
        2.18,
        2.67,
        3.24,
        3.82,
        4.47,
        5.16,
        5.91,
        6.7,
        7.51,
        8.59,
        9.97,
        11.83,
        14.48,
        17.93,
        20.8,
        23.5,
    ]
)

# Axis with s_b [mm] due to pile-shaft mobilization for settlement-curve 3
sb_rs_3 = np.array(
    [
        0,
        0.55,
        0.91,
        1.3,
        1.73,
        2.18,
        2.67,
        3.24,
        3.82,
        4.47,
        5.16,
        5.91,
        6.7,
        7.51,
        8.59,
        9.97,
        11.83,
        14.48,
        17.93,
        20.8,
        23.5,
    ]
)

# Axis with s_b [m] due to pile-shaft mobilization for settlement-curve 1 [ANCHOR]
mob_over_max_anchor = np.array(
    [
        0,
        0.25,
        0.4,
        0.5,
        0.75,
        1.0,
        1.5,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        7.5,
        8.0,
        9.0,
        9.5,
        10,
        10.6,
        11.0,
        12.0,
        13.0,
        14.0,
        15.0,
        16.0,
        17.0,
        18.0,
        19.0,
        20,
        21.0,
        22.0,
        23.0,
        24.0,
        25.0,
        26.0,
        27.0,
        28.0,
        29.0,
        30.0,
        50.0,
    ]
)

# Axis with mobilized capacity as a fraction of maximum for settlement-curve 1 [ANCHOR]
sb_rs_1_anchor = np.array(
    [
        0.0,
        0.25,
        0.29,
        0.32,
        0.40,
        0.44,
        0.53,
        0.60,
        0.73,
        0.81,
        0.865,
        0.902,
        0.930,
        0.942,
        0.954,
        0.976,
        0.987,
        1.0,
        1.0,
        1.0,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
    ]
)

# Axis with mobilized capacity as a fraction of maximum for settlement-curve 2 [ANCHOR]
sb_rs_2_anchor = np.array(
    [
        0.0,
        0.048,
        0.06,
        0.08,
        0.11,
        0.16,
        0.23,
        0.29,
        0.39,
        0.47,
        0.55,
        0.61,
        0.668,
        0.69,
        0.723,
        0.77,
        0.79,
        0.805,
        0.825,
        0.835,
        0.863,
        0.885,
        0.902,
        0.919,
        0.93,
        0.943,
        0.954,
        0.964,
        0.972,
        0.98,
        0.984,
        0.99,
        0.995,
        1.0,
        1.0,
        0.50,
        0.50,
        0.50,
        0.50,
        0.50,
    ]
)

curve_type_map = {
    1: {
        "sb_rs": sb_rs_1,
        "sb_rb": sb_rb_1,
    },
    2: {
        "sb_rs": sb_rs_2,
        "sb_rb": sb_rb_2,
    },
    3: {
        "sb_rs": sb_rs_3,
        "sb_rb": sb_rb_3,
    },
}


def get_load_settlement_axes_data(
    curve_type: int,
) -> Tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """
    Returns the axis values from the settlement lines in Figure 7.n & 7.o

    Parameters
    ----------
    curve_type:
        The settlement-curve type

    Returns
    -------
    mob_ratio
        Array of mobilized bearing capacity ratios
    sb_rb
        Array of settlements due to Rb-mobilization, as a percentage of Deq.
    sb_rs
        Array of settlements due to Rs-mobilization [mm].
    """

    mob_ratio = deepcopy(mob_over_max)

    curves = curve_type_map[curve_type]

    return mob_ratio, curves["sb_rb"], curves["sb_rs"]


def get_load_settlement_plot(
    settlement_curve: int,
    d_eq: float,
    s_b: float,
    f_c_k: float,
    f_nk_k: float,
    r_b_k: float,
    r_s_k: float,
    rs_mob_ratio: float,
    rb_mob_ratio: float,
    sb_max: float = 25,
    axes: Axes | None = None,
    figsize: Tuple[float, float] = (6.0, 6.0),
    **kwargs: Any,
) -> Axes:
    """
    Returns a `Axes` object with a load-settlement diagram. Based on NEN 9997-1+C2
    section 7.6.4.2(i).

    Parameters
    ----------
    settlement_curve: int
        The settlement curve of the pile, according to table 7.c of NEN 9997-1+C2.
    d_eq: float
        The equivalent diameter of the pile base [m].
    s_b: float
        The settlement at pile-tip level [mm].
    f_c_k: float
        The compressive force on the pile-head [kN].
    f_nk_k: float
        The characteristic negative friction force [kN].
    r_b_k: float
        The characteristic pile-tip resistance [kN].
    r_s_k: float
        The characteristic shaft resistance [kN].
    rs_mob_ratio: float
        Ratio of the mobilized shaft resistance [-].
    rb_mob_ratio: float
        Ratio of the mobilized base resistance [-].
    sb_max: float
        Maximum pile-tip settlement [mm].
    axes:
        Optional `Axes` object. If not provided, a `plt.Figure`
        and `Axes` objects will be created.
    figsize: Tuple[float, float]
        The figure dimensions. Default = (6.0, 6.0)
    **kwargs:
        All additional keyword arguments are passed to the `pyplot.figure` call.

    """
    # Create axes objects if not provided
    if axes is not None:
        if not isinstance(axes, Axes):
            raise ValueError(
                "'axes' argument to get_load_settlement_plot() must be a `pyplot.axes.Axes` object or None."
            )
    else:
        kwargs_subplot = {
            "figsize": figsize,
            "tight_layout": True,
        }

        kwargs_subplot.update(kwargs)

        _, axes = plt.subplots(
            1,
            1,
            **kwargs_subplot,
        )

        if not isinstance(axes, Axes):
            raise ValueError(
                "Could not create Axes objects. This is probably due to invalid matplotlib keyword arguments. "
            )

    mob_ratio, sb_rb_deq, sb_rs = get_load_settlement_axes_data(settlement_curve)

    # Conversion from sb/Deq [%] to sb [mm]
    # sb_rb = sb/Deq [%] * Deq [m] / 100 [%] * 1000 (to mm)
    sb_rb = sb_rb_deq * 10 * d_eq
    sb_chart = np.append(np.flip(sb_rs), sb_rb)

    # forces
    rb_a = mob_ratio * r_b_k
    rs_a = -mob_ratio * r_s_k
    r_chart = np.append(np.flip(rs_a), rb_a)

    axes.set_ylabel("$s_b$ [mm]")
    axes.set_xlabel(
        "<-- $R_{s,k}$ [kN]                                        $R_{b,k}$ [kN] -->"
    )
    axes.plot(r_chart, sb_chart)
    axes.grid()
    if s_b <= sb_max:
        axes.annotate(
            "",
            xy=(max(-1 * rs_mob_ratio * r_s_k, -r_s_k), s_b),
            xytext=(min(rb_mob_ratio * r_b_k, r_b_k), s_b),
            arrowprops={"arrowstyle": "<|-|>"},
        )
        axes.annotate(
            f"$F_{{c,k,tot}}$: $F_{{c,k}} + F_{{s,k}}$\n$F_{{c,k}}$:{f_c_k: 3.2f} kN\n$F_{{s,k}}$:{f_nk_k: 3.2f} kN",
            xy=(0, s_b),
            xytext=(-60, -60),
            textcoords="offset pixels",
        )
        axes.annotate(
            f"$s_b$ = {s_b:3.2f} mm",
            xy=(min(rb_mob_ratio * r_b_k, r_b_k), s_b),
        )
    else:
        axes.annotate(
            f"$s_b$ = {s_b:3.2f} mm",
            xy=(-25, 0.9 * sb_max),
        )
    axes.axis((-r_s_k, r_b_k, sb_max, 0))

    axes.set_xticks(axes.get_xticks().tolist())  # to avoid FixedLocator warning
    axes.set_xticklabels([str(abs(x)) for x in axes.get_xticks()])

    return axes
