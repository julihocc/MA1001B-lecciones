# Lección 17 - Modelo de Poisson para eventos raros

Esta microlección de 50 minutos modela el número de eventos de parada
completamente sintéticos $X$ en un turno con tasa media $\lambda=3.2$. Los
estudiantes calculan $P(X=0)$ y $P(X\ge 6)$, simulan $10{,}000$ turnos con
semilla $42$ y luego sustituyen una tasa constante por una mezcla agrupada
cuya varianza excede $\lambda$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Sección 4.4.
- **Prerrequisitos:** FMP discretas de la Lección 13 y conteos binomiales de
  las Lecciones 14--15.
- **Aviso de datos:** Cada turno y conteo de eventos es sintético. Los scripts
  no contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar la media de Poisson $\lambda$ y la propiedad de media igual a varianza.
2. Calcular $P(X=0)$ y $P(X\ge 6)$ para $\lambda=3.2$.
3. Comparar esas probabilidades con una simulación de $10{,}000$ turnos con semilla $42$.
4. Explicar por qué los eventos agrupados producen sobredispersión: $\mathrm{Var}(X)>\lambda$.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: eventos raros por turno | Nombrar $\lambda=3.2$. |
| 06-16 | La media de Poisson iguala la varianza | Escribir $\mathrm{Var}(X)=\lambda$. |
| 16-24 | Ejecutar el Paso 1 | Leer $P(X=0)=0.040762$ y $P(X\ge 6)=0.105408$. |
| 24-34 | Simular $10{,}000$ turnos | Predecir la tasa empírica. |
| 34-42 | Ejecutar el Paso 2 | Comparar $0.040000$ y $0.109000$ con los valores exactos. |
| 42-48 | Ejecutar el Paso 3 con mezcla agrupada | Ver varianza simulada $6.811382>\lambda$. |
| 48-50 | Verificación de conceptos y transición a la Lección 18 | Nombrar tiempos de espera. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma tasa de
Poisson con `SEED = 42` y agrega el siguiente concepto sin importar otro
script de la lección. Estos valores provienen de dos ejecuciones coincidentes
en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `poisson_01_fmp.py` | FMP de Poisson y colas | $\lambda=3.200000$, $P(X=0)=0.040762$, $P(X\ge 6)=0.105408$. |
| 2 | `poisson_02_simular_turnos.py` | $10{,}000$ turnos con semilla $42$ | $P(X=0)$ simulada $=0.040000$, $P(X\ge 6)=0.109000$, media $3.209300$, varianza $3.256094$. |
| 3 | `poisson_03_sobdispersion.py` | Mezcla agrupada | $70\%$ $\lambda=2.0$ y $30\%$ $\lambda=6.0$; varianza teórica $6.560000$; varianza simulada $6.811382$. |

El resultado del Paso 3 es un límite: si los eventos se agrupan, la varianza
excede $\lambda$. La Lección 18 modela tiempos de espera hasta el primer o el
$r$-ésimo éxito.

## Libreta de estudio

La libreta autocontenida
[`notebooks/leccion_17_poisson_eventos_raros.ipynb`](notebooks/leccion_17_poisson_eventos_raros.ipynb)
convierte los tres hitos de los scripts en un solo recorrido acumulativo para
el estudiante. Conserva en memoria el modelo Poisson exacto y las simulaciones
con semilla 42, embebe tres figuras, incluye prácticas editables con respuestas
sugeridas desplegables y termina con aserciones para escalamiento de tasa,
colas exactas, identidad de simulación, momentos de mezcla y sobredispersión.
No lee archivos del repositorio ni requiere acceso a la red.

La libreta se ejecutó tanto en su paquete como después de copiarla por sí sola
a un directorio temporal vacío. Se inspeccionaron sus renderizados guardados en
HTML y Markdown y sus tres figuras extraídas.

## Conceptos erróneos comunes

- La $X$ de Poisson es un conteo, no un tiempo de espera.
- $\mathrm{Var}(X)=\lambda$ es un supuesto, no un hecho de los datos.
- Una estimación de simulación puede acercarse a la FMP exacta sin sustituirla.
- Una mezcla de tasas con la misma media no es Poisson.
- Los turnos sintéticos ilustran la aritmética de eventos raros. No afirman
  nada sobre ningún escritorio de operaciones real.

## Estructura del paquete

```text
L17_Poisson_Eventos_Raros/
|-- README.md
|-- src/
|   |-- poisson_01_fmp.py
|   |-- poisson_02_simular_turnos.py
|   `-- poisson_03_sobdispersion.py
|-- figuras/
|   |-- poisson_01_fmp.png
|   |-- poisson_02_simular_turnos.png
|   `-- poisson_03_sobdispersion.png
|-- notebooks/
|   `-- leccion_17_poisson_eventos_raros.ipynb
`-- diapositivas/
    |-- leccion_17.tex
    `-- leccion_17.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L17_Poisson_Eventos_Raros/src/poisson_01_fmp.py
uv run es/L17_Poisson_Eventos_Raros/src/poisson_02_simular_turnos.py
uv run es/L17_Poisson_Eventos_Raros/src/poisson_03_sobdispersion.py
```

Ejecutar y guardar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace es/L17_Poisson_Eventos_Raros/notebooks/leccion_17_poisson_eventos_raros.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_17.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_17.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La distribución de Poisson sigue a Alexander Holmes, Barbara Illowsky y Susan
Dean, *Introductory Business Statistics 2e*, Sección
[4.4](https://openstax.org/books/introductory-business-statistics-2e/pages/4-4-poisson-distribution).
OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. Los turnos sintéticos, el código y las
figuras de este paquete son materiales originales del curso.

