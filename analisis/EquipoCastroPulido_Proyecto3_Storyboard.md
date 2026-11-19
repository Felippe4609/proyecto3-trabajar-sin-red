# Proyecto 3 · Narrativa visual integrada
## Sostener un hogar sin respaldo: informalidad laboral de las jefas de hogar con hijos menores

**Equipo Castro–Pulido** · David Castro y Felipe Pulido · Visualización I · Universidad Externado de Colombia

> Todas las cifras salen del notebook ejecutado sobre la GEIH 2026 (enero–junio) y **coinciden con el dashboard de Power BI a cuatro decimales**. La sección 10 del notebook lo verifica automáticamente.

---

## 1. Continuidad con el Proyecto 1

El Proyecto 1 respondió, para un decisor de política pública, **dónde** priorizar la intervención. El Proyecto 3 conserva la fuente, el período, la paleta y **la misma función de clasificación de informalidad**, pero cambia el destinatario: ahora habla con las mujeres de las que tratan los datos.

| | Proyecto 1 | Proyecto 3 |
|---|---|---|
| Audiencia | Decisor de política pública | Mujeres que sostienen un hogar con hijos menores |
| Pregunta | Dónde priorizar | Qué tan común es mi situación y qué la explica |
| Unidad | Tasas, ranking, volumen | Pesos al mes, «de cada 10», tipo de empleo |

**Coherencia técnica.** La función `fxInformalidadDANE` de Power Query se tradujo a Python línea por línea. No es una reimplementación aproximada: las dos producen exactamente las mismas cifras.

**Sin repeticiones.** Ninguna visualización del Proyecto 1 se reutiliza. Las figuras de Python responden preguntas que el tablero no responde, y el mapa es un producto nuevo.

---

## 2. Audiencia ciudadana

**Mujeres que son jefas de hogar con hijos menores de 18 años y trabajan.** No es «la ciudadanía»: es un grupo delimitado y contable, **2.263.845 mujeres al mes**.

**Por qué les resulta relevante.** De su ingreso depende un hogar con hijos menores. Más de la mitad trabaja sin cotizar a pensión ni a salud: una enfermedad, un embarazo o la vejez no tienen respaldo. Muchas no se identifican con la palabra «informal»; dicen que trabajan por su cuenta.

**Necesidad de comprensión.** Entender que su situación no es un caso aislado ni una falla personal, ver qué parte se explica por el lugar y el tipo de empleo, y saber qué cambia concretamente entre estar y no estar protegida.

**Lenguaje.** Nada de «tasa de informalidad» sin explicar. Se dice «trabajar sin cotizar a pensión ni salud». Se usan pesos al mes y «de cada 10», no puntos porcentuales ni decimales.

---

## 3. Pregunta analítica

> ¿Qué tan frecuente es trabajar sin protección social entre las mujeres que sostienen un hogar con hijos menores en Colombia, y en qué medida esa situación depende de la región y del tipo de empleo?

---

## 4. La Gran Idea

> **De cada 10 mujeres que sostienen un hogar con hijos menores y trabajan, más de 5 lo hacen sin cotizar a pensión ni a salud: son 1.213.692 mujeres. Dónde viven y de qué trabajan explica buena parte de la diferencia: en Bogotá son 3 de cada 10; en la región Pacífica, 7 de cada 10.**

| Dato | Valor |
|---|---|
| Jefas con hijos menores ocupadas | 2.263.845 al mes |
| En trabajo informal | 1.213.692 (53,6 %) |
| Ganan menos de un salario mínimo | 57,7 % |
| Ingreso medio de las jefas | $1.995.232 |
| Ingreso medio de los jefes en igual situación | $2.679.828 |
| Diferencia | 25,5 % menos |
| Informalidad de los jefes (hombres) | 51,8 % |

---

## 5. Las diez diapositivas

| # | Título (la conclusión, no el tema) | Evidencia | Herramienta |
|---|---|---|---|
| 1 | Sostener un hogar sin respaldo: informalidad laboral de las jefas de hogar con hijos menores | Portada, audiencia y pregunta | — |
| 2 | 2,26 millones de mujeres sostienen un hogar con hijos menores. Más de la mitad trabaja sin protección | Tarjetas de la Gran Idea | Tarjetas |
| 3 | Qué significa «trabajar sin protección», en concreto | Definición en lenguaje corriente | Texto |
| 4 | Dónde vive cambia su probabilidad: del 29 % en Bogotá al 68 % en el Pacífico | **Mapa de las seis regiones** | **R (sf + ggplot2)** |
| 5 | El empleo doméstico y el trabajo por cuenta propia casi nunca traen protección | Barras por tipo de empleo y zona | **Python (Seaborn)** |
| 6 | 58 de cada 100 ganan menos de un salario mínimo | Distribución del ingreso frente al mínimo | **Python (Seaborn)** |
| 7 | Las jefas ganan 25,5 % menos que los jefes en la misma situación familiar | Comparación por región | **Power BI** |
| 8 | Busque su caso: región y tipo de empleo | Exploración interactiva | **Python (Plotly)** / app |
| 9 | Qué no dicen estas cifras | Límites | Texto |
| 10 | Qué puede hacer con esto, y de dónde salen los datos | Mensaje final y fuentes | Texto |

**Reparto de herramientas.** El mapa (R) responde *dónde*; Seaborn responde *de qué trabaja* y *cuánto gana*; Plotly y la app permiten buscar el caso propio; Power BI aporta la brecha de ingresos y la evolución mensual que ya tenía el Proyecto 1.

---

## 6. Hallazgos

**Por región** (% de jefas en trabajo informal):

| Región | Informalidad | Jefas ocupadas/mes | Ingreso medio | Casos |
|---|---|---|---|---|
| Pacífica | 68,0 % | 385.951 | $1.411.531 | 2.928 |
| Caribe | 67,5 % | 482.694 | $1.301.596 | 4.678 |
| Central | 51,8 % | 497.707 | $2.051.953 | 4.753 |
| Oriental | 50,0 % | 476.791 | $2.239.974 | 3.285 |
| Orinoquía-Amazonía | 49,1 % | 28.275 | $2.025.821 | 1.151 |
| Bogotá | 29,4 % | 392.426 | $3.044.881 | 579 |

**Por tipo de empleo y zona** (% informal):

| Tipo de empleo | Urbana | Rural |
|---|---|---|
| Empleada doméstica | 86 % | 94 % |
| Por cuenta propia | 77 % | 94 % |
| Jornalera o peona | 69 % | 88 % |
| Empleada de empresa privada | 26 % | 57 % |

Dos referencias que no entran en la figura por falta de casos rurales: **empleada del gobierno, 0 %**, y **patrona o empleadora, 34 %** en zona urbana.

**La lectura para la audiencia:** el tipo de empleo pesa más que el esfuerzo individual, y vivir fuera de una cabecera agrava cada caso. El mismo oficio protege mucho menos en zona rural.

---

## 7. Qué no podemos afirmar (diapositiva 9)

- **Describe, no explica.** Las diferencias entre regiones no dicen por qué ocurren ni permiten evaluar políticas públicas.
- **No mide discriminación salarial.** La diferencia de 25,5 % no compara el mismo cargo con la misma jornada y experiencia.
- **Sin márgenes de error.** No se calcularon intervalos de confianza con el diseño muestral; diferencias pequeñas entre regiones pueden no ser distinguibles. Pacífica (68,0 %) y Caribe (67,5 %) están a medio punto: **no conviene afirmar cuál es la más alta**.
- **Orinoquía-Amazonía:** la encuesta cubre solo las capitales de sus nueve departamentos, y su muestra es pequeña (1.151 registros).
- **Bogotá** tiene pocos casos de jefas (579) pese a su tamaño.
- **El ingreso es autorreportado** y se calcula solo sobre quienes declaran un ingreso mayor que cero.
- **Es el promedio de enero a junio de 2026**, no una tendencia.

---

## 8. Fuentes y definiciones (diapositiva 10)

- **Fuente:** DANE, Gran Encuesta Integrada de Hogares (GEIH) 2026, marco 2018. Microdatos de enero a junio, módulos *Características generales* y *Ocupados*. https://microdatos.dane.gov.co/index.php/catalog/900
- **Contraste oficial:** el DANE publicó **54,5 %** de informalidad nacional para abril–junio de 2026; el notebook reproduce **54,52 %** para ese mismo trimestre. https://www.dane.gov.co/index.php/estadisticas-por-tema-2/mercado-laboral/empleo-informal-y-seguridad-social
- **Jefa de hogar con hijos menores:** mujer registrada como jefa del hogar (`P6050 = 1`, `P3271 = 2`) en un hogar con al menos una persona registrada como hijo o hija menor de 18 años.
- **Trabajo informal:** sintaxis oficial del DANE (anexo *Empleo informal y seguridad social*, marco 2018), tal como la implementa `fxInformalidadDANE` en el modelo. Empleadas del gobierno son formales; sin remuneración son informales; para las independientes decide el registro y la contabilidad del negocio; para las asalariadas, tener salud contributiva pagada por el empleador **y** pensión.
- **Cartografía del mapa:** GADM 4.1, límites administrativos de uso libre. Se intentó primero el Marco Geoestadístico Nacional del DANE (paquete `ColOpenData`), pero su servidor no respondía el día de la entrega; el script deja constancia de ello y el pie del mapa indica la fuente usada.
- **Salario mínimo 2026:** $1.750.905 (Decreto 1469 de 2025).
- **Ponderación:** factor de expansión `FEX_C18`. Los conteos de personas son **promedios mensuales**: sumar los seis meses contaría seis veces a la misma población.

---

## 9. Revisar antes de entregar

1. Ejecutar el notebook completo y guardarlo **con los resultados visibles**. La sección 10 debe terminar en «Todas las cifras coinciden con el dashboard de Power BI».
2. Generar el mapa con el script de R y el HTML de Plotly (requiere `pip install plotly`).
3. Verificar que el enlace de Power BI abre en una ventana de incógnito.
4. Que los dos integrantes puedan explicar la definición de informalidad, el factor de expansión, el promedio mensual y por qué el mapa es por regiones.

---

## 10. Preguntas probables en la sustentación

1. **¿Por qué el mapa es por regiones y no por departamentos?** Es la unidad del Proyecto 1 y la que respalda la muestra. En Orinoquía-Amazonía la GEIH cubre solo las capitales; pintar 33 departamentos sugeriría una precisión que la encuesta no tiene. La columna `Cobertura` del modelo ya lo registra.
2. **¿Por qué promedio mensual y no la suma de los seis meses?** Cada mes es una muestra distinta de la misma población. Sumar los factores de expansión contaría seis veces a las mismas mujeres: daría 7,3 millones en vez de 1,21 millones.
3. **¿Cómo se define informal?** Con la sintaxis oficial del DANE. Hay tres caminos según la posición ocupacional, y para las asalariadas se exigen **las dos** condiciones: salud contributiva pagada por el empleador y pensión.
4. **¿Cómo saben que Python y Power BI dicen lo mismo?** La función M se tradujo a Python y el notebook compara diez indicadores y las seis regiones contra los valores del modelo. Si alguno se desviara, la celda falla.
5. **¿Hay causalidad?** No. Son diferencias descriptivas.
6. **¿Por qué la media y no la mediana del ingreso?** Para mantener la comparabilidad con el Proyecto 1 y con las medidas del dashboard.
7. **¿Qué aporta Python que no esté en Power BI?** La distribución del ingreso frente al salario mínimo y el cruce de tipo de empleo con zona.
8. **¿Por qué la cartografía es de GADM y no del DANE?** Se intentó primero el MGN del DANE, pero el servidor que lo publica no respondía. GADM es una fuente estándar de límites administrativos y los polígonos de los departamentos son los mismos; además, las cifras no dependen de la cartografía, solo del cruce departamento–región.
9. **¿Pacífica o Caribe es la más alta?** Están a medio punto porcentual y no se calcularon márgenes de error: se presentan como las dos regiones con mayor informalidad, sin afirmar un orden entre ellas.
