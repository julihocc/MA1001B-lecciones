# Lección 33 - Fundamentos de pruebas de hipótesis: H0, H1, tipo I y tipo II

Esta microlección de 50 minutos fija el lenguaje de una prueba unilateral
$H_{0}:\mu=50$ frente a $H_{1}:\mu>50$ con $\alpha=0.05$. Una simulación con
semilla 42 recupera una tasa de tipo I cercana a $\alpha$. Luego se mide la
potencia en $\mu=53$. El paso final muestra que no rechazar $H_{0}$ no prueba
que $H_{0}$ sea verdadera.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 9, Secciones 9.1 y 9.2 (hipótesis; errores de tipo I y tipo II).
- **Prerrequisitos:** Distribución muestral de la media y el intervalo z con
  sigma conocida de las Lecciones 23 y 27.
- **Aviso de datos:** Cada tiempo de ciclo es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar $H_{0}$ y $H_{1}$ para una prueba unilateral de media.
2. Convertir $\alpha$ en un corte de rechazo para $\bar{x}$.
3. Interpretar un error de tipo I como rechazar una $H_{0}$ verdadera.
4. Explicar por qué no rechazar $H_{0}$ no prueba que $H_{0}$ sea verdadera.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: $H_{0}:\mu=50$ frente a $H_{1}:\mu>50$ | Escribir ambas hipótesis. |
| 06-16 | $\alpha=0.05$ como área de cola | Confirmar $z^{*}=1.644854$. |
| 16-24 | Ejecutar el Paso 1 | Leer el corte $\bar{x}=52.193138$. |
| 24-34 | Definición de tipo I | Nombrar un rechazo falso. |
| 34-42 | Ejecutar el Paso 2 | Tasa simulada de tipo I $0.053100$. |
| 42-48 | Ejecutar el Paso 3 de potencia y un fallo cercano | Potencia $0.724100$; $\bar{x}=51.590798$ cercano no rechaza. |
| 48-50 | Verificación de conceptos y paso a la Lección 34 | Nombrar la prueba z de una muestra. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el esquema de
prueba con `SEED = 42` y no importa otro script de la lección. Estos valores
provienen de dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `fundamentos_ph_01_hipotesis_alfa.py` | $H_{0}$, $H_{1}$, $\alpha$, corte | $n=36$, $\sigma=8$, $\mathrm{EE}=1.333333$, $z^{*}=1.644854$, corte $=52.193138$. |
| 2 | `fundamentos_ph_02_tasa_tipo_i.py` | Tasa simulada de tipo I | 531 rechazos en 10{,}000 muestras $H_{0}$; tasa $=0.053100$. |
| 3 | `fundamentos_ph_03_tipo_ii_no_prueba.py` | Potencia y no es prueba | Potencia en $\mu=53$ es $0.724100$; tipo II $=0.275900$; muestra $\mu=51$ con $\bar{x}=51.590798$ no rechaza. |

El resultado del Paso 3 es un límite: un no rechazo puede ocurrir cuando
$H_{0}$ es falsa. La ausencia de evidencia contra $H_{0}$ no es prueba de
$H_{0}$.

## Prueba unilateral sintética

$\sigma=8$ conocida, $n=36$, $\mathrm{EE}=8/\sqrt{36}=1.333333$.

\[
\bar{x}_{\text{crit}}=50+1.644854\times 1.333333=52.193138.
\]

Se rechaza $H_{0}$ cuando $\bar{x}\ge 52.193138$. Bajo $\mu=50$ la tasa
simulada de rechazo falso es $0.053100$. Bajo $\mu=53$ la prueba detecta el
desplazamiento en $0.724100$ de 10{,}000 muestras, así que aún pierde
$0.275900$ de ellas.

## Conceptos erróneos comunes

- $\alpha$ se elige antes de ver la muestra, no después.
- Un error de tipo I no es «la prueba está mal»; es un rechazo falso cuando
  $H_{0}$ es verdadera.
- La potencia no es 1 solo porque $H_{1}$ sea verdadera.
- No rechazar $H_{0}$ no es lo mismo que probar $\mu=50$.
- Los ciclos sintéticos ilustran tasas de error. No afirman nada sobre ningún
  objetivo real de empaque.

## Estructura del paquete

```text
L33_Fundamentos_Pruebas_Hipotesis/
|-- README.md
|-- src/
|   |-- fundamentos_ph_01_hipotesis_alfa.py
|   |-- fundamentos_ph_02_tasa_tipo_i.py
|   `-- fundamentos_ph_03_tipo_ii_no_prueba.py
|-- figuras/
|   |-- fundamentos_ph_01_hipotesis_alfa.png
|   |-- fundamentos_ph_02_tasa_tipo_i.png
|   `-- fundamentos_ph_03_tipo_ii_no_prueba.png
|-- notebooks/
|   `-- leccion_33_fundamentos_pruebas_hipotesis.ipynb
`-- diapositivas/
    |-- leccion_33.tex
    `-- leccion_33.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L33_Fundamentos_Pruebas_Hipotesis/src/fundamentos_ph_01_hipotesis_alfa.py
uv run es/L33_Fundamentos_Pruebas_Hipotesis/src/fundamentos_ph_02_tasa_tipo_i.py
uv run es/L33_Fundamentos_Pruebas_Hipotesis/src/fundamentos_ph_03_tipo_ii_no_prueba.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L33_Fundamentos_Pruebas_Hipotesis/notebooks/leccion_33_fundamentos_pruebas_hipotesis.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_33.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_33.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

Las hipótesis nula y alternativa, los errores de tipo I y tipo II, y el
papel de $\alpha$ siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Capítulo 9, Secciones
[9.1](https://openstax.org/books/introductory-business-statistics-2e/pages/9-1-null-and-alternative-hypotheses)
y
[9.2](https://openstax.org/books/introductory-business-statistics-2e/pages/9-2-outcomes-and-the-type-i-and-type-ii-errors).
La prueba z de una muestra con varianza conocida se prepara para las
Secciones
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-distribution-needed-for-hypothesis-testing)
y
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples)
en la Lección 34. OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

