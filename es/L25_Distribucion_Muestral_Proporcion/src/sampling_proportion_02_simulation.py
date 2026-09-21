"""
Lección 25 - Paso 2: Distribución muestral simulada de phat
==========================================================
La Receta
Partir de sampling_proportion_01_se_phat.py e introducir:
    1. simulate_phat()          5,000 muestras binomiales de n = 120, semilla 42
    2. empirical_summaries()    media y EE de phat versus p y EE de fórmula
    3. save_figure()            histograma de phat con superposición normal

Se reconstruye la misma proporción de entrega tardía p = 0.18. No se
importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
P = 0.18
N = 120
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def proportion_se(p: float = P, n: int = N) -> float:
    """Retorna EE(phat) = sqrt(p (1 - p) / n)."""
    return float(np.sqrt(p * (1.0 - p) / n))


# --- NUEVO (1) simulate_phat() -----------------------------------------------
def simulate_phat(n: int = N, n_reps: int = N_REPS) -> np.ndarray:
    """Extrae n_reps proporciones muestrales de Binomial(n, p)."""
    rng = np.random.default_rng(SEED)
    successes = rng.binomial(n=n, p=P, size=n_reps)
    return successes / n
# ------------------------------------------------------------------------------


# --- NUEVO (2) empirical_summaries() -----------------------------------------
def empirical_summaries(phats: np.ndarray, n: int = N) -> dict[str, float]:
    """Compara media y EE simulados de phat con las fórmulas."""
    se = proportion_se(P, n)
    return {
        "mean_phat": float(np.mean(phats)),
        "empirical_se": float(np.std(phats, ddof=1)),
        "theoretical_se": se,
        "p_gt_0_22": float(np.mean(phats > 0.22)),
        "normal_p_gt_0_22": float(1.0 - stats.norm(P, se).cdf(0.22)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(phats: np.ndarray) -> Path:
    """Histograma de 5,000 valores de phat contra N(p, EE)."""
    output_path = DIR_FIGURES / "sampling_proportion_02_simulation.png"
    se = proportion_se()
    grid = np.linspace(P - 4 * se, P + 4 * se, 200)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(phats, bins=25, density=True, color="#5B8DEF", alpha=0.6,
            edgecolor="#1A2E51", label="phat con semilla 42")
    ax.plot(grid, stats.norm(P, se).pdf(grid), color="#1A2E51", lw=2.2,
            label="Aproximación normal")
    ax.axvline(P, color="#EC2661", ls="--", lw=1.3, label="p = 0.18")
    ax.set_xlabel("Proporción muestral phat")
    ax.set_ylabel("Densidad")
    ax.set_title("5,000 muestras de n = 120 recuperan EE(phat)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    phats = simulate_phat()
    summary = empirical_summaries(phats)
    figure_path = save_figure(phats)

    print("================================================================")
    print("LECCIÓN 25 - PASO 2: SIMULACIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS:,}")
    print(f"Media de phat                   : {summary['mean_phat']:.6f}")
    print(f"EE teórico                      : {summary['theoretical_se']:.6f}")
    print(f"EE empírico                     : {summary['empirical_se']:.6f}")
    print(f"P simulada (phat > 0.22)        : {summary['p_gt_0_22']:.6f}")
    print(f"P normal (phat > 0.22)          : {summary['normal_p_gt_0_22']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

