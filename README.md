# Sostener un hogar sin respaldo

Las mujeres que sostienen un hogar con hijos menores en Colombia.

Producto digital narrativo del **Proyecto 3** de Visualización I, Universidad Externado
de Colombia. Equipo Castro–Pulido: David Ricardo Castro González y Felipe Alejandro
Pulido Díaz.

La aplicación recorre la historia en nueve pasos, con los datos de la Gran Encuesta
Integrada de Hogares (GEIH) 2026 del DANE, enero a junio.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `app.py` | La aplicación, en Streamlit |
| `geih_core.py` | Carga y validación de las tablas |
| `requirements.txt` | Dependencias |
| `outputs/` | Tablas agregadas y figuras |

## Sobre los datos

La aplicación **no lee microdatos**: lee las tablas agregadas de `outputs/`, que son
porcentajes y promedios ya ponderados con el factor de expansión. Los microdatos de la
GEIH no se republican aquí.

Fuente: DANE, Gran Encuesta Integrada de Hogares 2026.
Cálculos propios. Cartografía del mapa: GADM 4.1.

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Nota sobre el nombre del repositorio

El repositorio conserva `proyecto3-trabajar-sin-red`, el título de trabajo. Streamlit
Community Cloud identifica la aplicación por sus coordenadas de GitHub (propietario,
repositorio, rama y archivo de entrada), así que renombrarlo obliga a borrar la
aplicación y volver a desplegarla. Se decidió no arriesgar el despliegue cerca de la
entrega. El nombre definitivo del proyecto es **Sostener un hogar sin respaldo**.
