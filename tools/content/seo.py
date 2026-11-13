# Suchoptimierung der bestehenden Artikel, an einer Stelle gesammelt: Titel nach echten Suchanfragen
# (Search Console), Tabellen aus Fakten, die im Artikel schon stehen, und die SoA-Vorlage zum Download.
from content.ratgeber import NIS2_BETROFFEN, NIS2_MELDUNG
from content.ratgeber_mehr import SOA
from content.ratgeber_mapping import NIS2_DSGVO

UPDATED = "2026-11-13"
SOA_CSV = "/downloads/soa-vorlage-iso-27001.csv"


def insert_after(article, starts_with, extra):
    """Fügt Blöcke hinter dem ersten Block ein, dessen Text mit starts_with beginnt."""
    for i, (kind, val) in enumerate(article["body"]):
        if isinstance(val, str) and val.startswith(starts_with):
            article["body"][i + 1:i + 1] = extra
            article["updated"] = UPDATED
            return
    raise ValueError(f"{article['slug']}: kein Block beginnt mit {starts_with!r}")


# --- Erklärung zur Anwendbarkeit: Suchanfragen „anwendbarkeitserklärung“, „statement of applicability erstellen“
SOA.update(
    keyword="Anwendbarkeitserklärung erstellen",
    title="Anwendbarkeitserklärung (SoA) erstellen + Vorlage | CyberSecCheck",
    desc="Die Erklärung zur Anwendbarkeit nach ISO 27001 erstellen: was hineingehört, wie Sie die 93 Maßnahmen aus Anhang A begründen. Mit kostenloser Vorlage.",
    h1="Erklärung zur Anwendbarkeit (SoA) erstellen: Anleitung und Vorlage",
    lead="Die Erklärung zur Anwendbarkeit, auch Anwendbarkeitserklärung, englisch Statement of Applicability oder kurz SoA, ist eines der wichtigsten Dokumente eines ISMS nach ISO 27001. Jeder Auditor schaut sie sich an. Was hineingehört, wie Sie sie schlank halten, und eine kostenlose Vorlage zum Start.",
)
SOA["key"] = SOA["key"] + [f"Eine kostenlose Vorlage mit allen 93 Maßnahmen gibt es [hier als CSV-Datei]({SOA_CSV})."]
insert_after(SOA, "In der Praxis ist eine Tabelle mit einer Zeile je Maßnahme üblich.", [
    ("table", dict(
        caption="So kann eine Zeile der SoA aussehen",
        head=["Spalte", "Beispiel"],
        rows=[["Nummer und Maßnahme", "8.13 Datensicherung"],
              ["Anwendbar", "Ja"],
              ["Begründung", "Risiko R-03: Verlust der Auftragsdaten durch Ransomware"],
              ["Umsetzungsstand", "Umgesetzt"],
              ["Nachweis", "Richtlinie Datensicherung v1.2, Protokoll des Wiederherstellungstests"],
              ["Verantwortlich", "IT-Leitung"]])),
    ("h2", "Kostenlose Vorlage für die SoA"),
    ("p", f"Als Startpunkt können Sie unsere [SoA-Vorlage als CSV-Datei]({SOA_CSV}) herunterladen. Sie enthält alle 93 Maßnahmen aus Anhang A der ISO/IEC 27001:2022 mit Nummer, Thema und den Spalten aus der Tabelle oben. Die Datei öffnet sich in Excel, LibreOffice und Numbers."),
    ("note", "Die Themen in der Vorlage sind kurze, eigene Umschreibungen, damit Sie die Zeilen zuordnen können. Sie ersetzen nicht den Wortlaut der Norm, den Sie für die Begründungen neben sich haben sollten."),
])

# --- NIS2-Betroffenheit: Schwellenwerte als Tabelle
insert_after(NIS2_BETROFFEN, "Die Schwellenwerte regelt § 28 BSIG.", [
    ("table", dict(
        caption="Die zwei Kategorien nach § 28 BSIG im Überblick",
        head=["Kategorie", "Sektor", "Beschäftigte", "oder Umsatz und Bilanzsumme"],
        rows=[["Besonders wichtige Einrichtung", "Anlage 1", "ab 250", "über 50 Mio. € Umsatz und über 43 Mio. € Bilanzsumme"],
              ["Wichtige Einrichtung", "Anlage 1 oder 2", "ab 50", "je über 10 Mio. € Umsatz und Bilanzsumme"]])),
])

# --- NIS2-Meldepflichten: Fristen als Tabelle
insert_after(NIS2_MELDUNG, "Beachten Sie den Unterschied: Die 24 und die 72 Stunden", [
    ("table", dict(
        caption="Die Meldefristen nach § 32 BSIG",
        head=["Meldung", "Frist", "Fristbeginn", "Inhalt (Auszug)"],
        rows=[["Frühwarnung", "24 Stunden", "Kenntnis des Vorfalls", "Verdacht auf böswillige Handlung, mögliche grenzüberschreitende Auswirkungen"],
              ["Meldung", "72 Stunden", "Kenntnis des Vorfalls", "erste Bewertung von Schweregrad und Auswirkungen, Kompromittierungsindikatoren"],
              ["Zwischenmeldung", "auf Ersuchen des BSI", "Anforderung durch das BSI", "relevante Statusänderungen"],
              ["Abschlussmeldung", "1 Monat", "72-Stunden-Meldung", "ausführliche Beschreibung, Ursache, Abhilfemaßnahmen"]])),
])

# --- NIS2 und DSGVO: der Vergleich als Tabelle
insert_after(NIS2_DSGVO, "Ein Vorfall kann unter beide Regeln fallen", [
    ("table", dict(
        caption="NIS2 und DSGVO: die Meldepflichten im Vergleich",
        head=["", "NIS2", "DSGVO"],
        rows=[["Schützt", "die Dienste des Unternehmens", "die betroffenen Menschen"],
              ["Meldung an", "BSI (§ 32 BSIG)", "Datenschutzaufsicht (Art. 33 DSGVO)"],
              ["Meldeschwelle", "erheblicher Sicherheitsvorfall", "jede Verletzung, außer bei voraussichtlich keinem Risiko"],
              ["Erste Meldung", "Frühwarnung nach 24 Stunden", "möglichst binnen 72 Stunden"],
              ["Weitere Meldungen", "nach 72 Stunden und nach einem Monat", "Informationen dürfen schrittweise nachgereicht werden"]])),
])


# --- Anhang A der ISO/IEC 27001:2022: Nummern mit eigenen Kurzumschreibungen (nicht der Normtext)
ANNEX_A = [("Organisatorisch", "5", [
    "Leitlinie und Richtlinien zur Informationssicherheit", "Rollen und Zuständigkeiten", "Trennung unvereinbarer Aufgaben",
    "Pflichten der Leitung", "Kontakt zu Behörden", "Kontakt zu Fachgruppen und Verbänden", "Informationen über Bedrohungen",
    "Sicherheit in Projekten", "Verzeichnis der Informationen und Werte", "Regeln zur Nutzung von Informationen und Werten",
    "Rückgabe von Werten", "Einstufung von Informationen", "Kennzeichnung von Informationen", "Übermittlung von Informationen",
    "Regeln für Zugang und Zugriff", "Verwaltung von Identitäten", "Umgang mit Passwörtern und anderen Anmeldedaten",
    "Vergabe, Prüfung und Entzug von Berechtigungen", "Sicherheit bei Lieferanten", "Sicherheitsanforderungen in Lieferantenverträgen",
    "Sicherheit in der IT-Lieferkette", "Überwachung von Lieferantenleistungen", "Sicherheit bei Cloud-Diensten",
    "Vorbereitung auf Sicherheitsvorfälle", "Bewertung von Sicherheitsereignissen", "Reaktion auf Sicherheitsvorfälle",
    "Lernen aus Sicherheitsvorfällen", "Sicherung von Beweisen", "Informationssicherheit bei Störungen und Krisen",
    "IT-Vorsorge für den Notbetrieb", "Gesetzliche und vertragliche Anforderungen", "Schutz geistigen Eigentums",
    "Schutz von Aufzeichnungen", "Datenschutz und personenbezogene Daten", "Unabhängige Prüfung der Informationssicherheit",
    "Einhaltung der eigenen Regeln und Standards", "Dokumentierte Betriebsabläufe"]),
    ("Personenbezogen", "6", [
    "Überprüfung bei der Einstellung", "Sicherheitspflichten im Arbeitsvertrag", "Sensibilisierung und Schulung",
    "Umgang mit Verstößen", "Pflichten nach Ende oder Wechsel der Beschäftigung", "Vertraulichkeitsvereinbarungen",
    "Arbeiten außerhalb des Büros", "Meldung von Sicherheitsereignissen durch Beschäftigte"]),
    ("Physisch", "7", [
    "Sicherheitszonen und Gebäudegrenzen", "Zutrittskontrolle", "Schutz von Büros und Räumen", "Überwachung der Gebäude",
    "Schutz vor Feuer, Wasser und anderen Umwelteinflüssen", "Regeln für Sicherheitsbereiche",
    "Aufgeräumter Schreibtisch und Bildschirmsperre", "Aufstellung und Schutz von Geräten",
    "Geräte und Werte außerhalb des Unternehmens", "Umgang mit Datenträgern", "Strom, Klima und andere Versorgung",
    "Schutz der Verkabelung", "Wartung von Geräten", "Sichere Entsorgung und Wiederverwendung von Geräten"]),
    ("Technologisch", "8", [
    "Endgeräte der Nutzer", "Administrative Berechtigungen", "Beschränkung des Zugriffs auf Informationen", "Zugriff auf Quellcode",
    "Sichere Anmeldung", "Kapazitätsplanung", "Schutz vor Schadsoftware", "Umgang mit technischen Schwachstellen",
    "Verwaltung von Konfigurationen", "Löschen von Informationen", "Maskierung von Daten", "Verhinderung von Datenabfluss",
    "Datensicherung", "Redundanz von Systemen", "Protokollierung", "Überwachung auf Auffälligkeiten", "Zeitsynchronisation",
    "Einsatz mächtiger Hilfsprogramme", "Installation von Software auf Produktivsystemen", "Sicherheit von Netzwerken",
    "Sicherheit von Netzwerkdiensten", "Segmentierung von Netzwerken", "Filterung von Webzugriffen", "Einsatz von Verschlüsselung",
    "Sichere Softwareentwicklung", "Sicherheitsanforderungen an Anwendungen", "Grundsätze für sichere Systemarchitektur",
    "Sicheres Programmieren", "Sicherheitstests in Entwicklung und Abnahme", "Ausgelagerte Entwicklung",
    "Trennung von Entwicklung, Test und Betrieb", "Änderungsmanagement", "Testdaten", "Schutz von Systemen bei Audit-Prüfungen"]),
]
assert sum(len(x[2]) for x in ANNEX_A) == 93

SOA_COLUMNS = ["Nr.", "Thema (Kurzumschreibung)", "Kategorie", "Anwendbar (ja/nein)", "Begründung für Einbeziehung oder Ausschluss",
               "Risiko oder Anforderung", "Umsetzungsstand (umgesetzt/teilweise/geplant/nein)", "Nachweis oder Verweis", "Verantwortlich"]


def soa_csv():
    """Semikolon und UTF-8 mit BOM, damit Excel mit deutscher Einstellung Umlaute und Spalten richtig liest."""
    def cell(s):
        return '"' + s.replace('"', '""') + '"' if any(c in s for c in ';"\n') else s
    rows = [SOA_COLUMNS] + [[f"{prefix}.{i}", topic, cat] + [""] * (len(SOA_COLUMNS) - 3)
                            for cat, prefix, topics in ANNEX_A for i, topic in enumerate(topics, 1)]
    return "﻿" + "\r\n".join(";".join(cell(c) for c in r) for r in rows) + "\r\n"
