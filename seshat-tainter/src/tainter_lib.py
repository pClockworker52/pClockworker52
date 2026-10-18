"""Core definitions for the Phase 4/5 tests (T1, and the shared parts of HS1-HS3).

Implements the ★ primary definitions of docs/B2_options.md:
  C1  = PC1 of standardised [Hier, Gov, Info, Money] (missing-as-missing), fitted on training rows
  B1  = log10 polity population
  R1  = negative-return episode at t: C(t) - C(t-w) > 0 and B(t) - B(t-w) <= 0, w = 3 centuries
  K1  = collapse event: C falls >= thr * sd below its running max over the prior 3 centuries
        and stays below that line for >= 2 consecutive centuries. ★ sd = sd_delta (SD of 3-century
        changes), thr = 2.0; alternative K1-global: sd = SD of C over all rows, thr = 1.0
Only validated on synthetic data (tests/test_synthetic.py) until PREREG is signed.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.decomposition import PCA

C_COMPONENTS = ["Hier", "Gov", "Info", "Money"]


def fit_c1(train: pd.DataFrame, cols=C_COMPONENTS):
    """Return a function mapping a frame with `cols` to C1 scores (fitted on train only)."""
    mu, sd = train[cols].mean(), train[cols].std()
    p = PCA(n_components=1).fit(((train[cols] - mu) / sd).values)
    w = p.components_[0] * np.sign(p.components_[0].sum())
    return lambda d: ((d[cols] - mu) / sd).values @ w


def sd_delta(panel: pd.DataFrame, w: int = 3, c="C") -> float:
    """Pooled SD of w-century changes in C: the reference scale for K1 (★ since 2026-10-18 draft)."""
    assert not panel.duplicated(["NGA", "Time"]).any(), "panel must have one row per NGA-century"
    ds = []
    for _, g in panel.sort_values("Time").groupby("NGA", sort=False):
        lag = g.set_index("Time")[c].reindex(g.Time - 100 * w).values
        ds.append(g[c].values - lag)
    d = np.concatenate(ds)
    return float(np.nanstd(d, ddof=1))


def add_neg_return(panel: pd.DataFrame, w: int = 3, c="C", b="B") -> pd.DataFrame:
    """R1. Assumes one row per NGA-century, Time in years (step 100)."""
    out = []
    for _, g in panel.sort_values("Time").groupby("NGA", sort=False):
        g = g.copy()
        lag = g.set_index("Time")[[c, b]].reindex(g.Time - 100 * w).values
        dc, db = g[c].values - lag[:, 0], g[b].values - lag[:, 1]
        nr = np.where(np.isnan(dc) | np.isnan(db), np.nan, ((dc > 0) & (db <= 0)).astype(float))
        out.append(g.assign(NegReturn=nr))
    return pd.concat(out)


def add_collapse(panel: pd.DataFrame, sd: float, thr: float = 1.0, back: int = 3, persist: int = 2,
                 c="C") -> pd.DataFrame:
    """K1. Adds `collapse_event` (1 at the first century of each event), `in_collapse` (1 while below
    the line of an ongoing event) and `y_next2` (an event starts in t+1 or t+2)."""
    out = []
    for _, g in panel.sort_values("Time").groupby("NGA", sort=False):
        g = g.reset_index(drop=True).copy()
        cv = g[c].values
        n = len(cv)
        ev, inside = np.zeros(n), np.zeros(n)
        t = back
        while t < n:
            ref = np.nanmax(cv[t - back:t]) if np.isfinite(cv[t - back:t]).any() else np.nan
            line = ref - thr * sd
            if np.isfinite(cv[t]) and np.isfinite(line) and cv[t] <= line:
                run = 0
                while t + run < n and np.isfinite(cv[t + run]) and cv[t + run] <= line:
                    run += 1
                if run >= persist:
                    ev[t] = 1
                    inside[t:t + run] = 1
                    t += run
                    continue
            t += 1
        nxt = np.zeros(n)
        nxt[:-1] = ev[1:]
        nxt[:-2] = np.maximum(nxt[:-2], ev[2:])
        out.append(g.assign(collapse_event=ev, in_collapse=inside, y_next2=nxt))
    return pd.concat(out)


def firth_logit(X: np.ndarray, y: np.ndarray, maxiter=100, tol=1e-8):
    """Firth (1993) bias-reduced logistic regression: finite estimates under separation / rare events."""
    beta = np.zeros(X.shape[1])
    for _ in range(maxiter):
        p = 1 / (1 + np.exp(-(X @ beta)))
        w = p * (1 - p)
        info = X.T @ (w[:, None] * X)
        inv = np.linalg.pinv(info)
        h = w * np.einsum("ij,jk,ik->i", X, inv, X)
        step = inv @ (X.T @ (y - p + h * (0.5 - p)))
        beta = beta + np.clip(step, -5, 5)
        if np.max(np.abs(step)) < tol:
            break
    return beta


def logit_or(df: pd.DataFrame, y: str, x: str, controls=(), add_const=True):
    """Odds ratio for x from a Firth-penalised logit of y on x + controls."""
    d = df[[y, x, *controls]].dropna()
    X = d[[x, *controls]].astype(float)
    X = X[[c for c in X.columns if c == x or X[c].std() > 0]]  # drop constant controls (e.g. empty era dummies)
    if add_const:
        X = sm.add_constant(X, has_constant="add")
    beta = firth_logit(X.values, d[y].astype(float).values)
    return float(np.exp(beta[list(X.columns).index(x)])), len(d)


def cluster_bootstrap_or(df, y, x, controls=(), cluster="NGA", n_boot=2000, seed=0):
    rng = np.random.default_rng(seed)
    groups = df[cluster].unique()
    by = {k: v for k, v in df.groupby(cluster)}
    ors = []
    for _ in range(n_boot):
        pick = rng.choice(groups, size=len(groups), replace=True)
        b = pd.concat([by[k] for k in pick], ignore_index=True)
        try:
            ors.append(logit_or(b, y, x, controls)[0])
        except Exception:
            continue
    ors = np.array(ors)
    return np.nanpercentile(ors, [2.5, 97.5]), ors


def placebo_or(df, y, x, controls=(), n=1000, seed=0):
    """Circularly shift each NGA's outcome series: keeps event count and autocorrelation."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        parts = []
        for _, g in df.groupby("NGA"):
            parts.append(g.assign(**{y: np.roll(g[y].values, rng.integers(1, max(2, len(g))))}))
        try:
            out.append(logit_or(pd.concat(parts), y, x, controls)[0])
        except Exception:
            continue
    return np.array(out)


def t1_frame(panel: pd.DataFrame) -> pd.DataFrame:
    """At-risk rows for T1: not already inside a collapse."""
    return panel[panel.in_collapse == 0]
