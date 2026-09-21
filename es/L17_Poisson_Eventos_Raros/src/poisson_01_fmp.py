"""
Lección 17 - Paso 1: FMP de Poisson para eventos raros
======================================================
NUEVO EN ESTE PASO: poisson_rate(), poisson_probabilities() y save_figure().

La Receta
Un escritorio de operaciones completamente sintético registra el número de
eventos de parada X en un turno. La tasa media es lambda = 3.2 eventos por
turno. El modelo de Poisson da P(X = 0) y la cola superior P(X >= 6).

Ejecútalo:
    uv run es/L17_Poisson_Eventos_Raros/src/poisson_01_fmp.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
LAMBDA = 3.2
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) poisson_rate() ------------------------------------------------
def poisson_rate() -> dict[str, float]:
    """Devuelve la media de Poisson y la varianza igual a la media."""
    return {
        "lambda": LAMBDA,
        "mean": LAMBDA,
        "variance": LAMBDA,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) poisson_probabilities() ---------------------------------------
def poisson_probabilities() -> dict[str, float]:
    """Devuelve P(X = 0) y P(X >= 6) para X ~ Poisson(3.2)."""
    model = stats.poisson(mu=LAMBDA)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_least_six": float(model.sf(5)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure() -> Path:
    """Guarda la FMP de Poisson con x = 0 y x >= 6 resaltados."""
    output_path = DIR_FIGURES / "poisson_01_fmp.png"
    xs = np.arange(0, 13)
    masses = stats.poisson.pmf(xs, mu=LAMBDA)
    colors = ["#EC2661" if (x == 0 or x >= 6) else "#1A2E51" for x in xs]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color=colors, width=0.8)
    ax.set_xlabel("Eventos por turno x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Poisson(lambda = 3.2); x = 0 y x >= 6 en rojo")
    ax.set_xticks(xs)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    rate = poisson_rate()
    probs = poisson_probabilities()
    figure_path = save_figure()

    print("================================================================")
    print("LECCIÓN 17 - PASO 1: FMP DE POISSON")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"lambda                           : {rate['lambda']:.6f}")
    print(f"Media de Poisson                 : {rate['mean']:.6f}")
    print(f"Varianza de Poisson              : {rate['variance']:.6f}")
    print(f"P(X = 0)                         : {probs['p_zero']:.6f}")
    print(f"P(X >= 6)                        : {probs['p_at_least_six']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

