# Lección 18 - Tiempos de espera geométricos y binomiales negativos

Esta microlección de 50 minutos espera defectuosos en una auditoría
completamente sintética. Cada ensayo independiente tiene probabilidad de
éxito $p=0.12$. Los estudiantes calculan $P(X=1)$ y $E[X]=1/p$ para el tiempo
de espera geométrico, y luego esperan $r=3$ éxitos en el modelo binomial
negativo. El límite es la fatiga: si $p$ declina con el número de ensayo, los
ensayos ya no son independientes.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Sección 4.3.
- **Prerrequisitos:** Ensayos de Bernoulli de la Lección 14.
- **Aviso de datos:** Cada ensayo y tiempo de espera es sintético. Los scripts
  no contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Definir $X$ como el número de ensayo del primer éxito y calcular $P(X=1)=p$.
2. Calcular $E[X]=1/p$ para el modelo geométrico.
3. Extender la espera a $r=3$ éxitos con $E[X]=r/p$.
4. Explicar por qué un $p$ declinante por fatiga hace que la espera media exceda $1/p$.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: esperar el primer defectuoso | Nombrar $p=0.12$. |
| 06-16 | Geométrica $P(X=1)=p$ | Confirmar $0.120000$. |
| 16-24 | Ejecutar el Paso 1 | Leer $E[X]=8.333333$. |
| 24-34 | Binomial negativa $r=3$ | Calcular $r/p=25$. |
| 34-42 | Ejecutar el Paso 2 | Confirmar $E[X]=25.000000$ y $P(X=3)=0.001728$. |
| 42-48 | Ejecutar el Paso 3 con fatiga | Contrastar $8.333333$ con $17.162800$ simulado. |
| 48-50 | Verificación de conceptos | Nombrar independencia y $p$ constante. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma
probabilidad de éxito con `SEED = 42` y agrega el siguiente concepto sin
importar otro script de la lección. Estos valores provienen de dos ejecuciones
coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `tiempos_espera_01_geometrica.py` | Tiempo de espera geométrico | $P(X=1)=0.120000$, $P(X\le 5)=0.472268$, $E[X]=8.333333$, $\mathrm{Var}(X)=61.111111$. |
| 2 | `tiempos_espera_02_binomial_negativa.py` | Ensayos hasta $r=3$ éxitos | $E[X]=25.000000$, $\mathrm{Var}(X)=183.333333$, $P(X=3)=p^3=0.001728$. |
| 3 | `tiempos_espera_03_dependencia_fatiga.py` | $p$ declinante | $p$ en el ensayo $10$ es $0.091228$; la media con semilla 42 censurada en 400 ensayos es $17.162800$, con 165 de 10,000 esperas en el límite. |

Aquí $X$ cuenta ensayos hasta el primer éxito (geométrica) o hasta el
$r$-ésimo éxito (binomial negativa), coincidiendo con OpenStax. El
\texttt{nbinom} de scipy cuenta fallos antes de $r$ éxitos; los scripts
convierten eso a un conteo de ensayos.

El resultado del Paso 3 es un límite: los ensayos no son independientes si la
fatiga cambia $p$. Como $p_t=0.12(0.97)^{t-1}$ decrece geométricamente, el
modelo asigna probabilidad positiva a nunca observar un éxito; la probabilidad
límite es aproximadamente $0.016100$. Por tanto, $17.162800$ es un resumen de
simulación censurado, no una esperanza finita sin censura.

## Libreta de estudio estudiantil

La libreta ejecutada
[`notebooks/leccion_18_geometrica_binomial_negativa.ipynb`](notebooks/leccion_18_geometrica_binomial_negativa.ipynb)
es una guía de estudio autocontenida y compatible con Google Colab. Reconstruye
las convenciones de conteo de ensayos de las distribuciones geométrica y
binomial negativa, y luego diagnostica el modelo de fatiga con $p$ decreciente
sin leer archivos del repositorio. Incluye tres figuras embebidas, prácticas
editables con respuestas desplegables y aserciones ejecutables para los valores
verificados anteriores, las 165 esperas censuradas y la probabilidad límite de
no éxito $0.016100$.

La libreta se ejecutó tanto en su ubicación como siendo el único artefacto de
la lección en un directorio temporal vacío. Sus renders HTML y Markdown y sus
tres figuras se inspeccionaron después de la ejecución.

## Conceptos erróneos comunes

- La $X$ geométrica empieza en $1$, no en $0$, cuando $X$ es el ensayo del primer éxito.
- $E[X]=1/p$ es una espera media, no una probabilidad.
- La binomial negativa con $r=1$ es el modelo geométrico.
- El \texttt{nbinom} de scipy usa fallos, no ensayos, a menos que se convierta.
- La auditoría sintética ilustra tiempos de espera. No afirma nada sobre ningún
  proceso de inspección real.

## Estructura del paquete

```text
L18_Geometrica_Binomial_Negativa/
|-- README.md
|-- src/
|   |-- tiempos_espera_01_geometrica.py
|   |-- tiempos_espera_02_binomial_negativa.py
|   `-- tiempos_espera_03_dependencia_fatiga.py
|-- figuras/
|   |-- tiempos_espera_01_geometrica.png
|   |-- tiempos_espera_02_binomial_negativa.png
|   `-- tiempos_espera_03_dependencia_fatiga.png
|-- notebooks/
|   `-- leccion_18_geometrica_binomial_negativa.ipynb
`-- diapositivas/
    |-- leccion_18.tex
    `-- leccion_18.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L18_Geometrica_Binomial_Negativa/src/tiempos_espera_01_geometrica.py
uv run es/L18_Geometrica_Binomial_Negativa/src/tiempos_espera_02_binomial_negativa.py
uv run es/L18_Geometrica_Binomial_Negativa/src/tiempos_espera_03_dependencia_fatiga.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L18_Geometrica_Binomial_Negativa/notebooks/leccion_18_geometrica_binomial_negativa.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_18.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_18.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La distribución geométrica, y la interpretación de tiempo de espera usada aquí
para la binomial negativa, siguen a Alexander Holmes, Barbara Illowsky y Susan
Dean, *Introductory Business Statistics 2e*, Sección
[4.3](https://openstax.org/books/introductory-business-statistics-2e/pages/4-3-geometric-distribution).
OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. La auditoría sintética, el código y las
figuras de este paquete son materiales originales del curso.

