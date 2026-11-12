#!/usr/bin/env python3
"""Animal Site static page generator (Python standard library only).

Reads src/content.json and writes every HTML page, assets/js/data.js,
sitemap.xml and robots.txt into the project root. The generated site is
plain HTML/CSS/JS: open index.html in a browser, no build step needed.
Run this script only when you edit content or page templates:

    python3 src/build.py
"""
import json
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://shaher06.github.io/Animal-Site/"
SITE = "Animal Base"
CONTACT_EMAIL = "animalbase111@gmail.com"
INSTAGRAM = "https://www.instagram.com/animal.base/?igsh=c2E0MnZxZGQ4dTBm#"
FACEBOOK = "https://www.facebook.com/groups/animalsworld.dk/?ref=share&mibextid=NSMWBT"
NATGEO = "https://www.nationalgeographic.com/animals"
FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;700;800"
         "&family=Figtree:wght@400;500;600;700&display=swap")

content = json.loads((ROOT / "src" / "content.json").read_text(encoding="utf-8"))
CATS = content["categories"]
ANIMALS = content["animals"]
CAT = {c["id"]: c for c in CATS}

QUIZ = [
    {"name": "shark", "emoji": "🦈", "fish": True, "why": "Sharks are fish. They breathe with gills, and their skeletons are made of cartilage instead of bone."},
    {"name": "dolphin", "emoji": "🐬", "fish": False, "why": "Dolphins are mammals. They breathe air through a blowhole and feed their babies milk."},
    {"name": "clownfish", "emoji": "🐠", "fish": True, "why": "Clownfish are bony fish that live among sea anemones on coral reefs."},
    {"name": "jellyfish", "emoji": "🪼", "fish": False, "why": "Despite the name, jellyfish have no bones, no gills and no brain. They are related to corals and sea anemones."},
    {"name": "whale", "emoji": "🐋", "fish": False, "why": "Whales are mammals. They surface to breathe air and nurse their calves."},
    {"name": "pufferfish", "emoji": "🐡", "fish": True, "why": "Pufferfish are fish with gills and fins. They swell up with water when threatened."},
    {"name": "octopus", "emoji": "🐙", "fish": False, "why": "An octopus is a mollusk, a soft-bodied relative of snails and clams."},
    {"name": "sea turtle", "emoji": "🐢", "fish": False, "why": "Sea turtles are reptiles. They have lungs and must come up to breathe air."},
    {"name": "tuna", "emoji": "🐟", "fish": True, "why": "Tuna are fast, powerful bony fish that swim across entire oceans."},
]

GALLERY = [
    ("hero/savanna-herd.webp", "Animals of the savanna gathered together in golden light", "Animals of the savanna"),
    ("hero/lion-sunset.webp", "A lion standing on a rock as the sun sets over the savanna", "A lion at sunset"),
    ("hero/lion-acacia.webp", "A lion walking in tall grass beneath an acacia tree", "A lion on the plains"),
    ("hero/jungle-scene.webp", "A jungle scene with an elephant, birds and a waterfall", "A busy jungle waterhole"),
    ("hero/playful-friends.webp", "Cartoon animal friends playing in a flower meadow", "Playful friends in the meadow"),
    ("hero/welcome-herd.webp", "Giraffes, elephants, zebras and lions standing together", "Giraffes, elephants, zebras and lions"),
]

TEAM = [
    ("Shaher Mamdouh Ahmed", "Team leader", "Contributed to the layout."),
    ("Malak Samir Tolba", "Team member", "Worked on the navigation."),
    ("Tarek Hany Mohamed", "Team member", "Helped with the styling."),
    ("Aalaa Tarek Ibrahim", "Team member", "Developed the animal pages."),
    ("Mazen Mohamed Ahmed", "Team member", "Assisted with the design."),
    ("Sabrin Walid Moustafa", "Team member", "Managed the images."),
    ("Hamdy Waleed Abdullah", "Team member", "Wrote the introduction text."),
    ("Seifeldin Tamer Kamal", "Team member", "Organized the content."),
]

ICONS = {
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M21 13A9 9 0 1 1 11 3a7 7 0 0 0 10 10z"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
}
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
          + "".join(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                    f'stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items())
          + "</svg>")


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def cat_vars(c):
    return f'--c:{c["color"]};--c-ink:{c["ink"]};--c-tint:{c["tint"]}'


# ---------------------------------------------------------------- layout
def header(current, overlay=False):
    def link(href, label):
        cur = ' aria-current="page"' if href == current else ""
        return f'<li><a class="nav-link" href="{href}"{cur}>{label}</a></li>'

    mega = "".join(
        f'<li><a href="{c["file"]}"{" aria-current=page" if c["file"] == current else ""}>'
        f'<span class="dot" style="--dot:{c["color"]}"></span>{c["name"]}</a></li>' for c in CATS)
    animals_open = ' aria-current="true"' if any(c["file"] == current for c in CATS) else ""
    cls = "site-header header--overlay" if overlay else "site-header"
    return f'''<header class="{cls}">
  <div class="container site-header__inner">
    <a class="brand" href="{'index.html' if current == 'index.html' else 'home.html'}"><img src="assets/img/brand/logo.webp" alt="" width="40" height="40"><span>{SITE}</span></a>
    <button class="icon-btn nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">{icon("menu")}</button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul class="site-nav__list">
        {link("home.html", "Home")}
        <li class="has-menu"><button class="nav-link" type="button" data-menu-button aria-expanded="false" aria-controls="animals-menu"{animals_open}>Animals {icon("chevron")}</button>
          <ul id="animals-menu" class="mega" hidden>{mega}</ul></li>
        {link("about.html", "About")}
        {link("contact.html", "Contact")}
      </ul>
      <div class="header-actions">
        <button class="icon-btn theme-toggle" type="button" aria-label="Switch between light and dark theme">{icon("sun", "icon-sun")}{icon("moon", "icon-moon")}</button>
        <a class="icon-btn" href="settings.html" aria-label="Settings"{' aria-current="page"' if current == "settings.html" else ""}>{icon("sliders")}</a>
        <a class="btn btn--small btn--sun" href="login.html">Log in</a>
      </div>
    </nav>
  </div>
</header>'''


def footer():
    cats = "".join(f'<li><a href="{c["file"]}">{c["name"]}</a></li>' for c in CATS)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a class="brand" href="home.html"><img src="assets/img/brand/logo.webp" alt="" width="40" height="40"><span>{SITE}</span></a>
        <p>A friendly guide to the animal kingdom, built as a first-year team project and rebuilt as a modern front-end site.</p>
      </div>
      <div><h2>Animals</h2><ul>{cats}</ul></div>
      <div><h2>The site</h2><ul>
        <li><a href="about.html">About us</a></li><li><a href="contact.html">Contact</a></li>
        <li><a href="settings.html">Settings</a></li><li><a href="login.html">Log in (demo)</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{NATGEO}" target="_blank" rel="noopener">National Geographic Animals</a></li>
      </ul></div>
    </div>
    <small>© 2025 {SITE}. Created by our team. Thank you for exploring the amazing world of animals.</small>
  </div>
</footer>'''


def dialogs():
    return f'''<dialog id="animal-dialog" class="dialog" aria-labelledby="dialog-title">
  <button class="icon-btn dialog__close" type="button" aria-label="Close details">{icon("close")}</button>
  <div class="dialog__media"></div>
  <div class="dialog__body">
    <p class="animal-card__tag" data-d-cat></p>
    <h2 id="dialog-title"></h2>
    <p class="sci" style="font-style:italic;color:var(--ink-soft)" data-d-sci></p>
    <p data-d-summary></p>
    <dl class="facts">
      <div><dt>Habitat</dt><dd data-d-habitat></dd></div>
      <div><dt>Diet</dt><dd data-d-diet></dd></div>
    </dl>
    <p class="fun-fact"><strong>Fun fact:</strong> <span data-d-fun></span></p>
    <p class="hint" style="font-size:var(--step--1);color:var(--ink-soft)" data-d-credit hidden></p>
    <a class="btn btn--ghost btn--small" data-d-wiki target="_blank" rel="noopener" href="#">Read more on Wikipedia (opens in a new tab)</a>
  </div>
</dialog>'''


def page(filename, title, description, body, *, scripts=(), style="", body_class="", overlay=False,
         og_image="assets/img/hero/savanna-herd.webp", dialog=False, lightbox=False):
    full_title = f"{title} | {SITE}" if filename != "index.html" else f"{SITE}: explore the animal kingdom"
    js = "".join(f'<script src="assets/js/{s}.js" defer></script>\n' for s in ["site", *scripts])
    if "catalog" in scripts or "quiz" in scripts or "home" in scripts:
        js = '<script src="assets/js/data.js"></script>\n' + js
    lb = f'''<dialog id="lightbox" class="dialog dialog--lightbox" aria-label="Photo viewer">
  <button class="icon-btn dialog__close" type="button" aria-label="Close photo">{icon("close")}</button>
  <figure style="margin:0"><img src="" alt=""><figcaption></figcaption></figure>
</dialog>''' if lightbox else ""
    html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#14463f">
<link rel="canonical" href="{BASE_URL}{'' if filename == 'index.html' else filename}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{BASE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/brand/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<script src="assets/js/theme-init.js"></script>
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/components.css">
<link rel="stylesheet" href="assets/css/pages.css">
</head>
<body class="{body_class}"{f' style="{style}"' if style else ""}>
{SPRITE}
<a class="skip-link" href="#main">Skip to main content</a>
{header(filename, overlay)}
<main id="main">
{body}
</main>
{footer()}
{dialogs() if dialog else ""}
{lb}
{js}</body>
</html>
'''
    (ROOT / filename).write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- components
def card(a):
    c = CAT[a["cat"]]
    if a["img"]:
        media = (f'<img src="assets/img/animals/{a["img"]}.webp" alt="{esc(a["alt"])}" width="640" height="480" loading="lazy" decoding="async">')
    else:
        media = f'<div class="animal-card__emoji" aria-hidden="true">{a["emoji"]}</div>'
    return f'''<li data-id="{a["id"]}" data-cat="{a["cat"]}"><article class="animal-card" style="{cat_vars(c)};--focus:{a.get("focus", "50% 50%")}">
  <div class="animal-card__media">{media}</div>
  <div class="animal-card__body">
    <p class="animal-card__tag"><span class="dot"></span>{c["name"]}</p>
    <h3>{esc(a["name"])}</h3>
    <p class="sci">{esc(a["sci"])}</p>
    <p class="summary">{esc(a["summary"])}</p>
    <button class="animal-card__more" type="button" data-animal="{a["id"]}" aria-label="Learn more about {esc(a["name"])}">Learn more</button>
  </div>
</article></li>'''


def cat_tile(c, with_count=True):
    n = sum(1 for a in ANIMALS if a["cat"] == c["id"])
    count = f'<p class="cat-tile__count">{n} animals</p>' if with_count else ""
    return f'''<li><a class="cat-tile" href="{c["file"]}" style="{cat_vars(c)}">
  <div class="cat-tile__img"><img src="assets/img/{c["tile"]}" alt="" width="450" height="450" loading="lazy" decoding="async"></div>
  <div class="cat-tile__body">{count}<h3>{c["name"]}</h3><p>{esc(c["blurb"].split(". ")[0].rstrip("."))}.</p></div>
</a></li>'''


def info_cards(items):
    out = ""
    for title, lines in items:
        lis = "".join(f"<li>{l}</li>" for l in lines)
        out += f'<div class="info-card"><h3>{title}</h3><ul>{lis}</ul></div>'
    return f'<div class="info-grid">{out}</div>'


# ---------------------------------------------------------------- category extras
EXTRAS = {
    "mammals": lambda: f'''<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Three ways to be a mammal</h2><p>All mammals feed their young milk, but they start life in different ways.</p></div>
  {info_cards([
      ("Egg-laying mammals", ["The platypus and echidnas lay eggs.", "Babies hatch, then drink milk."]),
      ("Pouch mammals", ["Kangaroos and koalas are marsupials.", "A tiny newborn finishes growing in the mother's pouch."]),
      ("Placental mammals", ["Lions, zebras, whales and humans.", "Babies grow inside the mother before birth."]),
  ])}
</div></section>''',
    "birds": lambda: f'''<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Bird basics</h2><p>What every bird has in common, from the smallest finch to the largest eagle.</p></div>
  {info_cards([
      ("Feathers", ["Only birds have feathers.", "They keep birds warm, dry and ready to fly."]),
      ("Hollow bones", ["Light bones make flying easier.", "Some birds, like penguins and ostriches, cannot fly at all."]),
      ("Eggs and nests", ["Every bird lays eggs.", "Parents keep the eggs warm until they hatch."]),
  ])}
</div></section>''',
    "fish": lambda: f'''<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Fish at a glance</h2><p>Six quick facts about life under the surface.</p></div>
  {info_cards([
      ("Class", ["Fish are aquatic vertebrates.", "They live in fresh water (rivers, lakes) and salt water (oceans, seas).", "They breathe through gills and move using fins."]),
      ("Body structure", ["Scales protect most fish.", "Fins (dorsal, tail, pectoral) help them swim.", "A streamlined shape helps them move fast.", "Some glow in the dark (bioluminescence)."]),
      ("Dietary behavior", ["Carnivores eat other fish or small animals (sharks, piranhas).", "Herbivores feed on algae and plants (surgeonfish).", "Omnivores eat both (goldfish).", "Some filter tiny plankton (whale sharks)."]),
      ("Life span", ["Short-lived: 1 to 5 years (guppies, betta fish).", "Medium-lived: 10 to 20 years (clownfish, goldfish).", "Long-lived: 50 to 100+ years (koi, some sharks)."]),
      ("Toxicity", ["Venomous fish have poison in spines or fangs (lionfish, stonefish).", "Poisonous fish are toxic if eaten (pufferfish).", "Most fish are harmless (goldfish, salmon)."]),
      ("Natural habitat", ["Oceans: coral reefs and the deep sea (clownfish, anglerfish).", "Rivers and lakes (catfish, trout).", "Swamps and mangroves (mudskippers).", "Polar waters: icefish in Antarctica."]),
  ])}
</div></section>
<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Sea life that is not a fish</h2><p>Plenty of animals live in the sea without being fish.</p></div>
  <div class="not-fish">
    <div class="not-fish__item"><div class="big" aria-hidden="true">🐬</div><h3>Dolphins and whales</h3><p>Mammals. They breathe air and feed their calves milk.</p></div>
    <div class="not-fish__item"><div class="big" aria-hidden="true">🪼</div><h3>Jellyfish</h3><p>Soft animals with stinging tentacles, no bones and no gills.</p></div>
    <div class="not-fish__item"><div class="big" aria-hidden="true">🪸</div><h3>Corals</h3><p>Tiny animals called polyps that build reefs together.</p></div>
    <div class="not-fish__item"><div class="big" aria-hidden="true">🐙</div><h3>Octopuses</h3><p>Mollusks with soft bodies and eight arms.</p></div>
  </div>
  <div class="photo-strip" style="margin-top:var(--space)">
    <figure style="margin:0"><img src="assets/img/cat/fish.webp" alt="Colourful reef fish swimming above coral" width="640" height="400" loading="lazy"><figcaption class="lead" style="font-size:var(--step--1)">Reef fish live among corals.</figcaption></figure>
    <figure style="margin:0"><img src="assets/img/animals/humpback-whale.webp" alt="A humpback whale swimming near the surface" width="640" height="400" loading="lazy"><figcaption class="lead" style="font-size:var(--step--1)">Not a fish: a humpback whale is a mammal.</figcaption></figure>
  </div>
</div></section>
<section class="section section--tight" id="quiz"><div class="container">
  <div class="section__head"><h2>Fish or not a fish?</h2><p>Test what you just learned. Nine sea animals, one question each.</p></div>
  <div class="quiz" id="fish-quiz">
    <div class="quiz__progress" role="progressbar" aria-label="Quiz progress" aria-valuemin="0" aria-valuenow="0"><div class="quiz__bar"></div></div>
    <p class="lead" id="quiz-count" aria-live="polite"></p>
    <div id="quiz-stage"><noscript>The quiz needs JavaScript. You can still read the facts above.</noscript></div>
    <div class="quiz__feedback" id="quiz-feedback" role="status" aria-live="polite"></div>
    <button class="btn" type="button" id="quiz-next" hidden>Next question</button>
  </div>
</div></section>''',
    "insects": lambda: f'''<section class="section section--tight"><div class="container">
  <div class="split">
    <div><div class="section__head"><h2>Three body parts, six legs</h2><p>Every insect's body has the same plan.</p></div>
      <ul class="anatomy"><li>Head<span>Eyes, antennae and mouth</span></li><li>Thorax<span>Six legs and (often) wings</span></li><li>Abdomen<span>Digestion and breathing</span></li></ul></div>
    <div class="split__media"><img src="assets/img/hero/beetles-leaf.webp" alt="Green beetles resting on a leaf" width="700" height="392" loading="lazy"></div>
  </div>
  <p style="margin-top:var(--space)">Insects pollinate flowers, and others clean up nature by eating dead plants and animals. That makes them some of the most important animals on Earth.</p>
</div></section>''',
    "arachnids": lambda: f'''<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Arachnid or insect?</h2><p>Know the difference: arachnids have 8 legs and no wings.</p></div>
  <div class="table-wrap"><table>
    <caption class="visually-hidden">Comparison of arachnids and insects</caption>
    <thead><tr><th scope="col">Feature</th><th scope="col">Arachnids</th><th scope="col">Insects</th></tr></thead>
    <tbody>
      <tr><th scope="row">Legs</th><td>8</td><td>6</td></tr>
      <tr><th scope="row">Body sections</th><td>2 (cephalothorax and abdomen)</td><td>3 (head, thorax and abdomen)</td></tr>
      <tr><th scope="row">Antennae</th><td>None</td><td>One pair</td></tr>
      <tr><th scope="row">Wings</th><td>None</td><td>Often two pairs</td></tr>
      <tr><th scope="row">Examples</th><td>Spiders, scorpions, mites, ticks</td><td>Bees, ants, butterflies, beetles</td></tr>
    </tbody></table></div>
</div></section>''',
    "mollusks": lambda: f'''<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Body parts of mollusks</h2><p>Most mollusks have a soft body, a shell (not always), a head, and a foot to move.</p></div>
  <ul class="anatomy"><li>Soft body<span>No bones inside</span></li><li>Shell<span>Snails and clams have one</span></li><li>Head<span>Eyes and feelers</span></li><li>Foot<span>A strong muscle for moving</span></li></ul>
  <div class="callout" style="margin-top:var(--space)"><h2>Fun facts</h2><p>An octopus has three hearts. Some squids can grow longer than a bus.</p><p>Mollusks are amazing creatures, and they help nature in many ways.</p></div>
</div></section>''',
    "reptiles": lambda: f'''<section class="section section--tight"><div class="container">
  <div class="split">
    <div><div class="section__head"><h2>Built for the sun</h2><p>Reptiles cannot make their own body heat, so they bask in the sun to warm up and hide in the shade to cool down.</p></div>
      {info_cards([("Skin", ["Dry scales keep water in.", "Many reptiles shed their skin as they grow."]), ("Babies", ["Most reptiles lay leathery eggs.", "Some snakes and lizards give birth to live young."])])}</div>
    <div class="split__media"><img src="assets/img/hero/reptile-pond.webp" alt="Turtles and other reptiles gathered by a jungle stream" width="640" height="480" loading="lazy"></div>
  </div>
</div></section>''',
}

DESCRIPTIONS = {
    "mammals": "Meet lions, zebras, giraffes, kangaroos, whales and bats. Learn what makes an animal a mammal.",
    "birds": "Explore eagles, falcons, owls, parrots and lovebirds, and learn what makes a bird a bird.",
    "fish": "Learn how fish breathe, swim and live, discover sea animals that are not fish, and take the fish quiz.",
    "insects": "Discover bees, butterflies, ants, beetles, flies and locusts, and the three body parts every insect has.",
    "arachnids": "Meet tarantulas, scorpions, black widows and wolf spiders, and learn how arachnids differ from insects.",
    "mollusks": "Snails, clams, squids and octopuses: learn about soft-bodied mollusks and their amazing shells.",
    "reptiles": "Explore crocodiles, iguanas, geckos, tuataras, snakes and sea turtles, the scaly survivors of the animal kingdom.",
}


def build_category(i, c):
    animals = [a for a in ANIMALS if a["cat"] == c["id"]]
    pills = "".join(
        f'<li><a href="{x["file"]}" style="--dot:{x["color"]}"{" aria-current=page" if x["id"] == c["id"] else ""}>'
        f'<span class="dot"></span>{x["name"]}</a></li>' for x in CATS)
    prev_c, next_c = CATS[i - 1], CATS[(i + 1) % len(CATS)]
    traits = "".join(f"<li>{t}</li>" for t in c["traits"])
    body = f'''<div class="container">
  <nav aria-label="Animal categories"><ul class="cat-nav">{pills}</ul></nav>
  <section class="page-hero" style="--focus:{c["heroFocus"]}">
    <img class="page-hero__img" src="assets/img/{c["hero"]}" alt="" width="1280" height="720" fetchpriority="high">
    <div class="page-hero__body">
      <p class="crumbs"><a href="home.html">Home</a> / {c["name"]}</p>
      <h1>{c["name"]}</h1>
      <p>{esc(c["tagline"])}</p>
    </div>
  </section>
</div>
<section class="section section--tight"><div class="container intro-grid">
  <div><p class="lead">{esc(c["intro"])}</p><ul class="traits" aria-label="Key traits">{traits}</ul></div>
  <aside class="callout"><h2>Did you know?</h2><p>{esc(c["didyouknow"])}</p></aside>
</div></section>
<section class="section section--tight" id="animals"><div class="container">
  <div class="section__head"><h2>Meet the {c["name"].lower()}</h2><p>Select “Learn more” on any card for habitat, diet and a fun fact.</p></div>
  <ul class="card-grid">{"".join(card(a) for a in animals)}</ul>
</div></section>
{EXTRAS[c["id"]]()}
<section class="section section--tight"><div class="container" style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap">
  <a class="btn btn--ghost" href="{prev_c["file"]}">← {prev_c["name"]}</a>
  <a class="btn" href="{next_c["file"]}">{next_c["name"]} {icon("arrow")}</a>
</div></section>'''
    scripts = ["catalog"] + (["quiz"] if c["id"] == "fish" else [])
    page(c["file"], c["name"], DESCRIPTIONS[c["id"]], body, scripts=scripts, style=cat_vars(c), dialog=True,
         og_image="assets/img/" + c["hero"])


# ---------------------------------------------------------------- pages
def build_index():
    tiles = "".join(cat_tile(c) for c in CATS)
    body = f'''<section class="landing-hero">
  <img class="landing-hero__img" src="assets/img/hero/savanna-herd.webp" alt="Lions, giraffes, zebras and other animals gathered on the savanna" width="1472" height="832" fetchpriority="high">
  <div class="container"><div class="landing-hero__body">
    <h1>Animal Base</h1>
    <p>Prepare to discover the amazing and untamed world of animals. Facts, photos and fascinating information about creatures from every corner of the globe, from fuzzy companions to ferocious hunters.</p>
    <div class="cta-row"><a class="btn btn--sun" href="home.html">Start exploring {icon("arrow")}</a><a class="btn btn--on-image-ghost" href="#families">See the animal families</a></div>
  </div></div>
</section>
<section class="section" id="families"><div class="container">
  <div class="section__head"><h2>Seven families, one place</h2><p>Pick a family to meet its animals, or search them all from the home page.</p></div>
  <ul class="cat-tiles">{tiles}</ul>
</div></section>
<section class="section section--tight"><div class="container">
  <div class="split">
    <div class="section__head"><h2>Made for curious kids and grown-ups</h2>
      <p>There is something here for every animal enthusiast, whether you love lions, whales, birds or insects. Let us explore, study and enjoy the creatures of our planet together.</p>
      <ul class="steps" style="grid-template-columns:1fr"><li><h3>Search</h3><p>Find any animal by name, habitat or diet.</p></li><li><h3>Learn</h3><p>Open a card for facts, habitats and a fun fact.</p></li><li><h3>Play</h3><p>Test yourself with the fish quiz.</p></li></ul></div>
    <div class="split__media"><img src="assets/img/hero/jungle-scene.webp" alt="A jungle scene with an elephant, birds and a waterfall" width="728" height="409" loading="lazy"></div>
  </div>
</div></section>'''
    page("index.html", SITE, "Animal Base is a friendly educational guide to mammals, birds, fish, insects, arachnids, mollusks and reptiles, with facts, photos and a quiz.",
         body, overlay=True, body_class="page-landing")


def build_home():
    tiles = "".join(cat_tile(c) for c in CATS)
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{c["id"]}" aria-pressed="false"><span class="dot" style="--dot:{c["color"]}"></span>{c["name"]}</button>' for c in CATS)
    cards = "".join(card(a) for a in ANIMALS)
    gallery = "".join(
        f'<li><button type="button" data-lightbox="assets/img/{src}" data-alt="{esc(alt)}" data-caption="{esc(cap)}" aria-label="View photo: {esc(cap)}">'
        f'<img src="assets/img/{src}" alt="{esc(alt)}" width="640" height="480" loading="lazy" decoding="async"></button></li>' for src, alt, cap in GALLERY)
    body = f'''<section class="home-hero"><div class="container">
  <h1>What would you like to discover today?</h1>
  <p class="lead" data-greeting>Welcome to the animal kingdom. Pick a family, or search for any animal.</p>
  <div class="cta-row"><a class="btn" href="#explore">{icon("search")} Search animals</a></div>
</div></section>
<section class="section section--tight" id="families"><div class="container">
  <div class="section__head"><h2>Browse by family</h2></div>
  <ul class="cat-tiles">{tiles}</ul>
</div></section>
<section class="section section--tight" id="explore"><div class="container">
  <div class="section__head"><h2>Explore every animal</h2><p>Search by name, habitat or diet, or filter by family.</p></div>
  <div class="search-panel">
    <div class="search-box">{icon("search")}<label class="visually-hidden" for="animal-search">Search animals</label>
      <input id="animal-search" type="search" placeholder="Try “lion”, “ocean” or “insects”" autocomplete="off"></div>
    <div class="chip-row" role="group" aria-label="Filter by animal family">{chips}</div>
  </div>
  <p class="result-count" id="result-count" role="status" aria-live="polite"></p>
  <ul class="card-grid" id="explore-grid">{cards}</ul>
  <div class="empty-state" id="empty-state" hidden><h3>No animals match your search</h3><p>Check the spelling, try a shorter word, or clear the filters.</p><button class="btn" type="button" id="reset-filters">Clear search and filters</button></div>
</div></section>
<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Animal of the day</h2></div>
  <article class="featured" id="featured-animal" hidden>
    <div class="featured__media"><img src="" alt="" width="640" height="480"></div>
    <div class="featured__body">
      <p class="featured__label" data-f-cat></p><h3 style="font-size:var(--step-3)" data-f-name></h3>
      <p style="font-style:italic;color:var(--ink-soft)" data-f-sci></p><p data-f-summary></p>
      <button class="btn" type="button" data-animal="">Learn more</button>
    </div>
  </article>
</div></section>
<section class="section section--tight"><div class="container">
  <div class="fact-card"><small>Did you know? <span id="fact-source"></span></small><p id="fact-text" aria-live="polite"></p>
    <button class="btn btn--sun" type="button" id="fact-next">Another fact</button></div>
</div></section>
<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Wild moments</h2><p>Select a photo to view it larger.</p></div>
  <ul class="gallery">{gallery}</ul>
</div></section>'''
    page("home.html", "Home", "Browse seven animal families and search 38 animals by name, habitat or diet. Facts, photos and a daily featured animal.",
         body, scripts=["catalog", "home"], dialog=True, lightbox=True)


def build_about():
    members = "".join(
        f'<li><div class="avatar" aria-hidden="true">{n[0]}</div><h3>{n}</h3><p class="role">{r}</p><p>{d}</p></li>' for n, r, d in TEAM)
    body = f'''<section class="home-hero"><div class="container">
  <h1>About Animal Base</h1>
  <p class="lead">This website is an educational project aimed at children, introducing them to the world of animals and their different species in a simple and fun way.</p>
</div></section>
<section class="section section--tight"><div class="container split">
  <div><h2>What you will find here</h2>
    <p>The site covers seven animal families, with information about animal types and their characteristics to help children learn in an interactive and safe manner.</p>
    <p>It started as a first-year team assignment at the Faculty of Computers and Artificial Intelligence, built with HTML, CSS and JavaScript. This edition keeps the original idea and rebuilds the design and the code.</p>
    <div class="cta-row"><a class="btn" href="home.html">Explore the animals</a><a class="btn btn--ghost" href="contact.html">Get in touch</a></div></div>
  <div class="split__media"><img src="assets/img/hero/welcome-herd.webp" alt="Giraffes, elephants, zebras and lions standing together under a welcome banner" width="640" height="480" loading="lazy"></div>
</div></section>
<section class="section section--tight"><div class="container">
  <div class="section__head"><h2>Our team</h2><p>Eight first-year students, one shared project.</p></div>
  <ul class="team">{members}</ul>
</div></section>'''
    page("about.html", "About", "Animal Base is an educational animal website created by a team of first-year students. Meet the team and learn about the project.",
         body, og_image="assets/img/hero/welcome-herd.webp")


def field(fid, label, name, typ="text", extra="", hint=""):
    h = f'<p class="hint" id="{fid}-hint">{hint}</p>' if hint else ""
    desc = f"{fid}-error" + (f" {fid}-hint" if hint else "")
    return (f'<div class="field"><label for="{fid}">{label}</label>{h}'
            f'<input id="{fid}" name="{name}" type="{typ}" aria-describedby="{desc}" {extra}>'
            f'<p class="field__error" id="{fid}-error" aria-live="polite"></p></div>')


def pw_field(fid, label, name, autocomplete, hint=""):
    h = f'<p class="hint" id="{fid}-hint">{hint}</p>' if hint else ""
    desc = f"{fid}-error" + (f" {fid}-hint" if hint else "")
    return (f'<div class="field"><label for="{fid}">{label}</label>{h}<div class="password-wrap">'
            f'<input id="{fid}" name="{name}" type="password" autocomplete="{autocomplete}" aria-describedby="{desc}">'
            f'<button type="button" aria-controls="{fid}" aria-pressed="false">Show</button></div>'
            f'<p class="field__error" id="{fid}-error" aria-live="polite"></p></div>')


def build_contact():
    body = f'''<section class="home-hero"><div class="container"><h1>Contact us</h1>
  <p class="lead">Questions, ideas or a photo of your favourite animal? Fill in the form below.</p></div></section>
<section class="section section--tight"><div class="container two-col">
  <div class="panel"><div class="notice" style="margin-bottom:1.25rem">{icon("info")}<p>This form has no server behind it. When you send it, your own email app opens with the message ready to send to {CONTACT_EMAIL}.</p></div>
    <form class="form" id="contact-form" novalidate>
      {field("c-name", "Your name", "name", extra='autocomplete="name"')}
      {field("c-email", "Your email", "email", "email", 'autocomplete="email"')}
      <div class="field"><label for="c-message">Message</label>
        <textarea id="c-message" name="message" maxlength="1000" aria-describedby="c-message-error message-count"></textarea>
        <p class="hint" id="message-count">0 / 1000</p><p class="field__error" id="c-message-error" aria-live="polite"></p></div>
      <button class="btn" type="submit">Open email draft</button>
      <p class="form-status" id="contact-status" role="status" hidden></p>
    </form></div>
  <aside class="panel"><h2 style="font-size:var(--step-2)">Other ways to reach us</h2>
    <ul class="contact-list">
      <li>Email: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></li>
      <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram (opens in a new tab)</a></li>
      <li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook group (opens in a new tab)</a></li>
      <li><a href="{NATGEO}" target="_blank" rel="noopener">National Geographic: more about animals</a></li>
    </ul></aside>
</div></section>'''
    page("contact.html", "Contact", "Contact the Animal Base team by email, Instagram or Facebook.", body, scripts=["forms"])


def build_login():
    body = f'''<div class="auth">
  <div class="auth__art"><img src="assets/img/hero/login-animals.webp" alt="" width="1000" height="683"><h1>Welcome to the animal family</h1></div>
  <div class="auth__form">
    <div class="notice" style="margin-bottom:1.25rem">{icon("info")}<p><strong>Demo only.</strong> There are no real accounts on this site. Forms are checked in your browser, nothing is sent anywhere, and passwords are never saved.</p></div>
    <div class="tabs" role="tablist" aria-label="Log in or register">
      <button role="tab" id="tab-login" aria-selected="true" aria-controls="panel-login" type="button">Log in</button>
      <button role="tab" id="tab-register" aria-selected="false" aria-controls="panel-register" tabindex="-1" type="button">Register</button>
    </div>
    <div role="tabpanel" id="panel-login" aria-labelledby="tab-login">
      <form class="form" id="login-form" novalidate>
        {field("l-username", "Username", "username", extra='autocomplete="username"')}
        {pw_field("l-password", "Password", "loginPassword", "current-password")}
        <button class="btn" type="submit">Log in (demo)</button>
        <p class="form-status" id="login-status" role="status" hidden></p>
        <a class="btn btn--sun" id="login-continue" href="home.html" hidden>Go to the home page</a>
      </form>
      <p class="guest">New here? <a href="#register" data-switch="register">Create a demo account</a></p>
    </div>
    <div role="tabpanel" id="panel-register" aria-labelledby="tab-register" hidden>
      <form class="form" id="register-form" novalidate>
        {field("r-username", "Username", "username", extra='autocomplete="username"')}
        {field("r-email", "Email", "email", "email", 'autocomplete="email"')}
        {pw_field("r-password", "Password", "newPassword", "new-password", "At least 8 characters, with a letter and a number.")}
        {field("r-age", "Age", "age", "number", 'min="7" max="120" inputmode="numeric"', "You need to be 7 or older.")}
        <button class="btn" type="submit">Register (demo)</button>
        <p class="form-status" id="register-status" role="status" hidden></p>
        <a class="btn btn--sun" id="register-continue" href="home.html" hidden>Go to the home page</a>
      </form>
      <p class="guest">Already have a demo account? <a href="#login" data-switch="login">Log in</a></p>
    </div>
    <p class="guest"><a class="btn btn--ghost" href="home.html">Continue as guest</a></p>
  </div>
</div>'''
    page("login.html", "Log in", "Log in or register for the Animal Base demo. No real accounts are created and nothing is sent anywhere.",
         body, scripts=["forms"], og_image="assets/img/hero/login-animals.webp")


def build_settings():
    themes = [("system", "System", "Follow your device", ["#f3f7f2", "#0d1c1b"]),
              ("light", "Light", "Fresh and bright", ["#f3f7f2", "#14463f", "#f6b232"]),
              ("dark", "Dark", "Easy on the eyes", ["#0d1c1b", "#7bd3a2", "#f6b232"]),
              ("playful", "Playful", "Bold and colourful", ["#fff0a8", "#6a3ad6", "#ff7a3d"])]
    opts = "".join(
        f'<label class="theme-option"><input type="radio" name="theme" value="{v}"><span>{n}<small>{d}</small>'
        f'<span class="swatch" aria-hidden="true">{"".join(f"<i style=background:{c}></i>" for c in sw)}</span></span></label>'
        for v, n, d, sw in themes)
    body = f'''<section class="home-hero"><div class="container"><h1>Settings</h1>
  <p class="lead">Make the site yours. Changes save automatically and stay in this browser only.</p></div></section>
<section class="section section--tight"><div class="container"><div class="settings-stack" id="settings">
  <div class="panel"><fieldset class="theme-options"><legend class="visually-hidden">Theme</legend>
    <h2 style="font-size:var(--step-2);grid-column:1/-1;margin:0">Theme</h2>{opts}</fieldset></div>
  <div class="panel"><h2 style="font-size:var(--step-2)">Motion</h2>
    <label class="switch"><input type="checkbox" id="reduce-motion"> Reduce animations and movement</label></div>
  <div class="panel"><h2 style="font-size:var(--step-2)">Your name</h2>
    <form class="inline-form" id="name-form" novalidate>
      <div class="field"><label for="display-name">Display name</label><p class="hint">Shown in the home page greeting.</p><input id="display-name" maxlength="40" autocomplete="nickname"></div>
      <button class="btn" type="submit" style="margin-top:2.1rem">Save name</button>
    </form><p class="hint" id="name-status" role="status"></p></div>
  <div class="panel"><h2 style="font-size:var(--step-2)">My animal list</h2>
    <p>Keep a list of animals you want to learn about.</p>
    <form class="inline-form" id="list-form" novalidate>
      <div class="field"><label for="list-input">Animal name</label><input id="list-input" maxlength="60" aria-describedby="list-input-error" autocomplete="off"><p class="field__error" id="list-input-error" aria-live="polite"></p></div>
      <button class="btn" type="submit" style="margin-top:1.75rem">Add to list</button>
    </form>
    <p class="hint" id="list-empty">Your list is empty. Add an animal above.</p>
    <ul class="my-list" id="my-list"></ul>
    <button class="btn btn--ghost btn--small" type="button" id="list-clear" style="margin-top:1rem" hidden>Clear list</button></div>
  <details class="disclosure"><summary>Where is my data stored?</summary>
    <p style="margin-top:.75rem">Your theme, name and list are saved in your browser’s local storage on this device. They are never uploaded, and clearing your browser data removes them.</p></details>
  <div><button class="btn btn--ghost" type="button" id="reset-all">Reset all settings</button> <span class="hint" id="reset-status" role="status"></span></div>
</div></div></section>'''
    page("settings.html", "Settings", "Choose a light, dark or playful theme, reduce motion and keep a personal animal list. Saved only in your browser.",
         body, scripts=["settings"])


# ---------------------------------------------------------------- data + SEO files
def write_support_files():
    pub = [{k: v for k, v in a.items() if k not in ("alt",)} | {"alt": a["alt"]} for a in ANIMALS]
    data = {"categories": [{k: c[k] for k in ("id", "name", "color", "ink", "tint", "didyouknow")} for c in CATS], "animals": pub}
    js = ("/* Generated by src/build.py from src/content.json. Do not edit by hand. */\n"
          "window.AB_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
          "window.AB_QUIZ = " + json.dumps(QUIZ, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (ROOT / "assets" / "js" / "data.js").write_text(js, encoding="utf-8")
    pages = ["index.html", "home.html"] + [c["file"] for c in CATS] + ["about.html", "contact.html", "login.html", "settings.html"]
    urls = "".join(f"  <url><loc>{BASE_URL}{'' if p == 'index.html' else p}</loc></url>\n" for p in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8")


def main():
    build_index(); build_home(); build_about(); build_contact(); build_login(); build_settings()
    for i, c in enumerate(CATS):
        build_category(i, c)
    write_support_files()
    print("Built 13 pages, data.js, sitemap.xml and robots.txt")


if __name__ == "__main__":
    main()
