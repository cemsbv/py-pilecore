from dataclasses import dataclass
from typing import Dict, Hashable, List, Optional, Protocol, Union, runtime_checkable

import numpy as np
from numpy.typing import NDArray

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


@dataclass(frozen=True)
class GrouperCptInput:
    """
    A neutral, source-agnostic description of the per-CPT bearing numbers that the
    Grouper payload needs.

    It decouples the grouper-payload builder from any concrete bearing-results type
    (PileCore's ``MultiCPTCompressionBearingResults`` or a user's ``CustomBearingResults``).
    All arrays are aligned on the same pile-tip-level grid.

    Attributes
    ----------
    name:
        The CPT name (``test_id``).
    x:
        The x-coordinate of the CPT. May be ``None``; the payload builder rejects that.
    y:
        The y-coordinate of the CPT. May be ``None``; the payload builder rejects that.
    pile_tip_level_nap:
        The pile-tip levels [m w.r.t. NAP] the bearing numbers are evaluated at.
    R_b_cal:
        The calculated bottom (tip) bearing capacity [kN] per pile-tip level.
    R_s_cal:
        The calculated shaft bearing capacity [kN] per pile-tip level.
    F_nk_d:
        The design value of the negative shaft friction force [kN] per pile-tip level.
    """

    name: str
    x: Optional[float]
    y: Optional[float]
    pile_tip_level_nap: NDArray[np.float64]
    R_b_cal: NDArray[np.float64]
    R_s_cal: NDArray[np.float64]
    F_nk_d: NDArray[np.float64]


@runtime_checkable
class GrouperBearingResultsLike(Protocol):
    """
    Protocol expressing exactly what the Grouper consumers need from a bearing-results
    object, regardless of whether the numbers were computed by PileCore or by other
    software.

    Both ``MultiCPTCompressionBearingResults`` (via thin adapters) and the lean
    ``CustomBearingResults`` object satisfy this protocol, so the payload builder, the
    ``GrouperResults`` wrapping/fold and the viewers can all run source-agnostically.

    Deliberately Grouper-narrow: it is not a general bearing-results interface.
    """

    @property
    def cpt_names(self) -> List[str]:
        """The test-ids (CPT names) that carry bearing results."""
        ...

    @property
    def pile_tip_levels_nap(self) -> List[float]:
        """The shared pile-tip-level grid [m w.r.t. NAP] of all CPTs."""
        ...

    def grouper_cpt_inputs(self) -> List[GrouperCptInput]:
        """The per-CPT payload inputs (payload side of the seam)."""
        ...

    def base_max_bearing_results(self) -> MaxBearingResults:
        """The per-CPT baseline that the subgroup fold overlays onto (wrapping side)."""
        ...


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
