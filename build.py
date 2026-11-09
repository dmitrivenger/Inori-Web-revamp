#!/usr/bin/env python3
"""Build the INORI static site.

    pip install jinja2 pyyaml
    python3 build.py            # outputs to ./site

Content lives in src/content/*.yml (one file per language + site.yml for shared settings).
"""
import os, shutil, time, datetime, yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "site")

S = yaml.safe_load(open(os.path.join(SRC, "content", "site.yml"), encoding="utf-8"))
LANGS = {l: yaml.safe_load(open(os.path.join(SRC, "content", f"{l}.yml"), encoding="utf-8")) for l in S["languages"]}
BASE_PATH = S.get("base_path", "/")  # set to "/repo-name/" if hosted in a sub-folder (used only by 404 page)

# (page_id, path, template, extra context, title-key, description-key)
PAGES = [
    ("home", "", "home.html", {}, "home"),
    ("dpn", "dpn/", "dpn.html", {}, "dpn"),
    ("suppliers", "solutions/suppliers/", "solution.html", {"key": "suppliers"}, ("solutions", "suppliers")),
    ("buyers", "solutions/buyers/", "solution.html", {"key": "buyers"}, ("solutions", "buyers")),
    ("services", "services/", "services.html", {}, "services"),
    ("technology", "technology/", "technology.html", {}, "technology"),
    ("about", "about/", "about.html", {}, "about"),
    ("press", "press/", "press.html", {}, "press"),
    ("contact", "contact/", "contact.html", {}, "contact"),
    ("thanks", "contact/thanks/", "thanks.html", {}, None),
    ("terms", "legal/terms/", "legal.html", {"key": "terms"}, None),
    ("privacy", "legal/privacy/", "legal.html", {"key": "privacy"}, None),
    ("accessibility", "legal/accessibility/", "legal.html", {"key": "accessibility"}, None),
    ("regulatory", "legal/regulatory/", "legal.html", {"key": "regulatory"}, None),
]

# Old WordPress URLs -> new pages (static redirect stubs)
OLD = {
    "he": {"אודות/": "about/", "board/": "about/", "שיתופי-פעולה/": "contact/", "צור-קשר/": "contact/",
           "תקנון-אתר/": "legal/terms/", "privacy-policy/": "legal/privacy/"},
    "en": {"אודות/": "about/", "board/": "about/", "שיתופי-פעולה/": "contact/", "צור-קשר/": "contact/",
           "תקנון-אתר/": "legal/terms/", "privacy-policy/": "legal/privacy/"},
}

env = Environment(loader=FileSystemLoader(os.path.join(SRC, "templates")),
                  autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
version = str(int(time.time()))
CUR = {"rel": "../", "lang": "he"}          # state of the page being rendered
def _u(p): return f"{CUR['rel']}{CUR['lang']}/{p}"
def _asset(p): return f"{CUR['rel']}assets/{p}"
env.globals.update(u=_u, asset=_asset)

def write(rel, html):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html)

def render_page(lang, page_id, path, template, extra, meta_key, absolute=False):
    t = LANGS[lang]
    depth = 1 + path.count("/")
    rel = "../" * depth
    if absolute:
        rel = BASE_PATH
    CUR.update(rel=rel, lang=lang)
    u, asset = _u, _asset
    if meta_key is None:
        sec = t["legal"].get(extra.get("key", ""), None)
        title = (sec["title"] if sec else t["contact"]["thanks"]["title"]) + " | INORI Finance"
        desc = t["home"]["description"]
    else:
        m = t[meta_key] if isinstance(meta_key, str) else t[meta_key[0]][meta_key[1]]
        title, desc = m["title"], m["description"]
    ctx = dict(t=t, S=S, L=lang, langs=LANGS, page_id=page_id, path=path, title=title, description=desc,
               u=u, asset=asset, alt={l: f"{rel}{l}/{path}" for l in S["languages"]},
               version=version, year=datetime.date.today().year, **extra)
    return env.get_template(template).render(**ctx)

def redirect_html(target):
    return (f'<!DOCTYPE html><meta charset="utf-8"><title>INORI Finance</title>'
            f'<link rel="canonical" href="{target}"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={target}"><a href="{target}">{target}</a>')

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), os.path.join(OUT, "assets"))
    urls = []
    for lang in S["languages"]:
        for page_id, path, tpl, extra, mk in PAGES:
            write(f"{lang}/{path}index.html", render_page(lang, page_id, path, tpl, extra, mk))
            if page_id != "thanks":
                urls.append(f"{S['base_url']}/{lang}/{path}")
    # 404 (Hebrew, links to all languages) — uses absolute paths
    write("404.html", render_page("he", "404", "", "notfound.html", {"solid_header": False}, None, absolute=True)
          .replace("<title>", "<title>404 · "))
    # root: language detection
    write("index.html", env.get_template("root.html").render(S=S, langs=LANGS, version=version))
    # old URL redirects
    for lang, m in OLD.items():
        for old, new in m.items():
            prefix = "" if lang == "he" else "en/"
            depth = (prefix + old).count("/")
            write(f"{prefix}{old}index.html", redirect_html("../" * depth + f"{lang}/{new}"))
    # sitemap + robots
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{u}</loc></url>" for u in urls] + ["</urlset>"]
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {S['base_url']}/sitemap.xml\n")
    write(".nojekyll", "")
    shutil.copy(os.path.join(SRC, "vercel.json"), os.path.join(OUT, "vercel.json"))  # Vercel settings (redirects, caching)
    print(f"Built {len(urls)} pages into {OUT}")

if __name__ == "__main__":
    main()
