// Die 27 Anforderungen in sechs Themenfeldern, als eigene Kurzfassung angelehnt an
// DIN SPEC 27076. Vor dem Livegang gegen den Normtext prüfen (Nummerierung, TOP-Auswahl).
// top: TOP-Anforderung, zählt doppelt; eine offene TOP-Anforderung hebt das Risiko an.

export const FIELDS = [
  { key: "ORG", name: "Organisation & Sensibilisierung" },
  { key: "IDM", name: "Identitäts- & Berechtigungsmanagement" },
  { key: "DS", name: "Datensicherung & Protokollierung" },
  { key: "PAT", name: "Patch- & Änderungsmanagement" },
  { key: "SCH", name: "Schutz vor Schadprogrammen" },
  { key: "NET", name: "IT-Systeme & Netzwerke" },
];

const RAW = [
  ["ORG", "Gibt es eine benannte Person, die für IT-Sicherheit verantwortlich ist?", "Intern oder extern, mit Zeit und Rückendeckung der Geschäftsführung.", "Ohne klare Zuständigkeit bleibt IT-Sicherheit liegen. Das kann auch ein externer Dienstleister sein, wichtig ist, dass jemand es als Aufgabe hat."],
  ["ORG", "Gibt es schriftliche Regeln zur Nutzung der IT, die alle Mitarbeitenden kennen?", "Zum Beispiel zu Passwörtern, E-Mail, privaten Geräten und Homeoffice.", "Zwei Seiten reichen. Entscheidend ist, dass alle die Regeln kennen und bestätigt haben."],
  ["ORG", "Haben Sie eine aktuelle Übersicht über Ihre IT-Geräte, Programme und Cloud-Dienste?", "Inkl. der Dienstleister, die darauf Zugriff haben.", "Was Sie nicht kennen, können Sie nicht schützen. Eine gepflegte Tabelle ist ein guter Anfang."],
  ["ORG", "Werden Mitarbeitende regelmäßig zu Phishing und Betrugsmaschen geschult?", "Mindestens einmal im Jahr, auch neue Kolleginnen und Kollegen.", "Die meisten Angriffe beginnen mit einer E-Mail oder einem Anruf. Kurze, regelmäßige Schulungen wirken am besten."],
  ["ORG", "Sind externe IT-Dienstleister vertraglich zu Sicherheit und Vertraulichkeit verpflichtet?", "Inkl. Regelungen für Fernwartung und Datenschutz.", "Viele Angriffe laufen über Dienstleister mit Fernzugriff. Der Vertrag sollte Sicherheitspflichten und Meldewege regeln."],
  ["ORG", "Existiert ein dokumentierter Notfallplan für IT-Sicherheitsvorfälle (z. B. Ransomware)?", "Inkl. Meldeketten, Kontaktlisten und Wiederanlaufreihenfolge.", "Im Ernstfall zählt jede Stunde. Ein Plan auf Papier sagt, wer was tut, wen Sie anrufen und welche Systeme zuerst zurückkommen."],
  ["ORG", "Sind Laptops, Smartphones und mobile Datenträger verschlüsselt?", "Inkl. Regeln für den Verlust eines Geräts.", "Ein verlorener, unverschlüsselter Laptop kann eine meldepflichtige Datenpanne nach DSGVO sein."],
  ["IDM", "Hat jede Person ein eigenes Benutzerkonto, ohne geteilte Zugänge?", "Auch für Kasse, Maschinen und Cloud-Dienste.", "Geteilte Konten machen es unmöglich nachzuvollziehen, wer was getan hat, und sie werden selten geändert."],
  ["IDM", "Gibt es Vorgaben für sichere Passwörter oder einen Passwortmanager?", "Lange Passwörter, keine Mehrfachnutzung.", "Ein Passwortmanager ist der einfachste Weg zu langen, einzigartigen Passwörtern für jeden Dienst."],
  ["IDM", "Ist für E-Mail, Fernzugriff und Cloud-Dienste eine Mehrfaktor-Anmeldung aktiv?", "Zum Beispiel per App oder Sicherheitsschlüssel.", "Gestohlene Passwörter sind einer der häufigsten Einstiege. Ein zweiter Faktor stoppt die meisten dieser Angriffe.", true],
  ["IDM", "Werden Administratorrechte nur für Verwaltungsaufgaben und mit eigenen Konten genutzt?", "Im Alltag wird mit normalen Rechten gearbeitet.", "Wer mit Adminrechten im Internet surft, gibt Schadsoftware im Ernstfall die Schlüssel zum ganzen Netz."],
  ["IDM", "Werden Zugänge beim Austritt sofort entzogen und Berechtigungen regelmäßig geprüft?", "Inkl. Cloud-Konten und Fernzugänge.", "Vergessene Konten ehemaliger Mitarbeitender sind offene Türen, die niemand beobachtet."],
  ["DS", "Werden alle wichtigen Daten regelmäßig und automatisch gesichert?", "Server, Cloud-Daten, E-Mails und Buchhaltung.", "Ohne Backup kann ein Defekt oder ein Angriff Ihre Daten endgültig zerstören.", true],
  ["DS", "Wird mindestens eine Sicherung getrennt vom Netz oder unveränderbar aufbewahrt?", "Zum Beispiel offline, außer Haus oder in einem unveränderbaren Speicher.", "Ransomware verschlüsselt alles, was sie erreichen kann, auch Backups im selben Netz.", true],
  ["DS", "Wird die Wiederherstellung aus der Sicherung regelmäßig getestet?", "Mindestens einmal im Jahr.", "Viele merken erst im Ernstfall, dass ihr Backup unvollständig ist oder die Wiederherstellung Tage dauert."],
  ["DS", "Werden Protokolle wichtiger Systeme gespeichert und bei Auffälligkeiten ausgewertet?", "Zum Beispiel Anmeldeversuche an Firewall, Server und Cloud.", "Ohne Protokolle bleibt ein Angriff oft wochenlang unbemerkt und lässt sich später nicht aufklären."],
  ["PAT", "Werden Betriebssysteme und Programme zeitnah, möglichst automatisch aktualisiert?", "Kritische Sicherheitslücken innerhalb weniger Tage.", "Angreifer nutzen bekannte Lücken oft schon wenige Tage nach Veröffentlichung automatisiert aus.", true],
  ["PAT", "Werden Geräte und Programme ersetzt, für die es keine Sicherheitsupdates mehr gibt?", "Zum Beispiel alte Windows-Versionen oder Router.", "Für veraltete Systeme werden Lücken nicht mehr geschlossen. Sie sind ein dauerhaftes Einfallstor."],
  ["PAT", "Werden Änderungen an der IT geplant, getestet und dokumentiert?", "Zum Beispiel neue Software, Umbauten im Netz.", "Ungeplante Änderungen sind eine häufige Ursache für Ausfälle und Sicherheitslücken."],
  ["SCH", "Ist auf allen Geräten ein aktueller Virenschutz aktiv?", "Inkl. Servern und Laptops im Homeoffice.", "Ein aktueller Virenschutz erkennt bekannte Schadsoftware, bevor sie Schaden anrichtet.", true],
  ["SCH", "Werden E-Mails auf Spam, Phishing und gefährliche Anhänge gefiltert?", "Beim Anbieter oder auf dem eigenen Server.", "Ein guter Filter hält einen Großteil der gefährlichen E-Mails ab, bevor jemand darauf klicken kann."],
  ["SCH", "Ist das Ausführen von Makros und unbekannten Programmen eingeschränkt?", "Zum Beispiel Office-Makros aus dem Internet blockiert.", "Makros in Office-Dokumenten sind ein klassischer Weg, Schadsoftware einzuschleusen."],
  ["NET", "Schützt eine Firewall Ihr Netz zum Internet, mit nur den nötigen Freigaben?", "Regeln werden regelmäßig überprüft.", "Die Firewall ist die Haustür Ihres Netzes. Jede unnötige Freigabe ist ein offenes Fenster.", true],
  ["NET", "Ist Ihr WLAN verschlüsselt und ein Gästenetz vom Firmennetz getrennt?", "Mindestens WPA2, besser WPA3.", "Gäste und private Geräte gehören nicht ins selbe Netz wie Ihre Server und Buchhaltung."],
  ["NET", "Erfolgt Fernzugriff nur über eine gesicherte Verbindung (VPN)?", "Kein direkt erreichbarer Remote-Desktop.", "Offen erreichbarer Remote-Desktop ist eines der häufigsten Ziele automatisierter Angriffe."],
  ["NET", "Wurden Standardpasswörter geändert und nicht benötigte Dienste abgeschaltet?", "Bei Routern, Druckern, Kameras und Servern.", "Standardpasswörter stehen öffentlich im Handbuch und werden automatisiert ausprobiert."],
  ["NET", "Sind Server und Netzwerktechnik vor unbefugtem Zugang geschützt?", "Zum Beispiel ein abschließbarer Raum oder Schrank.", "Wer physisch an den Server kommt, kann fast jede technische Schutzmaßnahme umgehen."],
];

const counters = {};
export const QUESTIONS = RAW.map(([field, text, sub, help, top]) => {
  counters[field] = (counters[field] || 0) + 1;
  return Object.freeze({ field, id: `${field}.${counters[field]}`, text, sub, help, top: Boolean(top) });
});

export const ANSWERS = [
  { value: 2, label: "Ja" },
  { value: 1, label: "Teilweise" },
  { value: 0, label: "Nein" },
];

export const LEVELS = {
  ok: { label: "Niedriges Risiko", text: "Die Grundlagen stehen. Der nächste Schritt ist, das nachweisbar zu machen, etwa für Kunden oder Versicherer." },
  warn: { label: "Erhöhtes Risiko", text: "Einiges ist umgesetzt, aber es gibt Lücken, die Angreifer typischerweise ausnutzen. Die wichtigsten lassen sich meist in wenigen Wochen schließen." },
  crit: { label: "Hohes Risiko", text: "Grundlegende Schutzmaßnahmen fehlen. Ein Angriff könnte Ihren Betrieb tagelang lahmlegen. Fangen Sie mit den Punkten unten an." },
};

/** Reine Funktion: Antworten rein, Ergebnis raus. Testbar ohne DOM. */
export function evaluate(answers) {
  let got = 0, max = 0, topOpen = 0;
  const per = Object.fromEntries(FIELDS.map((f) => [f.key, { got: 0, max: 0 }]));
  const gaps = [];
  for (const q of QUESTIONS) {
    const weight = q.top ? 2 : 1;
    const value = [0, 1, 2].includes(answers[q.id]) ? answers[q.id] : 0;
    got += value * weight; max += 2 * weight;
    per[q.field].got += value * weight; per[q.field].max += 2 * weight;
    if (value < 2) gaps.push({ q, loss: (2 - value) * weight });
    if (q.top && value === 0) topOpen++;
  }
  gaps.sort((a, b) => b.loss - a.loss);
  const score = Math.round((got / max) * 100);
  const level = score >= 80 && topOpen === 0 ? "ok" : score >= 50 && topOpen <= 1 ? "warn" : "crit";
  const fields = FIELDS.map((f) => ({ ...f, pct: Math.round((per[f.key].got / per[f.key].max) * 100) }));
  return { score, level, fields, gaps, topOpen };
}

export function levelOf(pct) { return pct >= 80 ? "ok" : pct >= 50 ? "warn" : "crit"; }
