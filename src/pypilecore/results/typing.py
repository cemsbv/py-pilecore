from typing import List, Protocol, Union, runtime_checkable

from pypilecore.common.piles import PileProperties
from pypilecore.results.compression.multi_cpt_results import (
    CPTCompressionGroupResultsTable,
    SingleCPTCompressionBearingResultsContainer,
)
from pypilecore.results.tension.multi_cpt_results import (
    CPTTensionGroupResultsTable,
    SingleCPTTensionBearingResultsContainer,
)


@runtime_checkable
class MultiCPTBearingResults(Protocol):
    """
    protocol classes for MultiCPTBearingResults from compression or tension endpoint response
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
    ]: ...

    @property
    def cpt_names(self) -> List[str]: ...

    @property
    def group_results_table(
        self,
    ) -> Union[CPTCompressionGroupResultsTable, CPTTensionGroupResultsTable]: ...
