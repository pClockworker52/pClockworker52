"""Phase 2 check: is PC1 dominance only a shared long-run trend? PC1 variance within eras (release ImpSCDat).
Measure-level only, no trajectories. Usage: python -I src/p2_pc1_by_era.py <equinox.xlsx>
"""
import sys
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

CC = ["Pop", "Terr", "Cap", "Hier", "Gov", "Infra", "Info", "Money"]
imp = pd.read_excel(sys.argv[1], "ImpSCDat")
for lo, hi in [(-10000, -2001), (-2000, -1), (0, 999), (1000, 1900)]:
    d = imp[(imp.Time >= lo) & (imp.Time <= hi)]
    Z = (d[CC] - d[CC].mean()) / d[CC].std()
    p = PCA().fit(Z.fillna(0))
    print(f"{lo:>6}..{hi:>5}: n={len(d):4d} PC1 var={p.explained_variance_ratio_[0]:.3f} PC2={p.explained_variance_ratio_[1]:.3f}")
# within-NGA demeaned (removes between-region level differences)
Z = imp[CC] - imp.groupby("NGA")[CC].transform("mean")
Z = Z / Z.std()
p = PCA().fit(Z)
print(f"within-NGA demeaned: PC1 var={p.explained_variance_ratio_[0]:.3f} loadings={np.round(p.components_[0], 2)}")
