"""Sanea las cuatro capturas de LabopackWMS para labopack.com.

Cada dato de cliente se tapa y se reescribe con uno inventado, en la misma
fuente y tamano. Tambien se recorta el cromo de la ventana y la barra flotante
de captura.

Uso: python capturas.py <dir origen> <dir salida>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ORIG, SALIDA = sys.argv[1], sys.argv[2]
os.makedirs(SALIDA, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

REGULAR = "C:/Windows/Fonts/segoeui.ttf"
NEGRITA = "C:/Windows/Fonts/segoeuib.ttf"
_f = {}


def ft(ruta, px):
    _f.setdefault((ruta, px), ImageFont.truetype(ruta, px))
    return _f[(ruta, px)]


def bandas(im, x0, x1, y0, y1, umbral=200):
    """Detecta las filas de una tabla escaneando una columna en busca de tinta."""
    px = im.load()
    marcas = [any(sum(px[x, y]) / 3 < umbral for x in range(x0, x1, 2))
              for y in range(y0, y1)]
    out, ini = [], None
    for i, hay in enumerate(marcas):
        if hay and ini is None:
            ini = i
        elif not hay and ini is not None:
            if i - ini >= 3:
                out.append(y0 + ini)
            ini = None
    if ini is not None:
        out.append(y0 + ini)
    return out


class Captura:
    def __init__(self, nombre):
        self.im = Image.open(os.path.join(ORIG, nombre)).convert("RGB")
        self.d = ImageDraw.Draw(self.im)
        self.n = 0

    def tapar(self, caja, muestra=None):
        color = self.im.getpixel(muestra) if muestra else (255, 255, 255)
        self.d.rectangle(caja, fill=color)
        self.n += 1

    def poner(self, xy, texto, px=12, color=(64, 64, 64), negrita=False):
        self.d.text(xy, texto, font=ft(NEGRITA if negrita else REGULAR, px),
                    fill=color)

    def cambiar(self, caja, texto, px=12, color=(64, 64, 64), negrita=False,
                muestra=None, dy=0, dx=0):
        self.tapar(caja, muestra)
        self.poner((caja[0] + dx, caja[1] + dy), texto, px, color, negrita)

    def recortar(self, caja):
        self.im = self.im.crop(caja)
        self.d = ImageDraw.Draw(self.im)

    def guardar(self, nombre):
        r = os.path.join(SALIDA, nombre)
        self.im.save(r)
        print("  %-28s %4dx%-4d  %2d parches  %6.0f KB"
              % (nombre, self.im.width, self.im.height, self.n,
                 os.path.getsize(r) / 1024))


# ---------------------------------------------------------------- 1 · EDI 940
c = Captura("1.png")
GRIS = (90, 90, 90)
# Lista de ficheros: el subtitulo de cada fila lleva cliente y transportista.
for y, txt in ((486, "DISTRIBUCIONES AURORA (CENTRO SUR) · Rutas Levante · —"),
               (534, "DISTRIBUCIONES AURORA (CENTRO SUR) · Rutas Levante · —"),
               (581, "COMERCIAL MERIDIANO - CTR2-NORTE · Rutas Levante · —")):
    muestra = (640, y + 6) if y < 560 else (660, y + 6)
    c.cambiar((135, y, 470, y + 20), txt, px=12, color=GRIS, muestra=muestra, dy=3)
# Iniciales del avatar del panel derecho.
c.cambiar((700, 410, 728, 436), "CM", px=14, color=(255, 255, 255),
          negrita=True, muestra=(706, 416), dx=3, dy=3)
# Titulo del pedido.
c.cambiar((736, 406, 1010, 428), "COMERCIAL MERIDIANO - CTR2-NORTE", px=15,
          color=(33, 33, 33), negrita=True, dy=2)
# Linea de metadatos: transportista, poblacion, cliente, ordenes y PO.
c.tapar((694, 446, 1400, 466))
x = 694
for etiqueta, valor in (("Entrega", "— ()"), ("Transp.", "Rutas Levante"),
                        ("Poblac.", "GETAFE"), ("Cliente", "C100284"),
                        ("Órdenes", "2004518830"), ("PO", "demo-940")):
    c.poner((x, 449), etiqueta, px=11, color=(130, 130, 130))
    x += c.d.textlength(etiqueta, font=ft(REGULAR, 11)) + 5
    c.poner((x, 449), valor, px=11, color=(45, 45, 45), negrita=True)
    x += c.d.textlength(valor, font=ft(NEGRITA, 11)) + 16
# Descripcion del articulo de la linea.
c.cambiar((843, 554, 1060, 576), "CREMA HIDRATANTE 50 ml", px=12,
          color=(45, 45, 45), muestra=(1150, 565), dy=4)
# Fuera la barra de titulo, la barra flotante de captura y el pie con logos.
c.recortar((0, 60, 1920, 690))
c.guardar("wms-edi-940.png")

# ------------------------------------------------- 2 · Stock por SKU (3PL)
c = Captura("2.png")
DESC2 = [
    "01180952", "ALMOHADILLA INF 30U ESTUCHE",
    "CAJA EMBALAJE ALMOHADILLA INF 30 UND.", "ALMOHADILLA SUP 18U ESTUCHE ESP",
    "CAJA EMBALAJE ALMOHADILLA SUP 18 UND.", "ALMOHADILLA INF 18U ESTUCHE ESP",
    "CAJA EMBALAJE ALMOHADILLA INF 18 UND.", "ALMOHADILLA SUP 30U ESTUCHE",
    "CAJA EMBALAJE ALMOHADILLA SUP 30 UND.", "STOPPER PROMOCIONAL",
    "REGLETA EXPOSITORA EXTENSIBLE", "ALFOMBRILLA RATON JFM",
    "Etiqueta Símbolo reciclado amarillo", "TOTEM EXPOSITOR MOSTRADOR",
    "CAJA TIPO B", "CAJA TIPO C", "ETIQUETA SPRAY DESODORANTE PORTUGAL",
    "ETIQUETA GEL PH BALANCE PORTUGAL DELANTERA",
    "ETIQUETA GEL PH BALANCE PORTUGAL TRASERA",
    "ETIQUETA GEL DESODORANTE PORTUGAL DELANTERA",
    "ETIQUETA GEL DESODORANTE PORTUGAL TRASERA",
]
ACOND = "ALMACEN DE MATERIAL DE ACONDICIONAMIENTO"
ALM2 = [
    "Prod. Terminado España", ACOND + ", Depósito 2", ACOND, ACOND, ACOND,
    ACOND, " " + ACOND, ACOND + ", Depósito 2", ACOND,
    "Prod. Terminado España", "Prod. Terminado España", "Prod. Terminado España",
    "Prod. Terminado España", "Prod. Terminado España", ACOND, "Cuarentena",
    "Prod. Terminado España", "Cuarentena", "Cuarentena, Prod. Terminado España",
    "Cuarentena", "Cuarentena",
]
ys = bandas(c.im, 30, 105, 380, 1020)
for i, y in enumerate(ys):
    if i < len(DESC2):
        c.cambiar((215, y - 8, 862, y + 14), DESC2[i], px=12,
                  color=(55, 55, 55), dy=4)
    if i < len(ALM2):
        c.cambiar((1176, y - 8, 1860, y + 14), ALM2[i], px=12,
                  color=(55, 55, 55), dy=4)
c.recortar((0, 60, 1902, 998))
c.guardar("wms-stock-3pl.png")

# --------------------------------------------- 3 · Stock detalle (lote/caducidad)
c = Captura("3.png")
DESC3 = [
    "BLISTER ALMOHADILLA ADHESIVA INFERIOR",
    "BLISTER ALMOHADILLA ADHESIVA INFERIOR",
    "BLISTER ALMOHADILLA ADHESIVA INFERIOR",
    "ESTUCHE ALMOHADILLA SUPERIOR 18ct",
    "ESTUCHE ALMOHADILLA SUPERIOR 18ct",
    "ESTUCHE ALMOHADILLA SUPERIOR 30ct",
    "ESTUCHE ALMOHADILLA SUPERIOR 30ct",
    "EXPOSITOR MOSTRADOR SPRAY CORPORAL",
    "EXPOSITOR MOSTRADOR SPRAY CORPORAL",
    "EXPOSITOR SPRAY ANTIROZADURAS",
    "MUESTRA CREMA HIDRATANTE INTERNA",
    "GEL LIMPIADOR 118ml PRT", "GEL LIMPIADOR 118ml PRT",
    "PROMOCION DESODORANTE JAZMIN BLANCO",
    "PROMOCION JABON JAZMIN BLANCO",
    "LOCION CORPORAL 125ml 3dz 10/18",
]
ys = bandas(c.im, 30, 105, 370, 1025)
for i, y in enumerate(ys):
    if i < len(DESC3):
        c.cambiar((215, y - 9, 1240, y + 14), DESC3[i], px=12,
                  color=(55, 55, 55), dy=4)
c.recortar((0, 60, 1902, 988))
c.guardar("wms-lotes-farma.png")

# ------------------------------------------------------------- 4 · Android
c = Captura("4.png")
# El puntero del raton se quedo encima de una tarjeta.
c.tapar((220, 718, 242, 742), muestra=(300, 730))
# Fuera la ventana del emulador y lo que se cuela por los lados.
c.recortar((10, 28, 382, 874))
c.guardar("wms-android.png")
