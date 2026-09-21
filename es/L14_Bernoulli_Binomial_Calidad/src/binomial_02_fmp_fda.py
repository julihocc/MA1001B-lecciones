"""
Lección 14 - Paso 2: FMP, FDA, media y varianza binomiales
==========================================================
NUEVO EN ESTE PASO: binomial_pmf_cdf(), binomial_moments() y save_figure().

CAMBIOS RESPECTO A binomial_01_ensayos_bernoulli.py
La Receta
---------
Introduce estos cambios en este orden:
    1. binomial_pmf_cdf()   P(X = 0) y P(X <= 2) desde scipy.stats.binom
    2. binomial_moments()   media np y varianza np(1-p)
    3. save_figure()        FMP binomial con la cola izquierda resaltada

Los mismos n = 20 y p = 0.08 se reconstruyen a partir de constantes. No se
importa ningún script anterior de la lección.

Ejecútalo:
    uv run es/L14_Bernoulli_Binomial_Calidad/src/binomial_02_fmp_fda.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_TRIALS = 20
P_DEFECT = 0.08
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def bernoulli_trial() -> dict[str, float]:
    """Devuelve la distribución de dos puntos de una inspección."""
    return {
        "p_defect": P_DEFECT,
        "p_clean": 1.0 - P_DEFECT,
    }


# --- NUEVO (1) binomial_pmf_cdf() --------------------------------------------
def binomial_pmf_cdf(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Devuelve P(X = 0) y P(X <= 2) para X ~ Binomial(n, p)."""
    model = stats.binom(n=n, p=p)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_most_two": float(model.cdf(2)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) binomial_moments() --------------------------------------------
def binomial_moments(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Devuelve la media binomial np y la varianza np(1-p)."""
    return {
        "mean": n * p,
        "variance": n * p * (1.0 - p),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(n: int = N_TRIALS, p: float = P_DEFECT) -> Path:
    """Guarda la FMP binomial y resalta x = 0, 1, 2."""
    output_path = DIR_FIGURES / "binomial_02_fmp_fda.png"
    xs = np.arange(0, n + 1)
    masses = stats.binom.pmf(xs, n=n, p=p)
    colors = ["#EC2661" if x <= 2 else "#1A2E51" for x in xs]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color=colors, width=0.8)
    ax.set_xlabel("Conteo de defectos x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Binomial(n=20, p=0.08); cola izquierda x <= 2 en rojo")
    ax.set_xticks(xs)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    trial = bernoulli_trial()
    probs = binomial_pmf_cdf()
    moments = binomial_moments()
    figure_path = save_figure()

    print("================================================================")
    print("LECCIÓN 14 - PASO 2: FMP Y FDA BINOMIALES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"n                               : {N_TRIALS}")
    print(f"p                               : {trial['p_defect']:.6f}")
    print(f"P(X = 0)                        : {probs['p_zero']:.6f}")
    print(f"P(X <= 2)                       : {probs['p_at_most_two']:.6f}")
    print(f"Media np                        : {moments['mean']:.6f}")
    print(f"Varianza np(1-p)                : {moments['variance']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

