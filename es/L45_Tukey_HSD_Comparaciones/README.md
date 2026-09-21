# Lección 45 - Comparaciones múltiples Tukey HSD

Esta microlección de 50 minutos usa el mismo experimento de empaque
sintético con tres métodos y $n=12$ estaciones cada uno. Los estudiantes
primero corren pruebas $t$ por pares sin ajuste, luego Tukey HSD, y al
final ven que las pruebas por pares sin corrección inflan el error
familiar.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Secciones 12.2--12.3, continuadas como práctica post-hoc por pares
  después de un $F$ significativo de un factor.
- **Prerrequisitos:** La tabla ANOVA y el límite de pares sin etiquetar de
  la Lección 44.
- **Aviso de datos:** Cada estación, método de empaque y tiempo de ciclo es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Correr las tres pruebas $t$ por pares tras un $F$ de ANOVA significativo.
2. Leer diferencias de medias Tukey HSD, $p$-valores ajustados e IC
   simultáneos.
3. Identificar qué pares de método de empaque difieren a $\alpha=0.05$
   familiar.
4. Explicar por qué las pruebas por pares sin ajuste inflan el error
   familiar.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: $F$ fue significativo, quedan tres pares | Listar los tres pares. |
| 06-16 | Pruebas $t$ sin ajuste | Calcular tres $p$-valores. |
| 16-24 | Ejecutar el Paso 1 | Leer $p=0.287762$, $0.000071$, $0.000233$. |
| 24-34 | Intervalos simultáneos Tukey | Verificar qué IC contienen 0. |
| 34-42 | Ejecutar el Paso 2 | Retener Guiado vs Estándar; rechazar los otros dos. |
| 42-48 | Ejecutar el Paso 3 y el límite FWER | Contrastar $0.127800$ con Tukey $0.049000$. |
| 48-50 | Verificación de conceptos y transición a la Lección 46 | Preguntar qué supone aún ANOVA de varianzas iguales. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos
tiempos de ciclo sintéticos con `SEED = 42` y añade el siguiente concepto
sin importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `tukey_hsd_01_pares_sin_ajuste.py` | Tres pruebas $t$ por pares sin ajuste | Estándar-Guiado $p=0.287762$ (retener); Estándar-Automatizado $p=0.000071$ (rechazar); Guiado-Automatizado $p=0.000233$ (rechazar). |
| 2 | `tukey_hsd_02_tukey_hsd.py` | Tukey HSD con `pairwise_tukeyhsd` | Guiado vs Estándar $p_{\text{adj}}=0.521330$, IC que contiene 0, se retiene; los dos pares con Automatizado se rechazan. |
| 3 | `tukey_hsd_03_error_familiar.py` | Error familiar bajo la nula global | 5000 experimentos nulos: FWER sin ajuste $0.127800$; FWER Tukey $0.049000$; $\alpha$ anunciado $=0.05$. |

El resultado del Paso 3 es el límite. Tres pruebas $\alpha=0.05$ sin
ajuste no mantienen en 5 por ciento la probabilidad de algún par falso. La
Lección 46 chequea los supuestos de ANOVA de los que tanto $F$ como Tukey
siguen dependiendo.

## Decisiones Tukey sintéticas

Tukey HSD a $\alpha=0.05$ familiar, con pares en el orden de
`pairwise_tukeyhsd` (grupos únicos ordenados):

| Par | Diferencia de medias | $p$ ajustada | IC 95% simultáneo | ¿Rechazar? |
|---|---:|---:|---|---|
| Automatizado vs Estándar | $5.716390$ | $0.000033$ | $(3.002163,\ 8.430617)$ | Sí |
| Automatizado vs Guiado | $4.500557$ | $0.000789$ | $(1.786329,\ 7.214784)$ | Sí |
| Estándar vs Guiado | $-1.215833$ | $0.521330$ | $(-3.930061,\ 1.498394)$ | No |

Automatizado difiere de ambos competidores. Guiado y Estándar no se
distinguen. El IC que contiene 0 es la decisión de retener. El signo de
Estándar vs Guiado sigue el orden alfabético español de los grupos; el
$p$-valor coincide con el de Guiado vs Estándar en inglés.

## Conceptos erróneos comunes

- Un $F$ de ANOVA significativo no autoriza tres pruebas $t$ ordinarias a
  $0.05$.
- El error familiar es la chance de al menos un par falso, no el alfa por
  prueba.
- Un intervalo Tukey que contiene 0 es una decisión de retener, no una
  prueba de igualdad.
- La línea de empaque sintética ilustra comparaciones múltiples. No es una
  afirmación sobre ningún almacén real.

## Estructura del paquete

```text
L45_Tukey_HSD_Comparaciones/
|-- README.md
|-- src/
|   |-- tukey_hsd_01_pares_sin_ajuste.py
|   |-- tukey_hsd_02_tukey_hsd.py
|   `-- tukey_hsd_03_error_familiar.py
|-- figuras/
|   |-- tukey_hsd_01_pares_sin_ajuste.png
|   |-- tukey_hsd_02_tukey_hsd.png
|   `-- tukey_hsd_03_error_familiar.png
|-- notebooks/
|   `-- leccion_45_tukey_hsd_comparaciones.ipynb
`-- diapositivas/
    |-- leccion_45.tex
    `-- leccion_45.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L45_Tukey_HSD_Comparaciones/src/tukey_hsd_01_pares_sin_ajuste.py
uv run es/L45_Tukey_HSD_Comparaciones/src/tukey_hsd_02_tukey_hsd.py
uv run es/L45_Tukey_HSD_Comparaciones/src/tukey_hsd_03_error_familiar.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L45_Tukey_HSD_Comparaciones/notebooks/leccion_45_tukey_hsd_comparaciones.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_45.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_45.tex
```

## Atribución OpenStax

ANOVA de un factor y la necesidad de un seguimiento tras un $F$
significativo siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Secciones
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova)
y
[12.3](https://openstax.org/books/introductory-business-statistics-2e/pages/12-3-the-f-distribution-and-the-f-ratio).
Tukey HSD es la práctica de comparaciones múltiples post-hoc usada con esas
secciones. OpenStax publica este texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

