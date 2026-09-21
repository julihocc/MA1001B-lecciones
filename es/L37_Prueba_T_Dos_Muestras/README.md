# Lección 37 - Dos medias independientes (t de dos muestras)

Esta microlección de 50 minutos usa dos turnos de almacén completamente
sintéticos, $n_A=30$ y $n_B=32$, para comparar medias independientes con una
prueba $t$ de Welch. Cada grupo conserva su propia $s$. El paso final muestra
que una $t$ de dos muestras significativa no es un experimento aleatorizado:
los asociados no fueron asignados a turnos, y la experiencia difiere por
grupo.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 10, Sección 10.1 (comparación de dos medias poblacionales
  independientes).
- **Prerrequisitos:** $t$ de una muestra de la Lección 35 y la prueba $z$ de
  una proporción de la Lección 36.
- **Aviso de datos:** Cada tiempo de recolección y valor de experiencia es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Distinguir dos muestras independientes de observaciones pareadas.
2. Calcular un estadístico $t$ de Welch sin agrupar las dos varianzas.
3. Leer los grados de libertad de Satterthwaite y un valor p bilateral.
4. Explicar por qué un agrupamiento observacional no es un tratamiento
   aleatorizado.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: dos turnos, dos muestras independientes | Esbozar $H_0:\mu_A=\mu_B$. |
| 06-16 | Medias de grupo y $s$ muestral | Contrastar $n$, $\bar{x}$ y $s$ por turno. |
| 16-24 | Ejecutar el Paso 1 | Leer $\bar{x}_A=48.100885$ y $\bar{x}_B=52.826941$. |
| 24-34 | EE de Welch, no una $s_p$ agrupada | Escribir $\sqrt{s_A^2/n_A+s_B^2/n_B}$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $t=-3.363436$, $p=0.001382$, rechazar $H_0$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar experiencia $4.484559$ frente a $1.801265$ años. |
| 48-50 | Verificación de conceptos y paso a la Lección 38 | Nombrar la siguiente herramienta: $t$ pareada antes-después. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos
turnos sintéticos con `SEED = 42` y no importa otro script de la lección.
Estos valores provienen de dos ejecuciones coincidentes en el entorno
bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `t_dos_muestras_01_resumenes_grupos.py` | Resúmenes de grupos independientes | $n_A=30$, $n_B=32$; $\bar{x}_A=48.100885$, $\bar{x}_B=52.826941$; $s_A=4.660494$, $s_B=6.325509$; diferencia $-4.726057$. |
| 2 | `t_dos_muestras_02_prueba_welch.py` | $t$ de Welch, gl de Satterthwaite, $p$ bilateral | $EE=1.405128$, $t=-3.363436$, $gl=56.900423$, $p=0.001382$ (manual y scipy), $t^*=2.002541$, rechazar $H_0$. |
| 3 | `t_dos_muestras_03_limite_observacional.py` | Confounder observacional | Experiencia media $4.484559$ frente a $1.801265$ años. Los asociados no fueron asignados al azar, así que el valor $p$ de Welch no es una afirmación causal. |

El resultado del Paso 3 es un límite, no una prueba nueva. Welch responde si
las dos medias observadas son compatibles con una $\mu$ común. No responde
si el turno causó la diferencia. La Lección 38 estudia datos pareados
antes-después.

## Registro sintético de turnos

Welch no agrupa las varianzas:

\[
t=\frac{\bar{x}_A-\bar{x}_B}{\sqrt{s_A^2/n_A+s_B^2/n_B}}
=\frac{-4.726057}{1.405128}=-3.363436,
\]

con $gl$ de Satterthwaite $=56.900423$. El valor p bilateral es $0.001382$,
así que se rechaza $H_0:\mu_A=\mu_B$ con $\alpha=0.05$. El turno A también
es más experimentado por $2.683295$ años. Ese desequilibrio no fue creado
por asignación aleatoria.

## Conceptos erróneos comunes

- Dos columnas de tiempos no están automáticamente pareadas; el pareo exige
  un emparejamiento.
- Welch no exige $s_A=s_B$ ni $n_A=n_B$.
- El agrupamiento de varianzas iguales es un modelo distinto del
  procedimiento de Welch declarado.
- Un valor p pequeño compara medias. No identifica una causa.
- Los turnos sintéticos ilustran la $t$ de dos muestras. No afirman nada
  sobre ningún almacén real.

## Estructura del paquete

```text
L37_Prueba_T_Dos_Muestras/
|-- README.md
|-- src/
|   |-- t_dos_muestras_01_resumenes_grupos.py
|   |-- t_dos_muestras_02_prueba_welch.py
|   `-- t_dos_muestras_03_limite_observacional.py
|-- figuras/
|   |-- t_dos_muestras_01_resumenes_grupos.png
|   |-- t_dos_muestras_02_prueba_welch.png
|   `-- t_dos_muestras_03_limite_observacional.png
|-- notebooks/
|   `-- leccion_37_prueba_t_dos_muestras.ipynb
`-- diapositivas/
    |-- leccion_37.tex
    `-- leccion_37.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L37_Prueba_T_Dos_Muestras/src/t_dos_muestras_01_resumenes_grupos.py
uv run es/L37_Prueba_T_Dos_Muestras/src/t_dos_muestras_02_prueba_welch.py
uv run es/L37_Prueba_T_Dos_Muestras/src/t_dos_muestras_03_limite_observacional.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L37_Prueba_T_Dos_Muestras/notebooks/leccion_37_prueba_t_dos_muestras.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_37.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_37.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La prueba $t$ de dos muestras para medias independientes, el error estándar
sin agrupar (Welch) y la distinción entre grupos independientes y pares
emparejados siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Capítulo 10, Sección
[10.1](https://openstax.org/books/introductory-business-statistics-2e/pages/10-1-comparing-two-independent-population-means).
Práctica compañera de medias independientes está en *Introductory Statistics
2e*, Sección
[10.1](https://openstax.org/books/introductory-statistics-2e/pages/10-1-two-population-means-with-unknown-standard-deviations).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

