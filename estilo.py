"""Identidad visual de la aplicación: tipografía, espaciado y cabecera."""
from paleta import BORDE, CREMA, SUAVE, TINTA

EQUIPO = "Equipo Castro–Pulido"
INTEGRANTES = "David Ricardo Castro González · Felipe Alejandro Pulido Díaz"
CURSO = "Visualización I · Universidad Externado de Colombia"


def css(foco: str) -> str:
    return f"""
<style>
  .block-container {{ padding-top: 2.2rem; max-width: 1180px; }}
  html, body, [class*="st-"] {{
      font-family: "Source Sans Pro", system-ui, -apple-system, sans-serif;
      color: {TINTA};
  }}

  /* Cabecera */
  .masthead {{ border-top: 6px solid {foco}; padding-top: 1.1rem; margin-bottom: 1.6rem; }}
  .masthead h1 {{
      font-size: 2.55rem; font-weight: 700; letter-spacing: -0.02em;
      line-height: 1.12; margin: 0 0 .35rem 0; color: {TINTA};
  }}
  .masthead .bajada {{ font-size: 1.12rem; color: {SUAVE}; margin: 0 0 .9rem 0; line-height: 1.45; }}
  .masthead .firma {{
      font-size: .82rem; color: {SUAVE}; border-top: 1px solid {BORDE};
      padding-top: .6rem; letter-spacing: .01em;
  }}

  /* Titulares de sección: la conclusión, no el tema */
  .titular {{
      font-size: 1.72rem; font-weight: 700; line-height: 1.22;
      margin: .2rem 0 1.1rem 0; color: {TINTA};
  }}
  .entradilla {{ font-size: 1.06rem; line-height: 1.6; color: {TINTA}; max-width: 70ch; }}
  .nota {{ font-size: .93rem; line-height: 1.55; color: {SUAVE}; max-width: 75ch; }}

  /* Tarjetas */
  .tarjeta {{
      background: {CREMA}; border: 1px solid {BORDE}; border-radius: 12px;
      padding: 1.1rem 1.25rem; height: 100%;
  }}
  .tarjeta .cifra {{ font-size: 2.3rem; font-weight: 700; color: {foco}; line-height: 1.1; }}
  .tarjeta .rotulo {{ font-size: .95rem; color: {TINTA}; margin-top: .35rem; line-height: 1.4; }}
  .tarjeta .pie {{ font-size: .78rem; color: {SUAVE}; margin-top: .6rem; }}

  .fuente {{
      font-size: .8rem; color: {SUAVE}; border-top: 1px solid {BORDE};
      padding-top: .7rem; margin-top: 1.6rem; line-height: 1.5;
  }}

  [data-testid="stSidebar"] {{ border-right: 1px solid {BORDE}; }}
  [data-testid="stSidebar"] .block-container {{ padding-top: 1.4rem; }}
  div[data-testid="stMetricValue"] {{ font-size: 1.75rem; }}
  img {{ border-radius: 8px; }}
</style>
"""


def cabecera(st, titulo: str, bajada: str):
    st.markdown(
        f"""<div class="masthead">
              <h1>{titulo}</h1>
              <p class="bajada">{bajada}</p>
              <div class="firma">{EQUIPO} · {INTEGRANTES}<br>{CURSO}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def titular(st, texto: str):
    st.markdown(f'<div class="titular">{texto}</div>', unsafe_allow_html=True)


def tarjeta(st, cifra: str, rotulo: str, pie: str = ""):
    st.markdown(
        f"""<div class="tarjeta">
              <div class="cifra">{cifra}</div>
              <div class="rotulo">{rotulo}</div>
              <div class="pie">{pie}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def fuente(st, texto: str):
    st.markdown(f'<div class="fuente">{texto}</div>', unsafe_allow_html=True)
