# Lección 10 - Diagramas de árbol y descomposición del espacio muestral

Esta microlección de 50 minutos usa un registro sintético de lotes
entrantes para dibujar un árbol de dos etapas, multiplicar a lo largo de
ramas y sumar caminos mutuamente excluyentes. El paso final muestra que un
árbol en orden temporal no exhibe la condicional inversa, que la Lección 11
nombra como teorema de Bayes.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 3, Sección 3.4 (tablas de contingencia y árboles de
  probabilidad). Práctica complementaria: *Introductory Statistics 2e*,
  Sección 3.5.
- **Prerrequisitos:** Probabilidad condicional e independencia de la Lección
  09, más la regla de multiplicación de la Lección 08.
- **Aviso de datos:** Cada lote, marca de inspección y conteo de camino es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Descomponer un experimento de dos etapas en un árbol de caminos
   mutuamente excluyentes.
2. Etiquetar ramas con frecuencias o probabilidades.
3. Multiplicar a lo largo de un camino para obtener una probabilidad conjunta
   y sumar caminos disjuntos.
4. Explicar por qué $P(B\mid A)$ puede ser una sola rama mientras $P(A\mid B)$
   requiere combinar caminos.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: dos etapas, estado y luego inspección | Esbozar los cuatro caminos terminales. |
| 06-16 | Árbol de frecuencias y tamaño del espacio muestral | Confirmar que los cuatro conteos suman 100. |
| 16-24 | Ejecutar el Paso 1 | Leer 8, 2, 9 y 81 del árbol. |
| 24-34 | Etiquetas de probabilidad y multiplicación de caminos | Calcular $0.10\times0.80=0.08$. |
| 34-42 | Ejecutar el Paso 2 y sumar los caminos marcados | Obtener $P(\text{marcado})=0.17$. |
| 42-48 | Ejecutar el Paso 3 e invertir la condición | Contrastar $0.800000$ con $0.470588$. |
| 48-50 | Verificación de conceptos y entrega a la Lección 11 | Nombrar la inversión que Bayes organizará. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo registro
sintético con `SEED = 42` y agrega el siguiente concepto sin importar otro
script de la lección. Estos valores provienen de dos ejecuciones coincidentes
en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `diagramas_arbol_01_arbol_frecuencias.py` | Árbol de frecuencias, caminos terminales mutuamente excluyentes | $100$ lotes; $10$ defectuosos y $90$ limpios; conteos terminales $8$, $2$, $9$, $81$; total marcado $17$. |
| 2 | `diagramas_arbol_02_ramas_probabilidad.py` | Probabilidades de rama, multiplicación de caminos, suma de caminos disjuntos | $P(D)=0.100000$, $P(F\mid D)=0.800000$, $P(D\cap F)=0.080000$, $P(F)=0.170000$, suma de cuatro caminos $=1.000000$. |
| 3 | `diagramas_arbol_03_condicional_inversa.py` | Condicional inversa a partir de caminos combinados | $P(F\mid D)=0.800000$ versus $P(D\mid F)=0.470588=8/17$. Simulación semilla 42 de $100{,}000$ lotes: $0.469551$. |

El resultado del Paso 3 es un límite, no un teorema nombrado todavía. El
árbol se dibuja en orden temporal, de modo que $P(F\mid D)$ es una rama hacia
abajo mientras $P(D\mid F)$ no lo es. La Lección 11 organiza esa inversión
como teorema de Bayes usando *Principles of Data Science*, Sección 3.4.

## Registro sintético de inspección

| Estado del lote | Marcado | No marcado | Total de fila |
|---|---:|---:|---:|
| Defectuoso | 8 | 2 | 10 |
| Limpio | 9 | 81 | 90 |
| Total de columna | 17 | 83 | 100 |

Ramas de primera etapa: $P(D)=10/100=0.10$ y $P(C)=90/100=0.90$. Ramas de
segunda etapa: $P(F\mid D)=8/10=0.80$ y $P(F\mid C)=9/90=0.10$. La
probabilidad de marcado es la suma de dos caminos mutuamente excluyentes:

\[
P(F)=P(D)P(F\mid D)+P(C)P(F\mid C)=0.08+0.09=0.17.
\]

La pregunta invertida usa los mismos dos caminos como numerador y
denominador:

\[
P(D\mid F)=\frac{P(D\cap F)}{P(F)}=\frac{8}{17}=0.470588\ldots
\]

## Libreta de estudio

La guía estudiantil
[`notebooks/leccion_10_diagramas_arbol_espacio_muestral.ipynb`](notebooks/leccion_10_diagramas_arbol_espacio_muestral.ipynb)
integra los tres pasos en un solo estado acumulativo. Construye desde constantes
el registro sintético completo de 100 lotes, embebe un árbol de frecuencias y
dos figuras de probabilidad editables, y concluye con aserciones ejecutables,
práctica segura y respuestas plegables. Su verificación con semilla 42 simula
100,000 lotes y conserva el referente exacto $8/17$.

La libreta es autocontenida: no descarga datos, no lee archivos del
repositorio, no requiere acceso de red y no importa los scripts del paquete ni
las imágenes retenidas. Puede subirse directamente a Google Colab, abrirse en
VS Code con un kernel de Colab o ejecutarse en el entorno bloqueado del
proyecto. Sus figuras son salidas embebidas; los PNG de `figuras/` siguen
siendo la evidencia retenida producida por los scripts independientes.

## Conceptos erróneos comunes

- Un árbol es una descomposición de un experimento, no una segunda fuente de
  datos.
- Las etiquetas de rama en una etapa son condicionales a llegar a ese nodo.
- Las probabilidades conjuntas de camino son productos; los totales de
  caminos mutuamente excluyentes son sumas.
- $P(F\mid D)$ y $P(D\mid F)$ responden preguntas distintas y no tienen que
  coincidir.
- Una estimación de simulación puede acercarse a la razón exacta de caminos
  sin reemplazarla.
- El registro sintético ilustra la aritmética de árboles. No afirma nada
  sobre ningún proceso real de inspección.

## Estructura del paquete

```text
L10_Diagramas_Arbol_Espacio_Muestral/
|-- README.md
|-- notebooks/
|   `-- leccion_10_diagramas_arbol_espacio_muestral.ipynb
|-- src/
|   |-- diagramas_arbol_01_arbol_frecuencias.py
|   |-- diagramas_arbol_02_ramas_probabilidad.py
|   `-- diagramas_arbol_03_condicional_inversa.py
|-- figuras/
|   |-- diagramas_arbol_01_arbol_frecuencias.png
|   |-- diagramas_arbol_02_probabilidades_caminos.png
|   `-- diagramas_arbol_03_condicional_inversa.png
`-- diapositivas/
    |-- leccion_10.tex
    `-- leccion_10.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L10_Diagramas_Arbol_Espacio_Muestral/src/diagramas_arbol_01_arbol_frecuencias.py
uv run es/L10_Diagramas_Arbol_Espacio_Muestral/src/diagramas_arbol_02_ramas_probabilidad.py
uv run es/L10_Diagramas_Arbol_Espacio_Muestral/src/diagramas_arbol_03_condicional_inversa.py
```

Ejecutar la libreta y guardar todas las salidas de celda:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L10_Diagramas_Arbol_Espacio_Muestral/notebooks/leccion_10_diagramas_arbol_espacio_muestral.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_10.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_10.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de

## Atribución OpenStax

Los diagramas de árbol, etiquetas de rama, multiplicación de caminos y
descomposición del espacio muestral siguen a Alexander Holmes, Barbara
Illowsky y Susan Dean, *Introductory Business Statistics 2e*, Capítulo 3,
Sección
[3.4](https://openstax.org/books/introductory-business-statistics-2e/pages/3-4-contingency-tables-and-probability-trees).
La práctica complementaria de árboles y Venn está en *Introductory
Statistics 2e*, Sección
[3.5](https://openstax.org/books/introductory-statistics-2e/pages/3-5-tree-and-venn-diagrams).
El límite de la condicional inversa se prepara para *Principles of Data
Science*, Sección 3.4, en la Lección 11. OpenStax publica estos textos bajo
la licencia Creative Commons Attribution-NonCommercial-ShareAlike. El
conjunto sintético, el código y las figuras de este paquete son materiales
originales del curso.

