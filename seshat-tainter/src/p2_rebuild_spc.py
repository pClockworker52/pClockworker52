"""Phase 2: rebuild the Seshat complexity components (CCs) and SPC (PC1) from raw TSDat123.

Outputs only measure-level results (loadings, variance explained, agreement with the
release). It never prints or plots per-NGA trajectories: those are outcomes, reserved for Phase 3.

Treatments of missing data in the Gov and Info components:
  R  = release rules (reverse-engineered, verified exact): Info = sum of 13 vars / 13 (NA -> 0);
       Gov = mean of 11 vars with ExamSyst, MeritProm NA -> 0, and all-NA -> 0
  M  = missing-as-missing: mean over coded vars; NA if none coded
Imputation of remaining NA CCs:
  rel  = use the release's single imputation (ImpSCDat) for scale/Infra/Money/Hier
  cc   = complete cases only
  mi   = sklearn IterativeImputer, 20 posterior draws (seeded)

Usage: python -I src/p2_rebuild_spc.py <equinox.xlsx> <out_prefix>
"""
import sys
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer

XLSX, OUT = sys.argv[1], sys.argv[2]
KEY = ["NGA", "PolID", "Time"]
CC = ["Pop", "Terr", "Cap", "Hier", "Gov", "Infra", "Info", "Money"]
GOV = ["ProfOfficer", "ProfSoldier", "ProfPriest", "FullTBur", "ExamSyst", "MeritProm",
       "GovtBldg", "Court", "LegCode", "Judge", "Lawyer"]
INFRA = ["Irrigation", "WaterSuppl", "Market", "FoodStor", "Road", "Bridge", "Canal", "Port",
         "Mine", "Courier", "PostStation", "PostService"]
INFO = ["Mnemonic", "NonWRecord", "WRecord", "Script", "Lists", "Calendar", "SacrTxt", "ReligLit",
        "PractLit", "History", "Philosophy", "SciLit", "Fiction"]  # NonPhWrit, PhAlph not used by release
MONEY = ["Article", "Token", "PrecMetal", "ForCoin", "IndigCoin", "PaperCurr"]  # ordinal levels 1..6

ts = pd.read_excel(XLSX, "TSDat123").replace(-999, np.nan)
aggr = pd.read_excel(XLSX, "AggrSCWarAgriRelig")
imp = pd.read_excel(XLSX, "ImpSCDat")
spc = pd.read_excel(XLSX, "SPC_MilTech")


def build(ts, rule):
    d = ts[KEY + ["uniq", "Dupl"]].copy()
    d["Pop"], d["Terr"], d["Cap"] = np.log10(ts.PolPop), np.log10(ts.PolTerr), np.log10(ts.CapPop)
    d["Hier"] = ts[["AdmLev", "MilLev", "SettlHier"]].mean(axis=1)
    d["Infra"] = ts[INFRA].mean(axis=1)
    d["Money"] = pd.concat([ts[c] * i for i, c in enumerate(MONEY, 1)], axis=1).max(axis=1) / 6
    if rule == "R":
        g = ts[GOV].copy()
        g[["ExamSyst", "MeritProm"]] = g[["ExamSyst", "MeritProm"]].fillna(0)
        d["Gov"] = g.mean(axis=1).fillna(0)
        d["Info"] = ts[INFO].fillna(0).sum(axis=1) / len(INFO)
    else:
        d["Gov"] = ts[GOV].mean(axis=1)
        d["Info"] = ts[INFO].mean(axis=1)
    return d


def pc1(X):
    Z = (X - X.mean()) / X.std()
    p = PCA().fit(Z)
    load = p.components_[0] * np.sign(p.components_[0].sum())
    return p.explained_variance_ratio_[0], load, Z.values @ load


lines, rows = [], []
R, M = build(ts, "R"), build(ts, "M")

# 1. verify release rules reproduce AggrSCWarAgriRelig exactly
chk = R.merge(aggr, on=KEY, suffixes=("", "_rel"))
for c in CC:
    ok = chk[c].notna() & chk[c + "_rel"].notna()
    exact = (np.abs(chk[c] - chk[c + "_rel"])[ok] < 1e-6).mean()
    na_mm = (chk[c].isna() != chk[c + "_rel"].isna()).sum()
    lines.append(f"verify {c:5s}: exact on coded rows = {exact:.3f}; NA-pattern mismatches = {na_mm}")

# how much the R rules fill in
lines.append(f"rows where Info has >=1 missing var (R counts them as absent): {ts[INFO].isna().any(axis=1).sum()} of {len(ts)}")
lines.append(f"rows where Gov has >=1 missing var: {ts[GOV].isna().any(axis=1).sum()}; all 11 missing (R sets Gov=0): {ts[GOV].isna().all(axis=1).sum()}")
lines.append(f"rows where Info all 13 missing (R sets Info=0): {ts[INFO].isna().all(axis=1).sum()}")

subsets = {"all": lambda d: d, "uniq&Dupl=n": lambda d: d[(d.uniq == "y") & (d.Dupl == "n")]}
rel_spc = imp.merge(spc, on=KEY)[KEY + ["SPC"]]


def record(name, X, keys, cc=CC):
    v, load, score = pc1(X[cc])
    s = pd.concat([keys.reset_index(drop=True), pd.Series(score, name="pc1")], axis=1).merge(rel_spc, on=KEY)
    r = np.corrcoef(s.pc1, s.SPC)[0, 1] if len(s) > 2 else np.nan
    rows.append({"treatment": name, "n": len(X), "pc1_var": round(v, 4), "r_with_release_SPC": round(r, 4),
                 **{f"L_{c}": round(l, 3) for c, l in zip(cc, load)}})


for sname, sel in subsets.items():
    # release
    d = sel(imp)
    record(f"release ImpSCDat | {sname}", d, d[KEY])
    for rule, B in (("R", R), ("M", M)):
        b = sel(B)
        # rel: fill remaining NA with release single imputation
        f = b.merge(imp[KEY + CC], on=KEY, suffixes=("", "_imp"))
        for c in CC:
            f[c] = f[c].fillna(f[c + "_imp"])
        record(f"{rule} + release-imputation | {sname}", f, f[KEY])
        cc_ = b.dropna(subset=CC)
        record(f"{rule} + complete-case | {sname}", cc_, cc_[KEY])
        vs = []
        for k in range(20):
            X = IterativeImputer(sample_posterior=True, random_state=k, max_iter=25).fit_transform(b[CC])
            vs.append(pc1(pd.DataFrame(X, columns=CC))[0])
        rows.append({"treatment": f"{rule} + MI(20) | {sname}", "n": len(b),
                     "pc1_var": round(float(np.mean(vs)), 4), "pc1_var_sd": round(float(np.std(vs)), 4)})

# reduced C for the tests: no scale (-> B), no Infra (-> option closure)
CRED = ["Hier", "Gov", "Info", "Money"]
for sname, sel in subsets.items():
    b = sel(M)
    vs = [pc1(pd.DataFrame(IterativeImputer(sample_posterior=True, random_state=k, max_iter=25)
                           .fit_transform(b[CRED]), columns=CRED))[0] for k in range(20)]
    rows.append({"treatment": f"C_reduced(Hier,Gov,Info,Money) M + MI(20) | {sname}", "n": len(b),
                 "pc1_var": round(float(np.mean(vs)), 4), "pc1_var_sd": round(float(np.std(vs)), 4)})
    cc_ = b.dropna(subset=CRED)
    record(f"C_reduced M + complete-case | {sname}", cc_, cc_[KEY], CRED)

res = pd.DataFrame(rows)
res.to_csv(OUT + "_pca.csv", index=False)
with open(OUT + "_summary.txt", "w") as fh:
    fh.write("\n".join(lines) + "\n\n" + res.to_string(index=False) + "\n")
print("\n".join(lines)); print(res.to_string(index=False))
