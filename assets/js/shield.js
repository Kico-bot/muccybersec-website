// Dekoratives Schild aus Lichtpunkten über einem Netzwerk-Boden (Canvas).
// Ersetzt ein Stockfoto: keine Bildrechte, wenige Kilobyte, scharf auf jedem Display.

const OUTLINE = [[0, -1], [.78, -.72], [.78, -.05], [.55, .5], [0, 1], [-.55, .5], [-.78, -.05], [-.78, -.72], [0, -1]];

function seeded(a) {
  return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
function edge(t) {
  const seg = t * 8, k = Math.min(7, Math.floor(seg)), f = seg - k;
  return [OUTLINE[k][0] + (OUTLINE[k + 1][0] - OUTLINE[k][0]) * f, OUTLINE[k][1] + (OUTLINE[k + 1][1] - OUTLINE[k][1]) * f];
}
function inside(x, y) {
  let c = false;
  for (let i = 0, j = OUTLINE.length - 2; i < OUTLINE.length - 1; j = i++) {
    const a = OUTLINE[i], b = OUTLINE[j];
    if ((a[1] > y) !== (b[1] > y) && x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]) c = !c;
  }
  return c;
}

export function initShield(canvas) {
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let W = 0, H = 0, pts = [], floor = [], running = true;

  function build() {
    const r = canvas.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio || 1);
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const rnd = seeded(7);
    pts = Array.from({ length: 64 }, (_, i) => ({ p: edge(i / 64), edge: true }));
    while (pts.length < 150) { const x = rnd() * 2 - 1, y = rnd() * 2 - 1; if (inside(x * 1.1, y * 1.1)) pts.push({ p: [x, y] }); }
    floor = Array.from({ length: 160 }, () => ({ a: rnd() * Math.PI * 2, d: Math.sqrt(rnd()), s: rnd() }));
  }

  function draw(time = 0) {
    ctx.clearRect(0, 0, W, H);
    const cx = W / 2, cy = H * .44, sc = Math.min(W, H) * .34, tt = time / 1000;
    for (let r = 1; r <= 5; r++) {
      ctx.beginPath(); ctx.ellipse(cx, H * .84, W * .09 * r, H * .022 * r, 0, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(18,179,154,${.22 - r * .035})`; ctx.lineWidth = 1; ctx.stroke();
    }
    for (const f of floor) {
      const tw = .35 + .4 * Math.sin(tt * 1.3 + f.s * 9);
      ctx.fillStyle = `rgba(60,200,220,${Math.max(0, tw * (1 - f.d * .6))})`;
      ctx.beginPath(); ctx.arc(cx + Math.cos(f.a) * f.d * W * .55, H * .84 + Math.sin(f.a) * f.d * H * .14, 1 + f.s * 1.6, 0, 7); ctx.fill();
    }
    const P = pts.map((o) => [cx + o.p[0] * sc, cy + o.p[1] * sc * 1.05, o.edge]);
    const reach = sc * .24;
    ctx.lineWidth = .6;
    for (let a = 0; a < P.length; a++) for (let b = a + 1; b < P.length; b++) {
      const d = Math.hypot(P[a][0] - P[b][0], P[a][1] - P[b][1]);
      if (d < reach) { ctx.strokeStyle = `rgba(45,212,191,${.32 * (1 - d / reach)})`; ctx.beginPath(); ctx.moveTo(P[a][0], P[a][1]); ctx.lineTo(P[b][0], P[b][1]); ctx.stroke(); }
    }
    ctx.save();
    ctx.shadowColor = "rgba(45,212,191,.9)"; ctx.shadowBlur = 14; ctx.strokeStyle = "rgba(94,234,212,.85)"; ctx.lineWidth = 1.6; ctx.beginPath();
    for (let k = 0; k <= 64; k++) { const e = edge(k / 64), X = cx + e[0] * sc, Y = cy + e[1] * sc * 1.05; if (k) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }
    ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx, cy - sc * 1.05); ctx.lineTo(cx, cy + sc * 1.05); ctx.strokeStyle = "rgba(94,234,212,.35)"; ctx.lineWidth = 1; ctx.stroke();
    ctx.restore();
    P.forEach((p, i) => {
      const tw = .55 + .45 * Math.sin(tt * 2 + i);
      ctx.fillStyle = p[2] ? `rgba(153,246,228,${tw})` : `rgba(94,234,212,${tw * .7})`;
      ctx.beginPath(); ctx.arc(p[0], p[1], p[2] ? 1.8 : 1.3, 0, 7); ctx.fill();
    });
    const g = ctx.createRadialGradient(cx, cy + sc * 1.05, 0, cx, cy + sc * 1.05, sc * .5);
    g.addColorStop(0, "rgba(94,234,212,.5)"); g.addColorStop(1, "rgba(94,234,212,0)");
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy + sc * 1.05, sc * .5, 0, 7); ctx.fill();
    if (!reduce && running) requestAnimationFrame(draw);
  }

  build(); draw();
  // build() leert die Leinwand; ohne laufende Animation einmal neu zeichnen.
  addEventListener("resize", () => { build(); if (reduce || !running) draw(); });
  // Animation anhalten, wenn das Bild nicht sichtbar ist: spart Akku auf Mobilgeräten.
  if (!reduce && "IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      const was = running; running = entry.isIntersecting;
      if (running && !was) requestAnimationFrame(draw);
    }).observe(canvas);
  }
}
