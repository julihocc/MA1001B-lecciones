# Lección 46 - Supuestos de ANOVA: normalidad, homocedasticidad, independencia

Esta microlección de 50 minutos usa el experimento sintético de empaque
para inspeccionar residuos de ANOVA, correr la prueba de Levene y luego
romper la igualdad de varianzas con un segundo ejemplo de $n$ igual. El
paso final muestra que tamaños de muestra equilibrados no rescatan una
desigualdad fuerte de varianzas.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Secciones 12.2 y 12.4 (supuestos de ANOVA y hechos sobre la distribución
  $F$).
- **Prerrequisitos:** La tabla ANOVA de la Lección 44 y Tukey HSD de la
  Lección 45.
- **Aviso de datos:** Cada estación, método de empaque y tiempo de ciclo es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Formar residuos de ANOVA $e_{ij}=y_{ij}-\bar y_i$ e inspeccionar su
   histograma.
2. Usar la prueba de Levene y una gráfica residuo-frente-a-ajustado para
   chequear dispersión igual.
3. Afirmar que la independencia es un supuesto de diseño, no un
   estadístico de gráfica.
4. Explicar por qué $n$ igual no hace a ANOVA inmune a una
   heterocedasticidad fuerte.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: tres supuestos de ANOVA | Nombrar normalidad, varianza igual, independencia. |
| 06-16 | Residuos $e_{ij}=y_{ij}-\bar y_i$ | Confirmar media residual $0$. |
| 16-24 | Ejecutar el Paso 1 | Leer Shapiro $W=0.977891$, $p=0.673807$. |
| 24-34 | Levene y residuo frente a ajustado | Comparar las tres DE muestrales. |
| 34-42 | Ejecutar el Paso 2 | Obtener Levene $p=0.636619$. |
| 42-48 | Ejecutar el Paso 3 y el límite de $n$ igual | Contrastar Levene $p=2.455155\times10^{-4}$ con $F=9.678598$. |
| 48-50 | Verificación de conceptos y transición a la Lección 47 | Pasar de medias de grupo a una recta ajustada. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Los Pasos 1--2 reconstruyen la
muestra de empaque de la Lección 44 con `SEED = 42`. El Paso 3 reconstruye
una segunda muestra de $n$ igual cuyo grupo Automatizado es mucho más
ruidoso. Estos valores provienen de dos ejecuciones coincidentes en el
entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `diagnostico_anova_01_normalidad_residuos.py` | Histograma de residuos y Shapiro-Wilk | Media residual $0.000000$, DE $2.630914$; $W=0.977891$, $p=0.673807$. |
| 2 | `diagnostico_anova_02_levene_homocedasticidad.py` | Levene y residuo frente a ajustado | DE $3.067311$, $2.353358$, $2.660249$; Levene $0.457821$, $p=0.636619$. |
| 3 | `diagnostico_anova_03_limite_varianzas_desiguales.py` | $n$ igual, varianzas desiguales | DE $1.533655$, $1.323764$, $9.975934$; Levene $p=2.455155\times10^{-4}$; $F=9.678598$, $p=4.924585\times10^{-4}$. |

El resultado del Paso 3 es el límite. Los tres grupos siguen teniendo
$n=12$, pero Automatizado es varias veces más ruidoso. Un $F$
significativo ya no es una comparación limpia de medias.

## Diagnósticos sintéticos

Experimento de empaque equilibrado (Pasos 1--2):

- Los residuos son $y$ menos la media del método, de modo que suman 0
  dentro de cada grupo.
- Shapiro-Wilk no rechaza normalidad ($p=0.673807$).
- Levene no rechaza varianzas iguales ($p=0.636619$).
- La independencia se hereda de la asignación aleatoria de estaciones, no
  de una gráfica de residuos.

Ejemplo heterocedástico de $n$ igual (Paso 3):

- Medias $49.773530$, $50.186315$, $59.115014$.
- DE Automatizado $9.975934$ frente a $1.533655$ y $1.323764$.
- Levene rechaza; el $F$ de ANOVA también rechaza. $n$ igual no reparó el
  supuesto.

## Conceptos erróneos comunes

- Un histograma de residuos no puede probar independencia.
- Tamaños de muestra iguales no implican varianzas iguales.
- Un $F$ significativo bajo homocedasticidad rota no es un ranking
  confiable de medias.
- La línea de empaque sintética ilustra diagnósticos. No es una afirmación
  sobre ningún almacén real.

## Estructura del paquete

```text
L46_Diagnostico_Supuestos_ANOVA/
|-- README.md
|-- src/
|   |-- diagnostico_anova_01_normalidad_residuos.py
|   |-- diagnostico_anova_02_levene_homocedasticidad.py
|   `-- diagnostico_anova_03_limite_varianzas_desiguales.py
|-- figuras/
|   |-- diagnostico_anova_01_normalidad_residuos.png
|   |-- diagnostico_anova_02_levene_homocedasticidad.png
|   `-- diagnostico_anova_03_limite_varianzas_desiguales.png
|-- notebooks/
|   `-- leccion_46_diagnostico_supuestos_anova.ipynb
`-- diapositivas/
    |-- leccion_46.tex
    `-- leccion_46.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L46_Diagnostico_Supuestos_ANOVA/src/diagnostico_anova_01_normalidad_residuos.py
uv run es/L46_Diagnostico_Supuestos_ANOVA/src/diagnostico_anova_02_levene_homocedasticidad.py
uv run es/L46_Diagnostico_Supuestos_ANOVA/src/diagnostico_anova_03_limite_varianzas_desiguales.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L46_Diagnostico_Supuestos_ANOVA/notebooks/leccion_46_diagnostico_supuestos_anova.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_46.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_46.tex
```

## Atribución OpenStax

Los supuestos de ANOVA (poblaciones normales, muestras independientes y
desviaciones estándar iguales) siguen a Alexander Holmes, Barbara Illowsky
y Susan Dean, *Introductory Business Statistics 2e*, Secciones
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova)
y
[12.4](https://openstax.org/books/introductory-business-statistics-2e/pages/12-4-facts-about-the-f-distribution).
OpenStax publica este texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

