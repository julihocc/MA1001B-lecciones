# Lección 43 - Diseño experimental: factores y aleatorización

Esta microlección de 50 minutos usa una línea de empaque completamente
sintética para definir un factor de tres niveles, asignar al azar 36
estaciones y contrastar ese experimento con grupos autoseleccionados. El
paso final muestra que un factor observacional no es un tratamiento
aleatorizado.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  introducción del Capítulo 12 y Sección 12.2 (preparación de ANOVA de un
  factor: factor, respuesta y muestras independientes).
- **Prerrequisitos:** Comparaciones de dos muestras de las Lecciones 37-39
  y la idea de que asociación no es causalidad de la Lección 41.
- **Aviso de datos:** Cada estación, valor de experiencia, método de
  empaque y tiempo de ciclo es sintético. Los scripts no contienen datos
  reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Nombrar el factor experimental, sus niveles, las unidades experimentales
   y la respuesta.
2. Explicar por qué la asignación aleatoria equilibra covariables previas
   en esperanza.
3. Comparar medias de grupo tras una asignación aleatoria de 36 unidades.
4. Afirmar por qué los grupos autoseleccionados mezclan el factor con quién
   eligió el nivel.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: tres métodos de empaque, 36 estaciones | Nombrar factor, unidades y respuesta. |
| 06-16 | Asignación aleatoria de 12 estaciones por método | Confirmar que la asignación está equilibrada. |
| 16-24 | Ejecutar el Paso 1 | Leer conteos $12$, $12$, $12$ y brecha de experiencia $1.047694$. |
| 24-34 | Tiempos de ciclo tras la aleatorización | Comparar las tres medias aleatorizadas. |
| 34-42 | Ejecutar el Paso 2 | Obtener brecha Auto-Estándar $-8.019206$ frente al efecto verdadero $-7$. |
| 42-48 | Ejecutar el Paso 3 y el límite de autoselección | Contrastar brechas de experiencia $1.047694$ y $5.216727$. |
| 48-50 | Verificación de conceptos y transición a la Lección 44 | Preguntar si un $F$ significativo puede nombrar el par. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye las mismas
estaciones sintéticas con `SEED = 42` y añade el siguiente concepto sin
importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `diseno_experimental_01_factor_aleatorizacion.py` | Factor de tres niveles y asignación aleatoria de 36 unidades | $n=12$ por método; experiencia media $4.618485$, $5.943166$, $5.666180$ años; brecha Auto-Estándar $1.047694$. |
| 2 | `diseno_experimental_02_resultados_aleatorizados.py` | Tiempos de ciclo tras la aleatorización | Medias $51.871576$, $50.039332$, $43.852371$ segundos; brecha aleatorizada Auto-Estándar $-8.019206$; efecto verdadero Automatizado $-7$. |
| 3 | `diseno_experimental_03_limite_autoseleccion.py` | Grupos autoseleccionados confunden método con experiencia | Experiencia autoseleccionada $2.678106$, $5.654891$, $7.894834$ años; brecha observacional de experiencia $5.216727$; brecha observacional $Y$ $-14.809630$. |

El resultado del Paso 3 es un límite de diseño. Los operadores con más
experiencia eligen Automatizado, de modo que la brecha observacional mezcla
el método con quién lo seleccionó. La Lección 44 analiza la respuesta
aleatorizada de tres grupos con ANOVA de un factor.

## Experimento sintético de línea de empaque

Los efectos aditivos verdaderos sobre el tiempo de ciclo, en segundos, son
$0$ (Estándar), $-2$ (Guiado) y $-7$ (Automatizado). La asignación
aleatoria no usa la experiencia del operador para elegir un método. La
autoselección asigna el tercil de menor experiencia a Estándar, el tercil
medio a Guiado y el tercil más alto a Automatizado.

Brecha aleatorizada Auto-Estándar:

\[
\bar y_{\text{Automatizado}}-\bar y_{\text{Estándar}}=-8.019206.
\]

Brecha observacional Auto-Estándar:

\[
\bar y_{\text{Automatizado autoseleccionado}}-\bar y_{\text{Estándar autoseleccionado}}=-14.809630.
\]

La comparación observacional exagera el efecto del método porque la
experiencia ya no es una covariable equilibrada.

## Conceptos erróneos comunes

- Un nivel de factor observado en operaciones no es automáticamente un
  tratamiento.
- La asignación aleatoria equilibra covariables en esperanza; no hace
  idéntica cada media muestral.
- Una brecha observacional grande puede ser el número causal equivocado
  aunque $n$ esté equilibrado.
- La línea de empaque sintética ilustra diseño. No es una afirmación sobre
  ningún almacén real.

## Estructura del paquete

```text
L43_Principios_Diseno_Experimental/
|-- README.md
|-- src/
|   |-- diseno_experimental_01_factor_aleatorizacion.py
|   |-- diseno_experimental_02_resultados_aleatorizados.py
|   `-- diseno_experimental_03_limite_autoseleccion.py
|-- figuras/
|   |-- diseno_experimental_01_factor_aleatorizacion.png
|   |-- diseno_experimental_02_resultados_aleatorizados.png
|   `-- diseno_experimental_03_limite_autoseleccion.png
|-- notebooks/
|   `-- leccion_43_principios_diseno_experimental.ipynb
`-- diapositivas/
    |-- leccion_43.tex
    `-- leccion_43.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L43_Principios_Diseno_Experimental/src/diseno_experimental_01_factor_aleatorizacion.py
uv run es/L43_Principios_Diseno_Experimental/src/diseno_experimental_02_resultados_aleatorizados.py
uv run es/L43_Principios_Diseno_Experimental/src/diseno_experimental_03_limite_autoseleccion.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L43_Principios_Diseno_Experimental/notebooks/leccion_43_principios_diseno_experimental.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_43.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_43.tex
```

## Atribución OpenStax

Los factores experimentales, las muestras independientes y la preparación
para comparar más de dos medias siguen a Alexander Holmes, Barbara Illowsky
y Susan Dean, *Introductory Business Statistics 2e*, Capítulo 12,
[Introducción](https://openstax.org/books/introductory-business-statistics-2e/pages/12-introduction)
y Sección
[12.2](https://openstax.org/books/introductory-business-statistics-2e/pages/12-2-one-way-anova).
OpenStax publica este texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

