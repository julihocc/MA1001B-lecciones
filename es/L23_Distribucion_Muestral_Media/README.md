# Lección 23 - Distribución muestral de la media

Esta microlección de 50 minutos usa una población de tiempos de ciclo
completamente sintética modelada como $\mathrm{Normal}(\mu=80,\sigma=12)$
minutos. La distribución muestral de $\bar x$ tiene media $\mu$ y error
estándar $\sigma/\sqrt{n}$. Se comparan los tamaños $n=9$ y $n=36$, y
luego 5{,}000 muestras con semilla 42 recuperan esos errores estándar. El
paso final muestra que la fórmula del EE supone extracciones iid de la
población definida.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 7, Sección 7.1 (el teorema del límite central para medias
  muestrales). Práctica complementaria: *Introductory Statistics 2e*,
  Sección 7.1.
- **Prerrequisitos:** Cortes $z$ normales y rendimiento de proceso de las
  Lecciones 21 y 22.
- **Aviso de datos:** Cada tiempo de ciclo y cada media muestral es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar que $E[\bar x]=\mu$ y $\mathrm{EE}(\bar x)=\sigma/\sqrt{n}$.
2. Comparar las distribuciones muestrales para $n=9$ y $n=36$.
3. Verificar la fórmula del EE con una simulación sembrada de medias
   muestrales.
4. Explicar por qué copias agrupadas no iid inflan el EE observado.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: una unidad versus una media muestral | Nombrar $\mu=80$ y $\sigma=12$. |
| 06-16 | Fórmula del EE $\sigma/\sqrt{n}$ | Calcular $12/3=4$ y $12/6=2$. |
| 16-24 | Ejecutar el Paso 1 | Confirmar razón de EE $2.000000$. |
| 24-34 | Simular muchas muestras de $\bar x$ | Predecir EE empírico cerca de 4 y 2. |
| 34-42 | Ejecutar el Paso 2 | Leer $3.997160$ y $2.028859$. |
| 42-48 | Ejecutar el Paso 3 con copias agrupadas | Contrastar $2.028859$ con $4.992583$. |
| 48-50 | Verificación de conceptos y transición a la Lección 24 | Nombrar el TLC para una población asimétrica. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma
población $\mathrm{Normal}(80,12)$ con `SEED = 42` y añade el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `sampling_mean_01_standard_error.py` | $\mathrm{EE}=\sigma/\sqrt{n}$ | EE$(n=9)=4.000000$, EE$(n=36)=2.000000$, razón $=2.000000$. |
| 2 | `sampling_mean_02_n9_vs_n36.py` | 5{,}000 muestras iid, semilla 42 | $n=9$: media de las medias $80.036617$, EE empírico $3.997160$. $n=36$: media de las medias $79.994341$, EE empírico $2.028859$. |
| 3 | `sampling_mean_03_iid_limit.py` | Las copias agrupadas rompen iid | EE de fórmula para 6 conglomerados $=4.898979$, EE empírico agrupado $=4.992583$, razón de inflación $=2.460784$. |

El resultado del Paso 3 es un límite. Treinta y seis observaciones copiadas
de seis conglomerados no son 36 extracciones iid. La Lección 24 conserva el
muestreo iid pero parte de una población sesgada a la derecha e invoca el
teorema del límite central.

## Libreta de estudio para estudiantes

La [libreta estudiantil](notebooks/leccion_23_distribucion_muestral_media.ipynb)
ejecutada es autocontenida y compatible con Google Colab. Reconstruye los tres
pasos de la lección en un único estado acumulativo en memoria, embebe tres
figuras e incluye prácticas editables, respuestas plegables y aserciones para
los valores canónicos. También fue ejecutada desde un directorio temporal
vacío y representada en HTML y Markdown sin leer archivos del repositorio.

## Población sintética de tiempos de ciclo

Población: $X\sim N(80,12^2)$. Para muestras iid,

\[
E[\bar x]=80,\qquad
\mathrm{EE}(\bar x)=\frac{12}{\sqrt{n}}.
\]

Así $\mathrm{EE}(9)=4$ y $\mathrm{EE}(36)=2$. Un experimento con semilla 42
de 5{,}000 muestras recupera $3.997160$ y $2.028859$. Si cada muestra de 36
son seis valores de conglomerado copiados seis veces, el EE observado sube
a $4.992583$, cerca de $12/\sqrt{6}=4.898979$.

## Conceptos erróneos comunes

- $\sigma$ describe una observación. $\sigma/\sqrt{n}$ describe $\bar x$.
- Un $n$ mayor reduce el EE. No cambia la $\sigma$ poblacional.
- Un EE de simulación como $2.028859$ verifica la fórmula; no sustituye
  $2$.
- Repetir el mismo conglomerado seis veces no crea seis extracciones iid
  nuevas.
- La fórmula del EE supone muestreo iid de la población definida.
- Los tiempos de ciclo sintéticos ilustran la aritmética muestral. No son
  una afirmación sobre ninguna línea real.

## Estructura del paquete

```text
L23_Distribucion_Muestral_Media/
|-- README.md
|-- src/
|   |-- sampling_mean_01_standard_error.py
|   |-- sampling_mean_02_n9_vs_n36.py
|   `-- sampling_mean_03_iid_limit.py
|-- figuras/
|   |-- sampling_mean_01_standard_error.png
|   |-- sampling_mean_02_n9_vs_n36.png
|   `-- sampling_mean_03_iid_limit.png
|-- notebooks/
|   `-- leccion_23_distribucion_muestral_media.ipynb
`-- diapositivas/
    |-- leccion_23.tex
    `-- leccion_23.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L23_Distribucion_Muestral_Media/src/sampling_mean_01_standard_error.py
uv run es/L23_Distribucion_Muestral_Media/src/sampling_mean_02_n9_vs_n36.py
uv run es/L23_Distribucion_Muestral_Media/src/sampling_mean_03_iid_limit.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L23_Distribucion_Muestral_Media/notebooks/leccion_23_distribucion_muestral_media.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_23.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_23.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La distribución muestral de $\bar x$ y $\mathrm{EE}=\sigma/\sqrt{n}$
siguen a Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory
Business Statistics 2e*, Capítulo 7, Sección
[7.1](https://openstax.org/books/introductory-business-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar).
La práctica complementaria de distribuciones muestrales está en
*Introductory Statistics 2e*, Sección
[7.1](https://openstax.org/books/introductory-statistics-2e/pages/7-1-the-central-limit-theorem-for-sample-means-x-bar).
El límite iid prepara el teorema del límite central para una población
asimétrica en la Lección 24. OpenStax publica estos textos bajo la licencia
Creative Commons Attribution-NonCommercial-ShareAlike. El conjunto
sintético, el código y las figuras de este paquete son materiales originales
del curso.

