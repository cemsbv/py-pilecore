from __future__ import annotations

from typing import Dict


class PileType:
    """The PileType class represents the type of a pile."""

    def __init__(
        self,
        standard_pile: Dict[str, str | int] | None = None,
        alpha_s_sand: float | None = None,
        alpha_s_clay: float | None = None,
        alpha_p: float | None = None,
        alpha_t_sand: float | None = None,
        settlement_curve: int | None = None,
        negative_fr_delta_factor: float | None = None,
        adhesion: float | None = None,
        is_low_vibrating: bool | None = None,
        is_auger: bool | None = None,
    ):
        """
        Represents the type of a pile.

        Parameters:
        -----------
        standard_pile : dict, optional
            The standard pile definition of the pile type (if applicable), by default None.
        alpha_s_sand : float, optional
            The alpha_s_sand value of the pile type, by default None.
        alpha_s_clay : float, optional
            The alpha_s_clay value of the pile type, by default None.
        alpha_p : float, optional
            The alpha_p value of the pile type, by default None.
        alpha_t_sand : float, optional
            The alpha_t_sand value of the pile type, by default None.
        settlement_curve : int, optional
            The settlement curve of the pile type, by default None.
        negative_fr_delta_factor : float, optional
            The negative_fr_delta_factor value of the pile type, by default None.
        adhesion : float, optional
            The adhesion value of the pile type, by default None.
        is_low_vibrating : bool, optional
            The is_low_vibrating value of the pile type, by default None.
        is_auger : bool, optional
            The is_auger value of the pile type, by default None.
        """
        self._standard_pile = standard_pile
        self._alpha_s_sand = alpha_s_sand
        self._alpha_s_clay = alpha_s_clay
        self._alpha_p = alpha_p
        self._alpha_t_sand = alpha_t_sand
        self._settlement_curve = settlement_curve
        self._negative_fr_delta_factor = negative_fr_delta_factor
        self._adhesion = adhesion
        self._is_low_vibrating = is_low_vibrating
        self._is_auger = is_auger

    @classmethod
    def from_api_response(cls, pile_type: dict) -> PileType:
        """
        Instantiates a PileType from a pile type object in the API response payload.

        Parameters:
        -----------
        pile_type: dict
            A dictionary that is retrieved from the API response payload at "/pile_properties/pile_type".

        Returns:
        --------
        PileType
            A pile type.
        """
        return cls(
            standard_pile=pile_type.get("standard_pile"),
            alpha_s_sand=pile_type["properties"]["alpha_s_sand"],
            alpha_s_clay=pile_type["properties"]["alpha_s_clay"],
            alpha_p=pile_type["properties"]["alpha_p"],
            alpha_t_sand=pile_type["properties"]["alpha_t_sand"],
            settlement_curve=pile_type["properties"]["settlement_curve"],
            negative_fr_delta_factor=pile_type["properties"][
                "negative_fr_delta_factor"
            ],
            adhesion=pile_type["properties"]["adhesion"],
            is_low_vibrating=pile_type["properties"]["is_low_vibrating"],
            is_auger=pile_type["properties"]["is_auger"],
        )

    @property
    def standard_pile(self) -> Dict[str, str | int] | None:
        """The standard pile definition of the pile type (if applicable)"""
        return self._standard_pile

    @property
    def alpha_s_sand(self) -> float | None:
        """The alpha_s_sand value of the pile type"""
        return self._alpha_s_sand

    @property
    def alpha_s_clay(self) -> float | None:
        """The alpha_s_clay value of the pile type"""
        return self._alpha_s_clay

    @property
    def alpha_p(self) -> float | None:
        """The alpha_p value of the pile type"""
        return self._alpha_p

    @property
    def alpha_t_sand(self) -> float | None:
        """The alpha_t_sand value of the pile type"""
        return self._alpha_t_sand

    @property
    def settlement_curve(self) -> int | None:
        """The settlement curve of the pile type"""
        return self._settlement_curve

    @property
    def negative_fr_delta_factor(self) -> float | None:
        """The negative_fr_delta_factor value of the pile type"""
        return self._negative_fr_delta_factor

    @property
    def adhesion(self) -> float | None:
        """The adhesion value of the pile type"""
        return self._adhesion

    @property
    def is_low_vibrating(self) -> bool | None:
        """The is_low_vibrating value of the pile type"""
        return self._is_low_vibrating

    @property
    def is_auger(self) -> bool | None:
        """The is_auger value of the pile type"""
        return self._is_auger

    def serialize_payload(self) -> Dict[str, str | dict]:
        """
        Serialize the pile type to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the standard pile (if set), alpha_s_sand, alpha_s_clay, alpha_p,
            alpha_t_sand, settlement curve, negative_fr_delta_factor, adhesion, is_low_vibrating, and is_auger.
        """
        payload: Dict[str, str | dict] = {}

        if self.standard_pile is not None:
            payload["standard_pile"] = {
                "main_type": str(self.standard_pile["main_type"]),
                "specification": str(self.standard_pile["specification"]),
            }
            if (
                "installation" in self.standard_pile
                and self.standard_pile["installation"] is not None
            ):
                payload["standard_pile"]["installation"] = str(  # type: ignore
                    self.standard_pile["installation"]
                )

        custom_type_properties: Dict[str, float | bool] = {}

        if self.alpha_s_sand is not None:
            custom_type_properties["alpha_s_sand"] = self.alpha_s_sand

        if self.alpha_s_clay is not None:
            custom_type_properties["alpha_s_clay"] = self.alpha_s_clay

        if self.alpha_p is not None:
            custom_type_properties["alpha_p"] = self.alpha_p

        if self.alpha_t_sand is not None:
            custom_type_properties["alpha_t_sand"] = self.alpha_t_sand

        if self.settlement_curve is not None:
            custom_type_properties["settlement_curve"] = self.settlement_curve

        if self.negative_fr_delta_factor is not None:
            custom_type_properties[
                "negative_fr_delta_factor"
            ] = self.negative_fr_delta_factor

        if self.adhesion is not None:
            custom_type_properties["adhesion"] = self.adhesion

        if self.is_low_vibrating is not None:
            custom_type_properties["is_low_vibrating"] = self.is_low_vibrating

        if self.is_auger is not None:
            custom_type_properties["is_auger"] = self.is_auger

        if len(custom_type_properties.keys()) > 0:
            payload["custom_properties"] = custom_type_properties

        return payload
