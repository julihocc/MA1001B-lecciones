# Lección 09: Probabilidad condicional e independencia

Esta microlección de 50 minutos usa un escenario sintético de operaciones de
pedidos para reducir un espacio muestral, probar si dos eventos son
independientes y exponer la dependencia creada al muestrear sin reemplazo.

## Resultados de aprendizaje

Al final de la lección, un estudiante puede:

1. interpretar y calcular \(P(A\mid B)\) usando la condición como denominador;
2. explicar por qué \(P(A\mid B)\) y \(P(B\mid A)\) responden preguntas distintas;
3. probar independencia con una igualdad condicional o de producto;
4. actualizar una probabilidad secuencial cuando se muestrea sin reemplazo.

## Prerrequisitos

- eventos, intersecciones y espacios muestrales de la Lección 05;
- probabilidades de tablas de contingencia y reglas de multiplicación de la
  Lección 08;
- filtrado básico de pandas, arreglos de NumPy y gráficas de matplotlib.

## Ruta de facilitación de 50 minutos

| Tiempo | Actividad | Evidencia |
|---:|---|---|
| 0-6 min | Revisar la tabla sintética de 400 pedidos y plantear una pregunta condicional. | Identificar el denominador restringido. |
| 6-15 min | Derivar la probabilidad condicional como un espacio muestral reducido. | \(P(L\mid M)=48/120=0.40\). |
| 15-23 min | Ejecutar el Paso 1 e invertir la condición. | \(P(L\mid M)=0.40\), mientras \(P(M\mid L)=0.60\). |
| 23-32 min | Definir y probar independencia. | Se evalúan las igualdades condicional y de producto. |
| 32-39 min | Ejecutar el Paso 2 e interpretar la asociación con cuidado. | Ambas igualdades fallan; no se afirma causalidad. |
| 39-47 min | Ejecutar el Paso 3 para dos selecciones sin reemplazo. | Exacta 0.133333 y simulada 0.132938 reemplazan la ingenua 0.160000. |
| 47-50 min | Verificación de conceptos y puente a la L10. | Enunciar por qué se necesitan ramas para secuencias más largas. |

La verificación de conceptos puede conducir directamente a otra lección en la
misma sesión de clase. No es una actividad obligatoria de cierre de sesión.

## Escenario sintético de operaciones

Todos los pedidos, procesos de enrutamiento, resultados de entrega y
selecciones de inspección son sintéticos. No describen ninguna organización,
socio o proceso operativo reales.

| Proceso de enrutamiento | Retrasado | A tiempo | Total de fila |
|---|---:|---:|---:|
| Revisión manual | 48 | 72 | 120 |
| Automatizado | 32 | 248 | 280 |
| Total de columna | 80 | 320 | 400 |

Sea \(M\) revisión manual y \(L\) entrega retrasada. Condicionar en revisión
manual reduce el denominador de 400 pedidos a 120:

\[
P(L\mid M)=\frac{P(L\cap M)}{P(M)}=\frac{48}{120}=0.40.
\]

Invertir la condición cambia el grupo de referencia:

\[
P(M\mid L)=\frac{48}{80}=0.60.
\]

Los dos valores difieren porque sus denominadores responden preguntas
distintas.

## Probar independencia

Los eventos \(M\) y \(L\) son independientes si se cumple cualquier igualdad
equivalente, como

\[
P(L\mid M)=P(L)
\]

o

\[
P(M\cap L)=P(M)P(L).
\]

Aquí, \(0.40\ne0.20\) y \(0.12\ne0.06\), de modo que los eventos no son
independientes en la tabla sintética. Esto es evidencia de asociación
solamente; la tabla no muestra que la revisión manual cause entrega
retrasada.

## El límite sin reemplazo

En un lote sintético pequeño de inspección, cuatro de diez pedidos están
marcados. Si se seleccionan dos pedidos sin reemplazo, entonces

\[
P(\text{ambos marcados})=\frac{4}{10}\frac{3}{9}=\frac{2}{15}
=0.133333\ldots
\]

El cálculo independiente ingenuo \((4/10)^2=0.160000\) falla porque la
primera selección cambia tanto el numerador como el denominador de la
segunda. La simulación con semilla 42 de 500,000 selecciones produjo
0.132938. Seguir secuencias más largas motiva los diagramas de árbol y la
descomposición del espacio muestral en la L10.

## Libreta de estudio

La guía estudiantil
[`notebooks/leccion_09_probabilidad_condicional_independencia.ipynb`](notebooks/leccion_09_probabilidad_condicional_independencia.ipynb)
integra los tres pasos en un solo estado acumulativo. Reconstruye en memoria el
registro sintético de 400 pedidos, conserva los contratos funcionales de
`src/`, embebe tres figuras editables y concluye con aserciones ejecutables,
práctica segura y respuestas plegables. Su simulación con semilla 42 usa
500,000 selecciones y verifica el cálculo exacto sin reemplazo.

La libreta es autocontenida: no descarga datos, no lee archivos del
repositorio, no requiere acceso de red y no importa los scripts del paquete ni
las imágenes retenidas. Puede subirse directamente a Google Colab, abrirse en
VS Code con un kernel de Colab o ejecutarse en el entorno bloqueado del
proyecto. Sus figuras son salidas embebidas; los PNG de `figuras/` siguen
siendo la evidencia retenida producida por los scripts independientes.

## Scripts y resultados verificados

Cada script es independiente, usa la semilla 42, no acepta argumentos de
línea de comandos, no importa un paso anterior y escribe solo su PNG
correspondiente. Estos valores provienen de dos ejecuciones coincidentes en
el entorno bloqueado de `uv`.

| Paso | Script | Resultado verificado |
|:---:|---|---|
| 1 | `condicional_01_espacio_muestral_reducido.py` | \(P(L\mid M)=0.400000\), \(P(L\mid\text{Automatizado})=0.114286\) y \(P(M\mid L)=0.600000\). |
| 2 | `condicional_02_pruebas_independencia.py` | \(P(L)=0.200000\ne0.400000\); \(P(M\cap L)=0.120000\ne0.060000=P(M)P(L)\); independiente es `False`. |
| 3 | `condicional_03_limite_sin_reemplazo.py` | Ingenua 0.160000; exacta 0.133333; simulación semilla 42 0.132938 de 500,000 ensayos. |

## Conceptos erróneos comunes

- La condición después de la barra vertical determina el denominador.
- \(P(A\mid B)\) y \(P(B\mid A)\) son en general distintas.
- La independencia debe comprobarse; no debe inferirse de los nombres de los
  eventos.
- Eventos mutuamente excluyentes con probabilidades positivas no son
  independientes.
- Una diferencia en tasas condicionales es una asociación, no prueba de
  causalidad.
- Sin reemplazo, la primera selección cambia las probabilidades posteriores.

## Estructura del paquete

```text
L09_Probabilidad_Condicional_Independencia/
|-- README.md
|-- notebooks/
|   `-- leccion_09_probabilidad_condicional_independencia.ipynb
|-- src/
|   |-- condicional_01_espacio_muestral_reducido.py
|   |-- condicional_02_pruebas_independencia.py
|   `-- condicional_03_limite_sin_reemplazo.py
|-- figuras/
|   |-- condicional_01_tasas.png
|   |-- condicional_02_independencia.png
|   `-- condicional_03_secuencia.png
`-- diapositivas/
    |-- leccion_09.tex
    `-- leccion_09.pdf
```

## Ejecución

Desde la raíz del repositorio:

```bash
uv sync --frozen
uv run es/L09_Probabilidad_Condicional_Independencia/src/condicional_01_espacio_muestral_reducido.py
uv run es/L09_Probabilidad_Condicional_Independencia/src/condicional_02_pruebas_independencia.py
uv run es/L09_Probabilidad_Condicional_Independencia/src/condicional_03_limite_sin_reemplazo.py
```

Ejecutar la libreta y guardar todas las salidas de celda:

```powershell
uv run jupyter nbconvert --execute --to notebook --inplace `
  es/L09_Probabilidad_Condicional_Independencia/notebooks/leccion_09_probabilidad_condicional_independencia.ipynb
```

Compilar dos veces desde el directorio `diapositivas/`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error leccion_09.tex
pdflatex -interaction=nonstopmode -halt-on-error leccion_09.tex
```

## Atribución OpenStax

La definición de probabilidad condicional como espacio muestral reducido
sigue a OpenStax, *Introductory Business Statistics 2e*, Capítulo 3, Sección
3.1. Los criterios equivalentes de independencia y la dependencia creada al
muestrear sin reemplazo siguen la Sección 3.2. La regla general de
multiplicación es coherente con la Sección 3.3.

- Sección 3.1: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-1-terminology>
- Sección 3.2: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-2-independent-and-mutually-exclusive-events>
- Sección 3.3: <https://openstax.org/books/introductory-business-statistics-2e/pages/3-3-two-basic-rules-of-probability>
- Autores: Alexander Holmes, Barbara Illowsky y Susan Dean.
- Licencia: CC BY-NC-SA 4.0.

