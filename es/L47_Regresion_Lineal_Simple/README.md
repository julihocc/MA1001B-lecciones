# Lección 47 - Regresión lineal simple: mínimos cuadrados y R-cuadrada

Esta microlección de 50 minutos usa una muestra sintética de 40 semanas de
un centro de correo. Los estudiantes dispersan horas de coaching contra
unidades empacadas por hora-labor, ajustan la recta de mínimos cuadrados
$y=12+0.45x$ más ruido, y luego ven que una $R^2$ alta no es una palanca
causal.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Secciones 13.3 y 13.4 (ecuaciones lineales y la ecuación de regresión).
- **Prerrequisitos:** Nubes de puntos y correlación de resúmenes numéricos
  anteriores, más el contraste observacional-frente-a-aleatorizado de la
  Lección 43.
- **Aviso de datos:** Cada semana, hora de coaching y valor de
  productividad es sintético. Los scripts no contienen datos reales de
  empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Leer una nube de un predictor numérico y una respuesta numérica.
2. Calcular la pendiente y el intercepto de mínimos cuadrados a partir de
   $S_{xx}$ y $S_{xy}$.
3. Descomponer $SST=SSR+SSE$ y formar $R^2=1-SSE/SST$.
4. Explicar por qué una $R^2$ alta no autoriza una política causal de
   coaching.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: 40 semanas, $x$ horas de coaching, $y$ unidades por hora | Esbozar la nube. |
| 06-16 | Nube de puntos, aún sin recta | Leer $n=40$ y $r=0.910813$. |
| 16-24 | Ejecutar el Paso 1 | Confirmar el rango de $x$ $9.402$ a $39.220$. |
| 24-34 | Ecuaciones normales en el pizarrón | Comparar la pendiente manual con scipy. |
| 34-42 | Ejecutar el Paso 2 | Obtener $b_1=0.405936$, $b_0=13.136554$. |
| 42-48 | Ejecutar el Paso 3 y el límite de $R^2$ | Leer $R^2=0.829580$; rechazar la palanca causal. |
| 48-50 | Verificación de conceptos y transición a la Lección 48 | Pedir $EE(b_1)$ y gráficas de residuos. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma
muestra sintética de 40 semanas con `SEED = 42` y añade el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `regresion_simple_01_dispersion.py` | Nube de $x$ y $y$ | $n=40$; $\bar x=25.075277$; $\bar y=23.315500$; $r=0.910813$. |
| 2 | `regresion_simple_02_minimos_cuadrados.py` | Pendiente e intercepto de mínimos cuadrados | $b_1=0.405936$, $b_0=13.136554$; pendiente verdadera $0.45$; $SSE=113.102672$. |
| 3 | `regresion_simple_03_limite_r_cuadrada.py` | $R^2$ no es una palanca causal | $SST=663.669939$, $SSR=550.567267$, $R^2=0.829580$; ganancia ajustada $+10$h $4.059355$. |

El resultado del Paso 3 es un límite. $R^2=0.829580$ dice que la recta
sigue estas 40 semanas observadas. Las horas de coaching no se asignaron
al azar, de modo que la pendiente no es un botón de política. La Lección
48 añade $EE(b_1)$, una prueba $t$, gráficas de residuos y un punto
influyente.

## Ajuste sintético de mínimos cuadrados

Recta verdadera: $y=12+0.45x+\varepsilon$. Recta ajustada:

\[
\hat y=13.136554+0.405936\,x.
\]

Identidad de variación:

\[
SST=SSR+SSE=550.567267+113.102672=663.669939,
\]

\[
R^2=1-\frac{SSE}{SST}=0.829580.
\]

Un aumento de 10 horas de coaching tiene ganancia ajustada $4.059355$
unidades por hora en esta nube. Esa aritmética no es un efecto de
tratamiento aleatorizado.

## Conceptos erróneos comunes

- La recta de mínimos cuadrados es el minimizador único de huecos
  verticales al cuadrado, no una prueba de causa.
- Una $R^2$ cercana a 1 puede salir aún de una muestra observacional
  confundida.
- Coincidir con scipy `linregress` es un chequeo de las ecuaciones
  normales, no un segundo conjunto de datos.
- El centro de correo sintético ilustra la aritmética de regresión. No es
  una afirmación sobre ningún almacén real.

## Estructura del paquete

```text
L47_Regresion_Lineal_Simple/
|-- README.md
|-- src/
|   |-- regresion_simple_01_dispersion.py
|   |-- regresion_simple_02_minimos_cuadrados.py
|   `-- regresion_simple_03_limite_r_cuadrada.py
|-- figuras/
|   |-- regresion_simple_01_dispersion.png
|   |-- regresion_simple_02_minimos_cuadrados.png
|   `-- regresion_simple_03_limite_r_cuadrada.png
|-- notebooks/
|   `-- leccion_47_regresion_lineal_simple.ipynb
`-- diapositivas/
    |-- leccion_47.tex
    `-- leccion_47.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L47_Regresion_Lineal_Simple/src/regresion_simple_01_dispersion.py
uv run es/L47_Regresion_Lineal_Simple/src/regresion_simple_02_minimos_cuadrados.py
uv run es/L47_Regresion_Lineal_Simple/src/regresion_simple_03_limite_r_cuadrada.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L47_Regresion_Lineal_Simple/notebooks/leccion_47_regresion_lineal_simple.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_47.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_47.tex
```

## Atribución OpenStax

Las ecuaciones lineales, la recta de regresión de mínimos cuadrados y
$R^2$ siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Secciones
[13.3](https://openstax.org/books/introductory-business-statistics-2e/pages/13-3-linear-equations)
y
[13.4](https://openstax.org/books/introductory-business-statistics-2e/pages/13-4-the-regression-equation).
OpenStax publica este texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

