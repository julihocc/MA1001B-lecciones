# Lección 08: Reglas de probabilidad y tablas de contingencia

## Paquete activo por audiencia
- **Estudiante, estudio autogestionado:** [presentación extensa](estudiante/leccion_08.pdf), [fuente Beamer](estudiante/leccion_08.tex), [libreta extensa](estudiante/leccion_08_reglas_probabilidad_tablas_contingencia.ipynb) y [ZIP de nueve archivos](estudiante/leccion_08_estudiante.zip).
- **Docente, exposición:** [presentación compacta](docente/leccion_08_compacta.pdf), [fuente Beamer](docente/leccion_08_compacta.tex) y [libreta compacta](docente/leccion_08_compacta.ipynb). Son autónomas entre sí y la presentación tiene ocho láminas.
- **Compartido:** [tres scripts incrementales](src/README.md) y tres figuras verificadas en la carpeta figuras. La tabla fija de cuatro conteos define los 400 pedidos sintéticos; expandirla en filas es parte del paso didáctico de construir y cotejar una tabla de contingencia. No hay un dataset externo que adquirir.

**Versión de trabajo W08:** L08 para S04 de MA1001B.501; la ruta común de 40 minutos se inserta en un bloque de 50 minutos, seguido por otro bloque de muestreo preparado con fuentes existentes. No hay datos de socios en esta lección.


Esta microlección de 50 minutos usa un conjunto sintético de operaciones de
pedidos para leer probabilidades marginales y conjuntas en una tabla de
contingencia, aplicar las reglas de complemento y adición, y exponer el
supuesto oculto al multiplicar probabilidades marginales.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. leer celdas, totales de fila, totales de columna y el gran total de una
   tabla de doble entrada;
2. calcular probabilidades marginales, conjuntas y de complemento;
3. aplicar la regla general de adición sin contar dos veces una intersección;
4. explicar por qué \(P(A)P(B)\) no puede reemplazar \(P(A\cap B)\) a menos
   que se haya establecido independencia.

## Prerrequisitos

- resultados, eventos, uniones, intersecciones y complementos de la Lección 05;
- conteo de espacios muestrales finitos de las Lecciones 06 y 07;
- tablas básicas de pandas y gráficas de matplotlib.

## Ruta de facilitación de 50 minutos

| Tiempo | Actividad | Evidencia |
|---:|---|---|
| 0-5 min | Definir eventos a partir de una pregunta de negocio. | \(M\): revisión manual; \(L\): entrega retrasada. |
| 5-15 min | Leer una tabla de contingencia de doble entrada. | Distinguir celdas, márgenes y el gran total. |
| 15-24 min | Ejecutar el Paso 1. | Probabilidades marginales y conjuntas verificadas en 400 registros. |
| 24-33 min | Derivar las reglas de complemento y adición. | Se identifica el traslape antes de calcular un evento O. |
| 33-41 min | Ejecutar el Paso 2. | La unión correcta 0.38 reemplaza la suma ingenua 0.50. |
| 41-47 min | Ejecutar el Paso 3 y exponer el límite de multiplicación. | El producto marginal 0.06 no coincide con la intersección observada 0.12. |
| 47-50 min | Verificación de conceptos y puente a la L09. | Identificar el razonamiento de probabilidad condicional que falta. |

La verificación de conceptos puede conducir directamente a otra lección en la
misma sesión de clase. No es una actividad obligatoria de cierre de sesión.

## Conjunto sintético de operaciones

Los 400 registros de pedidos, procesos de enrutamiento y resultados de
entrega son sintéticos. No describen ninguna organización, socio o proceso
operativo reales.

| Proceso de enrutamiento | Retrasado | A tiempo | Total de fila |
|---|---:|---:|---:|
| Revisión manual | 48 | 72 | 120 |
| Automatizado | 32 | 248 | 280 |
| Total de columna | 80 | 320 | 400 |

Sea \(M\) revisión manual y \(L\) entrega retrasada. La tabla da

\[
P(M)=\frac{120}{400}=0.30,\qquad
P(L)=\frac{80}{400}=0.20,
\]

y

\[
P(M\cap L)=\frac{48}{400}=0.12.
\]

## Reglas de complemento y adición

La regla del complemento da

\[
P(M^c)=1-P(M)=0.70.
\]

La regla general de adición es

\[
P(M\cup L)=P(M)+P(L)-P(M\cap L).
\]

Para la tabla sintética,

\[
P(M\cup L)=0.30+0.20-0.12=0.38.
\]

La suma ingenua 0.50 cuenta dos veces los 48 pedidos en \(M\cap L\). Contar
directamente los 152 pedidos que son revisión manual, retrasados, o ambos
también da \(152/400=0.38\).

## El límite de la regla de multiplicación

La regla general de multiplicación es

\[
P(M\cap L)=P(M)P(L\mid M).
\]

La tabla da \(P(L\mid M)=48/120=0.40\), de modo que

\[
P(M)P(L\mid M)=0.30(0.40)=0.12.
\]

Multiplicar las probabilidades marginales en cambio da

\[
P(M)P(L)=0.30(0.20)=0.06,
\]

que no coincide con la intersección observada. Esta lección usa ese
desajuste como límite; la Lección 09 desarrolla probabilidad condicional e
independencia.

## Libreta de estudio

La guía estudiantil
[`estudiante/leccion_08_reglas_probabilidad_tablas_contingencia.ipynb`](estudiante/leccion_08_reglas_probabilidad_tablas_contingencia.ipynb)
integra los tres pasos en un solo estado acumulativo. Construye en memoria los
400 registros sintéticos, conserva los contratos funcionales documentados en
`src/`, embebe tres figuras editables y concluye con aserciones ejecutables,
práctica segura y respuestas plegables.

La libreta es autocontenida: no descarga datos, no lee archivos del
repositorio, no requiere acceso de red y no importa los scripts del paquete ni
las imágenes retenidas. Por ello puede subirse directamente a Google Colab,
abrirse en VS Code con un kernel de Colab o ejecutarse en el entorno bloqueado
del proyecto. Sus figuras son salidas embebidas; los PNG de `figuras/` siguen
siendo la evidencia retenida producida por los scripts independientes.

## Scripts y resultados verificados

Cada script es independiente, usa la semilla 42 para el orden determinista de
los registros, no acepta argumentos de línea de comandos, no importa un paso
anterior y escribe solo su PNG correspondiente. Los resultados de abajo
provienen de ejecuciones repetidas en el entorno bloqueado de `uv`.

| Paso | Script | Resultado verificado |
|:---:|---|---|
| 1 | `reglas_probabilidad_01_tabla_contingencia.py` | 400 registros; \(P(M)=0.30\), \(P(L)=0.20\) y \(P(M\cap L)=0.12\). |
| 2 | `reglas_probabilidad_02_complemento_adicion.py` | \(P(M^c)=0.70\); suma ingenua 0.50; unión corregida y contada de forma directa 0.38. |
| 3 | `reglas_probabilidad_03_limite_multiplicacion.py` | Intersección observada 0.12; producto marginal 0.06; \(P(L\mid M)=0.40\); producto general 0.12. |

## Conceptos erróneos comunes

- Una probabilidad de celda usa una celda conjunta; una probabilidad
  marginal usa un total de fila o de columna.
- O incluye el traslape a menos que los eventos sean mutuamente excluyentes.
- Sumar \(P(A)+P(B)\) sin restar \(P(A\cap B)\) cuenta dos veces los
  resultados compartidos.
- Mutuamente excluyente e independiente no significan lo mismo.
- El atajo \(P(A\cap B)=P(A)P(B)\) exige independencia; no es la regla
  general de multiplicación.
- Una tabla de contingencia describe asociaciones en los registros
  sintéticos. No establece un efecto causal de la revisión manual sobre la
  entrega retrasada.

## Estructura del paquete

- src/: tres programas autónomos.
- figuras/: tres PNG producidos por los scripts.
- estudiante/: presentación extensa, fuente Beamer y libreta extensa.
- docente/: presentación compacta, fuente Beamer y libreta compacta.

## Ejecución

Desde la raíz de 02-lecciones/, usar el entorno fijado por pyproject.toml y uv.lock. Ejecutar en orden los tres scripts de src/. Las dos libretas se pueden ejecutar de principio a fin desde un kernel Python limpio y una carpeta aislada, sin datos externos. Compilar las fuentes Beamer desde estudiante/ y docente/ con dos pasadas de pdflatex; ambos PDF usan las figuras compartidas y el preámbulo común.

La ruta compacta estimada suma 40 minutos: tabla y márgenes 12, complemento y unión 13, límite de multiplicación 10, comprobación y transición 5. Los 10 minutos restantes del bloque L08 de S04 cubren apertura, preguntas y contingencia. Esta estimación no es un ensayo de clase.

## Atribución OpenStax

Las definiciones de eventos, unión, intersección, complemento y
probabilidades desde una tabla de doble entrada siguen a OpenStax,
*Introductory Business Statistics 2e*, Capítulo 3, Sección 3.1. Las reglas
generales de adición y multiplicación siguen la Sección 3.3.

- Sección 3.1: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology>
- Sección 3.3: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-3-two-basic-rules-of-probability>
- Autores: Alexander Holmes, Barbara Illowsky y Susan Dean.
- Licencia: CC BY-NC-SA 4.0.

