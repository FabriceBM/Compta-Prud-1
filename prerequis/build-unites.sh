#!/bin/bash
# Compile chaque unité en PDF autonome, en version corrigée et étudiant.
# Usage : ./build-unites.sh
set -e

UNITES="U1-flux-certain U2-echeancier-certain U3-echeancier-taux U4-flux-aleatoire U5-flux-optionnel U6-contrat-assurance"
mkdir -p unites

for U in $UNITES; do
  for MODE in corrige etudiant; do
    if [ "$MODE" = "corrige" ]; then BOOL="\\correctiontrue"; else BOOL="\\correctionfalse"; fi
    cat > tmp-$U-$MODE.tex <<EOF
\documentclass[11pt,a4paper]{article}
\input{preambule}
$BOOL
\begin{document}
\input{$U}
\end{document}
EOF
    pdflatex -interaction=nonstopmode tmp-$U-$MODE.tex > /dev/null 2>&1 || true
    pdflatex -interaction=nonstopmode tmp-$U-$MODE.tex > /dev/null 2>&1 || true
    mv tmp-$U-$MODE.pdf unites/$U-$MODE.pdf
    rm -f tmp-$U-$MODE.*
  done
  echo "  $U"
done

echo "PDF par unité dans : unites/"
