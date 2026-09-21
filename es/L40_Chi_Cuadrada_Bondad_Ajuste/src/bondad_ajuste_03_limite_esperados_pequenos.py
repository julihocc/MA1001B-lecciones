"""
Lección 40 - Paso 3: Un conteo esperado menor que 5 debilita la aproximación
===========================================================================
LA RECETA
Parte de bondad_ajuste_02_chi_cuadrada.py e introduce:
    1. small_sample_counts()    n = 20 con dos celdas esperadas menores que 5
    2. monte_carlo_pvalue()     p-valor multinomial como chequeo de chi2
    3. save_figure()            conteos esperados con la regla E < 5 marcada

La curva ji-cuadrada es una aproximación de muestra grande. Con n = 20 el
conteo esperado de App es 2 y una celda observada es 0, de modo que
(O - E)^2 / E ya no es un resumen estable.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_SMALL = 20
N_SIM = 20_000
CATEGORIES = ("Teléfono", "Chat", "Correo", "App")
HYPOTHESIZED = np.array([0.40, 0.30, 0.20, 0.10])
OBSERVED_SMALL = np.array([14, 4, 2, 0], dtype=float)
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) small_sample_counts() -----------------------------------------
def small_sample_counts() -> dict[str, np.ndarray | float]:
    """Mezcla n = 20 con dos conteos esperados menores que 5."""
    expected = N_SMALL * HYPOTHESIZED
    contributions = (OBSERVED_SMALL - expected) ** 2 / expected
    return {
        "observed": OBSERVED_SMALL.copy(),
        "expected": expected,
        "contributions": contributions,
        "min_expected": float(np.min(expected)),
        "n_cells_below_5": float(np.sum(expected < 5.0)),
        "chi2": float(np.sum(contributions)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) monte_carlo_pvalue() ------------------------------------------
def monte_carlo_pvalue(observed: np.ndarray, expected: np.ndarray, chi2: float) -> dict[str, float]:
    """Simula muestras multinomiales bajo H0 y compara valores ji-cuadrada."""
    rng = np.random.default_rng(SEED)
    draws = rng.multinomial(N_SMALL, HYPOTHESIZED, size=N_SIM)
    simulated_chi2 = np.sum((draws - expected) ** 2 / expected, axis=1)
    p_mc = float(np.mean(simulated_chi2 >= chi2))
    p_chi2 = float(stats.chi2.sf(chi2, observed.size - 1))
    return {
        "p_chi2": p_chi2,
        "p_monte_carlo": p_mc,
        "n_sim": float(N_SIM),
        "chi2_app_zero": float((0.0 - expected[-1]) ** 2 / expected[-1]),
        "chi2_app_one": float((1.0 - expected[-1]) ** 2 / expected[-1]),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(expected: np.ndarray) -> Path:
    """Resalta conteos esperados que caen por debajo de la guía E = 5."""
    output_path = DIR_FIGURES / "bondad_ajuste_03_limite_esperados_pequenos.png"
    colors = ["#EC2661" if value < 5 else "#1A2E51" for value in expected]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(CATEGORIES, expected, color=colors, width=0.62)
    ax.axhline(5.0, color="#646464", linestyle="--", linewidth=1.4,
               label="guía E = 5")
    ax.set_ylabel("Conteo esperado")
    ax.set_title("n = 20: dos conteos esperados caen por debajo de 5")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, expected):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.15,
            f"{value:.1f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    small = small_sample_counts()
    mc = monte_carlo_pvalue(small["observed"], small["expected"], small["chi2"])
    figure_path = save_figure(small["expected"])

    print("================================================================")
    print("LECCIÓN 40 - PASO 3: LÍMITE DE CONTEO ESPERADO PEQUEÑO")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"n de muestra pequeña            : {N_SMALL}")
    print("Conteos observados              : 14, 4, 2, 0")
    print(
        "Conteos esperados               : "
        + ", ".join(f"{value:.1f}" for value in small["expected"])
    )
    print(f"Celdas con E < 5                : {int(small['n_cells_below_5'])}")
    print(f"Conteo esperado mínimo          : {small['min_expected']:.6f}")
    print(f"Estadístico ji-cuadrada         : {small['chi2']:.6f}")
    print(f"p-valor ji-cuadrada             : {mc['p_chi2']:.6f}")
    print(f"p-valor Monte Carlo             : {mc['p_monte_carlo']:.6f}")
    print(f"Contribución App si O = 0       : {mc['chi2_app_zero']:.6f}")
    print(f"Contribución App si O = 1       : {mc['chi2_app_one']:.6f}")
    print(f"Muestras simuladas              : {int(mc['n_sim'])}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

