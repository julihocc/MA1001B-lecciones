"""
Lección 32 - Paso 3: La F de dos varianzas es sensible a la no normalidad
=========================================================================
NUEVO EN ESTE PASO: type_i_normal(), type_i_heavy_tails() y save_figure().

La Receta
Partir de f_dos_var_02_prueba_f.py e introducir:
    1. type_i_normal()          tasa de tipo I de la prueba F bajo varianzas normales iguales
    2. type_i_heavy_tails()     la misma H0 de varianzas iguales, pero muestras t(3)
    3. save_figure()            contrastar las dos tasas empíricas de tipo I

Límite: cuando ambas estaciones tienen la misma varianza pero colas pesadas,
la prueba F rechaza H0 mucho más a menudo que alfa = 0.05. El procedimiento
F de dos varianzas es sensible a la no normalidad.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N1 = 25
N2 = 25
N_REPS = 5000
ALPHA = 0.05
EQUAL_SIGMA = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def f_reject_rate(samples_a: np.ndarray, samples_b: np.ndarray) -> float:
    """Proporción de replicaciones con valor p de cola superior menor que alfa."""
    s1_sq = np.var(samples_a, axis=1, ddof=1)
    s2_sq = np.var(samples_b, axis=1, ddof=1)
    f_stats = s1_sq / s2_sq
    p_values = stats.f.sf(f_stats, N1 - 1, N2 - 1)
    return float(np.mean(p_values < ALPHA))


# --- NUEVO (1) type_i_normal() -----------------------------------------------
def type_i_normal(n_reps: int = N_REPS) -> dict[str, float]:
    """Tasa de tipo I cuando ambas estaciones son normales con sigma igual."""
    rng = np.random.default_rng(SEED)
    a = rng.normal(0.0, EQUAL_SIGMA, size=(n_reps, N1))
    b = rng.normal(0.0, EQUAL_SIGMA, size=(n_reps, N2))
    return {"n_reps": float(n_reps), "type_i": f_reject_rate(a, b)}
# ------------------------------------------------------------------------------


# --- NUEVO (2) type_i_heavy_tails() ------------------------------------------
def type_i_heavy_tails(n_reps: int = N_REPS) -> dict[str, float]:
    """Tasa de tipo I cuando ambas estaciones son t(3) con la misma escala."""
    rng = np.random.default_rng(SEED)
    a = rng.standard_t(3, size=(n_reps, N1))
    b = rng.standard_t(3, size=(n_reps, N2))
    return {"n_reps": float(n_reps), "type_i": f_reject_rate(a, b)}
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(normal_rate: float, heavy_rate: float) -> Path:
    """Contrasta el alfa nominal con las tasas de tipo I bajo dos poblaciones."""
    output_path = DIR_FIGURES / "f_dos_var_03_sensibilidad_no_normal.png"
    labels = ["Varianzas iguales\nnormales", "Varianzas iguales\ncolas t(3)"]
    values = [normal_rate, heavy_rate]
    colors = ["#1A2E51", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.axhline(ALPHA, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label=f"Alfa nominal = {ALPHA:.2f}")
    ax.set_ylabel("Tasa empírica de tipo I")
    ax.set_title("La F de dos varianzas es sensible a la no normalidad")
    ax.set_ylim(0, max(0.25, heavy_rate + 0.05))
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    normal = type_i_normal()
    heavy = type_i_heavy_tails()
    figure_path = save_figure(normal["type_i"], heavy["type_i"])

    print("================================================================")
    print("LECCIÓN 32 - PASO 3: SENSIBILIDAD A LA NO NORMALIDAD")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS}")
    print(f"n1, n2                          : {N1}, {N2}")
    print(f"Alfa nominal                    : {ALPHA:.6f}")
    print(f"Tasa tipo I (normal, var. igual): {normal['type_i']:.6f}")
    print(f"Tasa tipo I (t(3), var. igual)  : {heavy['type_i']:.6f}")
    print("Límite                         : la F de dos varianzas es sensible a la no normalidad")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

