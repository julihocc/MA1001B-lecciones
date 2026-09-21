# Lección 25 - Distribución muestral de una proporción

Esta microlección de 50 minutos usa un indicador sintético de entrega
tardía con proporción poblacional $p=0.18$. Muestras de $n=120$ tickets
tienen $\mathrm{EE}(\hat p)=\sqrt{p(1-p)/n}$. Una simulación con semilla 42
de 5{,}000 muestras recupera ese EE. El paso final muestra que $np<5$ hace
fallar la aproximación normal de $\hat p$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 7, Sección 7.3 (el teorema del límite central para
  proporciones). Práctica complementaria: *Introductory Statistics 2e*,
  Sección 7.3.
- **Prerrequisitos:** Distribución muestral de $\bar x$ y el TLC de las
  Lecciones 23 y 24.
- **Aviso de datos:** Cada indicador de entrega tardía y cada proporción
  muestral es sintético. Los scripts no contienen datos reales de empresas,
  clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Escribir $E[\hat p]=p$ y $\mathrm{EE}(\hat p)=\sqrt{p(1-p)/n}$.
2. Verificar las condiciones $np$ y $n(1-p)$ para una aproximación normal.
3. Recuperar la fórmula del EE con una simulación binomial sembrada.
4. Explicar por qué $np<5$ hace que el modelo de campana de $\hat p$ sea la
   herramienta equivocada.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: un indicador 0-1 de entrega tardía | Nombrar $p=0.18$ y $n=120$. |
| 06-16 | Fórmula del EE y conteos $np$ | Calcular $np=21.6$ y $n(1-p)=98.4$. |
| 16-24 | Ejecutar el Paso 1 | Leer EE $=0.035071$. |
| 24-34 | Simular muchos $\hat p$ | Predecir media cerca de $0.18$. |
| 34-42 | Ejecutar el Paso 2 | Obtener EE empírico $0.035079$. |
| 42-48 | Ejecutar el Paso 3 con $n=20$ | Contrastar $np=3.6$ y $P(\hat p=0)=0.018892$. |
| 48-50 | Verificación de conceptos y transición a la Lección 26 | Nombrar la insesgadez de $\hat p$ como estimador. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo
indicador $p=0.18$ con `SEED = 42` y añade el siguiente concepto sin
importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `sampling_proportion_01_se_phat.py` | $\mathrm{EE}(\hat p)$ y verificaciones $np$ | $np=21.600000$, $n(1-p)=98.400000$, EE $=0.035071$. |
| 2 | `sampling_proportion_02_simulation.py` | 5{,}000 muestras de $n=120$ | Media de $\hat p=0.179663$, EE empírico $=0.035079$, $P(\hat p>0.22)$ simulada $=0.119800$ versus normal $0.127032$. |
| 3 | `sampling_proportion_03_np_condition_limit.py` | $n=20$, $np=3.6<5$ | $P(\hat p=0)$ exacta $=0.018892$, simulada $0.016600$, masa normal cerca de 0 $=0.035594$, asimetría $=0.430019$. |

El resultado del Paso 3 es un límite. La curva normal de $\hat p$ necesita
que $np$ y $n(1-p)$ valgan al menos 5. La Lección 26 trata $\bar x$ y un
estimador de una observación como estimadores puntuales competidores.

La [libreta estudiantil](notebooks/leccion_25_distribucion_muestral_proporcion.ipynb)
ejecutada es una guía de estudio autocontenida y compatible con Google Colab.
Reconstruye los tres pasos en un estado acumulativo en memoria, embebe tres
figuras e incluye prácticas editables, respuestas plegables y aserciones para
los valores canónicos. También se ejecutó desde un directorio temporal vacío y
se renderizó a HTML y Markdown sin leer archivos del repositorio.

## Indicador sintético de entrega tardía

Proporción poblacional $p=0.18$. Para tickets iid,

\[
E[\hat p]=0.18,\qquad
\mathrm{EE}(\hat p)=\sqrt{\frac{0.18\times 0.82}{120}}=0.035071.
\]

Los conteos $np=21.6$ y $n(1-p)=98.4$ superan ambos 5. Un experimento con
semilla 42 de 5{,}000 muestras recupera EE empírico $0.035079$. Para
$n=20$, $np=3.6<5$ y $P(\hat p=0)=0.018892$, una masa puntual que la
campana no puede representar.

## Conceptos erróneos comunes

- $\hat p$ es un estadístico muestral. $p$ es el parámetro poblacional.
- $\sqrt{p(1-p)/n}$ usa la $p$ poblacional, no un $\hat p$ observado
  único, cuando el objeto de estudio es la distribución muestral.
- $np\ge 5$ y $n(1-p)\ge 5$ son condiciones para la imagen normal, no
  para la existencia de $\hat p$.
- $P(\hat p=0)$ puede ser material cuando $n$ es pequeño. Una campana
  continua no tiene esa masa puntual.
- Un EE de simulación cercano como $0.035079$ verifica $0.035071$. No
  sustituye la fórmula.
- Los indicadores sintéticos ilustran la aritmética muestral. No son una
  afirmación sobre ningún proceso real de entrega.

## Estructura del paquete

```text
L25_Distribucion_Muestral_Proporcion/
|-- README.md
|-- src/
|   |-- sampling_proportion_01_se_phat.py
|   |-- sampling_proportion_02_simulation.py
|   `-- sampling_proportion_03_np_condition_limit.py
|-- figuras/
|   |-- sampling_proportion_01_se_phat.png
|   |-- sampling_proportion_02_simulation.png
|   `-- sampling_proportion_03_np_condition_limit.png
|-- notebooks/
|   `-- leccion_25_distribucion_muestral_proporcion.ipynb
`-- diapositivas/
    |-- leccion_25.tex
    `-- leccion_25.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L25_Distribucion_Muestral_Proporcion/src/sampling_proportion_01_se_phat.py
uv run es/L25_Distribucion_Muestral_Proporcion/src/sampling_proportion_02_simulation.py
uv run es/L25_Distribucion_Muestral_Proporcion/src/sampling_proportion_03_np_condition_limit.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L25_Distribucion_Muestral_Proporcion/notebooks/leccion_25_distribucion_muestral_proporcion.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_25.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_25.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La distribución muestral de $\hat p$ y $\mathrm{EE}=\sqrt{p(1-p)/n}$
siguen a Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory
Business Statistics 2e*, Capítulo 7, Sección
[7.3](https://openstax.org/books/introductory-business-statistics-2e/pages/7-3-the-central-limit-theorem-for-proportions).
La práctica complementaria de proporciones está en *Introductory Statistics
2e*, Sección
[7.3](https://openstax.org/books/introductory-statistics-2e/pages/7-3-the-central-limit-theorem-for-proportions).
El límite $np$ prepara las propiedades de estimadores puntuales en la
Lección 26. OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y
las figuras de este paquete son materiales originales del curso.

