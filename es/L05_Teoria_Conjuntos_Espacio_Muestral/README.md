# Lección 05 - Teoría de Conjuntos y Espacios Muestrales

## Corrección de accesibilidad — 23 de septiembre de 2026

La matriz de pertenencia conserva datos, categorías y colores, pero sus
anotaciones numéricas ahora son negras (`#000000`). Sobre el rosa `#EC2661`,
el contraste calculado es 5.02:1 (antes 4.19:1 con dígitos blancos); sobre
el fondo claro es mayor. Regeneré la figura, las salidas de la libreta extensa
y los PDF extenso y compacto, y comprobé visualmente la diapositiva de la
matriz. Los tres scripts mantienen los conteos canónicos. El enlace del
compacto a la libreta extensa usa ahora la ruta pública de GitHub, que también
funciona al abrir el compacto en Colab; la copia local sigue junto a él.
La nueva ejecución alojada y la propagación semanal se registran por separado.
Las referencias de páginas de la libreta extensa se alinearon con el PDF
vigente de 55 páginas; el número de páginas del mazo histórico queda sólo
como antecedente más abajo.

La revisión posterior de accesibilidad añadió a la libreta extensa un
equivalente textual de las 40 posiciones de la matriz (ocho resultados por
cinco operaciones). Las otras dos figuras ya tienen sus valores y unidades en
el texto adyacente. Sólo cambió la celda Markdown `interpretar-operaciones`:
las 27 celdas de código y sus salidas siguen idénticas a la ejecución previa.
`nbformat.validate` pasó con 59 celdas y el HTML volvió a renderizar. El
exportador HTML todavía advierte que las tres imágenes de salida carecen de
atributo `alt`; la explicación cercana no elimina ese aviso ni equivale por
sí sola a una prueba con lector de pantalla.

Esta lección utiliza un experimento de despacho completamente sintético para
conectar resultados de negocio con espacios muestrales y eventos. Los estudiantes enumeran todos
los resultados posibles, representan eventos como subconjuntos, calculan uniones,
intersecciones y complementos, y distinguen eventos mutuamente excluyentes de
eventos que juntos cubren el espacio muestral.

- **Ruta compacta de clase:** 40 minutos dentro del bloque asignado a L05.
- **Extensos para estudio:** `diapositivas/leccion_05.pdf` y
  `notebooks/leccion_05_teoria_conjuntos_espacio_muestral.ipynb`.
- **Compactos para exposición:** `diapositivas/leccion_05_compacta.pdf` (12 láminas) y
  `notebooks/leccion_05_compacta.ipynb` (11 celdas, cinco de código).
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 3, Secciones 3.1 y 3.2.
- **Prerrequisitos:** Colecciones básicas en Python, variables categóricas de la
  Lección 01, y la distinción entre resultados posibles y datos observados.
- **Aviso de datos:** Cada registro de despacho es sintético. No se utilizan datos
  reales de empresas, clientes, instalaciones, socios o datos operativos.

## Ruta compacta — clase de 40 minutos

La presentación y la libreta compactas se revisaron para esta demo de L05.
Abrir ambas y ejecutar cinco celdas de código; el cómputo tarda segundos y
queda incluido en cada bloque. La libreta usa la biblioteca estándar y las ocho
frecuencias sintéticas verificadas del script con semilla 42. La generación de
480 filas y sus gráficos permanece en el material extenso de estudio.

| Minutos | Objetivo y diapositivas/celdas | Acción docente y comprobación | Transición |
|---:|---|---|---|
| 00–10 | Modelo y ocho tuplas; láminas 1–3, celda 1. | Planteo el despacho, construyo $S$ y compruebo que tiene ocho tipos. | Distinguir registros. |
| 10–14 | Frecuencias sintéticas; lámina 4, celda 2. | Comparo 480 registros con ocho tipos; compruebo que repetir una tupla no cambia $|S|$. | Definir eventos. |
| 14–26 | Eventos y operaciones; láminas 5–7, celda 3. | Pido predecir intersección, unión y complemento; ejecuto y comparo tipos con registros. | Comparar pares. |
| 26–33 | Disyunción y exhaustividad; láminas 8–9, celda 4. | Contrasto A–B con C–D y verifico cada propiedad por separado. | Aplicar ambas condiciones. |
| 33–40 | Integración y cierre; láminas 10–12, celda 5. | Pido definir F, anticipar 2/40/1/5 y explicar las unidades; enlazo con L06. | Fin de L05. |

Esta es una estimación de conducción, no un ensayo cronometrado en aula.

## Resultados de Aprendizaje

Al final de la lección, un estudiante puede:

1. Definir el experimento, representar un resultado y construir su espacio muestral.
2. Distinguir posibilidades, registros, cardinalidades y frecuencias.
3. Representar eventos y calcular unión, intersección y complemento.
4. Justificar disyunción y exhaustividad por separado.
5. Implementar las operaciones en Python y explicar sus resultados.

## Ruta de estudio extensa (50 minutos estimados)

| Tiempo | Bloque | Producto verificable |
|---:|---|---|
| 00-05 | Caso y objetivos | Explicar qué representa un despacho. |
| 05-17 | Espacio muestral | Construir ocho tuplas y distinguirlas de 480 filas. |
| 17-34 | Eventos y operaciones | Justificar y programar filtros, unión, intersección y complemento. |
| 34-45 | Disyunción y exhaustividad | Comparar pares y justificar cada booleano. |
| 45-50 | Integración | Resolver el evento Exprés retrasado y comprobar los objetivos. |

El [PDF estudiantil](diapositivas/leccion_05.pdf) contiene una ruta central
y una sección diferenciada de consulta, sin límite fijo de diapositivas.
Las consignas anteceden a las soluciones; la consulta desarrolla simulación,

Los fragmentos se incluyen con `\lstinputlisting` desde los tres scripts
del commit `ab8351a`. Cada incremento identifica archivo, función, entradas,
tarea y comprobación. El caso define primero variables y significado de cada fila;
distingue explícitamente supuestos inventados y resultados observados.

### Trazabilidad de objetivos

| Objetivo | Explicación y actividad | Comprobación |
|---|---|---|
| Experimento y S | Tupla ordenada, producto cartesiano e incremento 1 | Ocho tuplas distintas, primera y última correctas. |
| Posibilidad y frecuencia | Tabla ilustrativa, simulación y lectura de gráfica | 8 posibilidades, 480 registros; máximo 196. |
| Operaciones | Ejemplos trabajados e incremento 2 | Cardinalidades 4/4/2/6/4; conteos 172/86/45/213/308. |
| Propiedades | Definiciones, contraejemplos e incremento 3 | A/B: falso/falso; C/D: verdadero/verdadero. |
| Implementación e interpretación | Integración F = Exprés retrasado | Dos tipos, 40 envíos; F frente a A complemento: tamaños 1/5. |

La integración puede conducir a L06 dentro de la misma sesión de 100 minutos.
La consulta no añade tareas obligatorias al recorrido de estudio.

## Experimento de Despacho Sintético

Un despacho produce un resultado ordenado con tres componentes:

$$
(\text{turno},\ \text{servicio},\ \text{estado}).
$$

Los valores posibles son:

- turno: Día o Noche;
- servicio: Estándar o Exprés;
- estado: A tiempo o Retrasado.

El espacio muestral resultante contiene ocho resultados posibles. Los scripts también
simulan 480 registros de despacho con `SEMILLA = 42`. Las probabilidades generadoras
son deliberadamente desiguales, por lo que la inclusión en el espacio muestral no implica que
todos los resultados ocurran con la misma probabilidad.

Los registros se obtienen al ejecutar el Paso 1:
`teoria_conjuntos_01_espacio_muestral.py`. Su función
`simular_despachos()` construye el `DataFrame` en memoria. No se descarga
un conjunto de datos externo ni se conserva un CSV; los Pasos 2 y 3 reconstruyen
las mismas 480 filas con la semilla 42.

| Campo | Rol |
|---|---|
| `id_despacho` | Identificador numérico. Etiqueta un registro pero no es un componente del resultado. |
| `turno` | Primer componente categórico del resultado. |
| `servicio` | Segundo componente categórico del resultado. |
| `estado` | Tercer componente categórico del resultado. |
| `resultado` | Tupla ordenada `(turno, servicio, estado)`. |

## Definiciones y Notación de Eventos

- Un **experimento** es el proceso planificado de despacho cuyo resultado no se fija
  de antemano.
- Un **resultado** es una consecuencia posible de ese experimento.
- El **espacio muestral** $S$ es el conjunto de todos los resultados posibles.
- Un **evento** es cualquier subconjunto del espacio muestral.
- La **unión** $A\cup B$ contiene los resultados en A, en B, o en ambos.
- La **intersección** $A\cap B$ contiene los resultados compartidos por A y B.
- El **complemento** $A^c$ contiene resultados en $S$ que no están en A.

La lección utiliza cuatro eventos:

| Evento | Definición | Resultados posibles |
|---|---|---:|
| A | Despacho en turno de noche | 4 |
| B | Despacho retrasado | 4 |
| C | Despacho con servicio estándar | 4 |
| D | Despacho con servicio exprés | 4 |

Los eventos son **mutuamente excluyentes** cuando su intersección está vacía. Un par es
**exhaustivo** cuando su unión es igual a todo el espacio muestral. Estas propiedades
responden a preguntas diferentes. Los eventos C y D son tanto mutuamente excluyentes como
exhaustivos, mientras que A y B no lo son.

## Scripts Incrementales y Resultados Verificados

Cada script es independiente, no usa argumentos de línea de comandos, reconstruye los mismos
datos sintéticos, y guarda solo su correspondiente archivo PNG. Los valores de abajo provienen
de la ejecución directa repetida en el entorno bloqueado de `uv`.

| Paso | Script | Idea añadida | Resultado verificado |
|:---:|---|---|---|
| 1 | `teoria_conjuntos_01_espacio_muestral.py` | Resultados y el espacio muestral completo | $|S|=8$. Los 8 resultados aparecen entre 480 registros. Día, Estándar, A tiempo es el más frecuente con 196 registros. No se asume igual probabilidad. |
| 2 | `teoria_conjuntos_02_operaciones_conjuntos.py` | Unión, intersección y complemento | $|A|=4$, $|B|=4$, $|A\cap B|=2$, $|A\cup B|=6$, y $|A^c|=4$. En los registros observados, A contiene 172, B contiene 86, su intersección contiene 45, y su unión contiene 213. |
| 3 | `teoria_conjuntos_03_eventos_disjuntos.py` | Pares mutuamente excluyentes y exhaustivos | A y B tienen tamaño de intersección 2 y tamaño de unión 6, por lo que no son ni disjuntos ni exhaustivos. C y D tienen tamaño de intersección 0 y tamaño de unión 8, por lo que son tanto disjuntos como exhaustivos. |

Los conteos teóricos de conjuntos describen tuplas de resultados posibles. Los conteos
observados de registros describen la frecuencia con la que esos resultados ocurrieron en esta
simulación con semilla. Mezclar estos dos niveles confundiría el espacio muestral con los
datos generados a partir de él.

## Revisión del código fuente — 20 de septiembre de 2026

Los tres scripts españoles usan nombres descriptivos en español y explican
el propósito de cada bloque, los parámetros sintéticos y la interpretación
de las operaciones vectorizadas. El cálculo, la construcción de figuras y
su guardado tienen responsabilidades separadas. Importar un script no crea
carpetas ni ejecuta la simulación. La figura del Paso 3 obtiene sus etiquetas
de la tabla y su referencia de cobertura del tamaño del espacio muestral.

La repetición entre scripts conserva los hitos autocontenidos de la lección;
no hay importaciones cruzadas. Dentro de cada paso se reutilizan los cálculos
y se evitan clases, configuraciones o capas sin una necesidad concreta.
Seaborn recibe una tabla de frecuencias en el Paso 1, una matriz de pertenencia
en el Paso 2 y una tabla de pares/medidas en el Paso 3. `barplot` resuelve la
colocación y agrupación de barras; `heatmap` representa pertenencia con escala
fija 0/1. Los conteos ya calculados se muestran sin intervalos de error.
Matplotlib queda para crear la figura, añadir la referencia de cobertura,
etiquetar mediante `bar_label` y guardar/cerrar; no se calculan coordenadas
de barras ni de sus etiquetas. No se añadieron dependencias.
La revisión posterior del mazo desarrolla estos scripts sin modificarlos.
La tercera fase incorpora esta revisión a la libreta española; el track inglés
no forma parte del rediseño.

## Estado de la revisión del mazo — 20 de septiembre de 2026

La presentación española se reconstruyó sobre los scripts de `ab8351a`,
sin editar esos scripts, sus figuras, la libreta ni el track inglés.
La matriz de objetivos anterior documenta explicación, actividad y comprobación.
Se verificaron las ocho frecuencias (196/16/71/25/89/30/38/15), las operaciones
y la integración F: dos tipos, 40 envíos; frente a A complemento, tamaños 1 y 5.

El PDF se compiló dos veces y se revisaron visualmente sus 58 páginas.
El registro final no contiene desbordamientos ni caracteres faltantes.
Sus fragmentos se contrastaron con los archivos y funciones fuente.
La revisión del mazo quedó registrada en `548a008`; no implica publicación en .
SHA-256 del PDF: `6097C8B134F2908A9B3CA028945C5D4B572FA2E4814E8435232CED76352D94BC`.

## Libreta de estudio — tercera fase, 20 de septiembre de 2026

La guía estudiantil
[`notebooks/leccion_05_teoria_conjuntos_espacio_muestral.ipynb`](notebooks/leccion_05_teoria_conjuntos_espacio_muestral.ipynb)
integra los tres pasos en un solo estado acumulativo. Construye en memoria el
espacio muestral de ocho miembros y los 480 despachos sintéticos, conserva las
identidades de fila sembradas, embebe tres figuras editables y concluye con
aserciones ejecutables, práctica segura y respuestas plegables.

La reconstrucción contiene 59 celdas (27 de código). Conserva literalmente
las diez funciones de cálculo y construcción de figuras de `ab8351a`, incluidos
firmas, comentarios y docstrings. Los bloques compartidos aparecen una sola
vez; la explicación alternativa de `etiqueta_resultado` se conserva en Markdown.
Las recetas originales se reproducen como referencia de los scripts.

Cada incremento intercala síntesis conceptual, referencia a `leccion_05.pdf`
(`548a008`, títulos y páginas físicas), pregunta de programación, código,
resultado e interpretación. Las síntesis no sustituyen la fundamentación del
mazo. Se incluye F: Exprés con retraso, dos tipos y 40 envíos; frente a Día,
intersección 1 y unión 5, sin disyunción ni exhaustividad.

La consulta final registra bloque fuente → ID de celda → tratamiento literal,
reutilizado o adaptado. `principal()` se sustituye por celdas secuenciales;
backend, rutas y guardado se sustituyen por `display()` y cierre seguro, sin
PNG adicionales. Las prácticas usan variables independientes del estado base.

### Evidencia de validación y límite pendiente

- `nbformat`, sintaxis de todas las celdas y comparación textual de las diez
  funciones contra la fuente, incluidos comentarios y docstrings: correctos.
- Dos ejecuciones completas desde kernels limpios, una con la libreta sola en
  una carpeta temporal: salidas idénticas y ningún archivo adicional creado.
- Las 480 filas coinciden exactamente con las funciones de los tres scripts;
  frecuencias, operaciones, pares y F coinciden con los valores del mazo.
- Se comprueban reconstrucción con semilla, entradas inválidas, cierre de
  figuras y ausencia de errores de ejecución. Se guardaron las salidas.
- Las tres figuras embebidas se inspeccionaron visualmente: etiquetas y
  valores legibles, sin recortes. El HTML fue exportado para revisión.
- **Pendiente:** inspección visual del HTML completo (Markdown, fórmulas,
  tablas, código y respuestas plegables). El navegador bloqueó la apertura
  del archivo local por política de seguridad; no se eludió el bloqueo.
  La revisión de las figuras no equivale a verificar toda la libreta renderizada.
- Ejecución comprobada en el entorno local bloqueado, no en Colab ni en el
  kernel de Colab de VS Code. La portabilidad a éstos sigue siendo prevista,
  no una prueba de ejecución realizada.
- Scripts, PNG, LaTeX y PDF se mantienen sin cambios. No se recompiló el mazo.

Para completar la revisión visual en un visor autorizado, exportar y abrir el
HTML (revisar también todas las respuestas desplegadas):

```powershell
uv run jupyter nbconvert --to html --output-dir <directorio-temporal> `
  es/L05_Teoria_Conjuntos_Espacio_Muestral/notebooks/leccion_05_teoria_conjuntos_espacio_muestral.ipynb
```

La libreta es autocontenida: no descarga datos, no lee archivos del repositorio,
no requiere conexión de red y no importa los scripts ni las imágenes retenidas
del paquete. Por ello puede subirse directamente a Google Colab, abrirse en VS
Code con un kernel de Colab o ejecutarse en el entorno bloqueado del proyecto.
Sus figuras son salidas embebidas de celda; los PNG bajo `figuras/` siguen
siendo la evidencia retenida producida por los scripts independientes.

## Publicación de L05 en  — 20 de septiembre de 2026

La autorización adicional del usuario incorpora  al cierre por lección.
Se reemplazó el PDF anterior y se añadieron la libreta y los tres scripts en
por curso figuran publicados en orden PDF, libreta y pasos 01–03. Los PNG ya
están embebidos en PDF/libreta; no se cargaron fuentes LaTeX ni documentos docentes.

Fuentes: scripts `ab8351a`, PDF `548a008`, libreta `7fe1caa`. No se modificaron
estos artefactos al publicarlos.  asignó nuevos IDs a los PDF al reemplazarlos,
pero conservó los items existentes, cuya apertura se comprobó:

| Curso | Item PDF conservado | Archivo PDF anterior → actual | Libreta (archivo / item) |
|---|---|---|---|
| 501 | `44958924` | `292941549` → `293000926` | `293000981` / `44991448` |
| 503 | `44959052` | `292941562` → `293001535` | `293001529` / `44991618` |

Vista de estudiante mostró los cinco enlaces y permitió abrir la libreta.
En 503, mostró los cinco recursos en el módulo bloqueado por la aceptación
pendiente del reglamento; no se completó ni se eliminó ese requisito.
No se alteraron evaluaciones, anuncios, encuadres, reglamentos ni otros idiomas.

La carga y la publicación están comprobadas, pero no se completó la descarga
para comparar SHA-256 remoto: no se afirma identidad binaria remota. Sigue
pendiente la revisión visual integral del HTML de la libreta descrita arriba;
esta publicación solicitada no la sustituye. La auditoría semanal conserva
el detalle de IDs, hashes locales y alcance de cada comprobación. El flujo
reutilizable quedó registrado en `b9f4976`, etapa 9 del README del módulo.

En el contraste final, la libreta semanal de 501 conservó el mismo texto/código
en sus 59 celdas, pero tenía salidas y metadatos distintos (Python 3.13.15).
Se preservó sin sobrescribirla: SHA-256
`DA31591A49E8D7111B784B5C8D4B51AA62622CA2C0B6EC8B015450858FFB33FC`.
La libreta semanal de 503 sí coincide con la fuente.  recibió la fuente
de `7fe1caa`, no la copia de trabajo modificada de 501. No se atribuye autoría
a esa diferencia ni se infiere una nueva revisión académica.

## Conceptos Erróneos Comunes

- Un espacio muestral contiene resultados posibles, no una lista de registros observados.
- Un evento puede contener varios resultados. No necesita ser un solo resultado.
- Un resultado pertenece solo una vez a un conjunto incluso cuando satisface más de una
  descripción de evento.
- La unión incluye la intersección. Los resultados compartidos no se listan dos veces.
- Mutuamente excluyente significa que la intersección está vacía. No significa
  que los eventos sean independientes.
- Exhaustivo significa que la unión cubre $S$. Los eventos exhaustivos aún pueden
  traslaparse.
- Listar todos los resultados posibles no los hace igualmente probables.
- Los resultados sintéticos no afirman nada sobre ningún proceso de despacho real.

## Estructura del Paquete

```text
L05_Teoria_Conjuntos_Espacio_Muestral/
|-- README.md
|-- notebooks/
|   `-- leccion_05_teoria_conjuntos_espacio_muestral.ipynb
|-- src/
|   |-- teoria_conjuntos_01_espacio_muestral.py
|   |-- teoria_conjuntos_02_operaciones_conjuntos.py
|   `-- teoria_conjuntos_03_eventos_disjuntos.py
|-- figuras/
|   |-- teoria_conjuntos_01_espacio_muestral.png
|   |-- teoria_conjuntos_02_operaciones_conjuntos.png
|   `-- teoria_conjuntos_03_eventos_disjuntos.png
`-- diapositivas/
    |-- leccion_05.tex
    `-- leccion_05.pdf
```

## Ejecución de la Lección

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L05_Teoria_Conjuntos_Espacio_Muestral/src/teoria_conjuntos_01_espacio_muestral.py
uv run es/L05_Teoria_Conjuntos_Espacio_Muestral/src/teoria_conjuntos_02_operaciones_conjuntos.py
uv run es/L05_Teoria_Conjuntos_Espacio_Muestral/src/teoria_conjuntos_03_eventos_disjuntos.py
```

Ejecutar la libreta y guardar todas las salidas de celda:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L05_Teoria_Conjuntos_Espacio_Muestral/notebooks/leccion_05_teoria_conjuntos_espacio_muestral.ipynb
```

Compila dos veces desde el directorio `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_05.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_05.tex
```

El PDF retenido integra la ruta de clase y la consulta estudiantil.
El repositorio lo almacena mediante Git LFS.

## Libreta de Estudio

`notebooks/leccion_05_teoria_conjuntos_espacio_muestral.ipynb` integra los tres
pasos en un estado acumulativo, embebe las tres figuras y ofrece ejercicios
editables, respuestas plegables y aserciones sobre las cifras canónicas. Es
autocontenida: no lee los scripts, las figuras retenidas ni archivos de datos.

Para ejecutarla localmente desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --execute --to notebook --inplace es/L05_Teoria_Conjuntos_Espacio_Muestral/notebooks/leccion_05_teoria_conjuntos_espacio_muestral.ipynb
```

También puede subirse directamente a Google Colab o abrirse con el kernel de
Colab en VS Code.

## Atribución a OpenStax

La base conceptual y las definiciones siguen a Alexander Holmes, Barbara
Illowsky, y Susan Dean, *Introductory Business Statistics 2e*, Capítulo 3:
Sección [3.1](https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology)
para experimentos, resultados, espacios muestrales, eventos, uniones, intersecciones, y
complementos, y Sección
[3.2](https://openstax.org/books/introductory-business-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events)
para eventos mutuamente excluyentes. El texto citado está licenciado bajo CC BY-NC-SA
4.0. Como repaso, se recomienda resolver de nuevo el Ejemplo 3.2 de la Sección
3.1 y revisar los Ejemplos 3.6 a 3.8 de la Sección 3.2. El ejemplo de despachos
no aparece en el libro: el caso, la simulación, las cifras, el código, las
figuras y la comparación entre disyunción y exhaustividad son materiales
originales del curso elaborados con datos sintéticos.

