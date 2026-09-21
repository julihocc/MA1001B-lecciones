# Lección 13 - Variables aleatorias discretas: FMP, FDA, esperanza, varianza

Esta microlección de 50 minutos especifica un conteo sintético de defectos
$X$ en $\{0,1,2,3\}$ con masas $0.50$, $0.30$, $0.15$ y $0.05$. Los
estudiantes grafican la FMP, la acumulan en una FDA y luego calculan $E[X]$
y $\mathrm{Var}(X)$ a partir de momentos. El límite es que $E[X^2]$ no es
$(E[X])^2$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Statistics 2e*, Secciones
  4.1--4.2. *Introductory Business Statistics 2e* Capítulo 4 avanza rápido a
  familias nombradas, de modo que el lenguaje general de FMP/FDA/momentos se
  toma de IS 2e.
- **Prerrequisitos:** Espacios muestrales y reglas de probabilidad de las
  Lecciones 05--10.
- **Aviso de datos:** Cada conteo de defectos y masa de probabilidad es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar las dos condiciones de una FMP: masas no negativas que suman 1.
2. Construir $F(x)=P(X\le x)$ al acumular la FMP.
3. Calcular $E[X]=\sum x\,P(X=x)$ y $E[X^2]=\sum x^2 P(X=x)$.
4. Obtener $\mathrm{Var}(X)=E[X^2]-(E[X])^2$ y rechazar $E[X^2]=(E[X])^2$.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: $X$ es un conteo de defectos | Listar los cuatro valores posibles. |
| 06-16 | Condiciones de la FMP | Comprobar $0.50+0.30+0.15+0.05=1$. |
| 16-24 | Ejecutar el Paso 1 | Leer las cuatro masas de la gráfica de tallos. |
| 24-34 | Acumular hacia una FDA | Calcular $F(1)=0.80$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $P(1<X\le 3)=0.20$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar $E[X^2]=1.350000$ con $(E[X])^2=0.562500$. |
| 48-50 | Verificación de conceptos y entrega a la Lección 14 | Nombrar el modelo Bernoulli/binomial. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma FMP
sintética con `SEED = 42` reservada y agrega el siguiente concepto sin
importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `va_discreta_01_fmp.py` | Soporte y FMP | Masas $0.500000$, $0.300000$, $0.150000$, $0.050000$; suma $=1.000000$. |
| 2 | `va_discreta_02_fda.py` | FDA y probabilidad de intervalo | $F(0)=0.500000$, $F(1)=0.800000$, $F(2)=0.950000$, $F(3)=1.000000$; $P(1<X\le 3)=0.200000$. |
| 3 | `va_discreta_03_esperanza_varianza.py` | $E[X]$, $E[X^2]$, varianza | $E[X]=0.750000$, $(E[X])^2=0.562500$, $E[X^2]=1.350000$, $\mathrm{Var}(X)=0.787500$. |

El resultado del Paso 3 es un límite: elevar al cuadrado la media no es el
segundo momento. La Lección 14 especializa este lenguaje discreto a ensayos
de Bernoulli y al modelo binomial.

## Distribución sintética del conteo de defectos

\[
P(X=x)=\begin{cases}
0.50 & x=0,\\
0.30 & x=1,\\
0.15 & x=2,\\
0.05 & x=3,\\
0 & \text{en otro caso.}
\end{cases}
\]

\[
E[X]=0\cdot0.50+1\cdot0.30+2\cdot0.15+3\cdot0.05=0.75,
\]
\[
E[X^2]=0+1\cdot0.30+4\cdot0.15+9\cdot0.05=1.35,
\]
\[
\mathrm{Var}(X)=1.35-0.75^2=0.7875.
\]

## Libreta de estudio

La guía ejecutada y autocontenida está en
[`notebooks/leccion_13_variables_aleatorias_discretas.ipynb`](notebooks/leccion_13_variables_aleatorias_discretas.ipynb).
Mantiene una sola FMP en memoria a través de los pasos de FMP, FDA y momentos,
plegables y aserciones para las cifras canónicas. La libreta se ejecutó tanto
en el paquete como desde un directorio temporal vacío; se inspeccionaron sus
renderizados HTML y Markdown y sus tres figuras.

## Conceptos erróneos comunes

- Una FMP es una lista de masas puntuales, no una densidad en un intervalo.
- $F(x)$ salta en los puntos de soporte; es una función escalón.
- $E[X]$ es una suma ponderada, no el valor más probable (aquí la moda es
  $0$).
- $E[X^2]$ no es $(E[X])^2$. La diferencia es la varianza.
- La FMP sintética ilustra aritmética discreta. No es una afirmación sobre
  ningún proceso real de inspección.

## Estructura del paquete

```text
L13_Variables_Aleatorias_Discretas/
|-- README.md
|-- notebooks/
|   `-- leccion_13_variables_aleatorias_discretas.ipynb
|-- src/
|   |-- va_discreta_01_fmp.py
|   |-- va_discreta_02_fda.py
|   `-- va_discreta_03_esperanza_varianza.py
|-- figuras/
|   |-- va_discreta_01_fmp.png
|   |-- va_discreta_02_fda.png
|   `-- va_discreta_03_esperanza_varianza.png
`-- diapositivas/
    |-- leccion_13.tex
    `-- leccion_13.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L13_Variables_Aleatorias_Discretas/src/va_discreta_01_fmp.py
uv run es/L13_Variables_Aleatorias_Discretas/src/va_discreta_02_fda.py
uv run es/L13_Variables_Aleatorias_Discretas/src/va_discreta_03_esperanza_varianza.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L13_Variables_Aleatorias_Discretas/notebooks/leccion_13_variables_aleatorias_discretas.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_13.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_13.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de

## Atribución OpenStax

La FMP, la FDA, el valor esperado y la desviación estándar de una variable
aleatoria discreta siguen a Barbara Illowsky y Susan Dean, *Introductory
Statistics 2e*, Secciones
[4.1](https://openstax.org/books/introductory-statistics-2e/pages/4-1-probability-distribution-function-pdf-for-a-discrete-random-variable)
y
[4.2](https://openstax.org/books/introductory-statistics-2e/pages/4-2-mean-or-expected-value-and-standard-deviation).
Las familias nombradas en *Introductory Business Statistics 2e* comienzan en
el Capítulo
[4](https://openstax.org/books/introductory-business-statistics-2e/pages/4-introduction).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. La distribución sintética, el código y
las figuras de este paquete son materiales originales del curso.

