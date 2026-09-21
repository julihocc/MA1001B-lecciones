# Lección 20 - Distribución uniforme continua y Monte Carlo

Esta microlección de 50 minutos usa un reloj de procesamiento de tickets
completamente sintético modelado como $\mathrm{Uniforme}(8,20)$ minutos. La
cola exacta $P(X>16)$ iguala longitud sobre $12$. Un Monte Carlo con semilla
42 de $100{,}000$ extracciones recupera esa cola. El paso final muestra que un
modelo plano falla cuando la densidad se acumula en un extremo.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 5, Sección 5.2 (la distribución uniforme). Práctica complementaria:
  *Introductory Statistics 2e*, Sección 5.2.
- **Prerrequisitos:** Densidad continua y probabilidad de intervalo de la
  Lección 19.
- **Aviso de datos:** Cada tiempo de procesamiento, densidad y extracción
  Monte Carlo es sintético. Los scripts no contienen datos reales de empresas,
  clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Escribir la densidad plana $f(x)=1/(b-a)$ en un intervalo cerrado.
2. Calcular $P(X>c)$ como longitud restante dividida entre $b-a$.
3. Comprobar una probabilidad uniforme exacta con una muestra Monte Carlo sembrada.
4. Explicar por qué una densidad acumulada hace que la cola uniforme sea el número equivocado.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: un reloj plano en $[8,20]$ | Bosquejar un rectángulo de altura $1/12$. |
| 06-16 | Razón de longitudes como probabilidad | Calcular $(20-16)/12=1/3$. |
| 16-24 | Ejecutar el Paso 1 | Leer altura $0.083333$ y $P(X>16)=0.333333$. |
| 24-34 | Idea Monte Carlo: simular, luego contar | Predecir una cola cercana a $1/3$. |
| 34-42 | Ejecutar el Paso 2 | Obtener cola Monte Carlo $0.333290$. |
| 42-48 | Ejecutar el Paso 3 y acumular la densidad | Contrastar $0.333333$ con $0.555556$. |
| 48-50 | Verificación de conceptos y transición a la Lección 21 | Nombrar $z$ como un reloj estandarizado. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo modelo
$\mathrm{Uniforme}(8,20)$ con `SEED = 42` y agrega el siguiente concepto sin
importar otro script de la lección. Estos valores provienen de dos ejecuciones
coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `uniforme_mc_01_uniforme_exacta.py` | Densidad plana, razón de longitudes, cola exacta | Altura $1/12=0.083333$, media $=14.000000$, $P(X>16)=0.333333$. |
| 2 | `uniforme_mc_02_monte_carlo.py` | Monte Carlo con semilla 42 de $100{,}000$ extracciones | Cola simulada $0.333290$, error absoluto $0.000043$, media simulada $14.007499$. |
| 3 | `uniforme_mc_03_limite_densidad_acumulada.py` | Acumulación triangular derecha en el mismo soporte | $P(X>16)$ acumulada $=0.555556$, media acumulada $=16.000000$, altura acumulada en $20$ es $0.166667$. |

El resultado del Paso 3 es un límite. Uniforme es el modelo correcto solo
cuando la densidad es realmente plana. La Lección 21 estandariza un reloj en
forma de campana con $z=(x-\mu)/\sigma$.

## Modelo sintético de tiempo de procesamiento

Soporte: $X\sim\mathrm{Uniforme}(8,20)$ minutos. Altura de densidad:

\[
f(x)=\frac{1}{20-8}=\frac{1}{12}=0.083333,\qquad 8\le x\le 20.
\]

Media $(a+b)/2=14$. Cola por longitud:

\[
P(X>16)=\frac{20-16}{12}=\frac{1}{3}=0.333333.
\]

Una muestra de $100{,}000$ extracciones con semilla 42 estima esa cola como
$0.333290$. Si el reloj verdadero es triangular derecho y se acumula en $20$
minutos, el mismo corte tiene probabilidad $0.555556$, no $1/3$.

## Libreta de estudio estudiantil

La libreta ejecutada
[`notebooks/leccion_20_uniforme_monte_carlo.ipynb`](notebooks/leccion_20_uniforme_monte_carlo.ipynb)
es una guía de estudio autocontenida y compatible con Google Colab. Construye
el modelo uniforme plano en memoria, reproduce la muestra Monte Carlo con
semilla 42 y compara después el rectángulo con una densidad triangular derecha
sobre el mismo soporte. Incluye tres figuras embebidas, prácticas editables con
respuestas desplegables y aserciones ejecutables para los valores verificados
del paquete, una práctica de 1,000 sorteos y comparaciones de probabilidad del
lado izquierdo.

La libreta se ejecutó tanto en su ubicación como siendo el único artefacto de
la lección en un directorio temporal vacío. Sus renders HTML y Markdown y sus
tres figuras se inspeccionaron después de la ejecución.

## Conceptos erróneos comunes

- Una densidad uniforme es plana. No es “cualquier forma en un intervalo acotado”.
- $P(X>16)$ es longitud restante sobre $b-a$, no una altura de densidad.
- Monte Carlo recupera la cola exacta; no sustituye la fórmula.
- Un error de simulación cercano como $0.000043$ es esperado con $100{,}000$
  extracciones. No es evidencia de que el valor exacto esté mal.
- Si los tickets se agrupan cerca de un extremo, la cola uniforme es el número equivocado.
- El reloj sintético ilustra la aritmética uniforme. No afirma nada sobre
  ningún escritorio de tickets real.

## Estructura del paquete

```text
L20_Uniforme_Monte_Carlo/
|-- README.md
|-- src/
|   |-- uniforme_mc_01_uniforme_exacta.py
|   |-- uniforme_mc_02_monte_carlo.py
|   `-- uniforme_mc_03_limite_densidad_acumulada.py
|-- figuras/
|   |-- uniforme_mc_01_uniforme_exacta.png
|   |-- uniforme_mc_02_monte_carlo.png
|   `-- uniforme_mc_03_limite_densidad_acumulada.png
|-- notebooks/
|   `-- leccion_20_uniforme_monte_carlo.ipynb
`-- diapositivas/
    |-- leccion_20.tex
    `-- leccion_20.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L20_Uniforme_Monte_Carlo/src/uniforme_mc_01_uniforme_exacta.py
uv run es/L20_Uniforme_Monte_Carlo/src/uniforme_mc_02_monte_carlo.py
uv run es/L20_Uniforme_Monte_Carlo/src/uniforme_mc_03_limite_densidad_acumulada.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L20_Uniforme_Monte_Carlo/notebooks/leccion_20_uniforme_monte_carlo.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_20.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_20.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La densidad uniforme continua, la probabilidad por razón de longitudes y la
media $(a+b)/2$ siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Capítulo 5, Sección
[5.2](https://openstax.org/books/introductory-business-statistics-2e/pages/5-2-the-uniform-distribution).
La práctica uniforme complementaria está en *Introductory Statistics 2e*,
Sección
[5.2](https://openstax.org/books/introductory-statistics-2e/pages/5-2-the-uniform-distribution).
El límite de densidad acumulada prepara la necesidad de otras familias
continuas, incluido el modelo normal de la Lección 21. OpenStax publica estos
textos bajo la licencia Creative Commons Attribution-NonCommercial-ShareAlike.
El conjunto sintético, el código y las figuras de este paquete son materiales
originales del curso.

