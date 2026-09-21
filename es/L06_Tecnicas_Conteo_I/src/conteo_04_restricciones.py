"""
Lección 06 - Paso 4: Restricciones que interactúan y sobreconteo
===============================================================
NUEVO EN ESTE PASO: conteo_ingenuo_falla(), descomposicion_correcta() y
verificacion_exhaustiva().

La Receta
CAMBIOS RESPECTO A conteo_03_combinaciones.py
Introdúcelos en este orden:
    1. conteo_ingenuo_falla()          elige categorías obligatorias antes de llenar cupos
    2. descomposicion_correcta()       retira grupos inválidos del universo completo
    3. verificacion_exhaustiva()       verifica cada grupo candidato de cuatro personas
    4. guardar_grafica_desglose()      muestra cómo las dos restricciones reducen el conteo

Ejecútalo:
    uv run es/L06_Tecnicas_Conteo_I/src/conteo_04_restricciones.py
"""

from itertools import combinations
import math
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR_FIGURAS = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURAS.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) conteo_ingenuo_falla() -----------------------------------------
def conteo_ingenuo_falla(n_o: int, n_d: int, k: int) -> int:
    """
    Error clásico de estudiante:
    'Elijo 1 analista de operaciones (5), elijo 1 especialista de datos (4) y
    luego los 2 restantes de los 7 candidatos que quedan: 5 * 4 * binom(7, 2) = 420'.
    Falla de forma catastrófica porque sobrecuenta el orden de selección.
    """
    return n_o * n_d * math.comb((n_o + n_d) - 2, k - 2)
# ------------------------------------------------------------------------------


# --- NUEVO (2) descomposicion_correcta() --------------------------------------
def descomposicion_correcta(n_o: int, n_d: int, k: int) -> tuple[int, int, int, int]:
    """
    Conteo riguroso por el principio del complemento:
        Universo total                 = binom(9, 4) = 126
        Solo analistas de operaciones  = binom(5, 4) = 5
        Solo especialistas de datos    = binom(4, 4) = 1
        Grupos mixtos                  = 126 - 5 - 1 = 120
        Grupos con conflicto {O1, D1}:
            Fijando O1 y D1, elijo 2 de los 7 restantes = binom(7, 2) = 21
        Total de grupos válidos        = 120 - 21 = 99
    """
    total_universo = math.comb(n_o + n_d, k)
    solo_operaciones = math.comb(n_o, k)
    solo_datos = math.comb(n_d, k)
    grupos_mixtos = total_universo - solo_operaciones - solo_datos

    # Grupos que contienen tanto a O1 como a D1
    conflicto_ambos = math.comb((n_o + n_d) - 2, k - 2)
    grupos_validos = grupos_mixtos - conflicto_ambos

    return total_universo, grupos_mixtos, conflicto_ambos, grupos_validos
# ------------------------------------------------------------------------------


# --- NUEVO (3) verificacion_exhaustiva() --------------------------------------
def verificacion_exhaustiva(
    analistas_operaciones: list[str], especialistas_datos: list[str], k: int
) -> list[tuple[str, ...]]:
    """Filtra todos los subconjuntos candidatos de tamaño k con ambas restricciones."""
    todos_candidatos = analistas_operaciones + especialistas_datos
    grupos_validos = []

    for grupo in combinations(todos_candidatos, k):
        tiene_operaciones = any(miembro in analistas_operaciones for miembro in grupo)
        tiene_datos = any(miembro in especialistas_datos for miembro in grupo)
        conflicto = ("O1" in grupo) and ("D1" in grupo)

        if tiene_operaciones and tiene_datos and not conflicto:
            grupos_validos.append(grupo)

    return grupos_validos
# ------------------------------------------------------------------------------


# --- NUEVO (4) guardar_grafica_desglose() -------------------------------------
def guardar_grafica_desglose(universo: int, no_diversos: int, conflicto: int, validos: int) -> None:
    """Gráfica de cascada que ilustra cómo las restricciones filtran el universo."""
    categorias = ["Todos los\ngrupos", "Una disciplina\nexcluida", "Conflicto\nexcluido", "Grupos\nválidos"]
    valores = [universo, no_diversos, conflicto, validos]
    colores = ["#646464", "#EC2661", "#EC2661", "#0039A6"]

    fig, ax = plt.subplots(figsize=(7.5, 4))
    barras = ax.bar(categorias, valores, color=colores, edgecolor="#1A2E51", linewidth=1.2)
    ax.set_title("Filtrado de grupos de revisión de cuatro personas", fontsize=14, fontweight="bold", pad=12)
    ax.set_ylabel("Número de grupos", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f"{altura}", xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    ruta_salida = DIR_FIGURAS / "conteo_04_restricciones.png"
    plt.savefig(ruta_salida, dpi=150)
    plt.close()
# ------------------------------------------------------------------------------


def main() -> None:
    analistas_operaciones = ["O1", "O2", "O3", "O4", "O5"]
    especialistas_datos = ["D1", "D2", "D3", "D4"]
    k = 4

    error_ingenuo = conteo_ingenuo_falla(len(analistas_operaciones), len(especialistas_datos), k)
    universo, mixtos, conflicto, validos_teoricos = descomposicion_correcta(
        len(analistas_operaciones), len(especialistas_datos), k
    )

    una_disciplina = universo - mixtos
    guardar_grafica_desglose(universo, una_disciplina, conflicto, validos_teoricos)

    grupos_reales = verificacion_exhaustiva(analistas_operaciones, especialistas_datos, k)
    total_real = len(grupos_reales)

    print("================================================================")
    print("LECCIÓN 06 - PASO 4: RESTRICCIONES QUE INTERACTÚAN")
    print("================================================================")
    print("Aviso de datos sintéticos                 : No se usan datos reales de empresa")
    print(
        f"Candidatos: {len(analistas_operaciones)} analistas de operaciones + "
        f"{len(especialistas_datos)} especialistas de datos = 9; tamaño del grupo k = 4"
    )
    print(f"Universo total binom(9, 4)                : {universo}")
    print(f"CÁLCULO INGENUO ERRÓNEO (la trampa)       : {error_ingenuo}  <-- ¡SOBRECONTEO!")
    print(f"Grupos de una disciplina excluidos        : {una_disciplina}")
    print(f"Grupos excluidos por ('O1', 'D1')         : {conflicto}")
    print(f"Total teórico por complemento             : {validos_teoricos}")
    print(f"Conteo exhaustivo por fuerza bruta        : {total_real}")
    print(f"Coincidencia exacta                       : {validos_teoricos == total_real}")
    print(f"Primeros 3 grupos válidos                 : {grupos_reales[:3]}")
    print(f"Figura guardada en                        : {DIR_FIGURAS / 'conteo_04_restricciones.png'}")
    print("================================================================")


if __name__ == "__main__":
    main()

