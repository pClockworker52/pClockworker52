"""G2: write the DRAFT variable-role contract (variable_roles.csv). Each variable gets exactly one role.
Roles: C, B, OC, control, shock, response, unused. The 'alt' column lists the alternative definitions for the battery.
Usage: python -I src/g2_variable_roles.py <equinox.xlsx> docs/g2_coverage.csv
"""
import sys
import pandas as pd

var = pd.read_excel(sys.argv[1], "Variables")[["ShortName", "Variable", "Category"]]
cov = pd.read_csv(sys.argv[2])[["ShortName", "share_coded", "ngas_with_any"]]
ROLE = {
    "scale": ("B", "Scale CCs: Pop, Terr = benefit proxy; Cap kept out of B (overlaps cities = option closure)", "C (C_full, circular variant, flagged)"),
    "levels": ("C", "Hier CC (AdmLev, MilLev, SettlHier; ReligLev only in Hier4)", ""),
    "government": ("C", "Gov CC", ""),
    "writing": ("C", "Info CC", ""),
    "texts": ("C", "Info CC", ""),
    "money": ("C", "Money CC (ordinal 1-6)", ""),
    "infrastruct": ("OC", "OC-A: fixed, maintained capital; removed from C", "C (C_full)"),
    "MilFort": ("OC", "OC-B: fortification; outside SPC", ""),
    "WarType": ("control", "warfare pressure: confounder for OC-B (fortification ~ threat)", ""),
    "WarDist": ("unused", "", ""),
    "WarIntensity": ("shock", "candidate shock markers (Sack, Destruction, Annexation); 27-45% coded", ""),
    "ArchWar": ("shock", "archaeological violence evidence; sparse (24-36%)", ""),
    "Stratification": ("unused", "", ""),
    "AA": ("unused", "Axial Age vars: potential 'perception/model-revision' proxies? flagged for Q2 workshop", ""),
    "MSP": ("unused", "moralizing religion; avoid (retraction history; not in any hypothesis)", ""),
}
rows = []
for _, r in var.iterrows():
    role, note, alt = ROLE.get(r.Category, ("unused", "military technology", ""))
    if r.ShortName == "CapPop":
        role, note, alt = "unused", "Cap CC: ambiguous (scale vs urban fixed capital); excluded from B and OC", "C (C_full)"
    if r.ShortName == "ReligLev":
        role, note = "unused", "only in Hier4 variant; release Hier uses 3 levels"
    if r.ShortName in ("NonPhWrit", "PhAlph"):
        role, note = "unused", "not used by release Info CC"
    rows.append({**r.to_dict(), "role": role, "alt": alt, "note": note})
out = pd.DataFrame(rows).merge(cov, on="ShortName", how="left")
# non-TSDat sources
extra = pd.DataFrame([
    {"ShortName": "HistYield", "Variable": "Agricultural productivity t/ha/y (HistYield+ sheet)", "Category": "agri",
     "role": "control", "alt": "", "note": "gradient-rival control for H-S3; modelled estimate; varies within NGA over time (mean within-NGA SD of log10 yield 0.19 vs between-NGA 0.34); 0 = pre-agricultural"},
    {"ShortName": "FAO.Crop", "Variable": "Staple crop (NGAs sheet)", "Category": "agri",
     "role": "control", "alt": "OC-C", "note": "grain vs tuber; cross-NGA only"},
    {"ShortName": "PolityDuration", "Variable": "Polity Start-End (Polities sheet)", "Category": "derived",
     "role": "B", "alt": "", "note": "secondary benefit proxy B2; risk: mechanically tied to turnover"},
])
out = pd.concat([out, extra], ignore_index=True)
out.insert(0, "status", "DRAFT-unsigned")
out.to_csv("variable_roles.csv", index=False)
print(out.groupby("role").size().to_string())
# disjointness check (the contract's purpose)
assert out.ShortName.is_unique, "a variable appears twice"
print("disjoint: OK (one role per variable)")
