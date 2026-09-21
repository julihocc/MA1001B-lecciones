"""
Lección 18 - Paso 1: Tiempo de espera geométrico
================================================
NUEVO EN ESTE PASO: geometric_parameters(), geometric_probabilities() y
save_figure().

La Receta
Una auditoría completamente sintética muestrea unidades independientes hasta
encontrar el primer defectuoso. Cada ensayo tiene probabilidad de éxito
p = 0.12. El tiempo de espera X es el número de ensayo del primer éxito, de
modo que P(X = 1) = p y E[X] = 1/p.

Ejecútalo:
    uv run es/L18_Geometrica_Binomial_Negativa/src/tiempos_espera_01_geometrica.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
P_SUCCESS = 0.12
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) geometric_parameters() ----------------------------------------
def geometric_parameters() -> dict[str, float]:
    """Devuelve p y E[X] = 1/p para ensayos hasta el primer éxito."""
    return {
        "p": P_SUCCESS,
        "mean": 1.0 / P_SUCCESS,
        "variance": (1.0 - P_SUCCESS) / P_SUCCESS ** 2,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) geometric_probabilities() -------------------------------------
def geometric_probabilities() -> dict[str, float]:
    """Devuelve P(X = 1) y P(X <= 5) para X ~ Geométrica(p)."""
    model = stats.geom(p=P_SUCCESS)
    return {
        "p_first_trial": float(model.pmf(1)),
        "p_at_most_five": float(model.cdf(5)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure() -> Path:
    """Guarda la FMP geométrica de los tiempos de espera."""
    output_path = DIR_FIGURES / "tiempos_espera_01_geometrica.png"
    xs = np.arange(1, 21)
    masses = stats.geom.pmf(xs, p=P_SUCCESS)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color="#1A2E51", width=0.8)
    ax.bar([1], [masses[0]], color="#EC2661", width=0.8)
    ax.set_xlabel("Ensayo del primer éxito x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Geométrica(p = 0.12): P(X = 1) = p")
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    params = geometric_parameters()
    probs = geometric_probabilities()
    scipy_mean = float(stats.geom.mean(p=P_SUCCESS))
    figure_path = save_figure()

    print("================================================================")
    print("LECCIÓN 18 - PASO 1: TIEMPO DE ESPERA GEOMÉTRICO")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"p                                : {params['p']:.6f}")
    print(f"P(X = 1)                         : {probs['p_first_trial']:.6f}")
    print(f"P(X <= 5)                        : {probs['p_at_most_five']:.6f}")
    print(f"E[X] = 1/p                       : {params['mean']:.6f}")
    print(f"Media geom de scipy              : {scipy_mean:.6f}")
    print(f"Var(X)                           : {params['variance']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

