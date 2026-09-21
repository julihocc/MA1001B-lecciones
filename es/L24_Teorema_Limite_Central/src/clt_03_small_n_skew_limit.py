"""
Lección 24 - Paso 3: n pequeño más asimetría es una mala aproximación TLC
========================================================================
La Receta
Partir de clt_02_means_n4_n40.py e introducir:
    1. tail_comparison()        P(xbar > mu + 2 EE) exacta versus normal
    2. normal_error()           error de cola TLC en n = 4 versus n = 40
    3. save_figure()            barras de la cola verdadera contra la normal

Para retrasos exponenciales, xbar tiene una ley Gamma exacta. En n = 4 la
cola normal a dos EE es aproximadamente la mitad de la cola verdadera. En
n = 40 el mismo corte z = 2 está más cerca, pero la asimetría no ha
desaparecido.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MEAN = 10.0
N_SMALL = 4
N_LARGE = 40
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) tail_comparison() ---------------------------------------------
def tail_comparison(n: int) -> dict[str, float]:
    """Compara la cola Gamma exacta de xbar con la cola normal TLC en z=2."""
    se = MEAN / np.sqrt(n)
    cut = MEAN + 2.0 * se
    exact = stats.gamma(a=n, scale=MEAN / n)
    normal = stats.norm(loc=MEAN, scale=se)
    exact_tail = float(1.0 - exact.cdf(cut))
    normal_tail = float(1.0 - normal.cdf(cut))
    return {
        "n": float(n),
        "cut": cut,
        "se": se,
        "exact_tail": exact_tail,
        "normal_tail": normal_tail,
        "abs_error": abs(normal_tail - exact_tail),
        "exact_skew": 2.0 / np.sqrt(n),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) normal_error() ------------------------------------------------
def normal_error() -> dict[str, dict[str, float]]:
    """Retorna comparaciones de cola z = 2 para n = 4 y n = 40."""
    return {
        "n4": tail_comparison(N_SMALL),
        "n40": tail_comparison(N_LARGE),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(table: dict[str, dict[str, float]]) -> Path:
    """Barras de colas exactas versus normales en z = 2."""
    output_path = DIR_FIGURES / "clt_03_small_n_skew_limit.png"
    labels = ["n = 4\nexacta", "n = 4\nnormal", "n = 40\nexacta", "n = 40\nnormal"]
    values = [
        table["n4"]["exact_tail"],
        table["n4"]["normal_tail"],
        table["n40"]["exact_tail"],
        table["n40"]["normal_tail"],
    ]
    colors = ["#1A2E51", "#5B8DEF", "#EC2661", "#F4A6B8"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("P(xbar > mu + 2 EE)")
    ax.set_title("n pequeño + asimetría: la cola normal es una mala aproximación")
    ax.set_ylim(0, 0.07)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.002,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    table = normal_error()
    figure_path = save_figure(table)

    print("================================================================")
    print("LECCIÓN 24 - PASO 3: LÍMITE N PEQUEÑO Y ASIMETRÍA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print("Evento de cola                  : xbar > mu + 2 EE")
    print(f"n = 4 corte                     : {table['n4']['cut']:.6f}")
    print(f"n = 4 cola exacta               : {table['n4']['exact_tail']:.6f}")
    print(f"n = 4 cola normal               : {table['n4']['normal_tail']:.6f}")
    print(f"n = 4 error absoluto            : {table['n4']['abs_error']:.6f}")
    print(f"n = 4 asimetría de xbar         : {table['n4']['exact_skew']:.6f}")
    print(f"n = 40 corte                    : {table['n40']['cut']:.6f}")
    print(f"n = 40 cola exacta              : {table['n40']['exact_tail']:.6f}")
    print(f"n = 40 cola normal              : {table['n40']['normal_tail']:.6f}")
    print(f"n = 40 error absoluto           : {table['n40']['abs_error']:.6f}")
    print(f"n = 40 asimetría de xbar        : {table['n40']['exact_skew']:.6f}")
    print("Límite: n pequeño + asimetría hace que el TLC sea una mala aproximación")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

