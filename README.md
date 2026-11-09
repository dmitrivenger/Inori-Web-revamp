# INORI Finance — Website

New website for [inori.co.il](https://inori.co.il): a premium, trilingual static site (Hebrew · English · Russian) for the DPN blockchain factoring platform.

## Languages
- **Hebrew is the default** (right-to-left), English and Russian are full translations.
- Visiting the root `/` picks the language automatically:
  1. the language the visitor chose before in the switcher (remembered in the browser),
  2. otherwise the browser/OS language (Hebrew, Russian or English),
  3. otherwise Hebrew.
- If someone lands directly on a page in another language, a small bar offers to switch to their own language (no forced redirect, so search engines and shared links keep working).

## Pages (per language: `/he/…`, `/en/…`, `/ru/…`)
Home · DPN Platform · Solutions (Payers, Suppliers, Funders) · Services · Technology · About (incl. leadership) · Press (articles + videos) · Contact (+ thank-you page) · Legal (Terms, Privacy, Accessibility statement, Regulatory) · 404.
Old WordPress addresses (`/אודות/`, `/en/board/`, `/צור-קשר/` …) redirect to the new pages.

## Edit content
All texts are in `src/content/`:
- `he.yml`, `en.yml`, `ru.yml` — page texts (same structure in each file)
- `site.yml` — shared settings: contact details, press links, videos, team LinkedIn links, **form endpoint**, domain

## Build & preview
```bash
pip install jinja2 pyyaml
python3 build.py                                  # → ./site
python3 -m http.server 8000 --directory site      # open http://localhost:8000
```

## Images
- Originals: `visuals/` (generated graphics) and `visuals/managment/` (headshots).
- Web versions are in `src/static/img/` (WebP, 960 + 1920 px). To regenerate after replacing a visual:
  `pip install pillow && python3 tools_process_images.py visuals src/static/img`
- Platform screenshots: currently placeholder mockups on the DPN page — replace `dpn_mockup-*` when real screenshots are ready.

## Publish (Vercel)
The site is hosted on Vercel and deploys automatically on every push to `main`.
Vercel project settings: **Framework: Other · Root Directory: `site` · Build command: empty**.
Redirects from old WordPress URLs, caching and security headers are in `src/vercel.json` (copied into `site/` by `build.py`).

Workflow: edit `src/` → `python3 build.py` → commit (including `site/`) → push.

A manual GitHub Pages workflow is also available in `.github/workflows/deploy.yml`.

## Before going live
- [ ] Connect the contact form: put a form-backend URL (e.g. Formspree) in `site.yml → form_endpoint`. Until then the form opens the visitor's e-mail app.
- [ ] Move the videos from the old WordPress host into `assets/video` (links in `site.yml` will break when WordPress is switched off).
- [ ] Legal review of Terms, Privacy, Accessibility statement (name an accessibility coordinator).
- [ ] Review copy in all three languages.
- [ ] Add real DPN platform screenshots.

## Docs
`docs/` — site audit, sitemap, visual prompts.
