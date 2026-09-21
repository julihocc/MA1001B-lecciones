# Lección 02 - Diseños de muestreo probabilístico

Esta microlección de 50 minutos desarrolla el detalle de diseño muestral
reservado intencionalmente en la Lección 01. Los estudiantes usan una población
de operaciones de negocio completamente sintética para implementar muestreo
aleatorio simple, estratificado proporcional y por conglomerados de una etapa,
e identificar la unidad de selección en cada diseño.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 1, Sección 1.2.
- **Prerrequisitos:** Conceptos de la Lección 01; funciones básicas de Python,
  indexación y datos agrupados.
- **Aviso de datos:** Cada registro es sintético. No se usan datos reales de
  empresas, clientes, instalaciones o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Explicar el papel de un marco muestral en una muestra probabilística.
2. Extraer una muestra aleatoria simple sin reemplazo y calcular la
   probabilidad de inclusión de un pedido.
3. Asignar y extraer una muestra estratificada proporcional en todas las
   regiones.
4. Distinguir la selección de pedidos individuales de la selección de
   conglomerados completos de instalaciones.
5. Explicar por qué una comparación con semilla no establece un ranking
   universal de diseños de muestreo.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-05 | Reconectar población, muestra y sesgo de selección con un marco muestral | Identificar el marco y la unidad que podría seleccionarse. |
| 05-15 | Definir muestreo aleatorio simple y ejecutar el Paso 1 | Calcular la probabilidad igual de inclusión e inspeccionar la composición. |
| 15-30 | Partir el marco por región y ejecutar el Paso 2 | Verificar la asignación proporcional y explicar por qué aparece cada región. |
| 30-43 | Seleccionar instalaciones completas y ejecutar el Paso 3 | Identificar la unidad de primera etapa y comparar tamaños y errores. |
| 43-50 | Verificación de conceptos y transición | Defender una elección de diseño sin afirmar que un método siempre es el mejor. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Población sintética y marco muestral

El marco contiene 12{,}000 pedidos sintéticos: 500 pedidos de cada una de 24
instalaciones. Seis instalaciones pertenecen a cada una de cuatro regiones. El
tiempo de procesamiento depende de la región, la instalación, el tamaño del
pedido y ruido aleatorio, de modo que los pedidos de una instalación
comparten un efecto de conglomerado.

| Campo | Rol en el diseño |
|---|---|
| `order_id` | Identifica una unidad poblacional individual. |
| `facility_id` | Identifica el conglomerado que contiene un pedido. |
| `region` | Define los cuatro estratos. |
| `items_per_order` | Contribuye al tiempo sintético de procesamiento. |
| `processing_time_minutes` | Variable cuantitativa cuya media poblacional se estima. |

## Libreta de estudio del estudiante

[`leccion_02_disenos_muestreo_probabilistico.ipynb`](notebooks/leccion_02_disenos_muestreo_probabilistico.ipynb)
es el punto de entrada autocontenido para el estudio independiente. Convierte
los tres scripts autónomos en un solo análisis acumulativo en memoria, conserva
la población y los diseños con semilla 42, embebe tres figuras editables e
incluye aserciones ejecutables, práctica segura y respuestas plegables.

La libreta genera toda la población sintética en memoria. No importa los
scripts, no lee los PNG retenidos, no accede a la red y no requiere datos
externos. Sus salidas guardadas reproducen los resultados canónicos de la MAS,
el muestreo estratificado y el muestreo por conglomerados descritos abajo.

## Scripts incrementales y resultados verificados

Cada script es autocontenido y reconstruye la misma población con `SEED = 42`.
Los valores numéricos siguientes se copiaron de la ejecución directa en el
entorno bloqueado de `uv`.

| Paso | Script | Diseño y unidad de selección | Resultado verificado |
|:---:|---|---|---|
| 1 | `disenos_muestreo_01_aleatorio_simple.py` | MAS; selecciona 240 pedidos individuales del marco completo | $N=12{,}000$, $n=240$, probabilidad de inclusión $=2.00\%$, $\mu=47.67$ min, $\bar{x}=47.17$ min, error absoluto $=0.50$ min. |
| 2 | `disenos_muestreo_02_estratificado.py` | Estratificado proporcional; selecciona pedidos de forma independiente en cada región | Asignación: 60 pedidos por región. Media estratificada $=47.95$ min y error absoluto $=0.28$ min. |
| 3 | `disenos_muestreo_03_conglomerados.py` | Conglomerados de una etapa; selecciona 4 instalaciones e incluye todos sus pedidos | Instalaciones F02, F11, F16 y F18; $n=2{,}000$ pedidos; probabilidad de inclusión $=16.67\%$; media $=48.76$ min; error $=1.09$ min. |

El MAS seleccionó 63 pedidos del Norte, 68 del Centro, 51 del Oeste y 58 del
Sureste. La estratificación fijó la asignación en 60 por región. Los
conglomerados de instalaciones representaron Centro, Norte y Oeste, pero no
Sureste.

Estos errores describen un ejemplo didáctico determinista, no un teorema de
que el muestreo estratificado siempre tiene el menor error o el de
conglomerados siempre el mayor. La precisión depende de la estructura
poblacional, la asignación, el estimador y la muestra aleatoria realizada. El
muestreo por conglomerados puede seguir siendo operacionalmente atractivo
cuando visitar unos pocos grupos es más barato que alcanzar unidades
dispersas.

## Comparación de diseños

| Diseño | Selección aleatorizada | Cobertura en esta lección | Requisito práctico |
|---|---|---|---|
| Aleatoria simple | 240 pedidos del marco completo | Cada pedido tiene la misma probabilidad de inclusión de 2.00% | Una lista completa de pedidos |
| Estratificado proporcional | 60 pedidos dentro de cada región | Cada región aporta observaciones | Etiquetas de región para cada pedido |
| Conglomerados de una etapa | 4 instalaciones y luego todos los pedidos de cada una | Aparecen cuatro instalaciones y tres regiones | Una lista de instalaciones y acceso a todas las unidades de las seleccionadas |

## Conceptos erróneos comunes

- El muestreo probabilístico exige un mecanismo aleatorio conocido; no implica
  que la muestra realizada coincida exactamente con cada porcentaje poblacional.
- En el muestreo estratificado proporcional, cada estrato aporta
  observaciones. Los estratos no son las unidades muestreadas; se muestrean
  pedidos dentro de ellos.
- En el muestreo por conglomerados de una etapa, las primeras unidades
  aleatorizadas son conglomerados. Todos los pedidos de una instalación
  seleccionada entran a la muestra en esta implementación.
- Una muestra de 2{,}000 pedidos conglomerados no necesariamente aporta tanta
  información independiente como 2{,}000 pedidos dispersos en el marco
  completo.
- Un error menor en una corrida con semilla no prueba que un diseño sea
  universalmente superior.
- Los resultados sintéticos no afirman nada sobre ninguna red operativa real.

## Estructura del paquete

```text
L02_Disenos_Muestreo_Probabilistico/
|-- README.md
|-- src/
|   |-- disenos_muestreo_01_aleatorio_simple.py
|   |-- disenos_muestreo_02_estratificado.py
|   `-- disenos_muestreo_03_conglomerados.py
|-- figuras/
|   |-- disenos_muestreo_01_aleatorio_simple.png
|   |-- disenos_muestreo_02_estratificado.png
|   `-- disenos_muestreo_03_conglomerados.png
|-- notebooks/
|   `-- leccion_02_disenos_muestreo_probabilistico.ipynb
`-- diapositivas/
    |-- leccion_02.tex
    `-- leccion_02.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L02_Disenos_Muestreo_Probabilistico/src/disenos_muestreo_01_aleatorio_simple.py
uv run es/L02_Disenos_Muestreo_Probabilistico/src/disenos_muestreo_02_estratificado.py
uv run es/L02_Disenos_Muestreo_Probabilistico/src/disenos_muestreo_03_conglomerados.py
```

Para volver a ejecutar la libreta estudiantil con el entorno bloqueado:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace es/L02_Disenos_Muestreo_Probabilistico/notebooks/leccion_02_disenos_muestreo_probabilistico.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_02.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_02.tex
```

## Atribución OpenStax

Las definiciones y la secuencia curricular de muestreo aleatorio simple,
estratificado y por conglomerados siguen a Alexander Holmes, Barbara Illowsky
y Susan Dean, *Introductory Business Statistics 2e*, Capítulo 1, Sección
[1.2](https://openstax.org/books/introductory-business-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling).
El texto citado está licenciado bajo CC BY-NC-SA 4.0. La población sintética,
el código, las figuras y la comparación con semilla de este paquete son
materiales originales del curso.

