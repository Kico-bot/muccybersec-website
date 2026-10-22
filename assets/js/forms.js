// Kontaktformular: strikte Prüfung im Browser, Versand an den Cloudflare Worker.
// Die Prüfung hier ist Komfort, keine Sicherheit: der Worker muss jede Eingabe selbst
// prüfen und darf dem Browser nie vertrauen (siehe README, Abschnitt Kontaktformular).
//
// Ohne JavaScript schickt der Browser das Formular ganz normal an action= ab.
// Mit JavaScript geht es im Hintergrund als einfacher POST (application/x-www-form-urlencoded,
// keine eigenen Header), damit der Browser keine CORS-Vorabanfrage stellt.

const RULES = {
  name: { required: true, max: 80, pattern: /^[\p{L}][\p{L}\p{M} .'-]{1,79}$/u, msg: "Bitte geben Sie Ihren Namen an (nur Buchstaben, Leerzeichen, Punkt, Bindestrich)." },
  email: { required: true, max: 254, pattern: /^[^\s@<>()[\]\\,;:"]{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$/, msg: "Bitte prüfen Sie die E-Mail-Adresse, sie scheint unvollständig zu sein." },
  subject: { required: false, max: 150, msg: "Der Betreff darf höchstens 150 Zeichen lang sein." },
  message: { required: true, max: 2000, msg: "Bitte schreiben Sie kurz, worum es geht (höchstens 2000 Zeichen)." },
};
const MIN_FILL_MS = 2500; // Bots schicken Formulare in Millisekunden ab

// Nur diese Ziele sind erlaubt, damit niemand das Formular per manipuliertem action= umleitet.
const ALLOWED_HOSTS = ["contact-form.kristian95.workers.dev"];

/** Unicode normalisieren, Steuerzeichen entfernen (Zeilenumbrüche nur in der Nachricht). */
function clean(value, multiline) {
  const s = String(value || "").normalize("NFC");
  return (multiline ? s.replace(/[^\P{C}\n]/gu, "") : s.replace(/\p{C}/gu, "")).trim();
}

function endpoint(form) {
  try {
    const url = new URL(form.getAttribute("action"), location.href);
    return url.protocol === "https:" && ALLOWED_HOSTS.includes(url.hostname) ? url.href : null;
  } catch {
    return null;
  }
}

export function bindLeadForm(form) {
  const status = form.querySelector("[data-status]");
  const submit = form.querySelector('button[type="submit"]');
  const startedAt = Date.now();

  const say = (text, isError) => {
    status.hidden = false;
    status.textContent = text;
    status.classList.toggle("error", Boolean(isError));
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (submit.disabled) return; // kein doppelter Versand

    const data = new URLSearchParams();
    let firstInvalid = null;
    for (const [name, rule] of Object.entries(RULES)) {
      const input = form.elements.namedItem(name);
      if (!input) continue;
      const value = clean(input.value, name === "message");
      input.value = value;
      const invalid = (rule.required && !value) || value.length > rule.max || (value && rule.pattern && !rule.pattern.test(value));
      input.setAttribute("aria-invalid", String(Boolean(invalid)));
      if (invalid && !firstInvalid) firstInvalid = { input, msg: rule.msg };
      if (value) data.set(name, value);
    }
    if (firstInvalid) { say(firstInvalid.msg, true); firstInvalid.input.focus(); return; }

    const consent = form.elements.namedItem("consent");
    if (consent && !consent.checked) { say("Bitte bestätigen Sie die Einwilligung, damit ich Ihre Anfrage bearbeiten darf.", true); consent.focus(); return; }

    // Honeypot gefüllt oder zu schnell: still verwerfen, Bots bekommen keine Rückmeldung.
    if (form.elements.namedItem("website")?.value || Date.now() - startedAt < MIN_FILL_MS) {
      say("Danke, Ihre Nachricht ist angekommen.");
      form.reset();
      return;
    }

    const url = endpoint(form);
    if (!url) { say("Das Formular ist gerade nicht erreichbar. Bitte schreiben Sie mir direkt per E-Mail.", true); return; }

    submit.disabled = true;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(url, { method: "POST", body: data, signal: controller.signal, credentials: "omit", referrerPolicy: "strict-origin-when-cross-origin" });
      if (!response.ok) throw new Error(String(response.status));
      say("Danke, Ihre Nachricht ist angekommen. Ich melde mich innerhalb von zwei Werktagen.");
      form.reset();
    } catch (error) {
      // Ein TypeError kann zweierlei heißen: Der Worker sendet keine CORS-Freigabe (Nachricht kam
      // an, die Antwort ist nur gesperrt) oder die Anfrage wurde gar nicht erst gesendet (Netz, CSP).
      // Beides lässt sich im Browser nicht unterscheiden, deshalb eine vorsichtige Meldung.
      const unclear = error instanceof TypeError;
      say(unclear
        ? "Ich konnte nicht bestätigen, dass Ihre Nachricht angekommen ist. Bitte schreiben Sie mir zur Sicherheit direkt per E-Mail."
        : "Die Nachricht konnte gerade nicht gesendet werden. Bitte versuchen Sie es später noch einmal oder schreiben Sie mir direkt per E-Mail.", true);
    } finally {
      clearTimeout(timer);
      submit.disabled = false;
    }
  });
}
