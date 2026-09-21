# Lección 36 - Prueba de hipótesis para una proporción de negocio

Esta microlección de 50 minutos usa un registro de inspección completamente
sintético para probar $H_0:p=0.10$ con $n=200$ lotes y $x=28$ banderas de
retraso. El estadístico $z$ usa $p_0$ en el error estándar. El paso final
muestra que sustituir $\hat{p}$ en ese error estándar es el estadístico de
prueba incorrecto y puede invertir la decisión con $\alpha=0.05$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 9, Sección 9.4 (ejemplos completos de pruebas de hipótesis,
  incluida una proporción). Compañero: *Introductory Statistics 2e*,
  Sección 9.4.
- **Prerrequisitos:** Lenguaje de pruebas de hipótesis de la Lección 33 y la
  prueba $t$ de una media de la Lección 35.
- **Aviso de datos:** Cada lote y bandera de retraso es sintético. Los
  scripts no contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar $H_0:p=p_0$ frente a una $H_1$ unilateral para una proporción de
   negocio.
2. Comprobar $np_0>5$ y $n(1-p_0)>5$ antes de usar una prueba z normal.
3. Calcular $z=(\hat{p}-p_0)/\sqrt{p_0(1-p_0)/n}$ y un valor p de cola
   derecha.
4. Explicar por qué el error estándar de la prueba debe usar $p_0$, no
   $\hat{p}$.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: un reclamo de 10 por ciento de banderas de retraso | Escribir $H_0:p=0.10$ y $H_1:p>0.10$. |
| 06-16 | Proporción muestral y condiciones | Confirmar $28/200=0.14$ y $np_0=20$. |
| 16-24 | Ejecutar el Paso 1 | Leer $\hat{p}=0.140000$, $np_0=20$, $n(1-p_0)=180$. |
| 24-34 | EE bajo $H_0$ y la fórmula $z$ | Escribir $\sqrt{0.10\times0.90/200}$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $z=1.885618$, $p=0.029673$, rechazar $H_0$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar $p=0.029673$ con el $p$ incorrecto $0.051521$. |
| 48-50 | Verificación de conceptos y paso a la Lección 37 | Nombrar la siguiente herramienta: dos medias independientes. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos
conteos sintéticos y no importa otro script de la lección. Estos valores
provienen de dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `prueba_proporcion_01_muestra_y_condiciones.py` | $\hat{p}$, $np_0$ y $n(1-p_0)$ | $n=200$, $x=28$, $\hat{p}=0.140000$, $p_0=0.100000$, $np_0=20$, $n(1-p_0)=180$, condiciones cumplidas. |
| 2 | `prueba_proporcion_02_z_valor_p.py` | $z$ con $p_0$ en el EE, $p$ de cola derecha | $EE=0.021213$, $z=1.885618$, $p=0.029673$, $z^*=1.644854$, rechazar $H_0$ con $\alpha=0.05$. |
| 3 | `prueba_proporcion_03_limite_ee_incorrecto.py` | $\hat{p}$ en el EE es el estadístico incorrecto | EE incorrecto $=0.024536$, $z$ incorrecto $=1.630278$, $p$ incorrecto $=0.051521$; la decisión se invierte a no rechazar $H_0$. |

El resultado del Paso 3 es un límite, no una segunda prueba legítima. Un
intervalo de confianza para $p$ puede usar $\hat{p}$ en el error estándar;
una prueba de $H_0:p=p_0$ no. La Lección 37 pasa de una muestra a dos medias
independientes.

## Registro sintético de inspección

\[
\hat{p}=\frac{28}{200}=0.14,\qquad
EE_0=\sqrt{\frac{0.10\times0.90}{200}}=0.021213,
\]

\[
z=\frac{0.14-0.10}{0.021213}=1.885618,\qquad
p=P(Z\ge 1.885618)=0.029673.
\]

La prueba de cola derecha rechaza $H_0:p=0.10$ con $\alpha=0.05$. Reemplazar
$p_0$ por $\hat{p}$ infla el error estándar a $0.024536$ y produce
$z=1.630278$ con $p=0.051521$, que no rechaza. Ese segundo cálculo no es el
estadístico de la prueba de hipótesis.

## Conceptos erróneos comunes

- $\hat{p}$ estima $p$, pero la prueba de $H_0:p=p_0$ estandariza con $p_0$.
- El EE del intervalo de Wald y el EE de la prueba no son intercambiables.
- $np_0$ y $n(1-p_0)$ se comprueban bajo $H_0$, no con $\hat{p}$.
- No rechazar después de usar el EE incorrecto no es un segundo análisis de
  la misma hipótesis; es un estadístico distinto e incorrecto.
- Las banderas de retraso sintéticas ilustran el procedimiento $z$. No
  afirman nada sobre ningún proceso real de inspección.

## Estructura del paquete

```text
L36_Prueba_Hipotesis_Proporcion/
|-- README.md
|-- src/
|   |-- prueba_proporcion_01_muestra_y_condiciones.py
|   |-- prueba_proporcion_02_z_valor_p.py
|   `-- prueba_proporcion_03_limite_ee_incorrecto.py
|-- figuras/
|   |-- prueba_proporcion_01_muestra_y_condiciones.png
|   |-- prueba_proporcion_02_z_valor_p.png
|   `-- prueba_proporcion_03_limite_ee_incorrecto.png
|-- notebooks/
|   `-- leccion_36_prueba_hipotesis_proporcion.ipynb
`-- diapositivas/
    |-- leccion_36.tex
    `-- leccion_36.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L36_Prueba_Hipotesis_Proporcion/src/prueba_proporcion_01_muestra_y_condiciones.py
uv run es/L36_Prueba_Hipotesis_Proporcion/src/prueba_proporcion_02_z_valor_p.py
uv run es/L36_Prueba_Hipotesis_Proporcion/src/prueba_proporcion_03_limite_ee_incorrecto.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L36_Prueba_Hipotesis_Proporcion/notebooks/leccion_36_prueba_hipotesis_proporcion.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_36.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_36.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La prueba $z$ de una proporción, las condiciones $np_0$ y $n(1-p_0)$, y el
requisito de que el error estándar use $p_0$ siguen a Alexander Holmes,
Barbara Illowsky y Susan Dean, *Introductory Business Statistics 2e*,
Capítulo 9, Secciones
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-probability-distribution-needed-for-hypothesis-testing)
y
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples).
Práctica compañera de prueba de proporción está en *Introductory Statistics
2e*, Sección
[9.4](https://openstax.org/books/introductory-statistics-2e/pages/9-4-full-hypothesis-test-examples).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

