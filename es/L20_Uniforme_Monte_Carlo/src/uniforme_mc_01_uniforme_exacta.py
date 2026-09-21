"""
Lección 20 - Paso 1: Tiempo de procesamiento uniforme exacto
============================================================
NUEVO EN ESTE PASO: uniform_model(), exact_summaries() y save_figure().

La Receta
Un reloj de procesamiento de tickets completamente sintético se modela como
Uniforme(8, 20) minutos. La densidad es plana, de modo que la probabilidad es
longitud dividida entre 12. La cola exacta P(X > 16) y la media (a + b) / 2
son los valores de referencia para la comprobación Monte Carlo del Paso 2.

Ejecútalo:
    uv run es/L20_Uniforme_Monte_Carlo/src/uniforme_mc_01_uniforme_exacta.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
A = 8.0
B = 20.0
CUT = 16.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) uniform_model() -----------------------------------------------
def uniform_model():
    """Devuelve el modelo uniforme continuo en [8, 20] minutos."""
    return stats.uniform(loc=A, scale=B - A)
# ------------------------------------------------------------------------------


# --- NUEVO (2) exact_summaries() ---------------------------------------------
def exact_summaries(model) -> dict[str, float]:
    """Calcula la altura plana, la media y la cola exacta P(X > 16)."""
    return {
        "height": float(model.pdf((A + B) / 2)),
        "mean": float(model.mean()),
        "p_gt_cut": float(1.0 - model.cdf(CUT)),
        "length_ratio": (B - CUT) / (B - A),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(model, height: float, tail: float) -> Path:
    """Guarda la densidad uniforme plana con la cola X > 16 sombreada."""
    output_path = DIR_FIGURES / "uniforme_mc_01_uniforme_exacta.png"
    x = np.linspace(A - 1, B + 1, 500)
    y = model.pdf(x)
    shade_x = np.linspace(CUT, B, 200)
    shade_y = model.pdf(shade_x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2)
    ax.fill_between(shade_x, shade_y, color="#EC2661", alpha=0.35,
                    label=f"P(X > 16) = {tail:.4f}")
    ax.axhline(height, color="#5B8DEF", ls=":", lw=1.2)
    ax.set_xlabel("Tiempo de procesamiento (minutos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("Uniforme(8, 20): la probabilidad iguala longitud sobre 12")
    ax.set_xlim(A - 1, B + 1)
    ax.set_ylim(0, 0.14)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    model = uniform_model()
    values = exact_summaries(model)
    figure_path = save_figure(model, values["height"], values["p_gt_cut"])

    print("================================================================")
    print("LECCIÓN 20 - PASO 1: UNIFORME EXACTA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Soporte [a, b]                   : [{A:.1f}, {B:.1f}]")
    print(f"Altura de densidad 1/(b - a)     : {values['height']:.6f}")
    print(f"Media (a + b) / 2                : {values['mean']:.6f}")
    print(f"Razón de longitudes (20 - 16)/12 : {values['length_ratio']:.6f}")
    print(f"P(X > 16) exacta                 : {values['p_gt_cut']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

