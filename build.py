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
IMG_DIR = "assets/projets"
CV_BASE = "cv-adem-nasri"          # le PDF du CV, empreinte lui aussi
MARQUE_DEBUT = "# >>> genere par build.py — ne pas editer a la main"
MARQUE_FIN = "# <<< fin du bloc genere"
RE_EMPREINTE = re.compile(r"^(?P<base>.+?)(?:\.[0-9a-f]{10})?\.webp$")


def empreinte(chemin):
    h = hashlib.sha256(open(chemin, "rb").read()).hexdigest()[:10]
    return h


def empreinte_images():
    """Renomme les captures en <base>.<empreinte>.webp.

    Meme raison que pour les CSS/JS : .htaccess demande un cache d'un an sur
    les images et le CDN garde des copies perimees. Deux captures corrigees
    etaient encore servies dans leur ancienne version. Le nom porte donc
    l'empreinte du contenu ; l'operation est idempotente (une empreinte
    existante est retiree avant d'etre recalculee)."""
    d = os.path.join(ROOT, IMG_DIR)
    if not os.path.isdir(d):
        return {}
    renommes = {}
    for f in sorted(os.listdir(d)):
        m = RE_EMPREINTE.match(f)
        if not m:
            continue
        base = m.group("base")
        h = empreinte(os.path.join(d, f))
        cible = f"{base}.{h}.webp"
        if cible != f:
            os.replace(os.path.join(d, f), os.path.join(d, cible))
            renommes[f] = cible
    return renommes


def empreinte_cv():
    """Empreinte le PDF du CV et maintient ses redirections dans .htaccess.

    Le CV est telecharge par des recruteurs : en servir une version perimee
    coute cher. .htaccess demande un cache d'un mois sur les PDF et le CDN
    servait encore le tout premier fichier. Le lien porte donc l'empreinte,
    et deux redirections gardent les anciennes adresses fonctionnelles."""
    courant = None
    for f in os.listdir(ROOT):
        m = re.match(rf"^{re.escape(CV_BASE)}(?:\.[0-9a-f]{{10}})?\.pdf$", f)
        if m:
            courant = f
            break
    if not courant:
        return None
    h = empreinte(os.path.join(ROOT, courant))
    cible = f"{CV_BASE}.{h}.pdf"
    if courant != cible:
        os.replace(os.path.join(ROOT, courant), os.path.join(ROOT, cible))

    # bloc de redirections regenere a chaque fois, entre marqueurs
    bloc = (
        f"{MARQUE_DEBUT}\n"
        "# Les anciennes adresses du CV pointent vers le fichier empreinte du moment.\n"
        f'RedirectMatch 301 "^/{CV_BASE}\\.pdf$" /{cible}\n'
        'RedirectMatch 301 "^/CV(?:%20|[ +])Adem(?:%20|[ +])Nasri(?:%20|[ +])FR(?:%20|[ +])Mainframe\\.pdf$"'
        f" /{cible}\n"
        f"{MARQUE_FIN}"
    )
    ht = os.path.join(ROOT, ".htaccess")
    contenu = open(ht, encoding="utf-8").read()
    if MARQUE_DEBUT in contenu:
        contenu = re.sub(re.escape(MARQUE_DEBUT) + r".*?" + re.escape(MARQUE_FIN),
                         bloc, contenu, flags=re.S)
    else:
        # on remplace l'ancienne redirection manuelle, sinon on ajoute en tete
        ancienne = re.compile(r'RedirectMatch 301 "\^/CV\(\?:%20.*?\n')
        if ancienne.search(contenu):
            contenu = ancienne.sub(bloc + "\n", contenu, count=1)
        else:
            contenu = bloc + "\n\n" + contenu
    open(ht, "w", encoding="utf-8").write(contenu)
    return cible


def pages_html():
    for base, dirs, fichiers in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "assets", "cv-source")]
        for f in fichiers:
            if f.endswith(".html"):
                yield os.path.join(base, f)


def main():
    renommes = empreinte_images()
    if renommes:
        print(f"{len(renommes)} captures renommees avec leur empreinte")
    cv = empreinte_cv()
    if cv:
        print(f"CV empreinte : {cv}")

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
    # le prefixe est soit relatif (../../), soit absolu (/) pour la page 404,
    # que le serveur rend a l'URL demandee : un chemin relatif y serait faux
    motif = re.compile(
        r'(href|src)="(/|(?:\.\./)*)(?:assets/build/)?'
        r'(styles|animations|nav|contact)(?:\.[0-9a-f]{6,12})?\.(css|js)"')
    motif_cv = re.compile(
        rf'(href)="(/|(?:\.\./)*)({re.escape(CV_BASE)})(?:\.[0-9a-f]{{10}})?\.pdf"')

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
        if cv:
            s2, n2 = motif_cv.subn(lambda m: f'{m.group(1)}="{m.group(2)}{cv}"', s2)
            n += n2
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
