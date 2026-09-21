"""
Lección 14 - Paso 3: Un p no constante rompe el binomial
========================================================
NUEVO EN ESTE PASO: mixed_lot_pmf(), compare_zero_and_variance() y save_figure().

CAMBIOS RESPECTO A binomial_02_fmp_fda.py
La Receta
---------
Introduce estos cambios en este orden:
    1. mixed_lot_pmf()      la mitad de los lotes tiene p=0.02, la mitad p=0.14
    2. compare_zero_and_variance()  mezcla versus Binomial(20, 0.08)
    3. save_figure()        P(X = 0) y varianza bajo ambos modelos

La chance media de defecto sigue siendo 0.08, pero p no es constante entre
lotes. Esa mezcla es el límite del supuesto binomial.

Ejecútalo:
    uv run es/L14_Bernoulli_Binomial_Calidad/src/binomial_03_p_no_constante.py
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
P_LOW = 0.02
P_HIGH = 0.14
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def binomial_pmf_cdf(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Devuelve P(X = 0) y P(X <= 2) para X ~ Binomial(n, p)."""
    model = stats.binom(n=n, p=p)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_most_two": float(model.cdf(2)),
    }


def binomial_moments(n: int = N_TRIALS, p: float = P_DEFECT) -> dict[str, float]:
    """Devuelve la media binomial np y la varianza np(1-p)."""
    return {
        "mean": n * p,
        "variance": n * p * (1.0 - p),
    }


# --- NUEVO (1) mixed_lot_pmf() -----------------------------------------------
def mixed_lot_pmf(n: int = N_TRIALS) -> np.ndarray:
    """Promedia Binomial(n, 0.02) y Binomial(n, 0.14) con peso igual."""
    xs = np.arange(0, n + 1)
    return 0.5 * stats.binom.pmf(xs, n=n, p=P_LOW) + 0.5 * stats.binom.pmf(
        xs, n=n, p=P_HIGH
    )
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_zero_and_variance() -----------------------------------
def compare_zero_and_variance(n: int = N_TRIALS) -> dict[str, float]:
    """Compara P(X = 0) y Var(X) para el binomial y la mezcla."""
    xs = np.arange(0, n + 1)
    mix = mixed_lot_pmf(n)
    mix_mean = float(np.sum(xs * mix))
    mix_second = float(np.sum((xs ** 2) * mix))
    mix_var = mix_second - mix_mean ** 2
    binomial = binomial_moments(n, P_DEFECT)
    return {
        "binomial_p_zero": float(stats.binom.pmf(0, n=n, p=P_DEFECT)),
        "mixture_p_zero": float(mix[0]),
        "binomial_variance": binomial["variance"],
        "mixture_mean": mix_mean,
        "mixture_variance": mix_var,
        "average_p": 0.5 * P_LOW + 0.5 * P_HIGH,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """Contrasta P(X = 0) y la varianza cuando p no es constante."""
    output_path = DIR_FIGURES / "binomial_03_p_no_constante.png"
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))
    labels = ["Binomial\np=0.08", "Mezcla\n0.02 y 0.14"]
    colors = ["#1A2E51", "#EC2661"]

    zeros = [comparison["binomial_p_zero"], comparison["mixture_p_zero"]]
    axes[0].bar(labels, zeros, color=colors, width=0.55)
    axes[0].set_ylabel("P(X = 0)")
    axes[0].set_title("Chance de un lote limpio")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(zeros):
        axes[0].text(idx, value + 0.01, f"{value:.3f}", ha="center", fontsize=8)

    variances = [comparison["binomial_variance"], comparison["mixture_variance"]]
    axes[1].bar(labels, variances, color=colors, width=0.55)
    axes[1].set_ylabel("Var(X)")
    axes[1].set_title("Varianza del conteo de defectos")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(variances):
        axes[1].text(idx, value + 0.05, f"{value:.3f}", ha="center", fontsize=8)

    fig.suptitle("El p promedio = 0.08 no restaura el binomial")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    comparison = compare_zero_and_variance()
    figure_path = save_figure(comparison)

    print("================================================================")
    print("LECCIÓN 14 - PASO 3: p NO CONSTANTE")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Lotes de p bajo                 : {P_LOW:.6f}")
    print(f"Lotes de p alto                 : {P_HIGH:.6f}")
    print(f"p promedio                      : {comparison['average_p']:.6f}")
    print(f"P(X = 0) binomial               : {comparison['binomial_p_zero']:.6f}")
    print(f"P(X = 0) de la mezcla           : {comparison['mixture_p_zero']:.6f}")
    print(f"Varianza binomial               : {comparison['binomial_variance']:.6f}")
    print(f"Media de la mezcla              : {comparison['mixture_mean']:.6f}")
    print(f"Varianza de la mezcla           : {comparison['mixture_variance']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

