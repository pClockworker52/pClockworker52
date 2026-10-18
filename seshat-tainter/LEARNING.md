# LEARNING.md

Each phase ends with:
- what it tells us about Tainter or Seshat
- two or three questions for Peter

---

## Phase 0 — Setup (2026-10-09)

**What we learned about Seshat as infrastructure:**
- **Equinox2020** is public on GitHub (`seshatdb/Equinox_Data`) as a single xlsx, so it is scriptable. It ships:
  - raw coded facts
  - a century-grid table
  - pre-aggregated complexity components
  - imputed versions
  - the release's own SPC
- **Polaris** is the current release. The Seshat site now names a "Polaris-2026" spreadsheet; the *Cliodynamics* report says "Polaris2025". It sits behind seshat-db.com / seshatdatabank.info, which this cloud container can't reach. Its GitHub repo name wasn't findable from here.
- The Seshat API package (`Seshat-Global-History-Databank/seshat_api`) points at `seshat-db.com/api`, which is also unreachable from this container.
- **CrisisDB:** I found no standalone public release. It is referenced as part of Seshat (150+ crises; Hoyer et al. 2024 preprint). Check the download page on PC.

**Questions for Peter:**
1. Polaris vs Equinox: should Phase 2 (reproduce 2018) run on Equinox, which is what the paper used, and Polaris enter only at Phase 5? I'd recommend yes. Reproduction should use the data the paper used.
2. Do you want the data snapshot committed (it's CC BY-NC-SA, so redistribution with attribution is allowed), or just pinned by SHA256 as now?

---

## Phase 1 — Tutor pass (2026-10-09)

The one-page primer is `PRIMER.md`. The Latium walk-through is `src/p1_walkthrough_latium.py`, with output in `docs/p1_latium_output.txt`.

**What this tells us about Tainter:**
- Seshat measures Tainter's *C* reasonably directly: hierarchy levels, specialised officials, information systems. That's the good news.
- Seshat measures his *B* (benefit) badly or not at all:
  - The nearest candidates (population, territory) are 63% missing.
  - They are also *inside* SPC.
  - So Tainter's key variable, dB/dC, is the hardest part. That was expected, and now it's quantified.
- **Rome, Tainter's flagship case, drops only 0.79 global SD in Latium.** Gov, Info and Money barely move because the Church carries them. Hierarchy, Territory and Population carry the drop.
  - Is "collapse" in Tainter's sense loss of *all* complexity dimensions, or of *hierarchy and scale*?
  - The answer changes which events count as collapses.

**What this tells us about Seshat:**
- **Values are polity-level, attached to a region.** A change of ruler can therefore look like a complexity change in the region. That is the turnover-vs-collapse trap, and it is built into the data structure.
- **Imputation can manufacture declines.** Latium's Copper Age SPC (3.09) is higher than its Bronze Age SPC (2.30) only because of what was imputed for missing scale variables.
- **Coding is uneven.** Courts are coded `absent` for the Principate. Per-fact provenance exists, so such oddities can be audited.
- **There are gaps in polity coverage** (458–492, 555–567, 1309–1377 in Latium). Collapses often happen exactly in such gaps, which is a documentation bias against detecting collapse.

**Questions for Peter:**
1. **Collapse = which dimensions?**
   - Option (a): a drop in SPC as a whole.
   - Option (b): a drop in Hierarchy + Scale only, Tainter's "sociopolitical" core.
   - Option (c): any component dropping more than x.
   - Rome is a good test of each. Write down *now*, before seeing other NGAs, whether you think Rome must count as a collapse. If you think it must, say why. Otherwise we risk tuning the threshold to Rome.
2. Tainter's power-vacuum condition (in a peer-polity cluster, polities get absorbed rather than collapsing) could be tested with Seshat's NGA succession. Do you want it as a secondary hypothesis?
3. For a mechanical engineer: SPC is PC1 of 8 standardised components. Physically, it's like a single mode shape of a coupled system. Is a single mode an adequate state variable for a system whose *failure* may be a mode decoupling, e.g. Info stays while Hierarchy falls?

---

## Phase 2 — Reproduce (2026-10-18)

**What this tells us about Seshat:**
- **The "single dimension" is robust.** PC1 carries 69–84% of the variance across every missing-data treatment, row selection and era. It holds within regions (87% demeaned) and with scale and infrastructure removed (80–87%).
- **The shared long-run trend isn't the reason.** Even within a single era, the components move together.
- **Engineering analogy:** the coupled system has one dominant mode almost everywhere. The real question (Phase 1, question 3) is whether *failure* is a decoupling, e.g. Hier falling while Info stays. Rome suggests it can be. PC1 hides such a decoupling by construction, so C3 (Hier alone) stays in the battery for that reason.
- **The Equinox aggregates code "missing" as "absent" for Info and Gov.** That's the moralizing-gods pattern, here inside the release's own aggregate sheets.
  - It doesn't move PC1 (r = 0.995).
  - It could still create or erase *events*: a century whose writing variables are uncoded gets Info = 0, which looks like a crash.
  - That is why C1 is built missing-as-missing.

**What this tells us about Tainter:**
- Tainter's C is measurable and coherent in Seshat. The bottleneck is entirely on the B side (log 002: population 37% coded, no per-capita benefit).

**Questions for Peter:**
1. C1 drops Infra from complexity so that infrastructure can serve as option closure. Tainter would count irrigation and roads as complexity. Is it acceptable that the Tainter test uses a C without infrastructure? The alternative is OC-B (fortification) for Sedentis, with full C for Tainter.
2. B1 is *total* population supported, not per-capita benefit. Do you accept testing a "scale-supported" proxy, stated as a limitation, or do you consider that a test of something other than Tainter?

**Update on Phase 0 (2026-10-18):** Polaris2026 is on GitHub (`build_polaris_dataset`), and it contains CrisisDB.
- **The methods lesson:** CrisisDB lists crises. It does *not* say which polity-centuries had none.
- **Your question to think about:** what is the right "denominator" for asking "do negative returns cause collapse", if the only independent collapse list is conditional on a crisis having happened?
