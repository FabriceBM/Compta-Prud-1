# =============================================================================
#  Comptabilité prudentielle : chaîne de production du cours
#
#     seances/*/diapos.tex, prerequis/main.tex  --make pdf-->   PDF à côté de leur source
#     *.qmd, notebooks/, PDF, données            --make site-->  _site/  (publié sur GitHub Pages)
#     notebooks et scripts Python                --make code-->  exécutés de bout en bout
#
#  make help     liste des cibles
# =============================================================================

QUARTO  ?= quarto
PYTHON  ?= python3
LATEXMK := latexmk -pdf -interaction=nonstopmode
DIAPOS  := $(wildcard seances/*/diapos.tex)
# make seance N=08 SLUG=orsa ; make release EDITION=2026-2027
N       ?=
SLUG    ?=
EDITION ?=

.PHONY: help pdf check-latex site site-enseignant preview code check check-links seance release clean

help:
	@echo "make pdf                    compile les diapositives (seances/*/diapos.tex) et le polycopié de prérequis"
	@echo "make check-latex            échoue s'il reste une erreur LaTeX dans les PDF compilés"
	@echo "make site                   construit le site dans _site/ (corrigés publiés selon chaque page)"
	@echo "make site-enseignant        même site, tous les corrigés visibles, dans _site-enseignant/ (jamais publié)"
	@echo "make preview                site en direct dans le navigateur, mis à jour à chaque enregistrement"
	@echo "make code                   exécute tous les notebooks et scripts Python des séances"
	@echo "make check                  construit le site et échoue sur tout avertissement Quarto (lien cassé…)"
	@echo "make check-links            échoue sur un lien cassé dans les fichiers Markdown du dépôt"
	@echo "make seance N=08 SLUG=orsa  crée seances/08_orsa/ à partir du modèle seances/_modele/"
	@echo "make release EDITION=...    fige les PDF de l'année dans editions/\$$EDITION/"
	@echo "make clean                  supprime les produits de compilation et le site"

# --- LaTeX -> PDF --------------------------------------------------------------
# Comme Overleaf, -f produit le PDF même s'il reste des erreurs, pour ne jamais bloquer la
# publication du site ; `make check-latex` signale ces erreurs.
pdf:
	@for f in $(DIAPOS); do \
	  echo "==> $$f"; \
	  (cd $$(dirname $$f) && $(LATEXMK) -f diapos.tex > /dev/null 2>&1) || echo "    erreurs LaTeX : voir $${f%.tex}.log"; \
	done
	@echo "==> prerequis/main.tex (version étudiant, puis corrigée)"
	@cd prerequis && ($(LATEXMK) -f -jobname=prerequis main.tex > /dev/null 2>&1 || echo "    erreurs LaTeX : voir prerequis/prerequis.log")
	@cd prerequis && ($(LATEXMK) -f -jobname=prerequis-corrige -usepretex='\def\Corrige{}' main.tex > /dev/null 2>&1 \
	  || echo "    erreurs LaTeX : voir prerequis/prerequis-corrige.log")

check-latex: pdf
	@! grep -n -A2 '^! ' $(DIAPOS:.tex=.log) prerequis/prerequis.log prerequis/prerequis-corrige.log \
	  || (echo "ERREUR : erreurs LaTeX ci-dessus (le PDF est produit, mais incomplet ou faux à cet endroit)"; exit 1)
	@echo "==> check-latex OK : aucune erreur LaTeX"

# --- site -------------------------------------------------------------------------
site:
	$(QUARTO) render
	@echo "==> _site/index.html"

site-enseignant:
	CORRIGES=tous $(QUARTO) render --output-dir _site-enseignant
	@echo "==> _site-enseignant/index.html (tous les corrigés ; ne pas publier)"

preview:
	$(QUARTO) preview

check:
	@mkdir -p _build
	NO_COLOR=1 $(QUARTO) render 2>&1 | tee _build/render.log
	@! grep -nE '^(WARN|ERROR)' _build/render.log \
	  || (echo "ERREUR : avertissements Quarto ci-dessus (voir _build/render.log)"; exit 1)
	@echo "==> check OK : site construit sans avertissement"

check-links:
	$(PYTHON) tools/check_md_links.py

# --- code ---------------------------------------------------------------------------
code:
	MPLBACKEND=Agg $(PYTHON) tools/executer_code.py

# --- nouvelle séance, édition figée --------------------------------------------------------
seance:
	@test -n "$(N)" -a -n "$(SLUG)" || (echo "usage : make seance N=08 SLUG=orsa"; exit 1)
	@test ! -e seances/$(N)_$(SLUG) || (echo "seances/$(N)_$(SLUG) existe déjà"; exit 1)
	cp -r seances/_modele seances/$(N)_$(SLUG)
	sed -i.bak -e 's/NN_slug/$(N)_$(SLUG)/g' -e "s/^numero: 0/numero: $$(expr $(N) + 0)/" \
	  -e '/^# Modèle de page/,/^# seances\/08_orsa/d' seances/$(N)_$(SLUG)/index.qmd
	rm -f seances/$(N)_$(SLUG)/index.qmd.bak
	@echo "==> seances/$(N)_$(SLUG)/index.qmd : remplir le titre, les objectifs et les liens"

release: pdf
	@test -n "$(EDITION)" || (echo "usage : make release EDITION=2026-2027"; exit 1)
	@test ! -e editions/$(EDITION) || (echo "editions/$(EDITION) existe déjà"; exit 1)
	mkdir -p editions/$(EDITION)
	@for f in $(DIAPOS:.tex=.pdf); do cp $$f editions/$(EDITION)/$$(basename $$(dirname $$f))_diapos.pdf; done
	cp prerequis/prerequis.pdf prerequis/prerequis-corrige.pdf editions/$(EDITION)/
	@echo "==> editions/$(EDITION)/ : ajouter une ligne à editions/README.md, puis"
	@echo "    git add editions && git commit -m 'Édition $(EDITION)' && git tag $(EDITION)"

clean:
	-@for f in $(DIAPOS); do (cd $$(dirname $$f) && latexmk -C diapos.tex > /dev/null 2>&1); done
	-@cd prerequis && latexmk -C -jobname=prerequis main.tex > /dev/null 2>&1; latexmk -C -jobname=prerequis-corrige main.tex > /dev/null 2>&1
	rm -f seances/*/diapos.nav seances/*/diapos.snm seances/*/diapos.vrb
	rm -rf _site _site-enseignant _build .quarto
