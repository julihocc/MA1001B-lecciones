"""
Lección 05 - Paso 3: Eventos Disjuntos y Exhaustivos
====================================================
NUEVO EN ESTE PASO: definir_eventos_servicio(), comparar_pares_eventos(), y
construir_figura_pares().

Cambios desde teoria_conjuntos_02_operaciones_conjuntos.py
La Receta
Introdúcelos en este orden:
    1. definir_eventos_servicio()         crea eventos Estándar y Exprés
    2. comparar_pares_eventos()           prueba traslape y cobertura del espacio muestral
    3. construir_figura_pares()   contrasta dos relaciones de eventos

Ejecútalo:
    uv run es/L05_Teoria_Conjuntos_Espacio_Muestral/src/teoria_conjuntos_03_eventos_disjuntos.py
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


# --- NUEVO (1) definir_eventos_servicio() ----------------------------------------
def definir_eventos_servicio(
    espacio_muestral: EspacioMuestral,
) -> tuple[set[Resultado], set[Resultado]]:
    """Devuelve los eventos (C: Estándar, D: Exprés) como conjuntos nuevos.

    Recibe S con tuplas (turno, servicio, estado); el componente 1 es servicio.
    En este modelo cada resultado tiene exactamente uno de esos dos servicios:
    los eventos no se traslapan y juntos cubren S.
    """
    # Se filtran posibilidades, sin depender de los despachos observados.
    evento_c = {resultado for resultado in espacio_muestral if resultado[1] == "Estándar"}
    evento_d = {resultado for resultado in espacio_muestral if resultado[1] == "Exprés"}
    return evento_c, evento_d
# ------------------------------------------------------------------------------


# --- NUEVO (2) comparar_pares_eventos() ------------------------------------------
def comparar_pares_eventos(
    espacio_muestral: EspacioMuestral,
    pares: dict[str, tuple[set[Resultado], set[Resultado]]],
) -> pd.DataFrame:
    """Resume dos propiedades independientes para cada par de eventos.

    espacio_muestral define S. pares asocia una etiqueta con dos conjuntos.
    Devuelve una tabla indexada por par con tamaños de intersección/unión y
    booleanos disjuntos/exhaustivos. No modifica los conjuntos recibidos.

    Lanza ValueError si no hay pares o si un evento contiene resultados
    ajenos a S. La cobertura se prueba por igualdad de conjuntos, no sólo
    por igualdad de tamaños: dos conjuntos pueden medir lo mismo y diferir.
    """
    if not pares:
        raise ValueError("Se necesita al menos un par de eventos para comparar.")
    universo = set(espacio_muestral)
    filas = []
    for nombre_par, (primero, segundo) in pares.items():
        if not primero <= universo or not segundo <= universo:
            raise ValueError("Los eventos deben ser subconjuntos del espacio muestral.")
        # Cada operación se calcula una vez y se reutiliza en ambas preguntas.
        interseccion = primero & segundo
        union = primero | segundo
        filas.append(
            {
                "par": nombre_par,
                "tamano_interseccion": len(interseccion),
                "tamano_union": len(union),
                "disjuntos": not interseccion,
                "exhaustivos": union == universo,
            }
        )
    return pd.DataFrame(filas).set_index("par")
# ------------------------------------------------------------------------------


# --- NUEVO (3) construir_figura_pares() ----------------------------------
def construir_figura_pares(
    comparacion: pd.DataFrame, tamano_espacio_muestral: int
) -> plt.Figure:
    """Representa traslape y cobertura de los pares recibidos.

    comparacion es la tabla de comparar_pares_eventos(), con etiquetas en
    su índice. tamano_espacio_muestral es |S|. Devuelve una Figure sin
    modificar la tabla ni escribir archivos; el llamador debe cerrarla.
    """
    # La tabla académica tiene dos columnas de tamaños. melt las organiza
    # como una fila por par y medida, el formato que Seaborn usa para hue.
    # Esta transformación cambia la presentación, no calcula nuevos tamaños.
    tamanos = comparacion[["tamano_interseccion", "tamano_union"]].rename(
        columns={
            "tamano_interseccion": "Intersección",
            "tamano_union": "Unión",
        }
    )
    tamanos = tamanos.rename_axis("par").reset_index().melt(
        id_vars="par", var_name="medida", value_name="resultados"
    )
    # El salto de línea permite leer ambos eventos. La tabla original conserva
    # su índice; el orden se toma de los datos, nunca de etiquetas prefijadas.
    tamanos["par"] = tamanos["par"].str.replace(" / ", "\n", regex=False)

    figura, eje = plt.subplots(figsize=(9.2, 5.2), layout="constrained")
    # hue agrupa y distingue las medidas sin calcular posiciones ni anchos.
    # Son cardinalidades exactas: no corresponde estimar intervalos de error.
    sns.barplot(
        data=tamanos, x="par", y="resultados", hue="medida",
        hue_order=["Intersección", "Unión"],
        estimator="sum", errorbar=None,
        palette={"Intersección": "#EC2661", "Unión": "#1A2E51"}, ax=eje,
    )
    # Un traslape cero indica disyunción. Alcanzar |S| indica cobertura porque
    # comparar_pares_eventos ya verificó que los eventos están dentro de S.
    eje.axhline(
        tamano_espacio_muestral, color="#0039A6", linestyle="--",
        label="Espacio muestral completo",
    )
    eje.set(
        title="Disyunción y exhaustividad",
        xlabel="", ylabel="Número de resultados posibles",
        ylim=(0, tamano_espacio_muestral + 2),
    )
    # bar_label resuelve las posiciones, incluido el cero. Un contenedor
    # corresponde a cada medida, no hace falta recorrer barras individuales.
    for barras in eje.containers:
        eje.bar_label(barras, fmt="%.0f", padding=3)
    eje.legend(title=None, loc="upper left", bbox_to_anchor=(1, 1), frameon=False)
    return figura
# ------------------------------------------------------------------------------


def principal() -> None:
    """Coordina el ejemplo: calcular, visualizar, guardar e informar resultados."""
    # Las funciones de cálculo no imprimen ni escriben archivos. Esta función
    # decide el orden de ejecución y reúne los resultados para el estudiante.
    espacio_muestral = construir_espacio_muestral()
    despachos = simular_despachos()
    evento_a, evento_b = definir_eventos(espacio_muestral)
    evento_c, evento_d = definir_eventos_servicio(espacio_muestral)
    comparacion = comparar_pares_eventos(
        espacio_muestral,
        {
            "A: Noche / B: Retrasado": (evento_a, evento_b),
            "C: Estándar / D: Exprés": (evento_c, evento_d),
        },
    )
    figura = construir_figura_pares(comparacion, len(espacio_muestral))
    ruta_figura = guardar_figura(
        figura, DIRECTORIO_FIGURAS / "teoria_conjuntos_03_eventos_disjuntos.png"
    )

    # El informe mantiene separados los resultados posibles y las observaciones.
    print("================================================================")
    print("LECCIÓN 05 - PASO 3: EVENTOS DISJUNTOS")
    print("================================================================")
    print("Aviso de datos sintéticos           : No se utilizan datos reales de la empresa")
    print(f"Resultados del espacio muestral |S| : {len(espacio_muestral)}")
    print(f"Registros de despachos sintéticos   : {len(despachos)}")
    for nombre_par, fila in comparacion.iterrows():
        print(f"Par                            : {nombre_par}")
        print(f"  Tamaño de intersección        : {int(fila['tamano_interseccion'])}")
        print(f"  Tamaño de unión               : {int(fila['tamano_union'])}")
        print(f"  Mutuamente excluyente         : {bool(fila['disjuntos'])}")
        print(f"  Exhaustivo                    : {bool(fila['exhaustivos'])}")
    print(f"Figura guardada en                  : {ruta_figura}")
    print("================================================================")


# Importar permite revisar las funciones sin ejecutar el ejemplo ni crear PNG.
if __name__ == "__main__":
    principal()

