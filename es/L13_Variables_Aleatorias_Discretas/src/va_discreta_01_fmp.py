"""
Lección 13 - Paso 1: Función de masa de probabilidad
====================================================
NUEVO EN ESTE PASO: defect_support(), pmf_values() y save_figure().

Contexto:
Una inspección sintética de lotes entrantes registra el conteo de defectos X
en {0, 1, 2, 3} con probabilidades 0.50, 0.30, 0.15 y 0.05. Una variable
aleatoria discreta se especifica por su soporte y su función de masa de
probabilidad (FMP). Las masas deben ser no negativas y sumar 1.

Ejecútalo:
    uv run es/L13_Variables_Aleatorias_Discretas/src/va_discreta_01_fmp.py
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


# --- NUEVO (1) defect_support() ----------------------------------------------
def defect_support() -> np.ndarray:
    """Devuelve los conteos de defectos posibles del lote sintético."""
    return SUPPORT.copy()
# ------------------------------------------------------------------------------


# --- NUEVO (2) pmf_values() --------------------------------------------------
def pmf_values() -> np.ndarray:
    """Devuelve las masas de probabilidad P(X = x) en el soporte."""
    return PMF.copy()
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(support: np.ndarray, masses: np.ndarray) -> Path:
    """Guarda la función de masa de probabilidad como gráfica de tallos."""
    output_path = DIR_FIGURES / "va_discreta_01_fmp.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.vlines(support, 0, masses, colors="#1A2E51", lw=2.4)
    ax.plot(support, masses, "o", color="#EC2661", markersize=9)
    for x_value, mass in zip(support, masses):
        ax.text(
            x_value,
            mass + 0.025,
            f"{mass:.2f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    ax.set_xticks(support)
    ax.set_xlabel("Conteo de defectos x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("FMP del conteo sintético de defectos X")
    ax.set_ylim(0, 0.65)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    support = defect_support()
    masses = pmf_values()
    mass_sum = float(masses.sum())
    nonnegative = bool(np.all(masses >= 0))
    figure_path = save_figure(support, masses)

    print("================================================================")
    print("LECCIÓN 13 - PASO 1: FUNCIÓN DE MASA DE PROBABILIDAD")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Soporte                         : {support.tolist()}")
    print(f"P(X = 0)                        : {masses[0]:.6f}")
    print(f"P(X = 1)                        : {masses[1]:.6f}")
    print(f"P(X = 2)                        : {masses[2]:.6f}")
    print(f"P(X = 3)                        : {masses[3]:.6f}")
    print(f"Suma de las masas               : {mass_sum:.6f}")
    print(f"Todas las masas no negativas    : {nonnegative}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

