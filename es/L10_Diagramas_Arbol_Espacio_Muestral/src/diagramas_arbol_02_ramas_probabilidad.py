"""
Lección 10 - Paso 2: Etiquetas de probabilidad y multiplicación de caminos
==========================================================================
NUEVO EN ESTE PASO: branch_probabilities(), path_probabilities() y save_figure().

CAMBIOS RESPECTO A diagramas_arbol_01_arbol_frecuencias.py
La Receta
---------
Introduce estos cambios en este orden:
    1. branch_probabilities()   convierte frecuencias en probabilidades de rama
    2. path_probabilities()     multiplica a lo largo de ramas; suma caminos disjuntos
    3. save_figure()            compara las cuatro probabilidades de caminos terminales

El mismo registro sintético de 100 lotes se reconstruye a partir de las mismas
constantes. No se importa ningún script anterior de la lección.

Ejecútalo:
    uv run es/L10_Diagramas_Arbol_Espacio_Muestral/src/diagramas_arbol_02_ramas_probabilidad.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SEED = 42
N_LOTS = 100
N_DEFECTIVE = 10
N_CLEAN = 90
N_FLAGGED_DEFECTIVE = 8
N_MISSED_DEFECTIVE = 2
N_FLAGGED_CLEAN = 9
N_CLEARED_CLEAN = 81
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) branch_probabilities() ----------------------------------------
def branch_probabilities() -> dict[str, float]:
    """Convierte frecuencias de primera y segunda etapa en probabilidades de rama."""
    return {
        "p_defective": N_DEFECTIVE / N_LOTS,
        "p_clean": N_CLEAN / N_LOTS,
        "p_flagged_given_defective": N_FLAGGED_DEFECTIVE / N_DEFECTIVE,
        "p_missed_given_defective": N_MISSED_DEFECTIVE / N_DEFECTIVE,
        "p_flagged_given_clean": N_FLAGGED_CLEAN / N_CLEAN,
        "p_cleared_given_clean": N_CLEARED_CLEAN / N_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) path_probabilities() ------------------------------------------
def path_probabilities(branches: dict[str, float]) -> dict[str, float]:
    """Multiplica a lo largo de cada rama y suma los dos caminos marcados."""
    p_def_flag = (
        branches["p_defective"] * branches["p_flagged_given_defective"]
    )
    p_def_miss = (
        branches["p_defective"] * branches["p_missed_given_defective"]
    )
    p_clean_flag = branches["p_clean"] * branches["p_flagged_given_clean"]
    p_clean_clear = branches["p_clean"] * branches["p_cleared_given_clean"]
    return {
        "defective_flagged": p_def_flag,
        "defective_missed": p_def_miss,
        "clean_flagged": p_clean_flag,
        "clean_cleared": p_clean_clear,
        "flagged": p_def_flag + p_clean_flag,
        "total": p_def_flag + p_def_miss + p_clean_flag + p_clean_clear,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(paths: dict[str, float]) -> Path:
    """Guarda las cuatro probabilidades de caminos mutuamente excluyentes."""
    output_path = DIR_FIGURES / "diagramas_arbol_02_probabilidades_caminos.png"
    labels = [
        "Defectuoso\ny marcado",
        "Defectuoso\ny omitido",
        "Limpio\ny marcado",
        "Limpio\ny liberado",
    ]
    values = np.array(
        [
            paths["defective_flagged"],
            paths["defective_missed"],
            paths["clean_flagged"],
            paths["clean_cleared"],
        ]
    )
    colors = ["#EC2661", "#F4A6B8", "#5B8DEF", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Probabilidad del camino")
    ax.set_title("Multiplicar a lo largo de ramas; sumar caminos mutuamente excluyentes")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    branches = branch_probabilities()
    paths = path_probabilities(branches)
    figure_path = save_figure(paths)

    print("================================================================")
    print("LECCIÓN 10 - PASO 2: RAMAS DE PROBABILIDAD")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"P(defectuoso)                   : {branches['p_defective']:.6f}")
    print(f"P(limpio)                       : {branches['p_clean']:.6f}")
    print(
        "P(marcado | defectuoso)         : "
        f"{branches['p_flagged_given_defective']:.6f}"
    )
    print(
        "P(omitido | defectuoso)         : "
        f"{branches['p_missed_given_defective']:.6f}"
    )
    print(
        "P(marcado | limpio)             : "
        f"{branches['p_flagged_given_clean']:.6f}"
    )
    print(
        "P(liberado | limpio)            : "
        f"{branches['p_cleared_given_clean']:.6f}"
    )
    print(f"P(defectuoso y marcado)         : {paths['defective_flagged']:.6f}")
    print(f"P(defectuoso y omitido)         : {paths['defective_missed']:.6f}")
    print(f"P(limpio y marcado)             : {paths['clean_flagged']:.6f}")
    print(f"P(limpio y liberado)            : {paths['clean_cleared']:.6f}")
    print(f"P(marcado) = suma de caminos    : {paths['flagged']:.6f}")
    print(f"Suma de los cuatro caminos      : {paths['total']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

