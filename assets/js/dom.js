// Kleine DOM-Helfer. Alles wird über createElement und textContent gebaut,
// nie über innerHTML: so kann kein Text, auch kein künftiger aus einer API,
// als Markup interpretiert werden (XSS strukturell ausgeschlossen).

const SVG_NS = "http://www.w3.org/2000/svg";

/**
 * h("button", { class: "chip", type: "button", onclick: fn }, "Text", kindElement)
 * Attribute mit "on" am Anfang werden als Event-Listener gebunden,
 * "text" setzt textContent, false/null/undefined werden ausgelassen.
 */
export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value === false || value === null || value === undefined) continue;
    if (key.startsWith("on") && typeof value === "function") el.addEventListener(key.slice(2), value);
    else if (key === "text") el.textContent = String(value);
    else el.setAttribute(key, value === true ? "" : String(value));
  }
  append(el, children);
  return el;
}

function append(el, children) {
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    el.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
}

/** Symbol aus dem SVG-Sprite im HTML, z. B. icon("i-arrow"). */
export function icon(id) {
  const svg = document.createElementNS(SVG_NS, "svg");
  svg.setAttribute("aria-hidden", "true");
  const use = document.createElementNS(SVG_NS, "use");
  use.setAttribute("href", "#" + id);
  svg.append(use);
  return svg;
}

/** SVG-Element mit Attributen, für den Ergebnisring. */
export function svg(tag, attrs = {}) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, String(value));
  return el;
}

/** Speicher, der in privaten Fenstern oder bei gesperrtem Speicher nicht wirft. */
export const store = {
  get(key) { try { return JSON.parse(sessionStorage.getItem(key) || "null"); } catch { return null; } },
  set(key, value) { try { sessionStorage.setItem(key, JSON.stringify(value)); } catch { /* ohne Speicher weiter */ } },
};
