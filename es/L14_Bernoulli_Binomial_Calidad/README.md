# Lección 14 - Ensayos de Bernoulli y el modelo binomial

Esta microlección de 50 minutos modela una inspección sintética de $n=20$
unidades, cada una defectuosa con chance $p=0.08$. Los estudiantes parten de
un ensayo de Bernoulli, calculan $P(X=0)$, $P(X\le 2)$, $np$ y $np(1-p)$, y
luego rompen el supuesto de $p$ constante con una mezcla de dos puntos de
lotes.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Sección 4.2.
- **Prerrequisitos:** Variables aleatorias discretas de la Lección 13.
- **Aviso de datos:** Cada ensayo, bandera de defecto y tipo de lote es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Enunciar el ensayo de Bernoulli y los cuatro supuestos binomiales.
2. Calcular $P(X=0)$ y $P(X\le 2)$ para $X\sim\mathrm{Binomial}(20,0.08)$.
3. Reportar la media $np$ y la varianza $np(1-p)$.
4. Explicar por qué una mezcla de tipos de lote con el mismo $p$ promedio no
   es binomial.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: una inspección | Etiquetar éxito como defectuoso, $p=0.08$. |
| 06-16 | Cuatro supuestos binomiales | Comprobar $n$, dos resultados, $p$ constante, independencia. |
| 16-24 | Ejecutar el Paso 1 | Confirmar $q=0.920000$ y $np=1.600000$. |
| 24-34 | FMP binomial y cola izquierda | Calcular $P(X=0)=(0.92)^{20}$. |
| 34-42 | Ejecutar el Paso 2 | Leer $P(X=0)=0.188693$ y $P(X\le 2)=0.787946$. |
| 42-48 | Ejecutar el Paso 3 con lotes mezclados | Contrastar $0.188693$ con la mezcla $0.358291$. |
| 48-50 | Verificación de conceptos y entrega a la Lección 15 | Nombrar el límite de $p$ constante. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye la misma
inspección sintética con `SEED = 42` reservada y agrega el siguiente
concepto sin importar otro script de la lección. Estos valores provienen de
dos ejecuciones coincidentes en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `binomial_01_ensayos_bernoulli.py` | Ensayo de Bernoulli e ingredientes binomiales | $p=0.080000$, $q=0.920000$, $n=20$, $np=1.600000$. |
| 2 | `binomial_02_fmp_fda.py` | FMP, FDA y momentos binomiales | $P(X=0)=0.188693$, $P(X\le 2)=0.787946$, $\mathrm{Var}(X)=1.472000$. |
| 3 | `binomial_03_p_no_constante.py` | Mezcla de $p=0.02$ y $p=0.14$ | $p$ promedio sigue $0.080000$; $P(X=0)$ de la mezcla $0.358291$; varianza de la mezcla $2.840000$. |

El resultado del Paso 3 es un límite: coincidir en el $p$ promedio no
restaura el modelo binomial. La Lección 15 conserva el modelo binomial y
compara dos políticas que comparten la misma media $np$.

## Libreta de estudio

La guía ejecutada y autocontenida está en
[`notebooks/leccion_14_bernoulli_binomial_calidad.ipynb`](notebooks/leccion_14_bernoulli_binomial_calidad.ipynb).
Mantiene el mismo estado de inspección con $n=20$ a través de los pasos de
Bernoulli, binomial exacta y lotes mezclados, y embebe tres figuras. También
las cifras canónicas. La libreta se ejecutó tanto en el paquete como desde un
directorio temporal vacío; se inspeccionaron sus renderizados HTML y Markdown
y sus tres figuras.

## Conceptos erróneos comunes

- Un ensayo de Bernoulli tiene dos resultados; el binomial cuenta éxitos en
  $n$ de ellos.
- $P(X=0)=(1-p)^n$ usa el supuesto de $p$ constante en cada ensayo.
- $np$ es una media, no una probabilidad.
- Lotes con $p=0.02$ y $p=0.14$ que promedian $0.08$ no son
  $\mathrm{Binomial}(20,0.08)$.
- La inspección sintética ilustra el modelo. No es una afirmación sobre
  ningún proceso real.

## Estructura del paquete

```text
L14_Bernoulli_Binomial_Calidad/
|-- README.md
|-- notebooks/
|   `-- leccion_14_bernoulli_binomial_calidad.ipynb
|-- src/
|   |-- binomial_01_ensayos_bernoulli.py
|   |-- binomial_02_fmp_fda.py
|   `-- binomial_03_p_no_constante.py
|-- figuras/
|   |-- binomial_01_ensayos_bernoulli.png
|   |-- binomial_02_fmp_fda.png
|   `-- binomial_03_p_no_constante.png
`-- diapositivas/
    |-- leccion_14.tex
    `-- leccion_14.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L14_Bernoulli_Binomial_Calidad/src/binomial_01_ensayos_bernoulli.py
uv run es/L14_Bernoulli_Binomial_Calidad/src/binomial_02_fmp_fda.py
uv run es/L14_Bernoulli_Binomial_Calidad/src/binomial_03_p_no_constante.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L14_Bernoulli_Binomial_Calidad/notebooks/leccion_14_bernoulli_binomial_calidad.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_14.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_14.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de

## Atribución OpenStax

Los ensayos de Bernoulli y la distribución de probabilidad binomial siguen a
Alexander Holmes, Barbara Illowsky y Susan Dean, *Introductory Business
Statistics 2e*, Sección
[4.2](https://openstax.org/books/introductory-business-statistics-2e/pages/4-2-binomial-distribution).
OpenStax publica este texto bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. La inspección sintética, el código y
las figuras de este paquete son materiales originales del curso.

