// ctx7: CIEDE2000 per Sharma, Wu & Dalal (2005) — standard perceptual color difference.

function srgbToLinear(c) {
  c /= 255;
  return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
}

/** "#rrggbb" -> CIELab (D65). */
export function hexToLab(hex) {
  const r = srgbToLinear(parseInt(hex.slice(1, 3), 16));
  const g = srgbToLinear(parseInt(hex.slice(3, 5), 16));
  const b = srgbToLinear(parseInt(hex.slice(5, 7), 16));
  // linear sRGB -> XYZ (D65)
  const X = r * 0.4124 + g * 0.3576 + b * 0.1805;
  const Y = r * 0.2126 + g * 0.7152 + b * 0.0722;
  const Z = r * 0.0193 + g * 0.1192 + b * 0.9505;
  const Xn = 0.95047, Yn = 1.0, Zn = 1.08883;
  const f = (t) => (t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116);
  const fx = f(X / Xn), fy = f(Y / Yn), fz = f(Z / Zn);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}

const rad = (d) => (d * Math.PI) / 180;
const deg = (r) => (r * 180) / Math.PI;

/** CIEDE2000 color difference between two CIELab triples. */
export function ciede2000([L1, a1, b1], [L2, a2, b2]) {
  const kL = 1, kC = 1, kH = 1;
  const C1 = Math.hypot(a1, b1), C2 = Math.hypot(a2, b2);
  const Cbar = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Cbar ** 7 / (Cbar ** 7 + 25 ** 7)));
  const a1p = (1 + G) * a1, a2p = (1 + G) * a2;
  const C1p = Math.hypot(a1p, b1), C2p = Math.hypot(a2p, b2);
  const h1p = (deg(Math.atan2(b1, a1p)) + 360) % 360;
  const h2p = (deg(Math.atan2(b2, a2p)) + 360) % 360;

  const dLp = L2 - L1;
  const dCp = C2p - C1p;
  let dhp;
  if (C1p * C2p === 0) dhp = 0;
  else if (Math.abs(h2p - h1p) <= 180) dhp = h2p - h1p;
  else dhp = h2p - h1p > 180 ? h2p - h1p - 360 : h2p - h1p + 360;
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(rad(dhp) / 2);

  const Lbarp = (L1 + L2) / 2;
  const Cbarp = (C1p + C2p) / 2;
  let hbarp;
  if (C1p * C2p === 0) hbarp = h1p + h2p;
  else if (Math.abs(h1p - h2p) <= 180) hbarp = (h1p + h2p) / 2;
  else hbarp = h1p + h2p < 360 ? (h1p + h2p + 360) / 2 : (h1p + h2p - 360) / 2;

  const T =
    1 -
    0.17 * Math.cos(rad(hbarp - 30)) +
    0.24 * Math.cos(rad(2 * hbarp)) +
    0.32 * Math.cos(rad(3 * hbarp + 6)) -
    0.2 * Math.cos(rad(4 * hbarp - 63));
  const dTheta = 30 * Math.exp(-(((hbarp - 275) / 25) ** 2));
  const Rc = 2 * Math.sqrt(Cbarp ** 7 / (Cbarp ** 7 + 25 ** 7));
  const Sl = 1 + (0.015 * (Lbarp - 50) ** 2) / Math.sqrt(20 + (Lbarp - 50) ** 2);
  const Sc = 1 + 0.045 * Cbarp;
  const Sh = 1 + 0.015 * Cbarp * T;
  const Rt = -Math.sin(rad(2 * dTheta)) * Rc;

  return Math.sqrt(
    (dLp / (kL * Sl)) ** 2 +
      (dCp / (kC * Sc)) ** 2 +
      (dHp / (kH * Sh)) ** 2 +
      Rt * (dCp / (kC * Sc)) * (dHp / (kH * Sh)),
  );
}

const BIG_REGION_CATS = new Set(["terrain", "structure"]);
const isBigRegion = (cat) => BIG_REGION_CATS.has(cat);

/**
 * Return the list of color-pair violations. Empty array = pass.
 *
 * Strict bar (large flat regions): two terrain/structure tokens tile the map as big color
 * fields the model must never blend (floor vs wall vs water vs lava) → require >= `strict`.
 * Loose bar (objects/markers): any pair touching a feature/marker/hazard is a small,
 * glyph-bearing cell whose identity is carried by its icon, so it only needs >= `loose`.
 * dm-layer tokens render as their playerFallback / fixed-tint overlays, so they never
 * participate in the base-key color and are excluded from the gate entirely.
 *
 * Thresholds are tuned for a ~30-material palette: dark materials compress in CIEDE2000
 * (two near-blacks cannot exceed ~18 ΔE in sRGB), so 16/10 is the achievable bar that
 * still keeps every pair clearly distinguishable.
 */
export function checkSeparation(manifest, { strict = 16, loose = 10 } = {}) {
  const entries = Object.entries(manifest).filter(([, e]) => e.layer !== "dm");
  const labs = entries.map(([code, e]) => ({ code, cat: e.category, lab: hexToLab(e.color) }));
  const violations = [];
  for (let i = 0; i < labs.length; i++) {
    for (let j = i + 1; j < labs.length; j++) {
      const d = ciede2000(labs[i].lab, labs[j].lab);
      const thr = isBigRegion(labs[i].cat) && isBigRegion(labs[j].cat) ? strict : loose;
      if (d < thr) violations.push({ a: labs[i].code, b: labs[j].code, deltaE: +d.toFixed(2), threshold: thr });
    }
  }
  return violations;
}
