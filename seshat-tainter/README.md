# Testing Tainter with Seshat (and Sedentis v2)

The full brief is in `HANDOFF.md`. This file tracks status and how to continue.

## Status (2026-10-09, prepared on mobile)

| Phase | State |
|---|---|
| 0 Setup | ✅ Structure, pinned env, Equinox2020 fetch script. Polaris still needed (see below) |
| 1 Tutor pass | ✅ Drafted: `PRIMER.md`, Latium walkthrough, `LEARNING.md` Phase 1. **Check-in 1 pending** |
| C1 Workshop | 📝 Prepared, not run: `SEDENTIS_V2.md` |
| 2–6, C2–C4 | Not started |

## Continue on PC

1. **Set up the environment.**
   ```bash
   python -m venv .venv && . .venv/bin/activate
   pip install -r requirements.txt
   ./src/fetch_data.sh
   python -I src/p1_walkthrough_latium.py data/raw/equinox_data/Equinox_on_GitHub_June9_2022.xlsx
   ```
2. **Get Polaris.** The cloud container couldn't reach seshat-db.com or seshatdatabank.info. From the downloads page:
   - Get the Polaris2025 (or "Polaris-2026") spreadsheet → `data/raw/polaris/`.
   - Note the GitHub repo name for Polaris, if there is one. Then it can go into `fetch_data.sh`.
   - Check whether CrisisDB has a public download.
   - Get Cliopatria from Zenodo if you want maps (optional, Phase 3).
3. **Answer the open questions:**
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
