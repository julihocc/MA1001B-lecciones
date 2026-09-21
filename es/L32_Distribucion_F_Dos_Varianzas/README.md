# Lección 32 - Distribución F y comparación de dos varianzas

Esta microlección de 50 minutos compara dos estaciones de empaque
completamente sintéticas mediante la razón $F=s_{1}^{2}/s_{2}^{2}$. La
probabilidad de cola superior proviene de `scipy.stats.f.sf`. El paso final
muestra que la prueba $F$ de dos varianzas es sensible a la no normalidad:
muestras $t(3)$ de varianza igual inflan la tasa de tipo I.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 12, Sección 12.1 (prueba de dos varianzas).
- **Prerrequisitos:** Un intervalo chi-cuadrada de una sola varianza de la
  Lección 31.
- **Aviso de datos:** Cada tiempo de ciclo es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular dos varianzas muestrales independientes $s_{1}^{2}$ y $s_{2}^{2}$.
2. Formar $F=s_{1}^{2}/s_{2}^{2}$ con $\mathrm{gl}_{1}=n_{1}-1$ y
   $\mathrm{gl}_{2}=n_{2}-1$.
3. Leer el valor $p$ de cola superior de la distribución $F$.
4. Explicar por qué la prueba $F$ de dos varianzas es sensible a la no
   normalidad.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: dos estaciones independientes | Nombrar dos varianzas muestrales. |
| 06-16 | Par de grados de libertad | Confirmar $(24,24)$. |
| 16-24 | Ejecutar el Paso 1 | Leer $s_{1}^{2}=44.205731$ y $s_{2}^{2}=12.024693$. |
| 24-34 | Razón $F$ | Calcular $3.676246$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $p=0.001125$ y rechazar $H_{0}$. |
| 42-48 | Ejecutar el Paso 3 de tipo I | Contrastar $0.052200$ con $0.202400$. |
| 48-50 | Verificación de conceptos y paso a la Lección 33 | Nombrar hipótesis y tipos de error. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye las muestras de
estación con `SEED = 42` y no importa otro script de la lección. Estos
valores provienen de dos ejecuciones coincidentes en el entorno bloqueado de
`uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `f_dos_var_01_varianzas_muestrales.py` | Dos varianzas muestrales | $n_{1}=n_{2}=25$; $s_{1}^{2}=44.205731$; $s_{2}^{2}=12.024693$. |
| 2 | `f_dos_var_02_prueba_f.py` | $F$ y `f.sf` | $F=3.676246$; $F_{0.05}=1.983760$; $p=0.001125$; rechazar $H_{0}$. |
| 3 | `f_dos_var_03_sensibilidad_no_normal.py` | Tipo I bajo colas pesadas | Tipo I normal $=0.052200$; tipo I $t(3)=0.202400$ (5000 reps). |

El resultado del Paso 3 es un límite: varianzas iguales más colas pesadas
hacen que la prueba $F$ rechace con demasiada frecuencia.

## Muestra sintética de dos estaciones

La estación A se genera de $N(40,8)$ y la estación B de $N(40,5)$, cada una
con $n=25$. La prueba es $H_{0}:\sigma_{1}^{2}=\sigma_{2}^{2}$ frente a
$H_{1}:\sigma_{1}^{2}>\sigma_{2}^{2}$.

\[
F=\frac{s_{1}^{2}}{s_{2}^{2}}=\frac{44.205731}{12.024693}=3.676246,
\]

\[
p=P(F_{24,24}\ge 3.676246)=0.001125.
\]

Bajo varianzas iguales, 5000 replicaciones normales rechazan a tasa
$0.052200$, cerca de $\alpha=0.05$. Replicaciones $t(3)$ de varianza igual
rechazan a $0.202400$.

## Conceptos erróneos comunes

- $F$ compara varianzas, no medias.
- Las dos muestras deben ser independientes.
- Un valor $p$ pequeño no es un enunciado sobre cuál estación es más rápida.
- La prueba $F$ no es robusta a colas pesadas como algunas pruebas de media.
- Las estaciones sintéticas ilustran la aritmética $F$. No afirman nada
  sobre ninguna línea de empaque real.

## Estructura del paquete

```text
L32_Distribucion_F_Dos_Varianzas/
|-- README.md
|-- src/
|   |-- f_dos_var_01_varianzas_muestrales.py
|   |-- f_dos_var_02_prueba_f.py
|   `-- f_dos_var_03_sensibilidad_no_normal.py
|-- figuras/
|   |-- f_dos_var_01_varianzas_muestrales.png
|   |-- f_dos_var_02_prueba_f.png
|   `-- f_dos_var_03_sensibilidad_no_normal.png
|-- notebooks/
|   `-- leccion_32_distribucion_f_dos_varianzas.ipynb
`-- diapositivas/
    |-- leccion_32.tex
    `-- leccion_32.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L32_Distribucion_F_Dos_Varianzas/src/f_dos_var_01_varianzas_muestrales.py
uv run es/L32_Distribucion_F_Dos_Varianzas/src/f_dos_var_02_prueba_f.py
uv run es/L32_Distribucion_F_Dos_Varianzas/src/f_dos_var_03_sensibilidad_no_normal.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L32_Distribucion_F_Dos_Varianzas/notebooks/leccion_32_distribucion_f_dos_varianzas.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_32.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_32.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La prueba $F$ de dos varianzas sigue a Alexander Holmes, Barbara Illowsky y
Susan Dean, *Introductory Business Statistics 2e*, Capítulo 12, Sección
[12.1](https://openstax.org/books/introductory-business-statistics-2e/pages/12-1-test-of-two-variances).
El lenguaje de pruebas de hipótesis ($H_{0}$, $H_{1}$, errores de tipo I y
tipo II) se prepara para el Capítulo 9, Secciones
[9.1](https://openstax.org/books/introductory-business-statistics-2e/pages/9-1-null-and-alternative-hypotheses)
y
[9.2](https://openstax.org/books/introductory-business-statistics-2e/pages/9-2-outcomes-and-the-type-i-and-type-ii-errors)
en la Lección 33. OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

