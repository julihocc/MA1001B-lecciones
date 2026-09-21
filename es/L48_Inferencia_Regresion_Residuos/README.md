# Lección 48 - Inferencia de regresión, diagnósticos de residuos y decisiones

Esta microlección de 50 minutos usa una muestra sintética de un centro de
correo: 39 semanas ordinarias de horas extra más un fin de semana de
emergencia en $(48,\ 42)$. Los estudiantes contrastan $H_0:\beta_1=0$,
leen una gráfica de residuos y luego ven que la pendiente significativa
desaparece al quitar el punto influyente.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Secciones 13.2 y 13.6 (significancia de la asociación lineal y
  predicción a partir de una ecuación de regresión).
- **Prerrequisitos:** Mínimos cuadrados y $R^2$ de la Lección 47.
- **Aviso de datos:** Cada semana, hora extra y conteo de unidades es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular $EE(b_1)$, el estadístico $t$ y un $p$-valor bilateral para
   $H_0:\beta_1=0$.
2. Dibujar residuo frente a valores ajustados y localizar una semana
   inusual.
3. Reajustar la recta tras eliminar el punto influyente.
4. Explicar por qué un punto puede crear una pendiente significativa que
   no es una decisión sobre operaciones ordinarias.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: 39 semanas ordinarias más un fin de semana de emergencia | Marcar $(48,\ 42)$ en un esbozo. |
| 06-16 | $EE(b_1)$ y $t=b_1/EE(b_1)$ | Enunciar $H_0:\beta_1=0$. |
| 16-24 | Ejecutar el Paso 1 | Leer $t=5.991932$, $p=5.839701\times10^{-7}$. |
| 24-34 | Residuo frente a ajustado | Encontrar el residuo más grande. |
| 34-42 | Ejecutar el Paso 2 | Obtener residuo de emergencia $8.570594$. |
| 42-48 | Ejecutar el Paso 3 y el límite de influencia | Contrastar $p=0.291492$ tras la eliminación. |
| 48-50 | Verificación de conceptos | Rechazar tratar la pendiente $n=40$ como política de semanas ordinarias. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma
muestra sintética de 40 semanas con `SEED = 42` y añade el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `inferencia_regresion_01_pendiente_ee_t.py` | $EE(b_1)$ y prueba $t$ de $H_0:\beta_1=0$ | $n=40$; $b_1=0.434381$; $EE=0.072494$; $t=5.991932$; $p=5.839701\times10^{-7}$; rechazar $H_0$. |
| 2 | `inferencia_regresion_02_grafica_residuos.py` | Residuo frente a ajustado | Media residual $0.000000$; DE $3.140288$; residuo de emergencia $8.570594$ (el más grande). |
| 3 | `inferencia_regresion_03_punto_influyente.py` | La pendiente desaparece sin el punto | Sin el fin de semana: $n=39$, $b_1=0.088445$, $t=1.070131$, $p=0.291492$, $R^2=0.030022$; no rechazar $H_0$. |

El resultado del Paso 3 es el límite. El fin de semana de emergencia no es
una semana extra típica. Una pendiente significativa $n=40$ no es una
decisión sobre operaciones ordinarias.

## Tabla sintética de inferencia

Las 40 semanas:

\[
t=\frac{0.434381}{0.072494}=5.991932,\qquad gl=38,\qquad p=5.839701\times10^{-7}.
\]

Tras eliminar el fin de semana de emergencia:

\[
t=\frac{0.088445}{0.082649}=1.070131,\qquad p=0.291492.
\]

$R^2$ cae de $0.485814$ a $0.030022$. La asociación era el punto.

## Conceptos erróneos comunes

- Un $p$-valor pequeño no es robusto a una semana de alto apalancamiento.
- Media residual 0 es una identidad de mínimos cuadrados, no un aprobado
  diagnóstico.
- Eliminar un punto es un chequeo de sensibilidad, no una licencia para
  descartar datos incómodos en operaciones.
- El centro de correo sintético ilustra influencia. No es una afirmación
  sobre ningún almacén real.

## Estructura del paquete

```text
L48_Inferencia_Regresion_Residuos/
|-- README.md
|-- src/
|   |-- inferencia_regresion_01_pendiente_ee_t.py
|   |-- inferencia_regresion_02_grafica_residuos.py
|   `-- inferencia_regresion_03_punto_influyente.py
|-- figuras/
|   |-- inferencia_regresion_01_pendiente_ee_t.png
|   |-- inferencia_regresion_02_grafica_residuos.png
|   `-- inferencia_regresion_03_punto_influyente.png
|-- notebooks/
|   `-- leccion_48_inferencia_regresion_residuos.ipynb
`-- diapositivas/
    |-- leccion_48.tex
    `-- leccion_48.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L48_Inferencia_Regresion_Residuos/src/inferencia_regresion_01_pendiente_ee_t.py
uv run es/L48_Inferencia_Regresion_Residuos/src/inferencia_regresion_02_grafica_residuos.py
uv run es/L48_Inferencia_Regresion_Residuos/src/inferencia_regresion_03_punto_influyente.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L48_Inferencia_Regresion_Residuos/notebooks/leccion_48_inferencia_regresion_residuos.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_48.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_48.tex
```

## Atribución OpenStax

Contrastar la significancia de una asociación lineal, el pensamiento de
residuos y la predicción a partir de una recta ajustada siguen a Alexander
Holmes, Barbara Illowsky y Susan Dean, *Introductory Business Statistics
2e*, Secciones
[13.2](https://openstax.org/books/introductory-business-statistics-2e/pages/13-2-testing-the-significance-of-the-correlation-coefficient)
y
[13.6](https://openstax.org/books/introductory-business-statistics-2e/pages/13-6-predicting-with-a-regression-equation).
OpenStax publica este texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

