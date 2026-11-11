"""
TD 1 - Mini-bilan prudentiel de l'Assureur Bêta : CORRIGÉ
Comptabilité prudentielle en assurance - séance 1

Montants en k€. Données : ../assureur-beta.csv (séparateur « ; », ouvrable dans Excel).
Hypothèses de l'énoncé : base fiscale = valeurs des comptes sociaux ; taux d'impôt 25 % ;
impôts différés actifs recouvrables ; SCR = 70 000 et MCR = 17 500 donnés ; CoC = 6 %.
"""
from pathlib import Path

import pandas as pd

FICHIER = "assureur-beta.csv"
TAUX_IS = 0.25
COC = 0.06
SCR, MCR = 70_000, 17_500


def charger(fichier=FICHIER):
    chemin = Path(fichier)
    if not chemin.exists():  # script lancé depuis corriges/
        chemin = Path(__file__).resolve().parent.parent / fichier
    return pd.read_csv(chemin, sep=";").set_index("poste")


def marge_de_risque():
    """Marge de risque simplifiée : CoC x (nombre d'années) x SCR moyen x facteur d'actualisation moyen."""
    tranches = pd.DataFrame({"annees": [5, 5, 10], "scr_moyen": [70_000, 50_000, 30_000],
                             "actualisation": [0.92, 0.75, 0.55]}, index=["1-5", "6-10", "11-20"])
    tranches["mr"] = COC * tranches["annees"] * tranches["scr_moyen"] * tranches["actualisation"]
    return tranches


def bilan_prudentiel(d, mr):
    actif = d[d["cote"] == "actif"]
    ecart_actifs = (actif["valeur_prudentielle"] - actif["valeur_comptable"]).sum()
    pt_s2 = d.loc["meilleure_estimation", "valeur_prudentielle"] + mr
    ecart_pt = pt_s2 - d.loc["provisions_techniques", "valeur_comptable"]
    # Différences temporaires : actifs plus bas et passifs plus hauts qu'en base fiscale -> impôt différé actif
    ida = -(ecart_actifs - ecart_pt) * TAUX_IS
    actif_s2 = actif["valeur_prudentielle"].sum() + ida
    passif_s2 = pt_s2 + d.loc[["dettes_subordonnees", "autres_dettes"], "valeur_prudentielle"].sum()
    return {"écart actifs": ecart_actifs, "PT S2": pt_s2, "écart PT": ecart_pt, "IDA nets": ida,
            "actif S2": actif_s2, "passif S2": passif_s2, "excédent": actif_s2 - passif_s2}


def niveaux(d, b):
    capital = d.loc["capital_social", "valeur_comptable"]
    t3 = b["IDA nets"]
    reserve_reconciliation = b["excédent"] - capital - t3
    t1 = capital + reserve_reconciliation
    t2 = d.loc["dettes_subordonnees", "valeur_prudentielle"]
    return {"capital social": capital, "réserve de réconciliation": reserve_reconciliation,
            "Tier 1": t1, "Tier 2": t2, "Tier 3": t3}


def eligibles(n, scr=SCR, mcr=MCR):
    """Limites du RD art. 82. SCR : T1 >= 50 %, T3 < 15 %, T2 + T3 <= 50 %. MCR : T1 >= 80 %, T2 <= 20 %, pas de T3."""
    t3 = min(n["Tier 3"], 0.15 * scr)
    t2 = min(n["Tier 2"], 0.50 * scr - t3)
    of_scr = n["Tier 1"] + t2 + t3
    of_mcr = n["Tier 1"] + min(n["Tier 2"], 0.20 * mcr)
    return {"T2 éligible SCR": t2, "T3 éligible SCR": t3, "FP éligibles SCR": of_scr,
            "ratio SCR": of_scr / scr, "T1 >= 50 % SCR": n["Tier 1"] >= 0.5 * scr,
            "FP éligibles MCR": of_mcr, "ratio MCR": of_mcr / mcr, "T1 >= 80 % MCR": n["Tier 1"] >= 0.8 * mcr}


def chocs(b):
    """Impact, après impôts différés, de chaque scénario sur l'excédent d'actif sur passif (SCR inchangé)."""
    scenarios = {"A. actions -20 %": -0.20 * 90_000,
                 "B. taux +100 pb (obligations -5 %, BE -45 750)": -0.05 * (480_000 + 195_000) + 45_750,
                 "C. spread +100 pb (obligations d'entreprises -4 %)": -0.04 * 195_000}
    lignes = []
    for nom, avant_impot in scenarios.items():
        excedent = b["excédent"] + avant_impot * (1 - TAUX_IS)
        ida = b["IDA nets"] - avant_impot * TAUX_IS
        lignes.append({"scénario": nom, "impact avant impôt": avant_impot,
                       "impact après impôt": avant_impot * (1 - TAUX_IS),
                       "excédent": excedent, "IDA nets": ida, "Tier 1": excedent - ida})
    return pd.DataFrame(lignes).set_index("scénario")


def main():
    pd.set_option("display.width", 120)
    d = charger()
    print("1. Revalorisation des actifs")
    actif = d[d["cote"] == "actif"][["libelle", "valeur_comptable", "valeur_prudentielle"]].copy()
    actif["écart"] = actif["valeur_prudentielle"] - actif["valeur_comptable"]
    print(actif.to_string(), "\n")

    tranches = marge_de_risque()
    mr_exacte = tranches["mr"].sum()
    mr = round(mr_exacte, -3)  # arrondie à 40 000 k€ dans l'énoncé
    print("2. Marge de risque (CoC 6 %)")
    print(tranches.to_string(), f"\n   total {mr_exacte:,.0f} -> retenue {mr:,.0f}\n")

    b = bilan_prudentiel(d, mr)
    print("3-4. Impôts différés et bilan prudentiel")
    for k, v in b.items():
        print(f"   {k:<14} {v:>12,.0f}")
    capitaux_propres = d.loc[["capital_social", "reserves_resultat"], "valeur_comptable"].sum()
    print(f"   contrôle : {capitaux_propres:,.0f} + {b['écart actifs']:,.0f} - {b['écart PT']:,.0f}"
          f" + {b['IDA nets']:,.0f} = {capitaux_propres + b['écart actifs'] - b['écart PT'] + b['IDA nets']:,.0f}\n")

    n = niveaux(d, b)
    print("5. Fonds propres par niveau")
    for k, v in n.items():
        print(f"   {k:<27} {v:>10,.0f}")
    e = eligibles(n)
    print("\n6. Éligibilité et ratios (SCR 70 000, MCR 17 500)")
    for k, v in e.items():
        print(f"   {k:<17} {v:>10.0%}" if k.startswith("ratio") else f"   {k:<17} {v!s:>10}")
    besoin_t1 = 0.5 * SCR - n["Tier 1"]
    print(f"   recapitalisation en Tier 1 pour couvrir le SCR : {besoin_t1:,.0f}\n")

    print("7. Scénarios de choc (SCR inchangé)")
    print(chocs(b).to_string(float_format=lambda x: f"{x:,.0f}"))

    # Valeurs reprises dans le corrigé du TD (td.tex)
    assert round(b["IDA nets"]) == 9_000 and round(b["excédent"]) == 23_000
    assert (n["Tier 1"], n["Tier 2"], n["Tier 3"]) == (14_000, 50_000, 9_000)
    assert round(e["FP éligibles SCR"]) == 49_000 and round(e["FP éligibles MCR"]) == 17_500
    assert besoin_t1 == 21_000


if __name__ == "__main__":
    main()
