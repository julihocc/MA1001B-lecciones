# Lección 26 - Estimación puntual: insesgadez, eficiencia, consistencia

Esta microlección de 50 minutos usa un reloj de costos sintético modelado
como $\mathrm{Normal}(\mu=100,\sigma=15)$. Se comparan dos estimadores de
$\mu$: la media muestral $\bar x$ y el estimador de una observación $X_1$.
Ambos son insesgados. $\bar x$ es más eficiente, y subir $n$ de 20 a 200
reduce su dispersión (consistencia). El paso final muestra que la
insesgadez no implica varianza pequeña en una muestra pequeña.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  introducción del Capítulo 8 (estimaciones puntuales y propiedades de
  estimadores). Práctica complementaria: *Introductory Statistics 2e*,
  introducción del Capítulo 8.
- **Prerrequisitos:** Distribuciones muestrales de $\bar x$ y $\hat p$ de
  las Lecciones 23 a 25.
- **Aviso de datos:** Cada costo y cada media muestral es sintético. Los
  scripts no contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Definir la insesgadez como $E[\hat\theta]=\theta$.
2. Comparar la eficiencia mediante $\mathrm{Var}(\bar x)$ versus
   $\mathrm{Var}(X_1)$.
3. Reconocer la consistencia como la reducción de la dispersión cuando $n$
   crece.
4. Explicar por qué un estimador insesgado puede seguir siendo demasiado
   ruidoso con $n$ pequeño.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: estimar $\mu=100$ a partir de una muestra | Nombrar dos estimadores candidatos. |
| 06-16 | Insesgadez como ``correcto en promedio'' | Predecir ambas medias cerca de 100. |
| 16-24 | Ejecutar el Paso 1 | Leer sesgos $-0.042690$ y $-0.083926$. |
| 24-34 | Eficiencia: gana la menor varianza | Calcular $225/20=11.25$. |
| 34-42 | Ejecutar el Paso 2 | Contrastar SD $3.352961$ con $1.052019$. |
| 42-48 | Ejecutar el Paso 3 en $n=5$ | Obtener $P(|\bar x-\mu|>10)=0.137875$. |
| 48-50 | Verificación de conceptos y transición a la Lección 27 | Nombrar un intervalo $z$ alrededor de $\bar x$. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma
población de costos $N(100,15)$ con `SEED = 42` y añade el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `point_estimation_01_unbiasedness.py` | Insesgadez de $\bar x$ y $X_1$ | Media de $\bar x=99.957310$ (sesgo $-0.042690$); media de $X_1=99.916074$ (sesgo $-0.083926$). |
| 2 | `point_estimation_02_efficiency_consistency.py` | Eficiencia y consistencia | $\mathrm{Var}(X_1)=227.612313$ versus $\mathrm{Var}(\bar x_{20})=11.242349$, razón $20.245975$. SD de $\bar x_{200}=1.052019$ versus fórmula $1.060660$. |
| 3 | `point_estimation_03_small_sample_variance.py` | Ruido de muestra pequeña | $n=5$: media $100.066209$, SD $6.737762$, $P(|\bar x-\mu|>10)=0.137875$. $n=200$: el mismo evento tiene probabilidad $0.000000$. |

El resultado del Paso 3 es un límite. Ser insesgado no es lo mismo que ser
preciso en una muestra pequeña. La Lección 27 envuelve $\bar x$ en un
intervalo de confianza $z$ cuando $\sigma$ es conocida.

La [libreta estudiantil](notebooks/leccion_26_estimacion_puntual_propiedades.ipynb)
ejecutada es una guía de estudio autocontenida y compatible con Google Colab.
Reconstruye los tres pasos en un estado acumulativo en memoria, embebe tres
figuras e incluye prácticas editables, respuestas plegables y aserciones para
los valores canónicos. También se ejecutó desde un directorio temporal vacío y
se renderizó a HTML y Markdown sin leer archivos del repositorio.

## Población sintética de costos

Población: $X\sim N(100,15^2)$. Estimadores:

\[
E[\bar x]=\mu,\qquad \mathrm{Var}(\bar x)=\frac{15^2}{n},
\qquad
E[X_1]=\mu,\qquad \mathrm{Var}(X_1)=225.
\]

En $n=20$, $\mathrm{Var}(\bar x)=11.25$, de modo que $\bar x$ es unas 20
veces más eficiente que $X_1$. En $n=5$, $\bar x$ sigue siendo insesgado
pero $P(|\bar x-100|>10)=0.137875$. En $n=200$ ese evento no se observa en
8{,}000 replicaciones con semilla 42.

## Conceptos erróneos comunes

- La insesgadez es una propiedad de promedio a largo plazo. No es una
  garantía para una sola muestra.
- $X_1$ es insesgado y sigue siendo un mal estimador porque su varianza es
  $\sigma^2$, no $\sigma^2/n$.
- La eficiencia compara varianzas de estimadores insesgados en el mismo
  $n$.
- La consistencia trata de $n\to\infty$, no de una sola extracción $n=5$.
- Una probabilidad del $13.8\%$ de errar $\mu$ por más de 10 puede ser
  inaceptable aunque el estimador sea insesgado.
- Los costos sintéticos ilustran propiedades de estimadores. No son una
  afirmación sobre ningún proceso real de costos.

## Estructura del paquete

```text
L26_Estimacion_Puntual_Propiedades/
|-- README.md
|-- src/
|   |-- point_estimation_01_unbiasedness.py
|   |-- point_estimation_02_efficiency_consistency.py
|   `-- point_estimation_03_small_sample_variance.py
|-- figuras/
|   |-- point_estimation_01_unbiasedness.png
|   |-- point_estimation_02_efficiency_consistency.png
|   `-- point_estimation_03_small_sample_variance.png
|-- notebooks/
|   `-- leccion_26_estimacion_puntual_propiedades.ipynb
`-- diapositivas/
    |-- leccion_26.tex
    `-- leccion_26.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L26_Estimacion_Puntual_Propiedades/src/point_estimation_01_unbiasedness.py
uv run es/L26_Estimacion_Puntual_Propiedades/src/point_estimation_02_efficiency_consistency.py
uv run es/L26_Estimacion_Puntual_Propiedades/src/point_estimation_03_small_sample_variance.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L26_Estimacion_Puntual_Propiedades/notebooks/leccion_26_estimacion_puntual_propiedades.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_26.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_26.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

Las estimaciones puntuales, la insesgadez y el papel del tamaño de muestra
en reducir la dispersión del estimador siguen a Alexander Holmes, Barbara
Illowsky y Susan Dean, *Introductory Business Statistics 2e*, Capítulo 8,
[Introduction](https://openstax.org/books/introductory-business-statistics-2e/pages/8-introduction).
La configuración complementaria de estimación está en *Introductory
Statistics 2e*, Capítulo 8,
[Introduction](https://openstax.org/books/introductory-statistics-2e/pages/8-introduction).
El límite de varianza de muestra pequeña prepara los intervalos de
confianza $z$ para una media en la Lección 27. OpenStax publica estos
textos bajo la licencia Creative Commons Attribution-NonCommercial-ShareAlike.
El conjunto sintético, el código y las figuras de este paquete son
materiales originales del curso.

