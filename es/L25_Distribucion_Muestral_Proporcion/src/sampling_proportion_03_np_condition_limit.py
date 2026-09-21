"""
Lección 25 - Paso 3: La aproximación normal falla cuando np < 5
==============================================================
La Receta
Partir de sampling_proportion_02_simulation.py e introducir:
    1. small_sample_phat()      n = 20, p = 0.18 de modo que np = 3.6 < 5
    2. discrete_vs_normal()     P(phat = 0) y un histograma asimétrico
    3. save_figure()            tallo de phat posibles versus una campana

La regla np < 5 (o n(1-p) < 5) es el límite. Una muestra de 20 indicadores
de entrega tardía es demasiado pequeña para el modelo normal de phat.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
P = 0.18
N_SMALL = 20
N_REPS = 5_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) small_sample_phat() -------------------------------------------
def small_sample_phat(n: int = N_SMALL, n_reps: int = N_REPS) -> np.ndarray:
    """Extrae n_reps proporciones muestrales de Binomial(20, 0.18)."""
    rng = np.random.default_rng(SEED)
    successes = rng.binomial(n=n, p=P, size=n_reps)
    return successes / n
# ------------------------------------------------------------------------------


# --- NUEVO (2) discrete_vs_normal() ------------------------------------------
def discrete_vs_normal(phats: np.ndarray, n: int = N_SMALL) -> dict[str, float]:
    """Contrasta la ley discreta de phat con el modelo normal ilegal."""
    se = float(np.sqrt(P * (1.0 - P) / n))
    p_zero = float(stats.binom.pmf(0, n=n, p=P))
    normal_p_zero = float(stats.norm(P, se).cdf(0.5 / n))
    return {
        "n": float(n),
        "np": n * P,
        "n_one_minus_p": n * (1.0 - P),
        "se": se,
        "empirical_mean": float(np.mean(phats)),
        "empirical_se": float(np.std(phats, ddof=1)),
        "p_phat_zero": p_zero,
        "simulated_p_zero": float(np.mean(phats == 0.0)),
        "normal_near_zero": normal_p_zero,
        "skewness": float(stats.skew(phats, bias=False)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(summary: dict[str, float]) -> Path:
    """Tallo de la pmf exacta Binomial(20, 0.18) contra una superposición normal."""
    output_path = DIR_FIGURES / "sampling_proportion_03_np_condition_limit.png"
    n = N_SMALL
    ks = np.arange(0, n + 1)
    phat_grid = ks / n
    pmf = stats.binom.pmf(ks, n=n, p=P)
    se = summary["se"]
    x = np.linspace(-0.05, 0.55, 300)
    normal_y = stats.norm(P, se).pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, normal_y, color="#5B8DEF", lw=2.0, label="Curva normal ilegal")
    ax.vlines(phat_grid, 0, pmf * n, color="#1A2E51", lw=1.6)
    ax.plot(phat_grid, pmf * n, "o", color="#EC2661", label="Binomial exacta")
    ax.set_xlabel("Proporción muestral phat")
    ax.set_ylabel("Escala de densidad")
    ax.set_title("np = 3.6 < 5: el modelo normal de phat falla")
    ax.set_xlim(-0.05, 0.55)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    phats = small_sample_phat()
    summary = discrete_vs_normal(phats)
    figure_path = save_figure(summary)

    print("================================================================")
    print("LECCIÓN 25 - PASO 3: LÍMITE DE LA CONDICIÓN NP")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"n pequeño                       : {int(summary['n'])}")
    print(f"np                              : {summary['np']:.6f}")
    print(f"n(1 - p)                        : {summary['n_one_minus_p']:.6f}")
    print(f"EE de fórmula                   : {summary['se']:.6f}")
    print(f"Media empírica de phat          : {summary['empirical_mean']:.6f}")
    print(f"EE empírico                     : {summary['empirical_se']:.6f}")
    print(f"P exacta (phat = 0)             : {summary['p_phat_zero']:.6f}")
    print(f"P simulada (phat = 0)           : {summary['simulated_p_zero']:.6f}")
    print(f"Masa normal cerca de 0          : {summary['normal_near_zero']:.6f}")
    print(f"Asimetría de phat               : {summary['skewness']:.6f}")
    print("Límite: np < 5 hace fallar la aproximación normal")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

