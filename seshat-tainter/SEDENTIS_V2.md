# SEDENTIS_V2.md — workshop preparation (Phase C1, not yet run)

*This is working material, not publishable prose. Peter writes every public sentence himself.*

*Status: prepared, not discussed. No Seshat data has been looked at for any H-S hypothesis. Only the Tainter-side inventory (log 000) has been looked at.*

---

## 0. Source problem: what exactly is "Sedentis v1"?

The handoff calls `github.com/pClockworker52/sedentis` the canonical text. **It isn't.** The repo is the Metaculus forecasting bot (`main.py`, @ `6d49ffc`). The theory exists there only as LLM prompt text:
- the research prompt, about lines 126–175
- the persona prompt, about lines 255–290

I also found these documents in your Drive (read-only):
- `Sedentis/consciousness_working_paper.docx` (March 2026), §7 "Implications for Sedentis"
- Two AI-generated evaluation docs from 2025: "Sedentis Forecasting Approach Analysis" and "Civilizational Collapse: Sedentis Model". I did not use these as sources.

**Ask 1.** Is there a canonical text I haven't found? If not, I propose we treat the two sources below as v1 and v1.5 and test both against the bot prompt.

### Two versions are already on the table, and they conflict

| | v1 (bot prompt, 2025) | v1.5 (working paper §7.3, 2026) |
|---|---|---|
| Where Act ≫ Per comes from | Permanent settlement | Any sufficiently complex dissipative structure (thermodynamic selection for faster dissipation) |
| Role of sedentism | Causal | "The logical intensification of what all life does"; not special |
| Collapse mechanism | Demands (E, M) and rigidity (A↓) collide with resource limits (R) or shocks (S) | Gradient depletion outruns perception of the depletion |

**Why this matters before any data:**
- H-S3 (sedentism, not gradient abundance) is your own strongest falsifier.
- But v1.5 *already concedes it*. If action dominance is generic to dissipative structures, then "option closure adds nothing beyond productivity" is what v1.5 predicts, not what refutes it.

So the workshop has to decide which theory is under test.
- **(a) Test v1.** H-S3 is a live falsifier.
- **(b) Test v1.5.** Sedentism drops out. The theory must then name a *different* distinctive variable, such as the perception deficit (how fast the system registers gradient depletion). Otherwise it collapses into "Prigogine + Tainter".

## 1. Ontology pass (draft translations)

Each agent-language claim is translated into a statement about system behaviour. Status codes:
- **T** = translatable and measurable in principle
- **T-S** = translatable, plausibly measurable in Seshat
- **M** = metaphor; drop or label as such
- **U** = untestable core; keep only if labelled honestly

| # | v1 claim (agent language) | Behavioural translation | Status | Needs FEP? |
|---|---|---|---|---|
| 1 | "Sedentis is an emergent logic driven to minimise 𝓕" | Persisting societies keep key state variables (food supply, order) within bounds | U: true of every persisting system, so it forbids nothing (your own critique) | Deflated: any homeostat does this |
| 2 | "Achieves this through Action rather than Perception (Act ≫ Per)" | After a perturbation, settled polities respond more by changing the environment or institutions outward (build, conquer, extract) than by changing location, scale or subsistence mode (simplify, move, switch) | T-S, partly: Seshat codes infrastructure, territory and warfare, but has no direct "perception" variable | Possibly not: Tainter's ratchet + sunk cost predict the same sign. FEP must predict a *magnitude* or *condition* the others don't |
| 3 | "Settlement forecloses adaptive movement" | Mobility options shrink as fixed capital per capita rises | T: needs an option-closure measure | No (Scott, plain economics) |
| 4 | "Control creates dependencies with rising maintenance costs (X, M)" | Maintenance load rises with structure | T, but this is Tainter's step 3 | No (thermodynamics) |
| 5 | "Growth wins because alternatives are eliminated (ratchet, Jevons, extraction limits)" | Under strain, territory and population expand rather than complexity falling | T-S (H-S4) | No |
| 6 | "Resource extension: control extends outward rather than reducing internal demand" | Same as 5, in spatial form | T-S | No |
| 7 | "Grain/energy nexus" | Societies dependent on storable, taxable staples show stronger Act-bias | T-S, partly: crop type in `NGAs` sheet, yields in `HistYield+` | No (Scott) |
| 8 | "Zombie mode: institutionally transmitted models persist while harming their agents" | Complexity is sustained beyond the point where benefit per capita is falling | T-S in principle (H-S1), but needs B, which is the weak link | Possibly: this is where an "inference-gone-wrong" story could make a distinct prediction |
| 9 | "Psychological entrainment" | Identity lock-in | U with Seshat (no variable) | — |
| 10 | (v1.5) "Action dissipates, perception conserves" | — | ⚠ **Physically questionable as stated.** Perception and modelling cost energy too (brains are ~20% of human resting metabolism; Landauer's bound applies to any information processing). And "maximum entropy production" as a selection principle is itself contested. The claim needs a quantitative version: perception costs *less per unit of surprise reduction* than action, under what conditions? | — |
| 11 | Bot: "Express as Act:Per ratio, e.g. 80:20" | — | M/U: subjective scoring, the epistemic problem from C2 | — |

**First reading:**
- Steps 1–7 translate, but each reduces to Tainter, Scott, or generic dissipative-structure thermodynamics. That is the "Prigogine deflation" you anticipated.
- The *distinctive* content is concentrated in #2 (as a magnitude or condition claim) and #8 (zombie mode), and possibly #10 if it can be made quantitative.
- I don't conclude from this that Sedentis is redundant. It means the workshop should focus on #2 and #8.

## 2. FEP deflation test: question to settle in the workshop

For #2 and #8: **name one observable pattern that FEP / active inference predicts and that "Tainter + sunk cost + Scott" does not.**

Candidates to discuss (none endorsed):
- **(i) Precision-weighting.** Active inference says that agents with high-precision priors under-update on contrary evidence. Translated: polities with *long, stable* prior histories (high "prior precision") should show longer lags between benefit decline and adjustment than young polities with the same option closure.
  - Tainter makes no age prediction.
  - Crude measurable proxy: polity duration and NGA continuity.
- **(ii) Novelty of the shock.** Active inference treats *expected* and *novel* perturbations differently. Recurrent shocks (familiar droughts) should get "perception" responses; novel ones (new enemy types) should get "action" responses. Or the reverse; the theory must commit.
  - Seshat has no shock-novelty variable. CrisisDB might.
- If neither survives, FEP is demoted to heuristic, and Sedentis v2 is a thermodynamic and economic theory. That is your call.

## 3. Option closure: candidate operationalisations

The definition: *the share of a system's viability that depends on fixed, place-bound, maintained capital.*

**A measurement-trap warning.** Seshat's natural option-closure variables are infrastructure: irrigation, food storage, water supply, canals, roads, bridges, ports, mines. But these make up the **Infra** complexity component, which is **inside SPC**. So:

| Option | Option closure from | Complexity C from | Cost |
|---|---|---|---|
| OC-A | Infra variables + fortifications | SPC rebuilt *without* Infra (7 components) | C loses a component; must check PC1 still holds |
| OC-B | Fortifications only (palisade, ramparts, stone walls, long walls, complex forts, defensive positions); these sit outside SPC in the MilTech block | Full SPC | Fortification is also military technology. It correlates with warfare intensity, so it confounds with "threat" |
| OC-C | Staple type (grain vs tuber vs mixed; `NGAs.FAO.Crop`) + yield (`HistYield+`) | Full SPC | Constant within NGA, so it gives only cross-NGA variation (~30 units). Low power. It is also the gradient rival's variable, so it cannot be used for H-S3 |
| OC-D | Settlement hierarchy + capital population share | — | Both overlap SPC (Hier, Cap). Rejected unless C is rebuilt |

My tentative recommendation for discussion is **OC-A vs OC-B as a pair**. Agreement between them would be informative. Disagreement points at the fortification/warfare confound.

## 4. Discriminating predictions: sharpened from handoff C5

| # | Sedentis claim | Tainter predicts | Gradient rival predicts | Note on distinctiveness |
|---|---|---|---|---|
| H-S1 | The lag between dB/dC < 0 and the complexity drop *increases with option closure* (dose-response) | Lag exists (Tainter's own ratchet) but does *not* scale with option closure | Lag scales with productivity, not option closure | **A lag alone is not distinctive.** Tainter also expects some lag. Only the dose-response slope discriminates |
| H-S2 | After a sharp loss (territory or population, or a CrisisDB crisis), high-OC polities add complexity or territory in the next century; low-OC polities simplify | Response sign depends on prior returns, not on OC | Response depends on yield | Needs a shock definition independent of C |
| H-S3 | OC effect survives controlling for productivity | — | OC effect vanishes given productivity | **Live only under v1** (see §0) |
| H-S4 | Under strain, territory grows rather than complexity falling | Overlaps with Turchin's secular cycles; must specify where they differ first | — | Probably "not distinguishable" unless sharpened |
| H-S5 | Higher OC means a slower rise and a more abrupt fall (rise/fall asymmetry) | Abruptness tracks returns | Abruptness tracks yield | Century resolution may be too coarse to measure abruptness |

**Natural controls in Equinox2020:**
- The Orkhon Valley (steppe) and Lena River Valley are the nearest to non-sedentary NGAs.
- Iceland, Chuuk, Oro PNG and Big Island Hawaii vary in staple type.
- Whether this is enough variation is a C2 feasibility question. I haven't looked yet, by design.

## 5. Scale note (state explicitly before testing)

The Metaculus bot failed at a 3-month horizon, where all of Sedentis' structural variables are constant. Seshat's century resolution is the scale the theory claims to work at. **A failure here is a real refutation, not a scale mismatch.** Please confirm you accept this before the C3 tests.

## 6. Questions for the workshop (Peter decides)

1. Is v1 or v1.5 the object under test? This decides whether H-S3 is live.
2. Which distinctive FEP prediction, if any: (i) precision/age, (ii) shock novelty, or something else?
3. Option closure: OC-A, OC-B, or both?
4. Is #10 (action dissipates, perception conserves) part of v2? If so, it needs a quantitative form first.
5. Do you accept §5 (a failure at century scale counts)?
