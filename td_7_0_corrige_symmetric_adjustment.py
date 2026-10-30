"""
TD 7.0 - Calcul du Symmetric Adjustment : CORRIGÉ COMPLET
Comptabilité Prudentielle en Assurance
Fabrice BOREL-MATHURIN - ACPR & SAF Lyon 1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuration graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================
# PARTIE 1 : IMPORT ET PRÉPARATION DES DONNÉES
# ============================================

def charger_donnees_marche(fichier='data_eurostoxx50_36mois.csv'):
    """
    Charge les données de marché depuis un fichier CSV.
    
    Paramètres:
        fichier (str): Chemin vers le fichier CSV
    
    Retourne:
        DataFrame: Données de marché avec dates converties
    """
    print("=" * 60)
    print("CHARGEMENT DES DONNÉES DE MARCHÉ")
    print("=" * 60)
    
    # Import
    df = pd.read_csv(fichier)
    
    # Conversion date
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Tri par date
    df = df.sort_values('Date').reset_index(drop=True)
    
    print(f"\nFichier chargé : {fichier}")
    print(f"Nombre de mois : {len(df)}")
    print(f"Période : {df['Date'].min().strftime('%Y-%m-%d')} à {df['Date'].max().strftime('%Y-%m-%d')}")
    print(f"\nPremières lignes :")
    print(df.head())
    print(f"\nDernières lignes :")
    print(df.tail())
    
    return df


# ============================================
# PARTIE 2 : CALCUL DU SYMMETRIC ADJUSTMENT
# ============================================

def calculer_moyenne_mobile_36m(df):
    """
    Calcule la moyenne mobile sur 36 mois de l'indice.
    
    Paramètres:
        df (DataFrame): DataFrame avec colonnes 'Date' et 'Indice_EuroStoxx50'
    
    Retourne:
        DataFrame: DataFrame enrichi avec colonne 'Moyenne_36m'
    """
    print("\n" + "=" * 60)
    print("CALCUL DE LA MOYENNE MOBILE 36 MOIS")
    print("=" * 60)
    
    # Calcul de la moyenne mobile
    df['Moyenne_36m'] = df['Indice_EuroStoxx50'].rolling(window=36, min_periods=1).mean()
    
    # Affichage du dernier point
    dernier_indice = df['Indice_EuroStoxx50'].iloc[-1]
    derniere_moyenne = df['Moyenne_36m'].iloc[-1]
    
    print(f"\nValeur actuelle de l'indice  : {dernier_indice:.2f} points")
    print(f"Moyenne sur 36 mois          : {derniere_moyenne:.2f} points")
    print(f"Écart (actuel - moyenne)     : {dernier_indice - derniere_moyenne:+.2f} points")
    print(f"Écart relatif                : {((dernier_indice / derniere_moyenne) - 1) * 100:+.2f}%")
    
    return df


def calculer_symmetric_adjustment(df):
    """
    Calcule le Symmetric Adjustment selon la formule EIOPA.
    
    Formule : SA = 0.5 * (I_current - I_avg) / I_avg
    Plafond : -10% ≤ SA ≤ +10%
    
    Paramètres:
        df (DataFrame): DataFrame avec colonnes 'Indice_EuroStoxx50' et 'Moyenne_36m'
    
    Retourne:
        DataFrame: DataFrame enrichi avec colonne 'SA'
    """
    print("\n" + "=" * 60)
    print("CALCUL DU SYMMETRIC ADJUSTMENT (SA)")
    print("=" * 60)
    
    # Formule EIOPA
    df['SA_brut'] = 0.5 * ((df['Indice_EuroStoxx50'] - df['Moyenne_36m']) / df['Moyenne_36m'])
    
    # Application du plafond [-10%, +10%]
    df['SA'] = df['SA_brut'].clip(lower=-0.10, upper=0.10)
    
    # Flag si plafonnement
    df['SA_plafonne'] = (df['SA_brut'] != df['SA'])
    
    # Affichage du résultat actuel
    sa_actuel_brut = df['SA_brut'].iloc[-1]
    sa_actuel = df['SA'].iloc[-1]
    plafonne = df['SA_plafonne'].iloc[-1]
    
    print(f"\nSymmetric Adjustment (brut)  : {sa_actuel_brut:+.2%}")
    
    if plafonne:
        print(f"⚠️  PLAFONNEMENT APPLIQUÉ")
        print(f"Symmetric Adjustment (final) : {sa_actuel:+.2%}")
    else:
        print(f"Symmetric Adjustment (final) : {sa_actuel:+.2%}")
        print(f"✅ Pas de plafonnement")
    
    return df


def calculer_chocs_ajustes(sa):
    """
    Calcule les chocs actions Type 1 et Type 2 ajustés du SA.
    
    Paramètres:
        sa (float): Symmetric Adjustment (en décimal, ex: 0.055 pour 5.5%)
    
    Retourne:
        dict: {'choc_type1': float, 'choc_type2': float, 'choc_type1_pct': str, 'choc_type2_pct': str}
    """
    print("\n" + "=" * 60)
    print("CALCUL DES CHOCS ACTIONS AJUSTÉS")
    print("=" * 60)
    
    # Chocs de base (Règlement Délégué 2015/35, Article 106)
    choc_base_type1 = 0.39  # 39%
    choc_base_type2 = 0.49  # 49%
    
    # Chocs ajustés
    choc_ajuste_type1 = choc_base_type1 + sa
    choc_ajuste_type2 = choc_base_type2 + sa
    
    print(f"\nChoc de base Type 1          : {choc_base_type1:.1%}")
    print(f"Symmetric Adjustment         : {sa:+.2%}")
    print(f"Choc ajusté Type 1           : {choc_ajuste_type1:.2%}")
    print()
    print(f"Choc de base Type 2          : {choc_base_type2:.1%}")
    print(f"Symmetric Adjustment         : {sa:+.2%}")
    print(f"Choc ajusté Type 2           : {choc_ajuste_type2:.2%}")
    
    return {
        'choc_type1': choc_ajuste_type1,
        'choc_type2': choc_ajuste_type2,
        'choc_type1_pct': f"{choc_ajuste_type1:.2%}",
        'choc_type2_pct': f"{choc_ajuste_type2:.2%}"
    }


# ============================================
# PARTIE 3 : VISUALISATIONS
# ============================================

def visualiser_indice_et_moyenne(df, save_path='sa_indice_et_moyenne.png'):
    """
    Visualise l'indice et sa moyenne mobile 36 mois.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Indice
    ax.plot(df['Date'], df['Indice_EuroStoxx50'], 
            label='EuroStoxx 50', linewidth=2, color='steelblue')
    
    # Moyenne mobile
    ax.plot(df['Date'], df['Moyenne_36m'], 
            label='Moyenne 36 mois', linewidth=2, 
            linestyle='--', color='orange', alpha=0.8)
    
    # Point actuel
    dernier_date = df['Date'].iloc[-1]
    dernier_indice = df['Indice_EuroStoxx50'].iloc[-1]
    ax.scatter(dernier_date, dernier_indice, 
               s=150, color='red', zorder=5, label='Niveau actuel', edgecolor='black')
    
    # Annotations
    ax.annotate(f'{dernier_indice:.0f}', 
                xy=(dernier_date, dernier_indice),
                xytext=(10, 10), textcoords='offset points',
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    # Mise en forme
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Indice (points)', fontsize=12)
    ax.set_title('EuroStoxx 50 vs Moyenne Mobile 36 mois', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nGraphique sauvegardé : {save_path}")
    plt.show()


def visualiser_sa_evolution(df, save_path='sa_evolution.png'):
    """
    Visualise l'évolution du Symmetric Adjustment.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # SA en %
    ax.plot(df['Date'], df['SA'] * 100, 
            linewidth=2.5, color='darkgreen', label='Symmetric Adjustment')
    
    # Zones de plafond
    ax.axhline(0, color='black', linestyle='-', linewidth=1)
    ax.axhline(10, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Plafond +10%')
    ax.axhline(-10, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Plafond -10%')
    
    # Zones colorées
    ax.fill_between(df['Date'], 0, 10, alpha=0.1, color='red')
    ax.fill_between(df['Date'], 0, -10, alpha=0.1, color='red')
    
    # Point actuel
    dernier_date = df['Date'].iloc[-1]
    dernier_sa = df['SA'].iloc[-1]
    ax.scatter(dernier_date, dernier_sa * 100, 
               s=150, color='red', zorder=5, edgecolor='black')
    
    # Annotation
    ax.annotate(f'{dernier_sa:.2%}', 
                xy=(dernier_date, dernier_sa * 100),
                xytext=(10, 10), textcoords='offset points',
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    # Mise en forme
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Symmetric Adjustment (%)', fontsize=12)
    ax.set_title('Évolution du Symmetric Adjustment - EIOPA', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim(-12, 12)
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Graphique sauvegardé : {save_path}")
    plt.show()


def visualiser_complet_sa(df, save_path='sa_analyse_complete.png'):
    """
    Visualisation complète : Indice + Moyenne + SA sur deux subplots.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), 
                                    gridspec_kw={'height_ratios': [2, 1]})
    
    # ========== SUBPLOT 1 : Indice et Moyenne ==========
    ax1.plot(df['Date'], df['Indice_EuroStoxx50'], 
             label='EuroStoxx 50', linewidth=2.5, color='steelblue')
    ax1.plot(df['Date'], df['Moyenne_36m'], 
             label='Moyenne 36 mois', linewidth=2.5, 
             linestyle='--', color='orange', alpha=0.8)
    
    # Point actuel
    dernier_date = df['Date'].iloc[-1]
    dernier_indice = df['Indice_EuroStoxx50'].iloc[-1]
    ax1.scatter(dernier_date, dernier_indice, 
                s=200, color='red', zorder=5, edgecolor='black', linewidth=2)
    
    ax1.set_ylabel('Indice (points)', fontsize=13)
    ax1.set_title('Analyse du Symmetric Adjustment EIOPA - EuroStoxx 50', 
                  fontsize=15, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    
    # ========== SUBPLOT 2 : Symmetric Adjustment ==========
    ax2.plot(df['Date'], df['SA'] * 100, 
             linewidth=2.5, color='darkgreen')
    ax2.axhline(0, color='black', linestyle='-', linewidth=1.2)
    ax2.axhline(10, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(-10, color='red', linestyle='--', linewidth=1, alpha=0.5)
    
    # Zones colorées
    ax2.fill_between(df['Date'], 0, df['SA'] * 100, 
                     where=(df['SA'] >= 0), alpha=0.3, color='green', label='SA positif')
    ax2.fill_between(df['Date'], 0, df['SA'] * 100, 
                     where=(df['SA'] < 0), alpha=0.3, color='red', label='SA négatif')
    
    # Point actuel
    dernier_sa = df['SA'].iloc[-1]
    ax2.scatter(dernier_date, dernier_sa * 100, 
                s=200, color='red', zorder=5, edgecolor='black', linewidth=2)
    
    # Annotation
    ax2.text(dernier_date, dernier_sa * 100 + 1.5, 
             f'SA actuel : {dernier_sa:+.2%}',
             fontsize=12, fontweight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.6', facecolor='yellow', alpha=0.8))
    
    ax2.set_xlabel('Date', fontsize=13)
    ax2.set_ylabel('Symmetric Adjustment (%)', fontsize=13)
    ax2.set_ylim(-12, 12)
    ax2.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Graphique sauvegardé : {save_path}")
    plt.show()


# ============================================
# PARTIE 4 : APPLICATION AU SCR
# ============================================

def calculer_scr_equity(actions_type1, actions_type2, sa, ajustement_pb=0.05):
    """
    Calcule le SCR Equity avec le SA calculé.
    
    Paramètres:
        actions_type1 (float): Montant actions Type 1 en M€
        actions_type2 (float): Montant actions Type 2 en M€
        sa (float): Symmetric Adjustment (décimal)
        ajustement_pb (float): Ajustement pour participation aux bénéfices (5% par défaut)
    
    Retourne:
        dict: Résultats détaillés
    """
    print("\n" + "=" * 60)
    print("CALCUL DU SCR EQUITY")
    print("=" * 60)
    
    # Chocs ajustés
    choc_type1 = 0.39 + sa
    choc_type2 = 0.49 + sa
    
    # Pertes brutes
    perte_type1_brute = actions_type1 * choc_type1
    perte_type2_brute = actions_type2 * choc_type2
    perte_totale_brute = perte_type1_brute + perte_type2_brute
    
    # Ajustement PB (capacité d'absorption)
    perte_type1 = perte_type1_brute * (1 - ajustement_pb)
    perte_type2 = perte_type2_brute * (1 - ajustement_pb)
    scr_equity = perte_type1 + perte_type2
    
    print(f"\nActions Type 1               : {actions_type1:.2f} M€")
    print(f"Choc ajusté Type 1           : {choc_type1:.2%}")
    print(f"Perte brute Type 1           : {perte_type1_brute:.2f} M€")
    print(f"Perte nette Type 1 (après PB): {perte_type1:.2f} M€")
    print()
    print(f"Actions Type 2               : {actions_type2:.2f} M€")
    print(f"Choc ajusté Type 2           : {choc_type2:.2%}")
    print(f"Perte brute Type 2           : {perte_type2_brute:.2f} M€")
    print(f"Perte nette Type 2 (après PB): {perte_type2:.2f} M€")
    print()
    print(f"{'='*60}")
    print(f"SCR EQUITY TOTAL             : {scr_equity:.2f} M€")
    print(f"{'='*60}")
    
    return {
        'actions_type1': actions_type1,
        'actions_type2': actions_type2,
        'choc_type1': choc_type1,
        'choc_type2': choc_type2,
        'scr_type1': perte_type1,
        'scr_type2': perte_type2,
        'scr_equity': scr_equity
    }


def analyse_sensibilite_sa_scr(actions_type1, actions_type2, sa_actuel, save_path='sensibilite_sa_scr.png'):
    """
    Analyse de sensibilité du SCR au SA.
    """
    print("\n" + "=" * 60)
    print("ANALYSE DE SENSIBILITÉ SCR vs SA")
    print("=" * 60)
    
    # Plage de SA : -10% à +10%
    sa_range = np.linspace(-0.10, 0.10, 41)
    scr_range = []
    
    for sa in sa_range:
        choc_type1 = 0.39 + sa
        choc_type2 = 0.49 + sa
        scr = (actions_type1 * choc_type1 + actions_type2 * choc_type2) * 0.95
        scr_range.append(scr)
    
    # Graphique
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(sa_range * 100, scr_range, linewidth=3, color='darkred', label='SCR Equity')
    
    # Point actuel
    scr_actuel = calculer_scr_equity(actions_type1, actions_type2, sa_actuel, 0.05)['scr_equity']
    ax.scatter(sa_actuel * 100, scr_actuel, s=300, color='red', 
               zorder=5, edgecolor='black', linewidth=2, label=f'SA actuel = {sa_actuel:+.2%}')
    
    # Ligne verticale SA actuel
    ax.axvline(sa_actuel * 100, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axhline(scr_actuel, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
    
    # Annotation
    ax.text(sa_actuel * 100, scr_actuel + 3, 
            f'SCR = {scr_actuel:.1f} M€',
            fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))
    
    # Mise en forme
    ax.set_xlabel('Symmetric Adjustment (%)', fontsize=13)
    ax.set_ylabel('SCR Equity (M€)', fontsize=13)
    ax.set_title('Sensibilité du SCR Actions au Symmetric Adjustment', 
                 fontsize=15, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12, loc='upper left', framealpha=0.9)
    
    # Statistiques
    scr_min = min(scr_range)
    scr_max = max(scr_range)
    plage = scr_max - scr_min
    impact_1pt = plage / 20
    
    textstr = f'SCR minimum (SA=-10%) : {scr_min:.1f} M€\n'
    textstr += f'SCR maximum (SA=+10%) : {scr_max:.1f} M€\n'
    textstr += f'Plage de variation : {plage:.1f} M€\n'
    textstr += f'Impact de 1 pt de SA : {impact_1pt:.2f} M€'
    
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nGraphique sauvegardé : {save_path}")
    plt.show()
    
    # Affichage statistiques
    print(f"\nStatistiques de sensibilité :")
    print(f"  SCR minimum (SA = -10%)     : {scr_min:.2f} M€")
    print(f"  SCR maximum (SA = +10%)     : {scr_max:.2f} M€")
    print(f"  Plage de variation          : {plage:.2f} M€")
    print(f"  Impact de 1 pt de SA        : {impact_1pt:.2f} M€")


# ============================================
# PARTIE 5 : RAPPORT DE SYNTHÈSE
# ============================================

def generer_rapport_synthese(df, resultats_scr, sa_actuel):
    """
    Génère un rapport de synthèse textuel.
    """
    print("\n" + "=" * 70)
    print(" " * 20 + "RAPPORT DE SYNTHÈSE")
    print(" " * 15 + "Calcul du Symmetric Adjustment")
    print("=" * 70)
    
    # Informations marché
    print("\n[1] DONNÉES DE MARCHÉ")
    print("-" * 70)
    dernier_indice = df['Indice_EuroStoxx50'].iloc[-1]
    derniere_moyenne = df['Moyenne_36m'].iloc[-1]
    dernier_date = df['Date'].iloc[-1].strftime('%d/%m/%Y')
    
    print(f"Date de valorisation         : {dernier_date}")
    print(f"Indice EuroStoxx 50          : {dernier_indice:.2f} points")
    print(f"Moyenne 36 mois              : {derniere_moyenne:.2f} points")
    print(f"Écart                        : {dernier_indice - derniere_moyenne:+.2f} points ({((dernier_indice/derniere_moyenne)-1)*100:+.2f}%)")
    
    # Symmetric Adjustment
    print("\n[2] SYMMETRIC ADJUSTMENT")
    print("-" * 70)
    print(f"Symmetric Adjustment calculé : {sa_actuel:+.2%}")
    
    if sa_actuel > 0:
        print(f"Interprétation               : Marché AU-DESSUS de sa moyenne")
        print(f"                               → Chocs actions AUGMENTÉS (marché 'cher')")
    else:
        print(f"Interprétation               : Marché EN-DESSOUS de sa moyenne")
        print(f"                               → Chocs actions RÉDUITS (marché 'déprimé')")
    
    # Chocs ajustés
    print("\n[3] CHOCS ACTIONS AJUSTÉS")
    print("-" * 70)
    choc_type1 = 0.39 + sa_actuel
    choc_type2 = 0.49 + sa_actuel
    print(f"Choc actions Type 1          : {choc_type1:.2%} (base 39% {sa_actuel:+.2%})")
    print(f"Choc actions Type 2          : {choc_type2:.2%} (base 49% {sa_actuel:+.2%})")
    
    # SCR
    print("\n[4] IMPACT SUR LE SCR EQUITY")
    print("-" * 70)
    print(f"Actions Type 1               : {resultats_scr['actions_type1']:.2f} M€")
    print(f"Actions Type 2               : {resultats_scr['actions_type2']:.2f} M€")
    print(f"SCR Equity Type 1            : {resultats_scr['scr_type1']:.2f} M€")
    print(f"SCR Equity Type 2            : {resultats_scr['scr_type2']:.2f} M€")
    print(f"SCR EQUITY TOTAL             : {resultats_scr['scr_equity']:.2f} M€")
    
    # Comparaison avec TD 7.1 (SA = -3%)
    print("\n[5] COMPARAISON AVEC TD 7.1")
    print("-" * 70)
    sa_td71 = -0.03
    scr_td71 = calculer_scr_equity(
        resultats_scr['actions_type1'], 
        resultats_scr['actions_type2'], 
        sa_td71, 
        0.05
    )['scr_equity']
    
    ecart_scr = resultats_scr['scr_equity'] - scr_td71
    ecart_scr_pct = (ecart_scr / scr_td71) * 100
    
    print(f"SCR avec SA TD 7.1 (-3%)     : {scr_td71:.2f} M€")
    print(f"SCR avec SA actuel ({sa_actuel:+.2%})   : {resultats_scr['scr_equity']:.2f} M€")
    print(f"Écart                        : {ecart_scr:+.2f} M€ ({ecart_scr_pct:+.2f}%)")
    
    print("\n" + "=" * 70)
    print("FIN DU RAPPORT")
    print("=" * 70)


# ============================================
# FONCTION MAIN
# ============================================

def main():
    """
    Pipeline complet du TD 7.0.
    """
    print("\n" + "=" * 70)
    print(" " * 10 + "TD 7.0 - CALCUL DU SYMMETRIC ADJUSTMENT")
    print(" " * 15 + "Comptabilité Prudentielle en Assurance")
    print("=" * 70)
    
    # 1. Chargement des données
    df = charger_donnees_marche('/home/claude/data_eurostoxx50_36mois.csv')
    
    # 2. Calcul moyenne mobile
    df = calculer_moyenne_mobile_36m(df)
    
    # 3. Calcul SA
    df = calculer_symmetric_adjustment(df)
    sa_actuel = df['SA'].iloc[-1]
    
    # 4. Chocs ajustés
    chocs = calculer_chocs_ajustes(sa_actuel)
    
    # 5. Visualisations
    print("\n[Génération des graphiques...]")
    visualiser_complet_sa(df, save_path='/home/claude/sa_analyse_complete.png')
    
    # 6. Application au SCR (données TD 7.1)
    resultats_scr = calculer_scr_equity(
        actions_type1=150,  # M€
        actions_type2=30,   # M€
        sa=sa_actuel,
        ajustement_pb=0.05
    )
    
    # 7. Analyse de sensibilité
    analyse_sensibilite_sa_scr(
        actions_type1=150,
        actions_type2=30,
        sa_actuel=sa_actuel,
        save_path='/home/claude/sensibilite_sa_scr.png'
    )
    
    # 8. Rapport de synthèse
    generer_rapport_synthese(df, resultats_scr, sa_actuel)
    
    # 9. Export des données
    print("\n[Export des données...]")
    df.to_csv('/home/claude/sa_resultats_complets.csv', index=False)
    print("Fichier sauvegardé : sa_resultats_complets.csv")
    
    print("\n" + "=" * 70)
    print("ANALYSE TERMINÉE !")
    print("=" * 70)
    print("\n📁 Fichiers générés :")
    print("  - sa_analyse_complete.png")
    print("  - sensibilite_sa_scr.png")
    print("  - sa_resultats_complets.csv")
    print("\n💡 Le Symmetric Adjustment vous permet de connecter")
    print("   la réglementation aux réalités des marchés financiers.")
    
    return {
        'df': df,
        'sa_actuel': sa_actuel,
        'chocs': chocs,
        'resultats_scr': resultats_scr
    }


# ============================================
# EXÉCUTION
# ============================================

if __name__ == "__main__":
    resultats = main()
    
    print("\n" + "🎯" * 35)
    print(f"SYMMETRIC ADJUSTMENT : {resultats['sa_actuel']:+.2%}")
    print(f"SCR EQUITY           : {resultats['resultats_scr']['scr_equity']:.2f} M€")
    print("🎯" * 35)
