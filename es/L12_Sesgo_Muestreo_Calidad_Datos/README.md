# Lección 12 - Sesgo de muestreo, calidad de datos y error no muestral

Esta microlección de 50 minutos usa un registro sintético de 8,000 filas de
tickets de servicio para comparar una muestra aleatoria simple con una
muestra de conveniencia más grande solo en línea y con un hueco de cobertura
que excluye una región. El paso final muestra que limpiar filas incompletas
no restaura unidades que nunca estuvieron en el marco.

- **Duración objetivo:** 50 minutos.
- **Referencia canónica:** OpenStax, *Introductory Business Statistics 2e*,
  Secciones 1.2 y 1.4. Discusión complementaria de calidad de datos:
  *Principles of Data Science*, Secciones 2.1 y 8.1.
- **Prerrequisitos:** Población versus muestra de la Lección 01 y diseños de
  muestreo de la Lección 02.
- **Aviso de datos:** Cada ticket, región, canal y bandera de queja es
  sintético. Los scripts no contienen datos reales de empresas, clientes o
  socios.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. Estimar una tasa poblacional de quejas a partir de una muestra aleatoria
   simple y reportar el error de muestreo.
2. Contrastar ese error con una muestra de conveniencia más grande
   restringida al canal En línea.
3. Identificar un hueco de cobertura cuando una región falta en el marco.
4. Explicar por qué la limpieza listwise de un marco sesgado no restaura
   unidades faltantes.

## Ruta de facilitación de 50 minutos

| Tiempo | Movimiento en clase | Trabajo observable del estudiante |
|---:|---|---|
| 00-06 | Apertura: parámetro versus error de muestreo | Nombrar el parámetro de tasa de quejas. |
| 06-16 | El registro de 8,000 filas | Confirmar conteos regionales $2400$, $2400$, $2000$, $1200$. |
| 16-24 | Ejecutar el Paso 1 | Leer población $0.119875$ y error MAS $0.014875$. |
| 24-34 | Selección solo en línea | Predecir la dirección del sesgo. |
| 34-42 | Ejecutar el Paso 2 | Contrastar $n=400$ error $0.014875$ con $n=1{,}200$ error $0.063208$. |
| 42-48 | Ejecutar el Paso 3 e inspeccionar el Oeste | Ver $0$ tickets del Oeste tras la limpieza. |
| 48-50 | Verificación de conceptos y entrega a la Lección 13 | Nombrar error de muestreo versus error no muestral. |

La presentación contiene ocho diapositivas centrales más un apéndice de

## Scripts incrementales y resultados verificados

Los tres programas son autocontenidos. Cada uno reconstruye el mismo registro
sintético con `SEED = 42` y agrega el siguiente concepto sin importar otro
script de la lección. Estos valores provienen de dos ejecuciones coincidentes
en el entorno bloqueado de `uv`.

| Paso | Script | Concepto nuevo | Resultado verificado |
|:---:|---|---|---|
| 1 | `sesgo_muestreo_01_mas.py` | Marco completo y MAS | $N=8{,}000$; tasa poblacional $0.119875$; MAS $n=400$ tasa $0.105000$; error absoluto $0.014875$. |
| 2 | `sesgo_muestreo_02_conveniencia_web.py` | Muestra de conveniencia solo en línea | Tasa En línea $0.057323$; conveniencia $n=1{,}200$ tasa $0.056667$; error absoluto $0.063208$. Muestra más grande, más error. |
| 3 | `sesgo_muestreo_03_hueco_cobertura.py` | Hueco de cobertura, faltantes, limpieza | Tasa Oeste $0.276667$; error sin Oeste $0.027669$; tras la limpieza, tickets del Oeste $=0$ y error $0.026509$. |

El resultado del Paso 3 es un límite: eliminar filas incompletas puede
ordenar una tabla sin reparar un marco que nunca contuvo el Oeste. La
Lección 13 pasa de la calidad de la muestra a una variable aleatoria discreta
definida en un espacio muestral bien especificado.

## Registro sintético de tickets

| Región | Tickets | Rol en la historia de sesgo |
|---|---:|---|
| Norte | $2{,}400$ | En el marco |
| Sur | $2{,}400$ | En el marco |
| Este | $2{,}000$ | En el marco; canal En línea pesado |
| Oeste | $1{,}200$ | Tasa de quejas más alta; se omite en el hueco de cobertura |

Tasas verificadas con `SEED = 42`:

| Cantidad | Valor |
|---|---:|
| Tasa poblacional de quejas | $0.119875$ |
| Tasa de quejas del canal En línea | $0.057323$ |
| Tasa de quejas del canal Tienda | $0.176555$ |
| Tasa de quejas del Oeste | $0.276667$ |
| Tasa de quejas no Oeste | $0.092206$ |
| Banderas de queja faltantes | $616$ ($253$ en el Oeste) |

## Libreta de estudio

La guía ejecutada y autocontenida está en
[`notebooks/leccion_12_sesgo_muestreo_calidad_datos.ipynb`](notebooks/leccion_12_sesgo_muestreo_calidad_datos.ipynb).
Reconstruye en memoria el registro sintético con `SEMILLA = 42`, desarrolla
acumulativamente los tres pasos de la lección y embebe tres figuras. También
las cifras canónicas. La libreta se ejecutó tanto en el paquete como desde un
directorio temporal vacío; se inspeccionaron sus renderizados HTML y Markdown
y sus tres figuras.

## Conceptos erróneos comunes

- Una muestra más grande no es automáticamente una mejor muestra.
- El muestreo de conveniencia desde un canal fácil no es una muestra
  aleatoria simple.
- El error de cobertura es un error no muestral: las unidades nunca
  estuvieron disponibles.
- La eliminación listwise quita filas incompletas; no imputa regiones
  faltantes.
- El registro sintético ilustra el sesgo. No es una afirmación sobre ningún
  proceso real de servicio.

## Estructura del paquete

```text
L12_Sesgo_Muestreo_Calidad_Datos/
|-- README.md
|-- notebooks/
|   `-- leccion_12_sesgo_muestreo_calidad_datos.ipynb
|-- src/
|   |-- sesgo_muestreo_01_mas.py
|   |-- sesgo_muestreo_02_conveniencia_web.py
|   `-- sesgo_muestreo_03_hueco_cobertura.py
|-- figuras/
|   |-- sesgo_muestreo_01_mas.png
|   |-- sesgo_muestreo_02_conveniencia_web.png
|   `-- sesgo_muestreo_03_hueco_cobertura.png
`-- diapositivas/
    |-- leccion_12.tex
    `-- leccion_12.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L12_Sesgo_Muestreo_Calidad_Datos/src/sesgo_muestreo_01_mas.py
uv run es/L12_Sesgo_Muestreo_Calidad_Datos/src/sesgo_muestreo_02_conveniencia_web.py
uv run es/L12_Sesgo_Muestreo_Calidad_Datos/src/sesgo_muestreo_03_hueco_cobertura.py
uv run jupyter nbconvert --execute --to notebook --inplace es/L12_Sesgo_Muestreo_Calidad_Datos/notebooks/leccion_12_sesgo_muestreo_calidad_datos.ipynb
```

Compilar las diapositivas desde `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_12.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_12.tex
```

El PDF compilado contiene el núcleo de ocho diapositivas y el apéndice de

## Atribución OpenStax

El muestreo, la variación y el diseño de estudios siguen a Alexander Holmes,
Barbara Illowsky y Susan Dean, *Introductory Business Statistics 2e*,
Secciones
[1.2](https://openstax.org/books/introductory-business-statistics-2e/pages/1-2-data-sampling-and-variation-in-data-and-sampling)
y
[1.4](https://openstax.org/books/introductory-business-statistics-2e/pages/1-4-experimental-design-and-ethics).
Las páginas complementarias de recolección de datos y ética son *Principles
of Data Science*, Secciones
[2.1](https://openstax.org/books/principles-data-science/pages/2-1-overview-of-data-collection-methods)
y
[8.1](https://openstax.org/books/principles-data-science/pages/8-1-ethics-in-data-collection).
OpenStax publica estos textos bajo la licencia Creative Commons
Attribution-NonCommercial-ShareAlike. El conjunto sintético, el código y las
figuras de este paquete son materiales originales del curso.

