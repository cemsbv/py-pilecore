from __future__ import annotations

from typing import Dict

MATERIALS = {
    "concrete": {"name": "concrete", "elastic_modulus": 20000, "color": "#525252"},
    "steel": {"name": "steel", "elastic_modulus": 195000, "color": "#E2E2E2"},
    "wood": {"name": "wood", "elastic_modulus": 3600, "color": "#BD7205"},
    "grout": {
        "name": "grout",
        "elastic_modulus": 15000,
        "yield_stress": 1.5,
        "color": "#8A8A8A",
    },
    "grout_extorted": {
        "name": "grout_extorted",
        "elastic_modulus": 20000,
        "yield_stress": 2,
        "color": "#8A8A8A",
    },
}


class Color:
    """The Color class represents an RGB color."""

    def __init__(self, red: int, green: int, blue: int):
        """
        Represents an RGB color.

        Parameters:
        -----------
        red : int
            The red component of the RGB color.
        green : int
            The green component of the RGB color.
        blue : int
            The blue component of the RGB color.
        """
        self.red = red
        self.green = green
        self.blue = blue

    @classmethod
    def from_hex(cls, hex: str) -> Color:
        """
        Instantiate a Color object from a hexadecimal color string.

        Parameters:
        -----------
        hex : str
            The hexadecimal representation of the RGB color.
            example: "#ff0000" for red.

        Returns:
        --------
        Color
            A Color object.
        """
        hex = hex.lstrip("#")
        return cls(
            red=int(hex[0:2], 16),
            green=int(hex[2:4], 16),
            blue=int(hex[4:6], 16),
        )

    @property
    def hex(self) -> str:
        """The hexadecimal representation of the RGB color. e.g. "#ff0000" for red."""
        return "#{:02x}{:02x}{:02x}".format(self.red, self.green, self.blue)

    def serialize_payload(self) -> Dict[str, int]:
        """Serialize the RGB color to a dictionary payload for the API."""
        return {"r": self.red, "g": self.green, "b": self.blue}


class PileMaterial:
    """The PileMaterial class represents a material that can be used in a pile geometry component."""

    def __init__(
        self,
        name: str,
        elastic_modulus: float,
        yield_stress: float | None = None,
        color: Color | str | Dict[str, int] | None = None,
    ):
        """
        Represents a material that can be used in a pile geometry component.

        Parameters:
        -----------
        name : str
            The name of the material.
        elastic_modulus : float
            The elastic modulus [MPa] of the material.
        yield_stress : float, optional
            The yield stress [MPa] of the material, by default None.
        color : Color or str or dict, optional
            The color of the material, by default None.
        """
        self._name = name
        self._elastic_modulus = elastic_modulus
        self._yield_stress = yield_stress
        if isinstance(color, str):
            color = Color.from_hex(hex=color)
        elif isinstance(color, dict):
            color = Color(
                red=color["r"],
                green=color["g"],
                blue=color["b"],
            )
        self._color = color

    @classmethod
    def from_api_response(cls, material: dict) -> PileMaterial:
        """
        Instantiates a PileMaterial from a material object in the API response payload.

        Args:
            material: A dictionary that is retrieved from the API response payload at "/pile_properties/geometry/materials/[i]".
        """
        if isinstance(material["color"], str):
            color = Color.from_hex(hex=material["color"])
        else:
            color = Color(
                red=material["color"]["r"],
                green=material["color"]["g"],
                blue=material["color"]["b"],
            )

        return cls(
            name=material["name"],
            elastic_modulus=material["elastic_modulus"],
            yield_stress=material.get("yield_stress"),
            color=color,
        )

    @property
    def name(self) -> str:
        """The name of the material"""
        return self._name

    @property
    def elastic_modulus(self) -> float:
        """The elastic modulus [MPa] of the material"""
        return self._elastic_modulus

    @property
    def yield_stress(self) -> float | None:
        """The yield stress [MPa] of the material"""
        return self._yield_stress

    @property
    def color(self) -> Color | Color | None:
        """The color of the material"""
        return self._color

    def serialize_payload(self) -> Dict[str, str | float | Dict[str, int]]:
        """
        Serialize the material to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the material's name, elastic modulus, and color.
        """
        payload: Dict[str, str | float | Dict[str, int]] = {
            "name": self.name,
            "elastic_modulus": self.elastic_modulus,
        }

        if self.color is not None:
            payload["color"] = self.color.serialize_payload()

        return payload
