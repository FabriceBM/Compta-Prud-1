"""
TD 3.5 - Refactorisation Chain-Ladder : CORRIGÉ COMPLET
Comptabilité Prudentielle en Assurance
Fabrice BOREL-MATHURIN - ACPR & SAF Lyon 1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# PARTIE 1 : DONNÉES
# ============================================

# Triangle initial (Sinistres cumulés en k€)
triangle_initial = np.array([
    [1000, 1800, 2300, 2600, 2750, 2800],
    [1100, 1950, 2500, 2800, 2950, np.nan],
    [950,  1700, 2200, 2500, np.nan, np.nan],
    [1050, 1900, 2450, np.nan, np.nan, np.nan],
    [1150, 2100, np.nan, np.nan, np.nan, np.nan],
    [1000, np.nan, np.nan, np.nan, np.nan, np.nan]
], dtype=float)

print("=" * 60)
print("TD 3.5 - CORRIGÉ : Refactorisation Chain-Ladder")
print("=" * 60)
print("\nTriangle initial (Sinistres cumulés en k€) :")
print(triangle_initial)

# ============================================
# PARTIE 2 : FONCTIONS PRINCIPALES
# ============================================

def calculer_facteurs_developpement(triangle):
    """
    Calcule les facteurs de développement (Link Ratios) d'un triangle.
    
    Paramètres:
        triangle (np.array): Triangle de liquidation (sinistres cumulés)
    
    Retourne:
        list: Facteurs de développement [f(0→1), f(1→2), ..., f(n-1→n)]
    """
    n_rows, n_cols = triangle.shape
    facteurs = []
    
    for col in range(n_cols - 1):
        # Pour chaque colonne, calculer le ratio col+1 / col
        ratios = []
        
        # On calcule les ratios sur les années où les deux valeurs existent
        for row in range(n_rows - col - 1):
            val_actuelle = triangle[row, col]
            val_suivante = triangle[row, col + 1]
            
            # Vérifier que les deux valeurs ne sont pas NaN
            if not np.isnan(val_actuelle) and not np.isnan(val_suivante):
                ratio = val_suivante / val_actuelle
                ratios.append(ratio)
        
        # Calculer la moyenne des ratios
        if len(ratios) > 0:
            facteur_moyen = np.mean(ratios)
            facteurs.append(facteur_moyen)
        else:
            # Si aucun ratio disponible, utiliser 1.0 par défaut
            facteurs.append(1.0)
    
    return facteurs


def completer_triangle(triangle, facteurs):
    """
    Complète le triangle de liquidation avec les facteurs de développement.
    
    Paramètres:
        triangle (np.array): Triangle initial (avec np.nan)
        facteurs (list): Facteurs de développement
    
    Retourne:
        np.array: Triangle complété
    """
    triangle_complete = triangle.copy()
    n_rows, n_cols = triangle.shape
    
    # Pour chaque ligne (année de survenance)
    for row in range(n_rows):
        # Pour chaque colonne de développement
        for col in range(n_cols):
            if np.isnan(triangle_complete[row, col]):
                # Trouver la dernière valeur connue
                # On part de col-1 et on remonte
                derniere_val = triangle_complete[row, col - 1]
                facteur_index = col - 1
                
                # Appliquer le facteur de développement
                triangle_complete[row, col] = derniere_val * facteurs[facteur_index]
    
    return triangle_complete


def calculer_best_estimate_non_vie(triangle_complete, triangle_initial, 
                                     taux_actualisation=0.02):
    """
    Calcule le Best Estimate Non-Vie à partir du triangle complété.
    
    Paramètres:
        triangle_complete (np.array): Triangle complété
        triangle_initial (np.array): Triangle initial
        taux_actualisation (float): Taux d'actualisation annuel
    
    Retourne:
        dict: {
            'be_total': float (Best Estimate total),
            'detail_par_annee': list (détail par année de survenance)
        }
    """
    n_rows, n_cols = triangle_complete.shape
    be_total = 0
    detail_par_annee = []
    
    for row in range(n_rows):
        # Sinistre ultime de cette année
        ultime = triangle_complete[row, -1]
        
        # Trouver la dernière valeur non-NaN du triangle initial pour cette ligne
        derniere_col_payee = -1
        for col in range(n_cols):
            if not np.isnan(triangle_initial[row, col]):
                derniere_col_payee = col
        
        # Sinistre déjà payé
        deja_paye = triangle_initial[row, derniere_col_payee]
        
        # Sinistre restant à payer
        reste_a_payer = ultime - deja_paye
        
        # Actualisation simplifiée : on suppose paiement étalé uniformément
        # sur les années restantes de développement
        annees_restantes = n_cols - derniere_col_payee - 1
        
        if annees_restantes > 0:
            # Durée moyenne de paiement : milieu de la période
            duree_moyenne = annees_restantes / 2
        else:
            duree_moyenne = 0.5  # Si déjà à maturité, on suppose 6 mois
        
        # Facteur d'actualisation
        facteur_actualisation = 1 / (1 + taux_actualisation) ** duree_moyenne
        
        # BE pour cette année
        be_annee = reste_a_payer * facteur_actualisation
        be_total += be_annee
        
        detail_par_annee.append({
            'annee_survenance': 2018 + row,
            'ultime': ultime,
            'deja_paye': deja_paye,
            'reste_a_payer': reste_a_payer,
            'duree_moyenne': duree_moyenne,
            'be': be_annee
        })
    
    return {
        'be_total': be_total,
        'detail_par_annee': detail_par_annee
    }


def calculer_chain_ladder(triangle_initial, taux_actualisation=0.02):
    """
    Pipeline complet Chain-Ladder : Triangle → Facteurs → Complétion → BE.
    
    Paramètres:
        triangle_initial (np.array): Triangle de liquidation initial
        taux_actualisation (float): Taux d'actualisation
    
    Retourne:
        dict: {
            'facteurs': list,
            'triangle_complete': np.array,
            'resultats_be': dict
        }
    """
    print("\n" + "=" * 60)
    print("CALCUL CHAIN-LADDER - PIPELINE COMPLET")
    print("=" * 60)
    
    # Étape 1 : Calculer les facteurs de développement
    print("\n[Étape 1] Calcul des facteurs de développement...")
    facteurs = calculer_facteurs_developpement(triangle_initial)
    print(f"Facteurs de développement calculés :")
    for i, f in enumerate(facteurs):
        print(f"  f({i}→{i+1}) = {f:.4f}")
    
    # Étape 2 : Compléter le triangle
    print("\n[Étape 2] Complétion du triangle...")
    triangle_complete = completer_triangle(triangle_initial, facteurs)
    print(f"Triangle complété :")
    print(triangle_complete)
    
    # Étape 3 : Calculer le BE
    print("\n[Étape 3] Calcul du Best Estimate...")
    resultats_be = calculer_best_estimate_non_vie(
        triangle_complete, triangle_initial, taux_actualisation
    )
    
    print(f"\nDétail par année de survenance :")
    for detail in resultats_be['detail_par_annee']:
        print(f"  Année {detail['annee_survenance']}: "
              f"Ultime={detail['ultime']:.0f} k€, "
              f"Reste à payer={detail['reste_a_payer']:.0f} k€, "
              f"BE={detail['be']:.2f} k€")
    
    print(f"\n{'='*60}")
    print(f"BEST ESTIMATE TOTAL : {resultats_be['be_total']:.2f} k€")
    print(f"{'='*60}")
    
    return {
        'facteurs': facteurs,
        'triangle_complete': triangle_complete,
        'resultats_be': resultats_be
    }


# ============================================
# PARTIE 3 : VISUALISATIONS
# ============================================

def visualiser_triangle(triangle, titre="Triangle de liquidation", ax=None):
    """
    Visualise le triangle avec une heatmap.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    # Créer un masque pour les valeurs manquantes
    mask = np.isnan(triangle)
    
    # Heatmap
    sns.heatmap(triangle, annot=True, fmt='.0f', cmap='YlOrRd', 
                mask=mask, cbar_kws={'label': 'Sinistres cumulés (k€)'},
                ax=ax, linewidths=0.5, linecolor='gray')
    
    ax.set_title(titre, fontsize=14, fontweight='bold')
    ax.set_xlabel('Année de développement', fontsize=11)
    ax.set_ylabel('Année de survenance', fontsize=11)
    
    # Labels des années
    annees = [str(2018 + i) for i in range(triangle.shape[0])]
    ax.set_yticklabels(annees, rotation=0)
    
    return ax


def visualiser_comparaison_triangles(triangle_initial, triangle_complete):
    """
    Visualise côte à côte le triangle initial et le triangle complété.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    visualiser_triangle(triangle_initial, "Triangle Initial", ax=axes[0])
    visualiser_triangle(triangle_complete, "Triangle Complété", ax=axes[1])
    
    plt.tight_layout()
    plt.savefig('/home/claude/triangles_comparaison.png', dpi=150, bbox_inches='tight')
    print("\nGraphique sauvegardé : triangles_comparaison.png")
    plt.show()


def visualiser_be_par_annee(resultats_be):
    """
    Visualise le BE par année de survenance.
    """
    detail = resultats_be['detail_par_annee']
    annees = [d['annee_survenance'] for d in detail]
    be_par_annee = [d['be'] for d in detail]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(annees, be_par_annee, color='steelblue', alpha=0.8, edgecolor='black')
    
    # Ajouter les valeurs au-dessus des barres
    for bar, be in zip(bars, be_par_annee):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{be:.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Année de survenance', fontsize=12)
    ax.set_ylabel('Best Estimate (k€)', fontsize=12)
    ax.set_title('Best Estimate par année de survenance', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/be_par_annee.png', dpi=150, bbox_inches='tight')
    print("Graphique sauvegardé : be_par_annee.png")
    plt.show()


# ============================================
# PARTIE 4 : ANALYSE DE SENSIBILITÉ
# ============================================

def analyse_sensibilite_taux(triangle_initial, taux_min=0.0, taux_max=0.05, n_points=11):
    """
    Analyse l'impact du taux d'actualisation sur le BE.
    """
    print("\n" + "=" * 60)
    print("ANALYSE DE SENSIBILITÉ - Taux d'actualisation")
    print("=" * 60)
    
    taux_liste = np.linspace(taux_min, taux_max, n_points)
    be_liste = []
    
    for taux in taux_liste:
        facteurs = calculer_facteurs_developpement(triangle_initial)
        triangle_complete = completer_triangle(triangle_initial, facteurs)
        resultats = calculer_best_estimate_non_vie(triangle_complete, triangle_initial, taux)
        be_liste.append(resultats['be_total'])
    
    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(taux_liste * 100, be_liste, marker='o', linewidth=2, 
            markersize=6, color='darkred', label='Best Estimate')
    
    ax.set_xlabel('Taux d\'actualisation (%)', fontsize=12)
    ax.set_ylabel('Best Estimate (k€)', fontsize=12)
    ax.set_title('Sensibilité du BE au taux d\'actualisation', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    
    # Ajouter le taux de base (2%)
    be_base = be_liste[np.argmin(np.abs(taux_liste - 0.02))]
    ax.axvline(2.0, color='green', linestyle='--', alpha=0.5, label='Taux de base (2%)')
    ax.axhline(be_base, color='green', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('/home/claude/sensibilite_taux.png', dpi=150, bbox_inches='tight')
    print("Graphique sauvegardé : sensibilite_taux.png")
    plt.show()
    
    # Tableau de résultats
    df_sensibilite = pd.DataFrame({
        'Taux (%)': taux_liste * 100,
        'BE (k€)': be_liste,
        'Variation vs base (%)': (np.array(be_liste) / be_base - 1) * 100
    })
    
    print("\nTableau de sensibilité :")
    print(df_sensibilite.to_string(index=False))
    
    return df_sensibilite


# ============================================
# PARTIE 5 : COMPARAISON AVEC EXCEL
# ============================================

def comparer_avec_excel(resultats_python, be_excel=None):
    """
    Compare les résultats Python avec les résultats Excel.
    
    Paramètres:
        resultats_python (dict): Résultats du calcul Python
        be_excel (float): BE calculé dans Excel (si disponible)
    """
    print("\n" + "=" * 60)
    print("COMPARAISON PYTHON vs EXCEL")
    print("=" * 60)
    
    be_python = resultats_python['resultats_be']['be_total']
    
    print(f"\nBest Estimate Python : {be_python:.2f} k€")
    
    if be_excel is not None:
        print(f"Best Estimate Excel  : {be_excel:.2f} k€")
        ecart = be_python - be_excel
        ecart_pct = (ecart / be_excel) * 100
        print(f"Écart                : {ecart:.2f} k€ ({ecart_pct:+.2f}%)")
        
        if abs(ecart_pct) < 0.1:
            print("\n✅ Résultats identiques ! Votre refactorisation est correcte.")
        elif abs(ecart_pct) < 1.0:
            print("\n⚠️  Petite différence (< 1%) : probablement due aux arrondis.")
        else:
            print("\n❌ Écart significatif : vérifiez votre implémentation.")
    else:
        print("\n(Résultat Excel non fourni pour comparaison)")
    
    # Comparaison des facteurs
    print("\nFacteurs de développement :")
    facteurs = resultats_python['facteurs']
    for i, f in enumerate(facteurs):
        print(f"  f({i}→{i+1}) = {f:.4f}")


# ============================================
# PARTIE 6 : FONCTION MAIN
# ============================================

def main():
    """
    Fonction principale : exécute tout le pipeline.
    """
    print("\n" + "=" * 70)
    print(" " * 10 + "TD 3.5 - REFACTORISATION CHAIN-LADDER")
    print(" " * 15 + "Comptabilité Prudentielle")
    print("=" * 70)
    
    # 1. Calcul Chain-Ladder complet
    resultats = calculer_chain_ladder(triangle_initial, taux_actualisation=0.02)
    
    # 2. Visualisations
    print("\n[Visualisations]")
    visualiser_comparaison_triangles(triangle_initial, resultats['triangle_complete'])
    visualiser_be_par_annee(resultats['resultats_be'])
    
    # 3. Analyse de sensibilité
    df_sensibilite = analyse_sensibilite_taux(triangle_initial)
    
    # 4. Comparaison avec Excel (exemple avec BE fictif Excel)
    # Remplacez None par votre valeur Excel si vous l'avez
    comparer_avec_excel(resultats, be_excel=None)
    
    # 5. Export des résultats
    print("\n[Export des résultats]")
    
    # Triangle complété en CSV
    df_triangle = pd.DataFrame(
        resultats['triangle_complete'],
        index=[f'Année {2018+i}' for i in range(6)],
        columns=[f'Dev {i}' for i in range(6)]
    )
    df_triangle.to_csv('/home/claude/triangle_complete.csv')
    print("Triangle complété sauvegardé : triangle_complete.csv")
    
    # Détail BE en CSV
    df_be = pd.DataFrame(resultats['resultats_be']['detail_par_annee'])
    df_be.to_csv('/home/claude/be_detail.csv', index=False)
    print("Détail BE sauvegardé : be_detail.csv")
    
    print("\n" + "=" * 70)
    print("ANALYSE TERMINÉE !")
    print("=" * 70)
    print("\n📁 Fichiers générés :")
    print("  - triangles_comparaison.png")
    print("  - be_par_annee.png")
    print("  - sensibilite_taux.png")
    print("  - triangle_complete.csv")
    print("  - be_detail.csv")
    print("\n💡 Vous pouvez maintenant comparer avec votre fichier Excel.")
    
    return resultats


# ============================================
# EXÉCUTION
# ============================================

if __name__ == "__main__":
    resultats = main()
    
    # Affichage final du résultat principal
    print("\n" + "🎯" * 35)
    print(f"BEST ESTIMATE FINAL : {resultats['resultats_be']['be_total']:.2f} k€")
    print("🎯" * 35)
