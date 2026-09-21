"""
Lección 13 - Paso 3: Esperanza y varianza
=========================================
NUEVO EN ESTE PASO: expected_value(), second_moment() y variance_from_moments().

CAMBIOS RESPECTO A va_discreta_02_fda.py
La Receta
---------
Introduce estos cambios en este orden:
    1. expected_value()     E[X] = suma x P(X = x)
    2. second_moment()      E[X^2] = suma x^2 P(X = x)
    3. variance_from_moments()  Var(X) = E[X^2] - (E[X])^2

El límite es la identidad E[X^2] != (E[X])^2. Elevar al cuadrado la media no
es el segundo momento, y la brecha entre ellos es la varianza.

Ejecútalo:
    uv run es/L13_Variables_Aleatorias_Discretas/src/va_discreta_03_esperanza_varianza.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SUPPORT = np.array([0, 1, 2, 3], dtype=int)
PMF = np.array([0.50, 0.30, 0.15, 0.05], dtype=float)
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def defect_support() -> np.ndarray:
    """Devuelve los conteos de defectos posibles del lote sintético."""
    return SUPPORT.copy()


def pmf_values() -> np.ndarray:
    """Devuelve las masas de probabilidad P(X = x) en el soporte."""
    return PMF.copy()


# --- NUEVO (1) expected_value() ----------------------------------------------
def expected_value(support: np.ndarray, masses: np.ndarray) -> float:
    """Devuelve E[X] como una suma de x P(X = x)."""
    return float(np.sum(support * masses))
# ------------------------------------------------------------------------------


# --- NUEVO (2) second_moment() -----------------------------------------------
def second_moment(support: np.ndarray, masses: np.ndarray) -> float:
    """Devuelve E[X^2] como una suma de x^2 P(X = x)."""
    return float(np.sum((support ** 2) * masses))
# ------------------------------------------------------------------------------


# --- NUEVO (3) variance_from_moments() ---------------------------------------
def variance_from_moments(mean: float, moment2: float) -> float:
    """Devuelve Var(X) = E[X^2] - (E[X])^2."""
    return moment2 - mean ** 2
# ------------------------------------------------------------------------------


def save_figure(mean: float, mean_squared: float, moment2: float, variance: float) -> Path:
    """Contrasta E[X]^2 con E[X^2] y muestra la varianza."""
    output_path = DIR_FIGURES / "va_discreta_03_esperanza_varianza.png"
    labels = ["E[X]", "(E[X])^2", "E[X^2]", "Var(X)"]
    values = [mean, mean_squared, moment2, variance]
    colors = ["#1A2E51", "#5B8DEF", "#EC2661", "#F4A6B8"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Valor")
    ax.set_title("E[X^2] no es (E[X])^2; la brecha es Var(X)")
    ax.set_ylim(0, 1.6)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.04,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path


def main() -> None:
    support = defect_support()
    masses = pmf_values()
    mean = expected_value(support, masses)
    moment2 = second_moment(support, masses)
    mean_squared = mean ** 2
    variance = variance_from_moments(mean, moment2)
    figure_path = save_figure(mean, mean_squared, moment2, variance)

    print("================================================================")
    print("LECCIÓN 13 - PASO 3: ESPERANZA Y VARIANZA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"E[X]                            : {mean:.6f}")
    print(f"(E[X])^2                        : {mean_squared:.6f}")
    print(f"E[X^2]                          : {moment2:.6f}")
    print(f"Var(X) = E[X^2] - (E[X])^2      : {variance:.6f}")
    print(f"E[X^2] igual a (E[X])^2         : {np.isclose(moment2, mean_squared)}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

