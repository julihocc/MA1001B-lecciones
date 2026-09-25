# Lección 07: Técnicas de conteo II

## Categorías repetidas y asignaciones

Esta lección extiende el conteo de objetos distintos a
categorías repetidas. Un escenario sintético de red de servicio conecta
permutaciones con repetición, asignaciones multinomiales y combinaciones con
repetición. El paso final expone el límite central del conteo: los perfiles de
ocupación posibles no son automáticamente igualmente probables.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. contar secuencias distintas cuando las etiquetas de categoría se repiten;
2. interpretar un coeficiente multinomial como una asignación de objetos
   etiquetados a categorías etiquetadas con tamaños fijos;
3. usar estrellas y barras para contar asignaciones no negativas de unidades
   idénticas;
4. explicar por qué contar perfiles posibles no determina sus
   probabilidades.

## Prerrequisitos

- espacios muestrales finitos y eventos de la Lección 05;
- la regla del producto, notación factorial, permutaciones y combinaciones de
  la Lección 06;
- funciones básicas de Python, tuplas, ciclos y gráficas de barras.

## Ruta vigente de 40 minutos

El profesor usa conjuntamente [la libreta compacta](notebooks/leccion_07_compacta.ipynb)
y [la presentación compacta](diapositivas/leccion_07_compacta.pdf).
La libreta incluye enumeración ejecutable y simulación con semilla; la
presentación expone derivaciones y preguntas. Esta estimación cabe en la sesión
S02 de 100 minutos.

| Tiempo | Enfoque compacto | Verificación y transición |
|---:|---|---|
| 00-04 | Definir solicitudes etiquetadas y etiquetas de cola repetidas. | Nombrar un resultado antes de elegir regla. |
| 04-12 | Permutaciones repetidas: $8!/(3!3!2!)=560$. | Verificar por enumeración y reinterpretar el coeficiente. |
| 12-21 | Asignación multinomial: 560 y distribución 210-210-140 para R01. | Identificar solicitudes etiquetadas y tamaños de categoría. |
| 21-36 | Estrellas y barras: 165 perfiles; comparar probabilidades exactas con simulación de semilla 42. | Explicar por qué los perfiles no son equiprobables. |
| 36-40 | Verificación conceptual y enlace con L08. | Decir qué información adicional necesita la probabilidad. |

## Ruta anterior de 50 minutos

Se conserva la distribución original como antecedente histórico; no es la
ruta de exposición vigente.

| Tiempo | Actividad | Evidencia |
|---:|---|---|
| 0-5 min | Definir un resultado antes de elegir una fórmula. | Distinguir solicitudes etiquetadas de etiquetas de cola repetidas. |
| 5-15 min | Derivar permutaciones con repetición. | Se dividen los reordenamientos duplicados. |
| 15-24 min | Ejecutar el Paso 1 e inspeccionar su gráfica. | Fórmula y enumeración exhaustiva devuelven 560. |
| 24-34 min | Reformular el mismo coeficiente como asignación multinomial. | El Paso 2 devuelve 560 asignaciones y la partición 210-210-140 para R01. |
| 34-43 min | Contar perfiles de ocupación con estrellas y barras. | El Paso 3 devuelve 165 perfiles no negativos de cuatro centros. |
| 43-48 min | Comparar el conteo con las probabilidades de enrutamiento. | Las probabilidades exactas y simuladas rechazan el supuesto de perfiles iguales. |
| 48-50 min | Verificación de conceptos y puente a la L08. | Enunciar por qué la probabilidad necesita más que un conteo. |

La verificación de conceptos puede conectar directamente con otra lección en la
misma sesión de clase. No es una actividad obligatoria de cierre de sesión.

## Escenario sintético de red de servicio

Todas las solicitudes, colas, centros de servicio y mecanismos de enrutamiento
son sintéticos. No se representa ninguna organización, socio o afirmación
operativa reales.

Ocho solicitudes de servicio etiquetadas entran primero a tres colas
etiquetadas con tamaños fijos: tres Prioridad, tres Estándar y dos Auditoría.
El paso final considera ocho unidades o solicitudes en cuatro centros de
servicio etiquetados.

### Permutaciones con repetición

Si una secuencia contiene conteos de categoría \(n_1,\ldots,n_k\), sus
reordenamientos distintos son

\[
\frac{n!}{n_1!n_2!\cdots n_k!}.
\]

Para el patrón de cola 3-3-2,

\[
\frac{8!}{3!3!2!}=560.
\]

El conteo ingenuo \(8!=40{,}320\) trata etiquetas de categoría idénticas como
distintas. Sobreconta cada secuencia única por \(3!3!2!=72\).

### Asignaciones multinomiales

El mismo coeficiente cuenta asignaciones de ocho solicitudes etiquetadas a
tres colas etiquetadas de tamaños 3, 3 y 2. La enumeración exhaustiva produce
560 asignaciones. En ellas, la solicitud R01 aparece en Prioridad 210 veces,
Estándar 210 veces y Auditoría 140 veces. Estos conteos reflejan los tamaños
fijos de cola: \(3/8\), \(3/8\) y \(2/8\) de las 560 asignaciones.

### Combinaciones con repetición

Estrellas y barras cuenta las formas de distribuir \(m\) unidades idénticas
entre \(r\) categorías etiquetadas:

\[
\binom{m+r-1}{r-1}.
\]

Para ocho unidades en cuatro centros, los scripts verifican

\[
\binom{8+4-1}{4-1}=\binom{11}{3}=165
\]

perfiles de ocupación ordenados no negativos.

## Scripts y resultados verificados

Cada script es independiente, no acepta argumentos de línea de comandos, no
importa otro paso de la lección y escribe solo su PNG correspondiente. Los
resultados de abajo provienen de ejecuciones repetidas en el entorno
bloqueado de `uv`.

| Paso | Script | Resultado verificado |
|:---:|---|---|
| 1 | `asignaciones_01_permutaciones_repetidas.py` | Fórmula y enumeración devuelven 560; el conteo ingenuo es 40,320 y el factor de duplicado es 72. |
| 2 | `asignaciones_02_categorias_multinomiales.py` | Fórmula y enumeración devuelven 560 asignaciones; R01 aparece 210, 210 y 140 veces en Prioridad, Estándar y Auditoría. |
| 3 | `asignaciones_03_estrellas_barras_limite_probabilidad.py` | Fórmula y enumeración devuelven 165 perfiles. Con 500,000 simulaciones y semilla 42, las estimaciones de perfiles seleccionados son 0.005288, 0.013000 y 0.025894. |

Para enrutamiento uniforme independiente a cuatro centros, las
probabilidades exactas de los perfiles ordenados son:

| Perfil | Valor igual incorrecto | Probabilidad exacta | Simulación semilla 42 |
|---|---:|---:|---:|
| `(5, 1, 1, 1)` | 0.00606061 | 0.00512695 | 0.00528800 |
| `(4, 2, 1, 1)` | 0.00606061 | 0.01281738 | 0.01300000 |
| `(3, 2, 2, 1)` | 0.00606061 | 0.02563477 | 0.02589400 |

El valor falso \(1/165\) supone que todos los perfiles de ocupación son
igualmente probables. El enrutamiento aleatorio pondera cada perfil por el
número de secuencias de solicitudes etiquetadas que lo producen. Contar
perfiles por sí solo no justifica una asignación de probabilidad.

## Libreta de estudio

La libreta y la presentación compactas son material de exposición del profesor.
La siguiente libreta extensa sigue siendo la guía de estudio del alumnado; se
conservan los scripts, las figuras y la presentación extensa originales.

La guía estudiantil
[`notebooks/leccion_07_tecnicas_conteo_ii.ipynb`](notebooks/leccion_07_tecnicas_conteo_ii.ipynb)
integra los tres pasos en un solo estado acumulativo. Construye todas las
colecciones finitas en memoria, conserva los contratos documentados de `src/`
con una interfaz de código en español, embebe tres figuras editables y concluye
con aserciones ejecutables, práctica segura y respuestas plegables. La
simulación con semilla 42 usa 500,000 sorteos e incluye una comprobación de
reconstrucción exacta.

La libreta es autocontenida: no descarga datos, no lee archivos del repositorio,
no requiere conexión de red y no importa los scripts del paquete ni las imágenes
retenidas. Puede cargarse directamente en Google Colab, abrirse en VS Code con
un kernel de Colab o ejecutarse en el entorno bloqueado del proyecto. Sus
figuras son salidas embebidas; los PNG de `figuras/` siguen siendo la evidencia
retenida producida por los scripts autónomos.

## Conceptos erróneos comunes

- Dividir por \(n!\) no es una corrección general. Divida solo por factoriales
  de categorías repetidas intercambiables.
- Una secuencia de etiquetas repetidas y una asignación de solicitudes
  etiquetadas son descripciones distintas que pueden compartir el mismo
  coeficiente multinomial.
- Estrellas y barras exige unidades idénticas y categorías etiquetadas;
  cambiar cualquiera de las dos condiciones cambia el espacio muestral.
- Un perfil ordenado como `(5, 1, 1, 1)` nombra qué centro recibe cada
  conteo. Permutar sus entradas crea otros perfiles ordenados.
- Contar 165 perfiles posibles no prueba que cada uno tenga probabilidad
  \(1/165\).
- El acuerdo de Monte Carlo respalda el modelo de enrutamiento enunciado; no
  prueba que ninguna red de servicio real enrute solicitudes de forma
  uniforme.

## Estructura del paquete

```text
L07_Tecnicas_Conteo_II/
|-- README.md
|-- notebooks/
|   |-- leccion_07_tecnicas_conteo_ii.ipynb
|   `-- leccion_07_compacta.ipynb
|-- src/
|   |-- asignaciones_01_permutaciones_repetidas.py
|   |-- asignaciones_02_categorias_multinomiales.py
|   `-- asignaciones_03_estrellas_barras_limite_probabilidad.py
|-- figuras/
|   |-- asignaciones_01_permutaciones_repetidas.png
|   |-- asignaciones_02_categorias_multinomiales.png
|   `-- asignaciones_03_estrellas_barras_limite_probabilidad.png
`-- diapositivas/
    |-- leccion_07.tex
    |-- leccion_07.pdf
    |-- leccion_07_compacta.tex
    `-- leccion_07_compacta.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L07_Tecnicas_Conteo_II/src/asignaciones_01_permutaciones_repetidas.py
uv run es/L07_Tecnicas_Conteo_II/src/asignaciones_02_categorias_multinomiales.py
uv run es/L07_Tecnicas_Conteo_II/src/asignaciones_03_estrellas_barras_limite_probabilidad.py
```

Ejecutar la libreta y guardar todas las salidas de las celdas:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L07_Tecnicas_Conteo_II/notebooks/leccion_07_tecnicas_conteo_ii.ipynb
```

Compilar dos veces desde el directorio `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_07.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_07.tex
```

## Atribución y alcance

El fundamento de probabilidad sigue a OpenStax, *Introductory Business
Statistics 2e*, Capítulo 3, Sección 3.1: espacios muestrales, resultados
igualmente probables, probabilidad teórica por conteo y frecuencia relativa
de largo plazo. Las fórmulas de permutación con repetición, multinomial y
estrellas y barras son una extensión combinatoria desarrollada en el curso y
alineada con el currículo MA1001B; no se atribuyen como definiciones de esa
sección de OpenStax.

- Sección OpenStax: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology>
- Autores: Alexander Holmes, Barbara Illowsky y Susan Dean.
- Aviso de licencia usado por la fuente del curso: CC BY-NC-SA 4.0.

## 25/09/2026 · comentarios guía en compactos

Cada celda de código de la libreta compacta docente contiene ahora comentarios explicativos junto a la operación pertinente. Se conservaron el Python ejecutable y las salidas guardadas; una ejecución limpia reprodujo esas salidas. No se cambiaron materiales estudiantiles.

| Libreta | Celdas de código | SHA-256 |
|---|---:|---|
| [leccion_07_compacta.ipynb](notebooks/leccion_07_compacta.ipynb) | 3 | FC3FDA7F9A2AF21723C4EEBB26978FEB9BAE261AFE6971273A9FC9FF91855FCB |
