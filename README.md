# CyberSecCheck Website

Statische Landingpage für CyberSecCheck: Cybersicherheit für den Mittelstand, mit eingebautem
Cyber-Check und der kostenlosen ISMS-Suite (https://github.com/Kico-bot/ISMS_SaaS) als zweitem Angebot. Kein Build, keine Abhängigkeiten im Browser, keine Dritt-Server.

```
index.html              Seite mit Meta-Tags, Open Graph, JSON-LD (ProfessionalService, SoftwareApplication, FAQPage)
leistungen/*.html       eine Unterseite je Leistung (ohne JavaScript)
impressum.html          Pflichtangaben nach § 5 DDG
datenschutz.html        Datenschutzerklärung, beschreibt was die Seite technisch tut
assets/css/site.css   einziges Stylesheet (keine Inline-Styles, wegen CSP)
assets/scripts/main.js       Einstieg (ES-Modul)
assets/scripts/check.js      Fragebogen und Auswertung, baut DOM ohne innerHTML
assets/scripts/questions.js  27 Fragen, Bewertung als reine Funktion
assets/scripts/forms.js      Formularprüfung, Honeypot, Zeitsperre, Versand an den Cloudflare Worker
assets/scripts/dom.js        DOM-Helfer, sessionStorage-Wrapper
assets/img/logo.svg     Wortmarke, favicon.svg das Kürzel M
assets/video/           Erklärvideo zur ISMS-Suite (MP4, 720p), Vorschaubild in assets/img/
assets/fonts/           Manrope, selbst gehostet (SIL OFL)
_headers                Security-Header für Netlify / Cloudflare Pages
robots.txt, sitemap.xml, llms.txt   SEO und KI-Crawler
```

Lokal ansehen: `python3 -m http.server 8080` im Hauptordner, dann <http://localhost:8080>.
Über `file://` laden Browser keine ES-Module.

## Vor dem Livegang

1. Die 27 Fragen gegen den Text der DIN SPEC 27076 prüfen (`assets/scripts/questions.js`).
2. Im Cloudflare Worker die Prüfungen aus dem Abschnitt „Kontaktformular“ umsetzen.
3. Header prüfen: <https://securityheaders.com>, <https://observatory.mozilla.org>.

## Sicherheit

- **XSS:** Es gibt kein `innerHTML`, kein `eval`, keine Inline-Skripte oder -Styles und keine
  `on…`-Attribute. Dynamische Inhalte entstehen über `createElement` und `textContent`.
  Dadurch reicht eine CSP mit `script-src 'self'` und `style-src 'self'`.
- **Kontaktformular:** geht an den Cloudflare Worker `contact-form.kristian95.workers.dev`.
  Die CSP erlaubt `connect-src` und `form-action` nur für diese Adresse, `forms.js` akzeptiert
  kein anderes Ziel. Im Browser: Prüfung jedes Felds, Honeypot `website`, Mindest-Ausfüllzeit.
- **Datenschutz:** Check-Antworten nur im `sessionStorage` des Tabs, keine Cookies, kein
  Tracking, Schriften vom eigenen Server.

## Kontaktformular: was der Worker selbst prüfen muss

Die Prüfung im Browser lässt sich umgehen. Der Worker muss deshalb:

1. nur `POST` annehmen, die Felder `name`, `email`, `subject`, `message` per `request.formData()`
   lesen und alles andere ignorieren, insbesondere ein gefülltes Feld `website` (Honeypot) still
   verwerfen;
2. Längen begrenzen (Name 80, E-Mail 254, Betreff 150, Nachricht 2000 Zeichen) und das Format der
   E-Mail prüfen;
3. Zeilenumbrüche aus Name, E-Mail und Betreff entfernen, bevor sie in Mail-Header wie `Subject`
   oder `Reply-To` gehen (sonst Mail-Header-Injection), und die Mail als Klartext versenden;
4. den `Origin` prüfen und nur `https://cyber-sec-check.de` zulassen;
5. Missbrauch begrenzen: Cloudflare Rate Limiting oder Turnstile;
6. für die Rückmeldung im Browser CORS erlauben:

```js
const ORIGIN = "https://cyber-sec-check.de";
const cors = { "Access-Control-Allow-Origin": ORIGIN, "Access-Control-Allow-Methods": "POST, OPTIONS", "Vary": "Origin" };
if (request.method === "OPTIONS") return new Response(null, { headers: cors });
if (request.headers.get("Origin") !== ORIGIN) return new Response("Forbidden", { status: 403 });
// … prüfen, Mail senden …
return new Response("OK", { headers: cors });
```

Ohne CORS-Freigabe kommt die Nachricht trotzdem an, die Seite kann die Antwort aber nicht lesen
und zeigt einen vorsichtigen Hinweis statt „Danke“.

### nginx

```nginx
add_header Content-Security-Policy "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self'; font-src 'self'; connect-src 'self' https://contact-form.kristian95.workers.dev; manifest-src 'self'; form-action 'self' https://contact-form.kristian95.workers.dev; base-uri 'none'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests" always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()" always;
add_header Cross-Origin-Opener-Policy "same-origin" always;
```
