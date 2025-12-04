from __future__ import annotations  # noqa: F404

from dataclasses import dataclass
from enum import Enum

from pypilecore.results.lib import Unit


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


class CPTResultDefinition(Enum):
    """
    Enumeration of available CPT result definitions.
    """

    F_nk_cal = ResultDefinition(
        name="F_nk_cal", unit=Unit.KN, html="F<sub>nk;cal</sub>"
    )
    F_nk_k = ResultDefinition(name="F_nk_k", unit=Unit.KN, html="F<sub>nk;k</sub>")
    F_nk_d = ResultDefinition(name="F_nk_d", unit=Unit.KN, html="F<sub>nk;d</sub>")
    R_b_cal = ResultDefinition(name="R_b_cal", unit=Unit.KN, html="R<sub>b;cal</sub>")
    R_b_k = ResultDefinition(name="R_b_k", unit=Unit.KN, html="R<sub>b;k</sub>")
    R_b_d = ResultDefinition(name="R_b_d", unit=Unit.KN, html="R<sub>b;d</sub>")
    R_s_cal = ResultDefinition(name="R_s_cal", unit=Unit.KN, html="R<sub>s;cal</sub>")
    R_s_k = ResultDefinition(name="R_s_k", unit=Unit.KN, html="R<sub>s;k</sub>")
    R_s_d = ResultDefinition(name="R_s_d", unit=Unit.KN, html="R<sub>s;d</sub>")
    R_c_cal = ResultDefinition(name="R_c_cal", unit=Unit.KN, html="R<sub>c;cal</sub>")
    R_c_k = ResultDefinition(name="R_c_k", unit=Unit.KN, html="R<sub>c;k</sub>")
    R_c_d = ResultDefinition(name="R_c_d", unit=Unit.KN, html="R<sub>c;d</sub>")
    R_c_d_net = ResultDefinition(
        name="R_c_d_net",
        unit=Unit.KN,
        html="R<sub>c;d;net</sub>",
    )
    F_c_k = ResultDefinition(name="F_c_k", unit=Unit.KN, html="F<sub>c;k</sub>")
    F_c_k_tot = ResultDefinition(
        name="F_c_k_tot",
        unit=Unit.KN,
        html="F<sub>c;k;tot</sub>",
    )
    negative_friction_range_nap_top = ResultDefinition(
        name="negative_friction_range_nap_top",
        unit=Unit.M_NAP,
        html="Top of negative friction",
    )
    negative_friction_range_nap_btm = ResultDefinition(
        name="negative_friction_range_nap_btm",
        unit=Unit.M_NAP,
        html="Bottom of negative friction",
    )
    positive_friction_range_nap_top = ResultDefinition(
        name="positive_friction_range_nap_top",
        unit=Unit.M_NAP,
        html="Top of positive friction",
    )
    positive_friction_range_nap_btm = ResultDefinition(
        name="positive_friction_range_nap_btm",
        unit=Unit.M_NAP,
        html="Bottom of positive friction",
    )
    q_b_max = ResultDefinition(name="q_b_max", unit=Unit.MPA, html="q<sub>b;max</sub>")
    q_s_max_mean = ResultDefinition(
        name="q_s_max_mean",
        unit=Unit.MPA,
        html="q<sub>s;max</sub>",
    )
    qc1 = ResultDefinition(name="qc1", unit=Unit.MPA, html="q<sub>c1</sub>")
    qc2 = ResultDefinition(name="qc2", unit=Unit.MPA, html="q<sub>c2</sub>")
    qc3 = ResultDefinition(name="qc3", unit=Unit.MPA, html="q<sub>c3</sub>")
    s_b = ResultDefinition(name="s_b", unit=Unit.MM, html="s<sub>b</sub>")
    s_el = ResultDefinition(name="s_el", unit=Unit.MM, html="s<sub>el</sub>")
    k_v_b = ResultDefinition(name="k_v_b", unit=Unit.MN_M, html="k<sub>v;b</sub>")
    k_v_1 = ResultDefinition(name="k_v_1", unit=Unit.MN_M, html="k<sub>v;1</sub>")
    R_t_d = ResultDefinition(name="R_t_d", unit=Unit.KN, html="R<sub>t;d</sub>")
    R_t_k = ResultDefinition(name="R_t_k", unit=Unit.KN, html="R<sub>t;k</sub>")
    R_t_d_plug = ResultDefinition(
        name="R_t_d_plug", unit=Unit.KN, html="R<sub>t;d;kluit</sub>"
    )
    R_s_mob = ResultDefinition(name="R_s_mob", unit=Unit.KN, html="R<sub>s;mob</sub>")
    R_s_mob_ratio = ResultDefinition(
        name="R_s_mob_ratio", unit=Unit.NONE, html="R<sub>s;mob;ratio</sub>"
    )
    s_e = ResultDefinition(name="s_e", unit=Unit.MM, html="s<sub>e</sub>")

    @classmethod
    def get(cls, name: str) -> CPTResultDefinition:
        """Returns the result definition the given name."""
        try:
            return cls[name]
        except KeyError:
            raise ValueError(
                f"Result with name '{name}' not found in 'CPTResultDefinition'."
            )


class CPTGroupResultDefinition(Enum):
    R_s_k = ResultDefinition(name="R_s_k", unit=Unit.KN, html="R<sub>s;k</sub>")
    R_b_k = ResultDefinition(name="R_b_k", unit=Unit.KN, html="R<sub>b;k</sub>")
    R_c_k = ResultDefinition(name="R_c_k", unit=Unit.KN, html="R<sub>c;k</sub>")
    R_s_d = ResultDefinition(name="R_s_d", unit=Unit.KN, html="R<sub>s;d</sub>")
    R_b_d = ResultDefinition(name="R_b_d", unit=Unit.KN, html="R<sub>b;d</sub>")
    R_c_d = ResultDefinition(name="R_c_d", unit=Unit.KN, html="R<sub>c;d</sub>")
    F_nk_cal_mean = ResultDefinition(
        name="F_nk_cal_mean", unit=Unit.KN, html="F<sub>nk;cal;mean</sub>"
    )
    F_nk_k = ResultDefinition(name="F_nk_k", unit=Unit.KN, html="F<sub>nk;k</sub>")
    F_nk_d = ResultDefinition(name="F_nk_d", unit=Unit.KN, html="F<sub>nk;d</sub>")
    R_c_d_net = ResultDefinition(
        name="R_c_d_net",
        unit=Unit.KN,
        html="R<sub>c;d;net</sub>",
    )
    F_c_k = ResultDefinition(name="F_c_k", unit=Unit.KN, html="F<sub>c;k</sub>")
    F_c_k_tot = ResultDefinition(
        name="F_c_k_tot",
        unit=Unit.KN,
        html="F<sub>c;k;tot</sub>",
    )
    s_b = ResultDefinition(name="s_b", unit=Unit.MM, html="s<sub>b</sub>")
    s_e = ResultDefinition(name="s_e", unit=Unit.MM, html="s<sub>e</sub>")
    s_e_mean = ResultDefinition(
        name="s_e_mean", unit=Unit.MM, html="s<sub>e;mean</sub>"
    )
    R_b_mob_ratio = ResultDefinition(
        name="R_b_mob_ratio", unit=Unit.NONE, html="R<sub>b;mob;ratio</sub>"
    )
    R_s_mob_ratio = ResultDefinition(
        name="R_s_mob_ratio", unit=Unit.NONE, html="R<sub>s;mob;ratio</sub>"
    )
    k_v_b = ResultDefinition(name="k_v_b", unit=Unit.MN_M, html="k<sub>v;b</sub>")
    k_v_1 = ResultDefinition(name="k_v_1", unit=Unit.MN_M, html="k<sub>v;1</sub>")
    R_c_min = ResultDefinition(name="R_c_min", unit=Unit.KN, html="R<sub>c;min</sub>")
    R_c_max = ResultDefinition(name="R_c_max", unit=Unit.KN, html="R<sub>c;max</sub>")
    R_c_mean = ResultDefinition(
        name="R_c_mean", unit=Unit.KN, html="R<sub>c;mean</sub>"
    )
    R_c_std = ResultDefinition(name="R_c_std", unit=Unit.KN, html="R<sub>c;std</sub>")
    R_s_mean = ResultDefinition(
        name="R_s_mean", unit=Unit.KN, html="R<sub>s;mean</sub>"
    )
    R_b_mean = ResultDefinition(
        name="R_b_mean", unit=Unit.KN, html="R<sub>b;mean</sub>"
    )
    var_coef = ResultDefinition(
        name="var_coef", unit=Unit.PERC, html="Variation coefficient"
    )
    n_cpts = ResultDefinition(name="n_cpts", unit=Unit.NONE, html="Number of CPTs")
    use_group_average = ResultDefinition(
        name="use_group_average", unit=Unit.NONE, html="Use group average"
    )
    xi_normative = ResultDefinition(
        name="xi_normative", unit=Unit.NONE, html="Normative ξ"
    )
    xi_value = ResultDefinition(
        name="xi_value", unit=Unit.NONE, html="ξ<sub>value</sub>"
    )
    cpt_Rc_min = ResultDefinition(
        name="cpt_Rc_min", unit=Unit.NONE, html="CPT with R<sub>c;min</sub>"
    )
    cpt_Rc_max = ResultDefinition(
        name="cpt_Rc_max", unit=Unit.NONE, html="CPT with R<sub>c;max</sub>"
    )
    cpt_normative = ResultDefinition(
        name="cpt_normative", unit=Unit.NONE, html="Normative CPT"
    )
    R_t_d = ResultDefinition(name="R_t_d", unit=Unit.KN, html="R<sub>t;d</sub>")
    R_t_d_mean = ResultDefinition(
        name="R_t_d_mean", unit=Unit.KN, html="R<sub>t;d;mean</sub>"
    )
    R_t_d_min = ResultDefinition(
        name="R_t_d_min", unit=Unit.KN, html="R<sub>t;d;min</sub>"
    )
    R_t_d_plug = ResultDefinition(
        name="R_t_d_plug", unit=Unit.KN, html="R<sub>t;d;kluit</sub>"
    )

    @classmethod
    def get(cls, name: str) -> CPTGroupResultDefinition:
        """Returns the result definition given the name."""
        try:
            return cls[name]
        except KeyError:
            raise ValueError(
                f"Result with name '{name}' not found in 'CPTGroupResultDefinition'."
            )


class GrouperResultsDefinition(Enum):
    """
    Enumeration of available GrouperResults definitions.
    """

    R_c_d_net = ResultDefinition(
        name="R_c_d_net",
        unit=Unit.KN,
        html="R<sub>c;d;net</sub>",
    )
    F_nk_d = ResultDefinition(name="F_nk_d", unit=Unit.KN, html="F<sub>nk;d</sub>")

    @classmethod
    def get(cls, name: str) -> GrouperResultsDefinition:
        """Returns the result definition given the name."""
        try:
            return cls[name]
        except KeyError:
            raise ValueError(
                f"Result with name '{name}' not found in 'GrouperResultsDefinition'."
            )
