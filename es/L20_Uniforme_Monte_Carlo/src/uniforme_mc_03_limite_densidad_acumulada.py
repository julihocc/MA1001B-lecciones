"""
Lección 20 - Paso 3: La uniforme falla cuando la densidad se acumula en un extremo
=================================================================================
NUEVO EN ESTE PASO: piled_model(), compare_tails() y save_figure().

La Receta
CAMBIOS RESPECTO A uniforme_mc_02_monte_carlo.py
Introdúcelos en este orden:
    1. piled_model()            densidad triangular derecha en el mismo [8, 20]
    2. compare_tails()          Uniforme P(X > 16) frente a la cola acumulada
    3. save_figure()            superpone la densidad plana y la densidad acumulada

Si los tickets se agrupan cerca de 20 minutos, la cola Uniforme(8, 20) de 1/3
es el número equivocado. El límite es que un modelo plano falla cuando la
densidad se acumula en un extremo.

Ejecútalo:
    uv run es/L20_Uniforme_Monte_Carlo/src/uniforme_mc_03_limite_densidad_acumulada.py
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


def uniform_model():
    """Devuelve el modelo uniforme continuo en [8, 20] minutos."""
    return stats.uniform(loc=A, scale=B - A)


# --- NUEVO (1) piled_model() -------------------------------------------------
def piled_model():
    """Devuelve una densidad triangular derecha en [8, 20] que se acumula en 20."""
    return stats.triang(c=1.0, loc=A, scale=B - A)
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_tails() -----------------------------------------------
def compare_tails(flat, piled) -> dict[str, float]:
    """Contrasta colas y medias uniforme y de densidad acumulada."""
    return {
        "uniform_tail": float(1.0 - flat.cdf(CUT)),
        "piled_tail": float(1.0 - piled.cdf(CUT)),
        "uniform_mean": float(flat.mean()),
        "piled_mean": float(piled.mean()),
        "uniform_height": float(flat.pdf(14.0)),
        "piled_at_cut": float(piled.pdf(CUT)),
        "piled_at_b": float(piled.pdf(B)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(flat, piled, comparison: dict[str, float]) -> Path:
    """Superpone la densidad uniforme plana y la alternativa acumulada a la derecha."""
    output_path = DIR_FIGURES / "uniforme_mc_03_limite_densidad_acumulada.png"
    x = np.linspace(A, B, 400)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, flat.pdf(x), color="#1A2E51", lw=2.2, label="Uniforme(8, 20)")
    ax.plot(x, piled.pdf(x), color="#EC2661", lw=2.2,
            label="Acumulación triangular derecha")
    ax.fill_between(
        x[x >= CUT],
        piled.pdf(x[x >= CUT]),
        color="#EC2661",
        alpha=0.25,
        label=f"P(X > 16) acumulada = {comparison['piled_tail']:.4f}",
    )
    ax.axvline(CUT, color="#646464", ls="--", lw=1.2)
    ax.set_xlabel("Tiempo de procesamiento (minutos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("Un modelo uniforme plano no captura una acumulación en 20")
    ax.set_xlim(A, B)
    ax.set_ylim(0, 0.20)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    flat = uniform_model()
    piled = piled_model()
    comparison = compare_tails(flat, piled)
    figure_path = save_figure(flat, piled, comparison)

    print("================================================================")
    print("LECCIÓN 20 - PASO 3: LÍMITE DE DENSIDAD ACUMULADA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Uniforme P(X > 16)               : {comparison['uniform_tail']:.6f}")
    print(f"Acumulada P(X > 16)              : {comparison['piled_tail']:.6f}")
    print(f"Media uniforme                   : {comparison['uniform_mean']:.6f}")
    print(f"Media acumulada                  : {comparison['piled_mean']:.6f}")
    print(f"Altura uniforme                  : {comparison['uniform_height']:.6f}")
    print(f"Densidad acumulada en 16         : {comparison['piled_at_cut']:.6f}")
    print(f"Densidad acumulada en 20         : {comparison['piled_at_b']:.6f}")
    print("Límite: la uniforme falla si la densidad se acumula en un extremo")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

