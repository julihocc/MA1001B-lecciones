"""
Lección 31 - Paso 2: Intervalo de confianza chi-cuadrada para la varianza
=========================================================================
NUEVO EN ESTE PASO: chi_square_criticals(), variance_interval() y
save_figure().

La Receta
Partir de chi_cuadrada_01_varianza_muestral.py e introducir:
    1. chi_square_criticals()   chi2.ppf en 0.025 y 0.975 con gl = 19
    2. variance_interval()      ((n-1)s^2 / chi2_U, (n-1)s^2 / chi2_L)
    3. save_figure()            dibujar el intervalo para sigma^2

Los mismos n = 20 ciclos sintéticos se reconstruyen con SEED = 42. No se
importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 20
MU_TRUE = 12.0
SIGMA_TRUE = 3.0
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_cycle_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n tiempos de ciclo iid normales. El analista no conoce sigma^2."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)


# --- NUEVO (1) chi_square_criticals() ----------------------------------------
def chi_square_criticals(df: int, confidence: float = CONFIDENCE) -> dict[str, float]:
    """Devuelve los cuantiles chi-cuadrada inferior y superior de un intervalo bilateral."""
    alpha = 1.0 - confidence
    chi2_lower = float(stats.chi2.ppf(alpha / 2.0, df))
    chi2_upper = float(stats.chi2.ppf(1.0 - alpha / 2.0, df))
    return {
        "df": float(df),
        "alpha": alpha,
        "chi2_lower": chi2_lower,
        "chi2_upper": chi2_upper,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) variance_interval() -------------------------------------------
def variance_interval(
    s2: float,
    df: int,
    criticals: dict[str, float],
) -> dict[str, float]:
    """Construye el intervalo al 95% para sigma^2 con valores críticos chi-cuadrada."""
    lower = df * s2 / criticals["chi2_upper"]
    upper = df * s2 / criticals["chi2_lower"]
    hidden = SIGMA_TRUE ** 2
    return {
        "s2": s2,
        "lower": float(lower),
        "upper": float(upper),
        "width": float(upper - lower),
        "hidden_sigma2": hidden,
        "covers_true": float(lower <= hidden <= upper),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(interval: dict[str, float]) -> Path:
    """Guarda el intervalo chi-cuadrada para la varianza poblacional."""
    output_path = DIR_FIGURES / "chi_cuadrada_02_intervalo_varianza.png"
    midpoint = (interval["lower"] + interval["upper"]) / 2.0
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.errorbar(
        [midpoint],
        [1],
        xerr=[[midpoint - interval["lower"]],
              [interval["upper"] - midpoint]],
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=3.0,
        capsize=8,
        markersize=9,
    )
    ax.axvline(interval["hidden_sigma2"], color="#5B8DEF", linestyle="--",
               linewidth=1.6, label=f"Sigma^2 verdadera = {interval['hidden_sigma2']:.1f}")
    ax.set_yticks([1])
    ax.set_yticklabels(["Intervalo chi-cuadrada al 95%"])
    ax.set_xlabel("Varianza poblacional (min^2)")
    ax.set_title("Intervalo chi-cuadrada para sigma^2, gl = 19")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        midpoint,
        1.18,
        f"[{interval['lower']:.2f}, {interval['upper']:.2f}]",
        ha="center",
        fontsize=10,
        color="#1A2E51",
        fontweight="bold",
    )
    ax.set_ylim(0.4, 1.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_cycle_sample()
    s2 = float(np.var(sample, ddof=1))
    df = N - 1
    criticals = chi_square_criticals(df)
    interval = variance_interval(s2, df, criticals)
    figure_path = save_figure(interval)

    print("================================================================")
    print("LECCIÓN 31 - PASO 2: INTERVALO CHI-CUADRADA PARA LA VARIANZA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Grados de libertad              : {df}")
    print(f"Varianza muestral s^2           : {s2:.6f}")
    print(f"chi2 inferior (0.025)           : {criticals['chi2_lower']:.6f}")
    print(f"chi2 superior (0.975)           : {criticals['chi2_upper']:.6f}")
    print(f"Límite inferior para sigma^2    : {interval['lower']:.6f}")
    print(f"Límite superior para sigma^2    : {interval['upper']:.6f}")
    print(f"Ancho del intervalo             : {interval['width']:.6f}")
    print(f"Sigma^2 oculta                  : {interval['hidden_sigma2']:.6f}")
    print(f"Cubre la sigma^2 verdadera      : {'sí' if interval['covers_true'] else 'no'}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

