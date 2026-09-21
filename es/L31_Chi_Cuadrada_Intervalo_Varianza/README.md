# Lección 31 - Chi-cuadrada e intervalo de confianza para la varianza

Esta microlección de 50 minutos usa una muestra de empaque completamente
sintética de $n=20$ tiempos de ciclo para estimar $\sigma^{2}$. El intervalo
usa valores críticos chi-cuadrada con $\mathrm{gl}=n-1$. El paso final muestra
que los datos no normales invalidan el procedimiento: la cobertura se derrumba
bajo ciclos exponenciales.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 11, Sección 11.2 (prueba de una sola varianza), usada aquí para
  construir el intervalo correspondiente para $\sigma^{2}$.
- **Prerrequisitos:** Varianza muestral y la idea de una distribución
  muestral de lecciones previas de estimación.
- **Aviso de datos:** Cada tiempo de ciclo es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular $s^{2}$ con divisor $n-1$.
2. Obtener valores críticos chi-cuadrada con $\mathrm{gl}=n-1$.
3. Formar el intervalo al 95% $((n-1)s^{2}/\chi^{2}_{U},(n-1)s^{2}/\chi^{2}_{L})$.
4. Explicar por qué los datos no normales invalidan el intervalo chi-cuadrada
   para la varianza.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: la varianza como parámetro de proceso | Nombrar $s^{2}$ como el estimador puntual. |
| 06-16 | Grados de libertad $n-1$ | Confirmar $\mathrm{gl}=19$. |
| 16-24 | Ejecutar el Paso 1 | Leer $s^{2}=6.814885$. |
| 24-34 | Cuantiles chi-cuadrada | Ver $8.906516$ y $32.852327$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $[3.941359, 14.537986]$. |
| 42-48 | Ejecutar el Paso 3 de cobertura | Contrastar $0.949400$ con $0.737200$. |
| 48-50 | Verificación de conceptos y paso a la Lección 32 | Nombrar una segunda varianza y $F$. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos ciclos
sintéticos con `SEED = 42` y no importa otro script de la lección. Estos
valores provienen de dos ejecuciones coincidentes en el entorno bloqueado de
`uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `chi_cuadrada_01_varianza_muestral.py` | $s^{2}$ con $\mathrm{gl}=19$ | $n=20$, $\bar{x}=11.901204$, $s=2.610533$, $s^{2}=6.814885$. |
| 2 | `chi_cuadrada_02_intervalo_varianza.py` | Intervalo chi-cuadrada al 95% para $\sigma^{2}$ | $\chi^{2}_{L}=8.906516$, $\chi^{2}_{U}=32.852327$; IC $[3.941359, 14.537986]$; cubre la $\sigma^{2}=9$ oculta. |
| 3 | `chi_cuadrada_03_limite_no_normal.py` | Cobertura bajo ciclos no normales | Cobertura normal $0.949400$; cobertura exponencial $0.737200$ (5000 reps). |

El resultado del Paso 3 es un límite: la fórmula sigue corriendo sobre datos
sesgados, pero ya no cubre cerca del 95% de las veces.

## Ciclos sintéticos de empaque

Los scripts generan $n=20$ tiempos de ciclo iid $N(12,3)$ para que se pueda
verificar la $\sigma^{2}=9$ oculta.

\[
\frac{(n-1)s^{2}}{\chi^{2}_{0.975,19}}
\le \sigma^{2} \le
\frac{(n-1)s^{2}}{\chi^{2}_{0.025,19}},
\]

\[
[3.941359, 14.537986].
\]

El intervalo no es simétrico alrededor de $s^{2}$. Ciclos exponenciales con
varianza verdadera $144$ producen cobertura empírica $0.737200$.

## Conceptos erróneos comunes

- El intervalo chi-cuadrada para $\sigma^{2}$ no es $\bar{x}\pm z\cdot\mathrm{EE}$.
- Los valores críticos van en el denominador, de modo que el valor chi-cuadrada
  más grande produce el límite inferior.
- Una cobertura aproximada del 95% es una propiedad del método bajo
  normalidad, no una garantía para una sola muestra.
- Tiempos de ciclo sesgados pueden dejar $s^{2}$ definida y destruir la
  cobertura.
- Los ciclos sintéticos ilustran la aritmética chi-cuadrada. No afirman nada
  sobre ninguna estación de empaque real.

## Estructura del paquete

```text
L31_Chi_Cuadrada_Intervalo_Varianza/
|-- README.md
|-- src/
|   |-- chi_cuadrada_01_varianza_muestral.py
|   |-- chi_cuadrada_02_intervalo_varianza.py
|   `-- chi_cuadrada_03_limite_no_normal.py
|-- figuras/
|   |-- chi_cuadrada_01_varianza_muestral.png
|   |-- chi_cuadrada_02_intervalo_varianza.png
|   `-- chi_cuadrada_03_limite_no_normal.png
|-- notebooks/
|   `-- leccion_31_chi_cuadrada_intervalo_varianza.ipynb
`-- diapositivas/
    |-- leccion_31.tex
    `-- leccion_31.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L31_Chi_Cuadrada_Intervalo_Varianza/src/chi_cuadrada_01_varianza_muestral.py
uv run es/L31_Chi_Cuadrada_Intervalo_Varianza/src/chi_cuadrada_02_intervalo_varianza.py
uv run es/L31_Chi_Cuadrada_Intervalo_Varianza/src/chi_cuadrada_03_limite_no_normal.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L31_Chi_Cuadrada_Intervalo_Varianza/notebooks/leccion_31_chi_cuadrada_intervalo_varianza.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_31.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_31.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La distribución muestral chi-cuadrada de $(n-1)s^{2}/\sigma^{2}$ y la
inferencia para una sola varianza siguen a Alexander Holmes, Barbara Illowsky
y Susan Dean, *Introductory Business Statistics 2e*, Capítulo 11, Sección
[11.2](https://openstax.org/books/introductory-business-statistics-2e/pages/11-2-test-of-a-single-variance).
La comparación de dos varianzas con la distribución $F$ se prepara para la
Sección
[12.1](https://openstax.org/books/introductory-business-statistics-2e/pages/12-1-test-of-two-variances)
en la Lección 32. OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

