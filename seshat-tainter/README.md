# Testing Tainter with Seshat (and Sedentis v2)

The full brief is in `HANDOFF.md`. This file tracks status and how to continue.

## Status (2026-10-18)

| Phase | State |
|---|---|
| 0 Setup | ✅ Structure, pinned env, Equinox2020 fetch script. Polaris still needed (see below) |
| 1 Tutor pass | ✅ `PRIMER.md`, Latium walk-through, `LEARNING.md` Phase 1. Check-in 1 pending |
| C1 Workshop | 🟡 Q1 decided (strict reading, 2026-10-18). Q1b–Q5 proposals pending (`SEDENTIS_V2.md` §7) |
| G2 Blind prep | ✅ Holdout locked (`holdout_ngas.csv`); coverage scan; draft `variable_roles.csv`; OC–yield collinearity check |
| 2 Reproduce | ✅ Done on Equinox. All 8 components rebuilt exactly; PC1 69–84% (log 003) |
| B2 / PREREG | 📝 Options in `docs/B2_options.md`; DRAFT blocks T1, HS1–HS6 in `PREREG.md`. **Unsigned: this is the stop point** |
| 3–6, C3–C4 | ⛔ Blocked until PREREG is signed. Phase 3 reveals outcomes, so it waits too |

## Continue on PC

1. **Set up the environment.**
   ```bash
   python -m venv .venv && . .venv/bin/activate
   pip install -r requirements.txt
   ./src/fetch_data.sh
   python -I src/p1_walkthrough_latium.py data/raw/equinox_data/Equinox_on_GitHub_June9_2022.xlsx
   ```
2. **Polaris: solved.** `fetch_data.sh` now also clones `Seshat-Global-History-Databank/build_polaris_dataset` (Polaris2026.xlsx, which includes a **CrisisDB** sheet). Cliopatria (Zenodo) is still optional for Phase 3 maps.
3. **Sign or amend:** `variable_roles.csv`, the ★ choices in `docs/B2_options.md`, and the DRAFT blocks in `PREREG.md`.
4. **Answer the open questions:**
   - `LEARNING.md` Phase 0 and Phase 1
   - `SEDENTIS_V2.md` §0 and §6

## Data and licence

Seshat data are © Seshat: Global History Databank, licensed CC BY-NC-SA. Any write-up must:
- include: "This research employed data from the Seshat Databank under Creative Commons Attribution Non-Commercial (CC By-NC SA) licensing."
- cite: Turchin et al. 2015, "Seshat: The Global History Databank", *Cliodynamics*.

`data/raw/` is gitignored. The snapshots are pinned by commit and SHA256 (see `ANALYSIS_LOG.md` 000).

## Layout

| Path | Contents |
|---|---|
| `src/` | Plain scripts, data path passed as an argument, no notebook state |
| `docs/` | Script outputs referenced from the logs |
| `figures/` | Plots |
| `PREREG.md` | Pass/fail criteria, signed before tests, never edited after |
| `ANALYSIS_LOG.md` | Numbered analysis entries |
| `LEARNING.md` | Per-phase notes and questions |
