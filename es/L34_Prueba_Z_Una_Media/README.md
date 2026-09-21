# Lección 34 - Prueba z para una media con varianza conocida

Esta microlección de 50 minutos ejecuta una prueba z unilateral sobre una
muestra de tiempos de entrega completamente sintética. Con $n=40$ y
$\sigma=6$ conocida, el estadístico es $z=(\bar{x}-80)/(\sigma/\sqrt{n})$ y
el valor $p$ es la cola superior de la normal estándar. El paso final muestra
que una $\sigma$ conocida rara vez es verdadera en datos de operaciones.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 9, Secciones 9.3 y 9.4 (distribución necesaria para pruebas;
  ejemplos completos de pruebas de hipótesis).
- **Prerrequisitos:** Lenguaje de pruebas de la Lección 33 y el intervalo z
  con sigma conocida de la Lección 27.
- **Aviso de datos:** Cada tiempo de entrega es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Calcular $z=(\bar{x}-\mu_{0})/(\sigma/\sqrt{n})$ cuando $\sigma$ es conocida.
2. Obtener el valor $p$ de cola superior de la normal estándar.
3. Decidir con $\alpha=0.05$ comparando $p$ con $\alpha$.
4. Explicar por qué una prueba z con $\sigma$ conocida rara vez es la
   herramienta correcta en operaciones.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: $H_{0}:\mu=80$ frente a $H_{1}:\mu>80$ | Escribir la fórmula z. |
| 06-16 | $\sigma=6$ conocida, $n=40$ | Confirmar $\mathrm{EE}=0.948683$. |
| 16-24 | Ejecutar el Paso 1 | Leer $\bar{x}=82.229590$ y $z=2.350194$. |
| 24-34 | Valor $p$ de cola superior | Sombrear $P(Z\ge z)$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $p=0.009382$ y rechazar $H_{0}$. |
| 42-48 | Ejecutar el Paso 3 con $s$ en lugar de $\sigma$ | Ver que $p$ cae a $0.002215$. |
| 48-50 | Verificación de conceptos y paso a la Lección 35 | Nombrar la prueba $t$ de una muestra. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye las mismas
entregas sintéticas con `SEED = 42` y no importa otro script de la lección.
Estos valores provienen de dos ejecuciones coincidentes en el entorno
bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `prueba_z_media_01_estadistico_z.py` | Estadístico $z$ con $\sigma$ conocida | $n=40$, $\sigma=6$, $\bar{x}=82.229590$, $\mathrm{EE}=0.948683$, $z=2.350194$. |
| 2 | `prueba_z_media_02_valor_p.py` | Valor $p$ de cola superior y decisión | $p=0.009382<\alpha=0.05$; rechazar $H_{0}$. |
| 3 | `prueba_z_media_03_limite_sigma_conocida.py` | $s$ no es $\sigma$ | $s=4.955099$; z inválido con $s$ da $z=2.845789$ y $p=0.002215$. |

El resultado del Paso 3 es un límite: los datos de operaciones casi nunca
llegan con una $\sigma$ poblacional conocida. Conservar una curva de
referencia z después de reemplazar $\sigma$ por $s$ es la prueba incorrecta.
La Lección 35 usa $t$ con $\mathrm{gl}=n-1$.

## Muestra sintética de entregas

El analista trata $\sigma=6$ minutos como conocida y prueba $H_{0}:\mu=80$
frente a $H_{1}:\mu>80$. Los scripts generan $n=40$ tiempos iid $N(82,6)$
solo para que se pueda verificar la media oculta.

\[
z=\frac{82.229590-80}{6/\sqrt{40}}=\frac{2.229590}{0.948683}=2.350194,
\]

\[
p=P(Z\ge 2.350194)=0.009382.
\]

La desviación estándar muestral de los mismos 40 tiempos es $s=4.955099\neq 6$.

## Conceptos erróneos comunes

- El valor $p$ no es la probabilidad de que $H_{0}$ sea verdadera.
- Un valor $p$ pequeño es evidencia contra $H_{0}$, no una prueba del valor
  exacto de la alternativa.
- $s$ es un estadístico. No autoriza la curva de referencia z.
- Una $\sigma$ conocida es un supuesto de modelado, no un hecho típico de
  operaciones.
- Las entregas sintéticas ilustran la aritmética z. No afirman nada sobre
  ningún proceso real de última milla.

## Estructura del paquete

```text
L34_Prueba_Z_Una_Media/
|-- README.md
|-- src/
|   |-- prueba_z_media_01_estadistico_z.py
|   |-- prueba_z_media_02_valor_p.py
|   `-- prueba_z_media_03_limite_sigma_conocida.py
|-- figuras/
|   |-- prueba_z_media_01_estadistico_z.png
|   |-- prueba_z_media_02_valor_p.png
|   `-- prueba_z_media_03_limite_sigma_conocida.png
|-- notebooks/
|   `-- leccion_34_prueba_z_una_media.ipynb
`-- diapositivas/
    |-- leccion_34.tex
    `-- leccion_34.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L34_Prueba_Z_Una_Media/src/prueba_z_media_01_estadistico_z.py
uv run es/L34_Prueba_Z_Una_Media/src/prueba_z_media_02_valor_p.py
uv run es/L34_Prueba_Z_Una_Media/src/prueba_z_media_03_limite_sigma_conocida.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L34_Prueba_Z_Una_Media/notebooks/leccion_34_prueba_z_una_media.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_34.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_34.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La prueba z para una media con varianza conocida, el estadístico de prueba y
la decisión por valor $p$ siguen a Alexander Holmes, Barbara Illowsky y Susan
Dean, *Introductory Business Statistics 2e*, Capítulo 9, Secciones
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-distribution-needed-for-hypothesis-testing)
y
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples).
La prueba $t$ con $\sigma$ desconocida es la continuación natural en la
Lección 35. OpenStax publica el texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

