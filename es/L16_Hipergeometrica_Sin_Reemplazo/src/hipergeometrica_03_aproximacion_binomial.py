"""
Lección 16 - Paso 3: Aproximación binomial cuando n/N no es pequeña
===================================================================
NUEVO EN ESTE PASO: binomial_p_zero(), compare_models() y save_figure().

La Receta
CAMBIOS RESPECTO A hipergeometrica_02_esperanza.py
Introdúcelos en este orden:
    1. binomial_p_zero()    chance binomial(n=10, p=K/N) de una muestra limpia
    2. compare_models()     hipergeométrica frente a binomial P(X = 0)
    3. save_figure()        superpone las dos FMP

La fracción de muestreo n/N = 10/80 = 0.125 no es pequeña. Extraer sin
reemplazo agota defectuosos, de modo que la binomial sobreestima P(X = 0).

Ejecútalo:
    uv run es/L16_Hipergeometrica_Sin_Reemplazo/src/hipergeometrica_03_aproximacion_binomial.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_POP = 80
K_DEFECTIVE = 6
N_DRAW = 10
P_BINOM = K_DEFECTIVE / N_POP
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def hypergeometric_p_zero() -> float:
    """Devuelve P(X = 0) para X ~ Hipergeométrica(N=80, K=6, n=10)."""
    return float(stats.hypergeom.pmf(0, M=N_POP, n=K_DEFECTIVE, N=N_DRAW))


def hypergeometric_mean() -> float:
    """Devuelve E[X] = n K / N."""
    return N_DRAW * K_DEFECTIVE / N_POP


# --- NUEVO (1) binomial_p_zero() ---------------------------------------------
def binomial_p_zero() -> float:
    """Devuelve P(X = 0) para la aproximación binomial con p = K/N."""
    return float(stats.binom.pmf(0, n=N_DRAW, p=P_BINOM))
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_models() ----------------------------------------------
def compare_models() -> dict[str, float]:
    """Compara P(X = 0) y las medias hipergeométrica y binomial."""
    return {
        "hyper_p_zero": hypergeometric_p_zero(),
        "binom_p_zero": binomial_p_zero(),
        "hyper_mean": hypergeometric_mean(),
        "binom_mean": N_DRAW * P_BINOM,
        "sampling_fraction": N_DRAW / N_POP,
        "overstatement": binomial_p_zero() - hypergeometric_p_zero(),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """Superpone las FMP hipergeométrica y binomial."""
    output_path = DIR_FIGURES / "hipergeometrica_03_aproximacion_binomial.png"
    xs = np.arange(0, K_DEFECTIVE + 1)
    hyper = stats.hypergeom.pmf(xs, M=N_POP, n=K_DEFECTIVE, N=N_DRAW)
    binom = stats.binom.pmf(xs, n=N_DRAW, p=P_BINOM)
    width = 0.38

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs - width / 2, hyper, width=width, color="#1A2E51", label="Hipergeométrica")
    ax.bar(xs + width / 2, binom, width=width, color="#EC2661", label="Aprox. binomial")
    ax.set_xlabel("Defectuosos en la muestra x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("La binomial sobreestima P(X = 0) cuando n/N = 0.125")
    ax.set_xticks(xs)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    comparison = compare_models()
    figure_path = save_figure(comparison)

    print("================================================================")
    print("LECCIÓN 16 - PASO 3: APROXIMACIÓN BINOMIAL")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"p = K/N                          : {P_BINOM:.6f}")
    print(f"Fracción de muestreo n/N         : {comparison['sampling_fraction']:.6f}")
    print(f"Hipergeométrica P(X = 0)         : {comparison['hyper_p_zero']:.6f}")
    print(f"Binomial P(X = 0)                : {comparison['binom_p_zero']:.6f}")
    print(f"Sobreestimación binomial         : {comparison['overstatement']:.6f}")
    print(f"Media hipergeométrica            : {comparison['hyper_mean']:.6f}")
    print(f"Media binomial                   : {comparison['binom_mean']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

