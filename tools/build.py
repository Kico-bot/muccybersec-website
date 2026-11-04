# Erzeugt die fünf Leistungsseiten unter leistungen/ aus einer Datenquelle (python3 tools/build.py),
# damit Aufbau, Navigation und strukturierte Daten auf allen Seiten gleich sind.
import html, json, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
DOMAIN = "https://cyber-sec-check.de"
BRAND = "CyberSecCheck"

S = [
  dict(slug="sicherheitsanalysen", title="Sicherheitsanalysen",
    desc="Sicherheitsanalysen für den Mittelstand: Risikoanalyse, Gap-Analyse nach ISO 27001 und Schwachstellenmanagement, für Kleinbetriebe nach DIN SPEC 27076. München und bundesweit.",
    lead="Bevor Sie Geld in Sicherheit stecken, sollten Sie wissen, wo die Lücken liegen. Ich schaue mir Ihr Unternehmen an und sage Ihnen, was zuerst kommt.",
    about=[
      "Die meisten Unternehmen haben schon einiges getan: Virenschutz, Backups, vielleicht eine Firewall. Was oft fehlt, ist der Überblick. Welche Systeme sind für den Betrieb wirklich wichtig? Wo liegen Daten, die nicht verloren gehen dürfen? Und welche Lücke würde ein Angreifer zuerst ausnutzen?",
      "Eine Sicherheitsanalyse beantwortet diese Fragen. Je nach Ausgangslage ist das eine Risikoanalyse, eine Gap-Analyse gegen ISO 27001 oder BSI IT-Grundschutz oder der Aufbau eines Schwachstellenmanagements, das bekannte Lücken in Ihren Systemen regelmäßig findet und nachverfolgt.",
      "Für Klein- und Kleinstunternehmen gibt es mit der DIN SPEC 27076 ein eigenes Verfahren. Es prüft 27 Anforderungen in sechs Themenfeldern, kommt mit einem Gespräch von wenigen Stunden aus und endet mit einem Bericht, den man auch ohne Fachwissen versteht.",
    ],
    get=["Eine Übersicht Ihrer wichtigsten Systeme, Daten und Dienstleister",
         "Eine Bewertung der Risiken nach Wahrscheinlichkeit und Schaden",
         "Einen Maßnahmenplan, sortiert nach Dringlichkeit und Aufwand",
         "Eine Ergebnisbesprechung mit der Geschäftsführung"],
    steps=[("Vorgespräch", "Wir klären, was geprüft wird und welches Verfahren passt. Danach bekommen Sie ein Angebot."),
           ("Bestandsaufnahme", "Gespräche mit Geschäftsführung und IT, ein Blick in vorhandene Unterlagen und auf die wichtigsten Systeme. Vor Ort in München oder per Video."),
           ("Bewertung", "Ich bewerte die Risiken und leite Maßnahmen ab. Was schnell und günstig umsetzbar ist, steht oben."),
           ("Ergebnis", "Sie bekommen den Bericht, und wir gehen ihn gemeinsam durch. Auf Wunsch begleite ich auch die Umsetzung.")],
    faq=[("Wie lange dauert eine Sicherheitsanalyse?", "Das hängt von Größe und Umfang ab. Bei einem kleinen Unternehmen reichen oft wenige Tage, verteilt auf zwei bis drei Wochen. Den genauen Rahmen nenne ich Ihnen im Angebot."),
         ("Was ist der Unterschied zum kostenlosen Cyber-Check?", "Der Cyber-Check ist eine Selbsteinschätzung in fünf Minuten. Bei der Analyse schaue ich mir Ihre Situation selbst an, frage nach und prüfe Unterlagen. Das Ergebnis ist genauer und hält auch gegenüber Kunden oder Versicherern stand."),
         ("Brauchen wir dafür einen eigenen IT-Mitarbeiter?", "Nein. Wenn Sie einen externen IT-Dienstleister haben, beziehe ich ihn ein. Viele Fragen kann er direkt beantworten.")]),
  dict(slug="security-awareness", title="Security Awareness",
    desc="Security Awareness für Unternehmen: Online-Schulungen und Phishing-Simulationen mit Auswertung, auch für die Geschäftsleitung nach NIS2. München und bundesweit.",
    lead="Die meisten Angriffe beginnen mit einer E-Mail oder einem Anruf. Mit Online-Schulungen und Phishing-Simulationen lernen Ihre Mitarbeitenden, solche Versuche zu erkennen.",
    about=[
      "Technik hält viel ab, aber nicht alles. Eine gut gemachte Phishing-Mail, eine gefälschte Rechnung oder ein Anruf vom angeblichen IT-Support erreichen trotzdem die Menschen in Ihrem Unternehmen. Ob daraus ein Schaden wird, entscheidet sich oft in wenigen Sekunden.",
      "Ich richte für Sie ein Awareness-Programm auf einer Lernplattform ein. Ihre Mitarbeitenden bekommen kurze Lerneinheiten, die sie am eigenen Rechner bearbeiten, wann es in den Arbeitstag passt. Präsenztermine sind nicht nötig.",
      "Phishing-Simulationen zeigen, ob das Gelernte ankommt. In festen Abständen gehen realistische, aber harmlose Test-Mails raus. Wer klickt, sieht sofort einen kurzen Hinweis, woran er die Mail hätte erkennen können. Die Auswertungen zeigen Ihnen, in welchen Bereichen nachgeschult werden sollte.",
      "Fällt Ihr Unternehmen unter NIS2, muss auch die Geschäftsleitung regelmäßig geschult werden. Das lässt sich mit eigenen Lerninhalten für Führungskräfte abdecken und über die Plattform nachweisen.",
    ],
    get=["Auswahl und Einrichtung einer passenden Lernplattform",
         "Einen Schulungsplan mit kurzen Online-Einheiten für alle Mitarbeitenden",
         "Regelmäßige Phishing-Simulationen mit sofortigem Hinweis bei einem Klick",
         "Auswertungen, die zeigen, wo nachgeschult werden sollte",
         "Nachweise für Kunden, Versicherer und Auditoren"],
    steps=[("Ausgangslage", "Wir klären, wie viele Mitarbeitende teilnehmen, welche Themen wichtig sind und ob es einen Betriebsrat gibt."),
           ("Einrichtung", "Ich richte die Plattform ein, stimme Inhalte und Zeitplan mit Ihnen ab und bereite die Ankündigung im Unternehmen vor."),
           ("Laufender Betrieb", "Lerneinheiten und Phishing-Simulationen laufen in festen Abständen. Ich behalte die Ergebnisse im Blick."),
           ("Auswertung", "Sie bekommen regelmäßig einen kurzen Bericht mit Empfehlungen, wo nachgesteuert werden sollte.")],
    faq=[("Sind Phishing-Simulationen rechtlich erlaubt?", "Ja, wenn sie sauber vorbereitet sind. Die Mitarbeitenden werden vorab über das Programm informiert, ausgewertet wird in der Regel nach Abteilungen und nicht nach Personen, und ein vorhandener Betriebsrat wird beteiligt. Die Abstimmung mit Ihrem Datenschutzbeauftragten gehört dazu."),
         ("Wie viel Zeit kostet das die Mitarbeitenden?", "Die Lerneinheiten dauern meist nur wenige Minuten und verteilen sich über das Jahr. Niemand fehlt dafür einen halben Tag."),
         ("Welche Software wird eingesetzt?", "Das hängt von Größe, Budget und Ihren Anforderungen ab. Ich empfehle eine Lösung, die zu Ihrem Unternehmen passt, und achte dabei auf Datenschutz und Serverstandort.")]),
  dict(slug="notfallmanagement", title="Notfall- und Krisenmanagement",
    desc="Notfall- und Krisenmanagement für den Mittelstand: Business-Impact-Analyse, Notfallplan für Ransomware und IT-Ausfall, Notfallübungen. München und bundesweit.",
    lead="Was passiert, wenn morgen alle Rechner verschlüsselt sind? Mit einem Notfallplan wissen Sie vorher, was zu tun ist.",
    about=[
      "Nach einem Ransomware-Angriff oder einem längeren IT-Ausfall zählt jede Stunde. Wer muss informiert werden? Welche Abläufe müssen zuerst wieder laufen? Wo liegt die letzte saubere Sicherung, und wie lange dauert die Wiederherstellung? Wer diese Fragen erst im Ernstfall klärt, verliert Zeit und meist auch Geld.",
      "Am Anfang steht eine Business-Impact-Analyse. Für jeden wichtigen Geschäftsprozess legen wir fest, wie lange er ausfallen darf und wie viele Daten im schlimmsten Fall verloren gehen dürfen. Daraus ergibt sich, welche Systeme zuerst wiederhergestellt werden und welche Sicherungen Sie dafür brauchen.",
      "Der Notfallplan selbst passt auf wenige Seiten: Ansprechpartner und Erreichbarkeiten, Meldeketten, erste Schritte und die Reihenfolge des Wiederanlaufs. Er liegt auch auf Papier vor, denn im Ernstfall funktioniert das Netzwerk vielleicht nicht. Eine Übung zeigt, ob der Plan in der Praxis trägt.",
      "Für Unternehmen unter NIS2 gelten feste Meldefristen. Spätestens 24 Stunden, nachdem Sie von einem erheblichen Sicherheitsvorfall erfahren haben, ist eine Frühwarnung an das BSI fällig. Innerhalb von 72 Stunden folgt die eigentliche Meldung mit einer ersten Bewertung, spätestens einen Monat danach der Abschlussbericht. Diese Meldewege gehören direkt in den Plan.",
    ],
    get=["Eine Business-Impact-Analyse für Ihre wichtigsten Geschäftsprozesse",
         "Wiederanlaufzeiten und die Reihenfolge der Wiederherstellung",
         "Einen kompakten Notfallplan mit Meldeketten und Kontakten",
         "Eine Notfallübung, zum Beispiel am Szenario Ransomware",
         "Bei NIS2 die passenden Meldewege und Fristen"],
    steps=[("Analyse", "Gemeinsam mit den Verantwortlichen bewerten wir Ihre Geschäftsprozesse und legen fest, was wie lange ausfallen darf."),
           ("Plan", "Ich erstelle den Notfallplan und stimme ihn mit Geschäftsführung und IT-Dienstleister ab."),
           ("Übung", "Wir spielen einen Ernstfall am Tisch durch. Lücken im Plan fallen dabei schnell auf."),
           ("Pflege", "Der Plan wird einmal im Jahr und nach jeder größeren Änderung überprüft.")],
    faq=[("Reicht nicht ein gutes Backup?", "Ein Backup ist die Grundlage. Es beantwortet aber nicht, wer entscheidet, wen Sie informieren und was zuerst wiederhergestellt wird. Das regelt der Notfallplan. Außerdem prüfen wir, ob sich das Backup im Ernstfall wirklich zurückspielen lässt."),
         ("Wie aufwendig ist eine Notfallübung?", "Eine Übung am Tisch dauert meist zwei bis drei Stunden. Die IT muss dafür nicht abgeschaltet werden."),
         ("Was ist eine Business-Impact-Analyse?", "Eine Bewertung, wie stark ein Ausfall Ihre Geschäftsprozesse trifft. Für jeden Prozess wird festgelegt, wie lange er ausfallen darf und wie viel Datenverlust tragbar ist. Sie ist die Grundlage jedes Notfallplans.")]),
  dict(slug="isms-zertifizierung", title="ISMS und Zertifizierung",
    desc="ISMS nach ISO 27001:2022 oder BSI IT-Grundschutz für den Mittelstand: schlanker Aufbau, internes Audit, Begleitung bis zur Zertifizierung, NIS2 bei Bedarf. München und bundesweit.",
    lead="Wenn Kunden einen Nachweis verlangen, führt oft kein Weg an ISO 27001 vorbei. Ich baue mit Ihnen ein Managementsystem auf, das im Alltag funktioniert und im Audit besteht.",
    about=[
      "Ein Informationssicherheits-Managementsystem, kurz ISMS, regelt, wie Ihr Unternehmen mit Informationssicherheit umgeht: wer zuständig ist, wie Risiken bewertet werden, welche Maßnahmen gelten und wie geprüft wird, ob sie wirken. ISO/IEC 27001:2022 ist der international anerkannte Standard dafür. Für öffentliche Auftraggeber kann BSI IT-Grundschutz der passende Weg sein.",
      "Viele ISMS scheitern daran, dass sie zu groß gebaut werden. Am Ende stehen Dutzende Dokumente, die niemand liest. Ich halte das System so schlank wie möglich: wenige, klare Richtlinien, eine Risikoanalyse, die Sie selbst fortschreiben können, und Abläufe, die zu Ihrer Größe passen.",
      "Als Werkzeug eignet sich die kostenlose ISMS-Suite. Sie zeigt, wie weit Sie für die Zertifizierung sind, und hält Risiken, Maßnahmen und Nachweise an einem Ort.",
      "Fällt Ihr Unternehmen unter NIS2, kümmern wir uns gleich mit um die Pflichten aus dem BSI-Gesetz: Registrierung beim BSI, Risikomanagement und Meldeprozess. Ein ISMS nach ISO 27001 deckt einen großen Teil davon ohnehin ab.",
    ],
    get=["Festlegung des Geltungsbereichs und eine Gap-Analyse zum Start",
         "Risikoanalyse und Erklärung zur Anwendbarkeit (SoA)",
         "Schlanke Richtlinien und Abläufe, die zu Ihrem Unternehmen passen",
         "Internes Audit und Managementbewertung",
         "Begleitung im Zertifizierungsaudit",
         "Bei Bedarf die Umsetzung der NIS2-Pflichten"],
    steps=[("Start", "Wir legen den Geltungsbereich fest und prüfen in einer Gap-Analyse, was schon vorhanden ist."),
           ("Aufbau", "Risikoanalyse, Richtlinien und Maßnahmen entstehen Schritt für Schritt, abgestimmt mit Ihrem Team."),
           ("Prüfung", "Ein internes Audit und die Managementbewertung zeigen, ob das System trägt. Offene Punkte werden vor dem Audit geschlossen."),
           ("Zertifizierung", "Eine akkreditierte Zertifizierungsstelle prüft in zwei Stufen. Ich begleite Sie durch beide Audits.")],
    faq=[("Wie lange dauert es bis zum Zertifikat?", "Für kleine und mittlere Unternehmen sind drei bis sechs Monate realistisch. Am meisten hängt davon ab, wie viel Zeit Ihr Team einbringen kann."),
         ("Stellen Sie das Zertifikat aus?", "Nein. Das Zertifikat vergibt eine akkreditierte Zertifizierungsstelle. Ich bereite Sie darauf vor und begleite Sie im Audit."),
         ("Wie lange gilt ein ISO-27001-Zertifikat?", "Drei Jahre. In dieser Zeit gibt es jährliche Überwachungsaudits, danach folgt eine Rezertifizierung.")]),
  dict(slug="externer-ciso", title="Externer CISO und ISB",
    desc="Externer CISO und Informationssicherheitsbeauftragter (ISB) in München und bundesweit: feste Betreuung für den Mittelstand zum monatlichen Festpreis, als Interim-Lösung oder dauerhaft.",
    lead="Sie brauchen jemanden, der die Informationssicherheit verantwortet, aber keine eigene Vollzeitstelle? Ich übernehme die Rolle, für eine Übergangszeit oder dauerhaft.",
    about=[
      "Für eine eigene Stelle als Informationssicherheitsbeauftragter oder CISO sind viele Unternehmen zu klein, oder die Stelle ist gerade nicht besetzt. Die Aufgaben bleiben trotzdem: Risiken im Blick behalten, Richtlinien aktuell halten, Vorfälle bewerten, der Geschäftsführung berichten und Fragen von Kunden und Auditoren beantworten.",
      "Als externer CISO oder Informationssicherheitsbeauftragter (ISB) übernehme ich diese Aufgaben mit einem festen Zeitkontingent pro Monat, als Interim-Lösung bis zur Besetzung einer eigenen Stelle oder dauerhaft. Vor Ort bin ich in München und Umgebung, alles andere läuft per Video. Sie haben einen Ansprechpartner, der Ihr Unternehmen kennt, und die Geschäftsführung bekommt regelmäßig einen kurzen Bericht zur Lage.",
      "Auf Wunsch begleite ich auch die Einführung einer zentralen Sicherheitsüberwachung (SIEM) oder die Zusammenarbeit mit einem externen Security Operations Center (SOC).",
      "Abgerechnet wird über einen monatlichen Festpreis. So wissen Sie vorher, was die Betreuung kostet.",
    ],
    get=["Einen festen Ansprechpartner für alle Fragen zur Informationssicherheit",
         "Laufende Pflege von Risikoanalyse, Richtlinien und Maßnahmen",
         "Bewertung von Sicherheitsvorfällen und Begleitung im Ernstfall",
         "Regelmäßige Berichte an die Geschäftsführung",
         "Antworten auf Sicherheitsfragebögen Ihrer Kunden",
         "Auf Wunsch Begleitung von SIEM und SOC"],
    steps=[("Kennenlernen", "Wir klären, welche Aufgaben anfallen und wie viel Zeit pro Monat sinnvoll ist."),
           ("Einarbeitung", "Ich verschaffe mir einen Überblick über Systeme, Dokumente und laufende Themen."),
           ("Laufende Betreuung", "Feste Termine, ein Ansprechpartner und ein kurzer Bericht an die Geschäftsführung in jedem Quartal."),
           ("Anpassung", "Ändert sich der Bedarf, passen wir das monatliche Kontingent an.")],
    faq=[("Was kostet ein externer CISO?", "Es gibt einen monatlichen Festpreis, der sich nach dem vereinbarten Zeitkontingent richtet. Den genauen Betrag nenne ich Ihnen nach dem Erstgespräch."),
         ("Was ist der Unterschied zwischen CISO und Informationssicherheitsbeauftragtem?", "Im Mittelstand meist nur der Titel. Beide verantworten die Informationssicherheit im Unternehmen. Der Titel CISO ist eher in größeren Organisationen üblich und stärker auf Strategie und Führung ausgerichtet."),
         ("Wie schnell reagieren Sie bei einem Vorfall?", "Das legen wir vorab fest. Im Notfallplan steht, wie ich erreichbar bin und wer in welcher Reihenfolge informiert wird.")]),
]

e = lambda t: html.escape(t, quote=False)
ARROW = '<svg aria-hidden="true"><use href="#i-arrow"/></svg>'

def page(i, s):
    url = f"{DOMAIN}/leistungen/{s['slug']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": s["title"], "description": s["lead"], "url": url,
         "areaServed": [{"@type": "City", "name": "München"}, {"@type": "Country", "name": "Deutschland"}],
         "provider": {"@type": "ProfessionalService", "name": BRAND, "url": DOMAIN + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Leistungen", "item": DOMAIN + "/#leistungen"},
            {"@type": "ListItem", "position": 3, "name": s["title"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]}]}
    others = "\n".join(
        f'        <li><a href="/leistungen/{o["slug"]}"><span><span class="ms-no">{j:02d}</span>{e(o["title"])}</span>{ARROW}</a></li>'
        for j, o in enumerate(S, 1) if o is not s)
    return f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(s["title"])} in München | {BRAND}</title>
  <meta name="description" content="{html.escape(s["desc"])}">
  <meta name="robots" content="index, follow">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="theme-color" content="#081326">
  <!-- Ersatz-CSP für Hosts ohne eigene Header; diese Seite braucht kein JavaScript. -->
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'none'; object-src 'none'; upgrade-insecure-requests">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/site.css">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{e(s["title"])} | {BRAND}">
  <meta property="og:description" content="{html.escape(s["lead"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<svg class="sprite" aria-hidden="true" focusable="false">
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</svg>

<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{BRAND}, zur Startseite"><span class="brand-word">CyberSec<span class="brand-accent">Check</span></span></a>
    <nav class="nav" aria-label="Hauptnavigation">
      <a href="/#leistungen">Leistungen</a>
      <a href="/#software">ISMS-Suite</a>
      <a href="/#faq">Fragen</a>
      <a href="/#kontakt">Kontakt</a>
      <a class="btn btn-sm" href="/#check">Cyber-Check</a>
    </nav>
  </div>
</header>

<main id="inhalt">
  <section class="sub-hero" aria-labelledby="page-title">
    <div class="wrap">
      <nav class="crumbs" aria-label="Brotkrumen"><a href="/">Startseite</a><span aria-hidden="true">/</span><a href="/#leistungen">Leistungen</a><span aria-hidden="true">/</span><span aria-current="page">{e(s["title"])}</span></nav>
      <span class="eyebrow">Leistung {i:02d}</span>
      <h1 id="page-title">{e(s["title"])}</h1>
      <p class="hero-sub">{e(s["lead"])}</p>
      <div class="actions">
        <a class="btn" href="/#kontakt">Erstgespräch anfragen {ARROW}</a>
        <a class="btn btn-line" href="/#check">Kostenloser Cyber-Check</a>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="about-title">
    <div class="wrap sub-grid">
      <div class="prose">
        <h2 id="about-title">Worum es geht</h2>
{chr(10).join(f"        <p>{e(p)}</p>" for p in s["about"])}
      </div>
      <aside class="deliver" aria-labelledby="get-title">
        <h2 id="get-title">Was Sie bekommen</h2>
        <ul class="checks">
{chr(10).join(f"          <li>{e(g)}</li>" for g in s["get"])}
        </ul>
      </aside>
    </div>
  </section>

  <section class="section mist" aria-labelledby="steps-title">
    <div class="wrap">
      <div class="head"><h2 id="steps-title">So läuft es ab</h2></div>
      <ol class="process">
{chr(10).join(f"        <li><h3>{e(t)}</h3><p>{e(p)}</p></li>" for t, p in s["steps"])}
      </ol>
    </div>
  </section>

  <section class="section" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="head head-c"><h2 id="faq-title">Häufige Fragen</h2></div>
      <div class="faq">
{chr(10).join(f"        <details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>" for q, a in s["faq"])}
      </div>
    </div>
  </section>

  <section class="section mist" aria-labelledby="more-title">
    <div class="wrap">
      <div class="head"><h2 id="more-title">Weitere Leistungen</h2></div>
      <ul class="more-services">
{others}
      </ul>
    </div>
  </section>

  <section class="cta-band" aria-labelledby="cta-title">
    <div class="wrap">
      <div>
        <h2 id="cta-title">Lassen Sie uns sprechen</h2>
        <p>30 Minuten, kostenlos und unverbindlich. Vor Ort in München und Umgebung oder per Video.</p>
      </div>
      <a class="btn" href="/#kontakt">Erstgespräch anfragen {ARROW}</a>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <span>© 2026 {BRAND} · Diese Seite setzt keine Tracking-Cookies.</span>
    <nav aria-label="Rechtliches"><a href="/impressum">Impressum</a><a href="/datenschutz">Datenschutz</a></nav>
  </div>
</footer>
</body>
</html>
'''

ORDER = ['isms-zertifizierung', 'externer-ciso', 'sicherheitsanalysen', 'notfallmanagement', 'security-awareness']
S.sort(key=lambda s: ORDER.index(s["slug"]))
os.makedirs(os.path.join(ROOT, "leistungen"), exist_ok=True)
for i, s in enumerate(S, 1):
    with open(os.path.join(ROOT, "leistungen", s["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page(i, s))
print("\n".join(s["slug"] for s in S))
