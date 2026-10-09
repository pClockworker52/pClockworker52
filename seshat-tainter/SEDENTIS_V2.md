# SEDENTIS_V2.md — workshop preparation (Phase C1, not yet run)

*This is working material, not publishable prose. Peter writes every public sentence himself.*

*Status: prepared, not discussed. Updated 2026-10-09 with the "Sedentis — Current State (Oct 2026)" doc. No Seshat data has been looked at for any H-S hypothesis. Only the Tainter-side inventory (log 000) has been looked at.*

---

## 0. Sources for "Sedentis v1"

**Canonical source (from 2026-10-09):** the Google Doc *"Sedentis — Current State (Oct 2026)"* (Drive id `1VuJT4O_e6DRpyuHopS5qnjhImB4Rh9YtazzUpIdTxts`). It contains:
- the May 2025 formal spec (R, X, M, growth imperative, A↓, S, P)
- the refined causal chain (Aug 2026)
- the core thesis wording (Jul 2026)
- prior art, the empirical record and open problems

Secondary sources:
- the bot prompts in `pClockworker52/sedentis` `main.py` (@ `6d49ffc`)
- §7 of `consciousness_working_paper.docx` (Mar 2026)

### What the Oct 2026 doc changes for this workshop

1. **The core thesis (Jul 2026) is the sharpest claim so far, and the most testable one:**
   > societies respond to *perceived surprise and system stability*, not to *consequences*. Perception is high-dimensional and internal; action is legible.

   This is a **legibility mechanism**. It predicts what a society corrects *for*: legible signals (territory, revenue, order) rather than consequences (welfare, health, ecological state). See claim #12 below.
   - **Prior art to add to the doc's §5 table:** Scott, *Seeing Like a State* (1998), on legibility and the simplification of what states see. If the thesis is "states act on legible proxies", Scott owns it. The distinctive part would then be the claim that this is a *free-energy* consequence (internal model updating is costly or unrewarded at system scale), and that it predicts *when* the proxy gap is worst.
2. **Spec dynamics: "collapse when M > R, or when S > A↓-reduced adaptability".** As written, this is Tainter's condition in different symbols. It counts toward the redundancy question, not against it.
3. **Causal chain step 3: "maintenance costs are dissipative and never plateau".** This is a falsifiable statement in principle, and stronger than Tainter, who says *returns* decline, not that *costs* never plateau.
   - Seshat has no cost variable.
   - The nearest test is whether C plateaus for long periods without growth in scale.
   - ⚠ **Contamination note (pre-registration hygiene):** I have *already seen* one relevant case, while doing the Phase 1 walk-through. The Papal States held SPC around 6.5–6.9 and territory constant (4.64) from 1200 to 1800. That looks like a 600-year plateau without territorial growth.
   - But the Papal States extracted revenue across Catholic Europe without holding the territory. So "expansion" may be **non-territorial**, which Seshat does not measure.
   - Either way, Latium must not be used to *calibrate* any H-S4 or plateau definition.
4. **The doc does not adopt the working paper's §7.3 refactoring.** It only says the paper "applies similar FEP/Prigogine ideas". The v1 vs v1.5 decision below therefore still needs to be made.
5. **This is outside this project, but it's cheap and decisive for the bot question.** The ablation `main_with_no_framework.py` has not been run. Running it is the only clean test of whether the Sedentis framing added or cost anything at the 3-month horizon.

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
| 12 | (Jul 2026 thesis) "Societies respond to perceived surprise and stability, not to consequences; action is legible, perception is not" | Corrective responses track *legible* state variables (territory, revenue, order) and lag or ignore *consequence* variables (welfare, mortality, ecological degradation) | T, but only weakly T-S: Seshat is rich in legible variables and poor in consequence variables. Candidates to check in C2: the Agri/yield data, any famine/epidemic codes in CrisisDB, skeletal-health datasets outside Seshat | Partly. Scott (legibility) predicts the same direction. FEP would need to add *when* the gap is largest (e.g. high prior precision; see §2 (i)) |
| 13 | (Causal chain step 3) "Maintenance costs never plateau" | No long plateau in C without a concurrent rise in scale or extraction | T-S, weakly: no cost variable. Proxy: plateau length in SPC with flat territory and population. ⚠ Latium already seen (see §0) | No |

**First reading:**
- **#12 is the strongest candidate for distinctive content.** It is a claim about *what the system's error signal is*, which neither Tainter nor thermodynamics specifies.
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
| H-S6 (new, from the Jul 2026 thesis) | After a *consequence* shock (famine, epidemic, yield collapse), the next-century response is in legible variables (territory, hierarchy, fortification), not in consequence-reducing ones (storage, water supply, subsistence change) | Tainter: the response depends on returns. Scott: same direction as Sedentis, so it must be distinguished by *when* the gap is largest | Yield-driven response | Feasibility depends on CrisisDB or other consequence-shock data. Without it, this is "untestable with Seshat" |

**Natural controls in Equinox2020:**
- The Orkhon Valley (steppe) and Lena River Valley are the nearest to non-sedentary NGAs.
- Iceland, Chuuk, Oro PNG and Big Island Hawaii vary in staple type.
- Whether this is enough variation is a C2 feasibility question. I haven't looked yet, by design.

## 5. Scale note (state explicitly before testing)

The Metaculus bot failed at a 3-month horizon, where all of Sedentis' structural variables are constant. Seshat's century resolution is the scale the theory claims to work at. **A failure here is a real refutation, not a scale mismatch.** Please confirm you accept this before the C3 tests.

## 6. Questions for the workshop (Peter decides)

1. Is v1 or v1.5 the object under test? This decides whether H-S3 is live.
1b. Is the Jul 2026 legibility thesis (#12) the core of v2? If so:
   - Does Scott's *Seeing Like a State* belong in the prior-art table?
   - What does FEP add over Scott?
2. Which distinctive FEP prediction, if any: (i) precision/age, (ii) shock novelty, or something else?
3. Option closure: OC-A, OC-B, or both?
4. Is #10 (action dissipates, perception conserves) part of v2? If so, it needs a quantitative form first.
5. Do you accept §5 (a failure at century scale counts)?
