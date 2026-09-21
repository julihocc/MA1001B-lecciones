# Lección 29 - Intervalo de confianza para una proporción poblacional

Esta microlección de 50 minutos usa una instantánea de servicio
completamente sintética para estimar una tasa de resolución en primer
contacto. El intervalo de Wald al 95% se construye después de verificar
$n\hat{p}$ y $n(1-\hat{p})$. El paso final muestra que un evento raro con
$x$ pequeña puede empujar el límite inferior de Wald por debajo de 0.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 8, Sección 8.3 (intervalo de confianza para una proporción
  poblacional).
- **Prerrequisitos:** El intervalo z para una media de la Lección 27 y la
  idea de una distribución muestral de $\hat{p}$ de la Lección 25.
- **Aviso de datos:** Cada conteo de tickets es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular $\hat{p}=x/n$ a partir de una instantánea binaria.
2. Verificar $n\hat{p}\ge 5$ y $n(1-\hat{p})\ge 5$ antes de usar la
   aproximación normal.
3. Formar el intervalo de Wald al 95%
   $\hat{p}\pm 1.96\sqrt{\hat{p}(1-\hat{p})/n}$.
4. Explicar por qué un evento raro con $x$ pequeña hace engañoso el
   intervalo de Wald.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: indicador binario de primer contacto | Escribir $\hat{p}=x/n$. |
| 06-16 | Productos éxito-fracaso | Confirmar que $27$ y $123$ superan ambos 5. |
| 16-24 | Ejecutar el Paso 1 | Leer $\hat{p}=0.180000$. |
| 24-34 | Error estándar de $\hat{p}$ | Calcular $0.031369$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $[0.118517, 0.241483]$. |
| 42-48 | Ejecutar el Paso 3 con $x=3$ | Ver límite inferior de Wald $-0.002405$. |
| 48-50 | Verificación de conceptos y transición a la Lección 30 | Nombrar a continuación la planificación del tamaño de muestra. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la instantánea
a partir de constantes con `SEED = 42` reservada y añade el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `prop_ci_01_sample_proportion.py` | $\hat{p}=x/n$ y los dos productos | $x=27$, $n=150$, $\hat{p}=0.180000$, $n\hat{p}=27$, $n(1-\hat{p})=123$. |
| 2 | `prop_ci_02_wald_interval.py` | Intervalo de Wald al 95% después de la verificación | Condiciones satisfechas; EE $=0.031369$; IC $[0.118517, 0.241483]$. |
| 3 | `prop_ci_03_rare_event_wald.py` | $x=3$ rara rompe Wald | $n\hat{p}=3$; Wald $[-0.002405, 0.042405]$; diagnóstico de Wilson $[0.006825, 0.057147]$. |

El resultado del Paso 3 es un límite: una proporción no puede ser negativa,
pero Wald reporta un límite negativo cuando $x$ es pequeña. El intervalo de
Wilson es un contraste diagnóstico, no el procedimiento principal de la
lección.

La [libreta estudiantil ejecutada](notebooks/leccion_29_intervalo_confianza_proporcion.ipynb)
es una guía de estudio autocontenida y compatible con Google Colab. Reconstruye
los tres pasos de la lección en un solo estado acumulativo en memoria, embebe
tres figuras e incluye celdas editables de práctica, respuestas desplegables y
aserciones para los valores canónicos. También se ejecutó desde un directorio
temporal vacío y se renderizó a HTML y Markdown sin leer archivos del
repositorio. La libreta calcula Wilson directamente con su fórmula de
puntuación para reproducir el diagnóstico del script sin una dependencia
exclusiva de `statsmodels`.

## Instantánea sintética de primer contacto

Ejemplo principal: $x=27$ resoluciones en primer contacto en $n=150$
tickets.

\[
\hat{p}=\frac{27}{150}=0.180000,\qquad
\mathrm{EE}=\sqrt{\frac{0.18\times 0.82}{150}}=0.031369,
\]

\[
\hat{p}\pm 1.96\cdot\mathrm{EE}=[0.118517, 0.241483].
\]

Contraste de evento raro: $x=3$, $n=150$, $\hat{p}=0.020000$,
$n\hat{p}=3<5$. El límite inferior de Wald es $-0.002405$.

## Conceptos erróneos comunes

- $\hat{p}$ es un estadístico. El intervalo estima la $p$ poblacional.
- El umbral 5 es una guía para la aproximación normal, no una ley de la
  naturaleza.
- Un intervalo de Wald puede salir de $[0,1]$ cuando $x$ es pequeña.
- Wilson se muestra solo para diagnosticar ese fallo; no se exige para el
  resultado de la lección.
- $n\hat{p}=27$ usa $\hat{p}$, no la $p$ desconocida.
- Los tickets sintéticos ilustran la aritmética de intervalos. No son una
  afirmación sobre ningún mostrador de servicio real.

## Estructura del paquete

```text
L29_Intervalo_Confianza_Proporcion/
|-- README.md
|-- src/
|   |-- prop_ci_01_sample_proportion.py
|   |-- prop_ci_02_wald_interval.py
|   `-- prop_ci_03_rare_event_wald.py
|-- figuras/
|   |-- prop_ci_01_sample_proportion.png
|   |-- prop_ci_02_wald_interval.png
|   `-- prop_ci_03_rare_event_wald.png
|-- notebooks/
|   `-- leccion_29_intervalo_confianza_proporcion.ipynb
`-- diapositivas/
    |-- leccion_29.tex
    `-- leccion_29.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L29_Intervalo_Confianza_Proporcion/src/prop_ci_01_sample_proportion.py
uv run es/L29_Intervalo_Confianza_Proporcion/src/prop_ci_02_wald_interval.py
uv run es/L29_Intervalo_Confianza_Proporcion/src/prop_ci_03_rare_event_wald.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L29_Intervalo_Confianza_Proporcion/notebooks/leccion_29_intervalo_confianza_proporcion.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_29.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_29.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

El intervalo de Wald para una proporción poblacional y la verificación
éxito-fracaso siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Capítulo 8, Sección
[8.3](https://openstax.org/books/introductory-business-statistics-2e/pages/8-3-a-confidence-interval-for-a-population-proportion).
La planificación del tamaño de muestra para un margen de error elegido se
prepara para la Sección
[8.4](https://openstax.org/books/introductory-business-statistics-2e/pages/8-4-calculating-the-sample-size-n-continuous-and-binary-random-variables)
en la Lección 30. OpenStax publica este texto bajo la licencia Creative
Commons Attribution-NonCommercial-ShareAlike. El conjunto sintético, el
código y las figuras de este paquete son materiales originales del curso.

