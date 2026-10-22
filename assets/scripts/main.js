// Einstiegspunkt. Wird als ES-Modul geladen (script-src 'self', kein Inline-Code).

import { initCheck } from "./check.js";
import { bindLeadForm } from "./forms.js";

const card = document.getElementById("check-card");
if (card) initCheck(card);

const contact = document.getElementById("contact-form");
if (contact) bindLeadForm(contact);

// E-Mail kopieren: Clipboard-API, sonst Text markieren.
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const target = document.getElementById(button.dataset.copy);
    if (!target) return;
    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      button.textContent = "Kopiert";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(target);
      const selection = getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = "Markiert";
    }
  });
});

// Mobiler Handlungsaufruf: nur sichtbar, solange weder Hero noch Check im Bild sind.
const sticky = document.getElementById("sticky-cta");
const watched = [document.getElementById("start"), document.getElementById("check"), document.getElementById("kontakt")].filter(Boolean);
if (sticky && watched.length && "IntersectionObserver" in window) {
  const visible = new Set();
  const observer = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) visible.add(e.target); else visible.delete(e.target);
    }
    sticky.classList.toggle("show", visible.size === 0);
  });
  watched.forEach((el) => observer.observe(el));
}
