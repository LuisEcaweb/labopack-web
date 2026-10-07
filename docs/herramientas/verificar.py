"""Comprobaciones de la fase 5 sobre las 10 paginas.

1. Contenido intacto: el <head> y el texto visible, contra la rama master.
2. Patrones prohibidos de la skill, buscados en el HTML y el CSS finales.
3. Peso de transferencia por pagina.

Uso: python -I verificar.py <raiz del repo>
Devuelve codigo 1 si algo falla.
"""
import io
import os
import re
import sys
import glob
import difflib
import subprocess
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = sys.argv[1]
os.chdir(RAIZ)

EMOJI = re.compile("[\U0001F000-\U0001FAFF⌀-➿⬀-⯿️]")
FLECHA = "→"
PAGINAS = sorted(p.replace(os.sep, "/") for p in glob.glob("**/*.html", recursive=True))

fallos = []
PIES = {}


def master(ruta):
    r = subprocess.run(["git", "show", "master:" + ruta], capture_output=True)
    return r.stdout.decode("utf-8")


def cabeza(h):
    m = re.search(r"<head>(.*?)</head>", h, re.S)
    return [l.strip() for l in m.group(1).splitlines() if l.strip()]


def visible(h):
    b = re.search(r"<body.*?</body>", h, re.S).group(0)
    b = re.sub(r"<script.*?</script>", " ", b, flags=re.S)
    b = re.sub(r"<[^>]+>", " ", b)
    b = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), b).replace("&nbsp;", " ")
    b = b.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    return re.sub(r"\s+", " ", b).strip()


# ---------------------------------------------------------------- 1. Contenido
print("=" * 78)
print("1. CONTENIDO INTACTO  (head y texto visible, contra master)")
print("=" * 78)

for pagina in PAGINAS:
    antes, ahora = master(pagina), io.open(pagina, encoding="utf-8").read()

    # --- el <head> ---
    dif = [l for l in difflib.unified_diff(cabeza(antes), cabeza(ahora), lineterm="")
           if l[:1] in "+-" and l[:3] not in ("---", "+++")]
    malas = [l for l in dif
             if not (l.startswith("+") and 'rel="preload"' in l and "font" in l)]

    # --- el texto visible ---
    # Del original se descuentan emojis, flechas y el antetitulo: lo autorizado.
    # El antetitulo se quita del HTML, por posicion. Quitarlo del texto plano por
    # coincidencia borraria la primera aparicion de la palabra, que en /contacto/
    # y /sectores/ es el enlace del menu y no el antetitulo.
    antes_sin_kicker = re.sub(r'<p class="kicker">.*?</p>', "", antes, flags=re.S)
    va = EMOJI.sub("", visible(antes_sin_kicker))
    va = re.sub(r"\s+", " ", va).strip()
    # Las capturas de LabopackWMS son material nuevo que el brief autoriza, y su
    # <figcaption> es texto visible que no estaba en master. Se descuenta del
    # lado nuevo y se lista aparte para que no pase desapercibido.
    ahora_sin_figuras = re.sub(r'<figure class="(?:captura|hueco).*?</figure>', "",
                               ahora, flags=re.S)
    PIES[pagina] = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).strip()
                    for c in re.findall(
                        r'<figure class="captura.*?<figcaption>(.*?)</figcaption>',
                        ahora, flags=re.S)]
    vb = visible(ahora_sin_figuras)
    # La marca pasa de alt de imagen a texto: aporta "Labopack" visible.
    vb_norm = vb.replace("Labopack ", "", 1) if vb.startswith("Labopack ") else vb
    # Las flechas de enlace desaparecen de ambos lados para comparar.
    va_norm = re.sub(r"\s*" + FLECHA + r"\s*", " ", va)
    va_norm = re.sub(r"\s+", " ", va_norm).strip()
    vb_cmp = re.sub(r"\s*" + FLECHA + r"\s*", " ", vb_norm)
    vb_cmp = re.sub(r"\s+", " ", vb_cmp).strip()

    ok_head = not malas
    ok_texto = va_norm == vb_cmp
    marca = "OK " if (ok_head and ok_texto) else "!! "
    print("  %s%-48s head:%s  texto:%s"
          % (marca, pagina, "ok" if ok_head else "DIFIERE", "ok" if ok_texto else "DIFIERE"))
    if malas:
        fallos.append(pagina + " head")
        for l in malas:
            print("        " + l[:120])
    if not ok_texto:
        fallos.append(pagina + " texto")
        sm = difflib.SequenceMatcher(None, va_norm, vb_cmp)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal":
                print("        %s  -%r  +%r" % (tag, va_norm[i1:i2][:90], vb_cmp[j1:j2][:90]))

# ------------------------------------------------------------ 2. Prohibiciones
print()
if any(PIES.values()):
    print("  Pies de las capturas (texto visible nuevo, autorizado por el brief):")
    for k, v in PIES.items():
        for pie in v:
            print("     %-26s %s" % (k.split("/")[-2] or "raiz", pie[:84]))
print()
print("=" * 78)
print("2. PATRONES PROHIBIDOS  (skill labopack-design)")
print("=" * 78)

css = io.open("assets/styles.css", encoding="utf-8").read()
PERMITIDAS = ("Fraunces", "Instrument Sans", "inherit", "Georgia", "serif",
              "system-ui", "sans-serif")
FAMILIAS = [f for f in re.findall(r"font-family:\s*([^;]+)", css)
            if not any(x in f for x in PERMITIDAS)]
RADIO_OK = ("var(--radio)", "999px", "18px", "0")
RADIOS_SUELTOS = [v.strip() for v in re.findall(r"border-radius:\s*([^;]+);", css)
                  if v.strip() not in RADIO_OK]
_mb = re.search(r"\nbody \{(.*?)\n\}", css, re.S)
_bg = re.search(r"background:\s*([^;]+);", _mb.group(1)) if _mb else None
FONDO_BODY = _bg.group(1).strip() if _bg else None
cuerpos = {}
for pagina in PAGINAS:
    h = io.open(pagina, encoding="utf-8").read()
    cuerpos[pagina] = re.search(r"<body.*?</body>", h, re.S).group(0)
todos = "\n".join(cuerpos.values())

REGLAS = [
    ("1  emoji como icono", lambda: {p: EMOJI.findall(c) for p, c in cuerpos.items() if EMOJI.search(c)}),
    ("2  flecha en enlace o boton",
     lambda: {p: re.findall(r"<a\b[^>]*>[^<]*" + FLECHA + r"[^<]*</a>", c)
              for p, c in cuerpos.items() if re.search(r"<a\b[^>]*>[^<]*" + FLECHA, c)}),
    ("3  antetitulo en mayusculas", lambda: _css(r"text-transform:\s*uppercase") or _html(r'class="[^"]*kicker')),
    ("4  palabra resaltada en h1", lambda: _html(r'class="hl"')),
    ("5  franja de 4 columnas", lambda: _css(r"\.stats[^{]*\{[^}]*repeat\(4")),
    ("6  degradado", lambda: _css(r"(?:linear|radial)-gradient")),
    ("7  desenfoque", lambda: _css(r"backdrop-filter|\bblur\(")),
    ("8  elevacion al hover", lambda: _css(r":hover[^{]*\{[^}]*translateY")),
    ("9  sombra gris difusa", lambda: _css(r"box-shadow")),
    # El radio es deliberado en tarjetas (--radio) y botones (pastillas); lo que
    # se vigila es que no aparezca ningun otro valor suelto.
    # Se filtra en Python, no con un lookahead: "\s*" puede retroceder a cero
    # caracteres y colocar el lookahead antes del espacio, con lo que pasaria
    # siempre y la comprobacion marcaria valores correctos.
    ("10 radio fuera de tarjetas y botones",
     lambda: ({"assets/styles.css": RADIOS_SUELTOS} if RADIOS_SUELTOS else {})),
    ("13 tipografia monoespaciada", lambda: _css(r"monospace")),
    # Se comprueba el valor, no la ausencia: "body" tambien casa con .case-body.
    ("14 fondo claro de pagina", lambda: {} if FONDO_BODY == "var(--marino)"
     else {"assets/styles.css": ["body background = " + str(FONDO_BODY)]}),
    ("15 otra familia que las dos",
     lambda: ({"assets/styles.css": [f.strip() for f in FAMILIAS]} if FAMILIAS else {})),
    ("16 recurso de tercero",
     lambda: {p: re.findall(r'(?:src|href)="https?://(?!www\.ecaweb\.es|www\.linkedin\.com)[^"]*', c)
              for p, c in cuerpos.items()
              if re.search(r'(?:src|href)="https?://(?!www\.ecaweb\.es|www\.linkedin\.com)', c)}),
    # "stock" a secas significa existencias en esta web; se busca la procedencia,
    # no la palabra.
    ("17 imagen de stock o generada",
     lambda: _html(r"unsplash|pexels|shutterstock|gettyimages|istockphoto|freepik"
                   r"|adobe\.?stock|stock\s*photo|foto\s*de\s*stock")),
]


def _css(patron):
    hits = re.findall(patron, css)
    return {"assets/styles.css": hits} if hits else {}


def _html(patron):
    out = {}
    for p, c in cuerpos.items():
        hits = re.findall(patron, c)
        if hits:
            out[p] = hits
    return out


for nombre, fn in REGLAS:
    hits = fn()
    if hits:
        fallos.append("prohibicion " + nombre)
        total = sum(len(v) for v in hits.values())
        print("  !! %-32s %d coincidencias" % (nombre, total))
        for p, v in list(hits.items())[:3]:
            print("        %s  %s" % (p, str(v[:3])[:110]))
    else:
        print("  OK %-32s limpio" % nombre)

# ------------------------------------------------------------------- 3. Peso
print()
print("=" * 78)
print("3. PESO DE TRANSFERENCIA  (sin comprimir; tope 400 KB)")
print("=" * 78)

COMUN = ["assets/styles.css", "assets/fonts/instrumentsans-variable.woff2",
         "assets/fonts/fraunces-variable.woff2", "assets/logo-icono.svg",
         "assets/favicon.svg", "assets/matriz.svg"]
base = sum(os.path.getsize(f) for f in COMUN)
for pagina in PAGINAS:
    peso = os.path.getsize(pagina) + base
    _html = io.open(pagina, encoding="utf-8").read()
    if "ecaweb-logo.png" in _html:
        peso += os.path.getsize("assets/ecaweb-logo.png")
    # Las capturas de producto cuentan: son lo mas pesado de la pagina.
    for _c in set(re.findall(r'/assets/capturas/([^"\s]+)', _html)):
        peso += os.path.getsize(os.path.join("assets/capturas", _c))
    estado = "OK" if peso <= 400 * 1024 else "!!"
    if peso > 400 * 1024:
        fallos.append(pagina + " peso")
    print("  %s %-48s %6.1f KB" % (estado, pagina, peso / 1024))

print()
print("=" * 78)
if fallos:
    print("FALLAN %d comprobaciones: %s" % (len(fallos), ", ".join(fallos)))
    sys.exit(1)
print("Las tres comprobaciones pasan en las %d paginas." % len(PAGINAS))
