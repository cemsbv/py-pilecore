from enum import StrEnum
from typing import Dict


class NEN99971_version(StrEnum):
    V2017 = "2017"
    V2025 = "2025"


class CUR236_version(StrEnum):
    V2024 = "2024"


class Nen99971:
    """
    NEN 9997-1 standard for pile design.
    """

    def __init__(self, version: NEN99971_version = NEN99971_version.V2025) -> None:
        if not isinstance(version, NEN99971_version):
            raise TypeError("version must be a NEN99971_version enum member")
        self._version = version

    def __str__(self) -> str:
        return f"NEN9997-1 ({self._version})"

    @property
    def version(self) -> NEN99971_version:
        """Returns the version of the NEN 9997-1 standard."""
        return self._version


class Cur236:
    """
    CUR236 standard for pile design.
    """

    def __init__(self, version: CUR236_version = CUR236_version.V2024) -> None:
        if not isinstance(version, CUR236_version):
            raise TypeError("version must be a CUR236_version enum member")
        self._version = version

    def __str__(self) -> str:
        return f"CUR236 ({self._version})"

    @property
    def version(self) -> CUR236_version:
        """Returns the version of the CUR236 standard."""
        return self._version


class Norms:
    """
    Container for all norm standards.
    """

    def __init__(
        self,
        nen_9997_1: str = "2025",
        cur_236: str = "2024",
    ) -> None:
        try:
            self.nen_9997_1 = Nen99971(version=NEN99971_version(nen_9997_1))
        except ValueError:
            raise ValueError(
                f"Invalid NEN9997-1 version selected: {nen_9997_1}, must be one of {[v.value for v in NEN99971_version]}"
            )
        try:
            self.cur_236 = Cur236(version=CUR236_version(cur_236))
        except ValueError:
            raise ValueError(
                f"Invalid CUR-236 version selected: {cur_236}, must be one of {[v.value for v in CUR236_version]}"
            )

    def serialize_payload(self) -> Dict[str, str]:
        """
        Serialize the norms to a dictonary payload for the API.

        Returns
        -------
        Dict[str, str]
            A dictionary payload containing the versions of the selected norms.
        """
        payload: Dict[str, str] = {
            "NEN99971_version": self.nen_9997_1.version,
            "CUR236_version": self.cur_236.version,
        }

        return payload
