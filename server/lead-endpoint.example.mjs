// Referenz für den Formular-Endpunkt POST /api/lead. Node 20+, keine Abhängigkeiten.
// Start zum Ausprobieren:  ALLOWED_ORIGIN=http://localhost:8080 CSRF_SECRET=$(openssl rand -hex 32) node server/lead-endpoint.example.mjs
//
// Grundsatz: Der Browser ist nicht vertrauenswürdig. Alles, was forms.js prüft, wird hier
// noch einmal und strenger geprüft. Eingaben werden nie zurückgegeben, nie als HTML
// ausgegeben und nie in SQL oder Shell-Befehle eingesetzt.

import { createServer } from "node:http";
import { createHmac, timingSafeEqual } from "node:crypto";

const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || "https://www.ihre-domain.de";
const CSRF_SECRET = process.env.CSRF_SECRET || "";
const MAX_BODY = 8 * 1024;             // 8 KB reichen für jedes legitime Formular
const RATE = { windowMs: 10 * 60e3, max: 5 }; // 5 Anfragen je IP in 10 Minuten

const RULES = {
  name: { required: true, max: 80, pattern: /^[\p{L}][\p{L}\p{M} .'-]{1,79}$/u },
  company: { required: false, max: 120, pattern: /^[\p{L}\p{N}][\p{L}\p{N}\p{M} .,&()'/+-]{0,119}$/u },
  email: { required: true, max: 254, pattern: /^[^\s@<>()[\]\\,;:"]{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$/ },
  message: { required: false, max: 2000 },
};
const CHECK_IDS = /^(ORG|IDM|DS|PAT|SCH|NET)\.[1-9]$/;

// --- CSRF: zustandsloses HMAC-Token, beim Ausliefern der Seite ins <meta name="csrf-token"> schreiben
export function issueCsrfToken(now = Date.now()) {
  const ts = String(now);
  return `${ts}.${createHmac("sha256", CSRF_SECRET).update(ts).digest("base64url")}`;
}
function validCsrf(token) {
  if (!CSRF_SECRET) return true; // ohne Secret greifen Origin-Prüfung und JSON-Pflicht allein
  const [ts, mac] = String(token || "").split(".");
  if (!ts || !mac || Date.now() - Number(ts) > 2 * 3600e3) return false;
  const expected = Buffer.from(createHmac("sha256", CSRF_SECRET).update(ts).digest("base64url"));
  const given = Buffer.from(mac);
  return given.length === expected.length && timingSafeEqual(given, expected);
}

// --- Rate Limit im Speicher (bei mehreren Instanzen: Redis oder Datenbank)
const hits = new Map();
function limited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < RATE.windowMs);
  list.push(now);
  hits.set(ip, list);
  return list.length > RATE.max;
}

// --- Bereinigen und Prüfen
function clean(value, multiline) {
  if (typeof value !== "string") return "";
  const s = value.normalize("NFC");
  return (multiline ? s.replace(/[^\P{C}\n]/gu, "") : s.replace(/\p{C}/gu, "")).trim();
}
function validate(body) {
  if (!body || typeof body !== "object" || Array.isArray(body)) return null;
  const lead = {};
  for (const [key, rule] of Object.entries(RULES)) {
    const value = clean(body[key], key === "message");
    if ((rule.required && !value) || value.length > rule.max || (value && rule.pattern && !rule.pattern.test(value))) return null;
    lead[key] = value;
  }
  if (body.consent !== true) return null;
  lead.source = body.source === "check" ? "check" : "kontakt";
  if (body.check && typeof body.check === "object") {
    const { score, level, open } = body.check;
    if (!Number.isInteger(score) || score < 0 || score > 100 || !["ok", "warn", "crit"].includes(level)) return null;
    if (!Array.isArray(open) || open.length > 5 || !open.every((id) => typeof id === "string" && CHECK_IDS.test(id))) return null;
    lead.check = { score, level, open };
  }
  return lead;
}

// --- Zustellung: hier Mail (Klartext, nie HTML) oder CRM anbinden.
// Header-Injection ist ausgeschlossen, weil clean() CR/LF aus allen Einzeilern entfernt.
async function deliver(lead) {
  console.log("Neue Anfrage", JSON.stringify({ ...lead, receivedAt: new Date().toISOString() }));
}

function send(res, status, payload) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
  });
  res.end(JSON.stringify(payload));
}

createServer((req, res) => {
  if (req.url !== "/api/lead") return send(res, 404, { ok: false });
  if (req.method !== "POST") return send(res, 405, { ok: false });

  // CSRF-Schutz Stufe 1: nur die eigene Herkunft. Moderne Browser senden Origin und Sec-Fetch-Site immer mit.
  if (req.headers.origin !== ALLOWED_ORIGIN || (req.headers["sec-fetch-site"] && req.headers["sec-fetch-site"] !== "same-origin")) return send(res, 403, { ok: false });
  // Stufe 2: application/json erzwingt bei fremden Seiten einen CORS-Preflight, den wir nicht beantworten.
  if (!String(req.headers["content-type"] || "").startsWith("application/json")) return send(res, 415, { ok: false });
  // Stufe 3: Token aus dem Meta-Tag.
  if (!validCsrf(req.headers["x-csrf-token"])) return send(res, 403, { ok: false });

  const ip = req.socket.remoteAddress || "unknown";
  if (limited(ip)) return send(res, 429, { ok: false });

  let size = 0;
  const chunks = [];
  req.on("data", (chunk) => {
    size += chunk.length;
    if (size > MAX_BODY) { send(res, 413, { ok: false }); req.destroy(); return; }
    chunks.push(chunk);
  });
  req.on("end", async () => {
    if (res.writableEnded) return;
    let body;
    try { body = JSON.parse(Buffer.concat(chunks).toString("utf8")); } catch { return send(res, 400, { ok: false }); }
    if (body && body.website) return send(res, 200, { ok: true }); // Honeypot: Bot bekommt ein stilles OK
    const lead = validate(body);
    if (!lead) return send(res, 422, { ok: false }); // generisch, verrät keine Regel
    try { await deliver(lead); send(res, 200, { ok: true }); } catch { send(res, 500, { ok: false }); }
  });
}).listen(Number(process.env.PORT) || 3001);
