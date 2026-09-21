"""
Lección 11 - Paso 1: Priori y verosimilitudes
=============================================
NUEVO EN ESTE PASO: prior_probability(), likelihoods() y save_figure().

Contexto:
El árbol de inspección de 100 lotes de la Lección 10 continúa aquí. La priori
es la tasa de defectuosos antes de ver la marca: P(D)=0.10. Las
verosimilitudes son las tasas de marca dadas cada estado: P(F|D)=0.80 y
P(F|C)=0.10. El teorema de Bayes combinará estas piezas en el Paso 2.

Ejecútalo:
    uv run es/L11_Teorema_Bayes_Actualizacion/src/bayes_01_priori_verosimilitud.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SEED = 42
P_DEFECTIVE = 0.10
P_CLEAN = 0.90
P_FLAGGED_GIVEN_DEFECTIVE = 0.80
P_FLAGGED_GIVEN_CLEAN = 0.10
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) prior_probability() -------------------------------------------
def prior_probability() -> dict[str, float]:
    """Devuelve la priori de la primera etapa antes de observar la marca."""
    return {
        "p_defective": P_DEFECTIVE,
        "p_clean": P_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) likelihoods() -------------------------------------------------
def likelihoods() -> dict[str, float]:
    """Devuelve las verosimilitudes de marca dado defectuoso y dado limpio."""
    return {
        "p_flagged_given_defective": P_FLAGGED_GIVEN_DEFECTIVE,
        "p_flagged_given_clean": P_FLAGGED_GIVEN_CLEAN,
        "p_cleared_given_defective": 1.0 - P_FLAGGED_GIVEN_DEFECTIVE,
        "p_cleared_given_clean": 1.0 - P_FLAGGED_GIVEN_CLEAN,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(prior: dict[str, float], like: dict[str, float]) -> Path:
    """Guarda una comparación de la priori y las dos verosimilitudes de marca."""
    output_path = DIR_FIGURES / "bayes_01_priori_verosimilitud.png"
    labels = [
        "Priori\nP(D)",
        "Verosimilitud\nP(F | D)",
        "Verosimilitud\nP(F | C)",
    ]
    values = np.array(
        [
            prior["p_defective"],
            like["p_flagged_given_defective"],
            like["p_flagged_given_clean"],
        ]
    )
    colors = ["#1A2E51", "#EC2661", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Probabilidad")
    ax.set_title("Tasa priori de defectuosos y verosimilitudes de marca")
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
    prior = prior_probability()
    like = likelihoods()
    figure_path = save_figure(prior, like)

    print("================================================================")
    print("LECCIÓN 11 - PASO 1: PRIORI Y VEROSIMILITUDES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"P(defectuoso) priori            : {prior['p_defective']:.6f}")
    print(f"P(limpio) priori                : {prior['p_clean']:.6f}")
    print(
        "P(marcado | defectuoso)         : "
        f"{like['p_flagged_given_defective']:.6f}"
    )
    print(
        "P(marcado | limpio)             : "
        f"{like['p_flagged_given_clean']:.6f}"
    )
    print(
        "P(liberado | defectuoso)        : "
        f"{like['p_cleared_given_defective']:.6f}"
    )
    print(
        "P(liberado | limpio)            : "
        f"{like['p_cleared_given_clean']:.6f}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

