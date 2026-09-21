# Lección 15 - Aplicaciones binomiales y riesgo de negocio

Esta microlección de 50 minutos compara dos políticas de inspección
completamente sintéticas que comparten la misma media de defectuosos: la
Política A usa $n=50$ y $p=0.04$, mientras que la Política B usa $n=20$ y
$p=0.10$. Ambas tienen $np=2$. Los estudiantes calculan $P(X\ge 3)$ y luego
examinan $P(X=0)$ y la cola lejana $P(X\ge 8)$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Sección 4.2.
- **Prerrequisitos:** Ensayos de Bernoulli y el modelo binomial de la Lección 14.
- **Aviso de datos:** Cada política, ensayo y conteo de defectos es sintético.
  Los scripts no contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar dos políticas binomiales que comparten la misma media $np$.
2. Calcular $P(X\ge 3)$ para cada política.
3. Comparar $P(X=0)$ y la cola lejana $P(X\ge 8)$.
4. Explicar por qué igualar $np$ no iguala el riesgo de cola.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: dos políticas, una media | Confirmar $np=2$ para ambas. |
| 06-16 | Varianza $np(1-p)$ | Obtener $1.920000$ frente a $1.800000$. |
| 16-24 | Ejecutar el Paso 1 | Leer $n$, $p$ y las medias coincidentes. |
| 24-34 | $P(X\ge 3)$ | Predecir si las colas coinciden. |
| 34-42 | Ejecutar el Paso 2 | Ver $P(X\ge 3)\approx 0.323$ pero razón $P(X\ge 8)$ de $1.88$. |
| 42-48 | Ejecutar el Paso 3 con superposición | Señalar la región de cola lejana $x\ge 8$. |
| 48-50 | Verificación de conceptos y transición a la Lección 16 | Nombrar el muestreo sin reemplazo. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye las mismas dos
políticas con `SEED = 42` reservada y agrega el siguiente concepto sin importar
otro script de la lección. Estos valores provienen de dos ejecuciones
coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `riesgo_binomial_01_dos_politicas.py` | Dos políticas, misma media | A: $n=50$, $p=0.040000$, $np=2.000000$, varianza $1.920000$. B: $n=20$, $p=0.100000$, $np=2.000000$, varianza $1.800000$. |
| 2 | `riesgo_binomial_02_probabilidades_cola.py` | $P(X=0)$, $P(X\ge 3)$, $P(X\ge 8)$ | $P(X\ge 3)$: $0.323286$ frente a $0.323073$. $P(X=0)$: $0.129886$ frente a $0.121577$. $P(X\ge 8)$: $0.000781$ frente a $0.000416$. |
| 3 | `riesgo_binomial_03_misma_media_colas_distintas.py` | Superposición de cola lejana | Razón de cola lejana $A/B=1.880028$. La misma media oculta una cola lejana más pesada para la Política A. |

El resultado del Paso 3 es un límite: igualar $np$ no es igualar el riesgo.
$P(X\ge 3)$ resulta casi idéntica, pero $P(X\ge 8)$ no. La Lección 16 sustituye
ensayos independientes por muestreo sin reemplazo.

## Libreta de estudio

La libreta autocontenida
[`notebooks/leccion_15_aplicaciones_binomial_riesgo.ipynb`](notebooks/leccion_15_aplicaciones_binomial_riesgo.ipynb)
convierte los tres hitos de los scripts en un solo recorrido acumulativo para
el estudiante. Reconstruye en memoria las dos políticas sintéticas, embebe tres
termina con aserciones para las políticas, probabilidades, FMP y prácticas
exactas. No lee archivos del repositorio ni requiere acceso a la red.

La libreta se ejecutó tanto en su paquete como después de copiarla por sí sola
a un directorio temporal vacío. Se inspeccionaron sus renderizados guardados en
HTML y Markdown y sus tres figuras extraídas.

## Conceptos erróneos comunes

- Medias iguales no implican distribuciones iguales.
- $P(X\ge 3)$ puede coincidir aunque una cola más lejana no coincida.
- Un $n$ más grande con $p$ más pequeño puede concentrar más masa en conteos extremos.
- Las políticas sintéticas ilustran el riesgo de cola. No afirman nada sobre
  ningún plan de inspección real.

## Estructura del paquete

```text
L15_Aplicaciones_Binomial_Riesgo/
|-- README.md
|-- src/
|   |-- riesgo_binomial_01_dos_politicas.py
|   |-- riesgo_binomial_02_probabilidades_cola.py
|   `-- riesgo_binomial_03_misma_media_colas_distintas.py
|-- figuras/
|   |-- riesgo_binomial_01_dos_politicas.png
|   |-- riesgo_binomial_02_probabilidades_cola.png
|   `-- riesgo_binomial_03_misma_media_colas_distintas.png
|-- notebooks/
|   `-- leccion_15_aplicaciones_binomial_riesgo.ipynb
`-- diapositivas/
    |-- leccion_15.tex
    `-- leccion_15.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L15_Aplicaciones_Binomial_Riesgo/src/riesgo_binomial_01_dos_politicas.py
uv run es/L15_Aplicaciones_Binomial_Riesgo/src/riesgo_binomial_02_probabilidades_cola.py
uv run es/L15_Aplicaciones_Binomial_Riesgo/src/riesgo_binomial_03_misma_media_colas_distintas.py
```

Ejecutar y guardar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace es/L15_Aplicaciones_Binomial_Riesgo/notebooks/leccion_15_aplicaciones_binomial_riesgo.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_15.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_15.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

Las aplicaciones binomiales siguen a Alexander Holmes, Barbara Illowsky y
Susan Dean, *Introductory Business Statistics 2e*, Sección
[4.2](https://openstax.org/books/introductory-business-statistics-2e/pages/4-2-binomial-distribution).
OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. Las políticas sintéticas, el código y
las figuras de este paquete son materiales originales del curso.

