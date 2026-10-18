"""G2: blind coverage scan. Reports only how often each variable is coded (not -999), never its values.
Training NGAs only (holdout excluded). Usage: python -I src/g2_coverage.py <equinox.xlsx> <out.csv>
"""
import sys
import pandas as pd

xlsx, out = sys.argv[1], sys.argv[2]
hold = set(pd.read_csv("holdout_ngas.csv").NGA)
ts = pd.read_excel(xlsx, "TSDat123")
ts = ts[~ts.NGA.isin(hold)]
var = pd.read_excel(xlsx, "Variables")[["ShortName", "Variable", "Category"]]
cols = [c for c in ts.columns[4:] if c not in ("uniq", "Dupl")]
rows = []
for c in cols:
    coded = ts[c] != -999
    rows.append({"ShortName": c, "share_coded": round(coded.mean(), 3),
                 "ngas_with_any": int(ts.loc[coded, "NGA"].nunique()), "n_rows_coded": int(coded.sum())})
cov = pd.DataFrame(rows).merge(var, on="ShortName", how="left")
cov.to_csv(out, index=False)
print(f"training NGA-centuries: {len(ts)}, NGAs: {ts.NGA.nunique()}")
print(cov.sort_values(["Category", "share_coded"]).to_string(index=False))
y = pd.read_excel(xlsx, "HistYield+", header=None)
print("\nHistYield+ rows (NGAs):", y.shape[0] - 1, " time points:", y.shape[1] - 1)
