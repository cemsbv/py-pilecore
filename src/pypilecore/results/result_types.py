from __future__ import annotations  # noqa: F404

from dataclasses import dataclass
from enum import Enum


@dataclass
class ResultType:
    """
    Dataclass containing the name, units and html representation of a result type.
    """

    name: str
    """The name of the result type."""
    units: str
    """The units of the result type."""
    html: str
    """The html representation of the result type"""

    def __post_init__(self) -> None:
        """
        Method to validate the input types of the dataclass.

        Raises
        ------
        ValueError
            If the input types are not correct.
        """
        if not isinstance(self.name, str):
            raise TypeError(
                f"Expected type 'str' for 'name', but got {type(self.name)}"
            )
        if not isinstance(self.units, str):
            raise TypeError(
                f"Expected type 'str' for 'units', but got {type(self.units)}"
            )

        if not isinstance(self.html, str):
            raise TypeError(
                f"Expected type 'str' for 'html', but got {type(self.html)}"
            )


class CPTResultTypes(Enum):
    """
    Enumeration of available CPT result types
    """

    F_nk_cal = ResultType(name="F_nk_cal", units="kN", html="F<sub>nk;cal</sub>")
    F_nk_k = ResultType(name="F_nk_k", units="kN", html="F<sub>nk;k</sub>")
    F_nk_d = ResultType(name="F_nk_d", units="kN", html="F<sub>nk;d</sub>")
    R_b_cal = ResultType(name="R_b_cal", units="kN", html="R<sub>b;cal</sub>")
    R_b_k = ResultType(name="R_b_k", units="kN", html="R<sub>b;k</sub>")
    R_b_d = ResultType(name="R_b_d", units="kN", html="R<sub>b;d</sub>")
    R_s_cal = ResultType(name="R_s_cal", units="kN", html="R<sub>s;cal</sub>")
    R_s_k = ResultType(name="R_s_k", units="kN", html="R<sub>s;k</sub>")
    R_s_d = ResultType(name="R_s_d", units="kN", html="R<sub>s;d</sub>")
    R_c_cal = ResultType(name="R_c_cal", units="kN", html="R<sub>c;cal</sub>")
    R_c_k = ResultType(name="R_c_k", units="kN", html="R<sub>c;k</sub>")
    R_c_d = ResultType(name="R_c_d", units="kN", html="R<sub>c;d</sub>")
    R_c_d_net = ResultType(
        name="R_c_d_net",
        units="kN",
        html="R<sub>c;d;net</sub>",
    )
    F_c_k = ResultType(name="F_c_k", units="kN", html="F<sub>c;k</sub>")
    F_c_k_tot = ResultType(
        name="F_c_k_tot",
        units="kN",
        html="F<sub>c;k;tot</sub>",
    )
    negative_friction_range_nap_top = ResultType(
        name="negative_friction_range_nap_top",
        units="m NAP",
        html="Top of negative friction",
    )
    negative_friction_range_nap_btm = ResultType(
        name="negative_friction_range_nap_btm",
        units="m NAP",
        html="Bottom of negative friction",
    )
    positive_friction_range_nap_top = ResultType(
        name="positive_friction_range_nap_top",
        units="m NAP",
        html="Top of positive friction",
    )
    positive_friction_range_nap_btm = ResultType(
        name="positive_friction_range_nap_btm",
        units="m NAP",
        html="Bottom of positive friction",
    )
    q_b_max = ResultType(name="q_b_max", units="MPa", html="q<sub>b;max</sub>")
    q_s_max_mean = ResultType(
        name="q_s_max_mean",
        units="MPa",
        html="q<sub>s;max</sub>",
    )
    qc1 = ResultType(name="qc1", units="MPa", html="q<sub>c1</sub>")
    qc2 = ResultType(name="qc2", units="MPa", html="q<sub>c2</sub>")
    qc3 = ResultType(name="qc3", units="MPa", html="q<sub>c3</sub>")
    s_b = ResultType(name="s_b", units="mm", html="s<sub>b</sub>")
    s_el = ResultType(name="s_el", units="mm", html="s<sub>el</sub>")
    k_v_b = ResultType(name="k_v_b", units="MN/m", html="k<sub>v;b</sub>")
    k_v_1 = ResultType(name="k_v_1", units="MN/m", html="k<sub>v;1</sub>")

    @classmethod
    def from_name(cls, name: str) -> CPTResultTypes:
        """Returns the result type with the given name."""
        for result_type in cls:
            if result_type.value.name == name:
                return result_type
        raise ValueError(
            f"Result type with name '{name}' not found in 'CPTResultTypes'."
        )


class CPTGroupResultTypes(Enum):
    R_s_k = ResultType(name="R_s_k", units="kN", html="R<sub>s;k</sub>")
    R_b_k = ResultType(name="R_b_k", units="kN", html="R<sub>b;k</sub>")
    R_c_k = ResultType(name="R_c_k", units="kN", html="R<sub>c;k</sub>")
    R_s_d = ResultType(name="R_s_d", units="kN", html="R<sub>s;d</sub>")
    R_b_d = ResultType(name="R_b_d", units="kN", html="R<sub>b;d</sub>")
    R_c_d = ResultType(name="R_c_d", units="kN", html="R<sub>c;d</sub>")
    F_nk_cal_mean = ResultType(
        name="F_nk_cal_mean", units="kN", html="F<sub>nk;cal;mean</sub>"
    )
    F_nk_k = ResultType(name="F_nk_k", units="kN", html="F<sub>nk;k</sub>")
    F_nk_d = ResultType(name="F_nk_d", units="kN", html="F<sub>nk;d</sub>")
    R_c_d_net = ResultType(
        name="R_c_d_net",
        units="kN",
        html="R<sub>c;d;net</sub>",
    )
    F_c_k = ResultType(name="F_c_k", units="kN", html="F<sub>c;k</sub>")
    F_c_k_tot = ResultType(
        name="F_c_k_tot",
        units="kN",
        html="F<sub>c;k;tot</sub>",
    )
    s_b = ResultType(name="s_b", units="mm", html="s<sub>b</sub>")
    s_e = ResultType(name="s_e", units="mm", html="s<sub>e</sub>")
    s_e_mean = ResultType(name="s_e_mean", units="mm", html="s<sub>e;mean</sub>")
    R_b_mob_ratio = ResultType(
        name="R_b_mob_ratio", units="-", html="R<sub>b;mob;ratio</sub>"
    )
    R_s_mob_ratio = ResultType(
        name="R_s_mob_ratio", units="-", html="R<sub>s;mob;ratio</sub>"
    )
    k_v_b = ResultType(name="k_v_b", units="MN/m", html="k<sub>v;b</sub>")
    k_v_1 = ResultType(name="k_v_1", units="MN/m", html="k<sub>v;1</sub>")
    R_c_min = ResultType(name="R_c_min", units="kN", html="R<sub>c;min</sub>")
    R_c_max = ResultType(name="R_c_max", units="kN", html="R<sub>c;max</sub>")
    R_c_mean = ResultType(name="R_c_mean", units="kN", html="R<sub>c;mean</sub>")
    R_c_std = ResultType(name="R_c_std", units="kN", html="R<sub>c;std</sub>")
    R_s_mean = ResultType(name="R_s_mean", units="kN", html="R<sub>s;mean</sub>")
    R_b_mean = ResultType(name="R_b_mean", units="kN", html="R<sub>b;mean</sub>")
    var_coef = ResultType(name="var_coef", units="%", html="Variation coefficient")
    n_cpts = ResultType(name="n_cpts", units="-", html="Number of CPTs")
    use_group_average = ResultType(
        name="use_group_average", units="-", html="Use group average"
    )
    xi_normative = ResultType(name="xi_normative", units="-", html="Normative ξ")
    xi_value = ResultType(name="xi_value", units="-", html="ξ<sub>value</sub>")
    cpt_Rc_min = ResultType(
        name="cpt_Rc_min", units="-", html="CPT with R<sub>c;min</sub>"
    )
    cpt_Rc_max = ResultType(
        name="cpt_Rc_max", units="-", html="CPT with R<sub>c;max</sub>"
    )
    cpt_normative = ResultType(name="cpt_normative", units="-", html="Normative CPT")

    @classmethod
    def from_name(cls, name: str) -> CPTGroupResultTypes:
        """Returns the result type with the given name."""
        for result_type in cls:
            if result_type.value.name == name:
                return result_type
        raise ValueError(
            f"Result type with name '{name}' not found in 'CPTGroupResultTypes'."
        )
