"""G2 / HS3 pre-check (blind to outcomes): can option closure be separated from productivity?
Correlation of OC-A (infrastructure mean) and OC-B (fortification mean) with log yield, training NGAs only.
Usage: python -I src/g2_oc_yield_collinearity.py <equinox.xlsx>
"""
import sys
import numpy as np
import pandas as pd

X = sys.argv[1]
hold = set(pd.read_csv("holdout_ngas.csv").NGA)
roles = pd.read_csv("variable_roles.csv")
ts = pd.read_excel(X, "TSDat123").replace(-999, np.nan)
ts = ts[~ts.NGA.isin(hold)]
infra = roles.query("Category == 'infrastruct'").ShortName.tolist()
fort = roles.query("Category == 'MilFort'").ShortName.tolist()
ts = ts.assign(OC_A=ts[infra].mean(axis=1), OC_B=ts[fort].mean(axis=1))

y = pd.read_excel(X, "HistYield+", header=0).iloc[:, :]  # row 0 = 'Time' row, first col = NGA
times = y.iloc[0, 1:].astype(float).values
y = y.iloc[:, :].T.reset_index(drop=True).T  # positional column labels
yl = (y.iloc[1:].set_index(0).set_axis(times, axis=1).stack().rename("yield").reset_index()
      .rename(columns={0: "NGA", "level_1": "Time"}))
yl["Time"] = yl.Time.astype(int); yl["yield"] = pd.to_numeric(yl["yield"], errors="coerce")
d = ts.merge(yl, on=["NGA", "Time"], how="left")
print("rows:", len(d), " with yield:", d["yield"].notna().sum(), " yield==0:", (d["yield"] == 0).sum())
d = d[d["yield"] > 0]
d["logY"] = np.log10(d["yield"].astype(float))
for oc in ("OC_A", "OC_B"):
    s = d[[oc, "logY"]].dropna()
    w = s.join(d.NGA).groupby("NGA")[[oc, "logY"]].transform(lambda v: v - v.mean())
    print(f"{oc}: n={len(s)} pearson={s.corr().iloc[0,1]:.2f} spearman={s.corr('spearman').iloc[0,1]:.2f}"
          f" | within-NGA pearson={w.corr().iloc[0,1]:.2f}")
print("between-NGA SD of mean logY:", round(d.groupby('NGA').logY.mean().std(), 3),
      " mean within-NGA SD:", round(d.groupby('NGA').logY.std().mean(), 3))
