#!/usr/bin/env python3
"""Empreinte les fichiers CSS/JS et met a jour les references dans le HTML.

Pourquoi : le .htaccess demande un cache long sur les CSS/JS, et le CDN de
Hostinger garde des variantes compressees (br/gzip) perimees bien apres un
deploiement — plusieurs noeuds servaient encore la toute premiere feuille de
style. Un nom de fichier different a chaque version rend ce cache inoffensif :
l'URL change, donc il ne peut plus y avoir de variante ancienne.

Usage : python3 build.py   (a relancer apres chaque modification de CSS/JS)
"""
import hashlib, os, re, sys, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCES = ["styles.css", "animations.js", "nav.js", "contact.js"]
OUT_DIR = "assets/build"


def empreinte(chemin):
    h = hashlib.sha256(open(chemin, "rb").read()).hexdigest()[:10]
    return h


def pages_html():
    for base, dirs, fichiers in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "assets", "cv-source")]
        for f in fichiers:
            if f.endswith(".html"):
                yield os.path.join(base, f)


def main():
    os.makedirs(os.path.join(ROOT, OUT_DIR), exist_ok=True)
    versions = {}
    for src in SOURCES:
        p = os.path.join(ROOT, src)
        if not os.path.exists(p):
            sys.exit(f"ABANDON : source introuvable — {src}")
        nom, ext = src.rsplit(".", 1)
        h = empreinte(p)
        cible = f"{nom}.{h}.{ext}"
        shutil.copy2(p, os.path.join(ROOT, OUT_DIR, cible))
        versions[src] = cible

    # references : href/src vers styles.css, nav.js... quel que soit le prefixe
    # relatif, et qu'elles soient deja empreintees ou non
    motif = re.compile(
        r'(href|src)="((?:\.\./)*)(?:assets/build/)?'
        r'(styles|animations|nav|contact)(?:\.[0-9a-f]{6,12})?\.(css|js)"')

    total = 0
    for page in pages_html():
        s = open(page, encoding="utf-8").read()

        def rempl(m):
            attr, prefixe, nom, ext = m.groups()
            cible = versions.get(f"{nom}.{ext}")
            if not cible:
                return m.group(0)
            return f'{attr}="{prefixe}{OUT_DIR}/{cible}"'

        s2, n = motif.subn(rempl, s)
        if n:
            open(page, "w", encoding="utf-8").write(s2)
            total += n

    # menage : on retire les empreintes qui ne sont plus referencees
    gardees = set(versions.values())
    retires = 0
    d = os.path.join(ROOT, OUT_DIR)
    for f in os.listdir(d):
        if f not in gardees:
            os.remove(os.path.join(d, f))
            retires += 1

    print(f"{len(versions)} fichiers empreintes, {total} references mises a jour, "
          f"{retires} anciennes empreintes supprimees")
    for k, v in versions.items():
        print(f"  {k:16} -> {OUT_DIR}/{v}")


if __name__ == "__main__":
    main()
