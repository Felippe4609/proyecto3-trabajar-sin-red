"""
Proyecto 3 · Visualización I · Equipo Castro–Pulido
Trabajar sin red: las mujeres que sostienen un hogar con hijos menores.

Producto digital narrativo (modalidad B). Recorre la historia en nueve pasos:
audiencia -> necesidad -> pregunta -> Gran Idea -> evidencia -> interpretación -> cierre.

Lee tablas agregadas de outputs/, no microdatos.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

import estilo
import geih_core as gc
from paleta import PALETAS, SECUENCIAL, SUAVE, TINTA

# ─────────────────────────────── completar antes de entregar
ENLACE_POWERBI = ""   # enlace del dashboard en Power BI Service
ENLACE_REPO = "https://github.com/Felippe4609/proyecto3-trabajar-sin-red"
ENLACE_NOTEBOOK = ""  # Colab o enlace al cuaderno

PERIODO = "enero a junio de 2026"
OUT = Path(__file__).parent / "outputs"

st.set_page_config(page_title="Trabajar sin red · Jefas de hogar en Colombia",
                   page_icon="📊", layout="wide",
                   initial_sidebar_state="expanded")

FUENTE = (f"Fuente: DANE, Gran Encuesta Integrada de Hogares (GEIH) {PERIODO}. "
          "Cálculos propios ponderados con el factor de expansión FEX_C18.")


@st.cache_data
def cargar():
    return (gc.cargar_resumen(OUT), gc.cargar_regiones(OUT), gc.cargar_posiciones(OUT),
            gc.cargar_posicion_zona(OUT), gc.cargar_hist_ingreso(OUT), gc.parametros(OUT))


try:
    resumen, regiones, posiciones, pos_zona, hist, param = cargar()
except gc.DatosFaltantes as e:
    st.error(f"Todavía no puedo mostrar la historia.\n\n{e}")
    st.stop()

try:
    import plotly.express as px
except ImportError:
    st.error("Falta Plotly. Instálelo con: pip install -r requirements.txt")
    st.stop()

SECCIONES = ["1 · De qué se trata", "2 · La Gran Idea",
             "3 · Qué significa trabajar sin protección", "4 · Dónde vive cambia todo",
             "5 · De qué trabaja", "6 · Cuánto gana", "7 · Busque su caso",
             "8 · Qué no dicen estas cifras", "9 · Mensaje final y fuentes"]

MODOS = {"Estándar": "estandar",
         "Daltonismo (deuteranopía y protanopía)": "daltonismo",
         "Alto contraste": "contraste"}

# ─────────────────────────────── estado del recorrido
if "seccion" not in st.session_state:
    st.session_state.seccion = SECCIONES[0]


def mover(pasos):
    """Avanza o retrocede un paso. Lo usan las flechas del navegador."""
    i = SECCIONES.index(st.session_state.seccion) + pasos
    st.session_state.seccion = SECCIONES[max(0, min(i, len(SECCIONES) - 1))]


with st.sidebar:
    st.markdown("### Accesibilidad")
    nombre_modo = st.selectbox(
        "Paleta de colores", list(MODOS),
        help="Cambia los colores de todas las gráficas interactivas de esta página.")
    modo = MODOS[nombre_modo]
    tramas = st.toggle(
        "Reforzar con tramas", value=(modo != "estandar"),
        help="Añade texturas además del color. Así la información no depende solo "
             "del color: también se distingue por el dibujo, e incluso impresa en "
             "blanco y negro.")
    st.caption("Las cifras no cambian con estas opciones; solo cambia cómo se ven.")

    st.divider()
    for etiqueta, url in [("Dashboard en Power BI", ENLACE_POWERBI),
                          ("Código en GitHub", ENLACE_REPO),
                          ("Análisis en Python", ENLACE_NOTEBOOK)]:
        if url:
            st.link_button(etiqueta, url, use_container_width=True)
    st.caption(f"{estilo.EQUIPO}\n\n{estilo.CURSO}")

P = PALETAS[modo]
FOCO, COMP, SERIE = P["foco"], P["comparacion"], P["serie"]
BORDE_BARRA = TINTA if modo == "contraste" else "rgba(0,0,0,0)"
TRAMAS = ["", "/", "x", "-", "\\", "+"] if tramas else [""]

st.markdown(estilo.css(FOCO), unsafe_allow_html=True)

# ─────────────────────────────── navegador: un unico control para todo el recorrido
_atras, _centro, _adelante = st.columns([1, 12, 1], vertical_alignment="center")
_atras.button("←", key="paso_atras", on_click=mover, args=(-1,),
              disabled=(st.session_state.seccion == SECCIONES[0]),
              use_container_width=True, help="Paso anterior")
seccion = _centro.selectbox("Paso del recorrido", SECCIONES, key="seccion",
                            label_visibility="collapsed")
_adelante.button("→", key="paso_adelante", on_click=mover, args=(1,),
                 disabled=(st.session_state.seccion == SECCIONES[-1]),
                 use_container_width=True, help="Paso siguiente")
paso = SECCIONES.index(seccion) + 1
st.caption(f"Paso {paso} de {len(SECCIONES)} · avance y retroceda con las flechas, "
           "o abra la lista para ir directo a un paso.")

alta, baja = gc.extremos(regiones)


def estilizar(fig, alto=430):
    fig.update_layout(
        height=alto, plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Source Sans Pro, system-ui, sans-serif", size=14, color=TINTA),
        margin=dict(t=30, b=50, l=10, r=20),
        legend=dict(title_text="", orientation="h", yanchor="bottom", y=-0.22),
        xaxis=dict(gridcolor="#EEE9E5"), yaxis=dict(gridcolor="#EEE9E5"))
    fig.update_traces(marker_line_color=BORDE_BARRA, marker_line_width=1.2)
    return fig


def imagen(nombre, pie, falta):
    ruta = OUT / nombre
    if ruta.exists():
        st.image(str(ruta), caption=pie)
    else:
        st.warning(falta)


# ─────────────────────────────── 1
if seccion == SECCIONES[0]:
    estilo.cabecera(
        st, "Trabajar sin red",
        "Las mujeres que sostienen un hogar con hijos menores en Colombia, "
        "y qué tan común es que trabajen sin pensión ni salud.")
    izq, der = st.columns([3, 2], gap="large")
    with izq:
        st.markdown(
            f"""<div class="entradilla">
            En Colombia <b>{gc.miles(resumen['jefas_ocupadas_mes'])} mujeres</b> son la
            cabeza de un hogar con hijos menores de 18 años y además trabajan.
            Esta historia es sobre ellas.<br><br>
            Muchas no se llaman a sí mismas «trabajadoras informales». Dicen que trabajan
            por su cuenta, que tienen un puesto, que hacen aseo por días. Pero si no
            cotizan a pensión ni a salud, el día que se enferman o cuando lleguen a la
            vejez no hay nada detrás.
            </div>""", unsafe_allow_html=True)
    with der:
        st.markdown(
            f"""<div class="tarjeta">
            <div class="rotulo"><b>La pregunta</b></div>
            <div class="rotulo" style="margin-top:.5rem">
            ¿Qué tan frecuente es trabajar sin protección social entre las mujeres que
            sostienen un hogar con hijos menores, y en qué medida depende de la región
            y del tipo de empleo?</div>
            <div class="pie">Recorra las secciones en orden con el menú de la izquierda.</div>
            </div>""", unsafe_allow_html=True)
    estilo.fuente(st, FUENTE)

# ─────────────────────────────── 2
elif seccion == SECCIONES[1]:
    estilo.titular(st, gc.gran_idea(resumen, regiones))
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        estilo.tarjeta(st, f"{resumen['informalidad_jefas_pct']:.0f} %",
                       "de las jefas de hogar con hijos menores trabaja sin cotizar "
                       "a pensión ni a salud", "DANE, GEIH 2026")
    with c2:
        estilo.tarjeta(st, gc.miles(resumen["jefas_informales_mes"]),
                       "mujeres, en promedio cada mes",
                       "Expandido con el factor FEX_C18")
    with c3:
        estilo.tarjeta(st, f"{resumen['jefas_bajo_smmlv_pct']:.0f} %",
                       "gana menos de un salario mínimo al mes",
                       f"Mínimo 2026: {gc.cop(gc.SMMLV_2026)}")
    st.markdown("")
    st.markdown(
        f"""<div class="entradilla">Cotizar a pensión y a salud es lo que separa una
        enfermedad de una deuda, y la vejez de la pobreza. Por eso es el centro de esta
        historia.</div>""", unsafe_allow_html=True)
    estilo.fuente(st, FUENTE + " Cifras verificadas contra el modelo de Power BI del Proyecto 1.")

# ─────────────────────────────── 3
elif seccion == SECCIONES[2]:
    estilo.titular(st, "Qué significa, en concreto, «trabajar sin protección»")
    c1, c2 = st.columns(2, gap="large")
    for col, (sub, cuerpo) in zip((c1, c2), [
        ("Si trabaja para alguien",
         "Es informal si su empleador no le paga pensión ni la tiene en salud "
         "contributiva. Da igual que lleve años en el puesto o que el acuerdo sea de palabra."),
        ("Si trabaja por su cuenta",
         "Es informal si su negocio no está registrado. Una venta, un puesto o un oficio "
         "por días sin registro entra en esta categoría.")]):
        with col:
            st.markdown(f"""<div class="tarjeta">
                <div class="rotulo" style="color:{FOCO};font-weight:700;font-size:1.05rem">{sub}</div>
                <div class="rotulo" style="margin-top:.5rem">{cuerpo}</div></div>""",
                        unsafe_allow_html=True)
    st.markdown("")
    st.markdown("""<div class="entradilla"><b>Qué cambia en la práctica:</b> sin semanas
        cotizadas no hay pensión al llegar a la vejez, no hay incapacidad pagada si se
        enferma y no hay licencia de maternidad.</div>""", unsafe_allow_html=True)
    st.markdown("")
    st.info("Estar en el **régimen subsidiado** de salud no es lo mismo que cotizar: para "
            "estas cifras sigue contando como trabajo informal. Y estas cifras describen "
            "una situación, no juzgan a nadie.")

# ─────────────────────────────── 4
elif seccion == SECCIONES[3]:
    estilo.titular(st, f"En {baja.region} son {gc.de_cada_diez(baja.informalidad_jefas)}. "
                       f"En {alta.region}, {gc.de_cada_diez(alta.informalidad_jefas)}.")
    izq, der = st.columns([3, 2], gap="large")
    with izq:
        imagen("p3_mapa_regiones.png", "Informalidad de las jefas de hogar, por región",
               "Falta el mapa. Ejecute el script de R.")
    with der:
        d = regiones.sort_values("informalidad_jefas")
        fig = px.bar(d, x="informalidad_jefas", y="region", orientation="h",
                     hover_data={"jefas_ocupadas_mes": ":,.0f",
                                 "ingreso_medio_jefas": ":,.0f", "n": True},
                     labels={"informalidad_jefas": "% en trabajo informal", "region": ""},
                     color="informalidad_jefas",
                     color_continuous_scale=SECUENCIAL, range_color=(20, 80))
        fig.update_layout(coloraxis_showscale=False, xaxis_range=[0, 100])
        st.plotly_chart(estilizar(fig, 420), use_container_width=True)
        st.caption("Pase el cursor para ver cuántas mujeres y cuánto ganan en cada región.")
    st.markdown("""<div class="nota">El mapa no dice que una región cause informalidad.
        Dice que la estructura del empleo es distinta en cada una: donde hay más empleo
        asalariado registrado, hay menos informalidad.</div>""", unsafe_allow_html=True)
    estilo.fuente(st, FUENTE + " Mapa elaborado en R (sf y ggplot2). Cartografía: GADM 4.1.")

# ─────────────────────────────── 5
elif seccion == SECCIONES[4]:
    estilo.titular(st, "El empleo doméstico y el trabajo por cuenta propia "
                       "casi nunca traen protección")
    comparables = (pos_zona.groupby("posicion").zona.nunique()
                   .pipe(lambda s: s[s == 2].index))
    d = pos_zona[pos_zona.posicion.isin(comparables)].copy()
    orden = (d.groupby("posicion").informalidad.mean()
             .sort_values(ascending=False).index.tolist())
    fig = px.bar(d, x="posicion", y="informalidad", color="zona", barmode="group",
                 category_orders={"posicion": orden, "zona": ["Rural", "Urbana"]},
                 color_discrete_map={"Rural": FOCO, "Urbana": COMP},
                 pattern_shape="zona" if tramas else None,
                 pattern_shape_sequence=TRAMAS,
                 text=d.informalidad.map(lambda v: f"{v:.0f} %"),
                 hover_data={"n": True, "jefas_mes": ":,.0f",
                             "informalidad": ":.1f", "posicion": False},
                 labels={"posicion": "", "informalidad": "% en trabajo informal",
                         "zona": "", "n": "casos en la encuesta",
                         "jefas_mes": "jefas al mes"})
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_range=[0, 112])
    st.plotly_chart(estilizar(fig, 460), use_container_width=True)
    st.caption("Pase el cursor para ver cuántas mujeres y cuántos casos hay en cada barra. "
               "Solo se muestran los tipos de empleo con 30 o más casos en ambas zonas.")
    st.markdown("""<div class="entradilla">Trabajar por cuenta propia es la puerta de
        entrada más común y, a la vez, la que casi nunca trae protección. El empleo
        doméstico está en una situación parecida. El empleo en una empresa privada es el
        que más protege, y aun así fuera de las cabeceras protege mucho menos.<br><br>
        <b>Esto no significa que baste con cambiar de empleo.</b> Significa que la
        diferencia no se explica por el empeño de cada quien, sino por el tipo de puesto
        al que se puede acceder.</div>""", unsafe_allow_html=True)
    estilo.fuente(st, FUENTE)

# ─────────────────────────────── 6
elif seccion == SECCIONES[5]:
    estilo.titular(st, f"{resumen['jefas_bajo_smmlv_pct']:.0f} de cada 100 ganan "
                       "menos de un salario mínimo")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        estilo.tarjeta(st, gc.cop(resumen["ingreso_medio_jefas"]),
                       "ingreso mensual promedio de las jefas de hogar")
    with c2:
        estilo.tarjeta(st, gc.cop(resumen["ingreso_medio_jefes"]),
                       "de los jefes, hombres, en la misma situación familiar")
    with c3:
        estilo.tarjeta(st, gc.pct(resumen["brecha_ingresos_pct"]),
                       "menos ganan ellas", "No mide discriminación salarial")
    st.markdown("")
    fig = px.line(hist, x="ingreso", y="porcentaje", color="situacion",
                  line_shape="hv",
                  color_discrete_map={"Trabajo informal": FOCO,
                                      "Trabajo formal": COMP},
                  line_dash="situacion" if tramas else None,
                  labels={"ingreso": "Ingreso laboral mensual",
                          "porcentaje": "% de jefas de hogar", "situacion": ""},
                  hover_data={"ingreso": ":,.0f", "porcentaje": ":.1f"})
    fig.update_traces(line_width=2.6)
    fig.add_vline(x=param["smmlv"], line_dash="dash", line_color=TINTA, line_width=1.6)
    fig.add_annotation(x=param["smmlv"], y=1.02, yref="paper", yanchor="bottom",
                       text=f"Salario mínimo {gc.cop(param['smmlv'])}",
                       showarrow=False, font=dict(size=13, color=TINTA))
    fig.update_xaxes(tickformat=",.0f", tickprefix="$")
    fig.update_layout(margin=dict(t=60, b=50, l=10, r=20))
    st.plotly_chart(estilizar(fig, 440), use_container_width=True)
    st.caption(f"Se recorta el 3 % de ingresos más altos, por encima de "
               f"{gc.cop(param['tope_ingreso'])}. Pase el cursor sobre las líneas.")
    st.markdown("""<div class="nota">En el trabajo formal los ingresos se concentran justo
        en el salario mínimo; en el informal se reparten muy por debajo. La diferencia con
        los hombres <b>no es</b> una medida de discriminación salarial: no compara el mismo
        cargo con la misma jornada.</div>""", unsafe_allow_html=True)
    estilo.fuente(st, FUENTE)

# ─────────────────────────────── 7
elif seccion == SECCIONES[6]:
    estilo.titular(st, "Busque su caso")
    st.markdown("""<div class="entradilla">Elija su región y vea cómo cambia la situación
        según el tipo de empleo.</div>""", unsafe_allow_html=True)
    st.markdown("")
    region = st.selectbox("Región", list(regiones.region))
    fila = gc.fila_region(regiones, region)

    if gc.solo_capital(regiones, region):
        st.warning(f"En {region} la encuesta cubre principalmente las capitales, y es la "
                   f"región con menos casos ({int(fila['n'])}). Estas cifras no "
                   "representan bien las zonas alejadas de las capitales.")
    elif gc.muestra_pequena(regiones, region):
        st.warning(f"En {region} la encuesta tiene pocos casos ({int(fila['n'])}). "
                   "Tome estas cifras como una señal aproximada.")

    c1, c2, c3 = st.columns(3, gap="medium")
    dif = fila["informalidad_jefas"] - resumen["informalidad_jefas_pct"]
    c1.metric("Trabajan sin protección", f"{fila['informalidad_jefas']:.0f} %",
              delta=f"{dif:+.0f} pp frente al país", delta_color="inverse")
    c2.metric("Jefas de hogar que trabajan", gc.miles(fila["jefas_ocupadas_mes"]))
    c3.metric("Ingreso mensual promedio", gc.cop(fila["ingreso_medio_jefas"]))

    sub = posiciones[posiciones.region == region].sort_values("informalidad")

    # Respuesta directa al caso de quien consulta
    if not sub.empty:
        st.markdown("")
        empleo = st.selectbox("¿De qué trabaja?", list(sub.posicion),
                              help="Solo aparecen los tipos de empleo con muestra "
                                   "suficiente en esta región.")
        caso = sub[sub.posicion == empleo].iloc[0]
        cuantas = round(caso.informalidad / 10)
        st.markdown(
            f"""<div class="tarjeta" style="border-left:5px solid {FOCO}">
            <div class="rotulo" style="font-size:1.18rem;line-height:1.5">
            De cada 10 mujeres que sostienen un hogar con hijos menores en
            <b>{region}</b> y trabajan como <b>{empleo.lower()}</b>,
            <b style="color:{FOCO}">{cuantas} lo hacen sin cotizar a pensión ni a
            salud</b> ({gc.pct(caso.informalidad)}).</div>
            <div class="pie">Basado en {int(caso.n)} casos de la encuesta.
            {"Son pocos: tome la cifra como una señal aproximada."
             if caso.n < 100 else ""}</div></div>""",
            unsafe_allow_html=True)
        st.markdown("")

    if sub.empty:
        st.info(f"No hay desglose por tipo de empleo para {region} con muestra suficiente.")
    else:
        fig = px.bar(sub, x="informalidad", y="posicion", orientation="h",
                     color="posicion", color_discrete_sequence=SERIE,
                     pattern_shape="posicion" if tramas else None,
                     pattern_shape_sequence=TRAMAS,
                     hover_data={"n": True, "posicion": False},
                     labels={"informalidad": "% en trabajo informal", "posicion": ""})
        fig.update_layout(showlegend=False, xaxis_range=[0, 100])
        st.plotly_chart(estilizar(fig, 380), use_container_width=True)
        st.caption("Solo se muestran los grupos con 30 o más casos encuestados.")

    with st.expander("Ver la tabla de todas las regiones"):
        st.dataframe(regiones, use_container_width=True, hide_index=True)
        st.download_button("Descargar la tabla (CSV)",
                           regiones.to_csv(index=False).encode("utf-8"),
                           file_name="informalidad_jefas_por_region.csv", mime="text/csv")
    estilo.fuente(st, FUENTE)

# ─────────────────────────────── 8
elif seccion == SECCIONES[7]:
    estilo.titular(st, "Qué no dicen estas cifras")
    segunda = regiones.iloc[1]
    par = (f"{alta.region} ({gc.pct(alta.informalidad_jefas)}) y "
           f"{segunda.region} ({gc.pct(segunda.informalidad_jefas)})")
    st.markdown(f"""<div class="entradilla">
    <b>Describen, no explican.</b> Que una región tenga más informalidad no dice por qué,
    ni permite evaluar programas del Gobierno.<br><br>
    <b>La diferencia de ingresos no mide discriminación salarial.</b> No compara el mismo
    cargo, con la misma jornada y experiencia.<br><br>
    <b>Vienen de una encuesta, no de un censo.</b> Cada cifra tiene un margen de error que
    aquí no se calculó. {par} están a medio punto: son las dos regiones con mayor
    informalidad, pero no se puede afirmar cuál encabeza la lista.<br><br>
    <b>Orinoquía-Amazonía</b> es la región con menos casos, y allí la encuesta cubre sobre
    todo las capitales.<br><br>
    <b>El ingreso es el que cada persona reporta</b>, y se calcula solo sobre quienes
    declaran un ingreso mayor que cero.<br><br>
    <b>Son un promedio de {PERIODO}</b>, no una tendencia ni una proyección.
    </div>""", unsafe_allow_html=True)
    st.markdown("")
    st.info("Si una cifra le sorprende, contrástela con los boletines del DANE antes de usarla.")

# ─────────────────────────────── 9
else:
    estilo.titular(st, "Que su situación sea común no la hace normal")
    st.markdown(f"""<div class="entradilla">
    {gc.miles(resumen['jefas_informales_mes'])} mujeres en Colombia sostienen un hogar con
    hijos menores trabajando sin pensión ni salud contributiva. No es un caso aislado ni
    una falla personal: depende en buena medida del tipo de empleo disponible y del lugar
    donde se vive.<br><br>
    Saberlo sirve para <b>reconocer qué cambia</b> si se consigue un empleo con cotización,
    o si un negocio propio se registra. Y para <b>pedir cuentas con datos</b> cuando se
    discuta qué hace el Estado por los hogares que dependen de una sola persona.
    </div>""", unsafe_allow_html=True)
    st.divider()
    c1, c2 = st.columns(2, gap="large")
    with c1:
        q2 = gc.pct(resumen["informalidad_nacional_q2_pct"], 2)
        st.markdown(f"""<div class="nota"><b>Fuentes</b><br><br>
        DANE, Gran Encuesta Integrada de Hogares 2026 (marco 2018), {PERIODO}. Módulos
        <i>Características generales</i> y <i>Ocupados</i>. Catálogo de microdatos 900.<br><br>
        El DANE publicó 54,5 % de informalidad nacional para abril–junio de 2026; este
        análisis reproduce {q2}.<br><br>
        Cartografía del mapa: GADM 4.1.</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="nota"><b>Definiciones</b><br><br>
        <b>Jefa de hogar con hijos menores:</b> mujer registrada como jefa del hogar, en un
        hogar donde vive al menos un hijo o hija menor de 18 años.<br><br>
        <b>Trabajo informal:</b> definición oficial del DANE. Asalariadas que no cotizan a
        pensión ni están en salud contributiva; independientes cuyo negocio no tiene
        registro; trabajadoras sin remuneración.<br><br>
        <b>Promedios mensuales:</b> sumar los seis meses contaría seis veces a las mismas
        personas.<br><br>
        <b>Herramientas:</b> Power BI, Python (Seaborn y Plotly) y R (sf y ggplot2).
        </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"""<div class="nota"><b>Sobre los colores de esta página</b><br><br>
    La paleta viene del Proyecto 1 y se mantiene en las tres herramientas. Los contrastes
    se verificaron contra el estándar WCAG 2.1: todos los colores superan la razón mínima
    de 3,0 frente al fondo. El mapa usa una escala de un solo tono, de ámbar a terracota,
    porque una escala de tono único se percibe igual con cualquier tipo de daltonismo: la
    información está en la claridad, no en el matiz.<br><br>
    En el menú de la izquierda puede cambiar a una <b>paleta para daltonismo</b>
    (Okabe-Ito) o a <b>alto contraste</b>, y activar <b>tramas</b> para que cada serie se
    distinga también por su textura, no solo por el color.</div>""",
                unsafe_allow_html=True)
    estilo.fuente(st, f"{estilo.EQUIPO} · {estilo.INTEGRANTES} · {estilo.CURSO}")


# ─────────────────────────────── continuacion al terminar de leer el paso
_i = SECCIONES.index(seccion)
if _i < len(SECCIONES) - 1:
    st.markdown("")
    st.button(f"Siguiente paso: {SECCIONES[_i + 1].split(' · ')[1]}  →",
              key="seguir_leyendo", on_click=mover, args=(1,), type="primary")
