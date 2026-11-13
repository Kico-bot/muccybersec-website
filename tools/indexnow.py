# Meldet geänderte Seiten per IndexNow an Bing, Yandex, Seznam und Naver. Bing speist auch die
# Suche von ChatGPT und Copilot, deshalb lohnt sich das für die Sichtbarkeit in KI-Antworten.
# Erst nach dem Deploy ausführen, wenn die Seiten live sind:
#   python3 tools/indexnow.py            Seiten aus dem letzten Commit
#   python3 tools/indexnow.py HEAD~3     Seiten aus den letzten drei Commits
#   python3 tools/indexnow.py --all      alle Seiten aus der Sitemap
# Der Schlüssel liegt als <Schlüssel>.txt im Wurzelverzeichnis und wird von tools/build.py geschrieben.
import json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from build import DOMAIN, INDEXNOW_KEY  # noqa: E402

HOST = DOMAIN.split("//")[1]


def sitemap_urls():
    return re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())


def changed_urls(since):
    files = subprocess.run(["git", "diff", "--name-only", since, "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.split()
    known = set(sitemap_urls())
    out = []
    for f in files:
        if not f.endswith(".html"):
            continue
        path = f[:-len("index.html")] if f.endswith("index.html") else f[:-len(".html")]
        u = f"{DOMAIN}/{path}"
        if u in known:
            out.append(u)
    return out


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    urls = sitemap_urls() if arg == "--all" else changed_urls(arg)
    if not urls:
        print("Keine geänderten Seiten aus der Sitemap gefunden.")
        return
    body = json.dumps({"host": HOST, "key": INDEXNOW_KEY, "keyLocation": f"{DOMAIN}/{INDEXNOW_KEY}.txt",
                       "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        # 200 und 202 heißen angenommen; 403 heißt meist, die Schlüsseldatei ist noch nicht live.
        print(f"IndexNow: HTTP {r.status}, {len(urls)} Adressen gemeldet")
    print("\n".join(urls))


if __name__ == "__main__":
    main()
