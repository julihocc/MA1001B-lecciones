# Lección 19 - Variables aleatorias continuas: densidad y probabilidad de intervalo

Esta microlección de 50 minutos usa un reloj de tiempo de servicio de mesa de
ayuda completamente sintético para introducir una densidad continua en
$[2, 14]$ minutos. La probabilidad es área bajo la curva, no una altura
puntual. El paso final muestra que $P(X=c)=0$ para cada minuto individual $c$,
incluida la moda.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Capítulo 5, Sección 5.1 (funciones de probabilidad continuas). Práctica
  complementaria: *Introductory Statistics 2e*, Sección 5.1.
- **Prerrequisitos:** Variables aleatorias discretas, FMP y $E[X]$ de las
  Lecciones 13 a 18.
- **Aviso de datos:** Cada tiempo de servicio, densidad y probabilidad de
  intervalo es sintético. Los scripts no contienen datos reales de empresas,
  clientes o socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Distinguir una densidad continua $f(x)$ de una FMP discreta.
2. Leer $P(a<X<b)$ como el área entre $a$ y $b$ bajo $f$.
3. Usar la diferencia de FDA $F(b)-F(a)$ para calcular una probabilidad de intervalo.
4. Explicar por qué $P(X=c)=0$ para una variable aleatoria continua.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: minutos en un reloj, no conteos de defectos | Nombrar el soporte $[2, 14]$. |
| 06-16 | Densidad frente a FMP | Confirmar que $f(6)$ es una altura, no una probabilidad. |
| 16-24 | Ejecutar el Paso 1 | Leer $f(6)=0.166667$ y área total $1.000000$. |
| 24-34 | Probabilidad de intervalo como área | Calcular $F(10)-F(4)$. |
| 34-42 | Ejecutar el Paso 2 | Obtener $P(4<X<10)=0.750000$. |
| 42-48 | Ejecutar el Paso 3 y encoger la ventana | Contrastar $0.158854$ con $0.003330$ y $P(X=6)=0$. |
| 48-50 | Verificación de conceptos y transición a la Lección 20 | Nombrar el modelo uniforme como densidad plana. |

La presentación contiene ocho diapositivas centrales más un apéndice de
mostrarse después de la discusión o omitirse cuando la misma sesión continúa
directamente en otra lección.

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo modelo
triangular de tiempo de servicio con `SEED = 42` y agrega el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `va_continua_01_densidad.py` | Densidad triangular en $[2, 14]$ | $f(2)=0.000000$, $f(6)=0.166667$, $f(14)=0.000000$, media $=7.333333$, área total $=1.000000$. |
| 2 | `va_continua_02_probabilidad_intervalo.py` | Probabilidad de intervalo como área | $F(4)=0.083333$, $F(10)=0.833333$, $P(4<X<10)=P(4\le X\le 10)=0.750000$. |
| 3 | `va_continua_03_limite_masa_puntual.py` | $P(X=c)=0$ desde una FDA continua | $P(\|X-6\|<0.50)=0.158854$, $P(\|X-6\|<0.10)=0.033021$, $P(\|X-6\|<0.01)=0.003330$, $F(6)=0.333333$, salto $=0.000000$, $P(X=6)=0.000000$. |

El resultado del Paso 3 es un límite, no una familia nombrada todavía. Un
reloj continuo puede asignar probabilidad a intervalos, no a un minuto
individual. La Lección 20 usa una densidad uniforme plana y una comprobación
Monte Carlo de $P(X>16)$.

## Modelo sintético de tiempo de servicio

Soporte: $X\in[2,14]$ minutos. Forma: triangular con moda $6$. Media:

\[
E[X]=\frac{a+b+\text{moda}}{3}=\frac{2+14+6}{3}=7.333333.
\]

Densidad pico $f(6)=2/(14-2)=1/6=0.166667$. Esa altura no es $P(X=6)$.
La ventana de 6 minutos de 4 a 10 tiene probabilidad

\[
P(4<X<10)=F(10)-F(4)=0.833333-0.083333=0.750000.
\]

El mismo número se obtiene con extremos cerrados. Encoger una ventana alrededor
de la moda lleva la probabilidad a 0, que es $P(X=6)$.

## Libreta de estudio estudiantil

La libreta ejecutada
[`notebooks/leccion_19_variables_aleatorias_continuas.ipynb`](notebooks/leccion_19_variables_aleatorias_continuas.ipynb)
es una guía de estudio autocontenida y compatible con Google Colab. Reconstruye
la densidad triangular en memoria, calcula áreas de intervalo mediante
diferencias de FDA y relaciona las ventanas decrecientes y la ausencia de un
salto en la FDA con una masa puntual cero. Incluye tres figuras embebidas,
prácticas editables con respuestas desplegables y aserciones ejecutables para
todos los valores verificados del paquete, además de $f(8)=0.125000$ y
$P(6<X<12)=0.625000$.

La libreta se ejecutó tanto en su ubicación como siendo el único artefacto de
la lección en un directorio temporal vacío. Sus renders HTML y Markdown y sus
tres figuras se inspeccionaron después de la ejecución.

## Conceptos erróneos comunes

- $f(x)$ es una altura de densidad. No es $P(X=x)$.
- La probabilidad continua vive en intervalos, no en puntos aislados.
- $P(a<X<b)$ y $P(a\le X\le b)$ coinciden porque cada extremo tiene masa 0.
- La moda es la *región* más probable, no un punto con masa positiva.
- Una FDA sin salto en $c$ es el enunciado geométrico de $P(X=c)=0$.
- El reloj sintético ilustra la aritmética continua. No afirma nada sobre
  ninguna mesa de ayuda real.

## Estructura del paquete

```text
L19_Variables_Aleatorias_Continuas/
|-- README.md
|-- src/
|   |-- va_continua_01_densidad.py
|   |-- va_continua_02_probabilidad_intervalo.py
|   `-- va_continua_03_limite_masa_puntual.py
|-- figuras/
|   |-- va_continua_01_densidad.png
|   |-- va_continua_02_probabilidad_intervalo.png
|   `-- va_continua_03_limite_masa_puntual.png
|-- notebooks/
|   `-- leccion_19_variables_aleatorias_continuas.ipynb
`-- diapositivas/
    |-- leccion_19.tex
    `-- leccion_19.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L19_Variables_Aleatorias_Continuas/src/va_continua_01_densidad.py
uv run es/L19_Variables_Aleatorias_Continuas/src/va_continua_02_probabilidad_intervalo.py
uv run es/L19_Variables_Aleatorias_Continuas/src/va_continua_03_limite_masa_puntual.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L19_Variables_Aleatorias_Continuas/notebooks/leccion_19_variables_aleatorias_continuas.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_19.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_19.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de
mediante Git LFS.

## Atribución OpenStax

Las densidades continuas, la probabilidad de intervalo como área y $P(X=c)=0$
siguen a Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory
Business Statistics 2e*, Capítulo 5, Sección
[5.1](https://openstax.org/books/introductory-business-statistics-2e/pages/5-1-continuous-probability-functions).
La práctica complementaria de funciones continuas está en *Introductory
Statistics 2e*, Sección
[5.1](https://openstax.org/books/introductory-statistics-2e/pages/5-1-continuous-probability-functions).
El límite de densidad uniforme se prepara para la Lección 20. OpenStax publica
estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

