# Lección 40 - Bondad de ajuste ji-cuadrada

Esta microlección de 50 minutos usa una mezcla de tickets de soporte
completamente sintética para contrastar participaciones hipotéticas $0.40$,
$0.30$, $0.20$ y $0.10$. Los conteos esperados son $np$, el estadístico es
$\chi^2=\sum(O-E)^2/E$ y $df=3$. El paso final muestra que un conteo
esperado menor que 5 convierte la aproximación ji-cuadrada en una mala
herramienta de decisión.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 11, Sección 11.3 (prueba de bondad de ajuste).
- **Prerrequisitos:** Pruebas $z$ de una y dos proporciones de las Lecciones
  36 y 39.
- **Aviso de datos:** Cada conteo de tickets es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Convertir participaciones hipotéticas de categoría en conteos esperados
   $E=np$.
2. Calcular $\chi^2=\sum(O-E)^2/E$ con $df=k-1$.
3. Leer un p-valor de cola derecha y decidir a $\alpha=0.05$.
4. Explicar por qué un conteo esperado menor que 5 debilita la aproximación.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: una mezcla de cuatro canales afirmada | Escribir $H_0:$ participaciones $=(0.40,0.30,0.20,0.10)$. |
| 06-16 | Observados frente a $E=np$ | Confirmar esperados $80$, $60$, $40$, $20$. |
| 16-24 | Ejecutar el Paso 1 | Leer $E$ mínimo $=20$ y la verificación $E\ge 5$. |
| 24-34 | Contribuciones celulares y $df=3$ | Calcular $(100-80)^2/80=5$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $\chi^2=9.166667$, $p=0.027155$, rechazar $H_0$. |
| 42-48 | Ejecutar el Paso 3 | Ver $E=4$ y $E=2$; un ticket mueve un término de $2.000$ a $0.500$. |
| 48-50 | Verificación de conceptos y transición a la Lección 41 | Nombrar la siguiente herramienta: prueba de independencia ji-cuadrada. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma mezcla
sintética de tickets sin importar otro script de la lección. Estos valores
provienen de dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `bondad_ajuste_01_observados_esperados.py` | Observados frente a $E=np$ | $n=200$; observados $100,50,30,20$; esperados $80,60,40,20$; todos $E\ge 5$. |
| 2 | `bondad_ajuste_02_chi_cuadrada.py` | $\chi^2$, $df=3$, $p$ de cola derecha | Contribuciones $5.000000$, $1.666667$, $2.500000$, $0.000000$; $\chi^2=9.166667$; $p=0.027155$; $\chi^{2*}=7.814728$; rechazar $H_0$. |
| 3 | `bondad_ajuste_03_limite_esperados_pequenos.py` | Límite $E<5$ | $n=20$; observados $14,4,2,0$; esperados $8,6,4,2$; dos celdas con $E<5$. Contribución App $2.000000$ si $O=0$ frente a $0.500000$ si $O=1$. |

El resultado del Paso 3 es un límite, no una segunda afirmación GOF. La
tabla $n=20$ tiene conteos esperados $4$ y $2$, de modo que el p-valor
ji-cuadrada no es una entrada estable de decisión. La Lección 41 usa una
tabla de doble entrada en lugar de una mezcla hipotética.

## Mezcla sintética de tickets

\[
\chi^2=\frac{(100-80)^2}{80}+\frac{(50-60)^2}{60}+\frac{(30-40)^2}{40}+\frac{(20-20)^2}{20}
=9.166667,
\]

con $df=4-1=3$ y $p=0.027155$. La tabla $n=200$ cumple $E\ge 5$. El
seguimiento $n=20$ no: Correo tiene $E=4$ y App tiene $E=2$, con un conteo
observado de App igual a $0$.

## Conceptos erróneos comunes

- Los conteos esperados son $np$ bajo $H_0$, no las participaciones
  muestrales observadas.
- La bondad de ajuste es de cola derecha: un $\chi^2$ grande es evidencia
  contra $H_0$.
- $df=k-1$ para $k$ categorías con probabilidades completamente
  especificadas.
- Una celda con $E<5$ ya es una advertencia, aunque el software siga
  imprimiendo $p$.
- Los tickets sintéticos ilustran GOF. No son una afirmación sobre ningún
  mostrador de soporte real.

## Estructura del paquete

```text
L40_Chi_Cuadrada_Bondad_Ajuste/
|-- README.md
|-- src/
|   |-- bondad_ajuste_01_observados_esperados.py
|   |-- bondad_ajuste_02_chi_cuadrada.py
|   `-- bondad_ajuste_03_limite_esperados_pequenos.py
|-- figuras/
|   |-- bondad_ajuste_01_observados_esperados.png
|   |-- bondad_ajuste_02_chi_cuadrada.png
|   `-- bondad_ajuste_03_limite_esperados_pequenos.png
|-- notebooks/
|   `-- leccion_40_chi_cuadrada_bondad_ajuste.ipynb
`-- diapositivas/
    |-- leccion_40.tex
    `-- leccion_40.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L40_Chi_Cuadrada_Bondad_Ajuste/src/bondad_ajuste_01_observados_esperados.py
uv run es/L40_Chi_Cuadrada_Bondad_Ajuste/src/bondad_ajuste_02_chi_cuadrada.py
uv run es/L40_Chi_Cuadrada_Bondad_Ajuste/src/bondad_ajuste_03_limite_esperados_pequenos.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L40_Chi_Cuadrada_Bondad_Ajuste/notebooks/leccion_40_chi_cuadrada_bondad_ajuste.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_40.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_40.tex
```

## Atribución OpenStax

El estadístico de bondad de ajuste ji-cuadrada, $df=k-1$, la guía de
conteos esperados y la decisión de cola derecha siguen a Alexander Holmes,
Barbara Illowsky y Susan Dean, *Introductory Business Statistics 2e*,
Capítulo 11, Sección
[11.3](https://openstax.org/books/introductory-business-statistics-2e/pages/11-3-goodness-of-fit-test).
La práctica complementaria de GOF está en *Introductory Statistics 2e*,
Sección
[11.2](https://openstax.org/books/introductory-statistics-2e/pages/11-2-goodness-of-fit-test).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

