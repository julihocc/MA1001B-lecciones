"""
Lección 05 - Paso 2: Unión, Intersección y Complemento
======================================================
NUEVO EN ESTE PASO: definir_eventos(), resumir_operaciones_conjuntos(), y
construir_figura_membresia().

Cambios desde teoria_conjuntos_01_espacio_muestral.py
La Receta
Introdúcelos en este orden:
    1. definir_eventos()                 crea dos subconjuntos del espacio muestral
    2. resumir_operaciones_conjuntos()      calcula unión, intersección, complemento
    3. construir_figura_membresia()    muestra la membresía de los resultados explícitamente

Ejecútalo:
    uv run es/L05_Teoria_Conjuntos_Espacio_Muestral/src/teoria_conjuntos_02_operaciones_conjuntos.py
"""

from itertools import product
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

# Agg guarda imágenes sin abrir ventanas; debe elegirse antes de pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


# Un resultado mantiene el orden (turno, servicio, estado). Este alias hace
# legibles los contratos sin introducir clases para tres categorías.
Resultado = tuple[str, str, str]
EspacioMuestral = tuple[Resultado, ...]

SEMILLA = 42
CANTIDAD_OBSERVACIONES = 480
TURNOS = ("Día", "Noche")
SERVICIOS = ("Estándar", "Exprés")
ESTADOS = ("A tiempo", "Retrasado")

# Parámetros del ejemplo sintético; no son estimaciones de una empresa.
# Cada probabilidad corresponde a la categoría en la misma posición.
PROBABILIDADES_TURNO = (0.65, 0.35)
PROBABILIDADES_SERVICIO = (0.70, 0.30)
PROBABILIDAD_BASE_RETRASO = 0.10
INCREMENTO_NOCTURNO = 0.08
INCREMENTO_EXPRES = 0.12

# Resolver desde este archivo permite ejecutar desde cualquier directorio.
# La carpeta se crea al guardar, nunca por el solo hecho de importar.
DIRECTORIO_FIGURAS = Path(__file__).resolve().parent.parent / "figuras"


def construir_espacio_muestral() -> EspacioMuestral:
    """Enumera los resultados posibles, independientemente de lo observado.

    Devuelve una tupla ordenada de ocho resultados (turno, servicio, estado).
    El modelo admite todas las combinaciones: 2 x 2 x 2 = 8. Esto describe
    posibilidades, no sus probabilidades ni el número de despachos.
    """
    # product equivale a tres ciclos anidados; el estado cambia más rápido.
    # tuple materializa el iterador para recorrerlo varias veces y conservar
    # el orden de tablas y figuras. Cada tupla interna puede usarse en un set.
    return tuple(product(TURNOS, SERVICIOS, ESTADOS))


def simular_despachos(semilla: int = SEMILLA) -> pd.DataFrame:
    """Genera 480 despachos sintéticos sin leer ni escribir archivos.

    Parámetros
    ----------
    semilla : int
        Entero no negativo para el generador local de NumPy. La misma semilla,
        parámetros y entorno reconstruyen las mismas filas y su orden.

    Devuelve
    -------
    pd.DataFrame
        Columnas id_despacho, turno, servicio, estado y resultado. Cada fila
        es una observación; resultado es su tupla (turno, servicio, estado).
        Los identificadores distinguen filas, no agregan posibilidades a S.

    Supuestos
    ---------
    Turno y servicio se sortean independientemente en este modelo. El retraso
    depende de ambos. Los parámetros son decisiones didácticas que producen
    frecuencias desiguales, no conclusiones sobre operaciones reales.

    Errores
    -------
    ValueError
        NumPy rechaza una semilla negativa. Las probabilidades de choice
        deben estar entre cero y uno y sumar uno.
    """
    # El generador vive dentro de la función: otro código no puede consumir
    # su secuencia antes de la simulación. No se reinicia entre sorteos.
    generador = np.random.default_rng(semilla)

    # Cada arreglo tiene una entrada por despacho. p sigue el orden de las
    # categorías; 0.35 es una probabilidad, no una cuota exacta del 35 %.
    turnos = generador.choice(
        TURNOS, size=CANTIDAD_OBSERVACIONES, p=PROBABILIDADES_TURNO
    )
    servicios = generador.choice(
        SERVICIOS, size=CANTIDAD_OBSERVACIONES, p=PROBABILIDADES_SERVICIO
    )

    # Las comparaciones producen arreglos booleanos alineados por despacho.
    # True aporta 1 y False aporta 0 al multiplicar: las probabilidades son
    # 0.10 (Día/Estándar), 0.18 (Noche/Estándar), 0.22 (Día/Exprés)
    # y 0.30 (Noche/Exprés). El aumento es en puntos porcentuales.
    probabilidades_retraso = (
        PROBABILIDAD_BASE_RETRASO
        + INCREMENTO_NOCTURNO * (turnos == "Noche")
        + INCREMENTO_EXPRES * (servicios == "Exprés")
    )
    # Un parámetro editado fuera del intervalo produciría una simulación
    # engañosa: rechazarlo es preferible a recortarlo silenciosamente.
    if np.any((probabilidades_retraso < 0) | (probabilidades_retraso > 1)):
        raise ValueError("Cada probabilidad de retraso debe estar entre 0 y 1.")

    # Para U uniforme en [0, 1), P(U < p) = p. Se toma un U por despacho;
    # np.where convierte cada decisión booleana en su etiqueta categórica.
    uniformes = generador.random(CANTIDAD_OBSERVACIONES)
    estados = np.where(uniformes < probabilidades_retraso, "Retrasado", "A tiempo")

    # Las columnas comparten posición: la fila i reúne los sorteos i.
    # El inicio 500001 sólo da etiquetas únicas; no interviene en el modelo.
    despachos = pd.DataFrame(
        {
            "id_despacho": np.arange(500_001, 500_001 + CANTIDAD_OBSERVACIONES),
            "turno": turnos,
            "servicio": servicios,
            "estado": estados,
        }
    )
    # zip agrupa por fila; list materializa las tuplas para pandas.
    # Repetir un resultado en varias filas incrementa su frecuencia, no |S|.
    despachos["resultado"] = list(zip(turnos, servicios, estados))
    return despachos


def guardar_figura(figura: plt.Figure, ruta: Path) -> Path:
    """Guarda una figura como PNG y libera sus recursos, incluso si falla.

    Recibe la figura ya construida y la ruta de destino; devuelve esa ruta.
    Crea sólo la carpeta necesaria al ejecutar esta función. Los errores de
    escritura se propagan: nunca se informa un guardado que no ocurrió.
    """
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        figura.savefig(ruta, dpi=170)
    finally:
        # Cerrar evita acumular figuras ocultas en ejecuciones repetidas.
        plt.close(figura)
    return ruta


def etiqueta_resultado(resultado: Resultado) -> str:
    """Une las tres etiquetas de un resultado con | para mostrarlo.

    La cadena es una etiqueta visual; la tupla sigue siendo la unidad de S.
    """
    return " | ".join(resultado)


# --- NUEVO (1) definir_eventos() ------------------------------------------------
def definir_eventos(
    espacio_muestral: EspacioMuestral,
) -> tuple[set[Resultado], set[Resultado]]:
    """Devuelve (A, B), subconjuntos del espacio muestral recibido.

    A contiene resultados de Noche; B contiene resultados Retrasados.
    Cada resultado debe ser una tupla (turno, servicio, estado).
    Se devuelven conjuntos nuevos; no se modifica espacio_muestral.
    """
    # Filtrar S pregunta qué puede ocurrir, no cuántas veces se observó.
    # Los índices 0 y 2 corresponden al contrato (turno, servicio, estado).
    evento_a = {resultado for resultado in espacio_muestral if resultado[0] == "Noche"}
    evento_b = {resultado for resultado in espacio_muestral if resultado[2] == "Retrasado"}
    return evento_a, evento_b
# ------------------------------------------------------------------------------


# --- NUEVO (2) resumir_operaciones_conjuntos() -------------------------------------
def resumir_operaciones_conjuntos(
    espacio_muestral: EspacioMuestral,
    evento_a: set[Resultado],
    evento_b: set[Resultado],
) -> dict[str, set[Resultado]]:
    """Devuelve un diccionario con A, B, intersección, unión y complemento.

    espacio_muestral define el universo; evento_a y evento_b deben ser
    subconjuntos de él. Lanza ValueError si incluyen resultados ajenos a S.
    No modifica las entradas. Las entradas A y B conservan sus referencias;
    las operaciones producen conjuntos nuevos.
    """
    # set permite operar por pertenencia; las frecuencias no intervienen.
    universo = set(espacio_muestral)
    if not evento_a <= universo or not evento_b <= universo:
        raise ValueError("Los eventos deben ser subconjuntos del espacio muestral.")
    # & exige ambas condiciones; | acepta una o ambas sin duplicar resultados.
    # El complemento es S - A, nunca una negación sin universo definido.
    return {
        "A": evento_a,
        "B": evento_b,
        "A intersección B": evento_a & evento_b,
        "A unión B": evento_a | evento_b,
        "A complemento": universo - evento_a,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) construir_figura_membresia() -----------------------------------
def construir_figura_membresia(
    espacio_muestral: EspacioMuestral,
    operaciones: dict[str, set[Resultado]],
) -> plt.Figure:
    """Representa la pertenencia de los resultados a cada conjunto.

    Recibe S ordenado y el diccionario de resumir_operaciones_conjuntos().
    Devuelve una Figure sin modificar entradas ni guardar archivos.
    Las filas son resultados; las columnas, conjuntos. Un 1 significa
    pertenencia y un 0 ausencia, no frecuencia de despachos.
    """
    # El diccionario conserva el orden académico: A, B, intersección, unión
    # y complemento. Cada columna evalúa pertenencia para todos los miembros
    # de S; int convierte False/True en 0/1 para hacer visible esa respuesta.
    membresia = pd.DataFrame(
        {
            nombre: [int(resultado in conjunto) for resultado in espacio_muestral]
            for nombre, conjunto in operaciones.items()
        },
        index=[etiqueta_resultado(resultado) for resultado in espacio_muestral],
    )

    # heatmap coloca celdas, etiquetas y números. Fijar vmin/vmax mantiene
    # el significado de los colores incluso si un ejercicio contiene sólo
    # ceros o sólo unos. La variable es binaria; no necesita barra continua.
    figura, eje = plt.subplots(figsize=(10.2, 5.4), layout="constrained")
    sns.heatmap(
        membresia, cmap=["#EEF1F7", "#EC2661"], vmin=0, vmax=1,
        annot=True, fmt="d", cbar=False, linewidths=1, ax=eje,
    )
    eje.set(
        title="Pertenencia a eventos y operaciones de conjuntos",
        xlabel="Evento u operación", ylabel="Resultado posible",
    )
    eje.tick_params(axis="both", labelrotation=0, labelsize=9)
    return figura
# ------------------------------------------------------------------------------


def principal() -> None:
    """Coordina el ejemplo: calcular, visualizar, guardar e informar resultados."""
    # Las funciones de cálculo no imprimen ni escriben archivos. Esta función
    # decide el orden de ejecución y reúne los resultados para el estudiante.
    espacio_muestral = construir_espacio_muestral()
    despachos = simular_despachos()
    evento_a, evento_b = definir_eventos(espacio_muestral)
    operaciones = resumir_operaciones_conjuntos(espacio_muestral, evento_a, evento_b)
    figura = construir_figura_membresia(espacio_muestral, operaciones)
    ruta_figura = guardar_figura(
        figura, DIRECTORIO_FIGURAS / "teoria_conjuntos_02_operaciones_conjuntos.png"
    )

    # Aquí cambia la unidad: cada booleano corresponde a una de las 480 filas.
    # eq compara elemento a elemento; sumar True/False cuenta despachos.
    # & y | combinan máscaras fila por fila (and/or no sirven para esta tarea).
    registro_a = despachos["turno"].eq("Noche")
    registro_b = despachos["estado"].eq("Retrasado")
    # El informe mantiene separados los resultados posibles y las observaciones.
    print("================================================================")
    print("LECCIÓN 05 - PASO 2: OPERACIONES DE CONJUNTOS")
    print("================================================================")
    print("Aviso de datos sintéticos           : No se utilizan datos reales de la empresa")
    print(f"Resultados del espacio muestral |S| : {len(espacio_muestral)}")
    for nombre in ["A", "B", "A intersección B", "A unión B", "A complemento"]:
        print(f"Conteo de resultados |{nombre}|".ljust(36) + f": {len(operaciones[nombre])}")
    print(f"Registros observados en A           : {int(registro_a.sum())}")
    print(f"Registros observados en B           : {int(registro_b.sum())}")
    print(f"Registros observados en A y B       : {int((registro_a & registro_b).sum())}")
    print(f"Registros observados en A o B       : {int((registro_a | registro_b).sum())}")
    print(f"Figura guardada en                  : {ruta_figura}")
    print("================================================================")


# Importar permite revisar las funciones sin ejecutar el ejemplo ni crear PNG.
if __name__ == "__main__":
    principal()

