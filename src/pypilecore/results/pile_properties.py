from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Dict, Set, Union

import numpy as np
from numpy.typing import NDArray

"""
Defines the pile property geometry classes.

Notes:
- The type of abstract-method property decorators are ignored as a workaround
    to a known mypy issue. (https://github.com/python/mypy/issues/4165)
"""


def _get_depth_keys(d: Union[str, dict], depth: int) -> Set[str]:
    if isinstance(d, str):
        return set([])
    if depth == 0:
        return set(d.keys())
    else:
        # recurse and flatten
        return set(
            [a for diction in d.values() for a in _get_depth_keys(diction, depth - 1)]
        )


# PileProperties inheritance structure:
#  -------------------------------------
#
# - PileProperties
#   - RoundPileProperties
#   - RectPileProperties
#   - TaperedPileProperties


class PileProperties(ABC):
    """
    abstract base class for geometrical pile properties
    """

    _shape: str

    def __init__(
        self,
        pile_type_specification: Dict[str, str],
        alpha_s_sand: float,
        alpha_s_clay: float | str,
        alpha_p: float,
        beta_p: float,
        pile_tip_factor_s: float | int,
        settlement_curve: int,
        elastic_modulus: float | int,
        negative_fr_delta_factor: float | int,
        adhesion: float | int,
        is_low_vibrating: bool,
        is_auger: bool,
        height_base: float,
        name: str | None = None,
    ):
        """
        Parameters
        ----------
        pile_type_specification
            Keys
                pile_type: str
                    One of ["concrete", "steel", "micro", "wood"]
                specification: str
                    One of ["1", "2", "3", "4", "5", "6", "7"]
                installation: str
                    One of ["A", "B", "C", "D", "E", "F", "G"]
            See Also:
                pilecore/lib/pile_types.json
        height_base : float, int
            height of pile base [m].
        alpha_s_sand
            Alpha s factor for coarse layers used in the positive friction calculation [-].
        alpha_s_clay
            Alpha s factor for soft layers used in the positive friction calculation [-].
        alpha_p
            Alpha p factor used in pile tip resistance calculation [-].
        beta_p
            The beta-factor 𝛽_𝑝 to account for the shape of the pile tip according to NEN9997-1 Fig 7.i.
        pile_tip_factor_s
            Factor s [-] used in pile tip resistance calculation as per NEN 9997-1 7.6.2.3 (h).
        settlement_curve
            Settlement lines for figures 7.n and 7.o of NEN-9997-1
        elastic_modulus : float
            Modulus of elasticity of the pile [MPa].
        negative_fr_delta_factor : float
            factor * φ = δ. This parameter is multiplied with phi to get the delta
            parameter used in negative friction calculation according to NEN-9997-1 7.3.2.2 (e).
            Typically values are 1.0 for piles cast in place, and 0.75 for other pile types.
        adhesion
            Adhesion value [kPa], for if the pile shaft has undergone a special treatment.
            Examples:
                - adhesion = 50 kN/m2 for synthetic coating
                - adhesion = 20 kN/m2 for bentonite
                - adhesion = 10 kN/m2 for bitumen coating
            See 7.3.2.2(d) of NEN 9997-1 for examples.
        is_low_vibrating
            Determines wether the pile has an installation type with low vibration.
        is_auger
            Determines wether the pile the pile is an auger pile or not.
        name
            The name of the pile instance.
        """
        self._name = name
        self._alpha_s_clay = alpha_s_clay
        self._adhesion = adhesion
        self._pile_tip_factor_s = pile_tip_factor_s
        self._pile_type_specification = pile_type_specification
        self._pile_type = pile_type_specification["pile_type"]
        self._installation = pile_type_specification["installation"]
        self._specification = pile_type_specification["specification"]

        self._alpha_s_sand = alpha_s_sand
        self._alpha_p = alpha_p
        self._beta_p = beta_p
        self._settlement_curve = settlement_curve
        self._elastic_modulus = elastic_modulus
        self._negative_fr_delta_factor = negative_fr_delta_factor
        self._is_low_vibrating = is_low_vibrating
        self._is_auger = is_auger

        self._height_base = height_base

    @property
    def name(self) -> str | None:
        """
        Pile name (optional)
        """
        if self._name is not None:
            return str(self._name)
        else:
            return None

    @property
    def alpha_s_clay(self) -> str | float:
        """
        Alpha s factor for soft layers used in the positive friction calculation [-].
        """
        if isinstance(self._alpha_s_clay, str):
            return self._alpha_s_clay
        else:
            return float(self._alpha_s_clay)

    @property
    def alpha_s_sand(self) -> float:
        """
        Alpha s factor for coarse layers used in the positive friction calculation [-].
        """
        return float(self._alpha_s_sand)

    @property
    def alpha_p(self) -> float:
        """
        Alpha p factor used in pile tip resistance calculation [-].
        """
        return float(self._alpha_p)

    @property
    def elastic_modulus(self) -> float:
        """
        Modulus of elasticity of the pile [MPa].
        """
        return float(self._elastic_modulus)

    @property
    def negative_fr_delta_factor(self) -> float:
        """
        factor * φ = δ. This parameter will be multiplied with phi to get the delta
        parameter used in negative friction calculation according to NEN-9997-1 7.3.2.2 (e).
        """
        return float(self._negative_fr_delta_factor)

    @property
    def is_low_vibrating(self) -> bool:
        """
        Determines wether the pile has an installation type with low vibration.
        """
        return bool(self._is_low_vibrating)

    @property
    def is_auger(self) -> bool:
        """
        Determines wether the pile the pile is an auger pile or not.
        """
        return bool(self._is_auger)

    @property
    def adhesion(self) -> float:
        """
        Adhesion value [kPa], used if the pile shaft has undergone a special treatment
        """
        return float(self._adhesion)

    @property
    def shape(self) -> str:
        """
        The shape of the pile (round or rect).
        """
        return str(self._shape)

    @property
    def pile_type(self) -> str:
        """
        The pile type of the pile in the configured locale setting.
        """
        return str(self._pile_type)

    @property
    def installation(self) -> str:
        """
        The installation of the pile.
        """
        return str(self._installation)

    @property
    def specification(self) -> str:
        """
        The specification of the pile.
        """
        return str(self._specification)

    @property
    def height_base(self) -> float:
        """
        Height of the pile base [m].
        """
        return float(self._height_base)

    @property
    def settlement_curve(self) -> int:
        """
        The settlement curve number.
        """
        return int(self._settlement_curve)

    @property
    def pile_tip_factor_s(self) -> float:
        """
        Factor s [-], used in pile tip resistance calculation as per NEN 9997-1 7.6.2.3 (h).
        """
        return float(self._pile_tip_factor_s)

    @property
    def pile_type_specification(self) -> Dict[str, str]:
        """
        A Dictionary with default pile-type definition.
        """
        return self._pile_type_specification

    @property
    @abstractmethod
    def circumference_pile_shaft(self) -> float:
        """
        Circumference of the pile shaft [m].
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def circumference_pile_base(self) -> float:
        """
        Circumference of the pile base [m].
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def area_pile_tip(self) -> float:
        """
        Cross-sectional area of the pile tip [m^2].
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def equiv_base_diameter(self) -> float:
        """
        Equivalent base diameter [m].
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def equiv_shaft_diameter(self) -> float:
        """
        Equivalent shaft diameter [m].
        """
        raise NotImplementedError

    @property
    def beta_p(self) -> float:
        """
        The beta-p factor 𝛽_𝑝 to account for the shape of the pile tip according to NEN9997-1 Fig 7.i.
        """
        return float(self._beta_p)

    @abstractmethod
    def get_circum_vs_depth(
        self,
        pile_tip_level: float | int,
        pile_head_level: float | int,
        depth: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns an array with pile circumferences for the depths in the depth parameter.

        Parameters
        ----------
        pile_tip_level
            pile tip level in the depth array.
        pile_head_level
            pile head level in the depth array.
        depth : numpy.ndarray
            Array with depths below surface [m].
        """
        raise NotImplementedError

    @abstractmethod
    def get_area_vs_depth(
        self,
        pile_tip_level: float | int,
        pile_head_level: float | int,
        depth: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns an array with cross-sectional areas for the depths in the depth parameter.

        Parameters
        ----------
        pile_tip_level
            pile tip level in the depth array.
        pile_head_level
            pile head level in the depth array.
        depth : numpy.ndarray
            Array with depths below surface [m].
        """
        raise NotImplementedError


class RoundPileProperties(PileProperties):
    """
    A class with round pile properties
    """

    _shape = "round"

    def __init__(
        self,
        pile_type_specification: Dict[str, str],
        diameter_base: float | int,
        diameter_shaft: float | int,
        height_base: float | int,
        alpha_s_sand: float,
        alpha_s_clay: float | str,
        alpha_p: float,
        beta_p: float,
        pile_tip_factor_s: float,
        settlement_curve: int,
        elastic_modulus: float | int,
        negative_fr_delta_factor: float | int,
        adhesion: float | int,
        is_low_vibrating: bool,
        is_auger: bool,
        name: str | None = None,
    ):
        """
        Parameters
        ----------
        pile_type_specification
            Keys
                pile_type: str
                    One of ["concrete", "steel", "micro", "wood"]
                specification: str
                    One of ["1", "2", "3", "4", "5", "6", "7"]
                installation: str
                    One of ["A", "B", "C", "D", "E", "F", "G"]
            See Also:
                pilecore/lib/pile_types.json
        diameter_base : float, int
            Diameter of pile base [m].
        diameter_shaft : float, int
            Diameter of pile shaft [m].
        height_base : float, int
            height of pile base [m].
        alpha_s_sand
            Alpha s factor for coarse layers used in the positive friction calculation [-].
        alpha_s_clay
            Alpha s factor for soft layers used in the positive friction calculation [-].
        alpha_p
            Alpha p factor used in pile tip resistance calculation [-].
        beta_p
            The beta-factor 𝛽_𝑝 to account for the shape of the pile tip according to NEN9997-1 Fig 7.i.
        pile_tip_factor_s
            Factor s [-] used in pile tip resistance calculation as per NEN 9997-1 7.6.2.3 (h).
        settlement_curve
            Settlement lines for figures 7.n and 7.o of NEN-9997-1
        elastic_modulus : float
            Modulus of elasticity of the pile [MPa].
        negative_fr_delta_factor : float
            factor * φ = δ. This parameter is multiplied with phi to get the delta
            parameter used in negative friction calculation according to NEN-9997-1 7.3.2.2 (e).
            Typically values are 1.0 for piles cast in place, and 0.75 for other pile types.
        adhesion
            Adhesion value [kPa], for if the pile shaft has undergone a special treatment.
            Examples:
                - adhesion = 50 kN/m2 for synthetic coating
                - adhesion = 20 kN/m2 for bentonite
                - adhesion = 10 kN/m2 for bitumen coating

            See 7.3.2.2(d) of NEN 9997-1 for examples.
        is_low_vibrating : bool
            Determines wether the pile has an installation type with low vibration.
        is_auger : bool
            Determines wether the pile the pile is an auger pile or not.
        name
            The name of the pile instance.
        """
        super().__init__(
            pile_type_specification=pile_type_specification,
            pile_tip_factor_s=pile_tip_factor_s,
            alpha_s_sand=alpha_s_sand,
            alpha_s_clay=alpha_s_clay,
            alpha_p=alpha_p,
            beta_p=beta_p,
            elastic_modulus=elastic_modulus,
            adhesion=adhesion,
            settlement_curve=settlement_curve,
            negative_fr_delta_factor=negative_fr_delta_factor,
            is_low_vibrating=is_low_vibrating,
            is_auger=is_auger,
            height_base=height_base,
            name=name,
        )
        self._diameter_shaft = diameter_shaft
        self._diameter_base = diameter_base

    @property
    def diameter_base(self) -> float:
        """
        Diameter of the pile tip/base [m].
        """
        return float(self._diameter_base)

    @property
    def diameter_shaft(self) -> float:
        """
        Diameter of the pile shaft [m].
        """
        return float(self._diameter_shaft)

    @property
    def circumference_pile_shaft(self) -> float:
        """
        Circumference of the pile shaft [m].
        """
        return float(math.pi * self.diameter_shaft)

    @property
    def circumference_pile_base(self) -> float:
        """
        Circumference of the pile tip/base [m].
        """
        return float(math.pi * self.diameter_base)

    @property
    def area_pile_tip(self) -> float:
        """
        Cross-sectional area of the pile tip/base [m].
        """
        return float(0.25 * math.pi * self.diameter_base**2)

    @property
    def area_pile_shaft(self) -> float:
        """
        Cross-sectional area of the pile shaft [m].
        """
        return float(0.25 * math.pi * self.diameter_shaft**2)

    @property
    def equiv_base_diameter(self) -> float:
        """
        Equivalent base diameter [m]. Equal to base diameter for round piles.
        """
        return float(self.diameter_base)

    @property
    def equiv_shaft_diameter(self) -> float:
        """
        Equivalent shaft diameter [m]. Equal to shaft diameter for round piles.
        """
        return float(self.diameter_shaft)

    def get_diameter_vs_depth(
        self,
        pile_tip_level: float | int,
        pile_head_level: float | int,
        depth: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns pile diameters for given input depths.

        Parameters
        ----------
        pile_tip_level : float
            pile tip level in the depth array.
        pile_head_level : float
            pile head level in the depth array.
        depth : np.array
            Array with depths below surface [m].

        Returns
        -------
        np.array
            Array with pile diameters for the depths in the depth parameter.
        """
        diameter_vs_depth = np.zeros_like(depth)
        diameter_vs_depth[
            (depth >= pile_head_level) & (depth < pile_tip_level - self.height_base)
        ] = self.diameter_shaft
        diameter_vs_depth[
            (depth >= pile_tip_level - self.height_base) & (depth <= pile_tip_level)
        ] = self.diameter_base
        return diameter_vs_depth

    def get_circum_vs_depth(
        self,
        pile_tip_level: float | int,
        pile_head_level: float | int,
        depth: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns pile circumferences for given input depths.

        Parameters
        ----------
        pile_tip_level : float
            pile tip level in the depth array.
        pile_head_level : float
            pile head level in the depth array.
        depth : np.array
            Array with depths below surface [m].

        Returns
        -------
        np.array
            Array with pile circumferences for the depths in the depth parameter.
        """
        return (
            self.get_diameter_vs_depth(
                pile_tip_level=pile_tip_level,
                pile_head_level=pile_head_level,
                depth=depth,
            )
            * math.pi
        )

    def get_area_vs_depth(
        self,
        pile_tip_level: float | int,
        pile_head_level: float | int,
        depth: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns cross-sectional areas of the pile for given input depths.

        Parameters
        ----------
        pile_tip_level : float
            pile tip level in the depth array.
        pile_head_level : float
            pile head level in the depth array.
        depth : np.array
            Array with depths below surface [m].

        Returns
        -------
        np.array
            Array with cross-sectional areas for the depths in the depth parameter.
        """
        return (
            self.get_diameter_vs_depth(
                pile_tip_level=pile_tip_level,
                pile_head_level=pile_head_level,
                depth=depth,
            )
            / 2
        ) ** 2 * math.pi


class RectPileProperties(PileProperties):
    """
    A class with rectangular pile properties
    """

    _shape = "rect"

    def __init__(
        self,
        pile_type_specification: Dict[str, str],
        width_base_large: float | int,
        width_base_small: float | int,
        width_shaft_large: float | int,
        width_shaft_small: float | int,
        height_base: float | int,
        alpha_s_sand: float,
        alpha_s_clay: float | str,
        alpha_p: float,
        beta_p: float,
        pile_tip_factor_s: float | int,
        settlement_curve: int,
        elastic_modulus: float | int,
        negative_fr_delta_factor: float | int,
        adhesion: float | int,
        is_low_vibrating: bool,
        is_auger: bool,
        name: str | None = None,
    ):
        """
        Parameters
        ----------
        pile_type_specification
            Keys
                pile_type: str
                    One of ["concrete", "steel", "micro", "wood"]
                specification: str
                    One of ["1", "2", "3", "4", "5", "6", "7"]
                installation: str
                    One of ["A", "B", "C", "D", "E", "F", "G"]
            See Also:
                pilecore/lib/pile_types.json
        width_base_large: Union[float, int]
            Largest dimension of the pile base [m].
        width_base_small: Union[float, int]
            Smallest dimension of the pile base [m].
        width_shaft_large: Union[float, int]
            Largest dimension of the pile shaft [m].
        width_shaft_small: Union[float, int]
            Smallest dimension of the pile shaft [m].
        height_base: Union[float, int]
            Height of pile base [m].
        alpha_s_sand
            Alpha s factor for coarse layers used in the positive friction calculation [-].
        alpha_s_clay
            Alpha s factor for soft layers used in the positive friction calculation [-].
        alpha_p
            Alpha p factor used in pile tip resistance calculation [-].
        beta_p
            The beta-factor 𝛽_𝑝 to account for the shape of the pile tip according to NEN9997-1 Fig 7.i.
        pile_tip_factor_s
            Factor s [-] used in pile tip resistance calculation as per NEN 9997-1 7.6.2.3 (h).
        settlement_curve
            Settlement lines for figures 7.n and 7.o of NEN-9997-1
        elastic_modulus
            Modulus of elasticity of the pile [MPa].
        negative_fr_delta_factor
            factor * φ = δ. This parameter is multiplied with phi to get the delta
            parameter used in negative friction calculation according to NEN-9997-1 7.3.2.2 (e).
            Typically values are 1.0 for piles cast in place, and 0.75 for other pile types.
        adhesion
            Adhesion value [kPa], for if the pile shaft has undergone a special treatment.
            Examples:
                - adhesion = 50 kN/m2 for synthetic coating
                - adhesion = 20 kN/m2 for bentonite
                - adhesion = 10 kN/m2 for bitumen coating

            See 7.3.2.2(d) of NEN 9997-1 for examples.
        is_low_vibrating
            Determines wether the pile has an installation type with low vibration.
        is_auger
            Determines wether the pile the pile is an auger pile or not.
        name
            The name of the pile instance.
        """
        super().__init__(
            pile_type_specification=pile_type_specification,
            alpha_s_sand=alpha_s_sand,
            alpha_s_clay=alpha_s_clay,
            alpha_p=alpha_p,
            beta_p=beta_p,
            pile_tip_factor_s=pile_tip_factor_s,
            settlement_curve=settlement_curve,
            elastic_modulus=elastic_modulus,
            adhesion=adhesion,
            negative_fr_delta_factor=negative_fr_delta_factor,
            is_low_vibrating=is_low_vibrating,
            is_auger=is_auger,
            height_base=height_base,
            name=name,
        )
        self._width_base_large = width_base_large
        self._width_base_small = width_base_small
        self._width_shaft_large = width_shaft_large
        self._width_shaft_small = width_shaft_small

    @property
    def width_base_large(self) -> float:
        """
        Largest dimension of the pile base [m].
        """
        return self._width_base_large

    @property
    def width_base_small(self) -> float:
        """
        Smallest dimension of the pile base [m].
        """
        return self._width_base_small

    @property
    def width_shaft_large(self) -> float:
        """
        Largest dimension of the pile shaft [m].
        """
        return self._width_shaft_large

    @property
    def width_shaft_small(self) -> float:
        """
        Smallest dimension of the pile shaft [m].
        """
        return self._width_shaft_small

    @property
    def circumference_pile_shaft(self) -> float:
        """
        Circumference of the pile shaft [m].
        """
        return float(2 * self.width_shaft_large + 2 * self.width_shaft_small)

    @property
    def circumference_pile_base(self) -> float:
        """
        Circumference of the pile tip/base [m].
        """
        return float(2 * self.width_base_large + 2 * self.width_base_small)

    @property
    def area_pile_tip(self) -> float:
        """
        Cross-sectional area of the pile tip/base [m].
        """
        return float(self.width_base_large * self.width_base_small)

    @property
    def area_pile_shaft(self) -> float:
        """
        Cross-sectional area of the pile shaft [m].
        """
        return float(self.width_shaft_large * self.width_shaft_small)

    @property
    def equiv_base_diameter(self) -> float:
        """
        Equivalent base diameter [m] according to NEN-9997-1+C2_2017
        paragraphs 1.5.2.106a and 7.6.2.3.(10)(e).

        Specifically: returns self.width_base_small
        if self.width_base_large > (1,5 * self.width_base_small)
        """
        a_min = self.width_base_small
        b_max = self.width_base_large
        if b_max > (1.5 * a_min):
            return a_min
        return float(1.13 * a_min * math.sqrt(b_max / a_min))

    @property
    def equiv_shaft_diameter(self) -> float:
        """
        Equivalent base diameter [m] according to NEN-9997-1+C2_2017
        paragraphs 1.5.2.106b and 7.6.2.3.(10)(e).

        Specifically: returns self.width_shaft_small
        if self.width_shaft_large > (1,5 * self.width_shaft_small)
        """
        a_min = self.width_shaft_small
        b_max = self.width_shaft_large
        if b_max > (1.5 * a_min):
            return a_min
        return float(1.13 * a_min * math.sqrt(b_max / a_min))

    def get_circum_vs_depth(
        self,
        pile_tip_level: float | int,
        pile_head_level: float | int,
        depth: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns pile circumferences for given input depths.

        Parameters
        ----------
        pile_tip_level : float
            pile tip level in the depth array.
        pile_head_level : float
            pile head level in the depth array.
        depth : np.array
            Array with depths below surface [m].

        Returns
        -------
        np.array
            Array with pile circumferences for the depths in the depth parameter.
        """
        circum_vs_depth = np.zeros_like(depth)
        circum_vs_depth[
            (depth >= pile_head_level) & (depth < pile_tip_level - self.height_base)
        ] = self.circumference_pile_shaft
        circum_vs_depth[
            (depth >= pile_tip_level - self.height_base) & (depth <= pile_tip_level)
        ] = self.circumference_pile_base
        return circum_vs_depth

    def get_area_vs_depth(
        self,
        pile_tip_level: float | int,
        pile_head_level: float | int,
        depth: NDArray[np.floating],
    ) -> NDArray[np.floating]:
        """
        Returns cross-sectional areas of the pile for given input depths.

        Parameters
        ----------
        pile_tip_level : float
            pile tip level in the depth array.
        pile_head_level : float
            pile head level in the depth array.
        depth : np.array
            Array with depths below surface [m].

        Returns
        -------
        np.array
            Array with cross-sectional areas for the depths in the depth parameter.
        """
        area_vs_depth = np.zeros_like(depth)
        area_vs_depth[
            (depth >= pile_head_level) & (depth <= pile_tip_level - self.height_base)
        ] = self.area_pile_shaft
        area_vs_depth[
            (depth > pile_tip_level - self.height_base) & (depth <= pile_tip_level)
        ] = self.area_pile_tip
        return area_vs_depth


def create_pile_properties_from_api_response(response_dict: dict) -> PileProperties:
    shape = response_dict["type"]
    props = response_dict["props"]

    kwargs = dict(
        height_base=props["height_base"],
        pile_type_specification=props["pile_type_specification"],
        alpha_s_sand=props["alpha_s_sand"],
        alpha_s_clay=props["alpha_s_clay"],
        alpha_p=props["alpha_p"],
        beta_p=props["beta_p"],
        pile_tip_factor_s=props["pile_tip_factor_s"],
        settlement_curve=props["settlement_curve"],
        elastic_modulus=props["elastic_modulus"],
        negative_fr_delta_factor=props["negative_fr_delta_factor"],
        adhesion=props["adhesion"],
        is_low_vibrating=props["is_low_vibrating"],
        is_auger=props["is_auger"],
    )

    if "name" in props.keys():
        kwargs.update(name=props["name"])

    if shape == "round":
        return RoundPileProperties(
            diameter_base=props["diameter_base"],
            diameter_shaft=props["diameter_shaft"],
            **kwargs,
        )
    elif shape == "rect":
        return RectPileProperties(
            width_base_large=props["width_base_large"],
            width_base_small=props["width_base_small"],
            width_shaft_large=props["width_shaft_large"],
            width_shaft_small=props["width_shaft_small"],
            **kwargs,
        )
    else:
        raise ValueError(f"Received unknown pile-type: {shape}.")
