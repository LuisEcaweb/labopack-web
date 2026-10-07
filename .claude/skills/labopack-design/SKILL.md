# Diseño de Labopack · dirección «Turno de noche»

Esta skill es la fuente de verdad del diseño de labopack.com. Si algo de aquí choca
con lo que ves en el repo, gana esta skill; si choca con `docs/brief-rediseno.md`,
gana el brief y hay que actualizar esta skill.

## Dirección estética

**Turno de noche.** El almacén a oscuras y el resplandor del escáner en el pasillo.
Umbrío cálido, no azulado: se aleja a propósito del azul marino de la web anterior, que
era un azul de pantalla y no de nave.

La razón es el posicionamiento, que la web ya dice con todas las letras: *«Consultoría
que no viene de un PowerPoint: viene de un almacén.»* Labopack opera su propio almacén
desde 2004 y escribe su propio WMS desde 2005.

De ahí salen tres consecuencias que mandan sobre todo lo demás:

- **El producto es el peso visual.** Una interfaz clara a pantalla completa sobre el
  fondo oscuro es lo que más pesa de la página, y es lo que se vende. La portada abre
  con una captura de LabopackWMS, no con tipografía sobre un fondo.
- **La brasa marca y dirige.** No decora, no hace degradados y no rellena fondos grandes.
- **La fuerza va en un solo sitio.** Lo que no es el titular o el producto, calla.

### Historia de esta decisión

El rediseño pasó primero por una dirección clara llamada «Muelle» (gris hormigón, rojo
teja, Archivo). Se descartó después de verla montada: hacía bien el trabajo de quitar
los rasgos de plantilla y ninguno el de dar presencia. **Quitar lo que sobra no es
diseñar.** Si alguna vez se plantea volver a una dirección clara, el problema a resolver
no es el gusto, es de dónde sale la energía visual.

## Paleta

```css
:root{
  --noche:#1C1613;        /* fondo de página: umbrío cálido, no azulado */
  --noche-2:#262019;      /* superficie elevada: cabecera, pie, bloques destacados */
  --crema:#E6DDD2;        /* texto principal: el crema del favicon */
  --apagado:#A3958A;      /* texto secundario */
  --linea:#3A2E26;        /* separadores decorativos */
  --linea-fuerte:#7A6656; /* bordes que delimitan un control */
  --brasa:#F0704A;        /* ÚNICO color de acento */
}
```

**Un solo acento: `--brasa`**, que es la parada alta del degradado del logo. No hay color
secundario, ni de éxito, ni de aviso. Si algo necesita destacar y la brasa ya está
ocupada, se destaca con peso, tamaño o espacio.

### Contraste comprobado

| Par | Ratio | Uso |
| --- | --- | --- |
| `--crema` sobre `--noche` | 13.33 | Texto corriente |
| `--crema` sobre `--noche-2` | 12.00 | Texto en superficie elevada |
| `--apagado` sobre `--noche` | 6.16 | Texto secundario |
| `--apagado` sobre `--noche-2` | 5.54 | Secundario en superficie |
| `--brasa` sobre `--noche` | 6.07 | Enlaces, cifras, acento |
| `--noche` sobre `--brasa` | 6.07 | Texto de botón sólido |
| `--linea-fuerte` sobre `--noche` | 3.29 | Borde de control (mínimo 3.0) |
| `--linea` sobre `--noche` | 1.36 | **Solo separadores decorativos** |

Dos reglas que salen de la medición y no son negociables:

- **`#D8451A` y `#AA2300` no se usan.** Las paradas media y baja del logo dan 4.08 y
  menos sobre `--noche`, por debajo de AA, y tampoco admiten texto encima. Se quedan en
  el logo.
- **`--linea` no puede delimitar un control.** A 1.36 solo vale para separar filas o
  bloques cuando el espaciado ya transmite la separación. Campos, botones fantasma y
  cualquier elemento interactivo usan `--linea-fuerte`.

## Tipografía

**Dos familias, claramente distintas.**

- **Fraunces** (serif variable, ejes SOFT, WONK y opsz) en titulares, cifras destacadas,
  la cita y el rótulo «Labopack». Es la voz de la dirección.
- **Instrument Sans** (variable, ejes de peso y anchura) en todo el texto corriente.

| | |
| --- | --- |
| Ficheros | `assets/fonts/fraunces-variable.woff2` (118 KB) y `assets/fonts/instrumentsans-variable.woff2` (56 KB), solo subset `latin` |
| Licencia | SIL Open Font License 1.1, en `assets/fonts/*-OFL.txt`. Permite alojarlas |
| Carga | `font-display: swap` y un `<link rel="preload">` por familia. **Nunca desde Google Fonts ni ningún tercero** |

El subset `latin-ext` **no** se incluye: todos los caracteres del español (á é í ó ú ñ ü
¿ ¡) están en `latin`.

### Escala

| Rol | Tamaño | Familia |
| --- | --- | --- |
| Titular de página (`h1`) | `clamp(2.35rem, 7.4vw, 5.4rem)` | Fraunces 500 |
| Titular de sección (`h2`) | `clamp(1.9rem, 3.4vw, 2.6rem)` | Fraunces 500 |
| Subtítulo (`h3`) | 1.25–1.35rem | Fraunces 500 |
| Entradilla | 1.16rem | Instrument Sans 400 |
| Texto corriente | 1rem (base 17px) | Instrument Sans 400 |
| Cifra destacada | `clamp(2rem, 4.4vw, 3.1rem)` | Fraunces 500 |
| Rótulo secundario | 0.95rem | Instrument Sans 500 |

- Las cifras llevan `font-variant-numeric: tabular-nums` siempre.
- Medida máxima de línea: **66 caracteres** en texto corriente, **16ch** en `h1`.
- `letter-spacing` negativo solo en titulares. En texto corriente, cero.

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
  `--noche` y `--crema`, con el módulo de acento en `--brasa`. Sin degradado.
- El rótulo «Labopack» **se compone con Fraunces** (peso 600, color `--brasa`), no con
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
10. **Ningún radio de esquina uniforme aplicado a todo.** El radio por defecto es **0**.
    Si un elemento concreto lo necesita, se justifica en su regla.
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
14. **Ningún fondo claro como base de página.** El fondo es `--noche`; la única
    superficie distinta es `--noche-2`, y solo para cabecera, pie y bloques destacados.
15. **Ninguna familia tipográfica además de Fraunces e Instrument Sans.**
16. **Ningún recurso de tercero.** Ni fuentes, ni scripts, ni píxeles, ni analítica.
17. **Ninguna imagen generada con IA ni foto de stock.**

## Referencias

El brief pedía dos o tres webs de referencia. **No se aportaron**, y la dirección se
eligió sobre el posicionamiento y la marca. Si llegan más adelante, se anotan aquí con
lo que se toma de cada una, y se revisa si obligan a corregir algo de lo anterior.
