"""
Lección 16 - Paso 1: Muestreo sin reemplazo
==========================================
NUEVO EN ESTE PASO: lot_parameters(), hypergeometric_p_zero() y save_figure().

La Receta
Un lote completamente sintético de N = 80 unidades contiene K = 6 defectuosos.
Un inspector extrae n = 10 unidades sin reemplazo. El conteo de defectos X
sigue una distribución hipergeométrica. La primera cantidad de interés es
P(X = 0).

Ejecútalo:
    uv run es/L16_Hipergeometrica_Sin_Reemplazo/src/hipergeometrica_01_sin_reemplazo.py
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


# --- NUEVO (1) lot_parameters() ----------------------------------------------
def lot_parameters() -> dict[str, int | float]:
    """Devuelve los ingredientes hipergeométricos N, K, n y n/N."""
    return {
        "N": N_POP,
        "K": K_DEFECTIVE,
        "n": N_DRAW,
        "sampling_fraction": N_DRAW / N_POP,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) hypergeometric_p_zero() ---------------------------------------
def hypergeometric_p_zero() -> float:
    """Devuelve P(X = 0) para X ~ Hipergeométrica(N=80, K=6, n=10)."""
    return float(stats.hypergeom.pmf(0, M=N_POP, n=K_DEFECTIVE, N=N_DRAW))
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(p_zero: float) -> Path:
    """Guarda la FMP hipergeométrica con P(X = 0) resaltada."""
    output_path = DIR_FIGURES / "hipergeometrica_01_sin_reemplazo.png"
    xs = np.arange(0, min(K_DEFECTIVE, N_DRAW) + 1)
    masses = stats.hypergeom.pmf(xs, M=N_POP, n=K_DEFECTIVE, N=N_DRAW)
    colors = ["#EC2661" if x == 0 else "#1A2E51" for x in xs]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(xs, masses, color=colors, width=0.62)
    ax.set_xlabel("Defectuosos en la muestra x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Hipergeométrica(N=80, K=6, n=10)")
    ax.set_xticks(xs)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.text(
        bars[0].get_x() + bars[0].get_width() / 2,
        p_zero + 0.02,
        f"{p_zero:.4f}",
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
    params = lot_parameters()
    p_zero = hypergeometric_p_zero()
    figure_path = save_figure(p_zero)

    print("================================================================")
    print("LECCIÓN 16 - PASO 1: SIN REEMPLAZO")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Tamaño del lote N                : {params['N']}")
    print(f"Defectuosos en el lote K         : {params['K']}")
    print(f"Tamaño de la extracción n        : {params['n']}")
    print(f"Fracción de muestreo n/N         : {params['sampling_fraction']:.6f}")
    print(f"P(X = 0) hipergeométrica         : {p_zero:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

