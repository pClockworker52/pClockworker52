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
