// Audita el contraste WCAG AA de todo el texto visible y de los bordes de control
// de las 10 paginas, con los colores que el navegador calcula de verdad.
// Uso: node contraste.mjs [baseUrl]
import { chromium } from 'playwright';

const BASE = process.argv[2] ?? 'http://127.0.0.1:8080';
const RUTAS = [
  '/', '/wms/', '/wms/3pl/', '/wms/farma/', '/consultoria/',
  '/casos/', '/sectores/', '/guias/edi-para-operadores-logisticos/',
  '/contacto/', '/aviso-legal/',
];
const ANCHOS = [{ w: 390, h: 844 }, { w: 1440, h: 900 }];

const AUDITORIA = () => {
  const lin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  const rgb = (s) => (s.match(/[\d.]+/g) || []).map(Number);
  const ratio = (a, b) => {
    const [la, lb] = [lum(a), lum(b)];
    const [hi, lo] = la > lb ? [la, lb] : [lb, la];
    return (hi + 0.05) / (lo + 0.05);
  };
  // Fondo efectivo: sube por los ancestros hasta encontrar uno opaco.
  const fondo = (el) => {
    for (let n = el; n; n = n.parentElement) {
      const c = rgb(getComputedStyle(n).backgroundColor);
      if (c.length >= 3 && (c[3] === undefined || c[3] > 0.95)) return c.slice(0, 3);
    }
    return [255, 255, 255];
  };

  const malos = [];
  for (const el of document.querySelectorAll('body *')) {
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;

    // Texto propio del elemento (no el de sus hijos).
    const propio = [...el.childNodes]
      .filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim();
    if (propio) {
      const px = parseFloat(st.fontSize);
      const peso = parseInt(st.fontWeight, 10) || 400;
      const grande = px >= 24 || (px >= 18.66 && peso >= 700);
      const min = grande ? 3 : 4.5;
      const cr = ratio(rgb(st.color).slice(0, 3), fondo(el));
      if (cr < min) {
        malos.push({
          tipo: 'texto', sel: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''),
          cr: +cr.toFixed(2), min, px: +px.toFixed(1), muestra: propio.slice(0, 48),
        });
      }
    }

    // Bordes de elementos interactivos: minimo 3:1 (WCAG 1.4.11).
    const interactivo = el.matches('a.btn, button, input, select, textarea');
    if (interactivo && st.borderTopWidth !== '0px') {
      const cr = ratio(rgb(st.borderTopColor).slice(0, 3), fondo(el.parentElement || el));
      if (cr < 3) {
        malos.push({
          tipo: 'borde', sel: el.tagName.toLowerCase() + '.' + String(el.className).split(' ')[0],
          cr: +cr.toFixed(2), min: 3, px: 0, muestra: (el.textContent || '').trim().slice(0, 48),
        });
      }
    }
  }
  return malos;
};

const b = await chromium.launch({ channel: 'chrome' });
let total = 0;
for (const { w, h } of ANCHOS) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  for (const ruta of RUTAS) {
    await page.goto(BASE + ruta, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const malos = await page.evaluate(AUDITORIA);
    // Un mismo selector se repite mucho: se agrupa.
    const vistos = new Map();
    for (const m of malos) {
      const k = `${m.tipo}|${m.sel}|${m.cr}`;
      vistos.set(k, (vistos.get(k) ?? { ...m, n: 0 }));
      vistos.get(k).n++;
    }
    if (vistos.size) {
      total += vistos.size;
      console.log(`  !! ${String(w).padStart(4)}px  ${ruta}`);
      for (const m of vistos.values()) {
        console.log(`        ${m.tipo} ${m.sel}  ratio ${m.cr} < ${m.min}  (${m.px}px, x${m.n})  "${m.muestra}"`);
      }
    } else {
      console.log(`  OK ${String(w).padStart(4)}px  ${ruta}`);
    }
  }
  await ctx.close();
}
await b.close();
console.log(total ? `\n${total} problemas de contraste.` : '\nTodo el texto y los controles pasan WCAG AA.');
process.exit(total ? 1 : 0);
