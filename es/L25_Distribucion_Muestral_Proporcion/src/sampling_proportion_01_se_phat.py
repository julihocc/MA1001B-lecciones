"""
Lección 25 - Paso 1: Error estándar de una proporción muestral
=============================================================
NUEVO EN ESTE PASO: proportion_se(), np_conditions() y save_figure().

La Receta
Un indicador sintético de entrega tardía tiene proporción poblacional
p = 0.18. Muestras de n = 120 tickets tienen
EE(phat) = sqrt(p(1-p)/n). Las verificaciones np y n(1-p) superan ambas 5.

Ejecútalo:
    uv run es/L25_Distribucion_Muestral_Proporcion/src/sampling_proportion_01_se_phat.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
P = 0.18
N = 120
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) proportion_se() -----------------------------------------------
def proportion_se(p: float = P, n: int = N) -> float:
    """Retorna EE(phat) = sqrt(p (1 - p) / n)."""
    return float(np.sqrt(p * (1.0 - p) / n))
# ------------------------------------------------------------------------------


# --- NUEVO (2) np_conditions() -----------------------------------------------
def np_conditions(p: float = P, n: int = N) -> dict[str, float]:
    """Verifica los conteos np y n(1-p) usados para una aproximación normal."""
    return {
        "p": p,
        "n": float(n),
        "np": n * p,
        "n_one_minus_p": n * (1.0 - p),
        "se": proportion_se(p, n),
        "mean": p,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(summary: dict[str, float]) -> Path:
    """Grafica la densidad normal aproximante de phat cuando n = 120."""
    output_path = DIR_FIGURES / "sampling_proportion_01_se_phat.png"
    se = summary["se"]
    x = np.linspace(P - 4 * se, P + 4 * se, 400)
    y = stats.norm(loc=P, scale=se).pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="N(p, EE)")
    ax.axvline(P, color="#EC2661", ls="--", lw=1.4, label="p = 0.18")
    ax.set_xlabel("Proporción muestral phat")
    ax.set_ylabel("Densidad")
    ax.set_title("n = 120, p = 0.18: EE = sqrt(p(1-p)/n)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    summary = np_conditions()
    figure_path = save_figure(summary)

    print("================================================================")
    print("LECCIÓN 25 - PASO 1: EE DE PHAT")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"p poblacional                   : {summary['p']:.6f}")
    print(f"Tamaño de muestra n             : {int(summary['n'])}")
    print(f"np                              : {summary['np']:.6f}")
    print(f"n(1 - p)                        : {summary['n_one_minus_p']:.6f}")
    print(f"EE(phat)                        : {summary['se']:.6f}")
    print("np y n(1-p) superan ambos 5")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

