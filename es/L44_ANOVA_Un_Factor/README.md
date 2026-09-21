# Lección 44 - ANOVA de un factor: SS, MS, F

Esta microlección de 50 minutos usa un experimento de empaque
completamente sintético con tres métodos y $n=12$ estaciones cada uno. Los
estudiantes construyen la tabla ANOVA a mano, coinciden con
`scipy.stats.f_oneway` y luego ven que un $F$ significativo no nombra qué
par difiere.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Secciones 12.2 y 12.3 (ANOVA de un factor, la distribución $F$ y el
  cociente $F$).
- **Prerrequisitos:** Factores experimentales y asignación aleatoria de la
  Lección 43, más la idea de $t$ de dos muestras de la Lección 37.
- **Aviso de datos:** Cada estación, método de empaque y tiempo de ciclo es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Leer $n$, $\bar y_i$ y $s_i$ para tres muestras independientes.
2. Descomponer $SST=SSB+SSE$ y formar $MSB$, $MSE$ y $F=MSB/MSE$.
3. Comparar la $F$ observada con un valor crítico $F(2,33)$ y un $p$-valor.
4. Explicar por qué una hipótesis de medias iguales rechazada aún no
   identifica un par.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: tres métodos, 12 estaciones cada uno | Esbozar las tres muestras. |
| 06-16 | Medias y desviaciones estándar de grupo | Confirmar $n=12$ en cada método. |
| 16-24 | Ejecutar el Paso 1 | Leer medias $49.547060$, $48.331227$, $43.830670$. |
| 24-34 | SST, SSB, SSE en el pizarrón | Verificar $SSB+SSE=SST$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $F=14.823283$ de $MSB/MSE$. |
| 42-48 | Ejecutar el Paso 3 y el límite de pares | Contrastar $p=2.550793\times10^{-5}$ con las brechas sin etiquetar. |
| 48-50 | Verificación de conceptos y transición a la Lección 45 | Nombrar Tukey como el seguimiento por pares. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos
tiempos de ciclo sintéticos con `SEED = 42` y añade el siguiente concepto
sin importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `anova_un_factor_01_resumenes_grupo.py` | $n$, medias y $s$ de tres grupos | Media general $47.236319$; medias $49.547060$, $48.331227$, $43.830670$; $s=3.067311$, $2.353358$, $2.660249$. |
| 2 | `anova_un_factor_02_tabla_ss_ms.py` | $SST$, $SSB$, $SSE$, $MS$, $F$ manual | $SST=459.901248$, $SSB=217.641499$, $SSE=242.259749$, $MSB=108.820749$, $MSE=7.341205$, $F=14.823283$; $gl=2,33,35$. |
| 3 | `anova_un_factor_03_limite_prueba_f.py` | $p$-valor `f_oneway`; $F$ no nombra un par | scipy $F=14.823283$, $p=2.550793\times10^{-5}$, $F_{0.05}(2,33)=3.284918$; brechas $1.215833$, $5.716390$, $4.500557$. |

El resultado del Paso 3 es un límite, no un procedimiento por pares. El $F$
ómnibus rechaza medias iguales, pero Estándar frente a Guiado es una brecha
mucho menor que cualquiera de las comparaciones con Automatizado. La
Lección 45 responde la pregunta por pares con Tukey HSD.

## Tabla ANOVA sintética

\[
H_0:\ \mu_{\text{Estándar}}=\mu_{\text{Guiado}}=\mu_{\text{Automatizado}},
\qquad
H_1:\ \text{al menos una media difiere.}
\]

| Fuente | SS | gl | MS | F |
|---|---:|---:|---:|---:|
| Entre (factor) | 217.641499 | 2 | 108.820749 | 14.823283 |
| Error (dentro) | 242.259749 | 33 | 7.341205 |  |
| Total | 459.901248 | 35 |  |  |

La identidad de reconstrucción es $SSB+SSE=SST=459.901248$. La $F$
observada supera $3.284918$, de modo que $H_0$ se rechaza a $\alpha=0.05$.

## Conceptos erróneos comunes

- Un $F$ grande es evidencia contra medias iguales, no un ranking de los
  tres métodos.
- $MSB$ no es una varianza de las observaciones originales; es $SSB/(k-1)$.
- Coincidir con `f_oneway` es un chequeo de la tabla, no un segundo
  experimento.
- La línea de empaque sintética ilustra la aritmética de ANOVA. No es una
  afirmación sobre ningún almacén real.

## Estructura del paquete

```text
L44_ANOVA_Un_Factor/
|-- README.md
|-- src/
|   |-- anova_un_factor_01_resumenes_grupo.py
|   |-- anova_un_factor_02_tabla_ss_ms.py
|   `-- anova_un_factor_03_limite_prueba_f.py
|-- figuras/
|   |-- anova_un_factor_01_resumenes_grupo.png
|   |-- anova_un_factor_02_tabla_ss_ms.png
|   `-- anova_un_factor_03_limite_prueba_f.png
|-- notebooks/
|   `-- leccion_44_anova_un_factor.ipynb
`-- diapositivas/
    |-- leccion_44.tex
    `-- leccion_44.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L44_ANOVA_Un_Factor/src/anova_un_factor_01_resumenes_grupo.py
uv run es/L44_ANOVA_Un_Factor/src/anova_un_factor_02_tabla_ss_ms.py
uv run es/L44_ANOVA_Un_Factor/src/anova_un_factor_03_limite_prueba_f.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L44_ANOVA_Un_Factor/notebooks/leccion_44_anova_un_factor.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_44.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_44.tex
```

## Atribución OpenStax

ANOVA de un factor, el cociente $F$ y la descomposición entre/dentro siguen
a Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory Business
Statistics 2e*, Secciones
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova)
y
[12.3](https://openstax.org/books/introductory-business-statistics-2e/pages/12-3-the-f-distribution-and-the-f-ratio).
OpenStax publica este texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

