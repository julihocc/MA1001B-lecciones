# Lección 04 - Detección de anomalías y boxplots

Esta microlección de 50 minutos usa una muestra de operaciones de negocio
completamente sintética para comparar tres formas de localizar tiempos de
procesamiento inusualmente distantes. Los estudiantes comprueban la regla
empírica bajo su condición de forma, aplican la desigualdad de Chebyshov
sin supuesto de forma y usan cercas de boxplot para marcar registros que
merecen investigación.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 2, Secciones 2.1, 2.2 y 2.7.
- **Prerrequisitos:** Estadística descriptiva de la Lección 03, incluida la
  media, la desviación estándar muestral, los cuartiles y el rango
  intercuartílico.
- **Aviso de datos:** Cada registro de pedido es sintético. No se usan datos
  reales de empresas, clientes, instalaciones, socios u operaciones.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar la condición de distribución que exige la regla empírica.
2. Aplicar la desigualdad de Chebyshov a datos de cualquier forma.
3. Calcular las cercas inferior y superior 1.5-IQR a partir de Q1 y Q3.
4. Leer un boxplot e identificar valores atípicos potenciales de forma
   reproducible.
5. Explicar por qué una bandera estadística inicia una investigación y no
   prueba una causa, un error o una anomalía de negocio.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-05 | Revisar centro, dispersión y distancia a la media | Nombrar la unidad y los resúmenes requeridos por una regla de distancia. |
| 05-17 | Establecer la regla empírica y ejecutar el Paso 1 | Comparar la cobertura observada con 68%, 95% y más de 99%. |
| 17-29 | Agregar retrasos de cola y ejecutar el Paso 2 | Calcular las dos cotas inferiores de Chebyshov y compararlas con la observación. |
| 29-43 | Introducir cercas de boxplot y ejecutar el Paso 3 | Reproducir Q1, Q3, IQR, ambas cercas y el número de banderas. |
| 43-50 | Verificación de conceptos y discusión de investigación | Separar una bandera reproducible de una conclusión sobre su causa. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Datos sintéticos de pedidos

Los tres scripts reconstruyen los mismos 600 registros sintéticos de pedidos
con `SEED = 42`. El Paso 1 comienza con tiempos de procesamiento en forma de
campana. El Paso 2 agrega retrasos positivos de cola a un subconjunto
sembrado y produce una cola derecha. El Paso 3 reemplaza cuatro tiempos por
extremos sintéticos conocidos para que la clase compare la construcción
conocida con los valores seleccionados por una regla estadística general.

| Campo | Rol |
|---|---|
| `order_id` | Identificador numérico. Etiqueta un pedido, pero no es una medición cuantitativa. |
| `processing_time_minutes` | Medición cuantitativa continua analizada en cada paso. |
| `has_queue_delay` | Indicador categórico agregado en el Paso 2. |
| `known_injected_extreme` | Etiqueta de construcción agregada en el Paso 3 solo para validación. |
| `flagged_by_iqr_rule` | Bandera estadística reproducible agregada en el Paso 3. |

La etiqueta de construcción está disponible porque los datos son sintéticos.
Los datos operativos reales rara vez ofrecen una respuesta conocida antes de
investigar.

## Tres reglas y sus condiciones

### Regla empírica

Para una distribución simétrica con forma de campana, aproximadamente 68% de
las observaciones caen dentro de una desviación estándar de la media,
aproximadamente 95% caen dentro de dos y más de 99% caen dentro de tres.
Estos porcentajes son aproximaciones, y la condición de forma importa.

### Desigualdad de Chebyshov

Para cualquier distribución y $k>1$, la proporción dentro de $k$ desviaciones
estándar de la media es al menos

$$
1-\frac{1}{k^2}.
$$

Las cotas inferiores son 75% para $k=2$ y 88.89% para $k=3$. La proporción
observada puede ser mucho mayor porque la desigualdad ofrece una garantía
mínima, no una predicción.

### Cercas de valores atípicos potenciales del boxplot

Con $\mathrm{IQR}=Q_3-Q_1$, las cercas usuales son

$$
Q_1-1.5(\mathrm{IQR})
\quad\text{y}\quad
Q_3+1.5(\mathrm{IQR}).
$$

Los valores más allá de cualquiera de las cercas son atípicos potenciales.
La regla describe su posición relativa a la mitad central de los datos. No
determina por qué ocurrieron esos valores.

## Scripts incrementales y resultados verificados

Cada script es autocontenido, no usa argumentos de línea de comandos y
escribe solo su PNG correspondiente. Los valores siguientes provienen de
ejecuciones directas repetidas en el entorno bloqueado de `uv`.

| Paso | Script | Idea añadida | Resultado verificado |
|:---:|---|---|---|
| 1 | `deteccion_anomalias_01_regla_empirica.py` | Cobertura de la regla empírica para una muestra con forma de campana | $n=600$, media $=44.87$ min, $s$ muestral $=4.87$ min. La cobertura observada es 69.17%, 94.83% y 99.50% dentro de una, dos y tres $s$. |
| 2 | `deteccion_anomalias_02_chebyshev.py` | Cotas inferiores sin forma después de agregar una cola derecha | 59 pedidos reciben un retraso de cola. Media $=45.79$ min, $s$ muestral $=5.84$ min y asimetría $=0.74$. La cobertura observada es 95.33% dentro de $2s$ frente a una cota de 75.00% y 98.67% dentro de $3s$ frente a 88.89%. |
| 3 | `deteccion_anomalias_03_banderas_boxplot.py` | Cercas 1.5-IQR y candidatos a investigación | Q1 $=42.19$, Q3 $=48.89$, IQR $=6.71$, cerca inferior $=32.13$ y cerca superior $=58.96$ min. La regla marca 24 pedidos, incluidos los 4 extremos inyectados y 20 observaciones más. |

Las otras 20 banderas no son automáticamente falsos positivos. Son valores
que cumplen la misma regla posicional sin llevar la etiqueta de
construcción conocida. Sus causas permanecen desconocidas y requieren
revisión del registro, del proceso y del contexto.

## Libreta de estudio

La guía estudiantil
[`notebooks/leccion_04_deteccion_anomalias_boxplots.ipynb`](notebooks/leccion_04_deteccion_anomalias_boxplots.ipynb)
integra los tres pasos en un solo estado acumulativo. Construye en memoria los
600 pedidos sintéticos, conserva las identidades de fila sembradas, embebe tres
figuras editables y concluye con aserciones ejecutables, práctica segura y
respuestas plegables.

La libreta es autocontenida: no descarga datos, no lee archivos del repositorio,
no requiere conexión de red y no importa los scripts ni las imágenes retenidas
del paquete. Por ello puede subirse directamente a Google Colab, abrirse en VS
Code con un kernel de Colab o ejecutarse en el entorno bloqueado del proyecto.
Sus figuras son salidas embebidas de celda; los PNG bajo `figuras/` siguen
siendo la evidencia retenida producida por los scripts independientes.

## Flujo de investigación

1. Verificar el registro, la unidad, la marca de tiempo y el historial de
   transformaciones.
2. Comparar el valor marcado con el contexto operativo y registros
   relacionados.
3. Determinar si refleja un evento raro válido, un cambio de proceso, un
   problema de datos u otra explicación.
4. Documentar la evidencia y decidir si se retiene, corrige, excluye o
   modela la observación por separado.

La regla estadística hace reproducible el cribado. La investigación
sustenta la decisión eventual.

## Conceptos erróneos comunes

- La regla empírica no aplica a toda distribución. Requiere un patrón
  aproximadamente simétrico y con forma de campana.
- Los porcentajes de Chebyshov son cotas inferiores, no porcentajes
  esperados ni predicciones exactas de cobertura.
- Un valor fuera de tres desviaciones estándar no es automáticamente un
  error.
- Una bandera de boxplot identifica un atípico potencial. No establece la
  causa ni la importancia de negocio de ese valor.
- El multiplicador 1.5 es una regla convencional de cribado, no una ley
  científica universal.
- Un conjunto de datos más grande no elimina la necesidad de inspeccionar
  la calidad de los datos y el contexto operativo.
- Los resultados sintéticos no afirman nada sobre ningún proceso operativo
  real.

## Estructura del paquete

```text
L04_Deteccion_Anomalias_Boxplots/
|-- README.md
|-- notebooks/
|   `-- leccion_04_deteccion_anomalias_boxplots.ipynb
|-- src/
|   |-- deteccion_anomalias_01_regla_empirica.py
|   |-- deteccion_anomalias_02_chebyshev.py
|   `-- deteccion_anomalias_03_banderas_boxplot.py
|-- figuras/
|   |-- deteccion_anomalias_01_regla_empirica.png
|   |-- deteccion_anomalias_02_chebyshev.png
|   `-- deteccion_anomalias_03_banderas_boxplot.png
`-- diapositivas/
    |-- leccion_04.tex
    `-- leccion_04.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L04_Deteccion_Anomalias_Boxplots/src/deteccion_anomalias_01_regla_empirica.py
uv run es/L04_Deteccion_Anomalias_Boxplots/src/deteccion_anomalias_02_chebyshev.py
uv run es/L04_Deteccion_Anomalias_Boxplots/src/deteccion_anomalias_03_banderas_boxplot.py
```

Ejecutar la libreta y guardar todas las salidas de celda:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L04_Deteccion_Anomalias_Boxplots/notebooks/leccion_04_deteccion_anomalias_boxplots.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_04.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_04.tex
```

## Atribución OpenStax

Las definiciones y la secuencia de enseñanza siguen a Alexander Holmes,
Barbara Illowsky y Susan Dean, *Introductory Business Statistics 2e*,
Capítulo 2: Sección
[2.1](https://openstax.org/books/introductory-business-statistics-2e/pages/2-1-stem-and-leaf-graphs-line-graphs-and-bar-graphs)
sobre la necesidad de investigar observaciones inusuales con información de
contexto, Sección
[2.2](https://openstax.org/books/introductory-business-statistics-2e/pages/2-2-measures-of-the-location-of-the-data)
para boxplots y las cercas 1.5-IQR de atípicos potenciales, y Sección
[2.7](https://openstax.org/books/introductory-business-statistics-2e/pages/2-7-measures-of-the-spread-of-the-data)
para la desigualdad de Chebyshov y la regla empírica. El texto citado está
licenciado bajo CC BY-NC-SA 4.0. Los datos sintéticos, el código, las
figuras y el flujo de investigación son materiales originales del curso.

