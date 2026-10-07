# labopack-web

Sitio estático de Labopack, S.L. Se publica en labopack.com desde la rama `master`
mediante GitHub Pages (`CNAME`). **El repositorio es público.**

## Stack

HTML estático escrito a mano. Sin build, sin frameworks, sin gestor de paquetes.
10 páginas, una hoja de estilos (`assets/styles.css`) y nada más.

El único `<script>` de cada página es `application/ld+json`: datos estructurados que
el navegador no ejecuta. **No hay JavaScript ejecutable en el sitio y no debe haberlo.**

Todos los recursos se cargan con rutas absolutas (`/assets/styles.css`), así que abrir
un `.html` con doble clic no aplica estilos. Hay que servir desde la raíz del repo.

## Restricciones

Valen para cualquier cambio, no solo para el rediseño en curso.

- **No se tocan** los textos, el `<head>` (title, description, canonical, Open Graph,
  JSON-LD), las URLs, `sitemap.xml`, `robots.txt` ni `CNAME`. Única excepción admitida
  en el `<head>`: precargas de fuentes propias.
- **Sin build, sin frameworks, sin JavaScript.**
- **Sin recursos de terceros**: ni fuentes, ni scripts, ni píxeles, ni analítica.
  Todo se sirve desde `/assets/`.
- **Sin imágenes generadas con IA ni fotos de stock.** Si falta material real, se deja
  el hueco marcado con su proporción.
- **Nada de datos de clientes** en archivos nuevos (código, capturas o documentación):
  el repositorio es público.

## Servir en local

    python -m http.server 8080

Y abrir <http://localhost:8080/>.

## Rediseño en curso

Trabajo en la rama `rediseno`. No se fusiona sin aprobación.

- El encargo completo, por fases: [`docs/brief-rediseno.md`](docs/brief-rediseno.md).
- La identidad visual (paleta, tipografía, retícula, prohibiciones) se fija en
  `.claude/skills/labopack-design/SKILL.md`. **Es la fuente de verdad del diseño:**
  léela antes de tocar el CSS o el marcado.
- Capturas de antes y después en `docs/rediseno/`.
