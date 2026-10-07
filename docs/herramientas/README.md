# Herramientas de verificación

Los cuatro guiones con los que se comprobó el rediseño. **No forman parte del sitio**:
`_config.yml` excluye `docs/`, así que nada de esto se publica en labopack.com. Tampoco
son dependencias del sitio, que sigue siendo HTML estático sin build ni paquetes.

La skill `.claude/skills/labopack-design/SKILL.md` da por hecho que estas comprobaciones
existen. Aquí están.

## Qué necesitan

- **Python 3** con [Pillow](https://pypi.org/project/Pillow/), solo para `capturas.py`.
- **Node** con [Playwright](https://playwright.dev/), para los `.mjs`.
- **Chrome instalado.** Los guiones usan `channel: 'chrome'`, así que **no descargan
  ningún navegador**: usan el que ya hay.

```bash
npm install playwright     # en un directorio fuera del repo
pip install Pillow         # solo si vas a sanear capturas
```

> En Windows, `python -I` ignora los paquetes del usuario y no encontrará Pillow.
> Ejecuta `capturas.py` sin esa bandera.

## Cómo se usan

Primero hay que servir el sitio desde la raíz del repositorio:

```bash
python -m http.server 8080
```

### `verificar.py` — contenido, patrones y peso

```bash
python verificar.py <raíz del repo>
```

Tres comprobaciones sobre las 10 páginas, con código de salida 1 si algo falla:

1. **Contenido intacto.** Compara el `<head>` y el texto visible contra la rama
   `master` del momento. Solo admite como diferencias las precargas de fuentes, los
   emojis, las flechas de enlace, los antetítulos y los pies de las capturas, y los
   lista para que no pasen desapercibidos.
2. **Los 15 patrones prohibidos** de la skill, buscados en el HTML y el CSS finales.
3. **Peso de transferencia** por página, incluidas las capturas, contra el tope de
   400 KB.

### `contraste.mjs` — WCAG AA medido en el navegador

```bash
node contraste.mjs http://127.0.0.1:8080
```

Recorre las 10 páginas a 390 y 1440 px y mide **el color que calcula el navegador**, no
el que dice la hoja de estilos. Sube por los ancestros hasta encontrar un fondo opaco,
distingue texto grande de texto normal y comprueba además el borde de los controles
(1.4.11). Es lo que encontró el botón de la cabecera renderizando a 1.05.

### `capture.mjs` — capturas de las 10 páginas

```bash
node capture.mjs <directorio> [ruta ...]
BASE_URL=https://labopack.com DSF=2 node capture.mjs ./salida /wms/
```

A 390 y 1440 px, página completa, con `prefers-reduced-motion: reduce` para que el
estado estático quede documentado. `DSF` controla la densidad (1 por defecto).

> En Git Bash hace falta `MSYS_NO_PATHCONV=1`, o las rutas de URL como `/wms/` se
> convierten en rutas de Windows.

### `capturas.py` — saneado de capturas de LabopackWMS

```bash
python capturas.py <directorio de origen> <directorio de salida>
```

**Está escrito contra unas capturas concretas**, con coordenadas fijas: sirve de
plantilla para la próxima tanda, no de utilidad general. Lo que hay que conservar es el
método, que está en la skill: **no se difumina, se tapa y se reescribe** el dato con uno
inventado, en la misma fuente y al mismo tamaño. Un difuminado se ve y delata que había
algo debajo.
