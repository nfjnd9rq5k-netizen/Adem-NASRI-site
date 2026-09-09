# -*- coding: utf-8 -*-
"""Generateur des pages etude de cas du portfolio Adem Nasri.
Une seule source de verite pour le gabarit : les 6 pages sortent identiques
en structure, seules les donnees changent."""
import datetime, html, json, os, subprocess, sys

# la racine du site = le dossier parent de tools/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://adem-nasri.fr"

def e(s):
    return html.escape(str(s), quote=True)

def nav(active, up):
    """up = prefixe pour remonter a la racine ('../' ou '../../')"""
    return f'''<nav class="nav">
  <a href="{up}" class="nav-logo">adem<span class="dot"></span></a>
  <button class="nav-burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="primary-nav">
    <span></span><span></span><span></span>
  </button>
  <ul class="nav-links" id="primary-nav">
    <li><a href="{up}">Accueil</a></li>
    <li><a href="{up}projets/"{' class="active"' if active=='projets' else ''}>Projets</a></li>
    <li><a href="{up}parcours/"{' class="active"' if active=='parcours' else ''}>Parcours</a></li>
    <li><a href="{up}contact/"{' class="active"' if active=='contact' else ''}>Contact</a></li>
  </ul>
  <a href="{up}cv-adem-nasri.pdf" download="CV-Adem-Nasri.pdf" class="nav-cv">↓ CV</a>
</nav>'''

def head(title, desc, canonical, up, og_image, extra_ld=""):
    return f'''<!doctype html>
<html lang="fr" data-accent="orange" data-mode="light">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<script>document.documentElement.classList.add('js')</script>
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}"/>
<meta name="author" content="Adem Nasri"/>
<meta name="robots" content="index, follow"/>
<meta name="theme-color" content="#d8541f"/>

<link rel="canonical" href="{canonical}"/>

<meta property="og:type" content="article"/>
<meta property="og:locale" content="fr_FR"/>
<meta property="og:site_name" content="Adem Nasri — Portfolio"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:title" content="{e(title)}"/>
<meta property="og:description" content="{e(desc)}"/>
<meta property="og:image" content="{og_image}"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="750"/>

<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{e(title)}"/>
<meta name="twitter:description" content="{e(desc)}"/>
<meta name="twitter:image" content="{og_image}"/>

<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Caveat:wght@400;500;600;700&family=Caveat+Brush&family=Kalam:wght@300;400;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>

<link rel="icon" type="image/svg+xml" href="{up}favicon.svg"/>
<link rel="icon" type="image/png" sizes="32x32" href="{up}favicon-32.png"/>
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png"/>

<link rel="stylesheet" href="{up}styles.css"/>
</head>
<body>
'''

def contact_strip(up, num):
    return f'''
<section class="section contact-strip" id="contact" style="margin-top:56px">
  <div class="shell">
    <div class="section-label" data-reveal><span class="ink-dot"></span><span class="label">✉ Contact · {num}</span></div>
    <div class="contact-grid">
      <div>
        <h2 class="hand-xxl" data-reveal data-reveal-delay="1">Causons<span style="color:var(--accent)">.</span></h2>
        <p class="body-lg lead" data-reveal data-reveal-delay="2">Un site à construire, un référencement à reprendre, ou simplement une question technique : je réponds vite, et toujours en personne.</p>
        <a href="{up}contact/" class="btn">M'écrire un mot →</a>
      </div>
      <div class="contact-list">
        <a href="mailto:nasri.adem@hotmail.fr" class="contact-line" data-reveal data-reveal-delay="0">
          <div class="label">Email</div><div class="value">nasri.adem@hotmail.fr</div>
        </a>
        <a href="tel:0618567675" class="contact-line" data-reveal data-reveal-delay="1">
          <div class="label">Téléphone</div><div class="value">06 18 56 76 75</div>
        </a>
        <a href="https://www.linkedin.com/in/adem-nasri" class="contact-line" data-reveal data-reveal-delay="2">
          <div class="label">LinkedIn</div><div class="value">linkedin.com/in/adem-nasri</div>
        </a>
        <div class="contact-line" data-reveal data-reveal-delay="3">
          <div class="label">Localisation</div><div class="value">12 rue d'Orchampt, Paris 18ᵉ</div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

def footer(up):
    return f'''
<footer class="footer">
  <div class="shell footer-row">
    <div data-reveal>
      <div class="hand-lg name">adem<span style="color:var(--accent)">.</span></div>
      <div class="marker-sm name-sub">Fait main, à Paris, en 2026.</div>
    </div>
    <div class="footer-meta mono" data-reveal data-reveal-delay="1">
      © 2026 Adem Nasri · tous droits réservés<br/>
      — pas de cookies, pas de tracking, juste un site.
    </div>
  </div>
</footer>
'''

def scripts(up):
    return f'''
<script src="{up}nav.js" defer></script>
<script src="{up}animations.js" defer></script>
</body>
</html>
'''

def site_frame(url_label, img, w, h, sf_h=320, dur=None, alt="", lazy=True, hint=True, autoplay=True):
    """Cadre navigateur avec capture qui defile. La duree est calee sur la
    hauteur reelle pour que la vitesse de defilement soit la meme partout."""
    if dur is None:
        # ~205 px de capture par seconde, borne entre 16 et 46 s
        dur = max(16, min(46, round(h / 205)))
    hint_html = '\n      <span class="sf-scrollhint">ça défile ↓</span>' if hint else ''
    style = f"--sf-dur:{dur}s" + (f";--sf-h:{sf_h}px" if sf_h else "")
    auto = " data-autoplay" if autoplay else ""
    return f'''<figure class="site-frame"{auto} style="{style}">
      <div class="sf-chrome">
        <span class="sf-dot"></span><span class="sf-dot"></span><span class="sf-dot"></span>
        <span class="sf-url">{e(url_label)}</span>
      </div>
      <div class="sf-view">
        <img src="{img}" alt="{e(alt)}" width="{w}" height="{h}"{' loading="lazy" decoding="async"' if lazy else ''}/>
      </div>{hint_html}
      <span class="pd-tape"></span>
    </figure>'''


def souligne(width=220):
    """Le double trait dessine a la main qui souligne les h2 de l'accueil."""
    return (f'<svg class="draw-stroke" viewBox="0 0 300 18" preserveAspectRatio="none" '
            f'style="width:{width}px;height:18px;margin-top:10px;color:var(--accent)" aria-hidden="true">'
            '<path d="M3 6 C 40 1, 80 11, 130 5 S 220 11, 297 4" fill="none" stroke="currentColor" '
            'stroke-width="2.5" stroke-linecap="round"/>'
            '<path d="M5 14 C 50 10, 100 17, 160 12 S 240 16, 295 13" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" opacity="0.7"/></svg>')


def label(symbole, texte, num=None):
    n = f" · {num}" if num else ""
    return (f'<div class="section-label" data-reveal><span class="ink-dot"></span>'
            f'<span class="label">{symbole} {texte}{n}</span></div>')


def case_page(c, prev, nxt):
    """Page etude de cas. Meme grammaire visuelle que l'accueil : tete de section
    en deux colonnes, alternance clair / sombre, polaroids inclines, traits dessines."""
    up = "../../"
    slug = c["slug"]
    canonical = f"{BASE}/projets/{slug}/"
    A = f"{up}assets/projets/"
    v = c.get("visuels", {})
    og = f"{BASE}/assets/projets/{v['hero'][0]}" if v.get("hero") else f"{BASE}/assets/og-image.webp"

    out = [head(c["title"], c["desc"], canonical, up, og)]
    out.append(nav("projets", up))
    out.append("\n<main id=\"main\">\n")

    # ---------- 1. HERO : texte a gauche, capture du site a droite ----------
    if v.get("scroll"):
        img, w, h = v["scroll"]
        frame = site_frame(c["lien_label"], A + img, w, h, sf_h=None,
                           alt="Le site " + c["nom"] + ", page d'accueil", lazy=False)
        shot = ('      <div class="case-shot" data-reveal data-reveal-delay="3">\n        '
                + frame + "\n      </div>")
        grid_open, grid_close = '<div class="case-hero-grid">', "</div>"
    else:
        shot, grid_open, grid_close = "", "<div>", "</div>"

    if c.get("lien"):
        cta = ('<a href="' + c["lien"] + '" target="_blank" rel="noopener noreferrer" '
               'class="btn">Voir le site en ligne →</a>')
    elif c.get("lien_note"):
        cta = '<span class="marker-lg" style="color:var(--ink-mute)">' + e(c["lien_note"]) + "</span>"
    else:
        cta = ""

    metas = [("Client", e(c["client"])), ("Année", e(c["annee"])),
             ("Mon rôle", e(c["role"])), ("Stack", e(" · ".join(c["stack"])))]
    meta_html = "\n        ".join(
        '<div><div class="k">' + k + '</div><div class="v">' + val + "</div></div>"
        for k, val in metas)

    out.append(f"""<section class="section case-intro">
  <div class="shell">
    <a href="{up}projets/" class="case-back" data-reveal>← Tous les projets</a>
    {label("✦", "Étude de cas", c["num"])}
    {grid_open}
      <div>
        <h1 class="hand-xxl" data-reveal data-reveal-delay="1">{e(c["nom"])}</h1>
        <p class="marker-lg lead" data-reveal data-reveal-delay="2">{e(c["accroche"])}</p>
        {cta}
      </div>
{shot}
    {grid_close}
    <div class="case-meta" data-reveal>
        {meta_html}
    </div>
  </div>
</section>
""")

    # ---------- 2. LE POINT DE DEPART ----------
    cite = ""
    if c.get("citation"):
        cite = ('\n        <blockquote class="case-quote" data-reveal data-reveal-delay="2">\n'
                "          <p>« " + e(c["citation"]) + " »</p>\n"
                "          <cite>Extrait du site " + e(c["lien_label"]) + "</cite>\n"
                "        </blockquote>")
    out.append(f"""<section class="section">
  <div class="shell">
    {label("✱", "Le point de départ", "01")}
    <div class="about-grid">
      <div>
        <h2 class="hand-xl" data-reveal data-reveal-delay="1">Le point<br/>de <span style="color:var(--accent)">départ</span>.</h2>
        {souligne(200)}
      </div>
      <div>
        <p class="body-lg" data-reveal data-reveal-delay="1">{e(c["probleme"])}</p>{cite}
      </div>
    </div>
  </div>
</section>
""")

    # ---------- 3. CE QUE J'AI FAIT (fond sombre) ----------
    items = "\n".join(
        '      <div class="did-item" data-reveal data-reveal-delay="' + str(min(i, 4)) + '">\n'
        '        <span class="num-circle">' + f"{i+1:02d}" + "</span>\n"
        '        <p class="body-md">' + e(x) + "</p>\n"
        "      </div>"
        for i, x in enumerate(c["fait"]))
    fonc = ""
    if c.get("fonctionnalites"):
        tags = "".join('<span class="tag">' + e(x) + "</span>" for x in c["fonctionnalites"])
        fonc = ('\n    <div style="margin-top:44px" data-reveal>\n'
                '      <div class="k" style="font-family:var(--font-mono);font-size:.68rem;'
                'text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px">'
                "Fonctionnalités livrées</div>\n"
                '      <div class="tags">' + tags + "</div>\n    </div>")
    out.append(f"""<section class="section section-night">
  <div class="shell">
    {label("✓", "Ce que j'ai fait", "02")}
    <div class="skills-head">
      <h2 class="hand-xl" data-reveal data-reveal-delay="1">Ce que<br/>j'ai <span style="color:var(--accent)">fait</span>.</h2>
      <p class="body-lg" data-reveal data-reveal-delay="2">{e(c.get("fait_intro", "Le détail de ce qui a été livré, point par point."))}</p>
    </div>
    <div class="did-grid">
{items}
    </div>{fonc}
  </div>
</section>
""")

    # ---------- 4. EN CHIFFRES ----------
    if c.get("preuves"):
        cards = "\n".join(
            '      <div class="proof-card" data-reveal data-reveal-delay="' + str(min(i, 4)) + '">'
            '<span class="n">' + e(p["n"]) + '</span><span class="l">' + e(p["l"]) + "</span></div>"
            for i, p in enumerate(c["preuves"]))
        out.append(f"""<section class="section">
  <div class="shell">
    {label("▲", "En chiffres", "03")}
    <div class="skills-head">
      <h2 class="hand-xl" data-reveal data-reveal-delay="1">En<br/><span style="color:var(--accent)">chiffres</span>.</h2>
      <p class="body-lg" data-reveal data-reveal-delay="2">{e(c["preuves_intro"])}</p>
    </div>
    <div class="proof-grid">
{cards}
    </div>
  </div>
</section>
""")

    # ---------- 5. DIRECTION ARTISTIQUE ----------
    if c.get("design"):
        d = c["design"]
        sw = "".join('<div class="swatch"><i style="background:' + col + '"></i><span>'
                     + e(col) + "</span></div>" for col in d.get("couleurs", [])[:5])
        duo = ""
        if v.get("page2") or v.get("mobile"):
            left = right = ""
            if v.get("page2"):
                i2, w2, h2 = v["page2"]
                left = ("<div>" + site_frame(c["page2_label"], A + i2, w2, h2, sf_h=None,
                                             alt="Page intérieure du site " + c["nom"])
                        + '<div class="marker-sm" style="color:var(--ink-mute);padding-top:12px">'
                        + e(c["page2_legende"]) + "</div></div>")
            if v.get("mobile"):
                i3, w3, h3 = v["mobile"]
                right = ('<figure class="shot-mobile">\n        <img src="' + A + i3
                         + '" alt="Le site ' + e(c["nom"]) + ' sur mobile" width="' + str(w3)
                         + '" height="' + str(h3) + '" loading="lazy" decoding="async"/>\n'
                         "        <figcaption>sur mobile</figcaption>\n      </figure>")
            duo = ('\n    <div class="shot-duo" data-reveal>\n      ' + left
                   + "\n      " + right + "\n    </div>")
        out.append(f"""<section class="section">
  <div class="shell">
    {label("◆", "La direction artistique", "04")}
    <div class="about-grid">
      <div>
        <h2 class="hand-xl" data-reveal data-reveal-delay="1">La direction<br/><span style="color:var(--accent)">artistique</span>.</h2>
        {souligne(240)}
        <div class="case-swatches" data-reveal data-reveal-delay="2">{sw}</div>
      </div>
      <div>
        <p class="body-lg" data-reveal data-reveal-delay="1">{e(d["signature"])}</p>
        <p class="marker-lg" style="color:var(--ink-mute);margin-top:18px" data-reveal data-reveal-delay="2">Typographie : {e(d["typo"])}</p>
      </div>
    </div>{duo}
  </div>
</section>
""")

    # ---------- 6. L'HISTOIRE (fond sombre) ----------
    out.append(f"""<section class="section section-night">
  <div class="shell">
    {label("✎", "L'histoire", "05")}
    <div class="story-grid">
      <div>
        <h2 class="hand-xl" data-reveal data-reveal-delay="1">L'<span style="color:var(--accent)">histoire</span>.</h2>
      </div>
      <div>
        <p class="story-text" data-reveal data-reveal-delay="2">{e(c["story"])}</p>
      </div>
    </div>
  </div>
</section>
""")

    # ---------- 7. precedent / suivant ----------
    p_html = ('<div><span class="k">Projet précédent</span><a href="../' + prev["slug"]
              + '/">← ' + e(prev["nom"]) + "</a></div>") if prev else "<div></div>"
    n_html = ('<div style="text-align:right"><span class="k">Projet suivant</span><a href="../'
              + nxt["slug"] + '/">' + e(nxt["nom"]) + " →</a></div>") if nxt else "<div></div>"
    out.append(f"""<section class="shell">
  <div class="case-jump">
    {p_html}
    {n_html}
  </div>
</section>
""")

    out.append(contact_strip(up, "06"))
    out.append("\n</main>\n")
    out.append(footer(up))

    ld = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": c["nom"],
        "headline": c["title"],
        "description": c["desc"],
        "url": canonical,
        "inLanguage": "fr",
        "creator": {"@type": "Person", "name": "Adem Nasri", "url": BASE + "/"},
        "keywords": ", ".join(c["stack"]),
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Projets", "item": BASE + "/projets/"},
                {"@type": "ListItem", "position": 3, "name": c["nom"], "item": canonical},
            ],
        },
    }
    if c.get("lien"):
        ld["about"] = {"@type": "Organization", "name": c["client_court"], "url": c["lien"]}
    out.append('\n<script type="application/ld+json">\n'
               + json.dumps(ld, ensure_ascii=False, indent=2) + "\n</script>\n")
    out.append(scripts(up))
    return "".join(out)


def listing_page(cases, intro):
    """Genere /projets/ : une grille de vignettes. Chaque vignette mene au site
    du client ET a l'etude de cas detaillee."""
    up = "../"
    canonical = f"{BASE}/projets/"
    A = f"{up}assets/projets/"
    title = "Projets — Adem Nasri | Sites clients, SEO/GEO et outils internes"
    desc = ("Six projets livrés : sites vitrines et e-commerce, référencement SEO/GEO, "
            "outil interne d'études consommateurs. Chaque projet avec son étude de cas détaillée.")

    out = [head(title, desc, canonical, up, f"{BASE}/assets/og-image.webp")]
    out.append(nav("projets", up))
    out.append('\n<main id="main">\n')
    out.append(f'''
<section style="padding:64px 0 22px">
  <div class="shell">
    <div class="label" data-reveal style="margin-bottom:16px">★ Projets · l'intégrale</div>
    <h1 class="hand-xl" data-reveal data-reveal-delay="1" style="margin-bottom:16px">
      Tout ce que j'ai déjà <span style="color:var(--accent)">livré.</span>
    </h1>
    <p class="body-lg" data-reveal data-reveal-delay="2" style="max-width:680px">{intro}</p>
  </div>
</section>

<section class="shell">
  <div class="case-grid">
''')

    for c in cases:
        v = c.get("visuels", {})
        if v.get("card"):
            img, w, h = v["card"]
            visual = site_frame(c["lien_label"], A + img, w, h, sf_h=None,
                                alt=f"Aperçu du site {c['nom']}", autoplay=False, hint=False)
        else:
            visual = (f'<div class="cc-noshot">{e(c.get("visuel_absent", "capture indisponible"))}'
                      f'<span class="pd-tape"></span></div>')

        proof = ""
        if c.get("preuves"):
            items = "".join(
                f'<div><span class="n">{e(p["n"])}</span><span class="l">{e(p["l"])}</span></div>'
                for p in c["preuves"][:2])
            proof = f'<div class="cc-proof">{items}</div>'

        if c.get("lien"):
            site = (f'<a href="{c["lien"]}" target="_blank" rel="noopener noreferrer" '
                    f'class="cc-site">Voir le site ↗</a>')
        else:
            site = f'<span class="cc-site is-off">{e(c.get("lien_note", "non public"))}</span>'

        out.append(f'''
    <article class="case-card" data-reveal>
      {visual}
      <div class="cc-head">
        <span class="cc-num">{c["num"]}</span>
        <span class="cc-year">{e(c["annee"])}</span>
      </div>
      <h2><a href="./{c["slug"]}/">{e(c["nom"])}</a></h2>
      <div class="cc-role">{e(c["role"])}</div>
      <p class="cc-body">{e(c["resume_carte"])}</p>
      {proof}
      <div class="cc-links">
        <a href="./{c["slug"]}/" class="cc-case">L'étude de cas →</a>
        {site}
      </div>
    </article>
''')

    out.append("\n  </div>\n</section>\n")
    out.append(contact_strip(up, "06"))
    out.append("\n</main>\n")
    out.append(footer(up))

    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Projets — Adem Nasri",
        "url": canonical,
        "inLanguage": "fr",
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Projets", "item": canonical},
            ],
        },
        "hasPart": [
            {"@type": "CreativeWork", "name": c["nom"],
             "url": f"{BASE}/projets/{c['slug']}/", "about": c["resume_carte"]}
            for c in cases
        ],
    }
    out.append('\n<script type="application/ld+json">\n'
               + json.dumps(ld, ensure_ascii=False, indent=2) + "\n</script>\n")
    out.append(scripts(up))
    return "".join(out)


def write_all(cases, intro):
    """Ecrit la page liste + une page par etude de cas."""
    written = []
    p = os.path.join(ROOT, "projets", "index.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(listing_page(cases, intro))
    written.append(p)
    for i, c in enumerate(cases):
        prev = cases[i - 1] if i > 0 else None
        nxt = cases[i + 1] if i < len(cases) - 1 else None
        d = os.path.join(ROOT, "projets", c["slug"])
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "index.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(case_page(c, prev, nxt))
        written.append(p)
    return written


def home_rows(cases):
    """Les lignes projet de la page d'accueil (structure .project-row existante)."""
    blocks = []
    for i, c in enumerate(cases):
        if c.get("lien"):
            url = f'<a href="{c["lien"]}" target="_blank" rel="noopener noreferrer" class="mono url">↗ {e(c["lien_label"])}</a>'
        else:
            url = f'<div class="mono url">{e(c.get("lien_note", ""))}</div>'
        tags = "".join(f'<span class="tag">{e(t)}</span>' for t in c["stack"][:4])
        blocks.append(f'''    <article class="project-row" data-reveal data-reveal-delay="{min(i, 4)}">
      <div class="num-circle">{c["num"]}</div>
      <div>
        <h3 class="hand-lg"><a href="projets/{c["slug"]}/">{e(c["nom"])}</a></h3>
        <div class="role">{e(c["role"])}</div>
        {url}
      </div>
      <div>
        <p class="body-md" style="margin-bottom:12px">{e(c["resume_home"])}</p>
        <div class="tags">{tags}</div>
        <a href="projets/{c["slug"]}/" class="marker-md" style="color:var(--accent);display:inline-block;margin-top:12px">Voir l'étude de cas →</a>
      </div>
      <div class="year">{e(c["annee"])}</div>
    </article>''')
    return "\n\n".join(blocks)


def patch_home(cases):
    """Remplace les .project-row de index.html par les nouvelles."""
    p = os.path.join(ROOT, "index.html")
    src = open(p, encoding="utf-8").read()
    start = src.find('    <article class="project-row"')
    if start == -1:
        raise SystemExit("ABANDON : bloc .project-row introuvable dans index.html")
    end_marker = "  </div>\n</section>\n\n<!-- EXPERIENCE -->"
    end = src.find(end_marker, start)
    if end == -1:
        raise SystemExit("ABANDON : fin de la section #projets introuvable")
    new = src[:start] + home_rows(cases) + "\n" + src[end:]
    open(p, "w", encoding="utf-8").write(new)
    return p, src.count('<article class="project-row"'), len(cases)


def _date_modif(chemin_relatif):
    """Date de derniere modification reelle d'une page.

    On interroge git plutot que la date du fichier : regenerer les pages touche
    le mtime meme quand le contenu n'a pas bouge, alors que lastmod doit dire
    quand le CONTENU a change. Si la page a des modifications non commitees,
    c'est qu'elle change aujourd'hui."""
    chemin = os.path.join(ROOT, chemin_relatif)
    if not os.path.exists(chemin):
        return datetime.date.today().isoformat()
    try:
        modifie = subprocess.run(["git", "status", "--porcelain", "--", chemin_relatif],
                                 cwd=ROOT, capture_output=True, text=True, timeout=10)
        if modifie.returncode == 0 and modifie.stdout.strip():
            return datetime.date.today().isoformat()
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", chemin_relatif],
                           cwd=ROOT, capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return datetime.date.today().isoformat()


def patch_sitemap(cases, lastmod=None):
    """Reecrit sitemap.xml. lastmod est calcule par page, pas fige."""
    urls = [(BASE + "/", "1.0", "index.html"),
            (BASE + "/projets/", "0.9", "projets/index.html"),
            (BASE + "/parcours/", "0.8", "parcours/index.html"),
            (BASE + "/contact/", "0.7", "contact/index.html")]
    urls += [(f"{BASE}/projets/{c['slug']}/", "0.7", f"projets/{c['slug']}/index.html")
             for c in cases]
    body = "\n".join(
        f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{_date_modif(f)}</lastmod>\n'
        f'    <changefreq>monthly</changefreq>\n    <priority>{pr}</priority>\n  </url>'
        for u, pr, f in urls)
    p = os.path.join(ROOT, "sitemap.xml")
    open(p, "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")
    return p, len(urls)


def error_page():
    """Page 404. Chemins ABSOLUS : le serveur la sert a l'URL demandee, donc
    des liens relatifs se resoudraient depuis /un/chemin/inconnu/."""
    up = "/"
    out = [head("Page introuvable — Adem Nasri",
                "Cette page n'existe pas ou plus. Retour à l'accueil, aux projets ou au contact.",
                BASE + "/404.html", up, f"{BASE}/assets/og-image.webp")]
    out[0] = out[0].replace('<meta name="robots" content="index, follow"/>',
                            '<meta name="robots" content="noindex, follow"/>')
    out.append(nav(None, up))
    out.append("\n<main id=\"main\">\n")
    out.append(f"""<section class="section" style="padding-top:64px">
  <div class="shell">
    {label("✱", "Erreur 404")}
    <div class="about-grid" style="margin-top:26px">
      <div>
        <h1 class="hand-xxl" data-reveal data-reveal-delay="1">Page<br/><span style="color:var(--accent)">introuvable</span>.</h1>
        {souligne(230)}
      </div>
      <div>
        <p class="body-lg" data-reveal data-reveal-delay="1" style="margin-bottom:22px">
          Cette adresse ne mène à rien. Soit la page a changé de nom, soit le lien
          qui t'a amené ici était déjà cassé. Dans les deux cas, ce n'est pas ta faute.
        </p>
        <p class="body-lg" data-reveal data-reveal-delay="2" style="margin-bottom:28px">
          Voilà par où reprendre :
        </p>
        <ul class="case-list" data-reveal data-reveal-delay="3">
          <li><a href="/">L'accueil</a> — qui je suis et ce que je fais</li>
          <li><a href="/projets/">Les projets</a> — six sites livrés, avec leur étude de cas</li>
          <li><a href="/parcours/">Le parcours</a> — d'où je viens</li>
          <li><a href="/contact/">Le contact</a> — pour me dire ce que tu cherchais</li>
        </ul>
      </div>
    </div>
  </div>
</section>
""")
    out.append("\n</main>\n")
    out.append(footer(up))
    out.append(scripts(up))
    return "".join(out)
