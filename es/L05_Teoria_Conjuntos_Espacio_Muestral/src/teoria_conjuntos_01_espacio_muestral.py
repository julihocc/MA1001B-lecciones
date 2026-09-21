"""
Lección 05 - Paso 1: Resultados y el Espacio Muestral
=====================================================
NUEVO EN ESTE PASO: construir_espacio_muestral(), simular_despachos(), y
construir_figura_frecuencias().

La Receta
    1. construir_espacio_muestral()   enumera posibilidades sin asignar frecuencias
    2. simular_despachos()           produce observaciones con probabilidades desiguales
    3. construir_figura_frecuencias() contrasta posibilidades y frecuencias

Lista cada resultado posible de un experimento de despachos sintético, simula
una colección sembrada de registros de despacho, y verifica cuáles resultados
posibles aparecen. Posible no significa igualmente probable.

Ejecútalo:
    uv run es/L05_Teoria_Conjuntos_Espacio_Muestral/src/teoria_conjuntos_01_espacio_muestral.py
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


# --- NUEVO (1) construir_espacio_muestral() -----------------------------------
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


# --- NUEVO (2) simular_despachos() --------------------------------------------
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
    """Convierte una tupla (turno, servicio, estado) en texto legible.

    Recibe un resultado de S y devuelve sus tres etiquetas unidas por |.
    El formato es sólo presentación: no altera el resultado ni su frecuencia.
    """
    return " | ".join(resultado)


# --- NUEVO (3) construir_figura_frecuencias() -------------------------------------
def construir_figura_frecuencias(
    espacio_muestral: EspacioMuestral,
    despachos: pd.DataFrame,
) -> plt.Figure:
    """Representa la frecuencia de cada resultado posible, incluidos los ceros.

    Recibe S ordenado y un DataFrame con la columna resultado. Devuelve una
    Figure sin modificar las entradas ni guardar archivos; el llamador debe
    guardarla o cerrarla. Cada barra cuenta despachos, no probabilidades.
    """
    # value_counts cuenta repeticiones de cada tupla observada. Recorrer S
    # conserva las posibilidades que no aparecieron; get(..., 0) les da cero.
    conteos = despachos["resultado"].value_counts()
    frecuencias = pd.DataFrame(
        {
            "resultado": [etiqueta_resultado(r) for r in espacio_muestral],
            "frecuencia": [int(conteos.get(r, 0)) for r in espacio_muestral],
        }
    )

    # Seaborn recibe columnas con significado y coloca las barras y etiquetas.
    # Cada fila ya contiene un conteo: sum lo representa directamente y
    # errorbar=None evita intervalos inferenciales que aquí no corresponden.
    figura, eje = plt.subplots(figsize=(10.2, 5.2), layout="constrained")
    sns.barplot(
        data=frecuencias, x="frecuencia", y="resultado",
        order=frecuencias["resultado"].tolist(),
        estimator="sum", errorbar=None, color="#EC2661", ax=eje,
    )
    eje.set(
        title="Resultados posibles y frecuencias observadas",
        xlabel="Despachos sintéticos observados", ylabel="",
    )
    # bar_label coloca cada conteo al extremo sin calcular coordenadas.
    # El margen deja espacio para el texto, también si todos los conteos son cero.
    eje.bar_label(eje.containers[0], fmt="%.0f", padding=3)
    eje.margins(x=0.18)
    return figura
# ------------------------------------------------------------------------------


def principal() -> None:
    """Coordina el ejemplo: calcular, visualizar, guardar e informar resultados."""
    # Las funciones de cálculo no imprimen ni escriben archivos. Esta función
    # decide el orden de ejecución y reúne los resultados para el estudiante.
    espacio_muestral = construir_espacio_muestral()
    despachos = simular_despachos()
    figura = construir_figura_frecuencias(espacio_muestral, despachos)
    ruta_figura = guardar_figura(
        figura, DIRECTORIO_FIGURAS / "teoria_conjuntos_01_espacio_muestral.png"
    )
    resultados_observados = set(despachos["resultado"])
    # Calcular la tabla una sola vez evita repetir la misma agregación.
    conteos = despachos["resultado"].value_counts()
    resultado_mas_frecuente = conteos.index[0]
    conteo_mas_frecuente = int(conteos.iloc[0])

    # El informe mantiene separados los resultados posibles y las observaciones.
    print("================================================================")
    print("LECCIÓN 05 - PASO 1: ESPACIO MUESTRAL")
    print("================================================================")
    print("Aviso de datos sintéticos           : No se utilizan datos reales de la empresa")
    print(f"Resultados posibles en S            : {len(espacio_muestral)}")
    print(f"Registros de despachos sintéticos   : {len(despachos)}")
    print(f"Resultados distintos observados     : {len(resultados_observados)}")
    print("Resultado observado más frecuente   : "
          f"{etiqueta_resultado(resultado_mas_frecuente)}")
    print(f"Registros con ese resultado         : {conteo_mas_frecuente}")
    print("Suposición de igual probabilidad    : No se asume")
    print(f"Figura guardada en                  : {ruta_figura}")
    print("================================================================")


# Importar permite revisar las funciones sin ejecutar el ejemplo ni crear PNG.
if __name__ == "__main__":
    principal()

