# Comptabilité prudentielle en assurance : cours de Master

*Solvabilité II : bilan prudentiel, meilleure estimation, SCR, MCR et fonds propres.*
Fabrice Borel-Mathurin (ACPR-DEAR ; Laboratoire SAF, Université Claude Bernard Lyon 1).

| | |
|---|---|
| **Site du cours** | <https://fabricebm.github.io/Compta-Prud-1/>, reconstruit et publié à chaque push sur `main` |
| **Public** | Master SAFIR, M2 en alternance, Université Paris 1 Panthéon-Sorbonne *(à confirmer)* |
| **Année** | 2026-2027 en préparation. Supports distribués en 2025-2026 figés dans [`editions/2025-2026/`](editions/2025-2026/) |
| **Construction** | `make check` construit le site et échoue sur tout lien cassé ; `make code` exécute tous les notebooks |
| **À relire** | [Points relevés dans le matériel déposé](relecture.md) : erreurs réglementaires, numérotation, sources manquantes |

---

## Organisation du dépôt

```
.
├── seances/             (1) le cours, une séance par dossier : à éditer ici
│   ├── NN_theme/
│   │   ├── index.qmd        page de la séance : objectifs, supports, TD, corrigés
│   │   ├── diapos.tex       diapositives Beamer (compilées en diapos.pdf par make pdf)
│   │   ├── notebooks/       notebooks du cours : publiés comme pages, ouvrables dans Colab
│   │   ├── corriges/        corrigés : mis en ligne quand la page déclare corriges: true
│   │   ├── figures/         images utilisées par les supports
│   │   └── *.csv, *.qmd     données des TD, notes et énoncés en texte
│   ├── _modele/         modèle de page de séance (make seance)
│   └── index.qmd        liste des séances
├── prerequis/           (2) polycopié de prérequis (LaTeX) : version étudiant et version corrigée
├── editions/            (3) supports figés tels que distribués, une année par dossier ; jamais modifiés
├── a-classer/           (4) boîte de dépôt : y poser le nouveau matériel, il sera rangé ensuite
├── archive/             versions remplacées, gardées pour mémoire ; pas publiées
├── ressources/          glossaire français–anglais, textes de référence
├── index.qmd, programme.qmd   accueil et programme du site
├── _quarto.yml          configuration du site (navigation, thème, pages publiées)
├── filtres/             corriges.lua (publication des corrigés), liens.lua (liens Colab et GitHub)
├── styles/              couleurs du site (le bleu des diapositives)
├── tools/               executer_code.py (make code), check_md_links.py (make check-links)
├── relecture.md         points à trancher dans le matériel déposé
├── CLAUDE.md            consignes pour les sessions Claude Code qui rangent le matériel
└── Makefile             la chaîne : pdf → site → check / code / release
```

Les dossiers numérotés (1) à (4) sont les séparations sur lesquelles repose le dépôt, comme dans
[SCR_After_Stress](https://github.com/FabriceBM/SCR_After_Stress) : contenu à éditer, polycopié,
versions figées, matériel brut. Chacun a son README avec ses règles.

## Démarrage rapide

Prérequis : Python ≥ 3.10 ; TeX Live avec `latexmk` pour compiler les PDF (sinon Overleaf, ou la CI).

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt   # Quarto compris
make pdf        # diapositives et polycopié en PDF
make preview    # le site en direct dans le navigateur
make check      # construit _site/ et échoue sur tout avertissement (lien cassé…)
make code       # exécute tous les notebooks et scripts Python
make help       # toutes les cibles
```

Sans rien installer : **Code > Codespaces** sur GitHub ouvre un environnement prêt (`.devcontainer/`, sans LaTeX).

## Publication du site

À chaque push sur `main`, [la CI](.github/workflows/site.yml) compile les PDF, vérifie les liens,
exécute le code, construit le site et le publie sur GitHub Pages. Une pull request fait les mêmes
vérifications sans publier.

**Une seule fois, à la création** : *Settings > Pages > Build and deployment > Source : GitHub Actions*.

## Ajouter du matériel

1. Déposer les fichiers dans [`a-classer/`](a-classer/) (sur GitHub : *Add file > Upload files*).
2. Les ranger dans `seances/NN_theme/` selon les règles de [`seances/README.md`](seances/README.md) ;
   `make seance N=08 SLUG=orsa` crée le dossier et la page d'une nouvelle séance.
3. Mettre la page de la séance à jour : objectifs, liens vers les supports, TD, corrigés.
4. `make check`, `make code`, `make check-latex` ; puis pull request vers `main`.

Une session Claude Code peut faire les étapes 2 à 4 : les consignes sont dans [`CLAUDE.md`](CLAUDE.md).

## Publier les corrigés

Dans l'en-tête de `seances/NN_theme/index.qmd`, passer `corriges: false` à `corriges: true` après la
séance : les blocs `::: {.corrige}` de la page apparaissent au prochain push. `make site-enseignant`
construit dans `_site-enseignant/` une version avec tous les corrigés, pour soi ; elle n'est jamais publiée.

**Le dépôt est public** : les corrigés y sont lisibles par qui les cherche ; le site ne les met
simplement pas en avant avant la séance. Sujets d'examen, notes, listes d'étudiants : dans `prive/`
(ignoré par git), jamais dans le dépôt.

## Fin d'année : figer une édition

`make release EDITION=2026-2027` copie les PDF compilés dans `editions/2026-2027/`. Ajouter une
ligne au registre [`editions/README.md`](editions/README.md), puis
`git add editions && git commit -m "Édition 2026-2027" && git tag 2026-2027`.
`git checkout 2026-2027` reconstruit ensuite le cours exactement tel qu'il a été donné.

## LaTeX

Chaque `diapos.tex` reste autonome et compile aussi seul sur Overleaf. La CI compile en pdfLaTeX :
les caractères Unicode hors T1 (≤, ≥, ≈, émojis) et les accents dans les blocs `lstlisting` y
provoquent des erreurs qu'Overleaf laisse passer. Le bloc « Compilation pdfLaTeX sans erreur » en
fin de préambule des diapositives 4 et 5 les traite ; le reprendre dans toute nouvelle diapositive.
`make check-latex` liste les erreurs restantes.

## Conventions

- **Noms** : minuscules ASCII, sans espace ni accent (ils cassent `make` et LaTeX). Séances :
  `NN_theme` ; données et corrigés : `td-n-m_sujet.ext`.
- **Pas de `v2`, `_vf`, `_final` dans les noms** : l'historique est dans git, les versions
  distribuées dans `editions/` et dans un tag.
- **Un PDF dans git est une édition figée** (`editions/`) ; un PDF compilable depuis une source du
  dépôt n'est jamais versionné.
- **Le site ne publie que les `.qmd` et les notebooks de `notebooks/`.** Les `.md` comme celui-ci
  documentent le dépôt et ne sont pas publiés.
- **Rien de confidentiel** : le dépôt est public. Ni document interne ACPR, ni donnée nominative, ni sujet d'examen.

## Principes pédagogiques

Le site met en œuvre quelques pratiques dont l'effet sur l'apprentissage est bien documenté :

- **alignement** des objectifs de chaque séance, des TD et de l'évaluation (Biggs, 1996, *Higher Education* 32(3)) ;
- **pratique de récupération** en ouverture de séance, plutôt que la relecture (Roediger et Karpicke,
  2006, *Psychological Science* 17(3) ; Dunlosky et al., 2013, *Psychological Science in the Public Interest* 14(1)) ;
- **apprentissage actif** en TD, de l'exemple résolu à l'exercice autonome (Freeman et al., 2014, *PNAS* 111(23)) ;
- **corrigés après l'effort**, publiés sur la page de la séance une fois celle-ci passée.
