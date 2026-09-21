# Lección 16 - Distribución hipergeométrica: muestreo sin reemplazo

Esta microlección de 50 minutos inspecciona un lote completamente sintético de
$N=80$ unidades que contiene $K=6$ defectuosos. Se extraen $n=10$ unidades sin
reemplazo, de modo que $X$ es hipergeométrica. Los estudiantes calculan
$P(X=0)$ y $E[X]=nK/N$, y luego comparan la aproximación binomial con
$p=K/N$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Sección 4.1.
- **Prerrequisitos:** Ensayos binomiales de las Lecciones 14--15.
- **Aviso de datos:** Cada lote, conteo de defectuosos y extracción es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Identificar $N$, $K$ y $n$ en una extracción sin reemplazo.
2. Calcular $P(X=0)$ a partir de la FMP hipergeométrica.
3. Calcular $E[X]=nK/N$.
4. Explicar por qué la binomial sobreestima $P(X=0)$ cuando $n/N$ no es pequeña.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: sin reemplazo | Nombrar $N=80$, $K=6$, $n=10$. |
| 06-16 | Fracción de muestreo $n/N$ | Obtener $0.125$, no pequeña. |
| 16-24 | Ejecutar el Paso 1 | Leer $P(X=0)=0.436326$. |
| 24-34 | Media $nK/N$ | Calcular $10\times 6/80=0.75$. |
| 34-42 | Ejecutar el Paso 2 | Confirmar $E[X]=0.750000$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar binomial $P(X=0)=0.458582$. |
| 48-50 | Verificación de conceptos y transición a la Lección 17 | Nombrar eventos raros y Poisson. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo lote
sintético con `SEED = 42` reservada y agrega el siguiente concepto sin importar
otro script de la lección. Estos valores provienen de dos ejecuciones
coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `hipergeometrica_01_sin_reemplazo.py` | Hipergeométrica $P(X=0)$ | $N=80$, $K=6$, $n=10$, $n/N=0.125000$, $P(X=0)=0.436326$. |
| 2 | `hipergeometrica_02_esperanza.py` | $E[X]=nK/N$ | $E[X]=0.750000$, coincidente con \texttt{scipy.stats.hypergeom.mean}. |
| 3 | `hipergeometrica_03_aproximacion_binomial.py` | Binomial con $p=K/N$ | $p=0.075000$; binomial $P(X=0)=0.458582$; sobreestimación $0.022257$. |

El resultado del Paso 3 es un límite: la binomial sobreestima $P(X=0)$ cuando
$n/N$ no es pequeña, porque extraer sin reemplazo agota defectuosos. La
Lección 17 modela eventos raros con una tasa de Poisson.

## Libreta de estudio

La libreta autocontenida
[`notebooks/leccion_16_hipergeometrica_sin_reemplazo.ipynb`](notebooks/leccion_16_hipergeometrica_sin_reemplazo.ipynb)
convierte los tres hitos de los scripts en un solo recorrido acumulativo para
el estudiante. Conserva en memoria un lote finito sintético, embebe tres
termina con aserciones para la FMP exacta, los momentos, el error de
aproximación y la comparación con una extracción menor. No lee archivos del
repositorio ni requiere acceso a la red.

La libreta se ejecutó tanto en su paquete como después de copiarla por sí sola
a un directorio temporal vacío. Se inspeccionaron sus renderizados guardados en
HTML y Markdown y sus tres figuras extraídas.

## Conceptos erróneos comunes

- Los ensayos hipergeométricos no son independientes: cada extracción cambia
  el lote restante.
- $E[X]=nK/N$ puede coincidir con una media binomial aunque $P(X=0)$ no coincida.
- La aproximación binomial necesita una fracción de muestreo $n/N$ pequeña.
- El lote sintético ilustra el muestreo sin reemplazo. No afirma nada sobre
  ningún almacén real.

## Estructura del paquete

```text
L16_Hipergeometrica_Sin_Reemplazo/
|-- README.md
|-- src/
|   |-- hipergeometrica_01_sin_reemplazo.py
|   |-- hipergeometrica_02_esperanza.py
|   `-- hipergeometrica_03_aproximacion_binomial.py
|-- figuras/
|   |-- hipergeometrica_01_sin_reemplazo.png
|   |-- hipergeometrica_02_esperanza.png
|   `-- hipergeometrica_03_aproximacion_binomial.png
|-- notebooks/
|   `-- leccion_16_hipergeometrica_sin_reemplazo.ipynb
`-- diapositivas/
    |-- leccion_16.tex
    `-- leccion_16.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L16_Hipergeometrica_Sin_Reemplazo/src/hipergeometrica_01_sin_reemplazo.py
uv run es/L16_Hipergeometrica_Sin_Reemplazo/src/hipergeometrica_02_esperanza.py
uv run es/L16_Hipergeometrica_Sin_Reemplazo/src/hipergeometrica_03_aproximacion_binomial.py
```

Ejecutar y guardar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace es/L16_Hipergeometrica_Sin_Reemplazo/notebooks/leccion_16_hipergeometrica_sin_reemplazo.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_16.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_16.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La distribución hipergeométrica sigue a Alexander Holmes, Barbara Illowsky y
Susan Dean, *Introductory Business Statistics 2e*, Sección
[4.1](https://openstax.org/books/introductory-business-statistics-2e/pages/4-1-hypergeometric-distribution).
OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El lote sintético, el código y las
figuras de este paquete son materiales originales del curso.

