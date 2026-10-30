# Points à relire dans le matériel déposé

Relevés en rangeant le dépôt (octobre 2026). **Ce n'est pas une relecture complète** : ce sont les
points rencontrés en chemin, à trancher par l'enseignant. Rien du contenu pédagogique n'a été modifié ;
seules ont été faites les corrections nécessaires à la compilation ou à l'exécution (voir l'historique git).

« Diapos V3 » désigne `editions/2025-2026/07_scr-mcr-fonds-propres_diapos.pdf`, dont la source LaTeX
n'est pas dans le dépôt : les mêmes erreurs y figurent, à corriger dans la source.

## 1. Contenu réglementaire (séance 7 : SCR, MCR, fonds propres)

| # | Où | Constat | Correction proposée |
|---|----|---------|---------------------|
| 1 | `seances/07_scr-mcr-fonds-propres/notes.qmd` §1.4 ; diapos V3 p. 7 | La matrice de corrélation de niveau 1 contient un module « Intangibles » et met 0,25 entre Vie et Non-vie, et entre Santé et Non-vie. Elle est attribuée à l'annexe IV du règlement délégué. | Matrice de l'**annexe IV de la directive** : Vie–Non-vie = 0, Santé–Non-vie = 0. Le risque des immobilisations incorporelles n'est pas dans la matrice : il s'ajoute après la racine (BSCR = √(Σ ρ·SCRᵢ·SCRⱼ) + SCR_intangibles, RD art. 87). |
| 2 | `notes.qmd` §7.1, exercice 7.1.1 (l. 312) | `150*0,36 + 30*0,46 * 0,95 = 68,4` : parenthèses manquantes et résultat faux. | (150 × 36 % + 30 × 46 %) × 0,95 = **64,4** M€, valeur reprise ailleurs (diapos V3, TD 7.3). |
| 3 | `notes.qmd` §7.1 ; diapos V3 ; corrigé `corriges/td-7-0_symmetric-adjustment.py` (`calculer_scr_equity`, l. 357) | SCR actions = somme des charges type 1 et type 2. | La formule standard les agrège avec une corrélation de 0,75 : √(54² + 2 × 0,75 × 54 × 13,8 + 13,8²) = 65,0 M€ avant l'abattement de 5 % (61,7 M€ après), au lieu de 67,8 (64,4). Si la somme est une simplification voulue, le dire dans l'énoncé. |
| 4 | `notes.qmd` §2.1.4 ; diapos V3 p. 38 (TD 7.1, question 3) | Choc de spread « a + b × duration » avec AAA-AA : 0,9 % + 0,06 %, A : 1,1 % + 0,07 %… ; d'où SCR spread = 2,9 M€ pour 200 M€ notés A, duration 5. | RD art. 176 : pour une duration ≤ 5 ans, choc = bᵢ × duration, avec bᵢ = 0,9 % / 1,1 % / 1,4 % / 2,5 % / 4,5 % / 7,5 % selon l'échelon de qualité de crédit 0 / 1 / 2 / 3 / 4 / 5-6 (AAA = 0, AA = 1, **A = 2**). Ici 1,4 % × 5 = 7 %, soit **14,0 M€**. |
| 5 | `notes.qmd` §3.1–3.2 | Ajustements pour capacité d'absorption des pertes rattachés aux articles 38 et 39 du RD. | Les articles 37 à 39 du RD portent sur la marge de risque. Ajustements : **RD art. 206** (PT) et **207** (impôts différés). |
| 6 | `notes.qmd` §2.5 | SCR opérationnel : `Op = max(0,03 × PT ; 0,03 × Primes)`, rattaché à l'article 164. | RD art. 204 : facteurs différents en vie et en non-vie (primes : 4 % vie, 3 % non-vie ; provisions : 0,45 % vie hors UC, 3 % non-vie), plus 25 % des frais des contrats en unités de compte. Simplification à signaler comme telle. |
| 7 | `notes.qmd` §5.2 et §7.2 ; diapos V3 p. 25 et TD 7.2 | MCR vie = 4 % × BE + 0,3 % × capitaux sous risque ; MCR non-vie = 8 % × primes + 6 % × BE ; « MCR = max(plancher ; min(MCR combiné ; 45 % SCR)) ». | RD art. 248 à 253. Vie : 3,7 % des engagements garantis des contrats avec participation, −5,2 % des prestations discrétionnaires futures, 0,7 % des UC, 2,1 % des autres engagements, **0,07 %** des capitaux sous risque. Non-vie : facteurs par segment. Encadrement : MCR combiné = min(max(MCR linéaire ; **25 %** SCR) ; 45 % SCR), puis MCR = max(MCR combiné ; plancher absolu). Les planchers (« 2,5 à 3,7 M€ ») sont révisés périodiquement : vérifier les montants en vigueur. |
| 8 | `notes.qmd` §6.2 ; diapos V3 p. 29 | « Tier 1 auxiliaire : capital *callable* » ; « Tier 3 : actifs incorporels éligibles ». | Les fonds propres auxiliaires ne sont jamais de niveau 1 : niveau 2 ou 3 seulement (directive art. 94). Les actifs incorporels sont des actifs, pas des éléments de fonds propres ; le niveau 3 comprend les impôts différés actifs nets et certains passifs subordonnés (RD art. 76). |
| 9 | `notes.qmd` §6.4 ; diapos V3 | « Tier 1 restreint + auxiliaire ≤ 20 % du SCR » ; « Tier 2 ≤ 50 % du SCR ». | RD art. 82 : niveau 1 ≥ 50 % du SCR ; niveau 3 < 15 % ; niveaux 2 + 3 ≤ 50 %. Les éléments de niveau 1 restreint sont limités à 20 % **du total du niveau 1**, pas du SCR. |
| 10 | `notes.qmd` §6.5 ; diapos V3 p. 30 | Réserve de réconciliation `… + Dividendes_prévisibles`. | Les dividendes prévisibles se **déduisent** (RD art. 70). |
| 11 | `notes.qmd` §1.1, §8 ; diapos V3 p. 3 et p. 47 | « Règlement délégué 2015/35, article 24 » pour la définition du SCR ; « ACPR, Instruction 2015-I-13 sur le calcul du SCR ». | Références non retrouvées, à vérifier. La définition du SCR est à l'article 101 de la directive. |

## 2. TD 7.0 : ajustement symétrique

| # | Où | Constat | Correction proposée |
|---|----|---------|---------------------|
| 12 | `td-7-0_symmetric-adjustment.qmd` (« Formule », l. 27) ; corrigé `.py` (l. 92 et 106) | SA = ½ × (I − Ī) / Ī. | Il manque le terme −8 % : **SA = ½ × ((I − Ī) / Ī − 8 %)**, borné à ± 10 % (directive art. 106 ; RD art. 172). Ī est la moyenne pondérée des niveaux quotidiens sur 36 mois d'un indice actions défini par l'EIOPA ; l'EuroStoxx 50 mensuel est une simplification acceptable si elle est annoncée. |
| 13 | même fichier, « Interprétation » (l. 41-42) | « SA > 0 : marché au-dessus de sa moyenne → choc **réduit** ». | Sens inversé : le choc vaut 39 % + SA, donc **SA > 0 augmente le choc** et SA < 0 le réduit. La question 4.1 du même TD donne d'ailleurs le bon sens. |
| 14 | même fichier, question 4.2 (l. 469) | « Contre : réduit le SCR quand le marché est haut ». | Inversé pour la même raison : l'ajustement alourdit la charge après une hausse et l'allège après une baisse (effet contracyclique). Les critiques portent plutôt sur la borne de ± 10 % ou l'hypothèse de retour à la moyenne. |
| 15 | titre du TD (l. 20) ; corrigé `.py` (l. 145) | « Article 106, Règlement délégué 2015/35 ». | Article 106 de la **directive** ; le calcul est au RD art. 172 ; les chocs de 39 % et 49 % au RD art. 169. |

## 3. Numérotation des séances

Le dépôt numérote les séances d'après les TD (TD 3.5 → séance 3, TD 4.x → 4, TD 7.x → 7), seule
numérotation cohérente entre les fichiers. À confirmer, puis aligner les titres :

- diapositives BE vie : sous-titre « Séance 5 » (`seances/04_be-vie/diapos.tex`, l. 58), dernière page
  « Prochaine séance : Risk Margin et SCR Vie » (l. 1607) ;
- diapositives stochastique : « Séance 6 & 7 » (`seances/05_stochastique-alm/diapos.tex`, l. 69) ;
  le notebook des codes dit « Séance 5 » ;
- cours de la séance 1 (PDF) : partie 7.2 annonce un autre plan (séance 2 SCR, 3 ALM, 4 ORSA, 5 cas pratique) ;
- TD de valorisation des produits financiers : placé en séance 2 sans certitude (il se dit « annexe au cours »).

## 4. Code

| # | Où | Constat |
|---|----|---------|
| 16 | `corriges/td-7-3_management-actions.ipynb` | La bibliothèque `waterfallcharts` (dernière version 2019) échoue avec pandas ≥ 2. Le notebook est exclu de `make code` ([`tools/code_exclu.txt`](tools/code_exclu.txt)) : remplacer le graphique en cascade par `matplotlib` (barres empilées), puis retirer l'exclusion. |
| 17 | `seances/04_be-vie/corriges/td-4_be-vie.ipynb` | Les cellules 13 et 14 répètent les cellules 4 et 5 (exercice 4.1). |
| 18 | `a-classer/untitled.ipynb` | Brouillon du graphique tornado du TD 7.3 : à intégrer ou à supprimer. |

## 5. Sources à déposer

- Source LaTeX des **diapositives SCR V3** (50 pages). `archive/07_scr-mcr-fonds-propres_diapos-courtes.tex`
  n'en produit que 18. Une fois déposée en `seances/07_scr-mcr-fonds-propres/diapos.tex`, la CI la compile.
- Source du **cours de la séance 1** (le PDF a été imprimé depuis un navigateur) et source LaTeX du
  **TD de valorisation** : avec elles, ces supports deviennent modifiables et recompilés.
- **Séance 3** : diapositives et énoncé du TD 3.5 (seul le corrigé est déposé).
- Fichiers Excel des TD, s'ils sont distribués.
