# Animal Base (Animal Site)

A friendly, educational guide to the animal kingdom. Originally a first-year team project at the Faculty of Computers and Artificial Intelligence, this edition rebuilds the design and the code as a modern, lightweight, front-end-only website.

## Features

- **13 pages:** landing, home, seven animal families (mammals, birds, fish, insects, arachnids, mollusks, reptiles), about, contact, login (demo) and settings.
- **38 animals** with habitat, diet, a fun fact and a link to read more. Each card opens an accessible details dialog.
- **Search and filter** across every animal on the home page, with live result count and an empty state.
- **Animal of the day**, rotating fun facts and a photo gallery with a lightbox.
- **Fish or not a fish?** A nine-question quiz with instant feedback and a score.
- **Three themes:** Light, Dark and Playful (plus "follow my device"), a reduce-motion option, a saved display name and a personal animal list. All saved in `localStorage` only.
- **Honest forms:** login and register are clearly labelled demos (nothing is sent or stored, and passwords are never saved). The contact form validates and opens your email app with a ready-made message.
- **Responsive and accessible:** mobile-first layout, semantic HTML, skip link, keyboard-friendly menus and dialogs, visible focus, ARIA live regions, `prefers-reduced-motion` support and WCAG-checked colour contrast.
- **SEO basics:** titles, descriptions, canonical URLs, Open Graph tags, `sitemap.xml`, `robots.txt`.

## Technologies

HTML5, modern CSS (custom properties, grid, `color-mix`, container-free responsive layout) and vanilla JavaScript (no frameworks, no dependencies, no build tooling). Fonts (Bricolage Grotesque and Figtree) load from Google Fonts with system-font fallbacks, so the site still works offline. Images are optimised WebP.

## Run it locally

No setup is needed. Extract the project and open `index.html` in a browser. To use a local server instead:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Project structure

```
index.html … settings.html   Generated pages (13)
assets/
  css/   base.css (tokens, themes, reset) · components.css · pages.css
  js/    theme-init · site · catalog · home · quiz · forms · settings · data (generated)
  img/   brand/ · hero/ · cat/ (family tiles) · animals/
src/
  content.json   All categories and animals: edit content here
  build.py       Page generator (Python standard library only)
sitemap.xml · robots.txt
```

### Editing content

The HTML pages are generated from `src/content.json` and `src/build.py` so the header, footer and cards are never copy-pasted. After editing either file, rebuild with:

```bash
python3 src/build.py
```

Python 3.8+ is the only requirement. You can also edit the generated HTML or CSS directly if you prefer.

## Images and licensing: please read

The original repository did not record where its images came from, so their licences are **unknown**. Several look AI-generated. This edition could not download Unsplash photos, so it keeps the original images (converted to WebP). Before publishing widely, replace them with photos whose licence you can verify:

1. Find a photo that matches the animal (for example on [Unsplash](https://unsplash.com/) and review its licence and attribution guidance).
2. Save it as WebP (about 1200 px wide, 4:3 works best) to `assets/img/animals/<id>.webp`, using the animal's `img` name from `content.json`.
3. Optionally add `"credit": "Photographer name / Unsplash"` to that animal in `content.json`. It is shown in the details dialog.
4. Run `python3 src/build.py`.

The four fish cards use emoji instead of photos because the original project had no matching fish photos.

## Known limitations

- Several original photos are small (about 270 px wide) and look soft on large or high-density screens.
- Login and register are demonstrations by design. There is no backend.
- The contact form relies on the visitor's email app (`mailto:`).
- Animal facts were rewritten for clarity and checked for common errors, but have not been reviewed by a biologist.
