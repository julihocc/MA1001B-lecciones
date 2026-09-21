"""
Lección 26 - Paso 3: La insesgadez no implica varianza pequeña
=============================================================
La Receta
Partir de point_estimation_02_efficiency_consistency.py e introducir:
    1. small_sample_xbar()      n = 5, todavía insesgado
    2. decision_error_rate()    P(|xbar - mu| > 10) en n = 5 versus n = 200
    3. save_figure()            contrastar las dos dispersiones muestrales

Un estimador insesgado puede seguir siendo demasiado ruidoso para una
decisión. En n = 5, xbar recupera 100 en promedio pero a menudo yerra mu
por más de 10.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 100.0
SIGMA = 15.0
N_TINY = 5
N_LARGE = 200
TOLERANCE = 10.0
N_REPS = 8_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def draw_means(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Extrae n_reps medias muestrales de tamaño n de N(100, 15)."""
    rng = np.random.default_rng(SEED)
    return rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n)).mean(axis=1)


# --- NUEVO (1) small_sample_xbar() -------------------------------------------
def small_sample_xbar() -> np.ndarray:
    """Simula xbar a partir de muestras de tamaño 5."""
    return draw_means(N_TINY)
# ------------------------------------------------------------------------------


# --- NUEVO (2) decision_error_rate() -----------------------------------------
def decision_error_rate(means: np.ndarray, n: int) -> dict[str, float]:
    """Reporta sesgo, dispersión y P(|xbar - mu| > 10)."""
    return {
        "n": float(n),
        "mean": float(np.mean(means)),
        "bias": float(np.mean(means) - MU),
        "sd": float(np.std(means, ddof=1)),
        "formula_se": SIGMA / np.sqrt(n),
        "p_miss_10": float(np.mean(np.abs(means - MU) > TOLERANCE)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(tiny: np.ndarray, large: np.ndarray) -> Path:
    """Superpone las distribuciones muestrales de xbar en n = 5 y n = 200."""
    output_path = DIR_FIGURES / "point_estimation_03_small_sample_variance.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(tiny, bins=30, density=True, color="#EC2661", alpha=0.45,
            edgecolor="#1A2E51", label="xbar n=5")
    ax.hist(large, bins=30, density=True, color="#1A2E51", alpha=0.55,
            edgecolor="#1A2E51", label="xbar n=200")
    ax.axvline(MU, color="#646464", ls="--", lw=1.3, label="mu verdadera = 100")
    ax.axvline(MU - TOLERANCE, color="#5B8DEF", ls=":", lw=1.2)
    ax.axvline(MU + TOLERANCE, color="#5B8DEF", ls=":", lw=1.2,
               label="|error| = 10")
    ax.set_xlabel("Estimador xbar")
    ax.set_ylabel("Densidad")
    ax.set_title("Insesgado en n = 5, pero demasiado ruidoso para una decisión de 10")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    tiny = small_sample_xbar()
    large = draw_means(N_LARGE)
    tiny_summary = decision_error_rate(tiny, N_TINY)
    large_summary = decision_error_rate(large, N_LARGE)
    figure_path = save_figure(tiny, large)

    print("================================================================")
    print("LECCIÓN 26 - PASO 3: VARIANZA DE MUESTRA PEQUEÑA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS:,}")
    print(f"n = 5 media de xbar             : {tiny_summary['mean']:.6f}")
    print(f"n = 5 sesgo                     : {tiny_summary['bias']:.6f}")
    print(f"n = 5 SD empírica               : {tiny_summary['sd']:.6f}")
    print(f"n = 5 EE de fórmula             : {tiny_summary['formula_se']:.6f}")
    print(f"n = 5 P(|xbar - mu| > 10)       : {tiny_summary['p_miss_10']:.6f}")
    print(f"n = 200 media de xbar           : {large_summary['mean']:.6f}")
    print(f"n = 200 sesgo                   : {large_summary['bias']:.6f}")
    print(f"n = 200 SD empírica             : {large_summary['sd']:.6f}")
    print(f"n = 200 P(|xbar - mu| > 10)     : {large_summary['p_miss_10']:.6f}")
    print("Límite: la insesgadez no implica varianza pequeña")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

