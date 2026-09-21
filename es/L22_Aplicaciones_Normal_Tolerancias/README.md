# Lección 22 - Aplicaciones normales: tolerancias e intervalos operativos

Esta microlección de 50 minutos usa un proceso de llenado completamente
sintético modelado como $\mathrm{Normal}(\mu=50,\sigma=4)$ gramos. El
intervalo de especificación es $[44,56]$. El rendimiento es la probabilidad
en especificación. Un desplazamiento de la media a $52$ reduce el
rendimiento. El paso final muestra que una alta conformidad con la
especificación no es lo mismo que un proceso centrado.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 6, Sección 6.2 (uso de la distribución normal). Práctica
  complementaria: *Introductory Statistics 2e*, Sección 6.2.
- **Prerrequisitos:** Puntuaciones $z$ y áreas normales estándar de la Lección 21.
- **Aviso de datos:** Cada peso de llenado, límite de especificación y
  rendimiento es sintético. Los scripts no contienen datos reales de empresas,
  clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Convertir límites de especificación en cortes $z$.
2. Calcular el rendimiento del proceso como $P(\mathrm{LIE}<X<\mathrm{LSE})$.
3. Cuantificar cómo un desplazamiento de la media cambia el rendimiento.
4. Explicar por qué un proceso de alto rendimiento no tiene que estar centrado en el objetivo.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: espec $[44,56]$ alrededor del objetivo $50$ | Bosquejar LIE, objetivo, LSE. |
| 06-16 | Cortes $z$ para un proceso centrado | Calcular $z=\pm 1.5$. |
| 16-24 | Ejecutar el Paso 1 | Leer rendimiento $0.866386$. |
| 24-34 | Desplazamiento de la media a $52$ | Recalcular cortes $z$ $-2$ y $1$. |
| 34-42 | Ejecutar el Paso 2 | Obtener rendimiento $0.818595$ y caída $0.047791$. |
| 42-48 | Ejecutar el Paso 3: proceso estrecho descentrado | Contrastar rendimiento $0.977218$ con una media de $52$. |
| 48-50 | Verificación de conceptos y transición a la Lección 23 | Nombrar la distribución muestral de $\bar x$. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el proceso de
llenado sintético con `SEED = 42` y agrega el siguiente concepto sin importar
otro script de la lección. Estos valores provienen de dos ejecuciones
coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `tolerancias_normal_01_rendimiento_espec.py` | Cortes $z$ de especificación y rendimiento en espec | $z=\pm 1.500000$, cada cola $0.066807$, rendimiento $0.866386$. |
| 2 | `tolerancias_normal_02_desplazamiento_media.py` | Desplazamiento de media $\mu=52$ | Nuevos cortes $z$ $-2.000000$ y $1.000000$, rendimiento $0.818595$, caída $0.047791$. |
| 3 | `tolerancias_normal_03_centrado_vs_conforme.py` | Proceso estrecho descentrado | $\mu=52$, $\sigma=2$, cortes $z$ $-4.000000$ y $2.000000$, rendimiento $0.977218$. |

El resultado del Paso 3 es un límite. Un proceso puede pasar la especificación
a una tasa alta y aun así situarse fuera del objetivo. La Lección 23 pasa de
una unidad a la distribución muestral de la media muestral.

## Libreta de estudio para estudiantes

La [libreta estudiantil](notebooks/leccion_22_aplicaciones_normal_tolerancias.ipynb)
ejecutada es autocontenida y compatible con Google Colab. Reconstruye los tres
pasos de la lección en un único estado acumulativo en memoria, embebe tres
figuras e incluye prácticas editables, respuestas plegables y aserciones para
los valores canónicos. También fue ejecutada desde un directorio temporal
vacío y representada en HTML y Markdown sin leer archivos del repositorio.

## Proceso sintético de llenado

Modelo centrado: $X\sim N(50,4^2)$. Especificación $[44,56]$:

\[
z_{\mathrm{LIE}}=\frac{44-50}{4}=-1.5,\qquad
z_{\mathrm{LSE}}=\frac{56-50}{4}=1.5,
\]
\[
P(44<X<56)=0.866386.
\]

Después de un desplazamiento de $+2$ gramos, $X\sim N(52,4^2)$ y el
rendimiento cae a $0.818595$. Un reloj más estrecho descentrado $N(52,2^2)$
eleva el rendimiento a $0.977218$ mientras permanece $2$ gramos por encima del
objetivo.

## Conceptos erróneos comunes

- El rendimiento es una probabilidad de intervalo, no una altura de densidad en el objetivo.
- La especificación no se mueve cuando se mueve la media del proceso; los cortes $z$ sí.
- Un $\sigma$ más pequeño puede elevar el rendimiento incluso cuando la media está fuera del objetivo.
- Una alta conformidad con la especificación no es evidencia de que el proceso esté centrado.
- Las colas iguales $0.066807$ aparecen solo cuando el proceso está centrado dentro de una especificación simétrica.
- Los llenados sintéticos ilustran la aritmética de tolerancias. No afirman nada sobre ninguna línea de llenado real.

## Estructura del paquete

```text
L22_Aplicaciones_Normal_Tolerancias/
|-- README.md
|-- src/
|   |-- tolerancias_normal_01_rendimiento_espec.py
|   |-- tolerancias_normal_02_desplazamiento_media.py
|   `-- tolerancias_normal_03_centrado_vs_conforme.py
|-- figuras/
|   |-- tolerancias_normal_01_rendimiento_espec.png
|   |-- tolerancias_normal_02_desplazamiento_media.png
|   `-- tolerancias_normal_03_centrado_vs_conforme.png
|-- notebooks/
|   `-- leccion_22_aplicaciones_normal_tolerancias.ipynb
`-- diapositivas/
    |-- leccion_22.tex
    `-- leccion_22.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L22_Aplicaciones_Normal_Tolerancias/src/tolerancias_normal_01_rendimiento_espec.py
uv run es/L22_Aplicaciones_Normal_Tolerancias/src/tolerancias_normal_02_desplazamiento_media.py
uv run es/L22_Aplicaciones_Normal_Tolerancias/src/tolerancias_normal_03_centrado_vs_conforme.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L22_Aplicaciones_Normal_Tolerancias/notebooks/leccion_22_aplicaciones_normal_tolerancias.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_22.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_22.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

Las probabilidades normales entre límites de especificación, los cortes $z$ y
los intervalos operativos siguen a Alexander Holmes, Barbara Illowsky y Susan
Dean, *Introductory Business Statistics 2e*, Capítulo 6, Sección
[6.2](https://openstax.org/books/introductory-business-statistics-2e/pages/6-2-using-the-normal-distribution).
La práctica complementaria de aplicaciones está en *Introductory Statistics
2e*, Sección
[6.2](https://openstax.org/books/introductory-statistics-2e/pages/6-2-using-the-normal-distribution).
El límite de rendimiento frente a centrado prepara las distribuciones
muestrales de la media en la Lección 23. OpenStax publica estos textos bajo la
licencia Creative Commons Attribution-NonCommercial-ShareAlike. El conjunto
sintético, el código y las figuras de este paquete son materiales originales
del curso.

