# Modalidad B · Producto digital narrativo (Streamlit)

**Sostener un hogar sin respaldo** · Equipo Castro–Pulido

**Estado:** la lógica de datos está probada contra las tablas reales; la interfaz no se ejecutó, porque Streamlit no estaba disponible en el entorno de preparación. **Pruébela en local antes de desplegar.**

## Qué es

La historia en nueve pasos, en la secuencia del enunciado: audiencia → necesidad → pregunta → Gran Idea → evidencia → interpretación → cierre. La interacción está en el paso 7, donde la persona elige su región y ve cómo cambia según el tipo de empleo.

## Archivos

| Archivo | Qué hace |
|---|---|
| `app.py` | Las nueve secciones |
| `geih_core.py` | Carga y validación de las tablas, sin Streamlit, para poder probarlo aparte |
| `requirements.txt` | Dependencias |
| `outputs/` | Tablas y figuras. **Se copian del notebook; no se versiona la carpeta de microdatos** |

## Antes de ejecutar

Complete el encabezado de `app.py`:

```python
ENLACE_POWERBI = ""   # el enlace de Power BI Service del Proyecto 1
ENLACE_NOTEBOOK = ""
ENLACE_REPO = ""
```

Si un enlace queda vacío, su botón no aparece; la app no se rompe.

## Ejecutar en local

```bash
pip install -r requirements.txt
# copie aquí la carpeta outputs/ generada por el notebook
streamlit run app.py
```

La app necesita en `outputs/`:

- `p3_resumen_nacional.csv`, `p3_por_region.csv`, `p3_region_posicion.csv` (notebook)
- `p3_fig1_ingreso.png`, `p3_fig2_posicion.png` (notebook)
- `p3_mapa_regiones.png` (script de R)

Si falta alguno, la app lo dice en pantalla y no se cae. Compruébelo: quite un archivo y confirme que aparece el mensaje.

## Desplegar en Streamlit Community Cloud

El enunciado exige que el producto sea accesible para la docente y tenga una ruta de consulta clara. No basta con que corra en su computador.

1. Suba a GitHub: `app.py`, `geih_core.py`, `requirements.txt` y `outputs/`. **No suba `data/raw/`:** son unos 120 MB de microdatos.
2. Entre a [share.streamlit.io](https://share.streamlit.io) con su cuenta de GitHub.
3. *New app* → repositorio, rama y `app.py` como archivo principal.
4. *Deploy*. La primera vez tarda unos minutos.
5. **Abra el enlace en una ventana de incógnito.** Es la única forma de confirmar que la docente podrá entrar.

Si el repositorio es privado, la app no será accesible: hágalo público o invite a la docente.

## Plan B

Exporte además las diez diapositivas del storyboard en PDF. Si el despliegue falla a última hora, ese PDF no depende de ningún servicio en línea.

## Lista de revisión

- [ ] Encabezado de `app.py` completo
- [ ] Las nueve secciones abren sin error
- [ ] Cambiar de región cambia las cifras
- [ ] El mapa de R se ve en el paso 4
- [ ] El enlace abre en incógnito
- [ ] Las cifras coinciden con el notebook y con Power BI
- [ ] La advertencia de muestra pequeña aparece donde corresponde

## Sobre el nombre del repositorio

El repositorio es `proyecto3-trabajar-sin-red`, el título de trabajo del proyecto. No se renombró porque Streamlit Community Cloud identifica la aplicación por sus coordenadas de GitHub (propietario, repositorio, rama y archivo de entrada): cambiar el nombre obliga a borrar la aplicación y volver a desplegarla. Se prefirió no arriesgar el despliegue cerca de la entrega. El nombre definitivo, «Sostener un hogar sin respaldo», sí está en el título de la aplicación, en la presentación y en el cuaderno.
