# DECISIONS.md — everything waiting on Peter (as of 2026-10-18)

Mark each item **accept** or **change**. The tests stay blocked until the starred block is signed in `PREREG.md`.

## Already decided
- **2026-10-18, workshop Q1:** v1 is the hypothesis and v1.5 its rival, decided by HS3. Sedentism is treated as a dose. **Strict reading:** if option closure adds nothing beyond productivity, v1 is refuted and Sedentis survives only as v1.5.

## To decide (my proposal in brackets)

| # | Decision | Proposal | Where |
|---|---|---|---|
| D1 | Complexity C | [C1 = PC1 of Hier, Gov, Info, Money, built missing-as-missing] | B2 §1 |
| D2 | Benefit B, accepted as a "scale-supported" proxy, not per-capita benefit | [B1 = log polity population] | B2 §2; LEARNING Phase 2 Q2 |
| D3 | Marginal return | [R1: C up and B flat or down over 3 centuries] | B2 §3 |
| D4 | Collapse | [K1 = drop ≥ 2.0 × SD of 3-century changes, persisting ≥ 2 centuries; K4 = CrisisDB as an independent check] | B2 §4 |
| D5 | **Rome:** must it count as a collapse? | [No pre-commitment: accept whatever K1 says] | B2 §4 |
| D6 | Missing-data treatments | [MD-drop, MD-MI (with range-sampling, still to implement), MD-worst] | B2 §6 |
| D7 | Option closure | [OC-A infrastructure primary; OC-B fortification as alternative] | B2 §7 |
| D8 | Tainter C without Infra (Infra is used as OC), acceptable? | [Yes; full SPC kept as a flagged circular variant] | LEARNING Phase 2 Q1 |
| D9 | Effect sizes | [HS1: HR ≤ 0.67 per SD; HS2: OR ≥ 1.5 per SD; HS3 SIMEX reliability 0.5] | PREREG |
| D10 | HS6 Act/Per mapping of CrisisDB consequences | [Draft mapping in PREREG HS6; needs your judgement] | PREREG HS6 |
| D11 | Q1b legibility core; Q2 FEP prediction; Q4 dissipation claim | [Candidate core, tested later; precision/age as exploratory; dissipation claim not in v2] | SEDENTIS_V2 §7 |
| D12 | Power-vacuum condition (Tainter) as a secondary hypothesis? | [Optional; not drafted] | LEARNING Phase 1 Q2 |
| D13 | Reordering: H-S prereg *before* Phase 3 | [Yes, because Phase 3 reveals outcomes] | README |
| ★ | **Sign:** `variable_roles.csv`, PREREG T1, T1b, HS1–HS3 | — | — |

## What happens after signing
1. Implement range-sampling (D6), then run `src/p4_run_t1.py` (T1) on the training NGAs.
2. Phase 3: descriptive event lists, training NGAs only.
3. HS1–HS3 runners use the same harness.
4. Phase 5 battery, including the Polaris rerun via `src/p5_polaris_grid.py`.
5. Holdout confirmation (`CONFIRM_HOLDOUT=1`).
6. `REPORT.md`.
