"""
TD 2 - Contrôler les états de six assureurs : CORRIGÉ (partie B, Python)
Comptabilité prudentielle en assurance - séance 2

Montants en M€. Données fictives : ../bilans-assureurs.csv (séparateur « ; »).
Fonds propres de base = excédent d'actif sur passif + dettes subordonnées (pas d'autre élément).
Limites d'éligibilité : règlement délégué (UE) 2015/35, art. 82. Plancher absolu du MCR supposé non contraignant.
"""
from pathlib import Path

import numpy as np
import pandas as pd

TOLERANCE = 0.005  # écart toléré entre ratio recalculé et ratio déclaré : 0,5 point


def chemin(nom):
    """Le fichier de données, que le script soit lancé depuis la séance ou depuis corriges/."""
    p = Path(nom)
    return p if p.exists() else Path(__file__).resolve().parent.parent / nom


def charger():
    return pd.read_csv(chemin("bilans-assureurs.csv"), sep=";").set_index("entite")


def eligibles(d):
    """Fonds propres éligibles à la couverture du SCR et du MCR, colonne par colonne (vectorisé)."""
    t3_scr = np.minimum(d["tier3"], 0.15 * d["scr"])                  # niveau 3 < 15 % du SCR
    t2_scr = np.minimum(d["tier2"], 0.50 * d["scr"] - t3_scr)         # niveaux 2 + 3 <= 50 % du SCR
    t2_mcr = np.minimum(d["tier2"], 0.20 * d["mcr"])                  # niveau 2 <= 20 % du MCR, pas de niveau 3
    return pd.DataFrame({
        "fp_scr": d["tier1"] + t2_scr + t3_scr,
        "fp_mcr": d["tier1"] + t2_mcr,
        "t1_min_scr": d["tier1"] >= 0.5 * d["scr"],                   # niveau 1 >= 50 % du SCR
        "t1_min_mcr": d["tier1"] >= 0.8 * d["mcr"],                   # niveau 1 >= 80 % du MCR
    })


def controles(d):
    """Une ligne par entité, une colonne par contrôle : True = anomalie."""
    e = eligibles(d)
    excedent = d["actif"] - d["provisions_techniques"] - d["dettes_subordonnees"] - d["autres_passifs"]
    ratio = e["fp_scr"] / d["scr"]
    c = pd.DataFrame(index=d.index)
    c["C0 donnée manquante"] = d.isna().any(axis=1)
    c["C1 excédent déclaré faux"] = ~np.isclose(excedent, d["excedent_declare"])
    c["C2 niveaux ≠ fonds propres de base"] = ~np.isclose(
        d[["tier1", "tier2", "tier3"]].sum(axis=1), excedent + d["dettes_subordonnees"])
    c["C3 ratio déclaré faux"] = (ratio - d["ratio_scr_declare"] / 100).abs() > TOLERANCE
    c["C4 MCR hors corridor 25-45 %"] = ~d["mcr"].div(d["scr"]).between(0.25, 0.45)
    c["C5 SCR non couvert"] = (ratio < 1) | ~e["t1_min_scr"]
    c["C6 MCR non couvert"] = (e["fp_mcr"] < d["mcr"]) | ~e["t1_min_mcr"]
    # Sans SCR, C3 à C5 ne peuvent pas être évalués : on ne conclut pas, C0 suffit à alerter.
    c.loc[d["scr"].isna(), ["C3 ratio déclaré faux", "C4 MCR hors corridor 25-45 %", "C5 SCR non couvert"]] = False
    return c, ratio


def bscr(fichier_matrice="matrice-correlation.csv", scr_modules=(60, 5, 30, 0, 0), incorporels=0.0):
    """BSCR = racine(s' C s) + SCR incorporels (directive, annexe IV ; règlement délégué, art. 87)."""
    c = pd.read_csv(chemin(fichier_matrice), sep=";", index_col="module").to_numpy()
    s = np.array(scr_modules, dtype=float)
    return float(np.sqrt(s @ c @ s)) + incorporels


def main():
    d = charger()
    c, ratio = controles(d)
    e = eligibles(d)
    synthese = pd.DataFrame({"nom": d["nom"], "FP éligibles SCR": e["fp_scr"],
                             "ratio recalculé (%)": (100 * ratio).round(1),
                             "ratio déclaré (%)": d["ratio_scr_declare"],
                             "FP éligibles MCR": e["fp_mcr"]})
    pd.set_option("display.width", 140)
    print("Ratios recalculés\n", synthese.to_string(), "\n", sep="")
    anomalies = c.apply(lambda ligne: ", ".join(ligne.index[ligne]) or "aucune", axis=1)
    print("Anomalies\n", anomalies.to_string(), "\n", sep="")
    valeur = bscr()
    print(f"BSCR de l'Assureur Gamma (marché 60, contrepartie 5, vie 30) : {valeur:.2f} M€")

    # Résultats repris dans le corrigé (td.tex)
    attendu = {"A": [], "B": ["C1"], "C": ["C3", "C5"], "D": ["C4"], "E": ["C5"], "F": ["C0"]}
    for entite, codes in attendu.items():
        assert [k.split()[0] for k in c.columns[c.loc[entite]]] == codes, (entite, c.loc[entite])
    assert np.isclose(ratio["C"], 59 / 60) and np.isclose(ratio["A"], 125 / 80) and ratio["B"] == 1
    assert round(valeur, 2) == 75.17


if __name__ == "__main__":
    main()
