from typing import Dict, Hashable, List, Protocol, Union, runtime_checkable

from pypilecore.common.piles import PileProperties
from pypilecore.results.compression.multi_cpt_results import (
    CPTCompressionGroupResultsTable,
    SingleCPTCompressionBearingResultsContainer,
)
from pypilecore.results.data_tables import CptResultsTable
from pypilecore.results.post_processing import MaxBearingResults
from pypilecore.results.tension.multi_cpt_results import (
    CPTTensionGroupResultsTable,
    SingleCPTTensionBearingResultsContainer,
)


@runtime_checkable
class LikeMultiCPTResults(Protocol):
    """
    Protocol class for MultiCPTBearingResults from compression or tension endpoint response
    """

    def __init__(self) -> None: ...

    @property
    def pile_properties(self) -> PileProperties: ...

    @property
    def cpt_results(
        self,
    ) -> Union[
        SingleCPTCompressionBearingResultsContainer,
        SingleCPTTensionBearingResultsContainer,
        MaxBearingResults,
    ]: ...

    @property
    def cpt_names(self) -> List[str]: ...

    @property
    def group_results_table(
        self,
    ) -> Union[CPTCompressionGroupResultsTable, CPTTensionGroupResultsTable]: ...


@runtime_checkable
class CasesMultiCPTResultsLike(Protocol):
    """Protocol for CasesMultiCPTResults."""

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

    @property
    def results_per_case(self) -> Dict[Hashable, LikeMultiCPTResults]:
        """The dictionary with case names as keys and MultiCPTBearingResults as values."""
        ...
