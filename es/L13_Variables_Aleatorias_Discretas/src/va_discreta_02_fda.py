"""
Lección 13 - Paso 2: Función de distribución acumulada
======================================================
NUEVO EN ESTE PASO: cdf_values(), interval_from_cdf() y save_figure().

CAMBIOS RESPECTO A va_discreta_01_fmp.py
La Receta
---------
Introduce estos cambios en este orden:
    1. cdf_values()     F(x) = P(X <= x) al acumular la FMP
    2. interval_from_cdf()  P(a < X <= b) = F(b) - F(a)
    3. save_figure()    FDA de función escalón en el soporte de defectos

La misma distribución sintética de conteo de defectos se reconstruye a partir
de las mismas constantes. No se importa ningún script anterior de la lección.

Ejecútalo:
    uv run es/L13_Variables_Aleatorias_Discretas/src/va_discreta_02_fda.py
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


# --- NUEVO (1) cdf_values() --------------------------------------------------
def cdf_values(masses: np.ndarray) -> np.ndarray:
    """Devuelve F(x) = P(X <= x) en el soporte ordenado."""
    return np.cumsum(masses)
# ------------------------------------------------------------------------------


# --- NUEVO (2) interval_from_cdf() -------------------------------------------
def interval_from_cdf(cdf: np.ndarray, left: int, right: int) -> float:
    """Devuelve P(left < X <= right) a partir de valores de FDA en {0, 1, 2, 3}."""
    f_right = float(cdf[right])
    f_left = 0.0 if left < 0 else float(cdf[left])
    return f_right - f_left
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(support: np.ndarray, cdf: np.ndarray) -> Path:
    """Guarda la FDA como una función escalón continua por la derecha."""
    output_path = DIR_FIGURES / "va_discreta_02_fda.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    x_plot = np.array([-0.6, 0, 1, 2, 3, 3.6])
    y_plot = np.array([0.0, cdf[0], cdf[1], cdf[2], cdf[3], 1.0])
    ax.step(x_plot, y_plot, where="post", color="#1A2E51", lw=2.2)
    ax.plot(support, cdf, "o", color="#EC2661", markersize=9)
    for x_value, value in zip(support, cdf):
        ax.text(
            x_value,
            value + 0.04,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    ax.set_xticks(support)
    ax.set_xlabel("Conteo de defectos x")
    ax.set_ylabel("F(x) = P(X <= x)")
    ax.set_title("La FDA acumula la FMP")
    ax.set_ylim(-0.05, 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    support = defect_support()
    masses = pmf_values()
    cdf = cdf_values(masses)
    p_at_most_1 = interval_from_cdf(cdf, -1, 1)
    p_between_1_and_3 = interval_from_cdf(cdf, 1, 3)
    figure_path = save_figure(support, cdf)

    print("================================================================")
    print("LECCIÓN 13 - PASO 2: FUNCIÓN DE DISTRIBUCIÓN ACUMULADA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"F(0) = P(X <= 0)                : {cdf[0]:.6f}")
    print(f"F(1) = P(X <= 1)                : {cdf[1]:.6f}")
    print(f"F(2) = P(X <= 2)                : {cdf[2]:.6f}")
    print(f"F(3) = P(X <= 3)                : {cdf[3]:.6f}")
    print(f"P(X <= 1) desde la FDA          : {p_at_most_1:.6f}")
    print(f"P(1 < X <= 3) = F(3)-F(1)       : {p_between_1_and_3:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

