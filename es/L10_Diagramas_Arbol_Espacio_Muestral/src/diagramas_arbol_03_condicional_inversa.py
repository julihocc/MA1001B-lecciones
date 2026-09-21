"""
Lección 10 - Paso 3: Condicional inversa a partir de caminos combinados
=======================================================================
NUEVO EN ESTE PASO: reverse_conditional(), simulate_lots() y save_figure().

CAMBIOS RESPECTO A diagramas_arbol_02_ramas_probabilidad.py
La Receta
---------
Introduce estos cambios en este orden:
    1. reverse_conditional()   P(defectuoso | marcado) a partir de caminos marcados
    2. simulate_lots()         comprobación con semilla 42 de la condicional inversa
    3. save_figure()           contrasta una etiqueta de rama con la pregunta invertida

El árbol se dibuja en orden temporal: estado del lote, luego inspección.
P(marcado | defectuoso) es una sola rama hacia abajo. P(defectuoso | marcado)
no lo es. Esa inversión es el límite que la Lección 11 nombra como teorema de
Bayes.

Ejecútalo:
    uv run es/L10_Diagramas_Arbol_Espacio_Muestral/src/diagramas_arbol_03_condicional_inversa.py
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
N_SIMULATIONS = 100_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) reverse_conditional() -----------------------------------------
def reverse_conditional() -> dict[str, float]:
    """Calcula la condicional inversa combinando los dos caminos marcados."""
    p_defective = N_DEFECTIVE / N_LOTS
    p_flagged_given_defective = N_FLAGGED_DEFECTIVE / N_DEFECTIVE
    p_flagged_given_clean = N_FLAGGED_CLEAN / N_CLEAN
    p_defective_and_flagged = p_defective * p_flagged_given_defective
    p_clean_and_flagged = (1.0 - p_defective) * p_flagged_given_clean
    p_flagged = p_defective_and_flagged + p_clean_and_flagged
    p_defective_given_flagged = p_defective_and_flagged / p_flagged
    return {
        "p_flagged_given_defective": p_flagged_given_defective,
        "p_defective": p_defective,
        "p_flagged": p_flagged,
        "p_defective_given_flagged": p_defective_given_flagged,
        "frequency_defective_given_flagged": (
            N_FLAGGED_DEFECTIVE / (N_FLAGGED_DEFECTIVE + N_FLAGGED_CLEAN)
        ),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) simulate_lots() -----------------------------------------------
def simulate_lots() -> float:
    """Simula el árbol de dos etapas y estima P(defectuoso | marcado)."""
    rng = np.random.default_rng(SEED)
    is_defective = rng.random(N_SIMULATIONS) < (N_DEFECTIVE / N_LOTS)
    p_flag = np.where(
        is_defective,
        N_FLAGGED_DEFECTIVE / N_DEFECTIVE,
        N_FLAGGED_CLEAN / N_CLEAN,
    )
    is_flagged = rng.random(N_SIMULATIONS) < p_flag
    return float(np.mean(is_defective[is_flagged]))
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    branch_label: float,
    reversed_exact: float,
    reversed_simulated: float,
) -> Path:
    """Contrasta la rama hacia abajo con la condicional inversa."""
    output_path = DIR_FIGURES / "diagramas_arbol_03_condicional_inversa.png"
    labels = [
        "P(marcado |\ndefectuoso)\nrama",
        "P(defectuoso |\nmarcado)\ncaminos combinados",
        "Simulación\nsemilla 42",
    ]
    values = [branch_label, reversed_exact, reversed_simulated]
    colors = ["#1A2E51", "#EC2661", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Probabilidad")
    ax.set_title("Un árbol en orden temporal no muestra la condicional inversa")
    ax.set_ylim(0, 1.05)
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
    results = reverse_conditional()
    simulated = simulate_lots()
    figure_path = save_figure(
        results["p_flagged_given_defective"],
        results["p_defective_given_flagged"],
        simulated,
    )

    print("================================================================")
    print("LECCIÓN 10 - PASO 3: CONDICIONAL INVERSA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Lotes simulados                 : {N_SIMULATIONS:,}")
    print(
        "P(marcado | defectuoso)         : "
        f"{results['p_flagged_given_defective']:.6f}"
    )
    print(f"P(defectuoso)                   : {results['p_defective']:.6f}")
    print(f"P(marcado)                      : {results['p_flagged']:.6f}")
    print(
        "P(defectuoso | marcado)         : "
        f"{results['p_defective_given_flagged']:.6f}"
    )
    print(
        "Comprobación de frecuencia 8/17 : "
        f"{results['frequency_defective_given_flagged']:.6f}"
    )
    print(f"Simulación semilla 42           : {simulated:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

