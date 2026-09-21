"""
Lección 23 - Paso 1: Error estándar de la media muestral
========================================================
NUEVO EN ESTE PASO: population_model(), standard_error() y save_figure().

La Receta
Una población sintética de tiempos de ciclo es Normal(mu=80, sigma=12)
minutos. La distribución muestral de xbar tiene media mu y error
estándar sigma / sqrt(n). Se comparan los tamaños n = 9 y n = 36.

Ejecútalo:
    uv run es/L23_Distribucion_Muestral_Media/src/sampling_mean_01_standard_error.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 80.0
SIGMA = 12.0
N_SMALL = 9
N_LARGE = 36
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) population_model() --------------------------------------------
def population_model():
    """Retorna la población de tiempos de ciclo Normal(80, 12)."""
    return stats.norm(loc=MU, scale=SIGMA)
# ------------------------------------------------------------------------------


# --- NUEVO (2) standard_error() ----------------------------------------------
def standard_error(n: int, sigma: float = SIGMA) -> float:
    """Retorna EE = sigma / sqrt(n) para una media muestral iid."""
    return sigma / np.sqrt(n)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(se_small: float, se_large: float) -> Path:
    """Grafica densidades muestrales de xbar para n = 9 y n = 36."""
    output_path = DIR_FIGURES / "sampling_mean_01_standard_error.png"
    x = np.linspace(MU - 4 * SIGMA, MU + 4 * SIGMA, 400)
    pop = stats.norm(loc=MU, scale=SIGMA)
    small = stats.norm(loc=MU, scale=se_small)
    large = stats.norm(loc=MU, scale=se_large)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, pop.pdf(x), color="#646464", lw=1.6, ls=":",
            label="Población sigma = 12")
    ax.plot(x, small.pdf(x), color="#5B8DEF", lw=2.2,
            label=f"xbar n=9, EE={se_small:.2f}")
    ax.plot(x, large.pdf(x), color="#EC2661", lw=2.2,
            label=f"xbar n=36, EE={se_large:.2f}")
    ax.axvline(MU, color="#1A2E51", ls="--", lw=1.2)
    ax.set_xlabel("Tiempo de ciclo (minutos)")
    ax.set_ylabel("Densidad")
    ax.set_title("Un n mayor reduce EE = sigma / sqrt(n)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    se_small = standard_error(N_SMALL)
    se_large = standard_error(N_LARGE)
    figure_path = save_figure(se_small, se_large)

    print("================================================================")
    print("LECCIÓN 23 - PASO 1: ERROR ESTÁNDAR")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Media poblacional mu            : {MU:.6f}")
    print(f"Desv. estándar poblacional sigma: {SIGMA:.6f}")
    print(f"EE para n = 9                   : {se_small:.6f}")
    print(f"EE para n = 36                  : {se_large:.6f}")
    print(f"Razón EE(9) / EE(36)            : {se_small / se_large:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

