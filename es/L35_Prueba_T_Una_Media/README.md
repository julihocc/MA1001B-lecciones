# Lección 35 - Prueba t para una media con varianza desconocida

Esta microlección de 50 minutos usa un registro de empaque de salida
completamente sintético para reemplazar una prueba z con sigma conocida por
la t de Student. La desviación estándar muestral s entra en el error
estándar, la curva de referencia tiene gl = n - 1, y la decisión usa un
valor p bilateral. El paso final muestra que n = 8 más sesgo a la derecha
hace frágil ese valor p.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 9, Secciones 9.3 (qué distribución) y 9.4 (ejemplos completos de
  pruebas de hipótesis). Compañero: *Introductory Statistics 2e*, Sección 9.4.
- **Prerrequisitos:** Lenguaje de pruebas de la Lección 33 y la prueba z con
  sigma conocida de la Lección 34.
- **Aviso de datos:** Cada tiempo de empaque es sintético. Los scripts no
  contienen datos reales de empresas, clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar $H_0:\mu=50$ frente a $H_1:\mu\neq 50$ cuando $\sigma$ es
   desconocida.
2. Calcular $t=(\bar{x}-\mu_0)/(s/\sqrt{n})$ e identificar $gl=n-1$.
3. Obtener un valor p bilateral de la t de Student y decidir con
   $\alpha=0.05$.
4. Explicar por qué una muestra pequeña y sesgada hace inestable el valor p
   de t.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: sigma ya no se da | Escribir $H_0$ y $H_1$ para un reclamo de 50 minutos. |
| 06-16 | Media muestral, s y EE | Contrastar $s/\sqrt{n}$ con un EE de sigma conocida. |
| 16-24 | Ejecutar el Paso 1 | Leer $\bar{x}=52.229590$, $s=4.955099$, $t=2.845789$. |
| 24-34 | Cola t bilateral | Sombrear ambas colas y nombrar $gl=39$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $p=0.007026$ y rechazar $H_0$. |
| 42-48 | Ejecutar el Paso 3 | Contrastar $p=0.767485$ con $p=0.081584$ al omitir un retraso. |
| 48-50 | Verificación de conceptos y paso a la Lección 36 | Nombrar la siguiente herramienta: una prueba para una proporción. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo registro
sintético con `SEED = 42` y no importa otro script de la lección. Estos
valores provienen de dos ejecuciones coincidentes en el entorno bloqueado de
`uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `prueba_t_media_01_error_estandar_muestral.py` | s muestral, EE, estadístico t, $gl=n-1$ | $n=40$, $\bar{x}=52.229590$, $s=4.955099$, $EE=0.783470$, $gl=39$, $t=2.845789$. |
| 2 | `prueba_t_media_02_valor_p_bilateral.py` | Valor p bilateral y $t^*$ | $p$ manual y scipy $=0.007026$; $t^*=2.022691$; rechazar $H_0$ con $\alpha=0.05$. |
| 3 | `prueba_t_media_03_limite_n_pequena_sesgo.py` | n pequeña más sesgo | $n=8$: sesgo $=1.935033$, Shapiro-Wilk $p=0.001286$, $t=0.307397$, $p$ bilateral $=0.767485$. Omitir el retraso de 83.174379 minutos y $p$ cae a $0.081584$. El valor p de $n=40$ se mantiene entre $0.001481$ y $0.013087$. |

El resultado del Paso 3 es un límite, no una prueba nueva. Con $n=8$ y una
cola derecha larga, una observación mueve el valor p en un orden de
magnitud. La Lección 36 deja las medias y prueba una proporción de negocio.

## Registro sintético de empaque de salida

El estándar de servicio hipotético es $\mu_0=50$ minutos. La muestra $n=40$
se extrae de un generador Normal$(52,6)$ para que la historia de sigma
desconocida continúe el escenario de sigma conocida de la Lección 34.

\[
t=\frac{\bar{x}-\mu_0}{s/\sqrt{n}}=\frac{52.229590-50}{0.783470}=2.845789,
\]

\[
p=2P(T_{39}\ge 2.845789)=0.007026.
\]

Como $|t|>t^*=2.022691$ y $p<\alpha=0.05$, la prueba bilateral rechaza
$H_0:\mu=50$. El seguimiento $n=8$ es un sorteo distinto: siete empaques
típicos más un retraso largo. Esa muestra está sesgada a la derecha, falla
una comprobación Shapiro-Wilk y no sostiene la misma decisión estable.

## Conceptos erróneos comunes

- Una $\sigma$ desconocida no autoriza a seguir usando $z$ con $s$ en lugar
  de $\sigma$ sin cambiar la curva de referencia.
- Un valor p bilateral cuenta ambas colas, aunque $\bar{x}$ esté de un lado.
- No rechazar $H_0$ en la muestra $n=8$ no prueba que $\mu=50$.
- Un solo retraso largo puede inflar $s$, encoger $|t|$ y mover $p$ con
  fuerza.
- Los tiempos de empaque sintéticos ilustran el procedimiento t. No afirman
  nada sobre ninguna línea real de cumplimiento.

## Estructura del paquete

```text
L35_Prueba_T_Una_Media/
|-- README.md
|-- src/
|   |-- prueba_t_media_01_error_estandar_muestral.py
|   |-- prueba_t_media_02_valor_p_bilateral.py
|   `-- prueba_t_media_03_limite_n_pequena_sesgo.py
|-- figuras/
|   |-- prueba_t_media_01_error_estandar_muestral.png
|   |-- prueba_t_media_02_valor_p_bilateral.png
|   `-- prueba_t_media_03_limite_n_pequena_sesgo.png
|-- notebooks/
|   `-- leccion_35_prueba_t_una_media.ipynb
`-- diapositivas/
    |-- leccion_35.tex
    `-- leccion_35.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L35_Prueba_T_Una_Media/src/prueba_t_media_01_error_estandar_muestral.py
uv run es/L35_Prueba_T_Una_Media/src/prueba_t_media_02_valor_p_bilateral.py
uv run es/L35_Prueba_T_Una_Media/src/prueba_t_media_03_limite_n_pequena_sesgo.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L35_Prueba_T_Una_Media/notebooks/leccion_35_prueba_t_una_media.ipynb
```

La libreta estudiantil ejecutada es autocontenida y compatible con Google
Colab. Integra los tres pasos de la lección en un solo estado acumulativo en
memoria, embebe tres figuras editables y no requiere archivos del repositorio,
descargas ni conjuntos de datos externos.

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_35.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_35.tex
```

El PDF compilado contiene las ocho diapositivas centrales y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La prueba t de una muestra cuando $\sigma$ es desconocida, el estadístico
$t$, los grados de libertad $n-1$ y las decisiones bilaterales siguen a
Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory Business
Statistics 2e*, Capítulo 9, Secciones
[9.3](https://openstax.org/books/introductory-business-statistics-2e/pages/9-3-probability-distribution-needed-for-hypothesis-testing)
y
[9.4](https://openstax.org/books/introductory-business-statistics-2e/pages/9-4-full-hypothesis-test-examples).
Práctica compañera de t de una media está en *Introductory Statistics 2e*,
Sección
[9.4](https://openstax.org/books/introductory-statistics-2e/pages/9-4-full-hypothesis-test-examples).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

