"""Phase 4, test T1 (PREREG.md): do negative-return episodes precede collapse?

Refuses to run unless the T1 block in PREREG.md is signed ("Signed off: Peter ...").
--dry-run builds every input and prints only shapes / NA counts (no events, no estimates).
--holdout evaluates the locked holdout NGAs; additionally requires env CONFIRM_HOLDOUT=1.

Usage: python -I src/p4_run_t1.py <equinox.xlsx> [--dry-run] [--holdout]
Missing-data treatments (docs/B2_options.md §6): MD-drop, MD-MI (Scale_MI draws for Pop +
IterativeImputer for C components), MD-worst (B imputed against the hypothesis).
TODO before the signed run: range-sampling of range-coded values from CanonDat inside MD-MI.
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tainter_lib as tl  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KEY = ["NGA", "PolID", "Time"]
GOV = ["ProfOfficer", "ProfSoldier", "ProfPriest", "FullTBur", "ExamSyst", "MeritProm", "GovtBldg", "Court",
       "LegCode", "Judge", "Lawyer"]
INFO = ["Mnemonic", "NonWRecord", "WRecord", "Script", "Lists", "Calendar", "SacrTxt", "ReligLit", "PractLit",
        "History", "Philosophy", "SciLit", "Fiction"]
MONEY = ["Article", "Token", "PrecMetal", "ForCoin", "IndigCoin", "PaperCurr"]
N_DRAWS, N_BOOT_PER_DRAW, N_PLACEBO = 20, 100, 1000


def signed(block="T1"):
    txt = open(os.path.join(ROOT, "PREREG.md")).read()
    m = re.search(rf"### {block} .*?\nSigned off: (.*)", txt)
    return bool(m) and m.group(1).strip().lower().startswith("peter")


def build(xlsx):
    ts = pd.read_excel(xlsx, "TSDat123").replace(-999, np.nan)
    # 3 NGA-centuries carry two polities (Galilee -200, Kansai 700/800): keep one row per NGA-century,
    # preferring the non-duplicated polity (Dupl == 'n'), then the better-coded one (blind rule, log 008)
    ts = (ts.sort_values(["Dupl", "PropCoded"], ascending=[True, False])
            .drop_duplicates(["NGA", "Time"]).sort_values(["NGA", "Time"]).reset_index(drop=True))
    d = ts[KEY + ["PropCoded"]].copy()
    d["Hier"] = ts[["AdmLev", "MilLev", "SettlHier"]].mean(axis=1)
    d["Gov"], d["Info"] = ts[GOV].mean(axis=1), ts[INFO].mean(axis=1)          # missing-as-missing (rule M)
    d["Money"] = pd.concat([ts[c] * i for i, c in enumerate(MONEY, 1)], axis=1).max(axis=1) / 6
    d["B"] = np.log10(ts.PolPop)
    d["era"] = (d.Time // 1000).clip(-5, 1).astype(int)
    scale_mi = pd.read_excel(xlsx, "Scale_MI")[KEY + ["Pop", "n"]]
    return d, scale_mi


def make_panel(d, scale_mi, draw, treatment, train_fit):
    p = d.copy()
    comps = tl.C_COMPONENTS
    if treatment == "drop":
        p = p.dropna(subset=comps)
    else:
        p[comps] = IterativeImputer(sample_posterior=True, random_state=draw, max_iter=25).fit_transform(p[comps])
    if treatment == "mi":
        mi = scale_mi[scale_mi.n == draw + 1].drop(columns="n").rename(columns={"Pop": "B_mi"})
        p = p.merge(mi, on=KEY, how="left")
        p["B"] = p.B.fillna(p.B_mi)
        p = p.drop(columns="B_mi")
    p["C"] = train_fit(p)
    return p


def worst_case_b(p):
    """Fill missing B so that it works against T1: rising (no negative return) in the 3 centuries
    before an event, falling elsewhere. Uses events detected from C only."""
    out = []
    for _, g in p.sort_values("Time").groupby("NGA", sort=False):
        g = g.copy()
        pre = np.zeros(len(g), bool)
        ev = np.flatnonzero(g.collapse_event.values == 1)
        for e in ev:
            pre[max(0, e - 3):e] = True
        b = g.B.values.copy()
        known = b[~np.isnan(b)]
        last = known[0] if len(known) else 0.0  # leading gaps start from the NGA's first known value
        for i in range(len(b)):
            if np.isnan(b[i]):
                base = last
                b[i] = base + (1.0 if pre[i] else -1.0)
            last = b[i]
        out.append(g.assign(B=b))
    return pd.concat(out)


def run(xlsx, dry, holdout):
    hold = set(pd.read_csv(os.path.join(ROOT, "holdout_ngas.csv")).NGA)
    d, scale_mi = build(xlsx)
    train = d[~d.NGA.isin(hold)]
    fit_rows = train.dropna(subset=tl.C_COMPONENTS)
    c_fit = tl.fit_c1(fit_rows)
    ref = train.dropna(subset=tl.C_COMPONENTS)
    sd = tl.sd_delta(ref.assign(C=c_fit(ref)))  # K1 reference scale (★): SD of 3-century changes
    THR = 2.0
    target = d[d.NGA.isin(hold)] if holdout else train
    if dry:
        print(f"[dry-run] rows: all={len(d)} train={len(train)} target={len(target)} "
              f"NGAs target={target.NGA.nunique()} | C-fit rows={len(fit_rows)} | "
              f"B coded share={target.B.notna().mean():.2f} | Scale_MI draws={scale_mi.n.nunique()}")
        return
    controls = ["C", "PropCoded"] + [f"era_{e}" for e in sorted(d.era.unique())[1:]]
    results = {}
    for treatment in ("drop", "mi", "worst"):
        ors, boots = [], []
        for k in range(N_DRAWS if treatment != "drop" else 1):
            p = make_panel(target, scale_mi, k, "mi" if treatment == "worst" else treatment, c_fit)
            p = tl.add_collapse(p, sd=sd, thr=THR)
            if treatment == "worst":
                p = worst_case_b(p)
            p = tl.add_neg_return(p)
            p = pd.get_dummies(p, columns=["era"], prefix="era", dtype=float)
            p = p.assign(**{c: p.get(c, 0.0) for c in controls})
            f = tl.t1_frame(p)
            ors.append(tl.logit_or(f, "y_next2", "NegReturn", controls)[0])
            boots.append(tl.cluster_bootstrap_or(f, "y_next2", "NegReturn", controls,
                                                 n_boot=N_BOOT_PER_DRAW, seed=k)[1])
            if treatment == "mi" and k == 0:
                pl = tl.placebo_or(f, "y_next2", "NegReturn", controls, n=N_PLACEBO)
                results["placebo_p95"] = float(np.percentile(pl, 95))
                results["n_events"] = int(f.y_next2.sum())
                if not holdout:
                    loo = [tl.logit_or(f[f.NGA != n], "y_next2", "NegReturn", controls)[0]
                           for n in f.NGA.unique()]
                    results["loo_share_or_gt1"] = float(np.mean(np.array(loo) > 1))
        b = np.concatenate(boots)
        results[treatment] = {"OR_median": float(np.median(ors)), "CI95": np.percentile(b, [2.5, 97.5]).round(3).tolist()}
    print(results)
    return results


if __name__ == "__main__":
    args = sys.argv[1:]
    dry, hold = "--dry-run" in args, "--holdout" in args
    if not dry and not signed("T1"):
        sys.exit("T1 is not signed in PREREG.md: refusing to run (use --dry-run).")
    if hold and not dry and os.environ.get("CONFIRM_HOLDOUT") != "1":
        sys.exit("Holdout run requires CONFIRM_HOLDOUT=1 (final confirmation only).")
    run(args[0], dry, hold)
