# -*- coding: utf-8 -*-
"""Donnees des etudes de cas. Chaque chiffre publie ici a ete verifie a la
source par un agent, puis recontrole par un second agent adverse ; les 52
affirmations non reproductibles ont ete corrigees ou retirees."""
import os, struct

A = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "assets", "projets")


def _webp_size(chemin):
    """Largeur et hauteur d'un WebP, lues dans l'en-tete du fichier.
    Pur Python : pas de dependance a sips (macOS) ni a une bibliotheque."""
    d = open(chemin, "rb").read(40)
    if d[0:4] != b"RIFF" or d[8:12] != b"WEBP":
        raise SystemExit(f"ABANDON : {chemin} n'est pas un WebP")
    tag = d[12:16]
    if tag == b"VP8X":                                   # etendu
        w = int.from_bytes(d[24:27], "little") + 1
        h = int.from_bytes(d[27:30], "little") + 1
    elif tag == b"VP8 ":                                 # avec perte
        if d[23:26] != b"\x9d\x01\x2a":
            raise SystemExit(f"ABANDON : en-tete VP8 illisible dans {chemin}")
        w = struct.unpack("<H", d[26:28])[0] & 0x3FFF
        h = struct.unpack("<H", d[28:30])[0] & 0x3FFF
    elif tag == b"VP8L":                                 # sans perte
        b = struct.unpack("<I", d[21:25])[0]
        w = (b & 0x3FFF) + 1
        h = ((b >> 14) & 0x3FFF) + 1
    else:
        raise SystemExit(f"ABANDON : type WebP inconnu ({tag!r}) dans {chemin}")
    return w, h


def dim(name):
    """(fichier, largeur, hauteur) lues sur le fichier reel — jamais recopiees."""
    chemin = os.path.join(A, name)
    if not os.path.exists(chemin):
        raise SystemExit(f"ABANDON : visuel introuvable — {chemin}")
    w, h = _webp_size(chemin)
    return (name, w, h)

LASTMOD = "2026-09-09"   # date des <lastmod> du sitemap

CASES = [
{
 "slug": "kines-paris-maison-du-peps",
 "resume_carte": "Deux sites et le référencement continu d'un réseau de cinq cabinets de kiné et deux salles de sport-santé à Paris.", "num": "01",
 "nom": "Kinés Paris & Maison du Peps",
 "client": "Jean-Charles Laporte — 5 cabinets de kiné, 2 salles de sport-santé",
 "client_court": "Kinés Paris",
 "annee": "2026 → aujourd'hui",
 "role": "Deux sites + SEO/GEO en continu",
 "lien": "https://www.kinesparis.fr/", "lien_label": "kinesparis.fr",
 "stack": ["HTML statique", "CSS à design tokens", "JS vanilla", "SEO/GEO", "Schema.org", "Doctolib"],
 "accroche": "Sept établissements, deux marques, cent pages : rendre chaque adresse trouvable sans diluer le nom.",
 "title": "Kinés Paris & Maison du Peps — étude de cas | Adem Nasri",
 "desc": "Deux sites et une stratégie SEO/GEO pour un réseau de 5 cabinets de kinésithérapie et 2 salles de sport-santé : 100 pages, 46 articles, plus de 4 000 visites mensuelles six mois après la mise en ligne.",
 "resume_liste": "Jean-Charles dirige cinq cabinets de kiné et deux salles de sport-santé à Paris et dans le Val-de-Marne, avec 51 praticiens. Chaque adresse vivait sur sa fiche Google et son agenda Doctolib, sans rien pour capter les recherches locales ni les recherches par pathologie. J'ai construit les deux sites et je suis leur référencement chaque mois.",
 "resume_home": "Deux sites pour un réseau de cinq cabinets de kiné et deux salles de sport-santé, plus le SEO/GEO suivi mois après mois. Cent pages, 46 articles, une version anglaise complète.",
 "probleme": "Jean-Charles Laporte dirige cinq cabinets de kinésithérapie et deux salles de sport-santé à Paris et dans le Val-de-Marne, avec 51 praticiens répartis entre les établissements. Chaque adresse vivait sur sa propre fiche Google et son propre agenda Doctolib, sans site capable de capter les recherches locales ni les recherches par pathologie — « balnéothérapie Le Perreux », « rééducation périnéale Paris », « salle de sport senior ». Il fallait aussi séparer nettement les deux marques, le soin remboursé d'un côté et le sport-santé de l'autre, tout en les faisant se renvoyer des patients.",
 "citation": "La kiné qui s'adapte à vous, pas l'inverse.",
 "fait": [
   "Construit deux sites HTML statiques distincts : kinesparis.fr (62 pages au sitemap) et maisondupeps.com (38 pages), sans CMS ni framework.",
   "Créé une page par établissement — sept au total — avec adresse, horaires, coordonnées GPS et lien vers le bon agenda Doctolib, plus cinq pages équipe par cabinet.",
   "Écrit et publié 46 articles de blog, organisés par pathologie côté kiné et par public côté salle de sport.",
   "Balisé 51 fiches praticiens en Person avec spécialité et diplômes, et le réseau entier en LocalBusiness, MedicalBusiness, Physiotherapy et GymOrFitnessCenter.",
   "Mis en place des avis Google pré-rendus au build par un script Python, puis rafraîchis en JavaScript : ils restent lisibles par les moteurs même sans exécution du JS.",
   "Livré une version anglaise complète (14 pages sur kinesparis.fr, 6 sur maisondupeps.com), avec hreflang fr/en/x-default sur les 99 pages.",
   "Ouvert le site aux moteurs génératifs : llms.txt et llms-full.txt sur les deux domaines, et 16 crawlers IA autorisés nommément dans robots.txt.",
   "Interconnecté les deux marques : 326 renvois des cabinets vers les salles, 379 dans l'autre sens.",
 ],
 "fonctionnalites": ["Prise de rendez-vous Doctolib sur 64 pages", "Sélecteur de langue FR/EN sur 97 pages",
   "Avis Google pré-rendus au build", "FAQ balisée sur 75 pages", "Deux pages FAQ autonomes de 36 questions",
   "Page mutuelles et tiers payant", "Programme musculation 12 semaines en PDF", "Images WebP responsives en srcset"],
 "preuves_intro": "Tous ces chiffres ont été relevés sur les sites en ligne : sitemaps recomptés, JSON-LD extrait page par page, balises vérifiées une à une.",
 "preuves": [
   {"n": "100", "l": "pages publiées, sitemaps des deux sites cumulés"},
   {"n": "4 000+", "l": "visites mensuelles six mois après la mise en ligne"},
   {"n": "46", "l": "articles de blog écrits et publiés"},
   {"n": "524", "l": "questions balisées en FAQPage, sur 75 pages"},
   {"n": "51", "l": "fiches praticiens balisées en Person"},
   {"n": "7", "l": "établissements, chacun sur sa propre page"},
   {"n": "100 %", "l": "des 1 113 images avec un attribut alt renseigné"},
   {"n": "FR + EN", "l": "hreflang complet sur les 99 pages"},
 ],
 "design": {
   "signature": "Un fond anthracite très sombre traversé par un seul orange brique, réservé aux titres forts, aux boutons et aux chiffres clés : aucune autre couleur d'accent, donc aucun appel à l'action qui se noie. Les deux marques partagent exactement la même feuille de style — le style.min.css de kinesparis.fr et celui de maisondupeps.com ont le même MD5, au bit près. Un seul système de design piloté par variables CSS, deux identités.",
   "couleurs": ["#D13D21", "#1C1D26", "#24252F", "#2D8A4E", "#FFFFFF"],
   "typo": "Source Sans Pro",
 },
 "story": "Jean-Charles gère cinq cabinets de kiné et deux salles de sport, 51 praticiens, sept établissements. Le vrai sujet n'était pas de faire un joli site : c'était de rendre chaque adresse trouvable sur sa propre requête, sans diluer la marque. J'ai donc construit deux sites séparés qui partagent une seule feuille de style — le même fichier, au bit près — et je les ai fait se renvoyer des patients : les cabinets envoient vers les salles, les salles renvoient vers les kinés. Ensuite j'ai écrit : 46 articles, plus de 150 000 mots, 524 questions balisées en FAQ. Le SEO et le GEO, je continue de les suivre chaque mois. Côté analytics du client, les deux sites cumulent plus de 4 000 visites mensuelles six mois après la mise en ligne.",
 "visuel_legende": "kinesparis.fr — le site des cinq cabinets. La capture défile toute seule.",
 "page2_label": "maisondupeps.com", "page2_legende": "L'autre marque du même client : Maison du Peps, les deux salles de sport-santé.",
 "visuels": {"card": dim("kinesparis-card.webp"), "scroll": dim("kinesparis-scroll.webp"),
             "page2": dim("maisondupeps-scroll.webp"), "mobile": dim("kinesparis-mobile.webp"),
             "hero": dim("kinesparis-hero.webp")},
},
{
 "slug": "chalery",
 "resume_carte": "Un site dessiné comme un plan technique, avec un simulateur qui trace le logement du client en direct.", "num": "02", "nom": "Chalery",
 "client": "Chalery — installateur de climatisation réversible",
 "client_court": "Chalery", "annee": "2026",
 "role": "Site vitrine + simulateur de prix",
 "lien": "https://www.chalery.fr/", "lien_label": "chalery.fr",
 "stack": ["HTML statique", "CSS natif", "JS vanilla", "SVG paramétrique", "Schema.org"],
 "accroche": "Un site dessiné comme un plan technique, avec un simulateur qui trace le logement du client en direct.",
 "title": "Chalery — étude de cas | Adem Nasri",
 "desc": "Site vitrine d'un installateur de climatisation réversible, dessiné dans un univers de plan technique, avec un simulateur de prix en 7 écrans qui redessine le logement en SVG à chaque réponse.",
 "resume_liste": "Le vrai frein commercial du métier, c'est le prix : personne ne sait ce que coûte une installation, et il faut appeler pour le savoir — ce qui filtre la moitié des prospects. Le site devait donner le chiffre avant la prise de contact, sans ressembler aux sites d'artisans que le secteur produit en série.",
 "resume_home": "Site vitrine dessiné comme un plan technique, avec un simulateur en 7 écrans qui redessine une coupe du logement en SVG à chaque réponse et sort un prix avant tout appel.",
 "probleme": "Chalery installe, entretient et met en service de la climatisation réversible chez des particuliers. Le vrai frein commercial du métier, c'est le prix : personne ne sait ce que coûte une installation, et il faut appeler pour le savoir — ce qui filtre la moitié des prospects avant même le premier contact. Le site devait donc répondre au chiffre avant la prise de contact, et le faire sans ressembler aux sites d'artisans que le secteur produit en série.",
 "citation": "Votre climatisation, au juste prix.",
 "fait": [
   "Construit 13 pages en HTML statique, sans framework ni étape de build, avec des URLs sans extension gérées par .htaccess.",
   "Décliné un système graphique de plan technique sur tout le site : j'ai compté 43 cadres au filet d'un pixel et 152 marques de repère en équerre sur les 10 pages principales.",
   "Développé un simulateur de prix en 7 écrans, dont un moteur de chiffrage qui estime la puissance par période de construction — de 130 W/m² avant 1975 à 80 W/m² après 2012.",
   "Dessiné un plan de coupe SVG qui se redessine à chaque réponse : le bâti s'élargit avec la surface, les cloisons se posent, les unités intérieures apparaissent pièce par pièce.",
   "Ajouté l'impression de l'estimation via une feuille de style dédiée, avec référence de devis générée, et le partage par URL — les réponses sont encodées en paramètres.",
   "Auto-hébergé les polices Barlow en woff2, découpées par unicode-range en 15 fichiers, les deux sous-ensembles latins étant préchargés dans le head.",
   "Écrit un bandeau de consentement où refuser est aussi grand et aussi accessible qu'accepter : même cible de 44 px, un seul niveau, aucun clic supplémentaire.",
 ],
 "fonctionnalites": ["Simulateur de prix en 7 écrans", "Plan de coupe SVG génératif", "Impression de l'estimation",
   "Partage de l'estimation par URL", "Accueil en défilement plein écran", "Vidéo hero adaptative",
   "Guides longs à sommaire ancré", "Consentement CNIL à deux boutons égaux"],
 "preuves_intro": "Relevés directement dans le code servi par le site, page par page.",
 "preuves": [
   {"n": "13", "l": "pages livrées, sans CMS ni framework"},
   {"n": "43", "l": "cadres blueprint et 152 marques d'angle"},
   {"n": "7", "l": "écrans dans le simulateur de prix"},
   {"n": "16", "l": "types schema.org distincts"},
   {"n": "6,8 Ko", "l": "de JavaScript partagé pour tout le site"},
   {"n": "0", "l": "requête déposée avant le consentement"},
 ],
 "design": {
   "signature": "Le site entier est dessiné comme un plan technique : encadrements au filet d'un pixel, marques de repère en équerre posées six pixels hors de la boîte aux quatre coins, cartouches en capitales espacées, croix de repérage sur la frise des étapes, et jusqu'à la mention « Éch. 1:100 » et un code de planche « CHY-01 » au-dessus du plan du simulateur. Ce n'est pas une décoration posée sur une page d'accueil : c'est le motif qui tient les treize pages.",
   "couleurs": ["#1d2d3d", "#5980a6", "#728fab", "#eef6ff", "#f2f2f3"],
   "typo": "Barlow Condensed 600 en capitales pour les titres, Barlow 400 pour le texte",
 },
 "story": "Au premier rendez-vous, il y avait un blueprint posé sur la table. J'ai gardé ça. Tout le site est dessiné à la règle : cadres au trait d'un pixel, marques de repère aux quatre coins, cartouche « Éch. 1:100 ». Le simulateur va au bout de l'idée — pendant que le client répond aux questions, une coupe de son logement se dessine en SVG : la maison s'élargit avec la surface, les cloisons se posent, les unités apparaissent pièce par pièce. Pas de framework, pas d'étape de build : du HTML, du CSS, et un fichier JS de 6,8 Ko.",
 "visuel_legende": "chalery.fr — l'univers du plan technique, du hero jusqu'au pied de page.",
 "page2_label": "chalery.fr/produits", "page2_legende": "La page produits : marques et formats d'unités.",
 "visuels": {"card": dim("chalery-card.webp"), "scroll": dim("chalery-scroll.webp"),
             "page2": dim("chalery-page2.webp"), "mobile": dim("chalery-mobile.webp"),
             "hero": dim("chalery-hero.webp")},
},
{
 "slug": "amb-energies",
 "resume_carte": "Le site d'un installateur solaire écrit à contre-courant du démarchage — et son référencement.", "num": "03", "nom": "AMB Énergies",
 "client": "AMB Énergies — installateur RGE, solaire et pompes à chaleur",
 "client_court": "AMB Énergies", "annee": "2026",
 "role": "Site + SEO/GEO",
 "lien": "https://ambenergies.com/", "lien_label": "ambenergies.com",
 "stack": ["HTML statique", "CSS en variables", "JS vanilla", "PHP", "SEO/GEO", "Schema.org"],
 "accroche": "Un site d'installateur solaire construit contre le démarchage : dire les mauvaises nouvelles avant que le concurrent les cache.",
 "title": "AMB Énergies — étude de cas | Adem Nasri",
 "desc": "Site et référencement d'un installateur RGE en solaire et pompes à chaleur : 101 pages, 65 guides, 12 pages villes, et un parti pris éditorial à contre-courant du démarchage.",
 "resume_liste": "Le problème d'AMB n'est pas la technique, c'est le secteur : le client type a déjà reçu trois appels lui promettant une prime qui n'existe plus, et il arrive méfiant. Le site devait faire l'inverse d'une plaquette commerciale et prouver, avant le premier rendez-vous, que l'entreprise ne vend pas au téléphone.",
 "resume_home": "Site et SEO/GEO d'un installateur RGE, écrit à contre-courant du démarchage : pas de grille de prix, une prime supprimée annoncée en page d'accueil, 65 guides.",
 "probleme": "AMB Énergies pose des panneaux solaires et des pompes à chaleur depuis 2016 au départ de Nîmes, avec ses propres équipes et trois qualifications RGE. Son problème n'est pas la technique, c'est le secteur : le client type a déjà reçu trois appels lui promettant une prime qui n'existe plus, et il arrive méfiant. Le site devait donc faire l'inverse d'une plaquette commerciale et prouver, avant le premier rendez-vous, que l'entreprise ne vend pas au téléphone.",
 "citation": "Nous vous disons ce à quoi vous avez droit avant la signature, pas après.",
 "fait": [
   "Construit 101 pages statiques en HTML multi-pages, sans framework, une page par URL.",
   "Écrit 65 guides et 12 pages villes pour couvrir les recherches réelles du secteur, plus 12 pages service.",
   "Assumé un parti pris éditorial rare dans le métier : pas de grille de prix, pas de durée d'amortissement type, et une page d'accueil qui annonce elle-même la suppression d'une prime.",
   "Corrigé le simulateur à la baisse — il affichait 35 % d'économies là où il en promettait 45, ce que le reste du site démentait.",
   "Développé un configurateur « Composez votre maison » : on coche des équipements, on règle sa facture au curseur, un schéma SVG et l'estimation se recalculent.",
   "Livré un formulaire de devis en deux étapes avec envoi réel en PHP et numéro de référence affiché, suivi d'un questionnaire complémentaire de 5 questions facultatives.",
   "Balisé 98 pages en FAQPage — seules les mentions légales, la politique cookies et le plan du site en sont exemptes.",
   "Maillé le site à 8 650 liens internes : aucune page orpheline sur les 101.",
 ],
 "fonctionnalites": ["Configurateur « Composez votre maison »", "Devis en 2 étapes avec envoi PHP",
   "Questionnaire complémentaire en 5 questions", "Accordéon FAQ sur 97 pages",
   "Galerie de chantiers à 4 filtres", "Consentement CNIL révocable", "Contact téléphone et WhatsApp"],
 "preuves_intro": "Sitemap recompté, liens internes extraits page par page, JSON-LD analysé sur les 101 pages.",
 "preuves": [
   {"n": "101", "l": "pages publiées et déclarées au sitemap"},
   {"n": "65", "l": "guides rédigés"},
   {"n": "12", "l": "pages villes pour le SEO local"},
   {"n": "98", "l": "pages balisées en FAQPage"},
   {"n": "8 650", "l": "liens internes, aucune page orpheline"},
   {"n": "0", "l": "bibliothèque tierce dans le JavaScript"},
 ],
 "design": {
   "signature": "Un fond gris chaud presque papier plutôt que le blanc clinique habituel du secteur, traversé par un seul rouge-orange saturé réservé aux actions et aux chiffres clés. Tout le reste est en gris neutres : le prix, l'aide ou le bouton de devis sont les seuls points de couleur de l'écran. La police Archivo est auto-hébergée en variable, sous-ensemble aux 114 caractères réellement présents sur le site — 19 556 octets pour l'ensemble.",
   "couleurs": ["#ec3013", "#201e1d", "#4d170e", "#eae9e9", "#f3f2f2"],
   "typo": "Archivo variable auto-hébergée",
 },
 "story": "Le photovoltaïque est un secteur abîmé par le démarchage. Le client d'AMB a déjà reçu trois appels lui promettant une prime supprimée. J'ai donc construit le site à l'envers d'une plaquette : pas de grille de prix, pas de durée d'amortissement type, et une page d'accueil qui annonce elle-même la suppression de la prime. J'ai même corrigé le simulateur à la baisse — il affichait 35 % d'économies là où il en promettait 45, ce que le reste du site démentait. Le référencement vient de là : 65 guides, 12 pages villes, et des questions auxquelles on répond pour de vrai.",
 "visuel_legende": "ambenergies.com — la page d'accueil, du hero jusqu'aux réalisations.",
 "page2_label": "ambenergies.com/services", "page2_legende": "La page services : les douze prestations, du photovoltaïque à l'eau chaude.",
 "visuels": {"card": dim("ambenergies-card.webp"), "scroll": dim("ambenergies-scroll.webp"),
             "page2": dim("ambenergies-page2.webp"), "mobile": dim("ambenergies-mobile.webp"),
             "hero": dim("ambenergies-hero.webp")},
},
{
 "slug": "relapro",
 "resume_carte": "Le DPE raconté comme une trajectoire : une échelle qui grimpe de G vers A au fil du défilement.", "num": "04", "nom": "Relapro",
 "client": "RELAPRO — bureau d'études thermiques, DPE et audit énergétique",
 "client_court": "RELAPRO", "annee": "2026",
 "role": "Site + SEO local",
 "lien": "https://relapro.fr/", "lien_label": "relapro.fr",
 "stack": ["HTML statique", "CSS en variables", "JS vanilla", "PHP", "SEO local", "Schema.org"],
 "accroche": "Le DPE raconté comme une trajectoire : une échelle de G vers A qui grimpe au fil du défilement.",
 "title": "Relapro — étude de cas | Adem Nasri",
 "desc": "Site et SEO local d'un bureau d'études thermiques de Nîmes : une échelle DPE qui grimpe de G vers A au défilement, un simulateur en 9 étapes, cinq villes couvertes.",
 "resume_liste": "Le métier de RELAPRO — DPE, audit énergétique, dossiers MaPrimeRénov' — s'adresse à des propriétaires qui arrivent contraints. Le sujet est réglementaire, anxiogène et illisible, et un bureau d'études local se retrouve à concurrencer des plateformes nationales sur « DPE Nîmes ».",
 "resume_home": "Site et SEO local d'un bureau d'études thermiques : une échelle DPE qui grimpe de G vers A au fil du défilement, un simulateur en 9 étapes, cinq villes couvertes.",
 "probleme": "RELAPRO est un bureau d'études thermiques certifié RGE installé à Nîmes, qui intervient dans un rayon de 50 km. Son métier — DPE, audit énergétique, dossiers MaPrimeRénov' et CEE — s'adresse à des propriétaires qui arrivent contraints : depuis le 1er janvier 2025, un logement classé G ne se loue plus, et vendre un bien E, F ou G impose un audit réglementaire. Le sujet est réglementaire, anxiogène et illisible, et un bureau d'études local se retrouve à concurrencer des plateformes nationales sur « DPE Nîmes ».",
 "citation": "Maison de village, mas, appartement ou copropriété — chaque bâti a ses points faibles thermiques. Le nôtre est de les trouver.",
 "fait": [
   "Construit 20 pages statiques en HTML/CSS/JS sans framework : 19 déclarées au sitemap, plus les mentions légales et une page 404 dédiée.",
   "Fait de la promesse une interface : une échelle DPE reste collée au bord de l'écran et grimpe de G vers A à mesure qu'on descend la page.",
   "Développé un simulateur en 9 étapes et 10 écrans qui estime la classe énergétique, sort les travaux prioritaires et qualifie le prospect.",
   "Intégré le barème MaPrimeRénov' 2026 : seuils de revenu fiscal de référence hors Île-de-France, de 1 à 5 personnes, extrapolés au-delà.",
   "Couvert cinq villes en SEO local — Nîmes, Montpellier, Alès, Avignon, Arles — plus une page zone d'intervention.",
   "Gardé la grille tarifaire côté serveur dans un _tarifs.php jamais exposé au navigateur, et envoyé les demandes en POST vers /envoi.php avec champ piège anti-spam.",
   "Repris le design system Modernist et posé par-dessus une surcouche maison qui redéfinit l'accent : une rampe verte de 100 à 900 dérivée du vert du logo.",
   "Balisé le site en 22 types schema.org, dont ProfessionalService sur 11 pages avec adresse, coordonnées géographiques et téléphone.",
 ],
 "fonctionnalites": ["Échelle DPE fixe qui grimpe au défilement", "Simulateur DPE en 9 étapes",
   "Barème MaPrimeRénov' 2026 intégré", "Mini-qualification en 2 questions dans le hero",
   "FAQ dépliantes sur 16 pages", "Écran de transition avec préchargement", "Vidéo de fond adaptative"],
 "preuves_intro": "Sitemap recompté, JSON-LD extrait, code du simulateur lu ligne à ligne.",
 "preuves": [
   {"n": "20", "l": "pages livrées, dont 19 au sitemap"},
   {"n": "9", "l": "étapes dans le simulateur DPE"},
   {"n": "5", "l": "villes couvertes en SEO local"},
   {"n": "22", "l": "types schema.org distincts"},
   {"n": "11", "l": "pages balisées ProfessionalService"},
   {"n": "~20 100", "l": "mots rédigés sur l'ensemble du site"},
 ],
 "design": {
   "signature": "Une échelle DPE fixée au bord de l'écran : sept cases de G à A qui se remplissent au fil du défilement, la case active passant en vert plein. Le message « on vous emmène de G vers A » est joué par l'interface elle-même, pas seulement écrit. Autour, une mise en page très typographique sur fond gris chaud, sans ombre ni carte arrondie, ponctuée d'un écran de transition entre les pages où le logo se retrace en 800 ms.",
   "couleurs": ["#0e8a14", "#043007", "#e4f3e4", "#201e1d", "#f3f2f2"],
   "typo": "Archivo, une seule famille pour les titres et le texte",
 },
 "story": "RELAPRO fait des DPE. Le problème n'est pas le diagnostic, c'est ce qu'il déclenche : un propriétaire qui apprend qu'il est classé G ne sait ni quoi faire, ni dans quel ordre, ni qui paie. J'ai donc construit le site autour d'une trajectoire plutôt qu'autour d'un catalogue. Une échelle DPE reste collée au bord de l'écran et grimpe de G vers A à mesure qu'on descend la page : la promesse rendue littérale. Derrière, un simulateur en 9 questions estime la classe, sort les travaux prioritaires et qualifie le prospect. Et vingt pages couvrent les recherches réelles : cinq villes, cinq guides, la réforme 2026.",
 "visuel_legende": "relapro.fr — l'accueil, avec l'échelle DPE qui accompagne le défilement.",
 "page2_label": "relapro.fr/simulateur", "page2_legende": "Le simulateur : neuf questions pour estimer la classe et les aides.",
 "visuels": {"card": dim("relapro-card.webp"), "scroll": dim("relapro-scroll.webp"),
             "page2": dim("relapro-page2.webp"), "mobile": dim("relapro-mobile.webp"),
             "hero": dim("relapro-hero.webp")},
},
{
 "slug": "malamour",
 "resume_carte": "Deux vins des Abruzzes, une marque entière à faire tenir sur deux références. Site, design et catalogue Shopify.", "num": "05", "nom": "Malamour",
 "client": "Malamour — deux fondatrices italiennes, vins des Abruzzes",
 "client_court": "Malamour", "annee": "2025",
 "role": "Création du site, du design et du catalogue Shopify",
 "lien": "https://malamourrrrrr.com/", "lien_label": "malamourrrrrr.com",
 "stack": ["Shopify", "Liquid", "JS vanilla", "Design", "SEO"],
 "accroche": "Deux femmes venues de la mode, deux vins des Abruzzes : faire tenir une marque entière sur deux références.",
 "title": "Malamour — étude de cas | Adem Nasri",
 "desc": "Création du site, du design et du catalogue Shopify d'une marque de vins italiens : huit sections Liquid écrites sur mesure pour faire tenir une marque entière sur deux références.",
 "resume_liste": "Deux fondatrices italiennes venues du monde de la mode lancent deux vins des Abruzzes. Elles ne voulaient pas d'un site de caviste : elles voulaient quelque chose de beau et d'élégant. Le problème n'était pas de faire une boutique, mais de faire tenir une marque entière sur deux produits.",
 "resume_home": "Création du site, du design et du catalogue Shopify pour deux fondatrices italiennes venues de la mode. Huit sections Liquid écrites sur mesure pour deux références.",
 "probleme": "Malamour, ce sont deux fondatrices italiennes venues du monde de la mode, qui lancent deux vins des Abruzzes : un Montepulciano rouge et un Trebbiano blanc. Ni catalogue, ni notoriété, ni distribution — juste deux références à vendre en direct dans toute l'Europe. Elles voulaient plus qu'un site : quelque chose de beau visuellement et d'élégant. Le problème n'était donc pas de faire une boutique, mais de faire tenir une marque entière sur deux produits, avec un niveau visuel qui tienne face à des sites de vin qui ressemblent tous à des catalogues.",
 "citation": "Born at the table, shared with friends, Malamour is made for generous plates and unhurried nights.",
 "fait": [
   "Pris Shopify comme moteur et tout redessiné par-dessus : le thème est entièrement retravaillé, pas configuré.",
   "Écrit huit sections Liquid spécifiques à la marque : hero vidéo, mise en avant produit, carrousel d'événements, notre histoire, Places & Faces, contact, popup newsletter, pied de page.",
   "Ouvert le site sur un preloader animé puis une vidéo 1080p plein écran en lecture automatique muette, sans texte marketing par-dessus.",
   "Refait la page produit avec un sélecteur de packs 1 / 3 / 6 bouteilles, badge « Best » sur le pack de six et pack de trois présélectionné.",
   "Structuré le catalogue Shopify et mis en place les catégories de produits.",
   "Construit la galerie Places & Faces : 44 photos en colonnes, avec une lightbox codée à la main et navigation précédent / suivant.",
   "Codé à la main la popup de bienvenue : temporisation, validation de l'email, envoi AJAX, révélation animée du code promo et bouton copier-coller.",
   "Ajouté un estimateur de livraison sur les 27 pays de l'Union européenne dans le tiroir panier.",
   "Rédigé les titles et méta-descriptions et écrit un article de fond, pour que Google trouve deux bouteilles au milieu de l'Italie entière.",
 ],
 "fonctionnalites": ["Preloader de marque animé", "Hero vidéo plein écran", "Sélecteur de pack 1/3/6",
   "Tiroir panier avec estimateur de livraison UE", "Popup newsletter codée à la main",
   "Galerie Places & Faces de 44 photos", "Carrousel d'événements en boucle", "Badge réglementaire en pied de page"],
 "preuves_intro": "Relevés dans le HTML servi par la boutique et dans ses sous-sitemaps Shopify.",
 "preuves": [
   {"n": "2", "l": "références à faire vivre comme une marque entière"},
   {"n": "8", "l": "sections Liquid écrites pour la marque"},
   {"n": "44", "l": "photos dans la galerie Places & Faces"},
   {"n": "27", "l": "pays de l'UE dans l'estimateur de livraison"},
   {"n": "1 / 3 / 6", "l": "packs proposés sur la page produit"},
   {"n": "0", "l": "tracker marketing tiers"},
 ],
 "design": {
   "signature": "Un bordeaux profond posé comme unique accent sur une base noir et blanc cassé : il ne sert qu'au panier, aux survols du menu, au liseré du pied de page et au bouton de la popup — jamais en aplat. Le site s'ouvre sur un preloader avec un GIF animé et la mention « Drink it. », puis sur une vidéo plein écran en lecture automatique muette, sans texte marketing par-dessus. C'est la retenue qui fait l'élégance ici, pas l'accumulation.",
   "couleurs": ["#7A001F", "#111111", "#0A0A0A", "#FFFBF7", "#FFFFFF"],
   "typo": "Montserrat en titres et en textes, DM Sans auto-hébergée",
 },
 "story": "Elles arrivent de la mode, elles lancent deux vins des Abruzzes, et la première phrase qu'elles m'ont dite, c'est qu'elles ne voulaient pas d'un site de caviste. J'ai donc pris Shopify comme moteur et j'ai tout redessiné par-dessus : preloader animé, vidéo plein écran à l'ouverture, un seul bordeaux comme accent, et huit sections Liquid écrites spécialement pour elles. Le vrai travail a été de faire tenir une marque sur deux références. J'ai refait la page produit avec un sélecteur de packs 1/3/6, structuré le catalogue Shopify, codé la popup de bienvenue à la main, et rédigé les titles et les descriptions pour que Google trouve deux bouteilles au milieu de l'Italie entière.",
 "visuel_legende": "malamourrrrrr.com — l'accueil, du hero vidéo jusqu'à l'histoire de la marque.",
 "page2_label": "malamourrrrrr.com/collections", "page2_legende": "Le catalogue : les deux références, structurées dans Shopify.",
 "visuels": {"card": dim("malamour-card.webp"), "scroll": dim("malamour-scroll.webp"),
             "page2": dim("malamour-page2.webp"), "mobile": dim("malamour-mobile.webp"),
             "hero": dim("malamour-hero.webp")},
},
{
 "slug": "la-maison-du-test",
 "resume_carte": "Le CRM maison des études consommateurs : collecte automatisée, nettoyage des données, analyse assistée par LLM.", "num": "06", "nom": "La Maison du Test",
 "client": "La Maison du Test — études consommateurs",
 "client_court": "La Maison du Test", "annee": "Déc. 2025 → aujourd'hui",
 "role": "Développeur — outil interne",
 "lien": None, "lien_note": "Outil interne, non public",
 "lien_label": "outil interne",
 "stack": ["PHP / Laravel", "Python", "JavaScript", "LLM (Claude / GPT)", "Pipelines de données"],
 "accroche": "Le CRM maison qui sert à monter et piloter les études consommateurs, de la collecte aux insights.",
 "title": "La Maison du Test — étude de cas | Adem Nasri",
 "desc": "Outil interne de création et de gestion d'études consommateurs : PHP/Laravel côté back, JavaScript côté front, automatisation de la collecte et intégration de LLM dans le workflow d'analyse.",
 "resume_liste": "Un CRM maison pour créer et piloter des études consommateurs. J'automatise la collecte et le nettoyage des données brutes, et j'intègre des LLM dans le workflow pour produire des insights plus vite. C'est mon poste actuel, et le seul projet de cette liste qui ne soit pas public.",
 "resume_home": "Le CRM maison qui sert à créer et piloter les études consommateurs : collecte automatisée, nettoyage des données brutes, LLM intégrés au workflow d'analyse.",
 "probleme": "Monter une étude consommateurs, la lancer, collecter les réponses, nettoyer les données brutes puis en tirer des enseignements : chaque étape se faisait dans un outil différent, et le temps passé à recoller les morceaux mangeait le temps d'analyse. L'enjeu était de tenir toute la chaîne dans un seul outil interne, et d'automatiser tout ce qui n'a pas besoin d'un cerveau humain.",
 "citation": None,
 "fait": [
   "Développé l'outil de création et de gestion des études consommateurs, en PHP/Laravel côté back et JavaScript côté front.",
   "Automatisé la collecte des réponses et le nettoyage des données brutes.",
   "Intégré des LLM dans le workflow d'analyse pour produire les premiers enseignements plus rapidement.",
   "Construit les pipelines de données qui relient la collecte, le nettoyage et la restitution.",
 ],
 "fonctionnalites": ["Création et gestion d'études", "Collecte automatisée", "Nettoyage des données brutes",
   "Analyse assistée par LLM", "Pipelines de données"],
 "preuves_intro": None, "preuves": None,
 "design": None,
 "story": "C'est mon poste actuel, et le seul projet de cette liste que personne ne peut aller voir en ligne : l'outil est interne. Il sert à monter les études consommateurs, à les lancer, à récupérer les réponses et à les nettoyer. La partie que je préfère, c'est ce qui se passe après la collecte : les données brutes arrivent en désordre, et les LLM branchés sur le pipeline permettent de sortir les premiers enseignements en une fraction du temps que ça prenait à la main.",
 "visuel_legende": None,
 "visuel_absent": "🔒 outil interne — pas de capture publiable",
 "page2_label": None, "page2_legende": None,
 "visuels": {},
},
]

INTRO = ('Six sites en ligne pour cinq clients — dont trois dont je tiens aussi le référencement — '
         'et l\'outil interne sur lequel je travaille. <span class="highlight">Chaque projet a son étude de cas</span> : '
         'ce qui a été construit, les chiffres relevés sur le site en ligne, et l\'histoire du client. '
         'Uniquement ce qui tourne ou ce qui a été livré.')
