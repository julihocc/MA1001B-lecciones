"""
Lección 26 - Paso 1: Dos estimadores insesgados de mu
=====================================================
NUEVO EN ESTE PASO: population_model(), estimator_means() y save_figure().

La Receta
Un reloj de costos sintético es Normal(mu=100, sigma=15). Se comparan dos
estimadores de mu: la media muestral xbar de n = 20 y la primera
observación X1. Ambos son insesgados: sus medias muestrales recuperan 100.

Ejecútalo:
    uv run es/L26_Estimacion_Puntual_Propiedades/src/point_estimation_01_unbiasedness.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 100.0
SIGMA = 15.0
N = 20
N_REPS = 8_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) population_model() --------------------------------------------
def population_model():
    """Retorna la población sintética de costos Normal(100, 15)."""
    return stats.norm(loc=MU, scale=SIGMA)
# ------------------------------------------------------------------------------


# --- NUEVO (2) estimator_means() ---------------------------------------------
def estimator_means(n: int = N, n_reps: int = N_REPS) -> dict[str, np.ndarray]:
    """Simula xbar y el estimador de una observación X1."""
    rng = np.random.default_rng(SEED)
    draws = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))
    return {
        "xbar": draws.mean(axis=1),
        "one_obs": draws[:, 0],
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(estimators: dict[str, np.ndarray]) -> Path:
    """Compara medias muestrales de xbar y de la primera observación."""
    output_path = DIR_FIGURES / "point_estimation_01_unbiasedness.png"
    labels = ["Media muestral\nxbar, n=20", "Una observación\nX1"]
    means = [float(np.mean(estimators["xbar"])),
             float(np.mean(estimators["one_obs"]))]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, means, color=colors, width=0.55)
    ax.axhline(MU, color="#646464", ls="--", lw=1.3, label="mu verdadera = 100")
    ax.set_ylabel("Media del estimador")
    ax.set_title("Ambos estimadores recuperan mu = 100: insesgadez")
    ax.set_ylim(90, 110)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    for bar, value in zip(bars, means):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.6,
            f"{value:.3f}",
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
    estimators = estimator_means()
    mean_xbar = float(np.mean(estimators["xbar"]))
    mean_one = float(np.mean(estimators["one_obs"]))
    figure_path = save_figure(estimators)

    print("================================================================")
    print("LECCIÓN 26 - PASO 1: INSESGÁDEZ")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS:,}")
    print(f"mu verdadera                    : {MU:.6f}")
    print(f"Media de xbar (n = 20)          : {mean_xbar:.6f}")
    print(f"Sesgo de xbar                   : {mean_xbar - MU:.6f}")
    print(f"Media de X1                     : {mean_one:.6f}")
    print(f"Sesgo de X1                     : {mean_one - MU:.6f}")
    print("Ambos estimadores son insesgados")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

