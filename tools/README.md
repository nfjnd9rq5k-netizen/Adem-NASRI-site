# tools/ — le generateur des pages projet

Le site est statique et n'a pas de build au sens habituel. Deux exceptions,
regroupees ici : les pages projet sont generees a partir d'un gabarit unique,
et les CSS/JS sont empreintes pour contourner le cache du CDN.

## Regenerer les pages projet

```bash
python3 tools/generate.py
```

Ecrit `projets/index.html`, les six `projets/<slug>/index.html`, met a jour
`sitemap.xml`, puis rejoue `build.py`.

## Les fichiers

| Fichier | Role |
|---|---|
| `data.py` | Le contenu des six etudes de cas : textes, chiffres, palettes, visuels. **C'est ici qu'on modifie le fond.** |
| `gen.py` | Le gabarit HTML commun. On y touche pour changer la mise en page, pas le contenu. |
| `generate.py` | Le lanceur : gabarit + sitemap + empreintes. |
| `../build.py` | Empreinte les CSS/JS et reecrit les references. |

## Modifier une etude de cas

Tout est dans `data.py`, une entree par projet dans `CASES` :

- `nom`, `accroche`, `role`, `annee`, `client`
- `probleme`, `story`, `citation` — les textes longs
- `fait` — la liste numerotee de la section sombre
- `preuves` — les fiches chiffrees (`n` = le chiffre, `l` = le libelle)
- `design.couleurs` — la palette relevee chez le client
- `visuels` — les captures, via `dim("fichier.webp")` qui lit les dimensions
  reelles dans le fichier (jamais de valeur recopiee a la main)

Puis `python3 tools/generate.py`.

## Regle importante sur les chiffres

Chaque chiffre publie dans `preuves` a ete releve sur le site client en ligne
puis recontrole. Si un site client evolue, le chiffre doit etre reverifie avant
d'etre laisse en ligne : un chiffre faux sur un portfolio coute plus cher que
pas de chiffre.

## Apres toute modification de CSS, de JS, d'une capture ou du CV

```bash
python3 build.py
```

Il empreinte `styles.css`, les trois fichiers JS, les 25 captures de
`assets/projets/` et le PDF du CV, puis reecrit toutes les references dans le
HTML — et les deux redirections du CV dans `.htaccess`, entre les marqueurs
`>>> genere par build.py`. Ne pas editer ce bloc a la main.

Sans ca, les visiteurs continuent de recevoir l'ancienne version : le CDN de
Hostinger garde des variantes compressees perimees, et `.htaccess` demande un
cache d'un mois. L'empreinte dans le nom de fichier est ce qui rend le
deploiement fiable.
