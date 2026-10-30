# Consignes pour Claude Code

Dépôt du cours de comptabilité prudentielle en assurance (Solvabilité II, Master 2), publié en
site Quarto sur GitHub Pages. Lire d'abord [`README.md`](README.md) (organisation, conventions) et
[`seances/README.md`](seances/README.md) (contenu d'une séance).

## Langue
Tout le contenu destiné aux étudiants et la documentation du dépôt sont en français. Termes
réglementaires : ceux de la version française des textes ([glossaire](ressources/glossaire.qmd)),
l'anglais entre parenthèses à la première occurrence.

## L'enseignant dépose du matériel au fil de l'eau
Il arrive dans `a-classer/` ou à la racine de `main` (« Add files via upload »). Pour chaque fichier :

1. **Identifier la séance** d'après son contenu (titre, numéros de TD), pas son nom : les numéros de
   séance des fichiers sources sont incohérents (voir `relecture.md`, § 3). En cas de doute, le dire.
2. **Le ranger** (`git mv`) avec un nom conforme aux conventions :
   - source Beamer → `seances/NN_theme/diapos.tex` ;
   - notebook du cours → `notebooks/` ; corrigé (`.py`, `.ipynb` avec solutions) → `corriges/` ;
   - données → racine de la séance ; images → `figures/` ;
   - PDF dont la source n'est pas dans le dépôt → `editions/<année>/NN_theme_<type>.pdf`, mis en lien
     depuis la page de la séance ; PDF compilé depuis une source du dépôt → supprimé (la CI le recompile) ;
   - archive `.zip` de sources → décompressée, le zip supprimé ;
   - version remplacée → `archive/`, avec une ligne dans `archive/README.md`.
3. **Mettre à jour** la page `seances/NN_theme/index.qmd` (créer la séance avec `make seance`), la
   table du [`programme.qmd`](programme.qmd), et le registre `editions/README.md` si un PDF y entre.
4. **Vérifier** : `make check-latex` (pdfLaTeX, aucune erreur), `make code` (chaque notebook et script
   s'exécute), `make check` (site sans avertissement), `make check-links`.
5. **Pull request vers `main`** ; l'enseignant fusionne. Ne jamais pousser directement sur `main`.

## Ce qu'on corrige, ce qu'on signale
- **On corrige** ce qui empêche de compiler ou d'exécuter, sans changer le contenu : erreur LaTeX,
  chemin absolu, JSON de notebook invalide, artefacts d'outils (`[cite_start]`, `[cite: …]`),
  dépendance manquante dans `requirements.txt`. Chaque correction est décrite dans le message de commit.
- **On signale** dans [`relecture.md`](relecture.md), sans le modifier, tout point de fond : erreur
  réglementaire ou de calcul, incohérence entre supports, source manquante. Citer le fichier, la ligne
  ou la page, et la référence réglementaire (directive 2009/138/CE, règlement délégué (UE) 2015/35).
  Ne citer un article que si on en est sûr ; sinon écrire « à vérifier ».

## Ne jamais
- Versionner un sujet d'examen, des notes, une liste d'étudiants ou un document interne : le dépôt est
  public (`prive/` est ignoré par git).
- Modifier un fichier de `editions/`.
- Publier un corrigé : c'est l'enseignant qui passe `corriges: true` dans l'en-tête de la page.
