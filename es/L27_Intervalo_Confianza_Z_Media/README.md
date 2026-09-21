# Lección 27 - Intervalo de confianza Z para una media (sigma conocida)

Esta microlección de 50 minutos usa una muestra sintética de una línea de
llenado para construir un intervalo z al 95% cuando la desviación estándar
poblacional se trata como conocida. El paso final muestra que sustituir
$\sigma$ por $s$ conservando $z^{*}=1.96$ es la herramienta equivocada, que
la Lección 28 nombra como el intervalo $t$ de Student.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 8, Sección 8.1 (intervalo de confianza cuando $\sigma$ es
  conocida o la muestra es grande).
- **Prerrequisitos:** Distribución muestral de la media y el teorema del
  límite central de las Lecciones 23-24, más estimación puntual de la
  Lección 26.
- **Aviso de datos:** Cada volumen de llenado es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular el error estándar $\sigma/\sqrt{n}$ cuando $\sigma$ es
   conocida.
2. Formar el intervalo z al 95% $\bar{x}\pm 1.96\cdot\sigma/\sqrt{n}$.
3. Interpretar el intervalo como un rango para la media desconocida, no
   para una botella.
4. Explicar por qué una $\sigma$ desconocida hace del intervalo z el
   procedimiento equivocado.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: $\sigma$ conocida, $\mu$ desconocida | Nombrar la estimación puntual $\bar{x}$. |
| 06-16 | Error estándar $\sigma/\sqrt{n}$ | Confirmar $10/\sqrt{36}=1.666667$. |
| 16-24 | Ejecutar el Paso 1 | Leer $\bar{x}=502.738498$ ml. |
| 24-34 | Margen $1.96\times$ EE | Calcular $3.266667$ ml. |
| 34-42 | Ejecutar el Paso 2 | Obtener $[499.471831, 506.005165]$. |
| 42-48 | Ejecutar el Paso 3 y contrastar $s$ con $\sigma$ | Ver $s=8.390375\neq 10$. |
| 48-50 | Verificación de conceptos y transición a la Lección 28 | Nombrar $t$ como la herramienta de $\sigma$ desconocida. |

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
| 1 | `z_ci_mean_01_sample_standard_error.py` | Media muestral y EE con sigma conocida | $n=36$, $\sigma=10$, $\bar{x}=502.738498$, $\mathrm{EE}=1.666667$. |
| 2 | `z_ci_mean_02_z_interval.py` | Intervalo z al 95% con $z^{*}=1.96$ | Margen $=3.266667$; IC $[499.471831, 506.005165]$; anchura $=6.533333$; cubre la $\mu$ verdadera $=502$. |
| 3 | `z_ci_mean_03_unknown_sigma_limit.py` | $s$ no es $\sigma$; z-con-$s$ es inválido | $s=8.390375$; intervalo z-con-$s$ inválido $[499.997642, 505.479354]$; diferencia de anchura $=1.051622$. |

El resultado del Paso 3 es un límite, no un intervalo $t$ todavía. El
intervalo z válido requiere una $\sigma$ conocida. La Lección 28 sustituye
$z^{*}$ por un valor crítico $t$ con $\mathrm{gl}=n-1$.

La [libreta estudiantil](notebooks/leccion_27_intervalo_confianza_z_media.ipynb)
ejecutada es una guía de estudio autocontenida y compatible con Google Colab.
Reconstruye los tres pasos en un estado acumulativo en memoria, embebe tres
figuras e incluye prácticas editables, respuestas plegables y aserciones para
los valores canónicos. También se ejecutó desde un directorio temporal vacío y
se renderizó a HTML y Markdown sin leer archivos del repositorio.

## Muestra sintética de la línea de llenado

El analista trata $\sigma=10$ ml como conocida a partir de la capacidad de
proceso de largo plazo y no conoce $\mu$. Los scripts generan $n=36$
llenados iid de $N(502, 10)$ solo para poder verificar la cobertura de la
media oculta.

\[
\mathrm{EE}=\frac{\sigma}{\sqrt{n}}=\frac{10}{\sqrt{36}}=1.666667,
\]

\[
\bar{x}\pm 1.96\cdot\mathrm{EE}=502.738498\pm 3.266667=[499.471831, 506.005165].
\]

La desviación estándar muestral de los mismos 36 llenados es $s=8.390375$,
que no es $\sigma$. Conservar $z^{*}=1.96$ después de esa sustitución
produce un intervalo más estrecho que ya no es un procedimiento z.

## Conceptos erróneos comunes

- Un intervalo al 95% no es un enunciado de probabilidad del 95% sobre
  esta muestra una vez observados los datos.
- El intervalo estima la media poblacional, no el llenado de la siguiente
  botella.
- $s$ es un estadístico. No autoriza el valor crítico z.
- Un intervalo más corto no es automáticamente un intervalo mejor.
- Cubrir la $\mu$ oculta en esta muestra con semilla 42 no prueba que el
  método siempre cubra $\mu$.
- Los llenados sintéticos ilustran la aritmética z. No son una afirmación
  sobre ninguna línea de llenado real.

## Estructura del paquete

```text
L27_Intervalo_Confianza_Z_Media/
|-- README.md
|-- src/
|   |-- z_ci_mean_01_sample_standard_error.py
|   |-- z_ci_mean_02_z_interval.py
|   `-- z_ci_mean_03_unknown_sigma_limit.py
|-- figuras/
|   |-- z_ci_mean_01_sample_standard_error.png
|   |-- z_ci_mean_02_z_interval.png
|   `-- z_ci_mean_03_unknown_sigma_limit.png
|-- notebooks/
|   `-- leccion_27_intervalo_confianza_z_media.ipynb
`-- diapositivas/
    |-- leccion_27.tex
    `-- leccion_27.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L27_Intervalo_Confianza_Z_Media/src/z_ci_mean_01_sample_standard_error.py
uv run es/L27_Intervalo_Confianza_Z_Media/src/z_ci_mean_02_z_interval.py
uv run es/L27_Intervalo_Confianza_Z_Media/src/z_ci_mean_03_unknown_sigma_limit.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L27_Intervalo_Confianza_Z_Media/notebooks/leccion_27_intervalo_confianza_z_media.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_27.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_27.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

El intervalo z para una media cuando la desviación estándar poblacional es
conocida sigue a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Capítulo 8, Sección
[8.1](https://openstax.org/books/introductory-business-statistics-2e/pages/8-1-a-confidence-interval-when-the-population-standard-deviation-is-known-or-large-sample-size).
El límite de $\sigma$ desconocida se prepara para la Sección
[8.2](https://openstax.org/books/introductory-business-statistics-2e/pages/8-2-a-confidence-interval-when-the-population-standard-deviation-is-unknown-and-small-sample-case)
en la Lección 28. OpenStax publica este texto bajo la licencia Creative
Commons Attribution-NonCommercial-ShareAlike. El conjunto sintético, el
código y las figuras de este paquete son materiales originales del curso.

