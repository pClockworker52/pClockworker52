"""Synthetic validation of src/tainter_lib.py. No Seshat data is touched.
Run: python -I tests/test_synthetic.py   (exits non-zero on failure)
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import tainter_lib as tl  # noqa: E402


def test_collapse_detector():
    # rise, then a 1.5-unit drop that persists 3 centuries, then a 1-century blip that must NOT count
    c = [0, 1, 2, 3, 3, 1.4, 1.4, 1.5, 3, 3, 3, 1.5, 3, 3]
    p = pd.DataFrame({"NGA": "x", "Time": np.arange(len(c)) * 100, "C": c})
    out = tl.add_collapse(p, sd=1.0, thr=1.0)
    assert out.collapse_event.tolist() == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], out.collapse_event.tolist()
    assert out.in_collapse.tolist()[5:8] == [1, 1, 1]
    assert out.y_next2.tolist()[3:5] == [1, 1]


def test_neg_return():
    p = pd.DataFrame({"NGA": "x", "Time": [0, 100, 200, 300, 400],
                      "C": [0, 1, 2, 3, 4], "B": [0, 1, 2, 2, 0.8]})
    out = tl.add_neg_return(p, w=3)
    nr = out.NegReturn.tolist()
    assert np.isnan(nr[:3]).all() and nr[3] == 0 and nr[4] == 1, nr


def simulate(effect_or, n_nga=30, T=60, seed=1, drop=1.5, growth=0.1):
    rng = np.random.default_rng(seed)
    rows = []
    for k in range(n_nga):
        C, B, noise = [0.0], [0.0], 0.0
        for t in range(1, T):
            noise = 0.7 * noise + rng.normal(0, 0.15)
            c_prev = C[-1]
            # negative-return state from the last 3 centuries
            nr = len(C) >= 4 and (C[-1] - C[-4] > 0) and (B[-1] - B[-4] <= 0)
            p = 0.02 * (effect_or if nr else 1.0)
            c = c_prev - drop if rng.random() < p else c_prev + growth + rng.normal(0, 0.05)
            C.append(c)
            B.append(np.sqrt(max(c, 0) + 1) + noise)
        rows.append(pd.DataFrame({"NGA": f"n{k}", "Time": np.arange(T) * 100, "C": C, "B": B}))
    panel = pd.concat(rows)
    return tl.add_collapse(tl.add_neg_return(panel), sd=1.0)


def test_recovers_effect_and_null():
    for eff, expect in ((5.0, "effect"), (1.0, "null")):
        d = tl.t1_frame(simulate(eff))
        orr, n = tl.logit_or(d, "y_next2", "NegReturn")
        ci, _ = tl.cluster_bootstrap_or(d, "y_next2", "NegReturn", n_boot=200)
        print(f"{expect}: OR={orr:.2f} CI={np.round(ci, 2)} n={n} events={int(d.y_next2.sum())}")
        if expect == "effect":
            assert ci[0] > 1, "planted effect not recovered"
        else:
            assert ci[0] <= 1 <= ci[1], "false positive under the null"


def test_placebo_centred():
    d = tl.t1_frame(simulate(5.0))
    pl = tl.placebo_or(d, "y_next2", "NegReturn", n=100)
    obs = tl.logit_or(d, "y_next2", "NegReturn")[0]
    print(f"placebo median OR={np.median(pl):.2f}; observed {obs:.2f} > 95th pct {np.percentile(pl, 95):.2f}")
    assert obs > np.percentile(pl, 95)


if __name__ == "__main__" and len(sys.argv) == 1:
    for f in (test_collapse_detector, test_neg_return, test_recovers_effect_and_null, test_placebo_centred):
        f()
        print("PASS", f.__name__)


def test_t1_runner_end_to_end():
    """Run src/p4_run_t1.run() on a synthetic panel shaped like TSDat123 (bypasses the signature guard)."""
    import p4_run_t1 as r
    rng = np.random.default_rng(7)
    sim = simulate(5.0, n_nga=20, T=50, seed=3, drop=4.0, growth=0.05)
    d = sim[["NGA", "Time"]].copy()
    d["PolID"], d["PropCoded"] = "p", 90.0
    for c in tl.C_COMPONENTS:  # components share the planted C plus noise
        d[c] = sim.C.values + rng.normal(0, 0.1, len(d))
    d["B"] = np.where(rng.random(len(d)) < 0.3, np.nan, sim.B.values)
    d["era"] = 0
    mi = pd.concat([d[["NGA", "PolID", "Time"]].assign(Pop=sim.B.values, n=k + 1) for k in range(r.N_DRAWS)])
    r.build = lambda _x: (d, mi)
    r.N_DRAWS, r.N_BOOT_PER_DRAW, r.N_PLACEBO = 2, 20, 20
    res = r.run("unused", dry=False, holdout=False)
    assert set(res) >= {"drop", "mi", "worst", "placebo_p95", "n_events", "loo_share_or_gt1"}
    assert res["n_events"] >= 10, res["n_events"]
    assert res["mi"]["OR_median"] > 1


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "runner":
    test_t1_runner_end_to_end()
    print("PASS test_t1_runner_end_to_end")
