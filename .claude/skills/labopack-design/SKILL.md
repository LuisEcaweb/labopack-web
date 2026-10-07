# Diseño de Labopack · dirección «Marino»

Esta skill es la fuente de verdad del diseño de labopack.com. Si algo de aquí choca
con lo que ves en el repo, gana esta skill.

## Dirección estética

**Marino.** Azul marino profundo con celeste, que es el mundo de color que la web ya
tenía. Sobre él, tipografía con carácter y el producto como pieza central.

### El brief se equivocaba en esto, y conviene que conste

`docs/brief-rediseno.md` lista «fondo azul marino con acento celeste» entre los rasgos a
sustituir, y manda derivar la paleta del rojo teja del logo. **Eso era un error de
diagnóstico.** El azul no era el problema:

- Es el activo de color que ya funcionaba. Dos direcciones derivadas del logo —«Muelle»,
  gris hormigón y rojo teja; «Turno de noche», umbrío cálido y brasa— se montaron
  enteras y las dos salieron **más apagadas** que lo que sustituían.
- **Es lo coherente con el producto.** La interfaz de LabopackWMS es turquesa: las
  cabeceras de las cuatro capturas lo son. La web azul y la app turquesa hablaban el
  mismo idioma. El que desentona es el logo rojo, no el sitio.

Lo que sí delataba una plantilla eran los **detalles**, no el color: emojis como iconos,
tarjetas con degradado que se elevan al pasar el ratón, la franja de cuatro cifras, el
antetítulo en mayúsculas espaciadas, el desenfoque de la cabecera, Segoe UI y las flechas
pegadas al texto de los enlaces. Eso es lo que se ha quitado.

**Si alguien vuelve a proponer cambiar la paleta, que empiece por explicar de dónde
saldría la energía visual que el azul ya aporta.**

### Las tres consecuencias que mandan

- **El producto es el peso visual.** Una interfaz clara a pantalla completa sobre el
  marino es lo que más pesa de la página, y es lo que se vende. La portada abre con una
  captura de LabopackWMS, no con tipografía sobre un fondo.
- **El celeste marca y dirige.** No decora, no hace degradados, no rellena fondos grandes.
- **La fuerza va en un solo sitio.** Lo que no es el titular o el producto, calla.

## Ritmo de secciones

La página alterna **bloques marinos y claros a sangre**, de pantalla casi completa. Ahí
está la mayor parte de la energía visual, y sale de la referencia que fijó el cliente
(apple.com): bloques enteros alternos, un titular grande y centrado por bloque, y una
pieza visual por bloque.

Las secciones claras **no sobreescriben reglas**: redefinen los tokens de color en su
propio ámbito con `section.claro { --marino: var(--claro); … }`, y todo el CSS se
invierte solo. Es lo que evita la pelea de especificidad que en este proyecto ya ha
costado dos fallos (el botón de la cabecera a 1.05 de contraste y la rejilla que se
salía 110 px en móvil).

El acento sobre claro **no puede ser `--cian`**: `#38BDF8` sobre `#F2F5F9` da 1.96. En
las secciones claras el token pasa a `#0B74A8` (4.71), que es el mismo tono oscurecido.

## Paleta

```css
:root{
  --marino:#0A0F1C;       /* fondo de página */
  --marino-2:#111A2B;     /* superficie elevada: cabecera, pie, bloques destacados */
  --texto:#E6EDF6;        /* texto principal */
  --apagado:#93A7C4;      /* texto secundario */
  --linea:#223049;        /* separadores decorativos */
  --linea-fuerte:#52678F; /* bordes que delimitan un control */
  --cian:#38BDF8;         /* ÚNICO color de acento */
}
```

El icono de `assets/logo-icono.svg` usa **los colores originales del logo**, sin
recolorear: fue dibujado exactamente para este fondo.

### Contraste comprobado

| Par | Ratio | Uso |
| --- | --- | --- |
| `--texto` sobre `--marino` | 16.22 | Texto corriente |
| `--texto` sobre `--marino-2` | 14.76 | Texto en superficie elevada |
| `--apagado` sobre `--marino` | 7.80 | Texto secundario |
| `--apagado` sobre `--marino-2` | 7.10 | Secundario en superficie |
| `--cian` sobre `--marino` | 8.93 | Enlaces, cifras, acento |
| `--marino` sobre `--cian` | 8.93 | Texto de botón sólido |
| `--linea-fuerte` sobre `--marino` | 3.37 | Borde de control (mínimo 3.0) |
| `--linea` sobre `--marino` | 1.45 | **Solo separadores decorativos** |

**`--linea` no puede delimitar un control.** A 1.45 solo vale para separar filas o
bloques cuando el espaciado ya transmite la separación. Campos, botones fantasma y
cualquier elemento interactivo usan `--linea-fuerte`.

## Cabecera

**Fija y opaca.** Acompaña al bajar (`position: sticky`), porque `/wms/` mide 11.162 px
—unas doce pantallas— y sin eso el visitante se queda sin navegación durante todo el
recorrido. Los elementos con `id` llevan `scroll-margin-top: 96px` para que un salto a un
ancla no aterrice debajo de ella.

**No es translúcida.** El desenfoque está prohibido (ver 7) y aquí tampoco hace falta:
sobre bloques que alternan claro y marino, una barra opaca es más legible que una
translúcida.

**Sin mega-menú.** La referencia lo usa para once líneas de producto con decenas de
páginas cada una. Aquí hay 6 enlaces y 10 páginas: un panel desplegable sería
arquitectura para un catálogo que no existe, y además necesitaría JavaScript.

## Tarjetas

Las tarjetas son **superficie, no un bloque de texto con una regla encima**: fondo
`var(--superficie)`, radio `var(--radio)` y separación corta entre ellas (`--e3`). En las
secciones marinas la superficie es `#16213A`; en las claras, blanco.

Sin sombra y sin elevación al pasar el ratón — eso sigue prohibido (ver 8 y 9). Lo que
las separa del fondo es la superficie, no un efecto.

## Tipografía

**Dos familias, claramente distintas.** Es lo que más distingue la web de su versión
anterior, ahora que el color se conserva: Segoe UI era uno de los rasgos de plantilla.

- **Fraunces** (serif variable, ejes SOFT, WONK y opsz) en titulares, cifras destacadas,
  la cita y el rótulo «Labopack».
- **Instrument Sans** (variable) en todo el texto corriente.

| | |
| --- | --- |
| Ficheros | `assets/fonts/fraunces-variable.woff2` (118 KB) e `instrumentsans-variable.woff2` (56 KB), solo subset `latin` |
| Licencia | SIL Open Font License 1.1, en `assets/fonts/*-OFL.txt` |
| Carga | `font-display: swap` y un `<link rel="preload">` por familia. **Nunca desde un tercero** |

### Escala

| Rol | Tamaño | Familia |
| --- | --- | --- |
| Titular de página (`h1`) | `clamp(2.35rem, 7.4vw, 5.4rem)` | Fraunces 500 |
| Titular de sección (`h2`) | `clamp(1.9rem, 3.4vw, 2.6rem)` | Fraunces 500 |
| Subtítulo (`h3`) | 1.25–1.35rem | Fraunces 500 |
| Entradilla | 1.16rem | Instrument Sans 400 |
| Texto corriente | 1rem (base 17px) | Instrument Sans 400 |
| Cifra destacada | `clamp(2rem, 4.4vw, 3.1rem)` | Fraunces 500 |

- Las cifras llevan `font-variant-numeric: tabular-nums` siempre.
- Medida máxima de línea: **66 caracteres** en texto corriente, **16ch** en `h1`.

## Espaciado y retícula

Escala de espaciado en múltiplos de 4, con saltos deliberados. Nada de valores sueltos.

```css
--e1:4px; --e2:8px; --e3:14px; --e4:22px; --e5:34px; --e6:56px; --e7:88px; --e8:136px;
```

- Ancho máximo de contenido: **1180px**, con `padding` lateral de 32px (20px bajo 820px).
- Columna de texto: nunca más de 66 caracteres, aunque el contenedor dé para más.
- Separación entre secciones: `--e7` arriba y abajo en escritorio, `--e6` en móvil.
- **La retícula se rompe cuando el contenido lo pide, no por ritmo visual.** Una sección
  con tres ideas equivalentes puede ir en tres columnas; una con tres ideas de peso
  distinto, no. Antes de poner N columnas iguales, comprueba que los N elementos son
  realmente equivalentes.
- Alineación por defecto: **izquierda**. El texto centrado se reserva para un único
  bloque de cierre por página como mucho.

## Imagen

### No hay fotografía

**Decisión tomada el 7 de octubre de 2026: la web no lleva fotografía.** El único
material gráfico son capturas de LabopackWMS. Ni fotos del almacén, ni retratos, ni
stock, ni imágenes generadas.

Eso tiene una consecuencia de diseño que manda sobre todo este apartado: **las páginas
que no pueden enseñar producto no se apoyan en imagen.** La home, `/casos/`,
`/sectores/`, `/consultoria/` y `/contacto/` sostienen su jerarquía con tipografía,
espacio y composición. Si un bloque de esas páginas «necesita una imagen», es que está
mal compuesto; se recompone, no se rellena.

Si en el futuro llega fotografía propia, se revisa este apartado: proporción 3:2 en
horizontal y 4:5 en vertical, color natural, sin filtro, sin marco y sin redondeo.
Fotos de stock e imágenes generadas quedan prohibidas en cualquier caso (ver
Prohibiciones 17).

### Capturas de LabopackWMS

Son el único activo visual, y solo tienen sitio donde ilustran producto: `/wms/`,
`/wms/3pl/`, `/wms/farma/` y, si aporta, `/consultoria/`.

- Del entorno de pruebas, nunca de producción, y sin un solo dato de cliente a la vista.
- Se muestran a tamaño legible o recortadas a la zona que ilustra el texto. Una captura
  entera reducida hasta ser ilegible no sirve de nada.
- Sin mockups de portátil ni de móvil con reflejos. El marco, si hace falta, es un borde
  de 1px en `--linea-fuerte`.
- Van en `<figure class="captura">` con su `<figcaption>`. La variante `.movil` para las
  de Android. `loading="lazy"`, `decoding="async"` y `width`/`height` explícitos siempre.
- Formato **WebP**, calidad 86, a **1520 px de ancho**: el doble del ancho máximo de
  presentación (760 px), que es lo que pide una pantalla de alta densidad. Más allá de
  eso solo se gastan kilobytes. Las de móvil van a su tamaño nativo.
- Hoy hay cuatro, en `assets/capturas/`: dos en `/wms/`, una en `/wms/3pl/` y una en
  `/wms/farma/`.

### Saneado obligatorio antes de publicar una captura

El repositorio es público y lo publicado no se puede retirar. **Ninguna captura se sube
sin pasar por esto.**

- Fuera **todo** nombre de cliente, depositante, transportista, marca de producto y
  logotipo ajeno. Repasar columnas, barras de título, pies de página y ventanas de fondo:
  en la primera tanda había nombres en siete sitios distintos de la misma pantalla.
- **No se difumina: se tapa y se reescribe** con un dato inventado, en la misma fuente y
  al mismo tamaño. Un difuminado se ve y delata que había algo debajo.
- Los códigos internos (SKU, lote, número de orden) pueden quedarse: no identifican a
  nadie fuera de la empresa.
- Fuera el cromo de la ventana, la barra flotante de captura y el puntero del ratón.
- Cada `figcaption` termina en **«Datos de demostración.»**, porque lo son.

### Iconos

- SVG propios, **trazo único de 1.5px**, `stroke` en `currentColor`, `fill:none`,
  extremos y uniones redondeados, lienzo de 24×24.
- Vocabulario del almacén: palé, estantería, escáner, etiqueta, caja, muelle, termómetro.
  Nada de metáforas abstractas (bombillas, cohetes, engranajes).
- Un icono entra solo si sustituye a una palabra. Si acompaña a un título que ya lo
  dice, sobra.

### Logo

- El icono va en `assets/logo-icono.svg`, recoloreado para fondo claro: módulos en
  los colores originales del logo, sin recolorear. Sin degradado.
- El rótulo «Labopack» **se compone con Fraunces** (peso 600, color `--cian`), no con
  una imagen. El `logo.svg` original, con su degradado y su texto en Arial, deja de
  usarse en la página.

## Movimiento

- **Solo CSS.** Ni librerías, ni JavaScript, ni secuencias en canvas.
- Las animaciones ligadas al scroll van dentro de `@supports (animation-timeline: view())`.
  Sin soporte, el contenido se ve completo y estático.
- `@media (prefers-reduced-motion: reduce)` desactiva toda animación.
- Solo `transform` y `opacity`.
- **Un solo momento orquestado por página**, no una entrada por sección. Si cada bloque
  aparece con fundido y desplazamiento, eso ya es el patrón genérico.
- Desplazamiento horizontal, si hiciera falta, con `scroll-snap`. Nunca secuestrando el
  scroll vertical.

## Prohibiciones

Cada una nombra un patrón exacto. Son comprobables con una búsqueda en el HTML y el CSS
finales; la fase 5 lo hace.

1. **Ningún emoji como icono.** Ni en `<span class="icon">`, ni en `<h3>`, ni en
   `content:` de CSS, ni en `.ci-icon`. Cero pictogramas Unicode en el marcado.
2. **Ninguna flecha `→` pegada al texto de un enlace o un botón.** El enlace se marca
   con subrayado o con color, no con un carácter.
3. **Ningún antetítulo en mayúsculas espaciadas** sobre un titular. Ni `.kicker`, ni
   `text-transform:uppercase` combinado con `letter-spacing` positivo en rótulos.
4. **Ninguna palabra suelta del titular en otro color o estilo.** Nada de `.hl`. El
   titular va entero con el mismo tratamiento.
5. **Ninguna franja de cuatro cifras en columnas iguales centradas.** Las cifras van en
   lista alineada por la derecha, con su rótulo al lado.
6. **Ningún degradado.** Ni en fondos, ni en tarjetas, ni en texto. `linear-gradient` y
   `radial-gradient` no aparecen en la hoja de estilos.
7. **Ningún `backdrop-filter` ni `blur()`.** La cabecera es una superficie plana.
8. **Ninguna tarjeta que se eleve al pasar el ratón.** Nada de `transform:translateY()`
   en `:hover`. El hover y el foco se marcan con color o con borde.
9. **Ninguna sombra gris difusa** del tipo `box-shadow: 0 Npx rgba(0,0,0,.1)`.
10. **El radio no se aplica a todo.** Solo lo llevan las tarjetas (`var(--radio)`,
    18px) y los botones, que son pastillas (`999px`). Imágenes, tablas, campos y
    cualquier otra superficie van a **0**. El radio de las tarjetas viene de la
    referencia que fijó el cliente (apple.com), no de un valor por defecto.
11. **Ningún marcador numerado 01 / 02 / 03** salvo que el contenido sea de verdad una
    secuencia (un proceso por pasos o una cronología).
12. **Ninguna cadena de metadatos unida por puntos medios** (`A · B · C`) **añadida por
    el diseño** como adorno. Los que ya están en el texto original se respetan, porque el
    texto no se toca: hay unos cuarenta repartidos por las 10 páginas (las etiquetas de
    `/casos/`, la numeración de los grupos de módulos de `/wms/`, el aviso del pie en las
    diez, los `›` de las migas de `/guias/`…). **Todos vienen de `master`.** La
    comprobación válida es comparar contra `master`, no contar apariciones: si el total
    no sube, el diseño no ha añadido ninguno.
13. **Ninguna tipografía monoespaciada** para rótulos pequeños o datos.
14. **Ningún fondo claro como base de página.** El fondo es `--marino`; la única
    superficie distinta es `--marino-2`, y solo para cabecera, pie y bloques destacados.
15. **Ninguna familia tipográfica además de Fraunces e Instrument Sans.**
16. **Ningún recurso de tercero.** Ni fuentes, ni scripts, ni píxeles, ni analítica.
17. **Ninguna imagen generada con IA ni foto de stock.**

## Referencias

El brief pedía dos o tres webs de referencia. **No se aportaron**, y la dirección se
eligió sobre el posicionamiento y la marca. Si llegan más adelante, se anotan aquí con
lo que se toma de cada una, y se revisa si obligan a corregir algo de lo anterior.
