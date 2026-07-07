# py-pilecore

Python client for the PileCore API: computes axial pile **bearing capacity** from
CPTs according to NEN 9997-1, and optimises foundation layout with the **Grouper**.
This glossary fixes the vocabulary of the pile-bearing/grouper domain.

## Language

**CPT**:
Cone Penetration Test (sondering) — the soil investigation whose trace drives every
bearing calculation. Identified by a `test_id`.
_Avoid_: sounding, probe.

**Pile-tip level (PTL)**:
The elevation of the pile tip, in metres w.r.t. NAP, at which a bearing capacity is
evaluated. A calculation spans a list of PTLs.
_Avoid_: depth, tip depth.

**Bearing capacity**:
The axial compressive resistance of a pile. Reported through the NEN symbols below;
all forces in kN.

**R_b_cal / R_s_cal**:
The calculated bottom (tip) and shaft components of the compressive bearing capacity
of a single CPT, before group statistics. Required inputs to the Grouper endpoint.

**F_nk_d**:
The design value of the negative shaft friction force — a downward load, subtracted
from gross capacity.

**R_c_d_net**:
The net design bearing capacity: design compressive resistance minus `F_nk_d`. The
headline number the Grouper optimises and the viewers plot.

**Grouper**:
The PileCore service that partitions a project's CPTs into valid **subgroups** and
reports the optimised net bearing capacity per CPT. Runs on bearing capacities that
may be produced by PileCore *or by other software*.

**Subgroup**:
A spatially-coherent set of CPTs the Grouper treats as one statistical group (variation
coefficient ≤ 12 %, no intervening CPTs, optional centre-to-centre check).
_Avoid_: cluster (used only for the internal `SingleClusterResult` type).

**Max-bearing result**:
The per-CPT, per-PTL best of the single-CPT baseline and any valid subgroup value —
the fold that `GrouperResults.cpt_results` produces and the viewers/report consume.

**Custom bearing results**:
Bearing capacities calculated outside PileCore ("bring your own") that a user wants to
feed into the Grouper. Minimum content is numbers + coordinates (Tier 1: per CPT/PTL
`R_b_cal`, `R_s_cal`, `F_nk_d`, `R_c_d_net` + x/y); raw CPT trace + soil layers are an
optional Tier-2 enrichment that unlocks the per-CPT overview plots.
_Avoid_: external bearing results.
