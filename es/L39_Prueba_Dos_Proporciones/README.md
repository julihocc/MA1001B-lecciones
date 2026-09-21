# Lección 39 - Dos proporciones en pruebas A/B

Esta microlección de 50 minutos usa una prueba A/B de pago completamente
sintética con $n_A=400$, $x_A=72$, $n_B=410$ y $x_B=61$. Un estadístico $z$
combinado contrasta $H_0:p_A=p_B$. El paso final muestra que espiar
p-valores en cuatro miradas interinas infla el error tipo I por encima de
$\alpha=0.05$.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 10, Sección 10.4 (comparación de dos proporciones poblacionales
  independientes).
- **Prerrequisitos:** $z$ de una proporción de la Lección 36 y dos medias
  independientes de la Lección 37.
- **Aviso de datos:** Cada visitante y cada indicador de conversión es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular dos tasas muestrales de conversión y su diferencia.
2. Formar la proporción combinada y el EE de $\hat{p}_A-\hat{p}_B$ bajo $H_0$.
3. Ejecutar una prueba $z$ bilateral para dos proporciones independientes.
4. Explicar por qué espiar p-valores a mitad del experimento infla el error
   tipo I.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Pregunta inicial: dos tasas de conversión independientes | Escribir $H_0:p_A=p_B$. |
| 06-16 | Tasas muestrales y $\hat{p}$ combinada | Confirmar $72/400=0.18$ y $61/410$. |
| 16-24 | Ejecutar el Paso 1 | Leer $\hat{p}_A=0.180000$, $\hat{p}_B=0.148780$, $p_{\text{comb}}=0.164198$. |
| 24-34 | EE combinado y $z$ | Escribir $\sqrt{\hat{p}(1-\hat{p})(1/n_A+1/n_B)}$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $z=1.199141$, $p=0.230473$, no rechazar $H_0$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar tipo I $0.047250$ con tipo I al espiar $0.124250$. |
| 48-50 | Verificación de conceptos y transición a la Lección 40 | Nombrar la siguiente herramienta: bondad de ajuste ji-cuadrada. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye los mismos
conteos A/B sintéticos (y, en el Paso 3, la misma simulación con semilla 42)
sin importar otro script de la lección. Estos valores provienen de dos
ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `dos_proporciones_01_tasas_muestrales.py` | Dos tasas y $\hat{p}$ combinada | $\hat{p}_A=0.180000$, $\hat{p}_B=0.148780$, diferencia $0.031220$, $p_{\text{comb}}=0.164198$. |
| 2 | `dos_proporciones_02_z_combinada.py` | $z$ combinada para $p_A-p_B$ | $EE=0.026035$, $z=1.199141$, $p=0.230473$, $z^*=1.959964$, no rechazar $H_0$. |
| 3 | `dos_proporciones_03_limite_espiar.py` | Espiar infla el error tipo I | 8000 experimentos nulos; una prueba final tipo I $=0.047250$; cuatro miradas tipo I $=0.124250$. |

El resultado del Paso 3 es un límite, no una receta de diseño secuencial.
Una prueba planeada con $\alpha=0.05$ usa una sola mirada en los $n_A$ y
$n_B$ finales. La Lección 40 pasa de dos proporciones a un ajuste
ji-cuadrada de más de dos categorías.

## Registro A/B sintético

\[
\hat{p}_A=\frac{72}{400}=0.18,\qquad
\hat{p}_B=\frac{61}{410}=0.148780,
\]

\[
\hat{p}=\frac{72+61}{810}=0.164198,\qquad
z=\frac{0.180000-0.148780}{0.026035}=1.199141.
\]

El p-valor bilateral es $0.230473$, de modo que la prueba no rechaza
$H_0:p_A=p_B$ a $\alpha=0.05$. Bajo una tasa nula compartida de $0.16$,
cuatro miradas interinas elevan la tasa de falsos positivos de $0.047250$ a
$0.124250$.

## Conceptos erróneos comunes

- Dos tasas de conversión son muestras independientes, no visitantes
  pareados.
- El EE de la prueba usa la $\hat{p}$ combinada bajo $H_0:p_A=p_B$, no dos
  EE de Wald sumados después sin combinar.
- Un resultado A/B no significativo no prueba que las versiones sean
  idénticas.
- Revisar $p$ tras cada actualización del tablero no es el mismo
  experimento que una prueba planeada.
- Los indicadores sintéticos de pago ilustran $z$ de dos proporciones. No
  afirman nada sobre ningún cambio real de producto.

## Estructura del paquete

```text
L39_Prueba_Dos_Proporciones/
|-- README.md
|-- src/
|   |-- dos_proporciones_01_tasas_muestrales.py
|   |-- dos_proporciones_02_z_combinada.py
|   `-- dos_proporciones_03_limite_espiar.py
|-- figuras/
|   |-- dos_proporciones_01_tasas_muestrales.png
|   |-- dos_proporciones_02_z_combinada.png
|   `-- dos_proporciones_03_limite_espiar.png
|-- notebooks/
|   `-- leccion_39_prueba_dos_proporciones.ipynb
`-- diapositivas/
    |-- leccion_39.tex
    `-- leccion_39.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L39_Prueba_Dos_Proporciones/src/dos_proporciones_01_tasas_muestrales.py
uv run es/L39_Prueba_Dos_Proporciones/src/dos_proporciones_02_z_combinada.py
uv run es/L39_Prueba_Dos_Proporciones/src/dos_proporciones_03_limite_espiar.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L39_Prueba_Dos_Proporciones/notebooks/leccion_39_prueba_dos_proporciones.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_39.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_39.tex
```

## Atribución OpenStax

La prueba $z$ de dos proporciones, la proporción estimada combinada y las
muestras independientes para $p_A-p_B$ siguen a Alexander Holmes, Barbara
Illowsky y Susan Dean, *Introductory Business Statistics 2e*, Capítulo 10,
Sección
[10.4](https://openstax.org/books/introductory-business-statistics-2e/pages/10-4-comparing-two-independent-population-proportions).
La práctica complementaria de dos proporciones está en *Introductory
Statistics 2e*, Sección
[10.3](https://openstax.org/books/introductory-statistics-2e/pages/10-3-comparing-two-independent-population-proportions).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

