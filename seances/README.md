# Séances : le contenu du cours

Un dossier par séance, `NN_theme` (numéro sur deux chiffres, thème en minuscules ASCII). Le site
liste les séances par le champ `numero` de leur `index.qmd`, pas par le nom du dossier.

| Fichier ou dossier | Rôle | Publié sur le site |
|---|---|---|
| `index.qmd` | page de la séance : objectifs, supports, TD, corrigés | oui |
| `diapos.tex` | diapositives Beamer, compilées en `diapos.pdf` par `make pdf` (le PDF n'est pas versionné) | le PDF, s'il est mis en lien |
| `notebooks/*.ipynb` | notebooks du cours, avec leurs sorties | oui, comme pages ; plus un lien « Ouvrir dans Colab » |
| `corriges/` | corrigés (`.py`, `.ipynb`) | seulement par lien, dans un bloc `{.corrige}` d'une page en `corriges: true` |
| `figures/` | images utilisées par les supports | si utilisées |
| `*.csv` | données des TD, à la racine de la séance : le code les lit dans le dossier courant | si mises en lien |
| `*.qmd` | notes ou énoncés en texte (Markdown) | oui |

## Règles
- **Une séance sans source** (PDF seul) pointe vers son PDF dans `editions/<année>/` ; dès que la
  source est déposée, elle prend place ici et la CI la compile.
- **Le code s'exécute depuis la racine de la séance** : `make code` copie le dossier de la séance et y
  lance chaque notebook et script. Un chemin absolu (`/home/...`) le casse.
- **Corrigés** : dans `corriges/`, liés depuis un bloc `::: {.corrige}` de `index.qmd`. Ils ne sont en
  ligne qu'avec `corriges: true` dans l'en-tête de la page.
- Liens vers le dépôt : `{{< colab chemin >}}` (ouvrir un notebook dans Colab) et `{{< github chemin >}}`,
  le chemin partant de la racine du dépôt.

## Nouvelle séance
```bash
make seance N=08 SLUG=orsa     # crée seances/08_orsa/index.qmd depuis _modele/
```
