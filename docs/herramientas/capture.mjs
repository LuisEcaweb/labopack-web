// Captura las paginas de labopack-web a dos anchos.
// Uso: node capture.mjs <dirDestino> [ruta ...]
// Sin rutas, captura las 10 paginas. Usa el Chrome instalado: sin descargas.
import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';

const BASE = process.env.BASE_URL ?? 'http://localhost:8080';
const WIDTHS = [
  { w: 390,  h: 844,  tag: '390',  mobile: true  },
  { w: 1440, h: 900,  tag: '1440', mobile: false },
];
const ALL = [
  '/', '/wms/', '/wms/3pl/', '/wms/farma/', '/consultoria/',
  '/casos/', '/sectores/', '/guias/edi-para-operadores-logisticos/',
  '/contacto/', '/aviso-legal/',
];

const outDir = process.argv[2];
if (!outDir) { console.error('Falta el directorio destino.'); process.exit(1); }
const routes = process.argv.length > 3 ? process.argv.slice(3) : ALL;

const slug = (r) => r === '/' ? 'home' : r.replace(/^\/|\/$/g, '').replace(/\//g, '-');

await mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ channel: 'chrome' });
let fails = 0;

for (const { w, h, tag, mobile } of WIDTHS) {
  const ctx = await browser.newContext({
    viewport: { width: w, height: h },
    deviceScaleFactor: Number(process.env.DSF ?? 1),
    isMobile: mobile,
    hasTouch: mobile,
    // Movimiento reducido: la captura documenta el estado estatico, que es
    // tambien el que ve quien no soporta lineas de tiempo de scroll.
    reducedMotion: 'reduce',
  });
  const page = await ctx.newPage();
  for (const route of routes) {
    const url = BASE + route;
    const file = `${outDir}/${slug(route)}-${tag}.png`;
    try {
      const res = await page.goto(url, { waitUntil: 'load', timeout: 20000 });
      if (!res || !res.ok()) throw new Error(`HTTP ${res ? res.status() : 'sin respuesta'}`);
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: file, fullPage: true });
      console.log(`ok   ${tag.padStart(4)}  ${route}`);
    } catch (err) {
      fails++;
      console.error(`FALLO ${tag.padStart(4)}  ${route}  ${err.message}`);
    }
  }
  await ctx.close();
}

await browser.close();
console.log(fails ? `\n${fails} capturas fallaron.` : '\nTodas las capturas correctas.');
process.exit(fails ? 1 : 0);
