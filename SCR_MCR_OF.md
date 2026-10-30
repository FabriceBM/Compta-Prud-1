# SCR, MCR et Fonds Propres en Assurance - Guide Complet

## 1. Le Capital de Solvabilité Requis (SCR)

### 1.1. Définition et objectif
- **Définition** : Montant de capital que doit détenir un assureur pour absorber les pertes imprévues sur un horizon d'un an avec un niveau de confiance de 99,5%
- **Sources réglementaires** :
  - Directive Solvabilité II (2009/138/CE), Article 101
  - Règlement Délégué (UE) 2015/35, Article 24
- **Concept économique** : Value-at-Risk (VaR) à 99,5% de la variation des fonds propres sur un an

### 1.2. Structure modulaire du SCR formule standard
```
SCR = BSCR + SCR_opérationnel - Adj_PT - Adj_DT
```

Où :
- **BSCR** : Basic SCR (agrégation des modules de risque de base)
- **SCR_opérationnel** : Risque opérationnel
- **Adj_PT** : Ajustement pour capacité d'absorption des provisions techniques
- **Adj_DT** : Ajustement pour capacité d'absorption des impôts différés

### 1.3. Les modules de risque du BSCR
**Référence** : EIOPA, "The underlying assumptions in the standard formula for the Solvency Capital Requirement calculation" (2014)

Les 6 modules principaux :
1. **Risque de marché** (SCR_market)
2. **Risque de contrepartie** (SCR_counterparty)
3. **Risque de souscription Vie** (SCR_life)
4. **Risque de souscription Non-Vie** (SCR_non-life)
5. **Risque de souscription Santé** (SCR_health)
6. **Risque d'immobilisations incorporelles** (SCR_intangible)

### 1.4. Matrice de corrélation niveau 1
**Référence** : Règlement Délégué (UE) 2015/35, Annexe IV

| Modules | Marché | Contrepartie | Vie | Non-Vie | Santé | Intangibles |
|---------|--------|--------------|-----|---------|-------|-------------|
| **Marché** | 1,00 | 0,25 | 0,25 | 0,25 | 0,25 | 0,25 |
| **Contrepartie** | 0,25 | 1,00 | 0,25 | 0,50 | 0,25 | 0,25 |
| **Vie** | 0,25 | 0,25 | 1,00 | 0,25 | 0,25 | 0,25 |
| **Non-Vie** | 0,25 | 0,50 | 0,25 | 1,00 | 0,25 | 0,25 |
| **Santé** | 0,25 | 0,25 | 0,25 | 0,25 | 1,00 | 0,25 |
| **Intangibles** | 0,25 | 0,25 | 0,25 | 0,25 | 0,25 | 1,00 |

## 2. Modules de Risque : Calculs Détaillés

### 2.1. Risque de marché - Sous-modules
**Référence** : Règlement Délégué (UE) 2015/35, Articles 105-133

#### 2.1.1. Risque action (SCR_eq)
- **Actions Type 1** (côtées EEE/OCDE) : Choc de 39% + symmetric adjustment
- **Actions Type 2** (autres) : Choc de 49% + symmetric adjustment
- **Calcul** : ΔNAV = (Actifs actions × choc) - (ΔBE lié aux actions)

#### 2.1.2. Risque immobilier (SCR_prop)
- Choc de -25% sur la valeur des actifs immobiliers
- Impact sur BE si l'assureur détient des actifs immobiliers en portefeuille

#### 2.1.3. Risque de taux (SCR_int)
- **Méthode** : Deux scénarios (hausse et baisse des taux)
- **Courbe de choc EIOPA** : Chocs par maturité (exemple : +100 bps à 10 ans)
- **Calcul** : Impact sur obligations + impact sur BE (effet inverse)

#### 2.1.4. Risque de spread (SCR_spread)
- **Formule** : Spread_choc = a + b × duration_modifiée
- **Coefficients par rating** :
  - Rating AAA-AA : a = 0,9%, b = 0,06%
  - Rating A : a = 1,1%, b = 0,07%
  - Rating BBB : a = 1,4%, b = 0,08%
  - Rating BB : a = 3,0%, b = 0,22%
  - Rating B : a = 6,5%, b = 0,38%
  - Rating C : a = 13,5%, b = 0,50%

### 2.2. Risque de contrepartie
**Référence** : Règlement Délégué (UE) 2015/35, Articles 134-142

#### 2.2.1. Type 1 (diversifiable)
- Calcul basé sur l'exposition et le rating du réassureur
- Formule : SCR_counterparty_type1 = 0,9 × LGD × PD

#### 2.2.2. Type 2 (non diversifiable)
- Applicable si concentration sur un seul réassureur important
- Calcul plus sévère

### 2.3. Risque de souscription Vie
**Référence** : Règlement Délégué (UE) 2015/35, Articles 143-153

**Chocs réglementaires** :
- **Mortalité** : +15% permanent sur les taux de mortalité
- **Longévité** : -20% permanent sur les taux de mortalité
- **Invalidité-Morbidité** : +35% année 1, +25% années suivantes
- **Rachat** : 
  - Mass lapse : 40% (ou 70%) des contrats
  - Lapse up : +50% du taux de base
  - Lapse down : -50% du taux de base
- **Frais** : +10% + inflation supplémentaire +1%
- **Catastrophe Vie** : Scénario pandémie (mortalité × 1,5)

### 2.4. Risque de souscription Non-Vie
**Référence** : Règlement Délégué (UE) 2015/35, Articles 154-163

#### 2.4.1. Module Primes-Réserves
- Formule : SCR_nl_pr = ρ(σ) × V
- Où :
  - V = volume (primes ou provisions)
  - σ = écart-type estimé par branche
  - ρ = fonction de transformation

#### 2.4.2. Catastrophe Non-Vie
- Scénarios par péril (tempête, séisme, inondation, grêle, terrorisme)
- Calcul basé sur l'exposition géographique et les limites de garantie

### 2.5. Risque opérationnel
**Référence** : Règlement Délégué (UE) 2015/35, Article 164

**Formule simplifiée** :
```
SCR_op = min(0,30 × BSCR ; Op_charge)
```
Où :
```
Op_charge = max(0,03 × Provisions_techniques ; 0,03 × Primes_annuelles)
```

## 3. Ajustements pour Capacités d'Absorption

### 3.1. Capacité d'absorption des provisions techniques (Adj_PT)
**Référence** : Règlement Délégué (UE) 2015/35, Article 38

**Concept** : Les FDB (Future Discretionary Benefits) peuvent être réduits en cas de choc, absorbant ainsi une partie des pertes

**Calcul** :
1. Calculer le BE avec PB future attendue (scénario central)
2. Calculer le BE avec PB réduite (scénario stressé)
3. Adj_PT = ΔNAV dû à la réduction de PB

**Limitation** : Adj_PT ≤ montant des FDB disponibles

### 3.2. Capacité d'absorption des impôts différés (Adj_DT)
**Référence** : Règlement Délégué (UE) 2015/35, Article 39

**Concept** : En cas de choc, création d'une perte fiscale générant des impôts différés actifs

**Calcul** :
```
Adj_DT = min(Perte_avant_impôts × Taux_IS ; IDA_max_récupérable)
```

**Conditions** :
- L'assureur doit démontrer sa capacité à générer des bénéfices futurs
- Plafonnement réglementaire

## 4. Management Actions dans le Calcul du SCR

### 4.1. Définition et importance
**Source** : EIOPA, "Guidelines on Own Risk and Solvency Assessment" (2014)

Les Management Actions (MA) sont des actions que l'assureur s'engage à prendre en cas de détérioration de sa situation financière

### 4.2. Exemples de Management Actions
1. **Réallocation d'actifs** : Vente d'actions pour réduire le SCR_market
2. **Réduction de la PB** : Diminution de la participation aux bénéfices
3. **Augmentation des primes** : Pour les produits à primes récurrentes
4. **Cession de portefeuille** : Transfert de risques

### 4.3. Conditions de reconnaissance
**Référence** : Directive Solvabilité II, Article 111

- Les MA doivent être réalistes et documentées
- Validation par le conseil d'administration
- Intégration dans l'ORSA
- Contrôle par le superviseur

## 5. Minimum Capital Requirement (MCR)

### 5.1. Définition et objectif
**Référence** : Directive Solvabilité II, Articles 129-131

Le MCR représente le seuil absolu en dessous duquel l'assureur ne peut plus exercer son activité

### 5.2. Calcul du MCR
**Référence** : Règlement Délégué (UE) 2015/35, Articles 246-258

#### 5.2.1. Formule linéaire par ligne of business

**Pour l'assurance Vie** :
```
MCR_Vie = 0,04 × BE_Vie + 0,003 × Capitaux_sous_risque
```

**Pour l'assurance Non-Vie** :
```
MCR_Non-Vie = 0,08 × Primes_annuelles + 0,06 × BE_Non-Vie
```

#### 5.2.2. Encadrement réglementaire

```
MCR = max(MCR_floor ; min(MCR_combined ; MCR_cap))
```

Où :
- **MCR_floor** : 2,5 à 3,7 M€ selon le type d'assureur
- **MCR_cap** : 45% du SCR
- **MCR_combined** : Somme des MCR par ligne of business

### 5.3. Comparaison SCR vs MCR

| Aspect | SCR | MCR |
|--------|-----|-----|
| **Niveau de confiance** | 99,5% sur 1 an | Non spécifié |
| **Objectif** | Seuil d'alerte | Seuil critique |
| **Conséquences** | Plan de rétablissement | Plan de financement ou retrait d'agrément |
| **Typique** | 100-200% du MCR | 25-35% du SCR |

## 6. Fonds Propres Prudentiels

### 6.1. Définition et composition
**Référence** : Directive Solvabilité II, Articles 87-98

Les fonds propres prudentiels représentent la différence entre la valeur des actifs et des passifs au bilan prudentiel

### 6.2. Classification en tiers
**Référence** : Règlement Délégué (UE) 2015/35, Articles 69-91

#### 6.2.1. Tier 1 - Capital de base
- **Tier 1 non restreint** : Capital social, primes d'émission, réserve de réconciliation
- **Tier 1 restreint** : Fonds de dotation mutuelles, instruments perpétuels
- **Tier 1 auxiliaire** : Capital callable

#### 6.2.2. Tier 2 - Capital complémentaire
- Dettes subordonnées (durée ≥ 10 ans)
- Lettres de crédit, garanties

#### 6.2.3. Tier 3 - Autres éléments
- Dettes subordonnées (durée 5-10 ans)
- Impôts différés actifs nets
- Actifs incorporels éligibles

### 6.3. Critères de classification
**Référence** : EIOPA, "Guidelines on the classification of own funds" (2015)

1. **Disponibilité permanente**
2. **Subordination totale**
3. **Durée suffisante** (perpétuelle pour Tier 1)
4. **Absence de charges obligatoires**
5. **Capacité d'absorption des pertes**

### 6.4. Limites d'éligibilité

**Pour couvrir le SCR** :
- Tier 1 ≥ 50% du SCR
- Tier 1 restreint + auxiliaire ≤ 20% du SCR
- Tier 3 ≤ 15% du SCR
- Tier 2 ≤ 50% du SCR

**Pour couvrir le MCR** :
- Tier 1 non restreint ≥ 80% du MCR
- Tier 2 ≤ 20% du MCR
- Tier 3 non éligible

### 6.5. Réserve de réconciliation
**Concept** : Élément central du Tier 1, représentant l'excédent d'actif sur passif après déduction des autres éléments de fonds propres

**Calcul** :
```
Réserve_réconciliation = Excédent_actif_passif
                       - Capital_social
                       - Primes_émission
                       - Autres_éléments_Tier1
                       + Dividendes_prévisibles
```

### 6.6. Évolution des fonds propres
**Facteurs d'augmentation** :
- Bénéfice de l'exercice
- Augmentation de capital
- Plus-values latentes sur actifs
- Diminution du BE (hausse des taux)

**Facteurs de diminution** :
- Perte de l'exercice
- Dividendes distribués
- Moins-values latentes
- Augmentation du BE (baisse des taux)

## 7. Travaux Dirigés (TD)

### 7.1. Calcul complet du SCR formule standard

#### Exercice 7.1.1 : Modules de risque de marché (Excel)

**Données** :
- Actifs :
  - Actions Type 1 : 150 M€
  - Actions Type 2 : 30 M€  
  - Obligations souveraines : 300 M€
  - Obligations corporate (rating A, duration 5 ans) : 200 M€
  - Immobilier : 80 M€
- Passifs : BE = 750 M€ (dont 90% sensible aux taux)
- Symmetric adjustment actions : -3%

**Calculs Excel** :

1. **SCR_Equity**
```excel
= (150 * (39% - 3%) + 30 * (49% - 3%)) * (1 - 5%)
= 150*0,36 + 30*0,46 * 0,95 = 68,4 M€
```

2. **SCR_Interest Rate**
- Scénario hausse : Impact obligations = -4,2%, Impact BE = +3,8%
- Scénario baisse : Impact obligations = +4,5%, Impact BE = -4,1%
- SCR_Int = max(Scénario hausse; Scénario baisse) = 45,2 M€

#### Exercice 7.1.2 : Agrégation avec matrice de corrélation

**Matrice Excel** :
```excel
= RACINE(SOMMEPROD(SOMMEPROD(matrice_SCR; matrice_corr); matrice_SCR))
```

### 7.2. MCR et éligibilité des fonds propres

#### Exercice 7.2.1 : Calcul du MCR

**Données** :
- BE_Vie = 500 M€
- Capitaux sous risque = 100 M€
- Primes Non-Vie = 50 M€
- BE_Non-Vie = 80 M€

**Calcul** :
```excel
MCR_Vie = 0,04*500 + 0,003*100 = 20,3 M€
MCR_Non-Vie = 0,08*50 + 0,06*80 = 8,8 M€
MCR_combined = 20,3 + 8,8 = 29,1 M€
```

#### Exercice 7.2.2 : Classification des fonds propres

**Tableau Excel de classification** :

| Élément | Montant (M€) | Tier | Limite SCR | Limite MCR |
|---------|--------------|------|------------|------------|
| Capital social | 60 | T1 non restreint | 100% | 100% |
| Dettes subordonnées 12 ans | 40 | T2 | 50% | 20% |
| Impôts différés actifs | 15 | T3 | 15% | 0% |

### 7.3. Management Actions et sensibilité du SCR

#### Exercice 7.3.1 : Impact des Management Actions

**Scénario sans MA** :
- SCR_market = 95 M€
- SCR total = 120 M€

**Scénario avec MA** :
- Vente de 50% des actions → SCR_market = 65 M€
- SCR total = 95 M€

**Économie de capital** : 25 M€ (21%)

#### Exercice 7.3.2 : Analyse de sensibilité Python

```python
import matplotlib.pyplot as plt
import numpy as np

# Données de sensibilité
parametres = ['Taux', 'Actions', 'Spread', 'Mortalité', 'Rachat']
scr_base = [45, 68, 23, 18, 22]
scr_sensibilite = [52, 81, 28, 21, 29]

# Graphique tornado
plt.figure(figsize=(10, 6))
plt.barh(parametres, np.array(scr_sensibilite) - np.array(scr_base))
plt.xlabel('Impact sur le SCR (M€)')
plt.title('Analyse de sensibilité du SCR')
plt.grid(True, alpha=0.3)
plt.show()
```

## 8. Sources Réglementaires Principales

1. **Directive 2009/138/CE** (Solvency II)
2. **Règlement Délégué (UE) 2015/35**
3. **EIOPA** - Guidelines on SCR standard formula (2014)
4. **ACPR** - Instruction 2015-I-13 sur le calcul du SCR
5. **EIOPA** - Technical documentation of the SCR standard formula
6. **Commission européenne** - Questions and Answers on Solvency II

Ce guide complet couvre l'ensemble des aspects réglementaires et techniques du SCR, MCR et des fonds propres en assurance selon le cadre Solvabilité II.