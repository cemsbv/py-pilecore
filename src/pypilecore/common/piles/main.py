from __future__ import annotations

from typing import Dict, List, Literal

from pypilecore.common.piles.geometry import PileGeometry
from pypilecore.common.piles.geometry.components import (
    PrimaryPileComponentDimension,
    RectPileGeometryComponent,
    RoundPileGeometryComponent,
)
from pypilecore.common.piles.geometry.materials import MATERIALS, PileMaterial
from pypilecore.common.piles.type import PileType


class PileProperties:
    """The PileProperties class represents all properties of a pile."""

    def __init__(
        self, geometry: PileGeometry, pile_type: PileType, name: str | None = None
    ):
        """
        Represents all properties of a pile.

        Parameters:
        -----------
        geometry: PileGeometry
            The geometry of the pile.
        pile_type: PileType
            The type of the pile.
        name: str, optional
            The name of the pile, by default None.
        """
        self._geometry = geometry
        self._pile_type = pile_type
        self._name = name

    @classmethod
    def from_api_response(cls, pile_properties: dict) -> PileProperties:
        """
        Instantiates a PileProperties from a response dictionary.

        Parameters:
        -----------
        pile_properties: dict
            A dictionary that is retrieved from the API response payload at "/pile_properties".

        Returns:
        --------
        PileProperties
            A pile properties object.
        """
        return cls(
            geometry=PileGeometry.from_api_response(pile_properties["geometry"]),
            pile_type=PileType.from_api_response(pile_properties["pile_type"]),
            name=pile_properties.get("name"),
        )

    @property
    def geometry(self) -> PileGeometry:
        """The geometry of the pile."""
        return self._geometry

    @property
    def pile_type(self) -> PileType:
        """The type of the pile."""
        return self._pile_type

    @property
    def name(self) -> str | None:
        """The name of the pile."""
        if self._name is not None:
            return str(self._name)
        return None

    def serialize_payload(self) -> Dict[str, dict | str]:
        """
        Serialize the pile properties to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the geometry, pile type, and name (if set).
        """
        payload: Dict[str, dict | str] = {
            "geometry": self.geometry.serialize_payload(),
            "pile_type": self.pile_type.serialize_payload(),
        }

        if self.name is not None:
            payload["name"] = self.name

        return payload


def create_basic_pile(
    pile_shape: Literal["round", "rect", "rectangle"],
    pile_name: str | None = None,
    main_type: Literal["concrete", "steel", "wood", "anchor"] | None = None,
    specification: str | int | float | None = None,
    installation: str | None = None,
    height_base: float | None = None,
    core_secondary_dimension: float | None = None,
    core_tertiary_dimension: float | None = None,
    base_secondary_dimension: float | None = None,
    base_tertiary_dimension: float | None = None,
    core_diameter: float | None = None,
    base_diameter: float | None = None,
    pile_material: Literal["concrete", "steel", "wood", "grout", "grout_extorted"]
    | None = None,
    custom_material: dict | None = None,
    settlement_curve: int | None = None,
    adhesion: float | None = None,
    alpha_p: float | None = None,
    alpha_s_clay: float | None = None,
    alpha_s_sand: float | None = None,
    beta_p: float | None = None,
    alpha_t_clay: float | None = None,
    alpha_t_sand: float | None = None,
    pile_tip_factor_s: float | None = None,
    is_auger: bool | None = None,
    is_low_vibrating: bool | None = None,
    negative_fr_delta_factor: float | None = None,
    qc_z_a_lesser_1m: float | None = None,
    qc_z_a_greater_1m: float | None = None,
    qb_max_limit: float | None = None,
    chamfered: float | None = None,
) -> PileProperties:
    """
    Create a basic pile with the provided parameters.
    A "basic" pile is a pile with a basic geometry, containing at most 2 components,
    namely a core component and an optional shell/widened-base component.

    Parameters
    ----------
    pile_shape :
        The shape of the pile.
        Both "rect" and "rectangle" are accepted for rectangular piles.
    pile_name :
        The name of the pile, by default None.
    main_type :
        The main type of the standard pile type definition, by default None.
    specification :
        The specification of the standard pile type definition, by default None.
        Required if `main_type` is provided.
    installation :
        The installation of the standard pile type definition, by default None.
    height_base :
        The height [m] of the base component, by default None.
        Required if base dimensions are provided.
        Note: When standard is CUR236, `height_base` should be None, making the
        shaft dimensions equal to the base dimensions.
    core_secondary_dimension :
        The largest dimension [m] of the rectangular core component's cross-section, by default None.
        Required for rectangular piles.
    core_tertiary_dimension :
        The smallest dimension [m] of the rectangular core component's cross-section, by default None.
        If None and pile shape is rectangular, `core_tertiary_dimension` is used resulting in a square core.
    base_secondary_dimension :
        The largest dimension [m] of the rectangular base/shell component's cross-section, by default None.
        If None and pile shape is rectangular, then the base has the same dimensions as the core.
        Requires `height_base` to be provided.
    base_tertiary_dimension :
        The smallest dimension [m] of the rectangular base/shell component's cross-section, by default None.
        If None and pile shape is rectangular, then:
            - If `base_secondary_dimension` is None, then the base has the same dimensions as the core.
            - If `base_secondary_dimension` is provided, then `base_tertiary_dimension` is used resulting
            in a square base.
        Requires `height_base` to be provided.
    core_diameter :
        The diameter [m] of the round core component's cross-section, by default None.
        Required for round piles.
    base_diameter :
        The diameter [m] of the round base/shell component's cross-section, by default None.
        If None and pile shape is round, then the base has the same diameter as the core.
        Requires `height_base` to be provided.
    pile_material :
        The material of the pile, by default None.
        It is ignored if `custom_material` is provided.
        Otherwise:
            - If None, it is inferred from the standard pile.
            - Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type and no custom material were specified.
    custom_material :
        A custom material for the pile, by default None.
        If provided, it is used even if a standard pile was selected.
        Required keys and value types:
            - "name": str
            - "elastic_modulus: float
                Unit: [MPa]
            - "color": str
                Hexadecimal color
        Example: {
            "name": "custom_material",
            "elastic_modulus": 15e3,
            "color": "#ff0000",
        }
    settlement_curve :
        The settlement curve of the pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    adhesion :
        The adhesion value [kPa] of the pile, by default None.
        Use it if the pile shaft has undergone a special treatment.
        If None, then adhesion is disregarded.
        Examples:
            - adhesion = 50 kPa for synthetic coating
            - adhesion = 20 kPa for bentonite
            - adhesion = 10 kPa for bitumen coating
    alpha_p :
        The alpha_p of the pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    alpha_s_clay :
        The alpha_s_clay of the pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    alpha_s_sand :
        The alpha_s_sand of the pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    alpha_t_clay :
        The alpha_t_clay of the pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    alpha_t_sand :
        The alpha_t_sand of the pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    beta_p :
        The beta_p of the pile, by default None.
        If None, the value is computed from the pile dimensions.
    pile_tip_factor_s :
        The pile tip factor s of the pile, by default None.
        If None, the value is computed from the pile dimensions and soil properties.
    is_auger :
        Whether the pile is an auger pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    is_low_vibrating :
        Whether the pile is low vibrating, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    negative_fr_delta_factor :
        The negative friction delta factor of the pile, by default None.
        If None, it is inferred from the standard pile.
        Overwrites the value of the standard pile if provided together with a standard pile.
        Required if no standard pile type was specified.
    qc_z_a_lesser_1m :
        Maximum cone resistance qc value [MPa] allowed for layers with thickness < 1m in the calculation of positive skin friction resistance.
        It must be less or equal to `qc_z_a_greater_1m`.
        If None, then 12 MPa is used.
        Default: None.
    qc_z_a_greater_1m :
        Maximum cone resistance qc value [MPa] allowed for layers with thickness >= 1m in the calculation of positive skin friction resistance.
        It must be greater or equal to `qc_z_a_lesser_1m`.
        If None, then 15 MPa is used.
        Default: None.
    qb_max_limit :
        Maximum value allowed for the pile tip resistance qb_max [MPa].
        Note that is value will be used as a limit for qb_max unless use_almere_rules is true and a higher value than 12 MPa is specified.
        If None, then 15 MPa is used.
        Default: None.
    chamfered :
        The chamfered value of the pile type, by default None.
        Required if no standard pile type was specified.

    Returns
    -------
    PileProperties
        The pile properties object.
    """
    materials = [
        PileMaterial(**material_value) for material_value in MATERIALS.values()  # type: ignore
    ]

    if custom_material is not None:
        materials = [PileMaterial(**custom_material)]

    if pile_shape == "round":
        if core_diameter is None:
            raise ValueError("`core_diameter` must be provided for a round pile.")

        components: List[RoundPileGeometryComponent | RectPileGeometryComponent] = [
            RoundPileGeometryComponent(
                diameter=core_diameter,
                primary_dimension=PrimaryPileComponentDimension(
                    length=None,
                ),
                material=pile_material,
            )
        ]

        if base_diameter is not None:
            components.append(
                RoundPileGeometryComponent(
                    diameter=base_diameter,
                    primary_dimension=PrimaryPileComponentDimension(
                        length=height_base,
                    ),
                    material=pile_material,
                )
            )

    elif pile_shape in ["rect", "rectangle"]:
        if core_secondary_dimension is None:
            raise ValueError(
                "`core_secondary_dimension` must be provided for a rectangular pile."
            )

        components = [
            RectPileGeometryComponent(
                primary_dimension=PrimaryPileComponentDimension(length=None),
                secondary_dimension=core_secondary_dimension,
                tertiary_dimension=core_tertiary_dimension,
                material=pile_material,
            )
        ]

        if base_secondary_dimension is not None:
            components.append(
                RectPileGeometryComponent(
                    secondary_dimension=base_secondary_dimension,
                    tertiary_dimension=base_tertiary_dimension,
                    primary_dimension=PrimaryPileComponentDimension(
                        length=height_base,
                    ),
                    material=pile_material,
                )
            )

    else:
        raise ValueError(f"Invalid pile shape: {pile_shape}")

    geometry = PileGeometry(
        components=components,
        materials=materials,
        pile_tip_factor_s=pile_tip_factor_s,
        beta_p=beta_p,
    )

    if main_type is not None:
        if specification is None:
            raise ValueError("Specification must be provided if main type is provided.")

        standard_pile: Dict[str, str | int] | None = {
            "main_type": main_type,
            "specification": int(specification),
        }

        if installation is not None:
            standard_pile["installation"] = installation  # type: ignore

    else:
        standard_pile = None

    pile_type = PileType(
        standard_pile=standard_pile,
        alpha_s_sand=alpha_s_sand,
        alpha_s_clay=alpha_s_clay,
        alpha_p=alpha_p,
        alpha_t_sand=alpha_t_sand,
        alpha_t_clay=alpha_t_clay,
        settlement_curve=settlement_curve,
        negative_fr_delta_factor=negative_fr_delta_factor,
        adhesion=adhesion,
        is_low_vibrating=is_low_vibrating,
        is_auger=is_auger,
        qc_z_a_lesser_1m=qc_z_a_lesser_1m,
        qc_z_a_greater_1m=qc_z_a_greater_1m,
        qb_max_limit=qb_max_limit,
        chamfered=chamfered,
    )

    return PileProperties(geometry=geometry, pile_type=pile_type, name=pile_name)
