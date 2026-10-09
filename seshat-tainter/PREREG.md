# PREREG.md

**Rules:**
- Pass/fail criteria are written here *before* each Phase 4+ test (Tainter) and each H-S test (Sedentis).
- Each block needs Peter's sign-off, with name and date.
- After sign-off, a block is never edited. Changes go into timestamped amendments below it.
- **Default verdict = no effect.** The null hypothesis is that complexity drops are unrelated to prior returns.
- Every headline result is rerun under at least three missing-data treatments: drop, impute-ranges and worst-case.

*Status: empty. Definitions (B2) are not yet chosen. See `docs/B2_options.md` once drafted on PC.*

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
