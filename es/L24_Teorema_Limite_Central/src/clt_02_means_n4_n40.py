"""
Lección 24 - Paso 2: Medias muestrales para n = 4 y n = 40
=========================================================
La Receta
Partir de clt_01_skewed_population.py e introducir:
    1. simulate_means()         5,000 medias muestrales, semilla 42
    2. sampling_summaries()     media, EE y asimetría de xbar
    3. save_figure()            histogramas con superposición normal

Se reconstruye la misma población exponencial de retrasos. Para n = 40 el
histograma de xbar está mucho más cerca de una campana que para n = 4. No
se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MEAN = 10.0
N_SMALL = 4
N_LARGE = 40
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def delay_population():
    """Retorna la población exponencial de retrasos con media 10 minutos."""
    return stats.expon(scale=MEAN)


# --- NUEVO (1) simulate_means() ----------------------------------------------
def simulate_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Extrae n_reps muestras de tamaño n de la población de retrasos."""
    rng = np.random.default_rng(SEED)
    model = delay_population()
    draws = model.rvs(size=(n_reps, n), random_state=rng)
    return draws.mean(axis=1)
# ------------------------------------------------------------------------------


# --- NUEVO (2) sampling_summaries() ------------------------------------------
def sampling_summaries(means: np.ndarray, n: int) -> dict[str, float]:
    """Resume la distribución muestral simulada de xbar."""
    se = MEAN / np.sqrt(n)
    return {
        "n": float(n),
        "mean_of_means": float(np.mean(means)),
        "empirical_se": float(np.std(means, ddof=1)),
        "theoretical_se": se,
        "skewness": float(stats.skew(means, bias=False)),
        "theoretical_skew": 2.0 / np.sqrt(n),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(means_small: np.ndarray, means_large: np.ndarray) -> Path:
    """Histograma de xbar para n = 4 y n = 40 con superposición normal."""
    output_path = DIR_FIGURES / "clt_02_means_n4_n40.png"
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6), sharey=False)
    panels = [
        (axes[0], means_small, N_SMALL, "#5B8DEF"),
        (axes[1], means_large, N_LARGE, "#EC2661"),
    ]
    for ax, means, n, color in panels:
        se = MEAN / np.sqrt(n)
        ax.hist(means, bins=30, density=True, color=color, alpha=0.6,
                edgecolor="#1A2E51")
        grid = np.linspace(means.min(), means.max(), 200)
        ax.plot(grid, stats.norm(MEAN, se).pdf(grid), color="#1A2E51", lw=2.0)
        ax.axvline(MEAN, color="#646464", ls="--", lw=1.2)
        ax.set_title(f"n = {n}")
        ax.set_xlabel("Media muestral xbar")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
    axes[0].set_ylabel("Densidad")
    fig.suptitle("TLC: n = 40 está más cerca de la normal que n = 4")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    means_small = simulate_means(N_SMALL)
    means_large = simulate_means(N_LARGE)
    small = sampling_summaries(means_small, N_SMALL)
    large = sampling_summaries(means_large, N_LARGE)
    figure_path = save_figure(means_small, means_large)

    print("================================================================")
    print("LECCIÓN 24 - PASO 2: MEDIAS N=4 Y N=40")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS:,}")
    print(f"n = 4 media de las medias       : {small['mean_of_means']:.6f}")
    print(f"n = 4 EE teórico                : {small['theoretical_se']:.6f}")
    print(f"n = 4 EE empírico               : {small['empirical_se']:.6f}")
    print(f"n = 4 asimetría teórica         : {small['theoretical_skew']:.6f}")
    print(f"n = 4 asimetría empírica        : {small['skewness']:.6f}")
    print(f"n = 40 media de las medias      : {large['mean_of_means']:.6f}")
    print(f"n = 40 EE teórico               : {large['theoretical_se']:.6f}")
    print(f"n = 40 EE empírico              : {large['empirical_se']:.6f}")
    print(f"n = 40 asimetría teórica        : {large['theoretical_skew']:.6f}")
    print(f"n = 40 asimetría empírica       : {large['skewness']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

