# Erzeugt alle Unterseiten (Landingpages, Leistungen, Ratgeber) und die Sitemap aus den
# Inhaltsdateien in tools/content/. Kopf, Fuß, Navigation und JSON-LD kommen so von einer Stelle.
# Start: python3 tools/build.py   Danach: python3 tools/check_links.py
import datetime, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from content import landing, leistungen, ratgeber  # noqa: E402

DOMAIN = "https://cyber-sec-check.de"
BRAND = "CyberSecCheck"
AUTHOR = "Cyber Security Check"
CREDS = "ISO/IEC 27001 Lead Implementer · ISO/IEC 27005 Risk Manager"
TODAY = datetime.date.today().isoformat()
ARROW = '<svg aria-hidden="true"><use href="#i-arrow"/></svg>'

NAV = [("Leistungen", "/#leistungen"), ("ISO 27001", "/iso-27001-beratung-muenchen"),
       ("NIS2", "/nis2-beratung-muenchen"), ("Ratgeber", "/ratgeber/"), ("Kontakt", "/#kontakt")]


def e(s):
    return html.escape(s, quote=False)


def t(s):
    """Fließtext: escapen, dann [Text](/pfad) als Link und **Text** als Hervorhebung."""
    s = e(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)


def plain(s):
    """Text für Meta-Tags und JSON-LD: ohne Link- und Hervorhebungsmarkup."""
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s))


def url(path):
    return f"{DOMAIN}/{path}" if path else DOMAIN + "/"


def blocks(items, indent="        "):
    out = []
    for kind, val in items:
        if kind in ("h2", "h3"):
            out.append(f"{indent}<{kind}>{t(val)}</{kind}>")
        elif kind == "p":
            out.append(f"{indent}<p>{t(val)}</p>")
        elif kind in ("ul", "ol"):
            li = "".join(f"<li>{t(x)}</li>" for x in val)
            out.append(f'{indent}<{kind} class="list">{li}</{kind}>')
        elif kind == "note":
            out.append(f'{indent}<p class="note">{t(val)}</p>')
        elif kind == "todo":
            out.append(f"{indent}<!-- TODO: {val} -->")
        else:
            raise ValueError(kind)
    return "\n".join(out)


def breadcrumb_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": url(p.lstrip("/")) if not p.startswith("http") else p}
        for i, (n, p) in enumerate(crumbs, 1)]}


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq]}


def header(current):
    links = "\n".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{n}</a>' for n, h in NAV)
    return f'''<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{BRAND}, zur Startseite"><span class="brand-word">CyberSec<span class="brand-accent">Check</span></span></a>
    <nav class="nav" aria-label="Hauptnavigation">
{links}
      <a class="btn btn-sm" href="/#check">Cyber-Check</a>
    </nav>
  </div>
</header>'''


def footer():
    col = lambda title, items: (f'      <nav aria-label="{title}"><h2>{title}</h2><ul>'
                                + "".join(f'<li><a href="{h}">{e(n)}</a></li>' for n, h in items) + "</ul></nav>")
    return f'''<footer>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <span class="brand-word">CyberSec<span class="brand-accent">Check</span></span>
      <p>Informationssicherheit für den Mittelstand. Vor Ort in München und Umgebung, bundesweit per Video.</p>
    </div>
{col("Themen", [(p["nav"], "/" + p["slug"]) for p in landing.PAGES] + [("ISMS-Suite", "/#software"), ("Cyber-Check", "/#check")])}
{col("Leistungen", [(p["nav"], "/" + p["slug"]) for p in leistungen.PAGES])}
{col("Ratgeber", [("Alle Artikel", "/ratgeber/")] + [(a["nav"], "/" + a["slug"]) for a in ratgeber.FEATURED])}
  </div>
  <div class="wrap footer-base">
    <span>© 2026 {BRAND} · Diese Seite setzt keine Tracking-Cookies.</span>
    <nav aria-label="Rechtliches"><a href="/impressum">Impressum</a><a href="/datenschutz">Datenschutz</a></nav>
  </div>
</footer>'''


def document(p, ld, main, og_type="website"):
    path = p["slug"]
    return f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(p["title"])}</title>
  <meta name="description" content="{html.escape(p["desc"])}">
  <meta name="robots" content="index, follow">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="theme-color" content="#081326">
  <!-- Ersatz-CSP für Hosts ohne eigene Header; diese Seite braucht kein JavaScript. -->
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'none'; object-src 'none'; upgrade-insecure-requests">
  <link rel="canonical" href="{url(path)}">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/site.css">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{html.escape(p["title"])}">
  <meta property="og:description" content="{html.escape(p["desc"])}">
  <meta property="og:url" content="{url(path)}">
  <meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
  <meta property="og:image:alt" content="CyberSecCheck: Informationssicherheit für den Mittelstand">
  <script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<svg class="sprite" aria-hidden="true" focusable="false">
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</svg>

{header(p.get("nav_current", ""))}

<main id="inhalt">
{main}
</main>

{footer()}
</body>
</html>
'''


def crumbs_html(crumbs):
    parts = [f'<a href="{h}">{e(n)}</a>' for n, h in crumbs[:-1]] + [f'<span aria-current="page">{e(crumbs[-1][0])}</span>']
    return '<nav class="crumbs" aria-label="Brotkrumen">' + '<span aria-hidden="true">/</span>'.join(parts) + "</nav>"


def hero(p, meta=""):
    return f'''  <section class="sub-hero" aria-labelledby="page-title">
    <div class="wrap">
      {crumbs_html(p["crumbs"])}
      <span class="eyebrow">{e(p["eyebrow"])}</span>
      <h1 id="page-title">{e(p["h1"])}</h1>
      <p class="hero-sub">{t(p["lead"])}</p>{meta}
      <div class="actions">
        <a class="btn" href="/#kontakt">Kostenloses Erstgespräch {ARROW}</a>
        <a class="btn btn-line" href="/#check">Cyber-Check in 5 Minuten</a>
      </div>
    </div>
  </section>'''


def related(items, title="Passt dazu"):
    li = "\n".join(f'        <li><a href="{h}"><span><strong>{e(n)}</strong><small>{e(d)}</small></span>{ARROW}</a></li>'
                   for n, h, d in items)
    return f'''  <section class="section mist" aria-labelledby="rel-title">
    <div class="wrap">
      <div class="head"><h2 id="rel-title">{title}</h2></div>
      <ul class="more-services rel">
{li}
      </ul>
    </div>
  </section>'''


def cta():
    return f'''  <section class="cta-band" aria-labelledby="cta-title">
    <div class="wrap">
      <div>
        <h2 id="cta-title">Lassen Sie uns sprechen</h2>
        <p>30 Minuten, kostenlos und unverbindlich. Vor Ort in München und Umgebung oder per Video. Die <a href="/#software">ISMS-Suite</a> können Sie schon vorher kostenlos ausprobieren.</p>
      </div>
      <div class="actions">
        <a class="btn" href="/#kontakt">Erstgespräch anfragen {ARROW}</a>
        <a class="btn btn-outline" href="/#check">Cyber-Check starten</a>
      </div>
    </div>
  </section>'''


def faq_html(faq):
    return f'''  <section class="section" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="head head-c"><h2 id="faq-title">Häufige Fragen</h2></div>
      <div class="faq">
{chr(10).join(f"        <details><summary>{e(q)}</summary><div><p>{t(a)}</p></div></details>" for q, a in faq)}
      </div>
    </div>
  </section>'''


def offer_page(p):
    """Landingpages und Leistungsseiten: gleicher Aufbau, eigener Inhalt."""
    ld = [{"@type": "Service", "name": p["service"], "serviceType": p["service"], "description": plain(p["lead"]),
           "url": url(p["slug"]), "provider": {"@id": DOMAIN + "/#business"},
           "areaServed": [{"@type": "City", "name": "München"}, {"@type": "State", "name": "Bayern"},
                          {"@type": "Country", "name": "Deutschland"}]},
          {"@type": "ProfessionalService", "@id": DOMAIN + "/#business", "name": BRAND, "url": DOMAIN + "/"},
          breadcrumb_ld(p["crumbs"]), faq_ld(p["faq"])]
    steps = "\n".join(f"        <li><h3>{e(a)}</h3><p>{t(b)}</p></li>" for a, b in p["steps"])
    main = f'''{hero(p)}

  <section class="section" aria-labelledby="about-title">
    <div class="wrap sub-grid">
      <div class="prose">
{blocks(p["body"])}
      </div>
      <aside class="deliver" aria-labelledby="get-title">
        <h2 id="get-title">Was Sie bekommen</h2>
        <ul class="checks">
{chr(10).join(f"          <li>{t(g)}</li>" for g in p["get"])}
        </ul>
        <a class="btn" href="/#kontakt">Erstgespräch anfragen {ARROW}</a>
      </aside>
    </div>
  </section>

  <section class="section mist" aria-labelledby="steps-title">
    <div class="wrap">
      <div class="head"><h2 id="steps-title">{e(p.get("steps_title", "So läuft es ab"))}</h2></div>
      <ol class="process{" process-" + str(len(p["steps"])) if len(p["steps"]) != 4 else ""}">
{steps}
      </ol>
    </div>
  </section>

  <section class="section" aria-labelledby="local-title">
    <div class="wrap">
      <div class="prose local">
        <h2 id="local-title">{e(p["local"][0])}</h2>
{blocks([("p", x) for x in p["local"][1:]])}
      </div>
    </div>
  </section>

{faq_html(p["faq"])}

{related(p["related"])}

{cta()}'''
    return document(p, ld, main)


def de_date(iso):
    y, m, d = iso.split("-")
    months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    return f"{int(d)}. {months[int(m) - 1]} {y}"


def author_box():
    return f'''      <aside class="author-box" aria-label="Über den Autor">
        <span class="author-mark" aria-hidden="true">CSC</span>
        <div>
          <strong>{AUTHOR}</strong>
          <p>{CREDS}. Beratung zu Informationssicherheit, ISO 27001 und NIS2 für kleine und mittlere Unternehmen, vor Ort in München und Umgebung, bundesweit per Video.</p>
        </div>
      </aside>'''


def article_page(a):
    a = dict(a, eyebrow="Ratgeber", nav_current="/ratgeber/",
             crumbs=[("Startseite", "/"), ("Ratgeber", "/ratgeber/"), (a["nav"], "/" + a["slug"])])
    ld = [{"@type": "Article", "headline": a["h1"].replace("\u00ad", ""), "description": a["desc"], "url": url(a["slug"]),
           "mainEntityOfPage": url(a["slug"]), "datePublished": a["date"], "dateModified": a.get("updated", a["date"]),
           "inLanguage": "de-DE", "image": DOMAIN + "/assets/img/og-image.jpg",
           "author": {"@type": "Organization", "name": AUTHOR, "url": DOMAIN + "/", "description": CREDS},
           "publisher": {"@type": "Organization", "name": BRAND, "url": DOMAIN + "/",
                         "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/img/logo.svg"}}},
          breadcrumb_ld(a["crumbs"])]
    if a.get("faq"):
        ld.append(faq_ld(a["faq"]))
    meta = f'\n      <p class="article-meta">Stand: <time datetime="{a.get("updated", a["date"])}">{de_date(a.get("updated", a["date"]))}</time> · {AUTHOR}</p>'
    keys = "".join(f"<li>{t(k)}</li>" for k in a["key"])
    sources = "".join(f'<li><a href="{h}" rel="noopener">{e(n)}</a></li>' for n, h in a["sources"])
    faq = ""
    if a.get("faq"):
        faq = "\n        <h2>Häufige Fragen</h2>\n" + "\n".join(
            f"        <details><summary>{e(q)}</summary><div><p>{t(ans)}</p></div></details>" for q, ans in a["faq"])
        faq = f'\n        <div class="faq faq-inline">{faq}\n        </div>'
    main = f'''{hero(a, meta)}

  <section class="section article-section">
    <div class="wrap">
      <article class="prose article">
        <div class="keypoints"><h2>Auf einen Blick</h2><ul class="checks">{keys}</ul></div>
{blocks(a["body"])}{faq}
        <div class="sources"><h2>Quellen</h2><ul>{sources}</ul>
          <p>Dieser Artikel ist eine allgemeine Information und keine Rechtsberatung. Maßgeblich ist der jeweils aktuelle Gesetzes- und Normtext.</p>
        </div>
      </article>
{author_box()}
    </div>
  </section>

{related(a["related"], "Weiterlesen")}

{cta()}'''
    return document(a, ld, main, og_type="article")


def ratgeber_index():
    p = dict(ratgeber.INDEX, slug="ratgeber/", nav_current="/ratgeber/",
             crumbs=[("Startseite", "/"), ("Ratgeber", "/ratgeber/")])
    def card(a):
        return f'''        <li><a href="/{a["slug"]}">
          <span class="eyebrow">{e(a["topic"])}</span>
          <h3>{e(a["h1"])}</h3>
          <p>{e(a["desc"])}</p>
          <span class="more">Artikel lesen {ARROW}</span>
        </a></li>'''
    groups = []
    for topic in ratgeber.TOPICS:
        items = [a for a in ratgeber.ARTICLES if a["topic"] == topic]
        if items:
            groups.append(f'''      <h2 class="topic-head" id="{re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")}">{e(topic)}</h2>
      <ul class="article-list">
{chr(10).join(card(a) for a in items)}
      </ul>''')
    cards = "\n".join(groups)
    ld = [{"@type": "CollectionPage", "name": p["h1"].replace("\u00ad", ""), "description": p["desc"], "url": url("ratgeber/"),
           "hasPart": [{"@type": "Article", "headline": a["h1"], "url": url(a["slug"])} for a in ratgeber.ARTICLES]},
          breadcrumb_ld(p["crumbs"])]
    main = f'''{hero(p)}

  <section class="section">
    <div class="wrap">
{cards}
    </div>
  </section>

{cta()}'''
    return document(p, ld, main)


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def inject_footer(path):
    """Startseite und Rechtstexte sind handgeschrieben; Navigation und Fuß kommen von hier."""
    full = os.path.join(ROOT, path)
    s = open(full, encoding="utf-8").read()
    s2 = re.sub(r"<footer>.*?</footer>", lambda m: footer(), s, count=1, flags=re.S)
    nav = re.search(r'    <nav class="nav".*?</nav>', header(""), re.S).group(0)
    s2 = re.sub(r'    <nav class="nav".*?</nav>', lambda m: nav, s2, count=1, flags=re.S)
    if s2 != s:
        write(path, s2)


def sitemap(paths):
    rows = "\n".join(f"  <url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod></url>" for p in paths)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{rows}
</urlset>
'''


if __name__ == "__main__":
    built = []
    for p in landing.PAGES + leistungen.PAGES:
        write(p["slug"] + ".html", offer_page(p)); built.append(p["slug"])
    write("ratgeber/index.html", ratgeber_index()); built.append("ratgeber/")
    for a in ratgeber.ARTICLES:
        write(a["slug"] + ".html", article_page(a)); built.append(a["slug"])
    for page in ("index.html", "impressum.html", "datenschutz.html"):
        inject_footer(page)
    write("sitemap.xml", sitemap([""] + built + ["impressum", "datenschutz"]))
    print("\n".join(built))
