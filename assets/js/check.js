// Der Cyber-Check: eine Frage nach der anderen, danach die Auswertung.
// Die Antworten verlassen den Browser nicht, außer der Nutzer schickt das
// Lead-Formular ab. Zwischenstand liegt nur im sessionStorage dieses Tabs.

import { h, icon, svg, store } from "./dom.js";
import { FIELDS, QUESTIONS, ANSWERS, LEVELS, evaluate, levelOf } from "./questions.js";
import { bindLeadForm } from "./forms.js";

const KEY = "crc-v1";
const fresh = () => ({ index: 0, answers: {}, done: false, help: false });

function loadState() {
  const s = store.get(KEY);
  const valid = s && Number.isInteger(s.index) && s.index >= 0 && s.index < QUESTIONS.length && typeof s.answers === "object";
  return valid ? { ...fresh(), ...s } : fresh();
}

export function initCheck(card) {
  let state = loadState();

  const save = () => store.set(KEY, state);
  const answeredCount = () => QUESTIONS.filter((q) => q.id in state.answers).length;
  const fieldName = (key) => FIELDS.find((f) => f.key === key).name;

  function render() {
    save();
    card.replaceChildren(...(state.done ? resultView() : questionView()));
  }

  function questionView() {
    const q = QUESTIONS[state.index];
    const progress = h("i");
    progress.style.width = `${(answeredCount() / QUESTIONS.length) * 100}%`;

    const chips = FIELDS.map((f) => {
      const complete = QUESTIONS.filter((x) => x.field === f.key).every((x) => x.id in state.answers);
      const cls = ["chip", f.key === q.field && "on", complete && "done"].filter(Boolean).join(" ");
      return h("button", { type: "button", class: cls, onclick: () => jumpTo(f.key) }, f.name);
    });

    return [
      h("div", { class: "check-top" }, h("span", { text: "Cyber-Check" }), h("span", { text: `Frage ${state.index + 1} von ${QUESTIONS.length}` })),
      h("div", { class: "bar", role: "progressbar", "aria-label": "Fortschritt", "aria-valuemin": 0, "aria-valuemax": QUESTIONS.length, "aria-valuenow": answeredCount() }, progress),
      h("div", { class: "chips", role: "group", "aria-label": "Themenfelder" }, chips),
      h("div", { class: "q-ref" }, `${q.id} · ${fieldName(q.field)}`, q.top && h("span", { class: "top-tag", text: "TOP-Anforderung" })),
      h("div", { class: "q-row" },
        h("p", { class: "q-text", id: "q-text", text: q.text }),
        h("button", { type: "button", class: "help-btn", "aria-expanded": String(state.help), "aria-controls": "q-help", onclick: toggleHelp }, icon("i-help"), "Hilfe")),
      h("p", { class: "q-sub", text: q.sub }),
      h("p", { class: "help", id: "q-help", hidden: !state.help, text: q.help }),
      h("div", { class: "answers", role: "group", "aria-labelledby": "q-text" },
        ANSWERS.map((a) => h("button", { type: "button", class: "answer", "aria-pressed": String(state.answers[q.id] === a.value), onclick: () => pick(a.value) }, a.label))),
      h("button", { type: "button", class: "back", disabled: state.index === 0, onclick: back }, icon("i-back"), "Zurück"),
    ];
  }

  function resultView() {
    const r = evaluate(state.answers);
    const level = LEVELS[r.level];
    const C = 2 * Math.PI * 42;

    const ring = svg("svg", { viewBox: "0 0 100 100", "aria-hidden": "true" });
    ring.append(
      svg("circle", { class: "track", cx: 50, cy: 50, r: 42, fill: "none", "stroke-width": 10 }),
      svg("circle", { class: `lvl-${r.level}`, cx: 50, cy: 50, r: 42, fill: "none", "stroke-width": 10, "stroke-linecap": "round", "stroke-dasharray": `${(C * r.score) / 100} ${C}` }),
    );

    const fieldRows = r.fields.map((f) => {
      const fill = h("i", { class: `lvl-${levelOf(f.pct)}` });
      fill.style.width = `${f.pct}%`;
      return h("div", { class: "field-row" },
        h("div", {}, h("span", { text: f.name }), h("span", { text: `${f.pct} %` })),
        h("div", { class: "bar", role: "img", "aria-label": `${f.name}: ${f.pct} Prozent` }, fill));
    });

    const gaps = r.gaps.slice(0, 3).map((g) =>
      h("li", {}, h("b", { text: g.q.id + (g.q.top ? " · TOP" : "") }), h("span", { text: g.q.text })));

    const lead = document.getElementById("lead-template").content.firstElementChild.cloneNode(true);
    bindLeadForm(lead.querySelector("form"), {
      source: "check",
      // Nur berechnete Werte, nie freier Text: Score, Stufe, offene Anforderungen.
      extra: () => ({ check: { score: r.score, level: r.level, open: r.gaps.slice(0, 5).map((g) => g.q.id) } }),
    });

    return [
      h("div", { class: "check-top" }, h("span", { text: "Cyber-Check · Ergebnis" }), h("span", { text: `${QUESTIONS.length} von ${QUESTIONS.length} beantwortet` })),
      h("div", { class: "result" },
        h("div", { class: "res-head" },
          h("div", { class: "ring" }, ring, h("div", {}, h("b", { text: r.score }), h("small", { text: "von 100" }))),
          h("div", {},
            h("span", { class: `status lvl-${r.level}`, text: level.label }),
            h("h3", { text: "Ihr Sicherheitsniveau" }),
            h("p", { text: level.text + (r.topOpen ? ` Offene TOP-Anforderungen: ${r.topOpen}.` : "") }))),
        h("div", { class: "fields" }, fieldRows),
        gaps.length > 0 && h("div", {}, h("h3", { class: "res-sub", text: "Zuerst angehen" }), h("ul", { class: "gaps" }, gaps)),
        lead,
        h("button", { type: "button", class: "restart", onclick: restart }, "Check neu starten")),
    ];
  }

  function pick(value) {
    const q = QUESTIONS[state.index];
    state.answers[q.id] = value;
    card.querySelectorAll(".answer").forEach((b, i) => b.setAttribute("aria-pressed", String(ANSWERS[i].value === value)));
    setTimeout(() => {
      state.help = false;
      const after = QUESTIONS.findIndex((x, i) => i > state.index && !(x.id in state.answers));
      const any = QUESTIONS.findIndex((x) => !(x.id in state.answers));
      const next = after >= 0 ? after : any;
      if (next < 0) state.done = true; else state.index = next;
      render();
      card.scrollIntoView({ behavior: "smooth", block: "nearest" });
      card.querySelector(".answer, .status")?.focus?.({ preventScroll: true });
    }, 160);
  }

  function jumpTo(fieldKey) { state.index = QUESTIONS.findIndex((q) => q.field === fieldKey); state.help = false; render(); }
  function back() { if (state.index > 0) { state.index--; state.help = false; render(); } }
  function toggleHelp() { state.help = !state.help; render(); card.querySelector(".help-btn").focus(); }
  function restart() { state = fresh(); render(); }

  // Tasten 1 bis 3 beantworten die Frage, solange die Karte sichtbar ist und kein Feld den Fokus hat.
  document.addEventListener("keydown", (e) => {
    if (state.done || e.altKey || e.ctrlKey || e.metaKey || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName)) return;
    const index = ["1", "2", "3"].indexOf(e.key);
    const box = card.getBoundingClientRect();
    if (index >= 0 && box.top < innerHeight && box.bottom > 0) pick(ANSWERS[index].value);
  });

  render();
}
