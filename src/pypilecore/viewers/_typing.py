from typing import Hashable, List, Protocol, runtime_checkable

from pypilecore.results.data_tables import CptResultsTable


@runtime_checkable
class CasesMultiCPTResultsProtocol(Protocol):
    """Protocol for CasesMultiCPTBearingResults."""

    @property
    def cases(self) -> List[Hashable]:
        """The case names of each MultiCPTBearingResults."""
        ...

    @property
    def test_ids(self) -> List[str]:
        """The test_ids (cpt names) of all the MultiCPTBearingResults."""
        ...

    @property
    def pile_tip_levels_nap(self) -> List[float]:
        """The pile tip levels w.r.t. NAP of all the MultiCPTBearingResults."""
        ...

    @property
    def cpt_results_table(self) -> CptResultsTable:
        """The Table object with all CPT results."""
        ...
