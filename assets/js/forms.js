// Lead- und Kontaktformular: strikte Prüfung im Browser, Versand als JSON.
// Die Prüfung hier ist Komfort, keine Sicherheit: der Server prüft alles noch
// einmal (siehe server/lead-endpoint.example.mjs) und vertraut dem Browser nie.

const RULES = {
  name: { required: true, max: 80, pattern: /^[\p{L}][\p{L}\p{M} .'-]{1,79}$/u, msg: "Bitte geben Sie Ihren Namen an (nur Buchstaben, Leerzeichen, Punkt, Bindestrich)." },
  company: { required: false, max: 120, pattern: /^[\p{L}\p{N}][\p{L}\p{N}\p{M} .,&()'/+-]{0,119}$/u, msg: "Der Firmenname enthält unzulässige Zeichen." },
  email: { required: true, max: 254, pattern: /^[^\s@<>()[\]\\,;:"]{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$/, msg: "Bitte prüfen Sie die E-Mail-Adresse, sie scheint unvollständig zu sein." },
  message: { required: false, max: 2000, msg: "Die Nachricht darf höchstens 2000 Zeichen lang sein." },
};
const MIN_FILL_MS = 2500; // Bots schicken Formulare in Millisekunden ab

/** Unicode normalisieren, Steuerzeichen entfernen (Zeilenumbrüche nur in der Nachricht). */
function clean(value, multiline) {
  const s = String(value || "").normalize("NFC");
  return (multiline ? s.replace(/[^\P{C}\n]/gu, "") : s.replace(/\p{C}/gu, "")).trim();
}

/** Nur relative Pfade derselben Herkunft, damit niemand das Ziel umbiegen kann. */
function endpoint() {
  const value = document.querySelector('meta[name="lead-endpoint"]')?.content || "";
  return /^\/(?!\/)[\w\-/]*$/.test(value) ? value : null;
}

function csrfToken() {
  return document.querySelector('meta[name="csrf-token"]')?.content || "";
}

/**
 * Bindet ein Formular. extra() liefert zusätzliche, nicht vom Nutzer getippte Daten
 * (z. B. die Check-Auswertung), die mitgeschickt werden.
 */
export function bindLeadForm(form, { extra = () => ({}), source = "kontakt" } = {}) {
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

    const data = {};
    let firstInvalid = null;
    for (const [name, rule] of Object.entries(RULES)) {
      const input = form.elements.namedItem(name);
      if (!input) continue;
      const value = clean(input.value, name === "message");
      input.value = value;
      const invalid = (rule.required && !value) || value.length > rule.max || (value && rule.pattern && !rule.pattern.test(value));
      input.setAttribute("aria-invalid", String(Boolean(invalid)));
      if (invalid && !firstInvalid) firstInvalid = { input, msg: rule.msg };
      data[name] = value;
    }
    if (firstInvalid) { say(firstInvalid.msg, true); firstInvalid.input.focus(); return; }

    const consent = form.elements.namedItem("consent");
    if (!consent.checked) { say("Bitte bestätigen Sie die Einwilligung, damit ich Ihre Anfrage bearbeiten darf.", true); consent.focus(); return; }

    // Honeypot gefüllt oder zu schnell: still verwerfen, Bots bekommen keine Rückmeldung.
    if (form.elements.namedItem("website")?.value || Date.now() - startedAt < MIN_FILL_MS) {
      say("Danke, Ihre Anfrage ist angekommen.");
      form.reset();
      return;
    }

    const url = endpoint();
    if (!url) { say("Das Formular ist noch nicht angebunden. Bitte schreiben Sie mir direkt per E-Mail.", true); return; }

    submit.disabled = true;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
        body: JSON.stringify({ ...data, consent: true, source, ...extra() }),
        signal: controller.signal,
      });
      if (!response.ok) throw new Error(String(response.status));
      say("Danke, Ihre Anfrage ist angekommen. Ich melde mich innerhalb von zwei Werktagen.");
      form.reset();
    } catch {
      say("Die Anfrage konnte gerade nicht gesendet werden. Bitte schreiben Sie mir direkt per E-Mail, die Adresse steht unten auf der Seite.", true);
    } finally {
      clearTimeout(timer);
      submit.disabled = false;
    }
  });
}
