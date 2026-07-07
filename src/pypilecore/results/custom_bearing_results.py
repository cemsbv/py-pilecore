from __future__ import annotations

from typing import Dict, List, Optional, Sequence

import numpy as np
from numpy.typing import NDArray

from pypilecore.results.post_processing import (
    MaxBearingResult,
    MaxBearingResults,
    MaxBearingTable,
)
from pypilecore.results.soil_properties import SoilProperties
from pypilecore.results.typing import GrouperCptInput

Number = float

# The per-CPT bearing arrays that must all share the same length (the pile-tip-level grid).
_ARRAY_FIELDS = ("pile_tip_level_nap", "R_b_cal", "R_s_cal", "F_nk_d", "R_c_d_net")


class CustomCptBearingResult:
    """
    Lean, externally-computed bearing result for a single CPT, over one pile-tip-level grid.

    This is the per-CPT record of a :class:`CustomBearingResults`. It carries only the
    numbers the Grouper needs plus coordinates (Tier 1); a raw CPT trace + soil layers
    (Tier 2) can optionally be attached via ``soil_properties`` to unlock the per-CPT
    overview plots.

    All five arrays (``pile_tip_level_nap``, ``R_b_cal``, ``R_s_cal``, ``F_nk_d``,
    ``R_c_d_net``) are aligned on the same pile-tip-level grid and must have equal length.
    ``R_c_d_net`` is a required input — it is not derived on the client (no client-side
    NEN 9997-1 math).
    """

    def __init__(
        self,
        test_id: str,
        x: float,
        y: float,
        pile_tip_level_nap: Sequence[Number],
        R_b_cal: Sequence[Number],
        R_s_cal: Sequence[Number],
        F_nk_d: Sequence[Number],
        R_c_d_net: Sequence[Number],
        soil_properties: Optional[SoilProperties] = None,
    ):
        """
        Parameters
        ----------
        test_id:
            Identifier (name) of the CPT.
        x:
            x-coordinate of the CPT. Required (may not be ``None``).
        y:
            y-coordinate of the CPT. Required (may not be ``None``).
        pile_tip_level_nap:
            The pile-tip levels [m w.r.t. NAP] the bearing numbers are evaluated at.
        R_b_cal:
            The calculated bottom (tip) bearing capacity [kN] per pile-tip level.
        R_s_cal:
            The calculated shaft bearing capacity [kN] per pile-tip level.
        F_nk_d:
            The design value of the negative shaft friction force [kN] per pile-tip level.
        R_c_d_net:
            The net design bearing capacity [kN] per pile-tip level. Required input.
        soil_properties:
            Optional Tier-2 enrichment: a full `SoilProperties` (raw CPT trace + soil
            layers) that unlocks the per-CPT overview plots. When provided, its
            ``test_id``/``x``/``y`` must match the declared ``test_id``/``x``/``y``.
        """
        if x is None or y is None:
            raise ValueError(
                f"CustomCptBearingResult for CPT {test_id!r} requires both an x and a y "
                f"coordinate, but got x={x!r}, y={y!r}."
            )

        self._test_id = test_id
        self._x = float(x)
        self._y = float(y)
        self._pile_tip_level_nap = np.asarray(pile_tip_level_nap).astype(np.float64)
        self._R_b_cal = np.asarray(R_b_cal).astype(np.float64)
        self._R_s_cal = np.asarray(R_s_cal).astype(np.float64)
        self._F_nk_d = np.asarray(F_nk_d).astype(np.float64)
        self._R_c_d_net = np.asarray(R_c_d_net).astype(np.float64)
        self._soil_properties = soil_properties

        # 1. All five arrays must share the same length (the pile-tip-level grid).
        lengths = {field: len(getattr(self, f"_{field}")) for field in _ARRAY_FIELDS}
        if len(set(lengths.values())) > 1:
            raise ValueError(
                f"CustomCptBearingResult for CPT {test_id!r} requires all arrays to have "
                f"the same length, but got lengths: {lengths}."
            )

        # 2. Hand-authored / external data must be clean: reject any NaN at the source.
        for field in _ARRAY_FIELDS:
            if np.isnan(getattr(self, f"_{field}")).any():
                raise ValueError(
                    f"CustomCptBearingResult for CPT {test_id!r} contains NaN values in "
                    f"{field!r}. Custom bearing results must be NaN-free."
                )

        # 3. If a Tier-2 SoilProperties is attached, its identity must agree (fail loud).
        if soil_properties is not None:
            self._assert_soil_properties_agree(soil_properties)

    def _assert_soil_properties_agree(self, soil_properties: SoilProperties) -> None:
        mismatches = []
        if (
            soil_properties.test_id is not None
            and soil_properties.test_id != self._test_id
        ):
            mismatches.append(
                f"test_id ({soil_properties.test_id!r} != {self._test_id!r})"
            )
        if soil_properties.x is not None and not np.isclose(
            soil_properties.x, self._x
        ):
            mismatches.append(f"x ({soil_properties.x!r} != {self._x!r})")
        if soil_properties.y is not None and not np.isclose(
            soil_properties.y, self._y
        ):
            mismatches.append(f"y ({soil_properties.y!r} != {self._y!r})")
        if mismatches:
            raise ValueError(
                f"The attached soil_properties for CPT {self._test_id!r} does not match "
                f"the declared parameters: {', '.join(mismatches)}."
            )

    @property
    def test_id(self) -> str:
        """Identifier (name) of the CPT."""
        return self._test_id

    @property
    def x(self) -> float:
        """x-coordinate of the CPT."""
        return self._x

    @property
    def y(self) -> float:
        """y-coordinate of the CPT."""
        return self._y

    @property
    def pile_tip_level_nap(self) -> NDArray[np.float64]:
        """The pile-tip levels [m w.r.t. NAP]."""
        return self._pile_tip_level_nap

    @property
    def R_b_cal(self) -> NDArray[np.float64]:
        """The calculated bottom (tip) bearing capacity [kN] per pile-tip level."""
        return self._R_b_cal

    @property
    def R_s_cal(self) -> NDArray[np.float64]:
        """The calculated shaft bearing capacity [kN] per pile-tip level."""
        return self._R_s_cal

    @property
    def F_nk_d(self) -> NDArray[np.float64]:
        """The design negative shaft friction force [kN] per pile-tip level."""
        return self._F_nk_d

    @property
    def R_c_d_net(self) -> NDArray[np.float64]:
        """The net design bearing capacity [kN] per pile-tip level."""
        return self._R_c_d_net

    @property
    def soil_properties(self) -> Optional[SoilProperties]:
        """The attached (Tier-2) `SoilProperties`, or ``None`` for a Tier-1 record."""
        return self._soil_properties

    def to_soil_properties(self) -> SoilProperties:
        """
        The `SoilProperties` for this CPT: the attached Tier-2 trace when provided, else a
        synthesized coordinate-only `SoilProperties` (``test_id``/``x``/``y`` only).
        """
        if self._soil_properties is not None:
            return self._soil_properties
        return SoilProperties(test_id=self._test_id, x=self._x, y=self._y)

    def to_grouper_cpt_input(self) -> GrouperCptInput:
        """The neutral payload-seam record for this CPT."""
        return GrouperCptInput(
            name=self._test_id,
            x=self._x,
            y=self._y,
            pile_tip_level_nap=self._pile_tip_level_nap,
            R_b_cal=self._R_b_cal,
            R_s_cal=self._R_s_cal,
            F_nk_d=self._F_nk_d,
        )

    def to_max_bearing_result(self) -> MaxBearingResult:
        """The per-CPT baseline `MaxBearingResult` that the subgroup fold overlays onto."""
        return MaxBearingResult(
            soil_properties=self.to_soil_properties(),
            pile_head_level_nap=None,
            table=MaxBearingTable(
                pile_tip_level_nap=self._pile_tip_level_nap,
                R_c_d_net=self._R_c_d_net,
                F_nk_d=self._F_nk_d,
                origin=[f"CPT:{self._test_id}"] * len(self._pile_tip_level_nap),
            ),
        )


class CustomBearingResults:
    """
    A lean, externally-computed bearing-results object that can drive the whole PileCore
    Grouper flow (payload, response wrapping, viewers and report) as a source-agnostic
    drop-in for the PileCore-computed `MultiCPTCompressionBearingResults`.

    It satisfies the `GrouperBearingResultsLike` protocol, so it can be passed to
    `create_grouper_payload_from_bearing_results` and
    `GrouperResults.from_grouper_response` exactly where a PileCore object was expected.

    The canonical constructor takes a **sequence of `CustomCptBearingResult` records**;
    the container derives its keys from each record's ``test_id`` and is the single
    validation funnel for the cross-CPT invariants.
    """

    def __init__(self, results: Sequence[CustomCptBearingResult]):
        """
        Parameters
        ----------
        results:
            A sequence of `CustomCptBearingResult` records, one per CPT. Every record must
            share the same pile-tip-level grid, and ``test_id``s must be unique.
        """
        results = list(results)

        for result in results:
            if not isinstance(result, CustomCptBearingResult):
                raise TypeError(
                    "CustomBearingResults expects a sequence of CustomCptBearingResult "
                    f"records, but got a {type(result)}."
                )

        # Reject duplicate test_ids: the key<->identity invariant holds by construction.
        test_ids = [result.test_id for result in results]
        duplicates = sorted({t for t in test_ids if test_ids.count(t) > 1})
        if duplicates:
            raise ValueError(
                f"CustomBearingResults received duplicate test_id(s): {duplicates}. "
                "Each CPT must appear exactly once."
            )

        # All CPTs must share the SAME pile-tip-level grid (compared rounded to 2 decimals).
        grids = [
            frozenset(np.round(result.pile_tip_level_nap, 2)) for result in results
        ]
        if len(set(grids)) > 1:
            raise ValueError(
                "The CPTs do not share the same pile-tip-level grid. All custom bearing "
                "results must be evaluated at the same pile tip levels."
            )

        self._results_dict: Dict[str, CustomCptBearingResult] = {
            result.test_id: result for result in results
        }

    def __getitem__(self, test_id: str) -> CustomCptBearingResult:
        if not isinstance(test_id, str):
            raise TypeError(f"Expected a test-id as a string, but got: {type(test_id)}")
        if test_id not in self._results_dict:
            raise ValueError(
                f"No custom bearing result was provided for this test-id: {test_id}."
            )
        return self._results_dict[test_id]

    @property
    def results_dict(self) -> Dict[str, CustomCptBearingResult]:
        """The dictionary mapping ``test_id`` to its `CustomCptBearingResult`."""
        return self._results_dict

    @property
    def results(self) -> List[CustomCptBearingResult]:
        """The `CustomCptBearingResult` records, as a list."""
        return list(self._results_dict.values())

    # --- GrouperBearingResultsLike protocol members ------------------------------------

    @property
    def cpt_names(self) -> List[str]:
        """The test-ids (CPT names)."""
        return list(self._results_dict.keys())

    @property
    def pile_tip_levels_nap(self) -> List[float]:
        """The shared pile-tip-level grid [m w.r.t. NAP], sorted descending."""
        if not self._results_dict:
            return []
        first = next(iter(self._results_dict.values()))
        grid = frozenset(np.round(first.pile_tip_level_nap, 2))
        return [float(value) for value in sorted(grid, reverse=True)]

    def grouper_cpt_inputs(self) -> List[GrouperCptInput]:
        """The per-CPT grouper-payload inputs (payload side of the seam)."""
        return [result.to_grouper_cpt_input() for result in self._results_dict.values()]

    def base_max_bearing_results(self) -> MaxBearingResults:
        """The per-CPT baseline that the subgroup fold overlays onto (wrapping side)."""
        return MaxBearingResults(
            cpt_results_dict={
                result.test_id: result.to_max_bearing_result()
                for result in self._results_dict.values()
            }
        )
