# Lección 30 - Determinación del tamaño de muestra para margen de error y presupuesto

Esta microlección de 50 minutos planifica $n$ antes de recolectar datos.
Un margen de error para una media usa $n=(z^{*}s/E)^{2}$. Una proporción
usa $n=z^{*2}p(1-p)/E^{2}$, con $p=0.5$ como valor conservador de
planificación. El paso final muestra que $E=0.01$ puede exigir una muestra
que el presupuesto no puede financiar.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 8, Sección 8.4 (cálculo del tamaño de muestra $n$).
- **Prerrequisitos:** Intervalos z para una media y una proporción de las
  Lecciones 27 y 29.
- **Aviso de datos:** Cada valor de planificación, costo y cifra de
  presupuesto es sintético. Los scripts no contienen datos reales de
  empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular $n=(z^{*}s/E)^{2}$ para una media y redondear hacia arriba.
2. Calcular $n=z^{*2}p(1-p)/E^{2}$ para una proporción.
3. Explicar por qué $p=0.5$ es el valor conservador de planificación.
4. Comparar un $n$ estadísticamente requerido con el $n$ que un
   presupuesto puede financiar.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: elegir $E$ antes de muestrear | Escribir la fórmula de la media. |
| 06-16 | Sustituir $z^{*}=1.96$, $s=10$, $E=2$ | Obtener $n$ crudo $=96.040000$. |
| 16-24 | Ejecutar el Paso 1 | Redondear hacia arriba a $n=97$. |
| 24-34 | Fórmula de proporción con $p=0.5$ | Ver $p(1-p)=0.25$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $n=1068$ versus $631$ en $p=0.18$. |
| 42-48 | Ejecutar el Paso 3 con $E=0.01$ | $n$ requerido $=9604$; $n$ asequible $=1666$. |
| 48-50 | Verificación de conceptos y transición a la Lección 31 | Nombrar la varianza como el siguiente parámetro. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye las constantes
de planificación con `SEED = 42` reservada y añade el siguiente concepto
sin importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `sample_size_01_mean_margin.py` | $n=(z^{*}s/E)^{2}$ | $n$ crudo $=96.040000$; $n$ redondeado $=97$. |
| 2 | `sample_size_02_proportion_conservative.py` | $p=0.5$ conservadora | $n=1068$ en $p=0.5$; $n=631$ en $p=0.18$; extra $=437$. |
| 3 | `sample_size_03_budget_vs_precision.py` | $E=0.01$ versus presupuesto | $n$ requerido $=9604$; $n$ asequible $=1666$; costo $\$115{,}248$; no puede financiar. |

El resultado del Paso 3 es un límite: reducir $E$ infla $n$ con $1/E^{2}$.
Un margen deseado no es lo mismo que un estudio financiable.

## Valores sintéticos de planificación

Tiempo medio de atención: $s=10$ minutos, $E=2$ minutos, $z^{*}=1.96$.

\[
n=\left(\frac{1.96\times 10}{2}\right)^{2}=96.040000 \;\to\; 97.
\]

Proporción de primer contacto: $E=0.03$, $p=0.5$ conservadora.

\[
n=\frac{1.96^{2}\times 0.25}{0.03^{2}}=1067.111111 \;\to\; 1068.
\]

El margen estrecho $E=0.01$ en $p=0.5$ exige $n=9604$. A $\$12$ por
observación y un presupuesto de $\$20{,}000$, solo $1666$ observaciones
son asequibles.

## Conceptos erróneos comunes

- El tamaño de muestra se elige antes de los datos, a partir de una $s$ o
  $p$ de planificación, no de la muestra eventual.
- $p=0.5$ es conservadora porque entonces $p(1-p)$ se maximiza.
- Redondear hacia abajo subestima la muestra necesaria para alcanzar $E$.
- Un $E$ menor no es gratis: $n$ crece con $1/E^{2}$.
- Una restricción de presupuesto puede hacer infactible un $E$
  estadísticamente atractivo.
- Los costos sintéticos ilustran la aritmética de planificación. No son
  una afirmación sobre ningún estudio real.

## Estructura del paquete

```text
L30_Determinacion_Tamano_Muestra/
|-- README.md
|-- src/
|   |-- sample_size_01_mean_margin.py
|   |-- sample_size_02_proportion_conservative.py
|   `-- sample_size_03_budget_vs_precision.py
|-- figuras/
|   |-- sample_size_01_mean_margin.png
|   |-- sample_size_02_proportion_conservative.png
|   `-- sample_size_03_budget_vs_precision.png
|-- notebooks/
|   `-- leccion_30_determinacion_tamano_muestra.ipynb
`-- diapositivas/
    |-- leccion_30.tex
    `-- leccion_30.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L30_Determinacion_Tamano_Muestra/src/sample_size_01_mean_margin.py
uv run es/L30_Determinacion_Tamano_Muestra/src/sample_size_02_proportion_conservative.py
uv run es/L30_Determinacion_Tamano_Muestra/src/sample_size_03_budget_vs_precision.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L30_Determinacion_Tamano_Muestra/notebooks/leccion_30_determinacion_tamano_muestra.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de planeación en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_30.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_30.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

Las fórmulas de tamaño de muestra para una media y una proporción siguen a
Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory Business
Statistics 2e*, Capítulo 8, Sección
[8.4](https://openstax.org/books/introductory-business-statistics-2e/pages/8-4-calculating-the-sample-size-n-continuous-and-binary-random-variables).
Los intervalos para una varianza usando la distribución ji-cuadrada se
preparan para la Sección
[11.2](https://openstax.org/books/introductory-business-statistics-2e/pages/11-2-test-of-a-single-variance)
en la Lección 31. OpenStax publica este texto bajo la licencia Creative
Commons Attribution-NonCommercial-ShareAlike. El conjunto sintético, el
código y las figuras de este paquete son materiales originales del curso.

