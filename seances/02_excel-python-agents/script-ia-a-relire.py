"""
Calcul des fonds propres éligibles et du ratio de couverture du SCR et du MCR
pour un ensemble d'assureurs, conformément à l'article 82 de la directive 2009/138/CE.

Script généré par un assistant d'IA à partir de la consigne :
« Écris un script Python qui calcule les fonds propres éligibles et les ratios de
couverture du SCR et du MCR à partir du fichier bilans-assureurs.csv, et qui signale
les ratios déclarés incorrects. »

TD 2, partie C : ce script contient des erreurs. Ne pas le corriger ici : les relever.
"""
import pandas as pd

# Chargement des données
df = pd.read_csv("C:/Users/stagiaire/Documents/TD2/bilans-assureurs.csv", sep=";")

# Nettoyage : suppression des lignes incomplètes
df = df.dropna()


def fonds_propres_eligibles_scr(tier1, tier2, tier3, scr):
    """Applique les limites d'éligibilité aux fonds propres pour la couverture du SCR."""
    tier3_eligible = min(tier3, 0.15 * (tier1 + tier2 + tier3))  # Tier 3 limité à 15 %
    tier2_eligible = min(tier2, 0.50 * scr)  # Tier 2 limité à 50 % du SCR
    return tier1 + tier2_eligible + tier3_eligible


def fonds_propres_eligibles_mcr(tier1, tier2, tier3):
    """Fonds propres éligibles à la couverture du MCR."""
    return tier1 + tier2 + tier3


df["fp_eligibles_scr"] = df.apply(
    lambda x: fonds_propres_eligibles_scr(x["tier1"], x["tier2"], x["tier3"], x["scr"]), axis=1)
df["fp_eligibles_mcr"] = df.apply(
    lambda x: fonds_propres_eligibles_mcr(x["tier1"], x["tier2"], x["tier3"]), axis=1)

df["ratio_scr"] = df["fp_eligibles_scr"] / df["scr"]
df["ratio_mcr"] = df["fp_eligibles_mcr"] / df["mcr"]

# Une entreprise couvre son SCR si son ratio est supérieur à 100 %
df["scr_couvert"] = df["ratio_scr"] > 1
df["mcr_couvert"] = df["ratio_mcr"] > 1

# Contrôle du ratio déclaré
df["ratio_declare_correct"] = df["ratio_scr"] == df["ratio_scr_declare"] / 100

print(df[["entite", "nom", "ratio_scr", "scr_couvert", "ratio_mcr", "mcr_couvert",
          "ratio_declare_correct"]].to_string(index=False))
print(f"\n{len(df)} entités analysées. Toutes les anomalies ont été détectées.")
