# Lokaler Testserver, der Adressen wie Cloudflare Pages auflöst:
# /impressum -> impressum.html, /ratgeber/ -> ratgeber/index.html.
# Start: python3 tools/serve.py [port], dann http://localhost:8000 öffnen.
import http.server, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def translate_path(self, path):
        local = super().translate_path(path)
        if not os.path.exists(local) and os.path.exists(local + ".html"):
            return local + ".html"
        return local

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
