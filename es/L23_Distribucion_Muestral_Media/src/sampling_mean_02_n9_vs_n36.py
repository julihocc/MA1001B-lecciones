"""
Lección 23 - Paso 2: Distribuciones muestrales simuladas
========================================================
La Receta
Partir de sampling_mean_01_standard_error.py e introducir:
    1. simulate_sample_means()  5,000 muestras iid de tamaño n, semilla 42
    2. empirical_se()           sd observada de xbar versus sigma / sqrt(n)
    3. save_figure()            histogramas de xbar para n = 9 y n = 36

Se reconstruye la misma población Normal(80, 12). No se importa ningún
script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 80.0
SIGMA = 12.0
N_SMALL = 9
N_LARGE = 36
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def standard_error(n: int, sigma: float = SIGMA) -> float:
    """Retorna EE = sigma / sqrt(n) para una media muestral iid."""
    return sigma / np.sqrt(n)


# --- NUEVO (1) simulate_sample_means() ---------------------------------------
def simulate_sample_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Extrae n_reps muestras iid de tamaño n y retorna las medias muestrales."""
    rng = np.random.default_rng(SEED)
    draws = rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))
    return draws.mean(axis=1)
# ------------------------------------------------------------------------------


# --- NUEVO (2) empirical_se() ------------------------------------------------
def empirical_se(means: np.ndarray, n: int) -> dict[str, float]:
    """Compara la sd observada de xbar con el EE teórico."""
    return {
        "n": float(n),
        "mean_of_means": float(np.mean(means)),
        "empirical_se": float(np.std(means, ddof=1)),
        "theoretical_se": standard_error(n),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(means_small: np.ndarray, means_large: np.ndarray) -> Path:
    """Histogramas de las distribuciones muestrales simuladas lado a lado."""
    output_path = DIR_FIGURES / "sampling_mean_02_n9_vs_n36.png"
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6), sharey=True)
    panels = [
        (axes[0], means_small, N_SMALL, "#5B8DEF"),
        (axes[1], means_large, N_LARGE, "#EC2661"),
    ]
    for ax, means, n, color in panels:
        ax.hist(means, bins=30, density=True, color=color, alpha=0.6,
                edgecolor="#1A2E51")
        grid = np.linspace(means.min(), means.max(), 200)
        ax.plot(grid, stats.norm(MU, standard_error(n)).pdf(grid),
                color="#1A2E51", lw=2.0)
        ax.axvline(MU, color="#646464", ls="--", lw=1.2)
        ax.set_title(f"n = {n}")
        ax.set_xlabel("Media muestral xbar")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
    axes[0].set_ylabel("Densidad")
    fig.suptitle("5,000 muestras con semilla 42 recuperan EE = sigma / sqrt(n)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    means_small = simulate_sample_means(N_SMALL)
    means_large = simulate_sample_means(N_LARGE)
    small = empirical_se(means_small, N_SMALL)
    large = empirical_se(means_large, N_LARGE)
    figure_path = save_figure(means_small, means_large)

    print("================================================================")
    print("LECCIÓN 23 - PASO 2: N=9 VERSUS N=36")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS:,}")
    print(f"n = 9 media de las medias       : {small['mean_of_means']:.6f}")
    print(f"n = 9 EE teórico                : {small['theoretical_se']:.6f}")
    print(f"n = 9 EE empírico               : {small['empirical_se']:.6f}")
    print(f"n = 36 media de las medias      : {large['mean_of_means']:.6f}")
    print(f"n = 36 EE teórico               : {large['theoretical_se']:.6f}")
    print(f"n = 36 EE empírico              : {large['empirical_se']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

