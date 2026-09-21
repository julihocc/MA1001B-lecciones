# Lección 42 - Prueba ji-cuadrada de homogeneidad

Esta microlección de 50 minutos usa tres muestras sintéticas de almacén
(Norte $n=120$, Centro $n=100$, Sur $n=90$) con las mismas tres categorías
de ticket. La homogeneidad contrasta si sitios muestreados de forma
independiente comparten una mezcla. El paso final muestra que homogeneidad
e independencia comparten la aritmética ji-cuadrada pero no la historia de
muestreo.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 11, Sección 11.5 (prueba de homogeneidad).
- **Prerrequisitos:** Independencia ji-cuadrada de la Lección 41.
- **Aviso de datos:** Cada conteo de tickets es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Mostrar tres mezclas de categoría muestreadas de forma independiente con
   totales de fila fijos.
2. Calcular la $\chi^2$ de homogeneidad con $df=(r-1)(c-1)$.
3. Decidir $H_0$: los sitios comparten una mezcla a $\alpha=0.05$.
4. Contrastar el plan de muestreo de homogeneidad con una tabla de
   independencia.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: tres muestras planeadas de sitio | Marcar los totales de fila como diseño, no azar. |
| 06-16 | Participaciones dentro del sitio | Calcular la participación telefónica Norte $60/120=0.50$. |
| 16-24 | Ejecutar el Paso 1 | Leer participaciones $0.500000$, $0.350000$, $0.277778$ para teléfono. |
| 24-34 | Conteos esperados de homogeneidad | Escribir $E=(\text{total de fila}\times\text{total de columna})/n$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $\chi^2=17.812605$, $df=4$, $p=0.001343$, rechazar $H_0$. |
| 42-48 | Ejecutar el Paso 3 | Nombrar la historia de independencia que reutiliza los mismos números. |
| 48-50 | Verificación de conceptos y transición a la Lección 43 | Nombrar el diseño experimental como la siguiente pregunta de muestreo. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye las mismas tres
muestras sintéticas de sitio sin importar otro script de la lección. Estos
valores provienen de dos ejecuciones coincidentes en el entorno bloqueado
de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `homogeneidad_01_tres_muestras.py` | Tres mezclas independientes | Norte $60,40,20$; Centro $35,40,25$; Sur $25,30,35$; participaciones telefónicas $0.500000$, $0.350000$, $0.277778$. |
| 2 | `homogeneidad_02_chi_cuadrada.py` | Homogeneidad $\chi^2$ | $\chi^2=17.812605$, $df=4$, $p=0.001343$, $\chi^{2*}=9.487729$, $E$ mínimo $=23.225806$, rechazar $H_0$. |
| 3 | `homogeneidad_03_limite_historia_muestreo.py` | El mismo estadístico, distinta $H_0$ | $\chi^2=17.812605$ y $p=0.001343$ compartidos. Homogeneidad fija tamaños de sitio; independencia clasifica una muestra de dos maneras. |

El resultado del Paso 3 es un límite, no un segundo cálculo. El número
$17.812605$ no dice qué diseño produjo la tabla. La Lección 43 pasa de
muestras observacionales de sitio a factores experimentales aleatorizados.

## Registro sintético de tres sitios

| Sitio | Teléfono | Chat | Correo | Tamaño de muestra |
|---|---:|---:|---:|---:|
| Norte | 60 | 40 | 20 | 120 |
| Centro | 35 | 40 | 25 | 100 |
| Sur | 25 | 30 | 35 | 90 |
| Total | 120 | 110 | 80 | 310 |

\[
\chi^2=17.812605,\qquad df=(3-1)(3-1)=4,\qquad p=0.001343.
\]

Los tres totales de fila los eligió el plan de muestreo. Esa es la historia
de homogeneidad. Las mismas celdas podrían haber salido de una muestra de
$310$ tickets clasificada después por sitio y canal; eso sería
independencia.

## Conceptos erróneos comunes

- Homogeneidad no es bondad de ajuste: no hay una mezcla hipotética de
  antemano, solo la afirmación de que varias poblaciones comparten una
  mezcla desconocida.
- Homogeneidad no es independencia: los totales de fila los fija el diseño.
- La fórmula $\chi^2$ no revela qué historia de muestreo se usó.
- Rechazar homogeneidad dice que las mezclas difieren; no dice qué par de
  sitios difiere.
- Los almacenes sintéticos ilustran homogeneidad. No son una afirmación
  sobre ninguna red real de sitios.

## Estructura del paquete

```text
L42_Chi_Cuadrada_Homogeneidad/
|-- README.md
|-- src/
|   |-- homogeneidad_01_tres_muestras.py
|   |-- homogeneidad_02_chi_cuadrada.py
|   `-- homogeneidad_03_limite_historia_muestreo.py
|-- figuras/
|   |-- homogeneidad_01_tres_muestras.png
|   |-- homogeneidad_02_chi_cuadrada.png
|   `-- homogeneidad_03_limite_historia_muestreo.png
|-- notebooks/
|   `-- leccion_42_chi_cuadrada_homogeneidad.ipynb
`-- diapositivas/
    |-- leccion_42.tex
    `-- leccion_42.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L42_Chi_Cuadrada_Homogeneidad/src/homogeneidad_01_tres_muestras.py
uv run es/L42_Chi_Cuadrada_Homogeneidad/src/homogeneidad_02_chi_cuadrada.py
uv run es/L42_Chi_Cuadrada_Homogeneidad/src/homogeneidad_03_limite_historia_muestreo.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L42_Chi_Cuadrada_Homogeneidad/notebooks/leccion_42_chi_cuadrada_homogeneidad.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_42.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_42.tex
```

## Atribución OpenStax

La prueba ji-cuadrada de homogeneidad, la aritmética compartida con el
estadístico de independencia y la historia distinta de muestreo de
poblaciones independientes siguen a Alexander Holmes, Barbara Illowsky y
Susan Dean, *Introductory Business Statistics 2e*, Capítulo 11, Sección
[11.5](https://openstax.org/books/introductory-business-statistics-2e/pages/11-5-test-for-homogeneity).
La práctica complementaria de homogeneidad está en *Introductory Statistics
2e*, Sección
[11.4](https://openstax.org/books/introductory-statistics-2e/pages/11-4-test-for-homogeneity).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

