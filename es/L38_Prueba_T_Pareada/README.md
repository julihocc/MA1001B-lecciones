# Lección 38 - Muestras pareadas (t antes-después)

Esta microlección de 50 minutos usa 25 estaciones de empaque completamente
sintéticas medidas antes y después de un cambio de layout. La unidad
observacional es la estación, así que la prueba es una $t$ de una muestra
sobre $d=\text{antes}-\text{después}$. El paso final muestra que una $t$ de
dos muestras no pareada sobre las mismas columnas ignora el emparejamiento y
puede invertir la decisión con $\alpha=0.05$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 10, Sección 10.6 (muestras emparejadas o pareadas).
- **Prerrequisitos:** $t$ de una muestra de la Lección 35 y dos medias
  independientes de la Lección 37.
- **Aviso de datos:** Cada tiempo de manejo es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Formar diferencias pareadas a partir de mediciones antes-después en las
   mismas unidades.
2. Ejecutar una prueba $t$ de una muestra de $H_0:\mu_d=0$ con $gl=n-1$.
3. Contrastar el error estándar pareado con un EE de dos muestras no pareado.
4. Explicar por qué el análisis no pareado de datos pareados ignora el
   emparejamiento.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: las mismas 25 estaciones dos veces | Esbozar $d_i=\text{antes}_i-\text{después}_i$. |
| 06-16 | Diferencia media y $s_d$ | Contrastar $s_d$ con $s_{\text{antes}}$ y $s_{\text{después}}$. |
| 16-24 | Ejecutar el Paso 1 | Leer $\bar{d}=2.720813$, $s_d=1.525772$, $r=0.973356$. |
| 24-34 | $t$ pareada como $t$ de una muestra sobre $d$ | Escribir $t=\bar{d}/(s_d/\sqrt{n})$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $t=8.916186$, $p=4.395592\times10^{-9}$, rechazar $H_0$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar $p$ pareado $=4.395592\times10^{-9}$ con $p$ no pareado $=0.147291$. |
| 48-50 | Verificación de conceptos y paso a la Lección 39 | Nombrar la siguiente herramienta: dos proporciones en una prueba A/B. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos 25
pares con `SEED = 42` y no importa otro script de la lección. Estos valores
provienen de dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `t_pareada_01_diferencias.py` | Diferencias emparejadas | $n=25$; $\bar{x}_{\text{antes}}=54.716880$, $\bar{x}_{\text{después}}=51.996067$; $\bar{d}=2.720813$; $s_d=1.525772$; $r=0.973356$. |
| 2 | `t_pareada_02_prueba_pareada.py` | $t$ de una muestra sobre $d$ | $EE=0.305154$, $t=8.916186$, $gl=24$, $p=4.395592\times10^{-9}$, $t^*=2.063899$, rechazar $H_0$. |
| 3 | `t_pareada_03_limite_no_pareada.py` | El análisis no pareado ignora el emparejamiento | EE no pareado $=1.847143$, $t=1.472985$, $p=0.147291$, no rechazar $H_0$. |

El resultado del Paso 3 es un límite, no una segunda prueba legítima del
cambio de layout. El pareo es el diseño. La Lección 39 compara dos
proporciones independientes en una prueba A/B.

## Registro sintético de estaciones

\[
t=\frac{\bar{d}-0}{s_d/\sqrt{n}}=\frac{2.720813}{0.305154}=8.916186,
\qquad gl=24,
\]

\[
p=2P(T_{24}\ge 8.916186)=4.395592\times10^{-9}.
\]

La correlación antes-después es $0.973356$. Ese emparejamiento encoge el EE
del no pareado $1.847143$ al pareado $0.305154$. Descartar el pareo infla
$p$ de $4.395592\times10^{-9}$ a $0.147291$ e invierte la decisión con
$\alpha=0.05$.

## Conceptos erróneos comunes

- Dos columnas de tiempos están pareadas solo cuando cada fila es la misma
  unidad.
- La prueba pareada no compara $\bar{x}_{\text{antes}}$ con
  $\bar{x}_{\text{después}}$ mediante un EE de dos muestras.
- Una $s_{\text{antes}}$ grande no bloquea un hallazgo pareado si $s_d$ es
  pequeña.
- El análisis no pareado de datos pareados no es una comprobación de
  robustez; es el modelo muestral incorrecto.
- Las estaciones sintéticas ilustran la $t$ pareada. No afirman nada sobre
  ningún cambio real de layout.

## Estructura del paquete

```text
L38_Prueba_T_Pareada/
|-- README.md
|-- src/
|   |-- t_pareada_01_diferencias.py
|   |-- t_pareada_02_prueba_pareada.py
|   `-- t_pareada_03_limite_no_pareada.py
|-- figuras/
|   |-- t_pareada_01_diferencias.png
|   |-- t_pareada_02_prueba_pareada.png
|   `-- t_pareada_03_limite_no_pareada.png
|-- notebooks/
|   `-- leccion_38_prueba_t_pareada.ipynb
`-- diapositivas/
    |-- leccion_38.tex
    `-- leccion_38.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L38_Prueba_T_Pareada/src/t_pareada_01_diferencias.py
uv run es/L38_Prueba_T_Pareada/src/t_pareada_02_prueba_pareada.py
uv run es/L38_Prueba_T_Pareada/src/t_pareada_03_limite_no_pareada.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L38_Prueba_T_Pareada/notebooks/leccion_38_prueba_t_pareada.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_38.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_38.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

Las pruebas de hipótesis de pares emparejados, la reducción a una $t$ de una
muestra sobre las diferencias y el contraste con muestras independientes
siguen a Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory
Business Statistics 2e*, Capítulo 10, Sección
[10.6](https://openstax.org/books/introductory-business-statistics-2e/pages/10-6-matched-or-paired-samples).
Práctica compañera de muestras pareadas está en *Introductory Statistics 2e*,
Sección
[10.4](https://openstax.org/books/introductory-statistics-2e/pages/10-4-matched-or-paired-samples).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

