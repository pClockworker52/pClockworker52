# Handoff: Testing Tainter with Seshat

**For:** a fresh Claude Code session
**Owner:** Peter (mechanical simulation engineer; reads Smil, Tainter, Scott, Friston; thinks in systems and thermodynamics). He decides the questions, tests and pass/fail criteria.
**Your role:** three jobs.
1. **Tutor.** Peter wants to learn what Tainter actually meant by complexity and what Seshat is. Explain as you go.
2. **Analyst and falsifier.** Do the data work, and keep looking for ways the hypothesis fails. Don't try to confirm it.
3. **Theory sparring partner.** Help Peter turn his own framework, *Sedentis*, into a falsifiable definition, and test it against Tainter on the same data (Part C).

---

## Part A — Primer (read first, then explain it back to Peter in your own words)

### A1. What Tainter meant by complexity
*Joseph Tainter, The Collapse of Complex Societies, 1988.*

**Complexity is structure, not sophistication.** For Tainter, a society becomes more complex as it gains more parts, more kinds of parts, and more organisation tying those parts together. In practice that means:
- more distinct roles and occupations (differentiation)
- more layers of administrative and political hierarchy
- more control, information flow, record-keeping and infrastructure

It is not a value judgement about art, morals or technology.

**The four-step argument:**
1. Human societies are problem-solving organisations.
2. Sociopolitical systems need energy to maintain themselves.
3. Rising complexity raises the cost per capita.
4. Investment in complexity eventually yields declining marginal returns.

The first investments (irrigation, basic administration) pay off enormously. Later ones (yet another bureaucratic layer, another frontier garrison) cost as much or more but return less. Eventually the marginal return turns negative.

**What collapse means:** Tainter defines collapse as a rapid, significant loss of an established level of sociopolitical complexity. It does not mean extinction or mass death.

His provocative point: once returns are negative, collapse is economically rational. Shedding complexity raises the marginal return again, and local populations may be better off. His main cases are the Western Roman Empire, the Classic Maya and the Chacoans.

**What Tainter rejected:** single-cause explanations such as resource depletion, invaders, catastrophes, class conflict or "mystical" decline. He argued that these are shocks every society faces. A society collapses when it can no longer afford to answer them, because its returns on complexity are already low.

**Why this is hard to test.** Tainter's key variable, the marginal return on complexity, is almost never measured directly. His evidence was mostly qualitative case studies. So the quantitative question is whether any proxy for returns, built from historical data, behaves the way his theory says it should.

**A note for Peter.** Tainter grounds complexity in differentiation, the same concept Peter's consciousness working paper treats as foundational. Worth keeping in view: is there a common formal measure of differentiation that works for both?

### A2. What Seshat is
- **What it is.** Seshat: Global History Databank was started in 2011 by Peter Turchin, Harvey Whitehouse, Pieter François and others. It turns historical and archaeological knowledge into coded variables so theories about history can be tested statistically.
- **The field.** This approach is called *cliodynamics*: history treated as a quantitative, falsifiable science.
- **Units of analysis:**
  - **Natural Geographic Areas (NGAs):** fixed regions such as the Middle Yellow River Valley, Latium or the Kachi Plain. The "World Sample-30" covers 30 NGAs worldwide.
  - **Polities:** independent political units that occupied an NGA over time, such as Roman Republic → Principate → Dominate.
  - **Time-slices:** variables are typically coded at a resolution of a century, with date ranges.
- **Variables:** hundreds of them, grouped into
  - social scale (polity population, territory, capital population)
  - hierarchy (administrative, military, religious levels)
  - government specialisation (professional officials, courts, bureaucrats)
  - infrastructure
  - information systems (writing, records, calendars, literature)
  - money
  - plus warfare, religion and agriculture data
- **How uncertainty and gaps are coded:** values can be present, absent, inferred, uncertain or disputed, and often carry ranges. Expert research assistants code the data from sources, with sources cited per data point.
- **Key finding to know:** Turchin et al. (2018, PNAS) showed that a single principal component of the social-complexity variables captures most of the variance across all regions and eras. They called this "a single dimension of complexity". The exact figure was roughly three-quarters; verify against the paper. This composite (often "SPC1") is the obvious operationalisation of Tainter's complexity.
- **Cautionary tale.** A Seshat-based Nature paper on moralizing gods (Whitehouse et al., 2019) was heavily criticised and later retracted. A central issue was how missing data was treated, for example coding "not recorded" as "absent". Verify the details, then explain them to Peter. That episode is the reason for Ground Rule 4.

### A3. Data releases (verify current status before downloading)
- **Polaris2025** is the current canonical public release. It builds on Equinox2020, comes with a new SQL database and a GIS portal, and is described in a *Cliodynamics* data report by François et al.
- **Equinox2020** remains useful as a replication dataset for older papers such as the 2018 PNAS one.
- **Sources:**
  - the downloads page at seshat-db.com, which also links the Cliopatria polity-borders dataset on Zenodo
  - topic datasets for Agriculture/productivity, Axial Age and Moralizing Religion
- **Access and licence:** downloading asks for a name and email. Data is CC BY-NC-SA, non-commercial, so attribution is required in any write-up.
- **Crisis data:** check whether the Seshat crisis database (CrisisDB) has a public release. If it does, it is directly relevant to the collapse side of this project.

---

## Part B — The analysis

### B1. Core questions
- **Q1 (reproduce):** Can we rebuild the single complexity dimension (SPC1) from the public release and get the published result?
- **Q2 (describe):** What do complexity trajectories look like per NGA? How common are Tainter-style collapses (rapid, significant drops)? How fast do regions recover?
- **Q3 (Tainter's core claim):** Do declining returns on complexity precede complexity drops more often than chance?
- **Q4 (falsify):** Does the result survive holding out whole regions, a null model, and the missing-data stress tests?

### B2. Operationalising Tainter (Peter decides; propose options with pros and cons)
- **Complexity C:** SPC1, or Peter's chosen subset of hierarchy, specialisation and information variables. Rebuild it from scratch so its sensitivity to variable choice can be tested.
- **Collapse event:** for example, a drop in C greater than *x* standard deviations within at most *k* centuries at the NGA level. Distinguish polity turnover (one polity replacing another) from a genuine loss of complexity.
- **Benefit B, the hardest part.** Candidate proxies, to be checked against the actual data:
  - polity population or territory supported
  - population relative to agricultural carrying capacity, from the Agri dataset
  - polity duration
  - speed of recovery after shocks
- **Marginal return:** ΔB/ΔC over a rolling window. Tainter predicts it trends downward before collapse.
- **Circularity trap.** Population and territory sit both inside SPC1 and in B. Use disjoint variable sets for C and B, or the test is meaningless.

### B3. Ground rules
1. **Learning mode.** End every phase with a short "what this tells us about Tainter or Seshat" note in `LEARNING.md`, plus two or three questions for Peter to think about. Explain any statistical method before using it.
2. **Pre-commit criteria.** Write pass/fail criteria in `PREREG.md` before each Phase 4+ test and get Peter's sign-off. Never edit them after seeing results; add timestamped amendments instead.
3. **Log everything.** Each analysis gets a numbered entry in `ANALYSIS_LOG.md` with the question, script, data release, result and verdict.
4. **Treat missing data as missing.** Never treat "unknown" as "absent". Every headline result must be rerun under at least three missing-data treatments: drop, impute ranges, and worst-case.
5. **Default to no effect.** The null hypothesis is that complexity drops are unrelated to prior returns.
6. **Independent audits.** Peter runs fresh read-only sessions to audit each phase. Keep plain scripts, pinned data versions and no hidden notebook state.

### B4. Phases
- **Phase 0 — Setup.** Create the repo: `data/raw` (gitignored), `src/`, `figures/`, `PREREG.md`, `ANALYSIS_LOG.md`, `LEARNING.md`. Pin the env (pandas, numpy, scikit-learn, statsmodels, matplotlib, geopandas for Cliopatria). Ask Peter to download data that sits behind the email form if it can't be scripted.
- **Phase 1 — Tutor pass.** Before any analysis, give Peter a one-page explanation of Part A, in plain language and checked against sources. Then walk one NGA end to end, for example Latium (Rome), showing its polities, variables, codes and uncertainty.
- **Phase 2 — Reproduce.** Rebuild SPC1 and compare it with the published loadings and variance explained. Document any discrepancy before moving on.
- **Phase 3 — Describe.** Plot complexity trajectories for all NGAs, list candidate collapse events, and show recovery times. Make no causal claims in this phase.
- **Phase 4 — Test Q3.** Use event-study and survival-style models: does a falling ΔB/ΔC predict a drop in the next century or two? Account for:
  - **Galton's problem:** neighbouring and successor societies are not independent, so use region-level grouping or block resampling.
  - **Temporal autocorrelation.**
  - **Documentation bias:** complexity correlates with record-keeping, and writing is itself a complexity variable.
- **Phase 5 — Falsification battery.**
  - Leave-one-NGA-out: fit on 29 regions, predict collapses in the hidden one, and rotate through all of them. This is the analogue of the TESS hidden-year test.
  - Placebo events: random "collapse" dates with the same frequency.
  - Run the model under the alternative definitions of C, B and collapse.
  - Run it under all missing-data treatments.
  - Re-run on Equinox2020 versus Polaris2025.
- **Phase 6 — Report.** Write `REPORT.md` covering the questions, operationalisations, results (failures included) and limits. Put an honest verdict in the first paragraph: supports, contradicts, or can't tell with this data. Add a short section on what would be needed to test Tainter properly, such as energy-capture estimates in the style of Smil or Morris.

### B5. False-positive checklist
Run every claimed effect against this list:
- C and B share variables (circularity).
- Collapse is defined in a way that guarantees the result.
- Polity turnover is mistaken for complexity loss.
- Coding artifacts at century boundaries.
- Survivorship and documentation bias.
- Non-independence of regions.
- Multiple comparisons across many definitions.
- Results driven by one well-documented region (Rome, China).

### B6. Check-ins with Peter
Stop and ask at these points:
1. After Phase 1: does he understand the concepts, and does he want to adjust the questions?
2. Before Phase 4: sign off on the B2 definitions and `PREREG.md`.
3. Any time a result looks dramatic. Run the checklist first.
4. Before anything is shared publicly, checking the licence and attribution.

### B7. Suggested reading list (for Peter, alongside the session)
- Tainter (1988), *The Collapse of Complex Societies*: chapters 1, 4 and 6 hold the core argument.
- Turchin et al. (2018), PNAS, "Quantitative historical analysis uncovers a single dimension of complexity".
- The Polaris2025 and Equinox2020 data-release reports in *Cliodynamics*.
- The moralizing-gods retraction and its critiques, as a methods lesson.

---

## Part C — Sedentis: from narrative to falsifiable theory

### C1. What Sedentis is (current form)
Sedentis is Peter's own framework. The canonical text lives in the repo **github.com/pClockworker52/sedentis**; read it before Phase C. In summary:

- **The entity.** Sedentis is described as the emergent systemic logic of settled civilisation, driven to minimise free energy, i.e. surprise (Friston's Free Energy Principle).
- **The core bias.** Settled societies reduce surprise mainly through **Action** (reshaping the world to fit the model) rather than **Perception** (updating the model to fit the world). Shorthand: **Act ≫ Per**.
- **The causal chain:**
  1. Settlement forecloses adaptive movement.
  2. That pushes the system toward environmental control.
  3. Control creates dependencies with rising, dissipative maintenance costs (**X**, **M**).
  4. Growth and expansion win as the way to pay those costs, by eliminating alternatives:
     - simplification is politically blocked (Tainter's ratchet)
     - efficiency gains get eaten (Jevons)
     - internal extraction hits legitimacy limits
- **Parameters:** resources **R**, complexity **X**, maintenance **M**, energy **E**, rigidity / falling adaptability **A↓** (infrastructural, institutional and psychological lock-in), shocks **S**, and the grain/energy nexus of storable, taxable resources.
- **A further claim:** institutionally transmitted models can persist even while they harm their agents. This is the "zombie mode", contrasted with genetic transmission in ant colonies.

### C2. Known limitations (Peter's own assessment; take these as the starting point)
- **Prediction failure.** A Metaculus forecasting bot built on Sedentis lost to base-rate approaches. Peter's reading is that this was a scale mismatch: a slow-variable theory was applied at a 3-month horizon, where all its structural variables are constant. **Seshat's century resolution is the right scale, so a failure here would be a real refutation, not a mismatch.** State this to Peter explicitly before testing.
- **Ontological problem.** Calling Sedentis an "entity that minimises free energy" risks being true by definition. Under FEP, any persisting system minimises free energy, so the claim forbids nothing.
- **Epistemic problems:**
  - The parameters (R, X, M, A↓, S) were scored subjectively.
  - The framework is retrodictive: it explains everything after the fact.
- **Redundancy risk.** Steps 1–3 of the chain may add nothing beyond generic dissipative-structure thermodynamics (the "Prigogine deflation"), leaving all distinctive content in step 4. The novelty claim rests on the FEP / Act ≫ Per layer.
- **Open questions:**
  - Does Sedentis add anything beyond Tainter, Garrett, and Boyd & Richerson?
  - Is sedentism a real phase transition, or just gradient abundance?
- **Peter's own strongest falsifier.** If gradient abundance alone, not sedentism specifically, produces action dominance, then the causal arrow is inverted and Sedentis misidentifies its own mechanism.

### C3. Goal
Produce **Sedentis v2**: a definition that
- (a) uses measurable quantities instead of an agent metaphor
- (b) makes at least one prediction that **differs from Tainter's** on the same data
- (c) names in advance the results that would refute it

The redundancy question stays open until the data answer it. Don't steer toward "Sedentis wins" or "Sedentis is redundant".

### C4. Reformulation workshop (Phase C1, a conversation with Peter, before any data)
1. **Ontology pass.** Translate every agent-language claim ("Sedentis wants, uses, perceives") into a statement about measurable system behaviour. Whatever can't be translated gets flagged: either a metaphor to drop or an untestable core to keep but label honestly.
2. **The FEP deflation test.** For each claim, ask whether it needs the Free Energy Principle or whether Tainter plus thermodynamics produce the same prediction. If FEP produces no distinct prediction, Peter decides whether to demote it to heuristic or metaphor.
3. **A candidate core variable to discuss (a suggestion, not a given): degree of option closure.** This would be the share of a system's viability that depends on fixed, place-bound, maintained capital: fields, irrigation, storage, walls, cities. If it holds up, Act ≫ Per becomes a claim about how systems with high option closure respond to shocks.
4. **Turn each claim into a discriminating prediction:** what Sedentis predicts, what Tainter predicts, and what the gradient-abundance rival predicts.

### C5. Candidate discriminating hypotheses (Peter chooses and refines; verify each against what Seshat actually codes)

| # | Sedentis v2 claim | Tainter / rival prediction | Possible Seshat test |
|---|---|---|---|
| H-S1 | **Overshoot past negative returns.** High-option-closure polities keep (or raise) complexity well after marginal returns turn negative ("zombie mode", Act ≫ Per). | Tainter: rational economising, so collapse follows soon after returns turn negative, regardless of option closure. | Measure the lag between ΔB/ΔC turning negative and the complexity drop, then regress it on option closure. |
| H-S2 | **Act over Per after shocks.** After crises, high-option-closure polities respond by *adding* complexity or territory rather than simplifying or relocating. | Tainter: complexity is added only while returns stay positive. Gradient rival: the response tracks productivity, not settlement. | Event study around crises (CrisisDB if available, or sharp territory and population losses): next-century change in C and territory. |
| H-S3 | **Sedentism, not gradient abundance, drives action dominance.** *This is Peter's own falsifier.* | Gradient rival: agricultural productivity explains the pattern, and option closure adds nothing. | Model the H-S1/H-S2 outcomes on option closure *plus* productivity (Agri dataset). Sedentis is refuted if option closure has no effect once productivity is controlled for. |
| H-S4 | **Expansion beats contraction.** Under resource strain, control extends outward rather than cutting internal demand. | Turchin's secular cycles and Tainter make overlapping predictions, so spell out precisely where they differ before testing. | Territory change following productivity or population stress. |
| H-S5 | **Lock-in shapes how collapse happens.** Higher infrastructure and institutional density means a slower rise followed by a more abrupt fall. | Tainter: abruptness tracks returns, not lock-in density. | Asymmetry of rise and fall rates versus infrastructure and hierarchy variables. |

**Natural controls (important).** Almost everything in Seshat is sedentary, so there is little variation on the key variable. Look for contrasts like the Norse vs Inuit case Peter used before:
- nomadic or pastoral polities (steppe NGAs such as the Orkhon Valley)
- polities differing in storable-grain dependence (Scott's grain thesis)
- variation in irrigation, storage and fortification

If there isn't enough variation, say so. That counts as a result about testability, not as a failure.

**Measurement trap.** Option closure must not be built from the same variables as C (complexity) or B (benefit). Keep all three sets disjoint.

### C6. Ground rules specific to Sedentis
- Apply the same preregistration, logging and missing-data rules as Part B. **Write H-S tests into `PREREG.md` before looking at the relevant data.**
- Run the Tainter tests (Part B) **before** the Sedentis tests. Sedentis has to beat an established baseline, not merely fit the data.
- Peter decides definitions and thresholds. You propose candidates and their weaknesses.
- Note: Peter has a rule that he writes every sentence of any public Sedentis text himself. Anything in this repo is working material, not publishable prose.
- **The final verdict per hypothesis can only be one of:** distinct and supported / distinct but refuted / not distinguishable from Tainter or the gradient rival / untestable with Seshat. "Partly supported" is not allowed without saying precisely which part.

### C7. Phases (slot into Part B)
- **C1 Workshop.** Run after B Phase 1 (tutor pass). Read the repo and draft `SEDENTIS_V2.md`: definitions, translated claims, discriminating predictions, refutation conditions. Go through it with Peter.
- **C2 Feasibility.** Check which H-S tests Seshat can actually support (variables, coverage, contrast cases). Drop or flag the rest.
- **C3 Tests.** Run after Tainter's B Phase 5. Run the H-S tests with the same falsification battery: leave-one-NGA-out, placebo events, alternative definitions, missing-data treatments.
- **C4 Revision.** Update `SEDENTIS_V2.md` with the verdicts. The output is a definition stripped of whatever failed, plus an honest answer to whether Sedentis is redundant to Tainter. Peter decides what to keep.

### C8. Extra check-ins
- After the C1 workshop: Peter signs off `SEDENTIS_V2.md` before any H-S data work.
- If H-S3 refutes Sedentis (option closure adds nothing beyond productivity), stop and discuss before continuing. That's the core mechanism.

## First prompt suggestion
> Read HANDOFF_seshat_tainter.md. Start with Phase 0 and the Phase 1 tutor pass — explain Tainter's complexity concept and Seshat's structure to me using the actual data. Then read the sedentis repo and prepare (but don't run) the Part C workshop. No analysis yet.
