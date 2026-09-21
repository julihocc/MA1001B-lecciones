# Lección 01 - Población, muestras y tipos de datos

Esta microlección de 50 minutos introduce el lenguaje que conecta preguntas de
negocio con evidencia estadística. Los estudiantes trabajan con un registro de
operaciones completamente sintético para distinguir una población de una
muestra, un parámetro de un estadístico, y datos categóricos de datos
cuantitativos.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 1, Secciones 1.1 y 1.2.
- **Prerrequisitos:** Álgebra básica, expresiones en Python y datos tabulares.
- **Aviso de datos:** Cada registro de esta lección es sintético. Los scripts y
  la libreta no contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Definir una población objetivo e identificar una muestra extraída de ella.
2. Emparejar un parámetro poblacional con su estadístico muestral.
3. Clasificar variables como categóricas, cuantitativas discretas o
   cuantitativas continuas según su significado analítico.
4. Explicar por qué una muestra de conveniencia más grande puede seguir sesgada.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-05 | Pregunta inicial: ¿qué queremos saber de todos los pedidos? | Enunciar población y variable. |
| 05-15 | Población, muestra, parámetro y estadístico | Etiquetar cada elemento en una pregunta de negocio. |
| 15-25 | Ejecutar el Paso 1 y comparar las dos distribuciones | Interpretar $N$, $n$, $\mu$ y $\bar{x}$. |
| 25-35 | Clasificar variables y ejecutar el Paso 2 | Justificar cada tipo por el significado, no por el almacenamiento. |
| 35-45 | Ejecutar el Paso 3 y examinar el sesgo de selección | Comparar tamaño de muestra con error de estimación. |
| 45-50 | Verificación de conceptos y transición | Defender una clasificación y una afirmación de muestreo. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Libreta de estudio del estudiante

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cc/MA1001B-lecciones/main/es/L01_Poblacion_Muestras_Datos/notebooks/leccion_01_poblacion_muestras_datos.ipynb)

[`leccion_01_poblacion_muestras_datos.ipynb`](notebooks/leccion_01_poblacion_muestras_datos.ipynb)
es el punto de entrada para el estudio independiente. Adapta los tres scripts
autónomos a un solo recorrido incremental, ejecutable de principio a fin, con
figuras embebidas, comprobaciones ejecutables, celdas editables de práctica y
conservan la documentación estudiantil de `src/`, traducida a una interfaz de
código en español, y explican las sustituciones propias de una libreta para los
puntos de entrada y las salidas gráficas.

La población sintética se genera completamente en memoria. La libreta no
importa los scripts, no lee los PNG retenidos y no requiere archivos externos.
Se almacena con sus salidas verificadas; una sesión nueva de Google Colab ya
incluye sus únicas dependencias: NumPy, pandas, Matplotlib e IPython.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma población
sintética con `SEED = 42` y no importa otro script de la lección. Estos valores
provienen de dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `fundos_datos_01_poblacion_muestra.py` | Población, muestra aleatoria, parámetro, estadístico | $N=12{,}000$, $n=200$, $\mu=45.26$ min, $\bar{x}=46.11$ min, error absoluto $=0.85$ min. |
| 2 | `fundos_datos_02_tipos_datos.py` | Tipos analíticos de variables | `order_id` actúa como identificador; `channel` y `region` son categóricas; `items_per_order` es discreta; tiempo y valor son continuos. |
| 3 | `fundos_datos_03_sesgo_muestreo.py` | Sesgo de selección como caso límite | Muestra aleatoria: $n=200$, error $0.85$ min. Muestra de conveniencia: $n=1{,}000$, error $6.24$ min. |

El resultado del Paso 3 demuestra un límite, no una regla numérica universal.
Una muestra grande puede producir una mala estimación cuando el proceso de
selección excluye partes importantes de la población. La Lección 02 desarrolla
los diseños de muestreo probabilístico.

## Diccionario de variables

| Variable | Rol analítico | Razón |
|---|---|---|
| `order_id` | Identificador con rol categórico | La aritmética sobre el código no tiene sentido de negocio. |
| `channel` | Categórica | Los valores nombran canales de pedido (Mostrador, En línea, Socio). |
| `region` | Categórica | Los valores nombran regiones operativas (Norte, Centro, Sur). |
| `items_per_order` | Cuantitativa discreta | El valor cuenta artículos individuales. |
| `processing_time_minutes` | Cuantitativa continua | El valor mide tiempo transcurrido. |
| `order_value_mxn` | Cuantitativa continua | El valor mide magnitud monetaria. |

## Conceptos erróneos comunes

- Una población es el conjunto definido por la pregunta, no necesariamente
  todas las personas o transacciones existentes.
- Un parámetro describe una población. Un estadístico proviene de una muestra
  y puede variar entre muestras.
- El almacenamiento numérico no garantiza un rol analítico cuantitativo.
- Una muestra más grande reduce la variación aleatoria bajo un muestreo
  adecuado, pero el tamaño solo no repara el sesgo de selección.
- El ejemplo sintético ilustra conceptos estadísticos. No afirma nada sobre
  ninguna organización real.

## Estructura del paquete

```text
L01_Poblacion_Muestras_Datos/
|-- README.md
|-- src/
|   |-- fundos_datos_01_poblacion_muestra.py
|   |-- fundos_datos_02_tipos_datos.py
|   `-- fundos_datos_03_sesgo_muestreo.py
|-- figuras/
|   |-- fundos_datos_01_poblacion_muestra.png
|   |-- fundos_datos_02_tipos_datos.png
|   `-- fundos_datos_03_sesgo_muestreo.png
|-- notebooks/
|   `-- leccion_01_poblacion_muestras_datos.ipynb
`-- diapositivas/
    |-- leccion_01.tex
    `-- leccion_01.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L01_Poblacion_Muestras_Datos/src/fundos_datos_01_poblacion_muestra.py
uv run es/L01_Poblacion_Muestras_Datos/src/fundos_datos_02_tipos_datos.py
uv run es/L01_Poblacion_Muestras_Datos/src/fundos_datos_03_sesgo_muestreo.py
```

Para volver a ejecutar la libreta localmente:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace es/L01_Poblacion_Muestras_Datos/notebooks/leccion_01_poblacion_muestras_datos.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_01.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_01.tex
```

## Atribución OpenStax

Las definiciones y la secuencia curricular siguen a Alexander Holmes,
Barbara Illowsky y Susan Dean, *Introductory Business Statistics 2e*,
Capítulo 1, Secciones
[1.1](https://openstax.org/books/introductory-business-statistics-2e/pages/1-1-definitions-of-statistics-probability-and-key-terms)
y
[1.2](https://openstax.org/books/introductory-business-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling).
OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

