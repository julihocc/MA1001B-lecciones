# Lección 28 - Intervalo t de Student cuando sigma es desconocida

Esta microlección de 50 minutos usa la misma muestra sintética de la línea
de llenado que la Lección 27, pero ahora $\sigma$ es desconocida. El
intervalo usa $s$ y un valor crítico $t$ con $\mathrm{gl}=n-1$. El paso
final muestra que un atípico extremo infla $s$ y el intervalo.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 8, Sección 8.2 (intervalo de confianza cuando $\sigma$ es
  desconocida).
- **Prerrequisitos:** El intervalo z con sigma conocida de la Lección 27.
- **Aviso de datos:** Cada volumen de llenado es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular $s$ y el error estándar estimado $s/\sqrt{n}$.
2. Obtener $t^{*}$ de la distribución $t$ con $\mathrm{gl}=n-1$.
3. Formar el intervalo $t$ al 95% $\bar{x}\pm t^{*}\cdot s/\sqrt{n}$.
4. Explicar cómo un atípico extremo infla $s$ y la anchura del intervalo.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: $\sigma$ ya no es conocida | Nombrar $s$ como la estimación de escala. |
| 06-16 | Grados de libertad $n-1$ | Confirmar $\mathrm{gl}=35$. |
| 16-24 | Ejecutar el Paso 1 | Leer $s=8.390375$ y $\widehat{\mathrm{EE}}=1.398396$. |
| 24-34 | $t^{*}$ versus $z^{*}=1.96$ | Ver $t^{*}=2.030108$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $[499.899604, 505.577392]$. |
| 42-48 | Ejecutar el Paso 3 con un llenado de 560 ml | Ver que $s$ sube a $12.616189$. |
| 48-50 | Verificación de conceptos y transición a la Lección 29 | Nombrar el siguiente objetivo: una proporción. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos
llenados sintéticos con `SEED = 42` y añade el siguiente concepto sin
importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `t_ci_mean_01_sample_sd.py` | $s$ y $s/\sqrt{n}$ | $n=36$, $\mathrm{gl}=35$, $\bar{x}=502.738498$, $s=8.390375$, $\widehat{\mathrm{EE}}=1.398396$. |
| 2 | `t_ci_mean_02_t_interval.py` | $t^{*}$ de `scipy.stats.t.ppf` | $t^{*}=2.030108$; margen $=2.838894$; IC $[499.899604, 505.577392]$; cubre la $\mu$ verdadera $=502$. |
| 3 | `t_ci_mean_03_outlier_inflates_s.py` | Un atípico de 560 ml infla $s$ | $s$ contaminada $=12.616189$; IC $[499.767301, 508.304710]$; inflación de anchura $=2.859620$. |

El resultado del Paso 3 es un límite del intervalo $t$: la fórmula sigue
algebraicamente definida después de un atípico, pero $s$ ya no es una
estimación de escala estable. La Lección 29 deja las medias y estima una
proporción poblacional.

La [libreta estudiantil ejecutada](notebooks/leccion_28_intervalo_confianza_t_media.ipynb)
es una guía de estudio autocontenida y compatible con Google Colab. Reconstruye
los tres pasos de la lección en un solo estado acumulativo en memoria, embebe
tres figuras e incluye celdas editables de práctica, respuestas desplegables y
aserciones para los valores canónicos. También se ejecutó desde un directorio
temporal vacío y se renderizó a HTML y Markdown sin leer archivos del
repositorio.

## Muestra sintética de la línea de llenado

El analista no conoce $\sigma$. Los scripts generan $n=36$ llenados iid de
$N(502, 10)$ con `SEED = 42`, coincidiendo con la Lección 27, y luego
estiman la escala a partir de la muestra.

\[
\widehat{\mathrm{EE}}=\frac{s}{\sqrt{n}}=\frac{8.390375}{\sqrt{36}}=1.398396,
\]

\[
t^{*}=t_{0.975,35}=2.030108,
\]

\[
\bar{x}\pm t^{*}\cdot\widehat{\mathrm{EE}}=[499.899604, 505.577392].
\]

Sustituir el último llenado por $560$ ml desplaza $\bar{x}$ a $504.036006$
e infla $s$ de $8.390375$ a $12.616189$. La anchura del intervalo crece de
$5.677789$ a $8.537408$.

## Conceptos erróneos comunes

- $s$ no es $\sigma$. La incertidumbre extra es la razón de que $t^{*}>z^{*}$.
- Un intervalo $t$ no es automáticamente más ancho que el intervalo z de la
  Lección 27: esta muestra tiene $s<\sigma$, de modo que el margen $t$
  todavía puede ser menor.
- Una observación extrema puede dominar $s$ incluso cuando $n=36$.
- El procedimiento $t$ supone normalidad aproximada de la población.
- Cubrir la $\mu$ oculta en esta muestra con semilla 42 no prueba
  robustez frente a atípicos.
- Los llenados sintéticos ilustran la aritmética $t$. No son una
  afirmación sobre ninguna línea de llenado real.

## Estructura del paquete

```text
L28_Intervalo_Confianza_T_Media/
|-- README.md
|-- src/
|   |-- t_ci_mean_01_sample_sd.py
|   |-- t_ci_mean_02_t_interval.py
|   `-- t_ci_mean_03_outlier_inflates_s.py
|-- figuras/
|   |-- t_ci_mean_01_sample_sd.png
|   |-- t_ci_mean_02_t_interval.png
|   `-- t_ci_mean_03_outlier_inflates_s.png
|-- notebooks/
|   `-- leccion_28_intervalo_confianza_t_media.ipynb
`-- diapositivas/
    |-- leccion_28.tex
    `-- leccion_28.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L28_Intervalo_Confianza_T_Media/src/t_ci_mean_01_sample_sd.py
uv run es/L28_Intervalo_Confianza_T_Media/src/t_ci_mean_02_t_interval.py
uv run es/L28_Intervalo_Confianza_T_Media/src/t_ci_mean_03_outlier_inflates_s.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L28_Intervalo_Confianza_T_Media/notebooks/leccion_28_intervalo_confianza_t_media.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_28.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_28.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

El intervalo $t$ de Student para una media cuando la desviación estándar
poblacional es desconocida sigue a Alexander Holmes, Barbara Illowsky y
Susan Dean, *Introductory Business Statistics 2e*, Capítulo 8, Sección
[8.2](https://openstax.org/books/introductory-business-statistics-2e/pages/8-2-a-confidence-interval-when-the-population-standard-deviation-is-unknown-and-small-sample-case).
El siguiente objetivo, una proporción poblacional, se prepara para la
Sección
[8.3](https://openstax.org/books/introductory-business-statistics-2e/pages/8-3-a-confidence-interval-for-a-population-proportion)
en la Lección 29. OpenStax publica este texto bajo la licencia Creative
Commons Attribution-NonCommercial-ShareAlike. El conjunto sintético, el
código y las figuras de este paquete son materiales originales del curso.

