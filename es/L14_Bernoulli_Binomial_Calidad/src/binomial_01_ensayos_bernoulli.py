"""
Lección 14 - Paso 1: Ensayos de Bernoulli
=========================================
NUEVO EN ESTE PASO: bernoulli_trial(), binomial_assumptions() y save_figure().

Contexto:
Una inspección sintética de una unidad es un ensayo de Bernoulli con
probabilidad de éxito p = 0.08 (la unidad es defectuosa). Repetir ese ensayo
n = 20 veces, de forma independiente y con el mismo p, produce un conteo
binomial X.

Ejecútalo:
    uv run es/L14_Bernoulli_Binomial_Calidad/src/binomial_01_ensayos_bernoulli.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_TRIALS = 20
P_DEFECT = 0.08
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) bernoulli_trial() ---------------------------------------------
def bernoulli_trial() -> dict[str, float]:
    """Devuelve la distribución de dos puntos de una inspección."""
    return {
        "p_defect": P_DEFECT,
        "p_clean": 1.0 - P_DEFECT,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) binomial_assumptions() ----------------------------------------
def binomial_assumptions() -> dict[str, float | int]:
    """Devuelve los ingredientes binomiales n, p, media np y q = 1 - p."""
    return {
        "n": N_TRIALS,
        "p": P_DEFECT,
        "q": 1.0 - P_DEFECT,
        "mean_np": N_TRIALS * P_DEFECT,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(trial: dict[str, float]) -> Path:
    """Guarda la función de masa de dos puntos de Bernoulli."""
    output_path = DIR_FIGURES / "binomial_01_ensayos_bernoulli.png"
    labels = ["Limpio\n(fracaso)", "Defectuoso\n(éxito)"]
    values = [trial["p_clean"], trial["p_defect"]]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Probabilidad")
    ax.set_title("Una inspección de Bernoulli: p = 0.08")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.2f}",
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
    trial = bernoulli_trial()
    assumptions = binomial_assumptions()
    figure_path = save_figure(trial)

    print("================================================================")
    print("LECCIÓN 14 - PASO 1: ENSAYOS DE BERNOULLI")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"P(defectuoso) en un ensayo      : {trial['p_defect']:.6f}")
    print(f"P(limpio) en un ensayo          : {trial['p_clean']:.6f}")
    print(f"Número de ensayos n             : {assumptions['n']}")
    print(f"p constante entre ensayos       : {assumptions['p']:.6f}")
    print(f"q = 1 - p                       : {assumptions['q']:.6f}")
    print(f"Media objetivo np               : {assumptions['mean_np']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

