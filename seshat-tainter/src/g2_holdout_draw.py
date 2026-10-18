"""G2: draw the locked holdout NGAs. Blind step: uses only NGA names and NGA-century counts.

Rule (fixed before running): eligible = NGAs with >= 10 NGA-century rows in TSDat123,
excluding Latium (already inspected in Phase 1). Draw 6 with numpy default_rng(20261018).
Usage: python -I src/g2_holdout_draw.py <equinox.xlsx>
"""
import sys
import numpy as np
import pandas as pd

ts = pd.read_excel(sys.argv[1], "TSDat123", usecols=["NGA"])
counts = ts.NGA.value_counts().sort_index()
eligible = sorted(n for n, c in counts.items() if c >= 10 and n != "Latium")
rng = np.random.default_rng(20261018)
holdout = sorted(rng.choice(eligible, size=6, replace=False).tolist())
print(f"eligible ({len(eligible)}):", eligible)
print("HOLDOUT:", holdout)
pd.Series(holdout, name="NGA").to_csv("holdout_ngas.csv", index=False)
