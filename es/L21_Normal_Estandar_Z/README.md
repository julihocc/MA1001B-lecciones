# Lección 21 - Distribución normal estándar y puntuaciones z

Esta microlección de 50 minutos usa un reloj de puntuación de auditoría
completamente sintético modelado como $\mathrm{Normal}(\mu=50,\sigma=8)$. La
puntuación $z$ $(x-\mu)/\sigma$ localiza una puntuación cruda en la regla
normal estándar. $P(X\le 60)$ iguala $P(Z\le 1.25)$. El paso final muestra que
una comparación de puntuación $z$ requiere forma similar: en un reloj de
retraso sesgado a la derecha, $z=-1$ queda fuera del soporte.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 6, Sección 6.1 (la distribución normal estándar). Práctica
  complementaria: *Introductory Statistics 2e*, Sección 6.1.
- **Prerrequisitos:** Densidad continua y el modelo uniforme de las Lecciones
  19 y 20.
- **Aviso de datos:** Cada puntuación de auditoría, tiempo de retraso y valor
  $z$ es sintético. Los scripts no contienen datos reales de empresas,
  clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Convertir una puntuación cruda en $z=(x-\mu)/\sigma$.
2. Leer $P(Z\le z)$ desde la curva normal estándar.
3. Transferir esa probabilidad de vuelta a $P(X\le x)$ en $N(\mu,\sigma)$.
4. Explicar por qué el sesgo hace que un percentil de puntuación $z$ sea la comparación equivocada.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: una campana de puntuaciones de auditoría | Nombrar $\mu=50$ y $\sigma=8$. |
| 06-16 | Estandarizar $x=60$ | Calcular $z=(60-50)/8=1.25$. |
| 16-24 | Ejecutar el Paso 1 | Confirmar $z=1.250000$. |
| 24-34 | Cola izquierda normal estándar | Bosquejar $P(Z\le 1.25)$. |
| 34-42 | Ejecutar el Paso 2 | Leer $P(Z\le 1.25)=0.894350$. |
| 42-48 | Ejecutar el Paso 3 en un reloj de retraso | Contrastar $0.158655$ con $0.000000$ en $z=-1$. |
| 48-50 | Verificación de conceptos y transición a la Lección 22 | Nombrar límites de especificación como cortes $z$. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye su reloj sintético
con `SEED = 42` y agrega el siguiente concepto sin importar otro script de la
lección. Estos valores provienen de dos ejecuciones coincidentes en el entorno
bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `normal_estandar_01_puntuaciones_z.py` | $z=(x-\mu)/\sigma$ en $N(50,8)$ | $z(60)=1.250000$; $z$ en $\mu\pm\sigma$ iguala $\pm 1.000000$. |
| 2 | `normal_estandar_02_probabilidades_estandar.py` | $P(Z\le 1.25)$ vía `scipy.stats.norm` | $P(Z\le 1.25)=P(X\le 60)=0.894350$, $P(Z>1.25)=0.105650$. |
| 3 | `normal_estandar_03_sesgo_rompe_z.py` | Reloj de retraso sesgado con la misma fórmula $z$ | Retrasos exponenciales: media $=\sigma=20$. $P(Z\le -1)=0.158655$ en la campana frente a $P(X\le 0)=0.000000$ en el reloj de retraso. |

El resultado del Paso 3 es un límite. Una puntuación $z$ es una ubicación en
unidades de desviación estándar, no un percentil portable entre formas. La
Lección 22 usa cortes $z$ como límites de especificación y rendimiento del
proceso.

## Libreta de estudio para estudiantes

La [libreta estudiantil](notebooks/leccion_21_normal_estandar_z.ipynb)
ejecutada es autocontenida y compatible con Google Colab. Reconstruye los tres
pasos de la lección en un único estado acumulativo en memoria, embebe tres
figuras e incluye prácticas editables, respuestas plegables y aserciones para
los valores canónicos. También fue ejecutada desde un directorio temporal
vacío y representada en HTML y Markdown sin leer archivos del repositorio.

## Modelo sintético de puntuación de auditoría

Modelo operativo: $X\sim N(50,8^2)$. La puntuación marcada es $x=60$:

\[
z=\frac{60-50}{8}=1.25,\qquad P(Z\le 1.25)=0.894350.
\]

La misma probabilidad es $P(X\le 60)$ en el reloj crudo. Un segundo reloj
sintético registra retrasos exponenciales con media $20$ minutos, de modo que
$\sigma=20$ y el soporte empieza en $0$. Entonces $z=-1$ corresponde a $x=0$,
que tiene probabilidad $0$, no el valor de campana $0.158655$.

## Conceptos erróneos comunes

- $z$ es una ubicación en unidades de $\sigma$. No es en sí una probabilidad.
- $P(Z\le 1.25)$ y $P(X\le 60)$ coinciden solo después de estandarizar $X$.
- Valores $z$ iguales son comparables solo cuando las formas son similares.
- En un reloj de retraso sesgado a la derecha, $z=-1$ puede situarse en el
  borde del soporte, de modo que el percentil de campana no se transfiere.
- `scipy.stats.norm.cdf` sustituye una tabla $z$ impresa; no cambia el
  significado del área.
- Las puntuaciones sintéticas ilustran la aritmética $z$. No afirman nada
  sobre ninguna auditoría real.

## Estructura del paquete

```text
L21_Normal_Estandar_Z/
|-- README.md
|-- src/
|   |-- normal_estandar_01_puntuaciones_z.py
|   |-- normal_estandar_02_probabilidades_estandar.py
|   `-- normal_estandar_03_sesgo_rompe_z.py
|-- figuras/
|   |-- normal_estandar_01_puntuaciones_z.png
|   |-- normal_estandar_02_probabilidades_estandar.png
|   `-- normal_estandar_03_sesgo_rompe_z.png
|-- notebooks/
|   `-- leccion_21_normal_estandar_z.ipynb
`-- diapositivas/
    |-- leccion_21.tex
    `-- leccion_21.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L21_Normal_Estandar_Z/src/normal_estandar_01_puntuaciones_z.py
uv run es/L21_Normal_Estandar_Z/src/normal_estandar_02_probabilidades_estandar.py
uv run es/L21_Normal_Estandar_Z/src/normal_estandar_03_sesgo_rompe_z.py
```

Ejecutar la libreta estudiantil desde la raíz del repositorio:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  es/L21_Normal_Estandar_Z/notebooks/leccion_21_normal_estandar_z.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_21.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_21.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

La curva normal estándar, las puntuaciones $z$ y las probabilidades de cola
izquierda siguen a Alexander Holmes, Barbara Illowsky y Susan Dean,
*Introductory Business Statistics 2e*, Capítulo 6, Sección
[6.1](https://openstax.org/books/introductory-business-statistics-2e/pages/6-1-the-standard-normal-distribution).
La práctica complementaria de normal estándar está en *Introductory
Statistics 2e*, Sección
[6.1](https://openstax.org/books/introductory-statistics-2e/pages/6-1-the-standard-normal-distribution).
El límite de sesgo prepara las aplicaciones de límites de especificación en
la Lección 22. OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

