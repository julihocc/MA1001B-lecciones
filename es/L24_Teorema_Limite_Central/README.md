# Lección 24 - Teorema del límite central

Esta microlección de 50 minutos usa un reloj de retraso completamente
sintético modelado como una población exponencial con media $10$ minutos.
La población está sesgada a la derecha (asimetría $2$). Las medias
muestrales de tamaño $n=4$ siguen siendo asimétricas; las medias de tamaño
$n=40$ están más cerca de la normal. El paso final muestra que un $n$
pequeño más asimetría hace que la cola normal sea una mala aproximación.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 7, Secciones 7.1--7.2 (TLC para medias muestrales y uso del TLC).
  Práctica complementaria: *Introductory Statistics 2e*, Secciones 7.1--7.2.
- **Prerrequisitos:** Distribución muestral de $\bar x$ y
  $\mathrm{EE}=\sigma/\sqrt{n}$ de la Lección 23.
- **Aviso de datos:** Cada tiempo de retraso y cada media muestral es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Reconocer una población sesgada a la derecha que no es ella misma normal.
2. Comparar histogramas de $\bar x$ para $n=4$ y $n=40$.
3. Usar el enunciado del TLC: para $n$ grande, $\bar x$ es aproximadamente
   normal.
4. Explicar por qué una cola a dos EE es poco fiable cuando $n$ es pequeño
   y la asimetría es grande.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: retrasos, no una campana | Nombrar media $=$ sd $=10$ y asimetría $2$. |
| 06-16 | Ejecutar el Paso 1 | Leer mediana $6.931472$ versus media $10$. |
| 16-24 | ¿Cómo debería verse $\bar x$? | Predecir menos asimetría para $n$ mayor. |
| 24-34 | Ejecutar el Paso 2 | Contrastar asimetría $1.049897$ con $0.332572$. |
| 34-42 | Cola a dos EE sobre una media Gamma | Comparar exacta versus $N(\mu,\mathrm{EE})$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar $0.042380$ con $0.022750$ en $n=4$. |
| 48-50 | Verificación de conceptos y transición a la Lección 25 | Nombrar $\hat p$ como otro estadístico muestral. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma
población exponencial de retrasos con `SEED = 42` y añade el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `clt_01_skewed_population.py` | Población exponencial de retrasos | Media $=$ sd $=10.000000$, mediana $=6.931472$, asimetría $=2.000000$, $P(X>20)=0.135335$. |
| 2 | `clt_02_means_n4_n40.py` | 5{,}000 medias, $n=4$ vs $n=40$ | $n=4$: EE empírico $5.076401$, asimetría $1.049897$. $n=40$: EE empírico $1.574371$, asimetría $0.332572$. |
| 3 | `clt_03_small_n_skew_limit.py` | Cola Gamma exacta versus normal TLC | $n=4$: exacta $P(\bar x>20)=0.042380$ versus normal $0.022750$. $n=40$: exacta $0.030560$ versus normal $0.022750$. |

El resultado del Paso 3 es un límite. El TLC es una aproximación de muestra
grande, no una promesa en $n=4$ sobre un reloj de asimetría $2$. La Lección
25 aplica la misma lógica muestral a una proporción muestral $\hat p$.

## Libreta de estudio para estudiantes

La [libreta estudiantil](notebooks/leccion_24_teorema_limite_central.ipynb)
ejecutada es autocontenida y compatible con Google Colab. Reconstruye los tres
pasos de la lección en un único estado acumulativo en memoria, embebe tres
figuras e incluye prácticas editables, respuestas plegables y aserciones para
los valores canónicos. También fue ejecutada desde un directorio temporal
vacío y representada en HTML y Markdown sin leer archivos del repositorio.

## Población sintética de retrasos

$X\sim\mathrm{Exponencial}(\text{media}=10)$. Entonces $E[X]=\sigma=10$ y
asimetría $=2$. Para muestras iid,
\[
E[\bar x]=10,\qquad
\mathrm{EE}(\bar x)=\frac{10}{\sqrt{n}},
\]
y $\bar x$ es exactamente $\mathrm{Gamma}(\text{forma}=n,\text{escala}=10/n)$.
El TLC sustituye esa ley Gamma por $N(10,10/\sqrt{n})$. En $n=4$ la cola a
dos EE $P(\bar x>20)$ es $0.042380$, casi el doble del valor normal
$0.022750$.

## Conceptos erróneos comunes

- El TLC trata de $\bar x$, no de que las observaciones originales se
  vuelvan normales.
- $n=4$ no es ``grande'' en un reloj de retraso con asimetría $2$.
- Igualar medias y EE no hace que las colas coincidan.
- Una cola normal a dos EE de $0.022750$ puede ser aproximadamente la
  mitad de la cola verdadera.
- Un $n$ mayor reduce la asimetría de $\bar x$ a tasa $2/\sqrt{n}$ para
  esta familia exponencial.
- Los retrasos sintéticos ilustran el TLC. No son una afirmación sobre
  ninguna cola real.

## Estructura del paquete

```text
L24_Teorema_Limite_Central/
|-- README.md
|-- src/
|   |-- clt_01_skewed_population.py
|   |-- clt_02_means_n4_n40.py
|   `-- clt_03_small_n_skew_limit.py
|-- figuras/
|   |-- clt_01_skewed_population.png
|   |-- clt_02_means_n4_n40.png
|   `-- clt_03_small_n_skew_limit.png
|-- notebooks/
|   `-- leccion_24_teorema_limite_central.ipynb
`-- diapositivas/
    |-- leccion_24.tex
    `-- leccion_24.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L24_Teorema_Limite_Central/src/clt_01_skewed_population.py
uv run es/L24_Teorema_Limite_Central/src/clt_02_means_n4_n40.py
uv run es/L24_Teorema_Limite_Central/src/clt_03_small_n_skew_limit.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L24_Teorema_Limite_Central/notebooks/leccion_24_teorema_limite_central.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_24.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_24.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

El teorema del límite central para medias muestrales y la aproximación
normal de muestra grande siguen a Alexander Holmes, Barbara Illowsky y
Susan Dean, *Introductory Business Statistics 2e*, Capítulo 7, Secciones
[7.1](https://openstax.org/books/introductory-business-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar)
y
[7.2](https://openstax.org/books/introductory-business-statistics-2e/pages/7-2-using-the-central-limit-theorem).
La práctica complementaria del TLC está en *Introductory Statistics 2e*,
Secciones
[7.1](https://openstax.org/books/introductory-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar)
y
[7.2](https://openstax.org/books/introductory-statistics-2e/pages/7-2-using-the-central-limit-theorem).
El límite de $n$ pequeño prepara la distribución muestral de una
proporción en la Lección 25. OpenStax publica estos textos bajo la licencia
Creative Commons Attribution-NonCommercial-ShareAlike. El conjunto
sintético, el código y las figuras de este paquete son materiales originales
del curso.

