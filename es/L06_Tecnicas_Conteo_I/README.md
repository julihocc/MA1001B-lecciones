# Lección 06 - Técnicas de conteo I

Esta microlección de 50 minutos usa un programa sintético de revisión de
operaciones para contar espacios muestrales finitos. Los estudiantes aplican
la regla del producto, distinguen permutaciones de combinaciones, verifican
fórmulas mediante enumeración exhaustiva en Python y diagnostican un error
de sobreconteo cuando las restricciones interactúan.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 3, en especial la Sección 3.1 para espacios muestrales y eventos.
- **Prerrequisitos:** Espacios muestrales, eventos, complementos y conjuntos
  disjuntos de la Lección 05, más notación factorial.
- **Aviso de datos:** Cada instalación, analista, rol y restricción es
  sintético. No se usan datos reales de empresas, socios, empleados u
  operaciones.
- **Nota de alcance:** Este paquete conserva cuatro pasos conceptuales
  acumulativos porque el cuarto expone el límite de sobreconteo requerido.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Aplicar la regla del producto a una secuencia de etapas de elección
   finitas.
2. Calcular permutaciones cuando las posiciones asignadas crean resultados
   distintos.
3. Calcular combinaciones cuando el subconjunto seleccionado no tiene roles
   internos.
4. Verificar una fórmula de conteo mediante enumeración exhaustiva.
5. Explicar por qué seleccionar primero categorías obligatorias puede contar
   el mismo grupo final más de una vez.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-08 | Conectar el tamaño del espacio muestral con la regla del producto y ejecutar el Paso 1 | Verificar $3\times4\times2=24$ por enumeración. |
| 08-20 | Asignar tres roles distintos y ejecutar el Paso 2 | Calcular $P(6,3)=120$ y explicar por qué el orden importa. |
| 20-31 | Quitar las etiquetas de rol y ejecutar el Paso 3 | Calcular $\binom{6}{3}=20$ y explicar la reducción por $3!$. |
| 31-44 | Agregar restricciones de categoría y conflicto y ejecutar el Paso 4 | Rechazar 420 por ser mayor que el universo de 126 elementos y derivar 99. |
| 44-50 | Verificación de conceptos y transición | Elegir un método de conteo y enunciar cómo el mismo grupo podría sobrecontearse. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Programa sintético de revisión de operaciones

Los cuatro pasos usan decisiones relacionadas en un mismo programa sintético
de revisión:

- El Paso 1 configura una revisión a través de tres centros de cumplimiento,
  cuatro etapas de flujo de trabajo y dos tipos de evidencia.
- El Paso 2 asigna tres roles distintos a partir de seis analistas de
  proceso.
- El Paso 3 forma un panel de pares de tres personas sin ranking a partir
  de los mismos seis analistas.
- El Paso 4 forma un grupo de revisión de cuatro personas a partir de cinco
  analistas de operaciones y cuatro especialistas de datos, bajo una regla
  de categoría y un conflicto enunciado.

Los scripts enumeran conjuntos finitos de forma exacta. No usan simulación
estocástica, así que una semilla aleatoria es innecesaria y cada ejecución
es determinista por construcción.

## Reglas de conteo

### Regla del producto

Si una configuración exige una elección de cada etapa sucesiva con
$n_1,n_2,\ldots,n_m$ opciones disponibles, el número total de
configuraciones es

$$
N=\prod_{i=1}^{m}n_i.
$$

Las etapas describen componentes de un resultado. La regla no exige que las
opciones tengan probabilidades iguales.

### Permutaciones

Cuando se llenan $k$ posiciones distintas sin reemplazo a partir de $n$
elementos disponibles, el orden cambia el resultado:

$$
P(n,k)=\frac{n!}{(n-k)!}.
$$

### Combinaciones

Cuando solo importa el subconjunto seleccionado, su ordenamiento interno no
crea un resultado nuevo:

$$
\binom{n}{k}=\frac{n!}{k!(n-k)!}=\frac{P(n,k)}{k!}.
$$

## Scripts incrementales y resultados verificados

Cada script es autocontenido, no usa argumentos de línea de comandos ni
importaciones cruzadas, y escribe solo su PNG correspondiente. Los valores
siguientes provienen de ejecuciones directas repetidas en el entorno
bloqueado de `uv`.

| Paso | Script | Idea añadida | Resultado verificado |
|:---:|---|---|---|
| 1 | `conteo_01_regla_producto.py` | Regla del producto y espacio muestral exhaustivo | $3\times4\times2=24$ configuraciones, coincidentes con las 24 ternas enumeradas. Cada centro aporta 8. |
| 2 | `conteo_02_permutaciones.py` | Asignaciones ordenadas de roles sin reemplazo | $P(6,3)=120$, coincidente con 120 asignaciones generadas. |
| 3 | `conteo_03_combinaciones.py` | Selección de subconjuntos sin ranking | $\binom{6}{3}=20$, coincidente con 20 paneles generados. La reducción desde 120 es $3!=6$. |
| 4 | `conteo_04_restricciones.py` | Trampa de sobreconteo y descomposición por complemento | El universo completo tiene $\binom{9}{4}=126$ grupos. La expresión ingenua da 420. Al retirar 6 grupos de una sola disciplina y 21 grupos de conflicto quedan 99, coincidentes con la enumeración exhaustiva. |

La expresión ingenua del Paso 4 es

$$
5\times4\times\binom{7}{2}=420.
$$

Primero designa un integrante de cada disciplina y luego llena las dos
posiciones restantes. Un grupo final con varios integrantes de una
disciplina puede surgir de varios pares designados distintos, así que la
expresión cuenta ese grupo más de una vez. El cálculo por complemento
parte de los 126 grupos únicos:

$$
126-5-1-21=99.
$$

Los cinco grupos solo de operaciones y el grupo solo de datos son disjuntos
de los 21 grupos que contienen el par en conflicto, así que esta resta no
introduce un segundo traslape.

## Libreta de estudio

La guía estudiantil
[`notebooks/leccion_06_tecnicas_conteo_i.ipynb`](notebooks/leccion_06_tecnicas_conteo_i.ipynb)
integra los cuatro pasos conceptuales en un solo estado determinista acumulativo.
Enumera cada colección finita en memoria, conserva los contratos documentados
de las funciones en `src/`, embebe cuatro figuras editables y concluye con
aserciones ejecutables, práctica segura y respuestas plegables.

La libreta es autocontenida: no descarga datos, no lee archivos del repositorio,
no requiere conexión de red y no importa los scripts del paquete ni las imágenes
retenidas. Puede cargarse directamente en Google Colab, abrirse en VS Code con
un kernel de Colab o ejecutarse en el entorno bloqueado del proyecto. Sus
figuras son salidas embebidas; los PNG de `figuras/` siguen siendo la evidencia
retenida producida por los scripts autónomos.

## Conceptos erróneos comunes

- La regla del producto cuenta configuraciones completas, no la suma de
  elecciones ofrecidas en etapas separadas.
- Permutaciones y combinaciones responden preguntas distintas. La presencia
  de personas u objetos no determina qué fórmula aplica.
- Reordenar integrantes crea una permutación nueva solo cuando las
  posiciones o la secuencia cambian el resultado.
- La enumeración exhaustiva verifica una fórmula para el ejemplo finito
  enunciado. No sustituye el razonamiento necesario para elegir la fórmula.
- Un conteo calculado mayor que todo el espacio muestral prueba que algunos
  resultados se contaron de forma repetida.
- Restar casos inválidos exige comprobar si las categorías excluidas se
  traslapan.
- Los resultados sintéticos no afirman nada sobre ningún programa real de
  revisión.

## Estructura del paquete

```text
L06_Tecnicas_Conteo_I/
|-- README.md
|-- notebooks/
|   `-- leccion_06_tecnicas_conteo_i.ipynb
|-- src/
|   |-- conteo_01_regla_producto.py
|   |-- conteo_02_permutaciones.py
|   |-- conteo_03_combinaciones.py
|   `-- conteo_04_restricciones.py
|-- figuras/
|   |-- conteo_01_regla_producto.png
|   |-- conteo_02_permutaciones.png
|   |-- conteo_03_combinaciones.png
|   `-- conteo_04_restricciones.png
`-- diapositivas/
    |-- leccion_06.tex
    `-- leccion_06.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L06_Tecnicas_Conteo_I/src/conteo_01_regla_producto.py
uv run es/L06_Tecnicas_Conteo_I/src/conteo_02_permutaciones.py
uv run es/L06_Tecnicas_Conteo_I/src/conteo_03_combinaciones.py
uv run es/L06_Tecnicas_Conteo_I/src/conteo_04_restricciones.py
```

Ejecutar la libreta y guardar todas las salidas de las celdas:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L06_Tecnicas_Conteo_I/notebooks/leccion_06_tecnicas_conteo_i.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_06.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_06.tex
```

El PDF retenido contiene el núcleo de ocho diapositivas y el apéndice de

## Atribución OpenStax

El encuadre probabilístico sigue a Alexander Holmes, Barbara Illowsky y
Susan Dean, *Introductory Business Statistics 2e*, Capítulo 3, Sección
[3.1](https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology),
que define experimentos, resultados, espacios muestrales y eventos. El
razonamiento por complemento se apoya en las operaciones de eventos
introducidas allí. El texto citado está licenciado bajo CC BY-NC-SA 4.0.
Las fórmulas de conteo, el ejemplo sintético de operaciones, la
verificación en Python, las figuras y la comparación de sobreconteo son
andamiaje original del curso.

