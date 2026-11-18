"""
Sistema de color del Proyecto 3 y verificación de contraste (WCAG 2.1).

Tres modos:
  estandar   — la identidad del Proyecto 1 (naranja terracota y azul)
  daltonismo — paleta Okabe-Ito, diseñada para deuteranopía y protanopía
  contraste  — máximo contraste, para baja visión

La escala secuencial es de un solo tono (ámbar a terracota): una escala de tono
único se percibe igual con cualquier tipo de daltonismo, porque la información
está en la luminosidad y no en el matiz.
"""

PALETAS = {
    "estandar": {
        "foco": "#EB6834",       # jefas de hogar (viene del Proyecto 1)
        "comparacion": "#2A78D6",  # jefes / zona urbana
        "serie": ["#EB6834", "#2A78D6", "#1B8A6B", "#9B5DE5", "#A8763E", "#6B7280"],
    },
    "daltonismo": {
        "foco": "#D55E00",       # bermellón Okabe-Ito
        "comparacion": "#0072B2",  # azul Okabe-Ito
        "serie": ["#D55E00", "#0072B2", "#009E73", "#CC79A7", "#E69F00", "#56565B"],
    },
    "contraste": {
        # Separados por LUMINOSIDAD, no por matiz: así se distinguen con cualquier
        # tipo de daltonismo, e incluso impresos en blanco y negro.
        "foco": "#A63603",
        "comparacion": "#9ECAE1",   # claro a propósito; se dibuja con borde oscuro
        "serie": ["#7F2704", "#9ECAE1", "#00441B", "#C7C7C7", "#D55E00", "#2B2B2B"],
    },
}

# Escala secuencial de un solo tono, de ámbar claro a terracota.
SECUENCIAL = ["#FFF5EB", "#FEE0C4", "#FDBE8B", "#F79044", "#DD5F12", "#A63603"]

TINTA = "#1F2328"      # texto principal
SUAVE = "#5B6168"      # texto secundario
BORDE = "#E6E1DD"
PAPEL = "#FFFFFF"
CREMA = "#FBF4EF"      # fondo de tarjetas


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminancia(hexa):
    h = hexa.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contraste(a, b):
    """Razón de contraste WCAG entre dos colores (1 a 21)."""
    la, lb = luminancia(a), luminancia(b)
    claro, oscuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (oscuro + 0.05)


if __name__ == "__main__":
    print("CONTRASTE CONTRA FONDO BLANCO (WCAG: 4,5 texto normal · 3,0 texto grande y gráficos)")
    print(f"{'color':>14}  {'contraste':>9}  cumple")
    for nombre, c in [("tinta", TINTA), ("suave", SUAVE)] + \
                     [(f"{m}/foco", PALETAS[m]["foco"]) for m in PALETAS] + \
                     [(f"{m}/comp", PALETAS[m]["comparacion"]) for m in PALETAS]:
        r = contraste(c, PAPEL)
        marca = "AA texto" if r >= 4.5 else ("AA gráficos" if r >= 3 else "NO CUMPLE")
        print(f"{nombre:>14}  {r:9.2f}  {marca}")

    print()
    print("SEPARACIÓN POR LUMINOSIDAD ENTRE LOS DOS COLORES PRINCIPALES")
    print("(si es alta, se distinguen con cualquier daltonismo y también en blanco y negro)")
    for modo in PALETAS:
        a, b = PALETAS[modo]["foco"], PALETAS[modo]["comparacion"]
        r = contraste(a, b)
        print(f"  {modo:11} {r:5.2f}  {'se separan por claridad' if r >= 3 else 'se separan solo por matiz: conviene reforzar con tramas'}")

    print()
    print("ESCALA SECUENCIAL: texto legible encima de cada tramo")
    for c in SECUENCIAL:
        cb, cn = contraste(c, "#FFFFFF"), contraste(c, TINTA)
        print(f"  {c}  blanco {cb:5.2f} · tinta {cn:5.2f}  -> usar "
              f"{'blanco' if cb > cn else 'tinta'}")
