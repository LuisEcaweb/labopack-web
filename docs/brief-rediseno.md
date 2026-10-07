# Brief labopack-web: diseño sin aspecto de IA

> **Nota de cierre — 7 de octubre de 2026.** Este documento se conserva tal como se
> escribió, porque es el encargo. Pero **tres de sus premisas no sobrevivieron al
> trabajo**, y la fuente de verdad del diseño es
> [`.claude/skills/labopack-design/SKILL.md`](../.claude/skills/labopack-design/SKILL.md).
>
> 1. **«Sustituir el azul marino con acento celeste».** Era un error de diagnóstico. El
>    azul no era un rasgo de plantilla: era el activo de color que funcionaba, y es lo
>    coherente con la interfaz de LabopackWMS, que es turquesa. Se probaron dos
>    direcciones derivadas del logo —«Muelle» y «Turno de noche»— y las dos salieron más
>    apagadas que lo que sustituían. El azul se queda; lo que se quitó fueron los
>    detalles: emojis, degradados, elevación al hover, antetítulos en mayúsculas,
>    desenfoque y Segoe UI.
> 2. **«Ninguna fotografía».** Se mantiene, pero tuvo un coste que no se advirtió a
>    tiempo: una web B2B sin imagen en portada parece floja por bien compuesta que esté.
>    Lo resolvieron las capturas de LabopackWMS, que pasaron a ser la pieza central.
> 3. **Las cifras de fechas no eran una inconsistencia.** 1991 es la constitución de la
>    sociedad, 2004 el almacén, 2005 el WMS y 2024 la reescritura: cuatro hechos
>    distintos. No se tocó ningún texto.
>
> La dirección final toma su ritmo de bloques alternos y sus tarjetas de **apple.com**,
> que el cliente fijó como referencia. No se copió nada suyo: ni diseño, ni imágenes, ni
> el menú — las razones están en el apartado «Cabecera» de la skill.


Oct 7, 2026 · @Luis

Brief para Claude Code en el repo `LuisEcaweb/labopack-web` (rama `master`, publicado en labopack.com). Encarga un rediseño visual con identidad propia en cinco fases, con una parada para tu aprobación después de la home.

## Objetivo

Que labopack.com se reconozca como Labopack y no como una plantilla, sin cambiar lo que dice ni cómo posiciona.

|  | Alcance |
| --- | --- |
| Se cambia | `assets/styles.css`, el marcado de presentación de las 10 páginas y los recursos nuevos (fuentes, fotos, iconos) |
| No se toca | Los textos, el `<head>` de cada página (title, description, canonical, Open Graph, JSON-LD), las URLs, `sitemap.xml`, `robots.txt` y `CNAME` |
| Se mantiene | HTML estático sin build, sin frameworks, sin JavaScript obligatorio y sin llamadas a servidores de terceros |

El repo es público. Nada de lo que se escriba en él (skill, `CLAUDE.md`, capturas) puede llevar nombres o datos de clientes.

## Punto de partida

La web actual reúne casi todos los rasgos que delatan un diseño generado, y no usa el color de su propio logo. Leído en el repo el 7 de octubre de 2026 (commit `83ff5a4`); Claude Code debe comprobarlo antes de cambiar nada.

| Rasgo actual | Dónde está | Qué hacer |
| --- | --- | --- |
| Fondo azul marino con acento celeste (`#0a0f1c`, `#38bdf8`) | `:root` de `assets/styles.css` | Sustituir por una paleta derivada del logo |
| Emojis como iconos | 56 elementos `.icon` en las 10 páginas, más los títulos de `.path-card` | Quitarlos o cambiarlos por iconos SVG propios de un solo trazo |
| Rejillas de tres tarjetas iguales que se elevan al pasar el ratón | `.card`, `.grid.cols-3` | Componer cada bloque según su contenido |
| Franja de cuatro cifras grandes en color de acento | `.stats` en la home | Dar contexto a cada cifra o integrarla en el texto |
| Antetítulo en mayúsculas espaciadas | `.hero .kicker` | Eliminar o replantear |
| Tarjetas con degradado y cabecera con desenfoque | `.path-card`, `.site-header` | Superficies planas, sin efectos |
| Tipografía de sistema (Segoe UI) | `--font` | Elegir una familia con intención |
| Ninguna fotografía ni captura del producto | Las únicas imágenes son `logo.svg` y `ecaweb-logo.png` | Añadir material real; es la carencia de más peso |

Dos datos que condicionan el rediseño:

- **Color de marca sin usar.** El logo lleva un rojo teja en degradado (`#AA2300`, `#D8451A`, `#F0704A`) y el favicon lo pone sobre crema (`#e6ddd2`). La hoja de estilos no usa ninguno de esos tonos.
- **Logo dibujado para fondo oscuro.** El texto de `logo.svg` es casi blanco (`#e6edf6`). Si la dirección elegida es clara, hace falta una variante del logo.

La parte técnica está bien y hay que conservarla: 12 KB de CSS, cero JavaScript, cero dependencias, metadatos y JSON-LD completos.

## Fase 1 · Preparar el repo y la skill base

Todo el trabajo va en una rama, porque el repo publica labopack.com.

1. **Rama de trabajo.** Crear `rediseno` desde `master`. Nada se fusiona hasta tu aprobación final.
2. **Skill oficial (lo haces tú).** Instalar `frontend-design` desde `/plugin`, buscándola por nombre y comprobando que el autor es Anthropic. Circulan varios comandos de instalación según el marketplace, así que mejor no copiar uno de un blog.
3. **Comprobar que carga.** `/plugin` debe listarla como activa. No es un comando: se activa sola cuando se pide una interfaz.
4. **`CLAUDE.md` en la raíz.** Corto y como índice: el stack, las restricciones del apartado Objetivo, cómo servir la web en local y un puntero a la skill de la fase 2.
5. **Servidor local.** Las páginas cargan los recursos con rutas absolutas (`/assets/styles.css`), así que abrir el HTML directamente no aplica estilos. Hay que servir desde la raíz del repo, por ejemplo con `python -m http.server 8080`.

## Fase 2 · Skill de diseño de Labopack

La identidad se fija por escrito en `.claude/skills/labopack-design/SKILL.md` antes de tocar el CSS, y la eliges tú entre tres propuestas.

1. **Tres direcciones.** Claude Code propone tres, cada una con nombre, paleta, tipografías y una captura de la cabecera y el primer bloque de la home.
2. **Elección.** Eliges una. Las otras dos se descartan, no se mezclan.
3. **Skill.** Se escribe con la dirección elegida y los apartados de la tabla.

| Apartado de la skill | Qué fija |
| --- | --- |
| Dirección estética | Una dirección con nombre y una frase que la justifique desde el posicionamiento: consultoría que viene de un almacén, no de un PowerPoint |
| Paleta | Tokens derivados del rojo teja y el crema del logo, un solo color de acento y contraste AA comprobado |
| Tipografía | Dos familias como máximo, en WOFF2 dentro de `assets/fonts/`, con licencia que permita alojarlas y `font-display: swap` |
| Espaciado y retícula | Escala de espaciado, anchos de columna y cuándo se rompe la retícula |
| Imagen | Tratamiento de fotos y capturas (proporción, recorte, color) y estilo de los iconos SVG |
| Prohibiciones | Los rasgos de la tabla de Punto de partida, escritos como reglas concretas |
| Referencias | Las webs que aportes, con lo que se toma de cada una |

Las prohibiciones tienen que nombrar el patrón exacto. «No hagas diseño genérico» no cambia nada; «ningún emoji como icono» sí.

## Fase 3 · Home con revisión visual

Primero solo la home, mirando capturas en cada vuelta, y con parada para tu aprobación antes de seguir.

1. **Capturas de partida.** Antes de cambiar nada, capturar la home actual a 390 px y a 1440 px de ancho y guardarlas en `docs/rediseno/antes/`.
2. **Rediseño.** Rehacer `index.html` y `assets/styles.css` siguiendo la skill de la fase 2.
3. **Bucle.** Tras cada cambio relevante, servir en local, capturar a los dos anchos con Playwright o la herramienta de navegador disponible, y mirar la captura.
4. **Corrección.** Revisar cada captura contra la skill: jerarquía, espaciado, contraste y prohibiciones. Repetir hasta que no quede ninguna.
5. **Parada.** Guardar las capturas finales en `docs/rediseno/despues/`, enseñarte el antes y el después, y esperar tu visto bueno.

La hoja de estilos es común, así que las otras nueve páginas pueden quedar descuadradas en la rama durante esta fase. Se arreglan en la fase 4.

## Fase 4 · Resto de páginas y movimiento

Con la home aprobada, el sistema se aplica a las otras nueve páginas y se añade movimiento solo con CSS.

Orden de las páginas, de más a menos peso comercial, con el mismo bucle de capturas en cada una:

1. `/wms/`, que es la más larga (26 KB) y la que más tarjetas tiene
2. `/wms/3pl/` y `/wms/farma/`
3. `/consultoria/`
4. `/casos/` y `/sectores/`
5. `/guias/edi-para-operadores-logisticos/`
6. `/contacto/` y `/aviso-legal/`

Reglas de movimiento:

- **Solo CSS.** Sin GSAP, sin Lenis y sin secuencias de imágenes en canvas. Rompen la regla de cero JavaScript, y lo que se pinta en un canvas no es texto indexable.
- **Mejora progresiva.** Las animaciones ligadas al scroll usan `animation-timeline: view()` dentro de un bloque `@supports`. Donde el navegador no lo soporte, el contenido se ve completo y estático.
- **Movimiento reducido.** Con `prefers-reduced-motion: reduce` no se anima nada.
- **Propiedades baratas.** Solo `transform` y `opacity`.
- **Sin secuestro del scroll.** Si algún bloque necesita desplazamiento horizontal, se hace con `scroll-snap`.

## Fase 5 · Control de calidad

Antes de pedirte la fusión, la rama pasa seis comprobaciones. Los umbrales numéricos son una propuesta mía; ajústalos si quieres.

| Comprobación | Cómo | Umbral |
| --- | --- | --- |
| Contenido intacto | Script que compara `master` y `rediseno` en las 10 páginas: el `<head>` y el texto visible | Title, description, canonical, Open Graph y JSON-LD idénticos. En el `<head>` solo se admiten precargas de fuentes. En el texto, solo desaparecen los emojis |
| Rendimiento | Lighthouse en móvil sobre la home y `/wms/` | Rendimiento, accesibilidad y SEO de 95 o más |
| Peso | Transferencia total de la home con fuentes e imágenes | 400 KB como máximo |
| Contraste | Texto y controles en las 10 páginas | WCAG AA |
| Prohibiciones | Buscar en el HTML y el CSS finales cada patrón prohibido de la skill | Ninguna coincidencia |
| Revisión independiente | Un subagente sin contexto del rediseño critica las capturas finales contra la skill | Sin objeciones abiertas |

Impeccable queda como paso opcional al final, como segundo linter de patrones. Antes de instalarla hay que leer su `SKILL.md`, igual que con cualquier skill de terceros.

## Lo que tienes que aportar

El material real es lo que más cambia el resultado, y solo puedes darlo tú.

- [ ] **Fotos.** Entre cinco y ocho del almacén, de gente trabajando y de terminales en uso. Sin etiquetas, albaranes ni pantallas donde se lean datos de clientes.
- [ ] **Capturas de LabopackWMS.** En Windows y en Android, sacadas del entorno de pruebas y nunca de producción.
- [ ] **Referencias.** Dos o tres webs que te gusten, de cualquier sector, y qué te gusta de cada una.
- [ ] **Tema.** Claro, oscuro o los dos.
- [ ] **Una duda de contenido.** La cita de la home firma «fundador y consultor principal», el JSON-LD da 1991 como año de fundación y el pie dice «desde 2004». El rediseño no toca textos; si hay algo que corregir, mejor decidirlo antes.

Si las fotos no están a tiempo, Claude Code deja los huecos marcados con su proporción. No genera imágenes ni usa fotos de stock.

## Hecho y fuera de alcance

El trabajo termina con un pull request abierto contra `master`, sin fusionar.

Se da por hecho cuando:

- Las 10 páginas siguen la skill y pasan las seis comprobaciones de la fase 5.
- `docs/rediseno/` guarda el antes y el después de cada página a los dos anchos.
- La rama `rediseno` está subida y el pull request resume qué cambió y qué quedó pendiente.

Queda fuera:

- Cambiar textos, URLs o metadatos, y crear páginas nuevas.
- Añadir frameworks, un paso de build o JavaScript.
- Secuencias de imágenes ligadas al scroll e imágenes generadas con IA.
- Fuentes, scripts o píxeles servidos por terceros.

## Mensaje de arranque

Guarda este documento en el repo como `docs/brief-rediseno.md` y pega este mensaje en una sesión de Claude Code abierta en `labopack-web`.

```text
Lee docs/brief-rediseno.md entero antes de hacer nada.

Trabaja en la rama rediseno, creada desde master. No fusiones ni publiques.

Empieza comprobando el apartado "Punto de partida" contra el repo y dime si algo ya no coincide.

Después ejecuta las fases 1 y 2. En la fase 2, para y enséñame las tres direcciones con sus capturas. No escribas la skill hasta que yo elija una.

Reglas para todas las fases:
- No cambies textos, URLs ni el <head>, salvo precargas de fuentes.
- HTML y CSS estáticos: sin build, sin JavaScript y sin recursos de terceros.
- No generes imágenes ni uses fotos de stock. Deja los huecos marcados.
- El repo es público: ningún nombre ni dato de cliente en archivos nuevos.
- Si algo del brief choca con lo que encuentres en el repo, pregunta antes de decidir.
```
