"""
Proyecto 3 · Visualización I · Equipo Castro–Pulido
Lógica de datos de la app. No importa Streamlit a propósito: así puede probarse
aparte y las cifras de la app coinciden con las del notebook.

La app NO lee microdatos: lee las tablas agregadas que produce el notebook.
Son porcentajes y promedios ya ponderados, así que pueden publicarse sin exponer
registros individuales de la encuesta.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

MIN_N = 100
SMMLV_2026 = 1_750_905
NARANJA, AZUL, GRIS = "#EB6834", "#2A78D6", "#8A8A8A"

COLS_REGION = ["region", "informalidad_jefas", "jefas_ocupadas_mes",
               "jefas_informales_mes", "ingreso_medio_jefas", "n", "solo_capital"]
COLS_POS = ["region", "posicion", "informalidad", "n"]

# Etiquetas largas del modelo -> versión corta y en femenino para la audiencia
ETIQUETAS_POSICION = {
    "Empleado(a) particular": "Empleada de empresa privada",
    "Empleado(a) doméstico(a)": "Empleada doméstica",
    "Empleado(a) del gobierno": "Empleada del gobierno",
    "Cuenta propia": "Por cuenta propia",
    "Patrón(a) o empleador(a)": "Patrona o empleadora",
    "Jornalero(a) o peón": "Jornalera o peona",
    "Trabajador(a) sin remuneración": "Sin remuneración",
}


class DatosFaltantes(Exception):
    """La tabla no existe o no trae las columnas esperadas."""


def _leer(ruta: Path, columnas=None) -> pd.DataFrame:
    if not ruta.exists():
        raise DatosFaltantes(
            f"No encuentro «{ruta.name}». Ejecute el notebook de Python: "
            "genera las tablas dentro de la carpeta outputs/."
        )
    df = pd.read_csv(ruta, encoding="utf-8")
    if columnas:
        faltan = [c for c in columnas if c not in df.columns]
        if faltan:
            raise DatosFaltantes(
                f"«{ruta.name}» no trae las columnas {faltan}. "
                "Vuelva a generarla con la versión actual del notebook."
            )
    return df


def cargar_resumen(carpeta: Path) -> dict:
    """Indicadores nacionales, como diccionario."""
    df = _leer(Path(carpeta) / "p3_resumen_nacional.csv")
    if df.shape[1] < 2:
        raise DatosFaltantes("«p3_resumen_nacional.csv» debería tener indicador y valor.")
    return dict(zip(df.iloc[:, 0], pd.to_numeric(df.iloc[:, 1], errors="coerce")))


def cargar_regiones(carpeta: Path) -> pd.DataFrame:
    df = _leer(Path(carpeta) / "p3_por_region.csv", COLS_REGION)
    return df.sort_values("informalidad_jefas", ascending=False).reset_index(drop=True)


def cargar_hist_ingreso(carpeta: Path) -> pd.DataFrame:
    """Distribución del ingreso en tramos, para dibujarla de forma interactiva."""
    return _leer(Path(carpeta) / "p3_ingreso_hist.csv",
                 ["situacion", "ingreso", "porcentaje"])


def cargar_posicion_zona(carpeta: Path) -> pd.DataFrame:
    """Informalidad por tipo de empleo y zona."""
    df = _leer(Path(carpeta) / "p3_posicion_zona.csv",
               ["posicion", "zona", "informalidad", "n"])
    df["posicion"] = df["posicion"].map(lambda x: ETIQUETAS_POSICION.get(x, x))
    return df


def parametros(carpeta: Path) -> dict:
    df = _leer(Path(carpeta) / "p3_parametros.csv")
    return dict(zip(df.iloc[:, 0], pd.to_numeric(df.iloc[:, 1], errors="coerce")))


def cargar_posiciones(carpeta: Path) -> pd.DataFrame:
    df = _leer(Path(carpeta) / "p3_region_posicion.csv", COLS_POS)
    df["posicion"] = df["posicion"].map(lambda p: ETIQUETAS_POSICION.get(p, p))
    return df


def solo_capital(regiones: pd.DataFrame, nombre: str) -> bool:
    """True si en esa región la encuesta cubre solo las capitales."""
    return bool(fila_region(regiones, nombre)["solo_capital"])


def fila_region(regiones: pd.DataFrame, nombre: str) -> pd.Series:
    sub = regiones[regiones.region == nombre]
    if sub.empty:
        raise DatosFaltantes(f"No hay datos para «{nombre}».")
    return sub.iloc[0]


def muestra_pequena(regiones: pd.DataFrame, nombre: str, minimo: int = MIN_N) -> bool:
    return bool(fila_region(regiones, nombre)["n"] < minimo)


def extremos(regiones: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Región con más y con menos informalidad."""
    r = regiones.dropna(subset=["informalidad_jefas"])
    if r.empty:
        raise DatosFaltantes("La tabla de regiones no trae informalidad.")
    return r.iloc[0], r.iloc[-1]


def de_cada_diez(pct: float) -> str:
    """Traduce un porcentaje al lenguaje de la audiencia."""
    return f"{round(pct / 10)} de cada 10"


def cop(valor: float) -> str:
    """Pesos colombianos con punto de miles. El signo va antes: -$10.026."""
    signo = "-" if valor < 0 else ""
    return f"{signo}$" + f"{abs(valor):,.0f}".replace(",", ".")


def pct(valor: float, dec: int = 1) -> str:
    """Porcentaje con coma decimal, como se escribe en español."""
    return f"{valor:.{dec}f}".replace(".", ",") + " %"


def miles(valor: float) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def gran_idea(resumen: dict, regiones: pd.DataFrame) -> str:
    """La Gran Idea, armada con las cifras reales."""
    pct = resumen["informalidad_jefas_pct"]
    alta, baja = extremos(regiones)
    return (
        f"De cada 10 mujeres que sostienen un hogar con hijos menores y trabajan, "
        f"{round(pct / 10)} lo hacen sin cotizar a pensión ni a salud. "
        f"En {baja.region} son {de_cada_diez(baja.informalidad_jefas)}; "
        f"en {alta.region}, {de_cada_diez(alta.informalidad_jefas)}."
    )
