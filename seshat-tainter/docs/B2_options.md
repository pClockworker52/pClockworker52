# B2 — Operationalisation options (DRAFT, for Peter's decision)

Every choice below is a *proposal*. ★ marks my recommended primary specification. The others become alternative definitions in the falsification battery (Phase 5).

All variable assignments follow `variable_roles.csv`, which keeps C, B and OC disjoint and is checked by script.

**What I knew when writing this (disclosed so you can judge contamination):**
- Latium's trajectory, from the Phase 1 walk-through. Rome falls 0.79 global SD in release SPC.
- Global SPC mean and SD.
- Variable *coverage* rates (`docs/g2_coverage.csv`).
- PCA structure (Phase 2).

**What I have not looked at:**
- any other NGA's trajectory
- any collapse event
- any B or ΔB/ΔC value
- any yield value

---

## 1. Complexity C

| | Definition | Pros | Cons |
|---|---|---|---|
| ★ C1 | PC1 of **Hier, Gov, Info, Money**. Gov and Info are built missing-as-missing ("M"). PCA is fitted on training NGAs only. | Disjoint from B (scale) and OC (Infra). PC1 still carries 80–87% of variance (`docs/p2_summary.txt`), so it stays one dimension. | Not Turchin's exact SPC. Loses the Infra component. |
| C2 | Release SPC (all 8 components) | The published measure | **Circular** with B, since it contains Pop and Terr. Use only as a flagged variant to show what the circular version would say. |
| C3 | Hier alone (mean of admin, military and settlement levels) | Closest to Tainter's "sociopolitical" core. The Rome lesson: Hier carries the fall. | Coarse integer steps. Noisier. |

## 2. Benefit B

| | Definition | Coverage (training) | Pros | Cons |
|---|---|---|---|---|
| ★ B1 | log₁₀ polity population | 37% coded; release ships 20 imputations (`Scale_MI`) | "Problem-solving capacity = people supported" is a defensible reading of Tainter | Total, not per capita. Tainter's benefit is per capita, and Seshat has nothing per capita. Polity-level, not NGA-level. |
| B2 | log₁₀ polity territory | 39% | Same | Same; conquest-driven |
| B3 | Polity duration (Polities sheet) | ~100% | Fully coded | Mechanically linked to turnover, which risks building the result in |

**This has to be said plainly in the report:** no Seshat variable measures Tainter's *per-capita* benefit. Whatever the result, the test is of a "scale-supported" proxy.

## 3. Marginal return

Tainter predicts B(C) is concave: dB/dC falls, then turns negative.

| | Definition | Note |
|---|---|---|
| ★ R1 | **Negative-return episode at century t:** over the window [t−3, t], C rose (ΔC > 0) while B did not (ΔB ≤ 0) | Discrete and well-defined. Avoids dividing by ΔC ≈ 0. |
| R2 | Rolling OLS slope of B on C over a 4-century window; "declining" if the slope at t is below the slope at t−4 | Closer to "dB/dC trends down". Unstable when C barely moves. |

## 4. Collapse event

Measured on C at the NGA level.

| | Definition |
|---|---|
| ★ K1 | Drop of **≥ 2.0 × SD of 3-century changes in C** (pooled over training NGAs) below the running maximum of the prior 3 centuries. Must **persist ≥ 2 centuries**, so a single-century coding blip doesn't count. *Changed 2026-10-18, before any real event was seen:* the synthetic runner test showed that an SD over all NGA-centuries mostly measures between-region and 10,000-year-trend spread, which makes "1 SD" very strict (Rome: 0.79). The SD of *changes* measures "rapid and significant" relative to normal movement. |
| K1-global | The earlier version: ≥ 1.0 SD of C over all training NGA-centuries. Kept as an alternative. |
| K2 | Same with 0.5 SD (sensitivity) |
| K3 | Hier drop of ≥ 1.0 level within 2 centuries, persisting ≥ 2 centuries |
| K4 | **CrisisDB-coded `collapse` = P/IP** (Polaris2026). Expert-coded, so independent of C. It can only be used **conditional on a crisis**, since CrisisDB lists crises only and absence is not coded. Use: among crises, does a prior negative-return episode raise P(collapse vs decline-only)? |

**Turnover rule.**
- A polity change *without* a qualifying drop in C is not a collapse. This follows from defining collapse on C, not on polity identity.
- Every event is tagged by whether it coincides with a polity change.
- Results are reported for all events and for the subset where the successor polity holds less territory.

**Gaps.** If an NGA has an uncoded gap (e.g. Latium 458–492), the drop is measured across the gap but the event is tagged `gap`. Then:
- *worst case:* drop all gap events
- *alternative:* keep them

**Rome pre-commitment (needs Peter).**
- Under K1 (1.0 SD), Rome's drop in *release SPC* (0.79 SD) would not qualify. It might still qualify under C1, which I have not computed.
- K2 (0.5 SD) would include it.
- I propose fixing K1 on general grounds ("rapid, significant loss"), **not** to include or exclude Rome, and accepting whatever Rome does.
- Please confirm, or state now that Rome must count, and why.

## 5. Confounds the Q3 model must handle

- **Regression to the mean.** NGAs at high C have more room to fall, and negative-return episodes may occur more at high C. **Control: C level at t.**
- **Documentation.** `PropCoded` changes over time, and imputation can create apparent drops (as with Latium's Copper Age). **Control: PropCoded. Also:** rerun with events in low-coverage centuries removed.
- **Galton's problem.**
  - 25 of the 123 holdout polities are shared with training NGAs (empires spanning regions).
  - Use the cluster bootstrap by NGA, plus a sensitivity check that clusters by polity "family" (connected components of shared PolIDs).
- **Time.** Use era fixed effects (millennium).

## 6. Missing-data treatments (Ground Rule 4)

| | Treatment |
|---|---|
| MD-drop | Complete cases only |
| ★ MD-MI | **Range-impute + MI.** Each of 20 draws first samples range-coded values uniformly within [From, To], read from CanonDat; e.g. Principate population 50–60 M. Remaining NA are then filled with multiple imputation (Scale_MI for scale, IterativeImputer for the rest), and the draws are pooled. This is Ground Rule 4's "impute ranges". |
| MD-worst | B imputed *against* the hypothesis: missing B in the 3 centuries before an event is set to rise with C, so the episode is not a negative-return one. Missing B elsewhere is set to fall. |

## 7. Option closure (Sedentis only)

| | Definition | Confound |
|---|---|---|
| ★ OC-A | Mean of 12 infrastructure variables (irrigation, storage, water, roads, canals, ports, posts…), i.e. the Infra component removed from C | Correlates with productivity (irrigation ~ yield), which is the H-S3 issue |
| OC-B | Mean of 11 fortification variables | Fortification ~ threat. Control: inter-polity war and internal war (WarType) |

## 8. Productivity control (H-S3)

`HistYield+` (t/ha/y per NGA per century; modelled, not observed). The measurement-error sensitivity check uses SIMEX, assuming yield reliability of 0.5.

**Collinearity pre-check** (blind, `docs/g2_oc_yield.txt`, training NGAs; yield > 0 rows only):

| Pair | Pearson | Within-NGA Pearson |
|---|---|---|
| OC-A ~ log yield | 0.53 | 0.68 |
| OC-B ~ log yield | 0.18 | 0.24 |

Both are below the 0.8 "untestable" bar, so HS3 is testable. But OC-A shares much of its variance with yield, probably through a common time trend, so era fixed effects matter.

148 training NGA-centuries have yield = 0, meaning pre-agricultural. They are a potential non-agricultural contrast for C2 feasibility, but they are early and data-poor.
