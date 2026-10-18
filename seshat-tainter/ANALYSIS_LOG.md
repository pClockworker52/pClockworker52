# ANALYSIS_LOG.md

Numbered entries. Each entry records the question, script, data release, result and verdict. No entry is ever edited after it's written; corrections get a new entry.

---

## 000 — Data inventory (descriptive, no hypothesis)

- **Date:** 2026-10-09
- **Question:** What does the Equinox2020 release contain, and how much is missing?
- **Script:** `src/p1_walkthrough_latium.py`; output in `docs/p1_latium_output.txt`
- **Data:**
  - `seshatdb/Equinox_Data` @ `602c7cdf0649e1fbbdb37f5b5a387edbe19915d0`
  - `Equinox_on_GitHub_June9_2022.xlsx`, sha256 `48c7fbd00b6ebca4405d171e1d8e4fb2ea74a2fcd3edd0762e699e7d472f0556`
- **Result:**
  - 13 sheets. The main ones:
    - `Equinox2020_CanonDat` (47,477 facts)
    - `TSDat123` (1,494 NGA-centuries × 163 vars, NA = -999)
    - `AggrSCWarAgriRelig`
    - `ImpSCDat` (single imputation)
    - `SPC_MilTech` (release SPC)
    - `Scale_MI` / `Class_MI` (20 imputations)
    - `HistYield+` (agricultural yields)
  - 35 NGAs and 373 polities in the facts table (444 rows in `Polities`).
  - 41% of social-complexity cells are missing. Population and territory are each 63% missing.
  - Latium SPC peaks at 7.79 (AD 100) and falls to 6.50 by AD 600, a drop of 0.79 global SD.
- **Verdict:** Descriptive only; no verdict. This entry feeds the B2 operationalisation discussion.

---

## 001 — Holdout draw (blind)

- **Date:** 2026-10-18
- **Script:** `src/g2_holdout_draw.py` → `holdout_ngas.csv`
- **Rule (fixed before running):** eligible = NGAs with ≥ 10 NGA-century rows, excluding Latium (already inspected). Draw 6 with `default_rng(20261018)`.
- **Result:**
  - Holdout = Basin of Mexico, Kachi Plain, Middle Yellow River Valley, Paris Basin, Susiana, Valley of Oaxaca. There were 23 eligible NGAs.
  - 25 of 123 holdout polities are shared with training NGAs (multi-region empires, e.g. Achaemenids, Rome). The holdout is therefore not fully independent at the polity level, so the holdout evaluation is also run on non-shared polity periods.
- **Verdict:** n/a (procedural).

## 002 — Coverage scan (blind)

- **Date:** 2026-10-18
- **Script:** `src/g2_coverage.py` → `docs/g2_coverage.csv`. Training NGAs only. Counts coded cells; never reads values.
- **Result:**
  - Polity population 37% coded; territory 39%; capital population 56%.
  - Government variables 56–74%; infrastructure 42–73%; fortification 53–90%.
  - Warfare-intensity markers (sack, destruction, annexation) 27–45%.
  - Army size 3%.
  - **No famine, epidemic or yield-shock variable exists in Equinox.**
- **Verdict:** HS6 (legibility) is untestable with Equinox. B proxies are sparse, so multiple imputation is essential.

## 003 — Phase 2: rebuild the complexity components and SPC

- **Date:** 2026-10-18
- **Scripts:** `src/p2_rebuild_spc.py` → `docs/p2_summary.txt`, `docs/p2_pca.csv`; `src/p2_pc1_by_era.py` → `docs/p2_pc1_by_era.txt`
- **Data:** Equinox2020 @ `602c7cd`; all 35 NGAs. This is a measure-level reproduction; no trajectories are output.
- **Result:**
  - **All 8 components reproduced exactly from raw TSDat123** (100% match on coded rows, 0 NA-pattern mismatches). The reverse-engineered rules are documented in the script docstring.
  - **The release's aggregation codes missing as absent in two components:**
    - Info = sum of 13 variables / 13, so any missing variable counts as 0. That affects 1,267 of 1,494 rows; 208 rows with all variables missing get Info = 0.
    - Gov treats missing ExamSyst and MeritProm as 0; 172 rows with all variables missing get Gov = 0.
  - **PC1 variance explained** (8 components):

    | Missing-data treatment | All rows | Unique rows, no duplicates |
    |---|---|---|
    | Release imputation | 84.3% | 79.2% |
    | Complete cases | 69–71% | 70–72% |
    | Multiple imputation (MI) | 81.4% | 76–77% |

    The paper reports "about three-quarters"; a secondary source gives 77.2%, on 9 components and 2017 data. **Consistent.**
  - **Loadings** are near-equal (0.31–0.39) in every treatment. Infra is consistently lowest.
  - **Missing-as-absent vs missing-as-missing** makes no difference to the measure: PC1 variance 81.4% vs 81.4% under MI, and scores correlate r = 0.995 with release SPC. Its effect on *events* (collapse detection) is untested.
  - **PC1 is not just a shared long-run trend.** Within eras it explains 65% (before −2000), 77%, 81% and 80%; within NGAs (demeaned), 87%.
  - **The reduced C1** (Hier, Gov, Info, Money) has PC1 = 80–87%, so a single dimension survives removing scale and Infra.
- **Verdict:** **Q1 reproduced.** A single complexity dimension holds across treatments, eras and the reduced variable set. **Discrepancy documented:** Equinox has 8 components, not the paper's 9, because writing and texts are merged into Info, and the exact 77% depends on the row selection.

## 004 — HS3 collinearity pre-check (blind to outcomes)

- **Date:** 2026-10-18
- **Script:** `src/g2_oc_yield_collinearity.py` → `docs/g2_oc_yield.txt`
- **Result:**

  | Pair | Pearson | Within-NGA |
  |---|---|---|
  | OC-A ~ log yield | 0.53 | 0.68 |
  | OC-B ~ log yield | 0.18 | 0.24 |

  148 pre-agricultural (yield = 0) training rows.
- **Verdict:** HS3 is testable (below the 0.8 bar). Overlap between OC-A and yield is substantial, so the SIMEX safeguard matters.

## 005 — Polaris2026 located, structure check (blind)

- **Date:** 2026-10-18
- **Source:** `Seshat-Global-History-Databank/build_polaris_dataset` @ `55ca5fb`. `Polaris2026.xlsx` sha256 `cf60c9f7…6c41`. The repo also holds `Equinox2020.05.2023.xlsx`.
- **Script:** inline, output in `docs/g2_polaris_structure.txt`. Counts and codebook only.
- **Result:**
  - 626 polities, 35 home NGAs (all 6 holdout NGAs present), 42 regions.
  - **Long format only:** no century grid, so a grid builder is needed for the Phase 5 rerun.
  - ~~All 77 social-complexity variables map to Equinox names.~~ **Corrected in 006:** that count included "not found" strings, and the release's crosswalk column is misaligned.
  - Range-coded share 12.7%; disputed and uncertain values each 0.6%.
  - **CrisisDB sheet:** 166 crises in 150 polities, 35 regions, −2200 to 1942.
    - 21 consequence flags: decline, collapse, epidemic, fragmentation, conquest, constitution, public goods and others.
    - Coded A / P / IA / IP / DIS / SU, fully non-null.
- **Verdict:**
  - CrisisDB exists publicly inside Polaris.
  - **It is a list of crises only.** A polity-century *not* in CrisisDB is not coded as "no crisis". Using absence as zero would repeat the moralizing-gods error, so CrisisDB can only be used *conditional on a crisis*.
  - HS6 moves from "untestable" to "possibly testable within crises" (see PREREG HS6).

## 006 — Polaris2026 century grid and PC1 (measure-level)

- **Date:** 2026-10-18
- **Script:** `src/p5_polaris_grid.py` → `data/interim/polaris_grid.csv` (gitignored), `docs/p5_polaris_pc1.txt`
- **Data-quality finding:** Polaris2026's `Variables.equinox_variable_name` crosswalk is **misaligned**. For example:
  - `military_level` maps to "elite status is hereditary"
  - `professional_military_officer` maps to "Professional Lawyers"
  - `nonwritten_record` maps to "Written records"
  - `religious_literature` maps to "Scientific literature"

  Many others are "not found". A hand-written crosswalk by variable name is used instead (in the script).
- **Grid rules:**
  - polity → NGA via `homeNGA`; 251 of 626 polities have none and are dropped
  - a polity is active for the centuries within its start–end years
  - dated values override undated ones
  - one polity per NGA-century, the one with the most coded variables
  - codes P = 1, IP = 0.9, A = 0, IA = 0.1, SU/U = NA
- **Result:**
  - 1,406 NGA-centuries, 35 NGAs, 363 polities.
  - Coverage: population 38%, territory 39%, Gov 88%, Info 85%.
  - **PC1 variance:** complete case 69.8% (n = 292); MI(20) 79.2% ± 0.2%. Loadings near-equal (0.33–0.39).
- **Verdict:** **the single dimension reproduces on Polaris2026.** Equinox gave 69.4% complete case and 81.4% MI. The grid rules are my own, not Seshat's, so the Phase 5 Equinox-vs-Polaris comparison is also a test of these rules.
