from enum import StrEnum
from typing import Dict

class NEN99971_version(StrEnum):
    V2017 = "2017"
    V2025 = "2025"


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


class CUR236_version(StrEnum):
    V2024 = "2024"


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
        nen_9997_1: NEN99971_version = NEN99971_version.V2025,
        cur_236: CUR236_version = CUR236_version.V2024,
    ) -> None:
        self.nen_9997_1 = Nen99971(version=nen_9997_1)
        self.cur_236 = Cur236(version=cur_236)

    def serialize_payload(self)-> Dict[str, str]:
        """
        Serialize the norms to a dictonary payload for the API.

        Returns
        -------
        Dict[str, str]
            A dictionary payload containing the versions of the selected norms.
        """
        payload: Dict[str, str] = {
            "NEN99971_version" : self.nen_9997_1.version,
            "CUR236_version" : self.cur_236.version
        }

        return payload


