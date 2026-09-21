# Lección 11 - Teorema de Bayes y actualización de probabilidad

Esta microlección de 50 minutos continúa el árbol sintético de inspección de
100 lotes de la Lección 10. Los estudiantes separan la priori $P(D)$ de las
verosimilitudes de marca, aplican el teorema de Bayes para obtener
$P(D\mid F)=8/17$ y luego cambian solo la tasa base para ver el colapso de
la posterior.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Principles of Data Science*, Sección 3.4
  (teorema de Bayes). Preparación y aritmética de árboles: *Introductory
  Business Statistics 2e*, Secciones 3.2--3.4.
- **Prerrequisitos:** Diagramas de árbol y condicionales inversas de la
  Lección 10.
- **Aviso de datos:** Cada lote, marca de inspección y priori es sintético.
  Los scripts no contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Identificar una priori $P(D)$ y las verosimilitudes $P(F\mid D)$ y
   $P(F\mid C)$.
2. Calcular una posterior con el teorema de Bayes y hacerla coincidir con la
   razón de caminos $8/17$.
3. Recalcular la posterior cuando cambia la priori y las verosimilitudes no.
4. Explicar por qué tratar $P(F\mid D)$ como $P(D\mid F)$ ignora la tasa
   base.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: priori versus verosimilitud | Etiquetar $P(D)=0.10$ y $P(F\mid D)=0.80$. |
| 06-16 | Piezas del teorema de Bayes | Escribir el numerador $P(F\mid D)P(D)$. |
| 16-24 | Ejecutar el Paso 1 | Confirmar $0.100000$, $0.800000$ y $0.100000$. |
| 24-34 | Ley de la probabilidad total para $P(F)$ | Obtener $0.08+0.09=0.17$. |
| 34-42 | Ejecutar el Paso 2 | Hacer coincidir la posterior $0.470588$ con $8/17$. |
| 42-48 | Ejecutar el Paso 3 con priori $0.02$ | Contrastar $0.470588$ con $0.140351$. |
| 48-50 | Verificación de conceptos y entrega a la Lección 12 | Nombrar la falacia de la tasa base. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo árbol
sintético con `SEED = 42` y agrega el siguiente concepto sin importar otro
script de la lección. Estos valores provienen de dos ejecuciones coincidentes
en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `bayes_01_priori_verosimilitud.py` | Priori $P(D)$ y verosimilitudes de marca | $P(D)=0.100000$, $P(C)=0.900000$, $P(F\mid D)=0.800000$, $P(F\mid C)=0.100000$. |
| 2 | `bayes_02_posterior.py` | Fórmula de Bayes, $P(F)$, posterior | Numerador $0.080000$, $P(F)=0.170000$, $P(D\mid F)=0.470588=8/17$. |
| 3 | `bayes_03_sensibilidad_tasa_base.py` | Sensibilidad a la tasa base | Priori $0.02$ produce $P(F)=0.114000$ y $P(D\mid F)=0.140351$. La $P(F\mid D)=0.800000$ ingenua no es la posterior. |

El resultado del Paso 3 es un límite, no una afirmación de que todo evento
raro tenga una posterior pequeña. Las verosimilitudes se mantienen fijas
para que solo se mueva la tasa base. La Lección 12 pasa de actualizar una
probabilidad a la calidad de la muestra que produjo los conteos.

## Actualización de Bayes en el árbol sintético

Las verosimilitudes se mantienen en $P(F\mid D)=0.80$ y $P(F\mid C)=0.10$.

\[
P(D\mid F)=\frac{P(F\mid D)P(D)}{P(F\mid D)P(D)+P(F\mid C)P(C)}.
\]

| Priori $P(D)$ | $P(F)$ | Posterior $P(D\mid F)$ |
|---:|---:|---:|
| $0.10$ | $0.170000$ | $0.470588=8/17$ |
| $0.02$ | $0.114000$ | $0.140351$ |

Un lote marcado sigue siendo más probable de ser defectuoso que la priori,
pero no está ni cerca de $80\%$ defectuoso cuando la tasa de defectuosos es
rara.

## Libreta de estudio

La guía estudiantil
[`notebooks/leccion_11_teorema_bayes_actualizacion.ipynb`](notebooks/leccion_11_teorema_bayes_actualizacion.ipynb)
integra los tres pasos en un solo estado acumulativo. Separa priori y
verosimilitudes, reconstruye ambos caminos hacia la evidencia, embebe tres
figuras editables y concluye con aserciones ejecutables, práctica segura y
respuestas plegables. Una curva posterior hace visible la sensibilidad a la
tasa base y conserva los referentes exactos de priori 0.10 y 0.02.

La libreta es autocontenida: no descarga datos, no lee archivos del
repositorio, no requiere acceso de red y no importa los scripts del paquete ni
las imágenes retenidas. Puede subirse directamente a Google Colab, abrirse en
VS Code con un kernel de Colab o ejecutarse en el entorno bloqueado del
proyecto. Sus figuras son salidas embebidas; los PNG de `figuras/` siguen
siendo la evidencia retenida producida por los scripts independientes.

## Conceptos erróneos comunes

- $P(F\mid D)$ es una verosimilitud, no una posterior.
- El teorema de Bayes reutiliza los mismos dos caminos marcados ya sumados
  en la Lección 10.
- Una tasa alta de detección no cancela una tasa base baja.
- Cambiar la priori manteniendo fijas las verosimilitudes aísla el efecto
  de la tasa base.
- El árbol sintético ilustra la actualización. No es una afirmación sobre
  ningún proceso real de inspección.

## Estructura del paquete

```text
L11_Teorema_Bayes_Actualizacion/
|-- README.md
|-- notebooks/
|   `-- leccion_11_teorema_bayes_actualizacion.ipynb
|-- src/
|   |-- bayes_01_priori_verosimilitud.py
|   |-- bayes_02_posterior.py
|   `-- bayes_03_sensibilidad_tasa_base.py
|-- figuras/
|   |-- bayes_01_priori_verosimilitud.png
|   |-- bayes_02_posterior.png
|   `-- bayes_03_sensibilidad_tasa_base.png
`-- diapositivas/
    |-- leccion_11.tex
    `-- leccion_11.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L11_Teorema_Bayes_Actualizacion/src/bayes_01_priori_verosimilitud.py
uv run es/L11_Teorema_Bayes_Actualizacion/src/bayes_02_posterior.py
uv run es/L11_Teorema_Bayes_Actualizacion/src/bayes_03_sensibilidad_tasa_base.py
```

Ejecutar la libreta y guardar todas las salidas de celda:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L11_Teorema_Bayes_Actualizacion/notebooks/leccion_11_teorema_bayes_actualizacion.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_11.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_11.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de

## Atribución OpenStax

El teorema de Bayes, las prioris, las verosimilitudes y la actualización
posterior siguen *Principles of Data Science*, Sección
[3.4](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory).
La preparación del árbol de inspección usa a Alexander Holmes, Barbara
Illowsky y Susan Dean, *Introductory Business Statistics 2e*, Secciones
[3.2](https://openstax.org/books/introductory-business-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events)
y
[3.4](https://openstax.org/books/introductory-business-statistics-2e/pages/3-4-contingency-tables-and-probability-trees).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

