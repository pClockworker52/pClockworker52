# Primer: Tainter and Seshat on one page

*Phase 1 tutor pass. Plain language, checked against sources where marked ✔. Items marked ⚠ still need checking against the primary text.*

## 1. What Tainter means by "complexity"

Tainter (1988) treats complexity as **structure, not sophistication**. A society is more complex when it has:
- more parts
- more kinds of parts (differentiated roles and occupations)
- more organisation tying them together (hierarchy layers, control, information flow, record-keeping)

Art, morals and technology don't count by themselves.

His argument as an engineer would put it:

| Step | Claim | What the engineer's version is |
|---|---|---|
| 1 | Societies are problem-solving organisations | The system responds to perturbations by adding structure |
| 2 | Structure needs a continuous energy throughput to persist | Dissipative structure: it has a maintenance load |
| 3 | More complexity means higher cost per capita | The maintenance load scales with structure |
| 4 | Returns on more complexity eventually diminish | A concave benefit curve B(C): dB/dC falls, then turns negative |

**Collapse** means a rapid, significant loss of an established level of sociopolitical complexity. It is not extinction. Once dB/dC < 0, shedding complexity is the *economical* move.

His main cases are Western Rome, the Classic Maya and Chaco. He rejected single-cause stories (depletion, invaders, catastrophe), because every society faces such shocks. The real question is why a society could no longer *afford* to absorb them.

⚠ **A condition worth testing.** Tainter also argues that collapse needs a **power vacuum**. A polity surrounded by peer competitors can't simply shed complexity, because a neighbour absorbs it instead. The prediction is: no peers, then collapse; peers present, then turnover or conquest. This maps directly onto the "polity turnover vs genuine complexity loss" distinction in our collapse definition. ⚠ Confirm the chapter and wording in the book. Also check the handoff's chapter numbers (1, 4, 6) against your edition's table of contents.

**The testing problem.** Tainter never measures dB/dC directly. His evidence is qualitative: Roman coin debasement, Maya monument investment and so on. Any quantitative test has to build a *proxy* for B, and that proxy must not share variables with C (otherwise the test is circular).

## 2. What Seshat is

- **Who and when.** Seshat: Global History Databank was founded in 2011 by Turchin, Whitehouse, François and others. Its purpose is to code historical and archaeological knowledge into variables so theories can be tested. The field is called *cliodynamics*.
- **Unit = NGA × century.** A *Natural Geographic Area* is a fixed patch of land, e.g. Latium. *Polities* succeed one another on that patch.
  - Each polity is coded once, sometimes with dated sub-values.
  - The release then lays these out on a 100-year grid.
  - **Important:** values are *polity-level*. In AD 100, "Latium" carries the population of the whole Roman Empire (50–60 M), not of the Latium region. ✔ (data, see §3)
- **Coding vocabulary.** ✔ (counted in Equinox2020)
  - Presence codes: `present`, `absent`, `inferred present`, `inferred absent`, `unknown`, `suspected unknown`
  - Value qualifiers: `simple`, `range` (e.g. 50–60 M), `list` (several dated values), `uncertain`, `disputed`
  - Every fact carries its research assistant and sources.
- **The 2018 result.** ✔ (abstract; precise figure still to be checked in Phase 2)
  - Data: 51 variables → 9 "complexity characteristics", across 414 polities in 30 NGAs over 10,000 years.
  - Result: one principal component (PC1, "SPC1") carries **about three-quarters** of the variance. A third-party summary gives 77.2%.
  - The Equinox release ships a pre-computed `SPC` (PC1 of 8 complexity components, from *single* imputation). Phase 2 rebuilds it from scratch.
  - Citation: Turchin et al., PNAS 115(2):E144–E151, doi:10.1073/pnas.1708800115.
- **The cautionary tale.** ✔
  - Whitehouse et al. (Nature, 2019) claimed that moralizing gods appear only *after* "megasocieties" of about 1 M people.
  - Beheim et al. (Nature 595, E29–E34, 2021) showed that about 61% of the moralizing-gods data points were missing, and that many unknowns had been recoded as *absent* before analysis.
  - Analysed on known data only, or with standard imputation, the result reversed: moralizing gods came first.
  - The paper was retracted in 2021. The authors' later "retake" maintains that the main result survives after corrections.
  - **Lesson for us:** how you code "missing" can decide the conclusion. That is Ground Rule 4.

## 3. What the data actually look like (Equinox2020, our local copy)

| Fact | Value |
|---|---|
| Coded facts (long format) | 47,477 rows; 35 NGAs; 373 polities; 135 variables |
| Missing NGA-century cells across 36 social-complexity variables | **41%** |
| Missing for polity population / territory | **63%** each |
| Imputation in the release | single (`ImpSCDat`) and 20-fold multiple (`Scale_MI`) |
| Agricultural productivity | `HistYield+` (t/ha/y per NGA per century) |

**What the 63% means for us.** Population and territory are the obvious "benefit" proxies, yet they are missing nearly two times in three. They also sit *inside* SPC. So the B proxy is both circular and sparse until we decide otherwise.

## 4. Latium end to end (output: `docs/p1_latium_output.txt`)

**Polity sequence:** 18 polity entries, from the Copper Age (−3600) through the Kingdom, Republic, Principate, Dominate (flagged `Dupl=y`, shared with another NGA), Western Empire, Ostrogoths, Exarchate of Ravenna and Republic of St Peter, to the Papal States (to 1800).

**The gaps are visible:**
- 458–492 (Odoacer) is not coded.
- 555–567 is not coded.
- 1309–1377 (the Avignon papacy) is not coded.

**SPC trajectory:**

| Period | SPC |
|---|---|
| Iron Age | 3.0 |
| Kingdom | 4.7 |
| Middle Republic | 6.6 |
| Principate (peak, AD 100) | **7.8** |
| Exarchate (600) | 6.5 |
| Then | flat ~6.5 for 1000 years |
| Papal States (1800) | 6.9 |

Rome's fall in Latium is a drop of **0.79 global SD**, about 1.3 SPC units. The fall is real but moderate. Gov, Info and Money barely drop, because the Church keeps records, courts and coinage alive. Hierarchy (8.2 → 5.3), Territory and Population carry most of the fall.

**What this means for the collapse threshold.** Tainter's flagship case might *not* count as a "collapse" under a strict threshold. We need to be careful not to tune the threshold until Rome qualifies. That would make the definition guarantee the result (false-positive checklist, item 2).

**Coding oddities to keep in mind:**
- **Courts:** coded `absent` for the Principate but `present` for the Ostrogoths. This is probably a coding artefact, not history.
- **Copper Age vs Bronze Age:** the Copper Age SPC (3.09) is *higher* than the Bronze Age (2.30), because the Copper Age's missing Pop/Terr/Cap were imputed. Imputation alone can create apparent "declines".

**Sources:**
- [Turchin et al. 2018 PNAS (CSH page)](https://csh.ac.at/publication/quantitative-historical-analysis-uncovers-a-single-dimension-of-complexity-that-structures-global-variation-in-human-social-organization/)
- [HRAF summary (77.2% figure)](https://hraf.yale.edu/documents/1172)
- [Retraction Watch on the moralizing-gods retraction](https://retractionwatch.com/2021/07/07/critique-topples-nature-paper-on-belief-in-gods/)
- [Beheim et al. 2021, Nature](https://www.doi.org/10.1038/S41586-021-03655-4)
- [Polaris2025 report, Cliodynamics](https://escholarship.org/uc/item/9wj6z91m)
- [Seshat data page](https://www.seshatdatabank.info/data)
- [Equinox data on GitHub](https://github.com/seshatdb/Equinox_Data)
