"""
Lección 09 - Paso 1: Probabilidad condicional
=============================================
NUEVO EN ESTE PASO: synthetic_orders(), conditional_rates() y save_evidence().

La Receta
Construye el primer paso de la lección en este orden:
    1. synthetic_orders()       crea y mezcla la población de 400 pedidos
    2. conditional_rates()      restringe el denominador a una condición
    3. save_evidence()          compara visualmente las probabilidades condicionales

Ejecútalo:
    uv run es/L09_Probabilidad_Condicional_Independencia/src/condicional_01_espacio_muestral_reducido.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SEED = 42
FIGURE_PATH = (
    Path(__file__).resolve().parents[1] / "figuras" / "condicional_01_tasas.png"
)


# --- NUEVO (1) synthetic_orders() --------------------------------------------
def synthetic_orders() -> pd.DataFrame:
    """Devuelve una tabla sintética mezclada con conteos fijos de enrutamiento y resultado."""
    records = (
        [("Revisión manual", "Retrasado")] * 48
        + [("Revisión manual", "A tiempo")] * 72
        + [("Automatizado", "Retrasado")] * 32
        + [("Automatizado", "A tiempo")] * 248
    )
    frame = pd.DataFrame(records, columns=["routing", "delivery"])
    rng = np.random.default_rng(SEED)
    return frame.iloc[rng.permutation(len(frame))].reset_index(drop=True)
# -----------------------------------------------------------------------------


# --- NUEVO (2) conditional_rates() -------------------------------------------
def conditional_rates(orders: pd.DataFrame) -> dict[str, float]:
    """Calcula probabilidades tras restringir el denominador relevante."""
    manual = orders[orders["routing"] == "Revisión manual"]
    automated = orders[orders["routing"] == "Automatizado"]
    late = orders[orders["delivery"] == "Retrasado"]
    return {
        "P(Late | Manual)": (manual["delivery"] == "Retrasado").mean(),
        "P(Late | Automated)": (automated["delivery"] == "Retrasado").mean(),
        "P(Manual | Late)": (late["routing"] == "Revisión manual").mean(),
    }
# -----------------------------------------------------------------------------


# --- NUEVO (3) save_evidence() -----------------------------------------------
def save_evidence(rates: dict[str, float]) -> None:
    """Guarda una gráfica de barras de tres probabilidades que dependen de la condición."""
    labels = ["Retrasado |\nManual", "Retrasado |\nAutomatizado", "Manual |\nRetrasado"]
    values = list(rates.values())
    colors = ["#D81B60", "#1E88E5", "#FFC107"]

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.70)
    ax.set_ylabel("Probabilidad condicional")
    ax.set_title("Condicionar cambia el grupo de referencia")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)
# -----------------------------------------------------------------------------


def main() -> None:
    orders = synthetic_orders()
    rates = conditional_rates(orders)
    print("Registros sintéticos de pedidos:", len(orders))
    print(f"P(Retrasado | Revisión manual): {rates['P(Late | Manual)']:.6f}")
    print(f"P(Retrasado | Automatizado): {rates['P(Late | Automated)']:.6f}")
    print(f"P(Revisión manual | Retrasado): {rates['P(Manual | Late)']:.6f}")
    save_evidence(rates)
    print("Figura guardada:", FIGURE_PATH)


if __name__ == "__main__":
    main()

