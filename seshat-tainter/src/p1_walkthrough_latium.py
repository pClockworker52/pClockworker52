"""Phase 1 tutor walk-through: one NGA (Latium) end to end, descriptive only.

Shows: polity sequence, raw coded facts with their uncertainty codes, and the
release's own pre-computed complexity components and SPC. No modelling.

Usage: python -I src/p1_walkthrough_latium.py data/raw/equinox_data/Equinox_on_GitHub_June9_2022.xlsx
"""
import sys
import pandas as pd

pd.set_option("display.width", 200)
XLSX = sys.argv[1]
NGA = sys.argv[2] if len(sys.argv) > 2 else "Latium"

canon = pd.read_excel(XLSX, "Equinox2020_CanonDat")
polities = pd.read_excel(XLSX, "Polities")
ts = pd.read_excel(XLSX, "TSDat123")
aggr = pd.read_excel(XLSX, "AggrSCWarAgriRelig")
spc = pd.read_excel(XLSX, "SPC_MilTech")

print("=" * 80, "\n1. Release-wide coding vocabulary (all NGAs)\n")
print("Value.Note (how a value is qualified):")
print(canon["Value.Note"].value_counts().to_string(), "\n")
print("Most common Value.From entries (presence/absence codes):")
print(canon["Value.From"].astype(str).value_counts().head(8).to_string(), "\n")

sc_cols = ts.columns[4:40]  # social-complexity block of TSDat123 (PolPop..Article)
miss = (ts[sc_cols] == -999).mean()
print(f"Share of NGA-century cells missing (-999) across the {len(sc_cols)} social-complexity vars: {miss.mean():.0%}")
print("Most-missing vars:", miss.sort_values(ascending=False).head(6).round(2).to_dict(), "\n")

print("=" * 80, f"\n2. Polity sequence in {NGA}\n")
print(polities.loc[polities.NGA == NGA, ["PolName", "PolID", "Start", "End", "Dupl"]].to_string(index=False), "\n")

print("=" * 80, f"\n3. Raw coded facts, {NGA}, Principate -> Ostrogoths -> Papacy\n")
show_pols = ["ItRomPr", "ItRomWe", "ItOstrg", "ItRav**", "ItStPet"]
show_vars = ["Polity Population", "Polity territory", "Population of the largest settlement",
             "Administrative levels", "Full-time bureaucrats", "Professional military officers",
             "Courts", "Examination system"]
sub = canon[(canon.NGA == NGA) & canon.Polity.isin(show_pols) & canon.Variable.isin(show_vars)]
for v in show_vars:
    print("##", v)
    print(sub.loc[sub.Variable == v, ["Polity", "Value.From", "Value.To", "Date.From", "Value.Note"]].to_string(index=False), "\n")

print("=" * 80, f"\n4. Century series for {NGA}: complexity components (CCs) and SPC, every 200 y\n")
m = spc[spc.NGA == NGA].merge(
    aggr[aggr.NGA == NGA][["PolID", "Time", "PropCoded", "Pop", "Terr", "Cap", "Hier", "Gov", "Infra", "Info", "Money"]],
    on=["PolID", "Time"])
print(m.loc[m.Time % 200 == 0, ["PolID", "Time", "SPC", "PropCoded", "Pop", "Terr", "Cap", "Hier", "Gov", "Infra", "Info", "Money"]]
      .round(2).to_string(index=False), "\n")
print(f"Global SPC: mean {spc.SPC.mean():.2f}, sd {spc.SPC.std():.2f}, range {spc.SPC.min():.2f}-{spc.SPC.max():.2f}")
peak = m.loc[m.SPC.idxmax()]
trough = m[(m.Time > peak.Time) & (m.Time <= 800)].SPC.min()
print(f"{NGA} peak SPC {peak.SPC:.2f} at {peak.Time}; min SPC by 800 CE {trough:.2f}; "
      f"drop = {(peak.SPC - trough) / spc.SPC.std():.2f} global sd")
