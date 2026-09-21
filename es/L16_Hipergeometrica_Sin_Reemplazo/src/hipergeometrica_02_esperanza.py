"""
Lección 16 - Paso 2: Esperanza hipergeométrica
=============================================
NUEVO EN ESTE PASO: hypergeometric_mean(), hypergeometric_pmf() y save_figure().

La Receta
CAMBIOS RESPECTO A hipergeometrica_01_sin_reemplazo.py
Introdúcelos en este orden:
    1. hypergeometric_mean()    E[X] = n K / N
    2. hypergeometric_pmf()     FMP completa en 0, ..., min(K, n)
    3. save_figure()            FMP con la media marcada

El mismo lote N = 80, K = 6, n = 10 se reconstruye desde constantes. No se
importa ningún script anterior de la lección.

Ejecútalo:
    uv run es/L16_Hipergeometrica_Sin_Reemplazo/src/hipergeometrica_02_esperanza.py
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def lot_parameters() -> dict[str, int | float]:
    """Devuelve los ingredientes hipergeométricos N, K, n y n/N."""
    return {
        "N": N_POP,
        "K": K_DEFECTIVE,
        "n": N_DRAW,
        "sampling_fraction": N_DRAW / N_POP,
    }


def hypergeometric_p_zero() -> float:
    """Devuelve P(X = 0) para X ~ Hipergeométrica(N=80, K=6, n=10)."""
    return float(stats.hypergeom.pmf(0, M=N_POP, n=K_DEFECTIVE, N=N_DRAW))


# --- NUEVO (1) hypergeometric_mean() -----------------------------------------
def hypergeometric_mean() -> float:
    """Devuelve E[X] = n K / N."""
    return N_DRAW * K_DEFECTIVE / N_POP
# ------------------------------------------------------------------------------


# --- NUEVO (2) hypergeometric_pmf() ------------------------------------------
def hypergeometric_pmf() -> tuple[np.ndarray, np.ndarray]:
    """Devuelve el soporte y las masas hipergeométricas."""
    xs = np.arange(0, min(K_DEFECTIVE, N_DRAW) + 1)
    masses = stats.hypergeom.pmf(xs, M=N_POP, n=K_DEFECTIVE, N=N_DRAW)
    return xs, masses
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(xs: np.ndarray, masses: np.ndarray, mean: float) -> Path:
    """Guarda la FMP con una línea vertical en E[X] = nK/N."""
    output_path = DIR_FIGURES / "hipergeometrica_02_esperanza.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color="#1A2E51", width=0.62)
    ax.axvline(mean, color="#EC2661", linestyle="--", lw=2.0, label=f"E[X] = {mean:.2f}")
    ax.set_xlabel("Defectuosos en la muestra x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Media hipergeométrica E[X] = nK/N = 0.75")
    ax.set_xticks(xs)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    params = lot_parameters()
    mean = hypergeometric_mean()
    xs, masses = hypergeometric_pmf()
    scipy_mean = float(stats.hypergeom.mean(M=N_POP, n=K_DEFECTIVE, N=N_DRAW))
    figure_path = save_figure(xs, masses, mean)

    print("================================================================")
    print("LECCIÓN 16 - PASO 2: MEDIA HIPERGEOMÉTRICA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"n K / N                          : {mean:.6f}")
    print(f"Media hypergeom de scipy         : {scipy_mean:.6f}")
    print(f"P(X = 0)                         : {hypergeometric_p_zero():.6f}")
    print(f"Fracción de muestreo n/N         : {params['sampling_fraction']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

