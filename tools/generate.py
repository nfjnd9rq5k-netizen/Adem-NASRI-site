#!/usr/bin/env python3
"""Regenere la page /projets/ et les six pages etude de cas, puis rejoue
l'empreinte des CSS/JS.

    python3 tools/generate.py

Ce que ca touche :
  - projets/index.html            (la grille de vignettes)
  - projets/<slug>/index.html     (une page par etude de cas)
  - sitemap.xml                   (les URLs des etudes de cas)
  - les references CSS/JS de toutes les pages (via build.py)

Ce que ca ne touche PAS : index.html, parcours/index.html, contact/index.html.
Ces trois pages s'editent a la main ; seules leurs references CSS/JS sont
mises a jour par build.py.
"""
import os, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ICI)
sys.path.insert(0, ICI)
sys.path.insert(0, ROOT)   # pour importer build.py

import gen


def main():
    # Les captures sont empreintees AVANT la generation : le HTML doit
    # referencer le nom definitif du fichier, empreinte comprise.
    import build
    renommes = build.empreinte_images()
    if renommes:
        print(f"{len(renommes)} captures renommees avec leur empreinte\n")

    import data                      # importe apres, pour lire les noms a jour
    pages = gen.write_all(data.CASES, data.INTRO)
    print(f"{len(pages)} pages ecrites :")
    for p in pages:
        print(f"  {os.path.relpath(p, ROOT):46} {os.path.getsize(p):>7} o")

    err = os.path.join(ROOT, "404.html")
    with open(err, "w", encoding="utf-8") as f:
        f.write(gen.error_page())
    print(f"  {'404.html':46} {os.path.getsize(err):>7} o")

    chemin, n = gen.patch_sitemap(data.CASES)
    print(f"\n{os.path.relpath(chemin, ROOT)} : {n} URLs (lastmod calcule par page)")

    print()
    r = subprocess.run([sys.executable, os.path.join(ROOT, "build.py")],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit("ABANDON : build.py a echoue")


if __name__ == "__main__":
    main()
