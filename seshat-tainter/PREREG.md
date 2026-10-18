# PREREG.md

**Rules:**
- Pass/fail criteria are written here *before* each Phase 4+ test (Tainter) and each H-S test (Sedentis).
- Each block needs Peter's sign-off, with name and date.
- After sign-off, a block is never edited. Changes go into timestamped amendments below it.
- **Default verdict = no effect.** The null hypothesis is that complexity drops are unrelated to prior returns.
- Every headline result is rerun under at least three missing-data treatments: drop, impute-ranges and worst-case.

*Status (2026-10-18): DRAFT blocks below, **all unsigned**. Definitions are proposed in `docs/B2_options.md` (★ = proposed primary). No test may run until Peter signs the block.*

---

## Template (copy per test)

```
### T<n> — <name>
Signed off: <Peter, date>
Data release + commit/sha:
Question:
C (complexity) definition + variables:
B (benefit) definition + variables:        # must be disjoint from C
Option closure definition (H-S only):     # must be disjoint from C and B
Collapse event definition (x SD, k centuries, turnover rule):
Model / test statistic:
Dependence handling (Galton, autocorrelation):
PASS if:
FAIL if:
INCONCLUSIVE if:
Missing-data treatments to run:
Multiple-comparison handling (how many definitions tried, correction):

Amendments:
- <timestamp> <what changed and why, before/after seeing which results>
```


---

# DRAFT blocks (unsigned)

Common to all blocks:
- **Data:** Equinox2020 @ `602c7cd`, sha256 `48c7fbd0…0556` (primary). Polaris is rerun in Phase 5.
- **Holdout:** `holdout_ngas.csv` (6 NGAs, seed 20261018). Not touched until the final confirmation run.
- **Variable roles:** `variable_roles.csv` (must be signed together with these blocks).
- **Inference:** NGA cluster bootstrap with 2,000 resamples, plus a sensitivity check clustering by polity family.
- **Multiple comparisons:** the primary spec decides the verdict. The alternative definitions (C1–C3 × B1–B3 × R1–R2 × K1–K3) are reported as a robustness *map*. They cannot rescue a failed primary result. A pass also requires a majority of the alternative specs to agree in sign.
- **Minimum events:** if the training set has fewer than 10 collapse events under K1, the verdict is "can't tell with this data", whatever the p-values.

### T1 — Tainter core: negative returns precede collapse (Q3)
Signed off: — (DRAFT)
- **Question:** is a collapse onset in (t, t+2] more likely after a negative-return episode at t?
- **Definitions:** C1, B1, R1, K1 (`docs/B2_options.md`)
- **Model:** discrete-time **Firth-penalised** logit (rare events; the synthetic tests showed separation in a plain logit), collapse_onset(t+1..t+2) ~ NegReturn(t) + C(t) + PropCoded(t) + era FE. Fitted on training NGA-centuries at risk (not already in a collapse).
- **Code:** `src/p4_run_t1.py`, validated on synthetic data (`tests/test_synthetic.py`). It refuses to run until this block is signed.
- **Statistic:** odds ratio (OR) for NegReturn.
- **Placebo:** circularly shift each NGA's event sequence (1,000 shifts). The observed OR is compared with the placebo distribution.
- **PASS if all of these hold:**
  - OR > 1 with 95% bootstrap CI excluding 1
  - observed OR above the 95th percentile of the placebo distribution
  - same sign under MD-drop, MD-MI and MD-worst
  - leave-one-NGA-out: OR > 1 in ≥ 80% of folds
  - holdout: OR > 1, with no significance needed given its size
- **FAIL if:** OR ≤ 1, or the CI includes 1 under MD-MI.
- **INCONCLUSIVE if:** passes MD-MI but fails MD-worst, *or* fewer than 10 events. Reported as "can't tell".

### T2 — Descriptive check: do collapses exist at Tainter's scale? (Phase 3, no hypothesis)
Signed off: — (DRAFT)
- Phase 3 outputs the K1–K3 event lists, recovery times and trajectories for **training NGAs only**.
- It runs **after** T1 and all H-S blocks are signed, because the trajectories reveal outcomes.

### HS-commit — Strict reading (decided by Peter 2026-10-18; to be countersigned)
If option closure adds nothing beyond productivity in HS3, then **v1 is refuted, and Sedentis survives only as v1.5**. v1.5 cannot be distinguished from generic dissipative-structure thermodynamics with this data.

### HS1 — Overshoot scales with option closure
Signed off: — (DRAFT)
- **Question:** among collapse events (K1), is the lag from the first negative-return episode to collapse onset longer when option closure is higher?
- **Definitions:** OC-A (★), with OC-B as the alternative. OC is measured at the start of the episode.
- **Model:** Cox model or discrete-time logit for time-to-collapse after episode onset ~ OC + productivity + C + PropCoded, clustered by NGA.
- **Sedentis predicts:** HR(OC) < 1, i.e. high OC delays collapse.
- **Tainter predicts:** HR(OC) = 1. A lag may exist, but it doesn't scale with OC.
- **PASS (distinct and supported) if:** HR(OC) < 1 with CI excluding 1, the effect is ≥ the pre-set size (proposed: HR ≤ 0.67 per SD of OC), and it holds under the three missing-data treatments and OC-B.
- **FAIL (distinct but refuted) if:** HR(OC) ≥ 1, or the CI includes 1 with the point estimate above 0.85.
- **NOT DISTINGUISHABLE if:** the CI includes 1 and the point estimate is ≤ 0.85.
- **UNTESTABLE if:** fewer than 10 episodes are followed by collapse.

### HS2 — After a shock, high option closure adds rather than simplifies
Signed off: — (DRAFT)
- **Shock (independent of C):** loss of ≥ 30% of polity territory within one century (Δlog₁₀ Terr ≤ −0.155). Secondary: Sack, Destruction or Settlement destruction coded present.
- **Outcome Y:** sign of ΔC1 over the next century (add = 1, simplify = 0). Territory is excluded from Y to avoid mean reversion.
- **Model:** logit Y ~ OC + productivity + C + PropCoded + era, clustered by NGA.
- **PASS if:** OR(OC) ≥ 1.5 per SD with CI excluding 1, in the primary spec and under all three missing-data treatments.
- **FAIL if:** OR ≤ 1.
- **NOT DISTINGUISHABLE otherwise.**
- **UNTESTABLE if:** fewer than 15 shocks.

### HS3 — Settlement vs gradient (decides between v1 and v1.5)
Signed off: — (DRAFT)
- **Same models as HS1 and HS2**, comparing two versions:
  - (a) without the productivity control
  - (b) with log yield (`HistYield+`)
- **v1 survives if:**
  - The OC effect in (b) meets HS1/HS2's PASS size, *and*
  - It remains significant after SIMEX correction assuming yield reliability = 0.5.
- **v1 is refuted, and the HS-commit applies, if:** the OC effect in (b) fails that test while (a) passes. This is the case where the gradient explains it.
- **If (a) already fails:** there is no Act-bias effect to explain, so H-S1/H-S2 are refuted on their own. The verdict follows from those.
- **Untestable if:** OC and log yield correlate above 0.8 in training data. This collinearity check is blind to outcomes, so it may run before sign-off.

### HS4 — Expansion beats contraction
Signed off: — (DRAFT, **flagged**)
Not distinguishable from Turchin's secular cycles until the difference is specified. Proposed verdict unless sharpened at the workshop: **not distinguishable**.

### HS5 — Rise/fall asymmetry scales with lock-in
Signed off: — (DRAFT, **flagged**)
Century resolution is likely too coarse to measure abruptness. Proposed: **untestable with Seshat**, unless the K1 events show multi-century falls.

### HS6 — Legibility: consequence shocks get legible responses
Signed off: — (DRAFT, **flagged; needs Peter's mapping first**)
- Equinox has no consequence-shock variable (log 002). Polaris2026's CrisisDB has an `epidemic` flag (log 005).
- **Test, within crises only:** for crises with epidemic = P/IP vs other crises, compare the share with a "Per-type" consequence vs an "Act-type" one.
- **Mapping to be fixed by Peter before any value is seen:**
  - Per-type (model or institution revised): `constitution`, `labor`, `suffrage`, `public_goods`, `religion`
  - Act-type (legible control): `conquest`, `extermination`, `unfree_labor`
  - Neither: `capital`, `depose`, `assassination`
- **Caveat:** CrisisDB codes *consequences*, not chosen *responses*. Reading them as Act or Per is interpretive and must be justified before testing.
- **Minimum:** ≥ 15 epidemic crises; otherwise untestable.
- **Predictions, within epidemic crises:**
  - Sedentis (legibility): Act-type ≥ Per-type
  - Tainter makes no prediction
  - Scott predicts the same direction. So even a pass is "not distinguishable from Scott", unless a precision/age interaction is pre-specified.

### T1b — Tainter, with CrisisDB as an independent collapse coding
Signed off: — (DRAFT)
- **Question:** among CrisisDB crises (training NGAs), is `collapse` = P/IP more likely when a negative-return episode (R1, B1, C1) was present in the 3 centuries before the crisis start?
- **Model:** logit, clustered by NGA.
- **PASS if:** OR > 1 with CI excluding 1, same sign under the three missing-data treatments.
- **FAIL if:** OR ≤ 1.
- **Value:** the collapse definition comes from independent experts, so it is not built from C. That guards against "defined so as to guarantee the result" (false-positive checklist, item 2).
