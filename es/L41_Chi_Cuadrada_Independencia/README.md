# Lección 41 - Prueba ji-cuadrada de independencia

Esta microlección de 50 minutos usa una tabla de pago sintética $2\times 3$,
$n=325$, para contrastar si la conversión es independiente del canal de
adquisición. Los conteos esperados usan la fórmula de independencia,
$df=(2-1)(3-1)=2$, y la V de Cramer resume la fuerza de asociación. El paso
final muestra que una asociación significativa no es una afirmación causal:
el patrón desaparece dentro de estratos de dispositivo.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 11, Sección 11.4 (prueba de independencia).
- **Prerrequisitos:** Bondad de ajuste ji-cuadrada de la Lección 40.
- **Aviso de datos:** Cada conteo de visitantes es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Formar conteos esperados $E=(\text{total de fila}\times\text{total de columna})/n$.
2. Calcular $\chi^2$ para una tabla de doble entrada con $df=(r-1)(c-1)$.
3. Reportar un p-valor de cola derecha y la V de Cramer.
4. Explicar por qué una asociación significativa no es una afirmación causal.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: conversión por canal | Esbozar la tabla $2\times 3$. |
| 06-16 | Márgenes y conteos esperados | Calcular $E_{11}=113\times120/325$. |
| 16-24 | Ejecutar el Paso 1 | Leer esperados $41.723$, $43.462$, $27.815$ en la fila convertida. |
| 24-34 | $\chi^2$ y $df=2$ | Nombrar independencia como $H_0$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $\chi^2=10.114985$, $p=0.006361$, $V=0.176417$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar $p$ conjunto $=0.006361$ con escritorio $p=0.368546$. |
| 48-50 | Verificación de conceptos y transición a la Lección 42 | Nombrar la siguiente herramienta: homogeneidad ji-cuadrada. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma tabla
sintética de pago sin importar otro script de la lección. Estos valores
provienen de dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `independencia_01_tabla_contingencia.py` | Tabla $2\times 3$ y $E_{ij}$ | $n=325$; convertidos observados $40,55,18$; no convertidos $80,70,62$; $E$ mínimo $=27.815385$. |
| 2 | `independencia_02_chi_cuadrada.py` | Independencia $\chi^2$, $df=2$, V de Cramer | $\chi^2=10.114985$, $p=0.006361$, $\chi^{2*}=5.991465$, $V=0.176417$, rechazar $H_0$. |
| 3 | `independencia_03_limite_no_causalidad.py` | Confusión por dispositivo | $p$ conjunto $=0.006361$; escritorio $p=0.368546$; móvil $p=0.761939$. La asociación no es una afirmación causal. |

El resultado del Paso 3 es un límite, no una variante nueva de ji-cuadrada.
El canal no se asignó al azar. La Lección 42 conserva la misma aritmética
pero cambia la historia de muestreo a muestras independientes.

## Tabla sintética de pago

| Resultado | Correo | Búsqueda | Redes | Total |
|---|---:|---:|---:|---:|
| Convertido | 40 | 55 | 18 | 113 |
| No convertido | 80 | 70 | 62 | 212 |
| Total | 120 | 125 | 80 | 325 |

\[
\chi^2=10.114985,\qquad df=2,\qquad p=0.006361,\qquad V=0.176417.
\]

Dentro de visitantes de escritorio el p-valor es $0.368546$; dentro de
visitantes móviles es $0.761939$. La asociación combinada es compatible con
una mezcla de dispositivos, no con un efecto causal de canal.

## Conceptos erróneos comunes

- La $H_0$ de independencia trata de una muestra clasificada en cruz, no de
  dos experimentos.
- $df=(r-1)(c-1)$, no $n-1$.
- La V de Cramer es un resumen de fuerza; no es un p-valor.
- Rechazar independencia no identifica qué celda causó el resultado, y no
  identifica una causa en el mundo.
- La tabla sintética de pago ilustra independencia. No es una afirmación
  sobre ningún canal real de adquisición.

## Estructura del paquete

```text
L41_Chi_Cuadrada_Independencia/
|-- README.md
|-- src/
|   |-- independencia_01_tabla_contingencia.py
|   |-- independencia_02_chi_cuadrada.py
|   `-- independencia_03_limite_no_causalidad.py
|-- figuras/
|   |-- independencia_01_tabla_contingencia.png
|   |-- independencia_02_chi_cuadrada.png
|   `-- independencia_03_limite_no_causalidad.png
|-- notebooks/
|   `-- leccion_41_chi_cuadrada_independencia.ipynb
`-- diapositivas/
    |-- leccion_41.tex
    `-- leccion_41.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L41_Chi_Cuadrada_Independencia/src/independencia_01_tabla_contingencia.py
uv run es/L41_Chi_Cuadrada_Independencia/src/independencia_02_chi_cuadrada.py
uv run es/L41_Chi_Cuadrada_Independencia/src/independencia_03_limite_no_causalidad.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L41_Chi_Cuadrada_Independencia/notebooks/leccion_41_chi_cuadrada_independencia.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_41.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_41.tex
```

## Atribución OpenStax

La prueba ji-cuadrada de independencia, los conteos esperados a partir del
producto de márgenes, $df=(r-1)(c-1)$ y la advertencia de que asociación no
es causalidad siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Capítulo 11, Sección
[11.4](https://openstax.org/books/introductory-business-statistics-2e/pages/11-4-test-of-independence).
La práctica complementaria de independencia está en *Introductory Statistics
2e*, Sección
[11.3](https://openstax.org/books/introductory-statistics-2e/pages/11-3-test-of-independence).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

