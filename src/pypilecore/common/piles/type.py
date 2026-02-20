from __future__ import annotations

from typing import Dict


def _is_anchor_reference(reference: str) -> bool:
    """
    Infer whether the pile is an anchor from the pile type reference in the payload.
     - If the reference is one of ["AA1", "AA2", "AB1", "AB2", "AC", "AD", "AE"], it is an anchor.
     - For all other references, it is not an anchor.
    """
    return reference in ("AA1", "AA2", "AB1", "AB2", "AC", "AD", "AE")


class PileType:
    """The PileType class represents the type of a pile."""

    def __init__(
        self,
        reference: str | None = None,
        installation_method: str | None = None,
        is_prefab: bool | None = None,
        is_open_ended: bool | None = None,
        is_low_vibrating: bool | None = None,
        is_auger: bool | None = None,
        settlement_curve: int | None = None,
        alpha_s_sand: float | None = None,
        alpha_s_clay: dict | None = None,
        alpha_p: float | None = None,
        alpha_t_sand: float | None = None,
        alpha_t_clay: dict | None = None,
        negative_fr_delta_factor: float | None = None,
        adhesion: float | None = None,
        qc_z_a_lesser_1m: float | None = None,
        qc_z_a_greater_1m: float | None = None,
        qb_max_limit: float | None = None,
        chamfered: float | None = None,
    ):
        """
        Represents the type of a pile.

        Parameters:
        -----------
        reference : str, optional
            The standard pile definition of the pile type (if applicable), by default None.
        installation_method: str, optional
            The installation method of the pile, by default None.
        alpha_s_sand : float, optional
            The alpha_s_sand value of the pile type, by default None.
        alpha_s_clay : float, optional
            The alpha_s_clay value of the pile type, by default None.
        alpha_p : float, optional
            The alpha_p value of the pile type, by default None.
        alpha_t_sand : float, optional
            The alpha_t_sand value of the pile type, by default None.
        alpha_t_clay : float, optional
            The alpha_t_clay value of the pile type, by default None.
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
        qc_z_a_lesser_1m : float, optional
            Maximum cone resistance qc value allowed for layers with thickness < 1m in the calculation of positive skin friction resistance.
            It must be less or equal to `qc_z_a_greater_1m`.
            If None, then 12 MPa is used.
            Default: None.
        qc_z_a_greater_1m : float, optional
            Maximum cone resistance qc value allowed for layers with thickness >= 1m in the calculation of positive skin friction resistance.
            It must be greater or equal to `qc_z_a_lesser_1m`.
            If None, then 15 MPa is used.
            Default: None.
        qb_max_limit : float, optional
            Maximum value allowed for the pile tip resistance qb_max.
            Note that is value will be used as a limit for qb_max unless use_almere_rules is true and a higher value than 12 MPa is specified.
            If None, then 15 MPa is used.
            Default: None.
        chamfered : float, optional
            The chamfered value of the pile type, by default None.
        """
        self._standard_pile = None if reference is None else {"reference": reference}
        self._reference = reference
        self._installation_method = installation_method
        self._is_prefab = is_prefab
        self._is_open_ended = is_open_ended
        self._alpha_s_sand = alpha_s_sand
        self._alpha_s_clay = alpha_s_clay
        self._alpha_p = alpha_p
        self._alpha_t_sand = alpha_t_sand
        self._alpha_t_clay = alpha_t_clay
        self._settlement_curve = settlement_curve
        self._negative_fr_delta_factor = negative_fr_delta_factor
        self._adhesion = adhesion
        self._is_low_vibrating = is_low_vibrating
        self._is_auger = is_auger
        self._qc_z_a_lesser_1m = qc_z_a_lesser_1m
        self._qc_z_a_greater_1m = qc_z_a_greater_1m
        self._qb_max_limit = qb_max_limit
        self._chamfered = chamfered

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
        standard_pile = pile_type.get("standard_pile", {})
        properties = pile_type.get("properties", {})
        return cls(
            reference=standard_pile.get("reference"),
            is_prefab=properties.get("is_prefab"),
            is_open_ended=properties.get("is_open_ended"),
            is_low_vibrating=properties.get("is_low_vibrating"),
            is_auger=properties.get("is_auger"),
            installation_method=properties.get("installation_method"),
            alpha_s_sand=properties.get("alpha_s_sand"),
            alpha_s_clay=properties.get("alpha_s_clay"),
            alpha_p=properties.get("alpha_p"),
            alpha_t_sand=properties.get("alpha_t_sand"),
            alpha_t_clay=properties.get("alpha_t_clay"),
            settlement_curve=properties.get("settlement_curve"),
            negative_fr_delta_factor=properties.get("negative_fr_delta_factor"),
            adhesion=properties.get("adhesion"),
            qc_z_a_lesser_1m=properties.get("qc_z_a_lesser_1m"),
            qc_z_a_greater_1m=properties.get("qc_z_a_greater_1m"),
            qb_max_limit=properties.get("qb_max_limit"),
        )

    @property
    def reference(self) -> str | None:
        """The standard pile definition of the pile type (if applicable)"""
        return self._reference

    @property
    def alpha_s_sand(self) -> float | None:
        """The alpha_s_sand value of the pile type"""
        return self._alpha_s_sand

    @property
    def alpha_s_clay(self) -> dict | None:
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
    def alpha_t_clay(self) -> dict | None:
        """The alpha_t_clay value of the pile type"""
        return self._alpha_t_clay

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
    def is_prefab(self) -> bool | None:
        """The is_prefab value of the pile type"""
        return self._is_prefab

    @property
    def is_open_ended(self) -> bool | None:
        """The is_open_ended value of the pile type"""
        return self._is_open_ended

    @property
    def installation_method(self) -> str | None:
        """The installation_method value of the pile type"""
        return self._installation_method

    @property
    def is_low_vibrating(self) -> bool | None:
        """The is_low_vibrating value of the pile type"""
        return self._is_low_vibrating

    @property
    def is_auger(self) -> bool | None:
        """The is_auger value of the pile type"""
        return self._is_auger

    @property
    def qc_z_a_lesser_1m(self) -> float | None:
        """Maximum cone resistance qc value allowed for layers with thickness < 1m in the calculation of positive skin friction resistance."""
        return self._qc_z_a_lesser_1m

    @property
    def qc_z_a_greater_1m(self) -> float | None:
        """Maximum cone resistance qc value allowed for layers with thickness >= 1m in the calculation of positive skin friction resistance."""
        return self._qc_z_a_greater_1m

    @property
    def qb_max_limit(self) -> float | None:
        """Maximum value allowed for the pile tip resistance qb_max."""
        return self._qb_max_limit

    @property
    def chamfered(self) -> float | None:
        """The chamfered value of the pile type"""
        return self._chamfered

    def serialize_payload(self) -> Dict[str, str | dict]:
        """
        Serialize the pile type to a dictionary payload for the API.

        Returns:
            A dictionary payload containing the standard pile (if set), alpha_s_sand, alpha_s_clay, alpha_p,
            alpha_t_sand, settlement curve, negative_fr_delta_factor, adhesion, is_low_vibrating, and is_auger.
        """
        payload: Dict[str, str | dict] = {}

        if self._standard_pile is not None:
            payload["standard_pile"] = self._standard_pile

        custom_type_properties: Dict[str, float | bool | dict | str] = {}

        if self.alpha_s_sand is not None:
            custom_type_properties["alpha_s_sand"] = self.alpha_s_sand

        if self.alpha_s_clay is not None:
            custom_type_properties["alpha_s_clay"] = self.alpha_s_clay

        if self.alpha_p is not None:
            custom_type_properties["alpha_p"] = self.alpha_p

        if self.alpha_t_sand is not None:
            custom_type_properties["alpha_t_sand"] = self.alpha_t_sand

        if self.alpha_t_clay is not None:
            custom_type_properties["alpha_t_clay"] = self.alpha_t_clay

        if self.settlement_curve is not None:
            custom_type_properties["settlement_curve"] = self.settlement_curve

        if self.negative_fr_delta_factor is not None:
            custom_type_properties["negative_fr_delta_factor"] = (
                self.negative_fr_delta_factor
            )

        if self.adhesion is not None:
            custom_type_properties["adhesion"] = self.adhesion

        if self.installation_method is not None:
            custom_type_properties["installation_method"] = self.installation_method

        if self.is_prefab is not None:
            custom_type_properties["is_prefab"] = self.is_prefab

        if self.is_low_vibrating is not None:
            custom_type_properties["is_low_vibrating"] = self.is_low_vibrating

        if self.is_auger is not None:
            custom_type_properties["is_auger"] = self.is_auger

        if self.is_open_ended is not None:
            custom_type_properties["is_open_ended"] = self.is_open_ended

        if self.qc_z_a_lesser_1m is not None:
            custom_type_properties["qc_z_a_lesser_1m"] = self.qc_z_a_lesser_1m

        if self.qc_z_a_greater_1m is not None:
            custom_type_properties["qc_z_a_greater_1m"] = self.qc_z_a_greater_1m

        if self.qb_max_limit is not None:
            custom_type_properties["qb_max_limit"] = self.qb_max_limit

        if self.chamfered is not None:
            custom_type_properties["chamfered"] = self.chamfered

        if len(custom_type_properties.keys()) > 0:
            payload["custom_properties"] = custom_type_properties

        return payload
