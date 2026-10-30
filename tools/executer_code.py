"""Exécute tout le code du cours : notebooks (.ipynb) et scripts (.py) de seances/ et prerequis/.

Chaque fichier s'exécute dans une copie temporaire de son dossier de séance, avec ce dossier comme
répertoire courant : les données (.csv) posées à la racine de la séance sont trouvées, et les fichiers
que le code écrit (figures, exports) ne salissent pas le dépôt. Les graphiques ne s'affichent pas
(MPLBACKEND=Agg). Les dossiers a-classer/ et archive/ ne sont pas exécutés.

Un fichier qui ne doit pas être exécuté (énoncé à trous, appel réseau, calcul trop long) se déclare
dans tools/code_exclu.txt, une ligne par chemin, avec la raison en commentaire.

Lancer depuis la racine du dépôt :  make code   (ou  python3 tools/executer_code.py [fichier ...])
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIERS = ["seances", "prerequis"]
DELAI = 600  # secondes par fichier


def exclus():
    f = RACINE / "tools" / "code_exclu.txt"
    if not f.exists():
        return {}
    out = {}
    for ligne in f.read_text(encoding="utf8").splitlines():
        chemin, _, raison = ligne.partition("#")
        if chemin.strip():
            out[chemin.strip()] = raison.strip()
    return out


def dossier_seance(fichier):
    """seances/07_x/corriges/a.py -> seances/07_x ; prerequis/a.py -> prerequis"""
    rel = fichier.relative_to(RACINE)
    return RACINE.joinpath(*rel.parts[:2]) if rel.parts[0] == "seances" else RACINE / rel.parts[0]


def executer(fichier):
    import nbformat
    from nbclient import NotebookClient

    base = dossier_seance(fichier)
    with tempfile.TemporaryDirectory() as tmp:
        copie = Path(tmp) / base.name
        shutil.copytree(base, copie, ignore=shutil.ignore_patterns("*.pdf", "*.aux", "*.log"))
        cible = copie / fichier.relative_to(base)
        if fichier.suffix == ".py":
            r = subprocess.run([sys.executable, str(cible)], cwd=copie, capture_output=True, text=True,
                               timeout=DELAI, env={**os.environ, "MPLBACKEND": "Agg"})
            if r.returncode:
                raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1])
        else:
            nb = nbformat.read(cible, as_version=4)
            os.environ["MPLBACKEND"] = "Agg"
            NotebookClient(nb, timeout=DELAI, kernel_name="python3",
                           resources={"metadata": {"path": str(copie)}}).execute()


def main(args):
    fichiers = [Path(a).resolve() for a in args] or sorted(
        p for d in DOSSIERS for ext in ("*.ipynb", "*.py") for p in (RACINE / d).rglob(ext)
        if ".ipynb_checkpoints" not in p.parts)
    a_exclure, echecs = exclus(), []
    for f in fichiers:
        rel = f.relative_to(RACINE).as_posix()
        if rel in a_exclure:
            print(f"  exclu  {rel}  ({a_exclure[rel]})")
            continue
        t0 = time.time()
        try:
            executer(f)
            print(f"  ok     {rel}  ({time.time() - t0:.0f} s)")
        except Exception as e:  # noqa: BLE001 -- on rapporte toute erreur du code exécuté
            msg = str(e).strip().splitlines()
            print(f"  ÉCHEC  {rel}\n         {msg[-1] if msg else type(e).__name__}")
            echecs.append(rel)
    print(f"==> {len(fichiers)} fichier(s) de code, {len(echecs)} échec(s)")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
