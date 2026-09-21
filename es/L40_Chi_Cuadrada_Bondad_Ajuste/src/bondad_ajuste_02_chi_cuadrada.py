"""
Lección 40 - Paso 2: Estadístico ji-cuadrada de bondad de ajuste
================================================================
LA RECETA
Parte de bondad_ajuste_01_observados_esperados.py e introduce:
    1. chi_square_contributions()  (O - E)^2 / E en cada categoría
    2. goodness_of_fit_test()      chi2, df = k - 1, p-valor de cola derecha
    3. save_figure()               contribuciones celulares a chi2

Los mismos n = 200 conteos sintéticos de tickets se reconstruyen desde
constantes. No se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 200
CATEGORIES = ("Teléfono", "Chat", "Correo", "App")
HYPOTHESIZED = np.array([0.40, 0.30, 0.20, 0.10])
OBSERVED = np.array([100, 50, 30, 20], dtype=float)
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) chi_square_contributions() ------------------------------------
def chi_square_contributions(observed: np.ndarray, expected: np.ndarray) -> np.ndarray:
    """Devuelve los cuatro términos (O - E)^2 / E."""
    return (observed - expected) ** 2 / expected
# ------------------------------------------------------------------------------


# --- NUEVO (2) goodness_of_fit_test() ----------------------------------------
def goodness_of_fit_test(observed: np.ndarray, expected: np.ndarray) -> dict[str, float]:
    """Prueba GOF ji-cuadrada con df = número de categorías menos 1."""
    contributions = chi_square_contributions(observed, expected)
    chi2 = float(np.sum(contributions))
    df = observed.size - 1
    p_value = float(stats.chi2.sf(chi2, df))
    scipy_test = stats.chisquare(observed, expected)
    return {
        "chi2": chi2,
        "df": float(df),
        "p_value": p_value,
        "scipy_chi2": float(scipy_test.statistic),
        "scipy_p": float(scipy_test.pvalue),
        "critical": float(stats.chi2.ppf(1.0 - ALPHA, df)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(contributions: np.ndarray) -> Path:
    """Barras de la contribución de cada categoría a ji-cuadrada."""
    output_path = DIR_FIGURES / "bondad_ajuste_02_chi_cuadrada.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(CATEGORIES, contributions, color=["#EC2661", "#5B8DEF", "#1A2E51", "#F4A6B8"])
    ax.set_ylabel("(O - E)^2 / E")
    ax.set_title("Contribuciones ji-cuadrada, df = 3")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, contributions):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.08,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    expected = N * HYPOTHESIZED
    contributions = chi_square_contributions(OBSERVED, expected)
    test = goodness_of_fit_test(OBSERVED, expected)
    decision = "rechazar H0" if test["p_value"] < ALPHA else "no rechazar H0"
    figure_path = save_figure(contributions)

    print("================================================================")
    print("LECCIÓN 40 - PASO 2: BONDAD DE AJUSTE JI-CUADRADA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print("Hipótesis                       : H0: mezcla = (0.40, 0.30, 0.20, 0.10)")
    print(
        "Contribuciones celulares        : "
        + ", ".join(f"{value:.6f}" for value in contributions)
    )
    print(f"Estadístico ji-cuadrada         : {test['chi2']:.6f}")
    print(f"Grados de libertad k-1          : {int(test['df'])}")
    print(f"p-valor de cola derecha (manual): {test['p_value']:.6f}")
    print(f"p-valor de cola derecha (scipy) : {test['scipy_p']:.6f}")
    print(f"chi2* crítica (alpha = 0.05)    : {test['critical']:.6f}")
    print(f"Decisión a alpha = 0.05         : {decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

