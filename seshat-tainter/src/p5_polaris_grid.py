"""Build an NGA x century grid from Polaris2026 (long format) using the same variable short names as
Equinox TSDat123, then rebuild the 8 CCs (missing-as-missing rules 'M') and report PC1 (measure-level only).

Crosswalk is hand-written: the release's own Variables.equinox_variable_name column is misaligned
(e.g. military_level -> 'elite status is hereditary'); see ANALYSIS_LOG 006.
Codes: P=1, IP=0.9, A=0, IA=0.1, SU/U/other text = NA (missing-as-missing). Numeric: midpoint of from/to.
Polity -> NGA via Polities.homeNGA; polity active at century t if start_year <= t <= end_year;
dated values (year_from/to) override undated ones for the centuries they cover.
Usage: python -I src/p5_polaris_grid.py <Polaris2026.xlsx> data/interim/polaris_grid.csv
"""
import sys
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer

XW = {  # Polaris variable_name -> Equinox ShortName
    "polity_population": "PolPop", "polity_territory": "PolTerr", "population_of_the_largest_settlement": "CapPop",
    "administrative_level": "AdmLev", "military_level": "MilLev", "religious_level": "ReligLev",
    "settlement_hierarchy": "SettlHier", "professional_military_officer": "ProfOfficer",
    "professional_soldier": "ProfSoldier", "professional_priesthood": "ProfPriest",
    "full_time_bureaucrat": "FullTBur", "examination_system": "ExamSyst", "merit_promotion": "MeritProm",
    "specialized_government_building": "GovtBldg", "court": "Court", "formal_legal_code": "LegCode",
    "judge": "Judge", "professional_lawyer": "Lawyer", "irrigation_system": "Irrigation",
    "drinking_water_supply_system": "WaterSuppl", "market": "Market", "food_storage_site": "FoodStor",
    "road": "Road", "bridge": "Bridge", "canal": "Canal", "port": "Port", "mines_or_quarry": "Mine",
    "courier": "Courier", "postal_station": "PostStation", "general_postal_service": "PostService",
    "mnemonic_device": "Mnemonic", "nonwritten_record": "NonWRecord", "written_record": "WRecord",
    "script": "Script", "non_phonetic_writing": "NonPhWrit", "phonetic_alphabetic_writing": "PhAlph",
    "lists_tables_and_classification": "Lists", "calendar": "Calendar", "sacred_text": "SacrTxt",
    "religious_literature": "ReligLit", "practical_literature": "PractLit", "history": "History",
    "philosophy": "Philosophy", "scientific_literature": "SciLit", "fiction": "Fiction",
    "article": "Article", "token": "Token", "precious_metal": "PrecMetal", "foreign_coin": "ForCoin",
    "indigenous_coin": "IndigCoin", "paper_currency": "PaperCurr",
}
CODE = {"P": 1.0, "IP": 0.9, "A": 0.0, "IA": 0.1}
GOV = ["ProfOfficer", "ProfSoldier", "ProfPriest", "FullTBur", "ExamSyst", "MeritProm", "GovtBldg", "Court",
       "LegCode", "Judge", "Lawyer"]
INFRA = ["Irrigation", "WaterSuppl", "Market", "FoodStor", "Road", "Bridge", "Canal", "Port", "Mine",
         "Courier", "PostStation", "PostService"]
INFO = ["Mnemonic", "NonWRecord", "WRecord", "Script", "Lists", "Calendar", "SacrTxt", "ReligLit", "PractLit",
        "History", "Philosophy", "SciLit", "Fiction"]
MONEY = ["Article", "Token", "PrecMetal", "ForCoin", "IndigCoin", "PaperCurr"]
CC = ["Pop", "Terr", "Cap", "Hier", "Gov", "Infra", "Info", "Money"]


def num(v_from, v_to):
    s = str(v_from).strip()
    if s in CODE:
        return CODE[s]
    try:
        a = float(s)
    except ValueError:
        return np.nan
    try:
        return (a + float(v_to)) / 2 if pd.notna(v_to) else a
    except ValueError:
        return a


def build_grid(xlsx):
    pol = pd.read_excel(xlsx, "Polities").dropna(subset=["homeNGA"])
    sc = pd.read_excel(xlsx, "Social complexity")
    sc = sc[sc.variable_name.isin(XW)].assign(var=lambda d: d.variable_name.map(XW))
    sc["x"] = [num(a, b) for a, b in zip(sc.value_from, sc.value_to)]
    # one value per polity x var: mean over undated entries (lists/ranges collapse to their mean)
    und = sc[sc.year_from.isna()].groupby(["polity_id", "var"]).x.mean().unstack()
    dated = sc[sc.year_from.notna()]
    rows = []
    for _, p in pol.iterrows():
        for t in range(int(np.ceil(p.start_year / 100) * 100), int(p.end_year) + 1, 100):
            r = {"NGA": p.homeNGA, "PolID": p.polity_id, "Time": t}
            if p.polity_id in und.index:
                r.update(und.loc[p.polity_id].to_dict())
            dd = dated[(dated.polity_id == p.polity_id) & (dated.year_from <= t) &
                       (dated.year_to.fillna(dated.year_from) >= t)]
            r.update(dd.groupby("var").x.mean().to_dict())
            rows.append(r)
    g = pd.DataFrame(rows)
    # one polity per NGA-century: keep the polity with the most coded variables
    g["ncoded"] = g.drop(columns=["NGA", "PolID", "Time"]).notna().sum(axis=1)
    g = g.sort_values("ncoded", ascending=False).drop_duplicates(["NGA", "Time"]).sort_values(["NGA", "Time"])
    return g.drop(columns="ncoded").reset_index(drop=True)


def ccs(g):
    d = g[["NGA", "PolID", "Time"]].copy()
    for c, v in (("Pop", "PolPop"), ("Terr", "PolTerr"), ("Cap", "CapPop")):
        d[c] = np.log10(g[v].where(g[v] > 0))
    d["Hier"] = g[["AdmLev", "MilLev", "SettlHier"]].mean(axis=1)
    d["Gov"], d["Infra"], d["Info"] = g[GOV].mean(axis=1), g[INFRA].mean(axis=1), g[INFO].mean(axis=1)
    d["Money"] = pd.concat([g[c] * i for i, c in enumerate(MONEY, 1)], axis=1).max(axis=1) / 6
    return d


if __name__ == "__main__":
    g = build_grid(sys.argv[1])
    g.to_csv(sys.argv[2], index=False)
    d = ccs(g)
    print(f"grid: {len(g)} NGA-centuries, {g.NGA.nunique()} NGAs, {g.PolID.nunique()} polities")
    print("CC coded share:", d[CC].notna().mean().round(2).to_dict())
    cc_ = d.dropna(subset=CC)
    Z = (cc_[CC] - cc_[CC].mean()) / cc_[CC].std()
    p = PCA().fit(Z)
    print(f"complete-case n={len(cc_)} PC1 var={p.explained_variance_ratio_[0]:.3f} "
          f"loadings={np.round(np.abs(p.components_[0]), 2).tolist()}")
    vs = []
    for k in range(20):
        X = pd.DataFrame(IterativeImputer(sample_posterior=True, random_state=k, max_iter=25).fit_transform(d[CC]), columns=CC)
        vs.append(PCA().fit((X - X.mean()) / X.std()).explained_variance_ratio_[0])
    print(f"MI(20) n={len(d)} PC1 var={np.mean(vs):.3f} ± {np.std(vs):.3f}")
