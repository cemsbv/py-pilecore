# Decouple the Grouper from PileCore-computed bearing results

**Status:** accepted

## Context

The PileCore **Grouper** flow (payload creation, response wrapping in `GrouperResults`, the
`CasesGrouperResults` viewers, and the grouper report) was hard-wired to
`MultiCPTCompressionBearingResults` — a type shaped by the PileCore bearing-capacity API. Users who
compute pile bearing capacity in *other* software could not use the Grouper, even though the Grouper
endpoints only need a handful of per-CPT numbers plus coordinates.

## Decision

Introduce a narrow, purpose-built seam so that both PileCore-computed and externally-computed
bearing results can drive the Grouper:

- A single `typing.Protocol`, **`GrouperBearingResultsLike`** (`@runtime_checkable`), expressing
  exactly what the Grouper consumers need: `cpt_names`, `pile_tip_levels_nap`,
  `grouper_cpt_inputs() -> List[GrouperCptInput]` (payload side), and
  `base_max_bearing_results() -> MaxBearingResults` (wrapping/fold side).
- A **source-agnostic fold**: `GrouperResults.cpt_results` folds group capacities over
  `bearing.base_max_bearing_results()` regardless of where the baseline came from.
- A lean **`CustomBearingResults`** container (of `CustomCptBearingResult`) that users hand-build
  from flat arrays over a shared pile-tip-level grid. `R_c_d_net` is a **required input** — the
  client carries no NEN 9997-1 bearing math and must not start now. NaNs are **rejected at
  construction** (external data must be clean).
- Two capability tiers: **Tier 1** = numbers + coordinates (payload, API, wrapping, table/scatter/
  plan viewers, report); **Tier 2** = optional raw CPT trace + soil layers unlocking
  `plot_bearing_overview`. To support Tier 1, `SoilProperties` gains a **coordinate-only** mode:
  `cpt_table`, `layer_table`, and the reference levels become optional, with `UserError` guards on
  the plotting methods that need them.

The change is **additive and non-breaking**: existing entry points keep their exact signatures.
`create_grouper_payload(cpt_results_dict=...)`, `GrouperResults.from_api_response(...,
multi_cpt_bearing_results=...)`, and the `multi_cpt_bearing_results` attribute remain (the attribute
becomes a `@deprecated` property). `MultiCPTCompressionBearingResults` satisfies the Protocol via
thin adapter methods with no behaviour change.

## Considered alternatives

- **Duck-type the PileCore types** (no explicit Protocol). Rejected: the coupling is implicit and
  fragile, and there is no type-checker-visible contract for what the Grouper actually requires.
- **Require a full `SoilProperties`** (raw trace) for the custom object. Rejected: the Grouper
  needs only numbers + coordinates; demanding a full CPT trace would exclude exactly the users this
  feature targets. Hence the coordinate-only `SoilProperties` mode.
- **Derive `R_c_d_net` client-side** from components. Rejected: it would introduce the repo's first
  client-side NEN 9997-1 logic and a server-consistency/norm-version drift risk. A
  `from_components(...)` classmethod can be added later if genuinely needed.

## Consequences

- `SoilProperties` invariant loosens to "always identifies a CPT (test_id/x/y); may carry a trace."
  Plotting methods that need the trace/levels now raise a clear "requires soil data" `UserError`
  (or, for `plot_bearing_capacities`, gracefully skip the groundwater/surface reference lines).
- Grouper consumers (`GrouperResults.__post_init__`, the fold, `CasesGrouperResults`) read the
  Protocol members instead of reaching into `multi_cpt_bearing_results.cpt_results.*`.
