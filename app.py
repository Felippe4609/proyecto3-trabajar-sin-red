"""
Proyecto 3 · Visualización I · Modalidad B · Equipo Castro–Pulido
Trabajar sin red: las mujeres que sostienen un hogar con hijos menores.

Recorre la historia en nueve pasos, en la secuencia del enunciado:
audiencia -> necesidad -> pregunta -> Gran Idea -> evidencia -> interpretación -> cierre.

Lee las tablas agregadas de outputs/, no microdatos. Ejecute antes el notebook.

ESTADO: escrita sin ejecutar (Streamlit no estaba disponible en el entorno de
preparación). Pruébela con `streamlit run app.py` antes de desplegar.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

import geih_core as gc

# =============================================================================
# COMPLETAR ANTES DE ENTREGAR
# =============================================================================
ENLACE_POWERBI = ""   # enlace de Power BI Service (el del Proyecto 1 sirve)
ENLACE_NOTEBOOK = ""  # Colab o repositorio
ENLACE_REPO = ""

EQUIPO = "Equipo Castro–Pulido"
INTEGRANTES = "David Castro y Felipe Pulido"
PERIODO = "enero a junio de 2026"

CARPETA = Path(__file__).parent
OUT = CARPETA / "outputs"

st.set_page_config(page_title="Trabajar sin red · GEIH 2026", page_icon="📊", layout="wide")

FUENTE = ("Fuente: DANE, Gran Encuesta Integrada de Hogares (GEIH) 2026, "
          f"{PERIODO}. Cálculos propios ponderados con el factor de expansión.")


@st.cache_data
def cargar():
    return (gc.cargar_resumen(OUT), gc.cargar_regiones(OUT), gc.cargar_posiciones(OUT))


try:
    resumen, regiones, posiciones = cargar()
except gc.DatosFaltantes as e:
    st.error(f"Todavía no puedo mostrar la historia.\n\n{e}")
    st.info("Ejecute el notebook, copie la carpeta `outputs/` junto a este archivo y recargue.")
    st.stop()

try:
    import plotly.express as px
except ImportError:
    st.error("Falta Plotly. Instálelo con: pip install -r requirements.txt")
    st.stop()

SECCIONES = [
    "1 · De qué se trata",
    "2 · La Gran Idea",
    "3 · Qué significa trabajar sin protección",
    "4 · Dónde vive cambia todo",
    "5 · De qué trabaja",
    "6 · Cuánto gana",
    "7 · Busque su caso",
    "8 · Qué no dicen estas cifras",
    "9 · Mensaje final y fuentes",
]

with st.sidebar:
    st.markdown("### Recorrido")
    seccion = st.radio("Secciones", SECCIONES, label_visibility="collapsed")
    st.divider()
    st.caption(f"{EQUIPO} · Visualización I")
    st.caption("Universidad Externado de Colombia")
    for etiqueta, url in [("Dashboard en Power BI", ENLACE_POWERBI),
                          ("Análisis en Python", ENLACE_NOTEBOOK),
                          ("Repositorio", ENLACE_REPO)]:
        if url:
            st.link_button(etiqueta, url, use_container_width=True)


def pie():
    st.caption(FUENTE)


def imagen(nombre: str, pie_foto: str, falta: str):
    ruta = OUT / nombre
    if ruta.exists():
        st.image(str(ruta), caption=pie_foto)
    else:
        st.info(falta)


# =============================================================================
if seccion == SECCIONES[0]:
    st.title("Trabajar sin red")
    st.subheader("Las mujeres que sostienen un hogar con hijos menores en Colombia")
    st.markdown(
        f"""
En Colombia **{gc.miles(resumen['jefas_ocupadas_mes'])} mujeres** son la cabeza de un hogar
con hijos menores de 18 años y además trabajan. Esta historia es sobre ellas.

Muchas no se llaman a sí mismas «trabajadoras informales». Dicen que trabajan por su cuenta,
que tienen un puesto, que hacen aseo por días. Pero si no cotizan a pensión ni a salud, el
día que se enferman o cuando lleguen a la vejez no hay nada detrás.

Estas cifras sirven para ver **qué tan común es esa situación, y qué parte de ella depende
del lugar donde se vive y del tipo de trabajo que se consigue.**
        """
    )
    st.info(
        "**La pregunta:** ¿qué tan frecuente es trabajar sin protección social entre las "
        "mujeres que sostienen un hogar con hijos menores, y en qué medida eso depende de "
        "la región y del tipo de empleo?"
    )
    st.caption("Recorra las secciones en orden con el menú de la izquierda.")

# =============================================================================
elif seccion == SECCIONES[1]:
    st.title("La Gran Idea")
    st.markdown(f"## {gc.gran_idea(resumen, regiones)}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Trabajan sin protección", f"{resumen['informalidad_jefas_pct']:.0f}%",
              help="De todas las jefas de hogar con hijos menores que trabajan")
    c2.metric("Son, en números", gc.miles(resumen["jefas_informales_mes"]),
              help="Promedio mensual de enero a junio de 2026")
    c3.metric("Ganan menos del mínimo", f"{resumen['jefas_bajo_smmlv_pct']:.0f}%",
              help=f"Salario mínimo 2026: {gc.cop(gc.SMMLV_2026)}")

    st.markdown(
        "Cotizar a pensión y a salud es lo que separa una enfermedad de una deuda, "
        "y la vejez de la pobreza. Por eso es el centro de esta historia."
    )
    pie()

# =============================================================================
elif seccion == SECCIONES[2]:
    st.title("Qué significa trabajar sin protección")
    st.markdown(
        """
Cuando el DANE dice que alguien trabaja de manera **informal**, no habla de trabajos ilegales
ni de calidad del trabajo. Habla de algo muy concreto:
        """
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
#### Si trabaja para alguien
Es informal si **su empleador no le paga pensión ni la tiene en salud contributiva**.
Da igual si lleva años en el puesto o si tiene un acuerdo de palabra.
            """
        )
    with c2:
        st.markdown(
            """
#### Si trabaja por su cuenta
Es informal si **su negocio no está registrado**. Una venta, un puesto o un oficio por días
sin registro entra en esta categoría.
            """
        )
    st.markdown(
        """
**Qué significa en la práctica:** sin semanas cotizadas no hay pensión al llegar a la vejez,
no hay incapacidad pagada si se enferma, y no hay licencia de maternidad.
        """
    )
    st.warning(
        "Dos aclaraciones. Primera: estar en el **régimen subsidiado de salud** (Sisbén) no "
        "es lo mismo que cotizar; para estas cifras sigue contando como trabajo informal. "
        "Segunda: estas cifras describen una situación, no juzgan a nadie."
    )

# =============================================================================
elif seccion == SECCIONES[3]:
    st.title("Dónde vive cambia todo")
    try:
        alta, baja = gc.extremos(regiones)
        st.markdown(
            f"## En {baja.region} son {gc.de_cada_diez(baja.informalidad_jefas)}. "
            f"En {alta.region}, {gc.de_cada_diez(alta.informalidad_jefas)}."
        )
    except gc.DatosFaltantes as e:
        st.warning(str(e))

    c1, c2 = st.columns([3, 2])
    with c1:
        imagen("p3_mapa_regiones.png", "Informalidad de las jefas de hogar, por región",
               "Falta el mapa. Ejecute el script de R: genera `p3_mapa_regiones.png`.")
    with c2:
        fig = px.bar(
            regiones.sort_values("informalidad_jefas"),
            x="informalidad_jefas", y="region", orientation="h",
            hover_data={"jefas_ocupadas_mes": ":,.0f", "ingreso_medio_jefas": ":,.0f", "n": True},
            labels={"informalidad_jefas": "% en trabajo informal", "region": ""},
        )
        fig.update_traces(marker_color=gc.NARANJA)
        fig.update_layout(height=400, margin=dict(t=30), xaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Pase el cursor para ver cuántas mujeres y cuánto ganan en cada región.")

    st.markdown(
        "**Cómo leerlo.** El mapa no dice que una región cause informalidad. Dice que la "
        "estructura del empleo es distinta en cada una: dónde hay más empleo asalariado "
        "registrado, hay menos informalidad."
    )
    pie()

# =============================================================================
elif seccion == SECCIONES[4]:
    st.title("De qué trabaja")
    st.markdown("## El tipo de empleo pesa más que el esfuerzo individual")
    imagen("p3_fig2_posicion.png",
           "Informalidad según tipo de empleo y zona",
           "Falta `p3_fig2_posicion.png`. Ejecute el notebook.")
    st.markdown(
        """
Trabajar por cuenta propia es la puerta de entrada más común y, a la vez, la que casi nunca
trae protección. El empleo doméstico está en una situación parecida. El empleo en una empresa
privada es el que más protege, y aun así fuera de las cabeceras protege mucho menos.

**Esto no significa que baste con cambiar de empleo.** Significa que la diferencia no se
explica por el empeño de cada quien, sino por el tipo de puesto al que se puede acceder.
        """
    )
    pie()

# =============================================================================
elif seccion == SECCIONES[5]:
    st.title("Cuánto gana")
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingreso medio de las jefas", gc.cop(resumen["ingreso_medio_jefas"]))
    c2.metric("Ingreso medio de los jefes", gc.cop(resumen["ingreso_medio_jefes"]),
              help="Hombres cabeza de hogar con hijos menores, en la misma situación")
    c3.metric("Diferencia", f"{resumen['brecha_ingresos_pct']:.1f}% menos")

    imagen("p3_fig1_ingreso.png",
           f"Ingreso laboral mensual frente al salario mínimo ({gc.cop(gc.SMMLV_2026)})",
           "Falta `p3_fig1_ingreso.png`. Ejecute el notebook.")
    st.markdown(
        f"""
**{resumen['jefas_bajo_smmlv_pct']:.0f} de cada 100** jefas de hogar con hijos menores ganan
menos de un salario mínimo al mes. En el trabajo formal, los ingresos se concentran justo en
el salario mínimo; en el informal, se reparten muy por debajo.

La diferencia con los hombres en la misma situación familiar es de
**{resumen['brecha_ingresos_pct']:.1f} %**. Esa diferencia **no es** una medida de
discriminación salarial: no compara el mismo cargo con la misma jornada.
        """
    )
    pie()

# =============================================================================
elif seccion == SECCIONES[6]:
    st.title("Busque su caso")
    st.markdown("Elija su región y vea cómo cambia la situación según el tipo de empleo.")

    region = st.selectbox("Región", list(regiones.region))
    fila = gc.fila_region(regiones, region)

    if gc.solo_capital(regiones, region):
        st.warning(
            f"En {region} la encuesta cubre principalmente las capitales, y es la región con "
            f"menos casos ({int(fila['n'])}). Estas cifras no representan bien las zonas "
            "alejadas de las capitales."
        )
    elif gc.muestra_pequena(regiones, region):
        st.warning(
            f"En {region} la encuesta tiene pocos casos ({int(fila['n'])}). "
            "Tome estas cifras como una señal aproximada."
        )

    c1, c2, c3 = st.columns(3)
    c1.metric("Trabajan sin protección", f"{fila['informalidad_jefas']:.0f}%",
              delta=f"{fila['informalidad_jefas'] - resumen['informalidad_jefas_pct']:+.0f} pp frente al país",
              delta_color="inverse")
    c2.metric("Jefas de hogar que trabajan", gc.miles(fila["jefas_ocupadas_mes"]))
    c3.metric("Ingreso medio", gc.cop(fila["ingreso_medio_jefas"]))

    sub = posiciones[posiciones.region == region]
    if sub.empty:
        st.info(f"No hay desglose por tipo de empleo para {region} con muestra suficiente.")
    else:
        fig = px.bar(sub.sort_values("informalidad"), x="informalidad", y="posicion",
                     orientation="h", hover_data={"n": True},
                     labels={"informalidad": "% en trabajo informal", "posicion": ""},
                     title=f"Tipo de empleo en {region}")
        fig.update_traces(marker_color=gc.NARANJA)
        fig.update_layout(height=320, xaxis_range=[0, 100], margin=dict(t=50))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Solo se muestran los grupos con 30 o más casos encuestados.")

    with st.expander("Ver la tabla de todas las regiones"):
        st.dataframe(regiones, use_container_width=True, hide_index=True)
        st.download_button("Descargar la tabla (CSV)",
                           regiones.to_csv(index=False).encode("utf-8"),
                           file_name="informalidad_jefas_por_region.csv", mime="text/csv")
    pie()

# =============================================================================
elif seccion == SECCIONES[7]:
    st.title("Qué no dicen estas cifras")
    st.markdown(
        f"""
- **Describen, no explican.** Que una región tenga más informalidad no dice por qué, ni
  permite evaluar programas del Gobierno.
- **La diferencia de ingresos de {resumen['brecha_ingresos_pct']:.1f} % no mide discriminación
  salarial.** No compara el mismo cargo, con la misma jornada y experiencia.
- **Son un promedio de {PERIODO}**, no una tendencia ni una proyección.
- **Vienen de una encuesta, no de un censo.** Cada cifra tiene un margen de error que aquí no
  se calculó, así que diferencias pequeñas entre regiones pueden no ser reales. Pacífica y
  Caribe están a medio punto de distancia: son las dos regiones con mayor informalidad, pero
  no se puede afirmar cuál encabeza la lista.
- **Orinoquía-Amazonía** es la región con menos casos encuestados, y allí la encuesta cubre
  sobre todo las capitales.
- **El ingreso es el que cada persona reporta**, y se calcula solo sobre quienes declaran un
  ingreso mayor que cero.
        """
    )
    st.info("Si una cifra le sorprende, contrástela con los boletines del DANE antes de usarla.")

# =============================================================================
elif seccion == SECCIONES[8]:
    st.title("Mensaje final")
    st.markdown(
        f"""
## Que su situación sea común no la hace normal

{gc.miles(resumen['jefas_informales_mes'])} mujeres en Colombia sostienen un hogar con hijos
menores trabajando sin pensión ni salud contributiva. No es un caso aislado ni una falla
personal: depende en buena medida del tipo de empleo disponible y del lugar donde se vive.

Saberlo sirve para dos cosas. Para **reconocer qué cambia** si se consigue un empleo con
cotización, o si un negocio propio se registra. Y para **pedir cuentas con datos** cuando se
discuta qué hace el Estado por los hogares que dependen del ingreso de una sola persona.
        """
    )
    st.divider()
    st.markdown("### Fuentes y definiciones")
    st.markdown(
        f"""
- **Fuente:** DANE, Gran Encuesta Integrada de Hogares (GEIH) 2026, marco 2018. Microdatos de
  {PERIODO}, módulos *Características generales* y *Ocupados*.
- **Jefa de hogar con hijos menores:** mujer registrada como jefa del hogar, en un hogar donde
  vive al menos un hijo o hija menor de 18 años.
- **Trabajo informal:** definición del DANE. Asalariadas y empleadas domésticas que no cotizan
  a pensión ni están en régimen contributivo o especial de salud; independientes cuyo negocio
  no tiene registro; trabajadoras sin remuneración.
- **Contraste:** el DANE publicó 54,5 % de informalidad nacional para abril–junio de 2026;
  este análisis reproduce {resumen['informalidad_nacional_q2_pct']:.2f} %.
- **Conteos de personas:** promedio mensual. Sumar los seis meses contaría seis veces a las
  mismas personas.
- **Herramientas:** Power BI, Python (Seaborn y Plotly) y R (sf y ggplot2).
- **Uso de IA:** ver el anexo técnico incluido en los entregables.
        """
    )
    st.caption(f"{EQUIPO} · {INTEGRANTES} · Visualización I · Universidad Externado de Colombia")
