# Prüft alle internen Links und Anker der HTML-Dateien gegen die Dateien im Repo
# und die JSON-LD-Blöcke auf gültiges JSON. Start: python3 tools/check_links.py
import glob, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links, self.ids, self.ld, self._in_ld = [], set(), [], False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        for k in ("href", "src", "poster"):
            if a.get(k): self.links.append(a[k])
        self._in_ld = tag == "script" and a.get("type") == "application/ld+json"
    def handle_data(self, data):
        if self._in_ld: self.ld.append(data)
    def handle_endtag(self, tag):
        if tag == "script": self._in_ld = False

def resolve(page, href):
    path = href.split("#")[0].split("?")[0]
    base = ROOT if path.startswith("/") else os.path.dirname(page)
    local = os.path.normpath(os.path.join(base, path.lstrip("/")))
    for cand in (local, local + ".html", os.path.join(local, "index.html")):
        if os.path.isfile(cand): return cand
    return None

pages = {p: Page() for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)}
for p, parser in pages.items(): parser.feed(open(p, encoding="utf-8").read())
errors = []
for p, parser in pages.items():
    rel = os.path.relpath(p, ROOT)
    for block in parser.ld:
        try: json.loads(block)
        except ValueError as e: errors.append(f"{rel}: JSON-LD ungültig ({e})")
    for href in parser.links:
        if re.match(r"^(https?:|mailto:|tel:|data:)", href) or href.startswith("#") and href[1:] in parser.ids: continue
        if href.startswith("#"): errors.append(f"{rel}: Anker fehlt {href}"); continue
        target = resolve(p, href)
        if not target: errors.append(f"{rel}: Link ins Leere {href}"); continue
        frag = href.split("#")[1] if "#" in href else ""
        if frag and target in pages and frag not in pages[target].ids:
            errors.append(f"{rel}: Anker fehlt {href}")
print("\n".join(errors) or f"{len(pages)} Seiten, alle Links und JSON-LD in Ordnung.")
sys.exit(1 if errors else 0)
