# Polycopié de prérequis

Six unités progressives, de la valeur actuelle d'un flux certain au contrat d'assurance
(`U1-…tex` à `U6-…tex`), réunies par `main.tex` ; mise en forme commune dans `preambule.tex`.
Déposé comme `poly_SAFiR.zip`, décompressé ici pour que chaque modification se lise dans git.

| Commande | Produit |
|---|---|
| `make pdf` (depuis la racine) | `prerequis.pdf` (version étudiant) et `prerequis-corrige.pdf` |
| `./build-unites.sh` (depuis ce dossier) | un PDF par unité, versions étudiant et corrigée, dans `unites/` |

La version corrigée s'obtient en définissant `\Corrige` avant la compilation
(`latexmk -pdf -jobname=prerequis-corrige -usepretex='\def\Corrige{}' main.tex`) ; `main.tex` donne
la version étudiant par défaut. Sur le site, la page `index.qmd` publie la version étudiant, et la
version corrigée quand elle passe en `corriges: true`.
