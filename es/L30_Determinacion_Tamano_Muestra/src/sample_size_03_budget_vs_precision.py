"""
Lección 30 - Paso 3: El E = 0.01 deseado puede exceder el presupuesto
====================================================================
La Receta
Partir de sample_size_02_proportion_conservative.py e introducir:
    1. tight_margin_n()        n conservador para E = 0.01
    2. budget_capacity()       observaciones que el presupuesto puede financiar
    3. save_figure()           n requerido versus n asequible

Límite: reducir el margen de error a 0.01 infla n con el cuadrado de 1/E.
Un estudio de $20,000 a $12 por observación no puede financiar esa muestra.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
Z_STAR = 1.96
P_CONSERVATIVE = 0.5
E_TIGHT = 0.01
COST_PER_OBS = 12.0
BUDGET = 20_000.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) tight_margin_n() ----------------------------------------------
def tight_margin_n(margin: float = E_TIGHT) -> dict[str, float]:
    """Calcula n conservador para un margen de error muy pequeño."""
    raw = (Z_STAR ** 2) * P_CONSERVATIVE * (1.0 - P_CONSERVATIVE) / (margin ** 2)
    return {
        "margin": margin,
        "raw_n": float(raw),
        "n_required": int(np.ceil(raw)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) budget_capacity() ---------------------------------------------
def budget_capacity(
    n_required: int,
    cost: float = COST_PER_OBS,
    budget: float = BUDGET,
) -> dict[str, float]:
    """Compara el n requerido con el número de observaciones que el presupuesto puede comprar."""
    affordable = int(np.floor(budget / cost))
    shortfall = n_required - affordable
    cost_required = n_required * cost
    return {
        "cost_per_obs": cost,
        "budget": budget,
        "affordable_n": float(affordable),
        "shortfall": float(shortfall),
        "cost_required": float(cost_required),
        "can_fund": float(affordable >= n_required),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(n_required: int, affordable_n: int) -> Path:
    """Contrasta el n estadísticamente requerido con el n asequible del presupuesto."""
    output_path = DIR_FIGURES / "sample_size_03_budget_vs_precision.png"
    labels = ["n requerido\npara E = 0.01", "n asequible\na $12 / obs"]
    values = [n_required, affordable_n]
    colors = ["#EC2661", "#1A2E51"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Número de observaciones")
    ax.set_title("El E = 0.01 deseado excede el presupuesto del estudio")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 120,
            f"{value:,}",
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
    plan = tight_margin_n()
    money = budget_capacity(plan["n_required"])
    figure_path = save_figure(plan["n_required"], int(money["affordable_n"]))

    print("================================================================")
    print("LECCIÓN 30 - PASO 3: PRESUPUESTO VERSUS PRECISIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"z-estrella de libro             : {Z_STAR:.6f}")
    print(f"p conservadora                  : {P_CONSERVATIVE:.6f}")
    print(f"Margen estrecho E               : {plan['margin']:.6f}")
    print(f"n crudo para E=0.01             : {plan['raw_n']:.6f}")
    print(f"n redondeado hacia arriba       : {plan['n_required']}")
    print(f"Costo por observación           : {money['cost_per_obs']:.2f}")
    print(f"Presupuesto del estudio         : {money['budget']:.2f}")
    print(f"n asequible                     : {int(money['affordable_n'])}")
    print(f"Costo del n requerido           : {money['cost_required']:.2f}")
    print(f"Déficit de observaciones        : {int(money['shortfall'])}")
    print(f"El presupuesto puede financiar el n requerido: {'Sí' if money['can_fund'] else 'No'}")
    print("Límite                          : E=0.01 puede exceder el presupuesto")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

