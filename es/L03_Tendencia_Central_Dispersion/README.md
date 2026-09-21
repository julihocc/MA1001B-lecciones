# Lección 03 - Tendencia central y dispersión

Esta microlección de 50 minutos usa una muestra de operaciones de negocio
completamente sintética para distinguir dos preguntas: dónde se centran los
tiempos de procesamiento y cuánto varían. Los estudiantes calculan la media,
la mediana, la desviación estándar muestral y el rango intercuartílico, y
luego examinan cómo un retraso extremo registrado afecta cada resumen.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 2, Secciones 2.2, 2.3 y 2.7.
- **Prerrequisitos:** Terminología de población y muestra de la Lección 01, un
  diseño de muestreo defendible de la Lección 02 y funciones básicas de Python.
- **Aviso de datos:** Cada registro es sintético. No se usan datos reales de
  empresas, clientes, instalaciones o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular e interpretar la media aritmética y la mediana en contexto.
2. Calcular la desviación estándar muestral usando el denominador $n-1$.
3. Calcular el primer cuartil, el tercer cuartil y el rango intercuartílico.
4. Emparejar media con desviación estándar y mediana con IQR al describir
   datos.
5. Explicar por qué un valor extremo afecta estos resúmenes de forma distinta
   sin tratar la sensibilidad como detección automática de anomalías.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-05 | Enmarcar las dos preguntas descriptivas: centro y dispersión | Nombrar la medición, la unidad y la muestra que se resume. |
| 05-17 | Definir media y mediana y ejecutar el Paso 1 | Calcular ambos centros e interpretar su diferencia de 0.49 minutos. |
| 17-31 | Definir desviación estándar muestral, cuartiles e IQR y ejecutar el Paso 2 | Reproducir $s$, Q1, Q3 e IQR en minutos. |
| 31-43 | Cambiar un valor registrado y ejecutar el Paso 3 | Comparar cómo responden los cuatro resúmenes a la misma modificación. |
| 43-50 | Verificación de conceptos y transición | Seleccionar y defender un par centro-dispersión, y enunciar lo que queda para L04. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Muestra sintética de pedidos

La muestra contiene 240 pedidos sintéticos. El tiempo de procesamiento se
genera a partir del número de artículos, un tiempo de cola simulado y ruido
de medición. La semilla permanece en 42 en cada script y los tiempos se
redondean a centésimas de minuto.

| Campo | Rol |
|---|---|
| `order_id` | Identificador numérico. Etiqueta un pedido, pero no es una medición. |
| `items_per_order` | Entrada cuantitativa discreta del proceso sintético. |
| `processing_time_minutes` | Variable cuantitativa continua resumida en esta lección. |

## Definiciones usadas en la lección

Para observaciones $x_1,\ldots,x_n$:

- La **media aritmética** es $\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i$.
- La **mediana** es el valor central después de ordenar las observaciones, o
  el promedio de los dos valores centrales cuando $n$ es par.
- La **desviación estándar muestral** es
  $s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}$ y mide la dispersión
  alrededor de la media en las unidades originales de la variable.
- El **rango intercuartílico** es $\mathrm{IQR}=Q_3-Q_1$ y cubre el 50%
  central de las observaciones ordenadas.

## Scripts incrementales y resultados verificados

Cada script es autocontenido y reconstruye la misma muestra con `SEED = 42`.
Los valores siguientes provienen de la ejecución directa en el entorno
bloqueado de `uv`.

| Paso | Script | Idea añadida | Resultado verificado |
|:---:|---|---|---|
| 1 | `estadistica_descriptiva_01_centro.py` | Media y mediana | $n=240$, media $=45.19$ min, mediana $=44.70$ min, diferencia $=0.49$ min. |
| 2 | `estadistica_descriptiva_02_dispersion.py` | Desviación estándar muestral, cuartiles e IQR | $s=6.38$ min, Q1 $=40.53$ min, Q3 $=49.01$ min, IQR $=8.48$ min. |
| 3 | `estadistica_descriptiva_03_sensibilidad.py` | Sensibilidad a un retraso extremo registrado | El pedido 300193 cambia de 65.22 a 180.00 min. La media cambia $+0.48$ min, la mediana $+0.00$ min, $s$ $+4.34$ min y el IQR $+0.00$ min. |

Los cambios mostrados como $+0.00$ resultan del redondeo a dos decimales. La
mediana y el IQR permanecen sin cambio a la precisión mostrada, mientras que
la media y la desviación estándar muestral aumentan. Esta comparación
demuestra sensibilidad solamente. La Lección 04 introduce boxplots y reglas
formales de detección de anomalías.

## Libreta de estudio

La guía estudiantil
[`notebooks/leccion_03_tendencia_central_dispersion.ipynb`](notebooks/leccion_03_tendencia_central_dispersion.ipynb)
integra los tres pasos en un solo estado acumulativo. Construye los 240 pedidos
sintéticos en memoria, conserva la misma semilla y los mismos valores
verificados, embebe tres figuras editables y termina con aserciones, práctica
segura y respuestas plegables.

La libreta es autocontenida: no descarga datos, no lee archivos del repositorio,
no requiere red y no importa los scripts ni las imágenes retenidas del paquete.
Por eso puede subirse directamente a Google Colab, abrirse en VS Code con un
kernel de Colab o ejecutarse con el entorno bloqueado del proyecto. Las figuras
de la libreta son salidas embebidas; los PNG de `figuras/` continúan siendo la
evidencia retenida de los scripts independientes.

## Elegir un par centro-dispersión

| Patrón de datos o propósito | Centro | Dispersión | Razón |
|---|---|---|---|
| Distribución aproximadamente simétrica sin extremos influyentes | Media | Desviación estándar muestral | Ambos usan cada observación y describen la variación alrededor de la media. |
| Distribución sesgada o valores extremos influyentes | Mediana | IQR | Ambos dependen de posiciones ordenadas y resisten un número pequeño de extremos. |

Estas son pautas, no decisiones automáticas. Quien analiza debe inspeccionar
la distribución, conservar la unidad y explicar por qué los resúmenes
elegidos se ajustan al contexto de decisión.

## Conceptos erróneos comunes

- La media y la mediana no miden dispersión. Dos muestras pueden compartir un
  centro y tener variabilidad muy distinta.
- La desviación estándar no es la distancia absoluta promedio a la media. Se
  basa en desviaciones al cuadrado y vuelve a las unidades originales después
  de tomar una raíz cuadrada.
- La fórmula muestral usa $n-1$. Usar $n$ calcula una desviación estándar
  poblacional de los valores observados.
- El IQR es $Q_3-Q_1$, no la distancia de la mediana a cualquiera de los
  cuartiles.
- Un resumen robusto es menos sensible a extremos, no completamente inmune
  en todo conjunto de datos.
- Un cambio grande en un resumen no prueba que un valor sea un error o una
  anomalía. Aún se requieren contexto y una regla de detección enunciada.
- Los resultados sintéticos no afirman nada sobre ningún proceso operativo
  real.

## Estructura del paquete

```text
L03_Tendencia_Central_Dispersion/
|-- README.md
|-- notebooks/
|   `-- leccion_03_tendencia_central_dispersion.ipynb
|-- src/
|   |-- estadistica_descriptiva_01_centro.py
|   |-- estadistica_descriptiva_02_dispersion.py
|   `-- estadistica_descriptiva_03_sensibilidad.py
|-- figuras/
|   |-- estadistica_descriptiva_01_centro.png
|   |-- estadistica_descriptiva_02_dispersion.png
|   `-- estadistica_descriptiva_03_sensibilidad.png
`-- diapositivas/
    |-- leccion_03.tex
    `-- leccion_03.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L03_Tendencia_Central_Dispersion/src/estadistica_descriptiva_01_centro.py
uv run es/L03_Tendencia_Central_Dispersion/src/estadistica_descriptiva_02_dispersion.py
uv run es/L03_Tendencia_Central_Dispersion/src/estadistica_descriptiva_03_sensibilidad.py
```

Ejecutar y guardar todas las salidas de la libreta:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L03_Tendencia_Central_Dispersion/notebooks/leccion_03_tendencia_central_dispersion.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_03.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_03.tex
```

## Atribución OpenStax

Las definiciones y la secuencia de enseñanza siguen a Alexander Holmes,
Barbara Illowsky y Susan Dean, *Introductory Business Statistics 2e*,
Capítulo 2: Sección
[2.2](https://openstax.org/books/introductory-business-statistics-2e/pages/2-2-measures-of-the-location-of-the-data)
para cuartiles e IQR, Sección
[2.3](https://openstax.org/books/introductory-business-statistics-2e/pages/2-3-measures-of-the-center-of-the-data)
para media y mediana, y Sección
[2.7](https://openstax.org/books/introductory-business-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data)
para la desviación estándar muestral. El texto citado está licenciado bajo
CC BY-NC-SA 4.0. La muestra sintética, el código, las figuras y la
comparación de sensibilidad son materiales originales del curso.

