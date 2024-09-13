from __future__ import annotations  # noqa: F404

from dataclasses import dataclass
from enum import Enum
from typing import List

from natsort import natsorted


@dataclass
class ResultDefinition:
    """
    Dataclass containing the name, units and html representation of a result.
    """

    name: str
    """The name of the result."""
    unit: str
    """The unit of the result."""
    html: str
    """The html representation of the result"""

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
        if not isinstance(self.unit, str):
            raise TypeError(
                f"Expected type 'str' for 'unit', but got {type(self.unit)}"
            )

        if not isinstance(self.html, str):
            raise TypeError(
                f"Expected type 'str' for 'html', but got {type(self.html)}"
            )


class CPTResultDefinitions(Enum):
    """
    Enumeration of available CPT result definitions.
    """

    F_nk_cal = ResultDefinition(name="F_nk_cal", unit="kN", html="F<sub>nk;cal</sub>")
    F_nk_k = ResultDefinition(name="F_nk_k", unit="kN", html="F<sub>nk;k</sub>")
    F_nk_d = ResultDefinition(name="F_nk_d", unit="kN", html="F<sub>nk;d</sub>")
    R_b_cal = ResultDefinition(name="R_b_cal", unit="kN", html="R<sub>b;cal</sub>")
    R_b_k = ResultDefinition(name="R_b_k", unit="kN", html="R<sub>b;k</sub>")
    R_b_d = ResultDefinition(name="R_b_d", unit="kN", html="R<sub>b;d</sub>")
    R_s_cal = ResultDefinition(name="R_s_cal", unit="kN", html="R<sub>s;cal</sub>")
    R_s_k = ResultDefinition(name="R_s_k", unit="kN", html="R<sub>s;k</sub>")
    R_s_d = ResultDefinition(name="R_s_d", unit="kN", html="R<sub>s;d</sub>")
    R_c_cal = ResultDefinition(name="R_c_cal", unit="kN", html="R<sub>c;cal</sub>")
    R_c_k = ResultDefinition(name="R_c_k", unit="kN", html="R<sub>c;k</sub>")
    R_c_d = ResultDefinition(name="R_c_d", unit="kN", html="R<sub>c;d</sub>")
    R_c_d_net = ResultDefinition(
        name="R_c_d_net",
        unit="kN",
        html="R<sub>c;d;net</sub>",
    )
    F_c_k = ResultDefinition(name="F_c_k", unit="kN", html="F<sub>c;k</sub>")
    F_c_k_tot = ResultDefinition(
        name="F_c_k_tot",
        unit="kN",
        html="F<sub>c;k;tot</sub>",
    )
    negative_friction_range_nap_top = ResultDefinition(
        name="negative_friction_range_nap_top",
        unit="m NAP",
        html="Top of negative friction",
    )
    negative_friction_range_nap_btm = ResultDefinition(
        name="negative_friction_range_nap_btm",
        unit="m NAP",
        html="Bottom of negative friction",
    )
    positive_friction_range_nap_top = ResultDefinition(
        name="positive_friction_range_nap_top",
        unit="m NAP",
        html="Top of positive friction",
    )
    positive_friction_range_nap_btm = ResultDefinition(
        name="positive_friction_range_nap_btm",
        unit="m NAP",
        html="Bottom of positive friction",
    )
    q_b_max = ResultDefinition(name="q_b_max", unit="MPa", html="q<sub>b;max</sub>")
    q_s_max_mean = ResultDefinition(
        name="q_s_max_mean",
        unit="MPa",
        html="q<sub>s;max</sub>",
    )
    qc1 = ResultDefinition(name="qc1", unit="MPa", html="q<sub>c1</sub>")
    qc2 = ResultDefinition(name="qc2", unit="MPa", html="q<sub>c2</sub>")
    qc3 = ResultDefinition(name="qc3", unit="MPa", html="q<sub>c3</sub>")
    s_b = ResultDefinition(name="s_b", unit="mm", html="s<sub>b</sub>")
    s_el = ResultDefinition(name="s_el", unit="mm", html="s<sub>el</sub>")
    k_v_b = ResultDefinition(name="k_v_b", unit="MN/m", html="k<sub>v;b</sub>")
    k_v_1 = ResultDefinition(name="k_v_1", unit="MN/m", html="k<sub>v;1</sub>")

    @classmethod
    def get(cls, name: str) -> CPTResultDefinitions:
        """Returns the result definition the given name."""
        try:
            return cls[name]
        except KeyError:
            raise ValueError(
                f"Result with name '{name}' not found in 'CPTResultDefinitions'."
            )

    @classmethod
    def natsorted_names(cls) -> List[str]:
        """Returns the names of the enum in natsorted order."""
        return natsorted([r.name for r in cls])


class CPTGroupResultDefinitions(Enum):
    R_s_k = ResultDefinition(name="R_s_k", unit="kN", html="R<sub>s;k</sub>")
    R_b_k = ResultDefinition(name="R_b_k", unit="kN", html="R<sub>b;k</sub>")
    R_c_k = ResultDefinition(name="R_c_k", unit="kN", html="R<sub>c;k</sub>")
    R_s_d = ResultDefinition(name="R_s_d", unit="kN", html="R<sub>s;d</sub>")
    R_b_d = ResultDefinition(name="R_b_d", unit="kN", html="R<sub>b;d</sub>")
    R_c_d = ResultDefinition(name="R_c_d", unit="kN", html="R<sub>c;d</sub>")
    F_nk_cal_mean = ResultDefinition(
        name="F_nk_cal_mean", unit="kN", html="F<sub>nk;cal;mean</sub>"
    )
    F_nk_k = ResultDefinition(name="F_nk_k", unit="kN", html="F<sub>nk;k</sub>")
    F_nk_d = ResultDefinition(name="F_nk_d", unit="kN", html="F<sub>nk;d</sub>")
    R_c_d_net = ResultDefinition(
        name="R_c_d_net",
        unit="kN",
        html="R<sub>c;d;net</sub>",
    )
    F_c_k = ResultDefinition(name="F_c_k", unit="kN", html="F<sub>c;k</sub>")
    F_c_k_tot = ResultDefinition(
        name="F_c_k_tot",
        unit="kN",
        html="F<sub>c;k;tot</sub>",
    )
    s_b = ResultDefinition(name="s_b", unit="mm", html="s<sub>b</sub>")
    s_e = ResultDefinition(name="s_e", unit="mm", html="s<sub>e</sub>")
    s_e_mean = ResultDefinition(name="s_e_mean", unit="mm", html="s<sub>e;mean</sub>")
    R_b_mob_ratio = ResultDefinition(
        name="R_b_mob_ratio", unit="-", html="R<sub>b;mob;ratio</sub>"
    )
    R_s_mob_ratio = ResultDefinition(
        name="R_s_mob_ratio", unit="-", html="R<sub>s;mob;ratio</sub>"
    )
    k_v_b = ResultDefinition(name="k_v_b", unit="MN/m", html="k<sub>v;b</sub>")
    k_v_1 = ResultDefinition(name="k_v_1", unit="MN/m", html="k<sub>v;1</sub>")
    R_c_min = ResultDefinition(name="R_c_min", unit="kN", html="R<sub>c;min</sub>")
    R_c_max = ResultDefinition(name="R_c_max", unit="kN", html="R<sub>c;max</sub>")
    R_c_mean = ResultDefinition(name="R_c_mean", unit="kN", html="R<sub>c;mean</sub>")
    R_c_std = ResultDefinition(name="R_c_std", unit="kN", html="R<sub>c;std</sub>")
    R_s_mean = ResultDefinition(name="R_s_mean", unit="kN", html="R<sub>s;mean</sub>")
    R_b_mean = ResultDefinition(name="R_b_mean", unit="kN", html="R<sub>b;mean</sub>")
    var_coef = ResultDefinition(name="var_coef", unit="%", html="Variation coefficient")
    n_cpts = ResultDefinition(name="n_cpts", unit="-", html="Number of CPTs")
    use_group_average = ResultDefinition(
        name="use_group_average", unit="-", html="Use group average"
    )
    xi_normative = ResultDefinition(name="xi_normative", unit="-", html="Normative ξ")
    xi_value = ResultDefinition(name="xi_value", unit="-", html="ξ<sub>value</sub>")
    cpt_Rc_min = ResultDefinition(
        name="cpt_Rc_min", unit="-", html="CPT with R<sub>c;min</sub>"
    )
    cpt_Rc_max = ResultDefinition(
        name="cpt_Rc_max", unit="-", html="CPT with R<sub>c;max</sub>"
    )
    cpt_normative = ResultDefinition(
        name="cpt_normative", unit="-", html="Normative CPT"
    )

    @classmethod
    def get(cls, name: str) -> CPTGroupResultDefinitions:
        """Returns the result definition given the name."""
        try:
            return cls[name]
        except KeyError:
            raise ValueError(
                f"Result with name '{name}' not found in 'CPTGroupResultDefinitions'."
            )

    @classmethod
    def natsorted_names(cls) -> List[str]:
        """Returns the names of the enum in natsorted order."""
        return natsorted([r.name for r in cls])
