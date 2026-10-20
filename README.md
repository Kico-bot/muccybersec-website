# Website: Cyber- und Risikoberatung für KMU

Statische Landingpage für CyberSec KMU 24 mit eingebautem Cyber-Check
(angelehnt an DIN SPEC 27076) und der kostenlosen ISMS-Software als zweitem Angebot. Kein Build, keine Abhängigkeiten im Browser, keine Dritt-Server.

```
index.html              Seite mit Meta-Tags, Open Graph, JSON-LD (ProfessionalService, SoftwareApplication, FAQPage)
impressum.html          Gerüst, vor dem Livegang ausfüllen
datenschutz.html        Gerüst, beschreibt was die Seite technisch tut
assets/css/styles.css   einziges Stylesheet (keine Inline-Styles, wegen CSP)
assets/js/main.js       Einstieg (ES-Modul)
assets/js/check.js      Fragebogen und Auswertung, baut DOM ohne innerHTML
assets/js/questions.js  27 Fragen, Bewertung als reine Funktion
assets/js/forms.js      Formularprüfung, Honeypot, Zeitsperre, JSON-Versand mit CSRF-Token
assets/js/dom.js        DOM-Helfer, sessionStorage-Wrapper
assets/img/logo.svg     Logo (auch als favicon.svg)
assets/fonts/           Source Serif 4 und IBM Plex Sans, selbst gehostet (SIL OFL)
_headers                Security-Header für Netlify / Cloudflare Pages
robots.txt, sitemap.xml, llms.txt   SEO und KI-Crawler
server/lead-endpoint.example.mjs    Referenz für POST /api/lead (Node, ohne Abhängigkeiten)
```

Lokal ansehen: `python3 -m http.server 8080` im Ordner `website/`, dann <http://localhost:8080>.
Über `file://` laden Browser keine ES-Module.

## Vor dem Livegang

1. `ihre-domain.de` überall durch die echte Domain ersetzen (`grep -r ihre-domain .`), auch in der Kontakt-E-Mail.
2. Impressum und Datenschutzerklärung vervollständigen, Foto und echte Kundenstimme einsetzen.
3. Die 27 Fragen gegen den Text der DIN SPEC 27076 prüfen (`assets/js/questions.js`).
4. Formular-Endpunkt betreiben (siehe unten) oder `lead-endpoint` im `<meta>` auf den eigenen Dienst setzen.
5. Header prüfen: <https://securityheaders.com>, <https://observatory.mozilla.org>.

## Sicherheit

- **XSS:** Es gibt kein `innerHTML`, kein `eval`, keine Inline-Skripte oder -Styles und keine
  `on…`-Attribute. Dynamische Inhalte entstehen über `createElement` und `textContent`, das
  Lead-Formular kommt aus einem `<template>`. Dadurch reicht eine CSP mit `script-src 'self'`
  und `style-src 'self'`.
- **CSRF:** Versand nur als `application/json` (fremde Seiten lösen einen CORS-Preflight aus,
  der nicht beantwortet wird), Prüfung von `Origin` und `Sec-Fetch-Site` auf dem Server, dazu
  ein HMAC-Token im `<meta name="csrf-token">`, das der Server beim Ausliefern einsetzt.
- **Injection:** Der Server prüft jedes Feld mit Allowlist-Mustern und Längen, entfernt
  Steuerzeichen (verhindert Mail-Header-Injection), akzeptiert vom Check nur Zahl, Stufe und
  bekannte IDs und gibt Eingaben nie zurück. Mails nur als Klartext versenden, Daten nur mit
  Prepared Statements speichern.
- **Missbrauch:** Honeypot-Feld, Mindest-Ausfüllzeit, Rate Limit (5 je IP in 10 Minuten),
  Body-Limit 8 KB, generische Fehlermeldungen.
- **Datenschutz:** Check-Antworten nur im `sessionStorage` des Tabs, keine Cookies, kein
  Tracking, Schriften vom eigenen Server.

### nginx

```nginx
add_header Content-Security-Policy "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; manifest-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests" always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()" always;
add_header Cross-Origin-Opener-Policy "same-origin" always;
location /api/ { proxy_pass http://127.0.0.1:3001; client_max_body_size 8k; }
```
