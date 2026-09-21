"""
Lección 09 - Paso 2: Pruebas de independencia
=============================================
NUEVO EN ESTE PASO: independence_tests() y save_evidence().

CAMBIOS RESPECTO A condicional_01_espacio_muestral_reducido.py
La Receta
---------
Introduce estos cambios en este orden:
    1. independence_tests()     compara dos criterios equivalentes de independencia
    2. save_evidence()          muestra ambos fallos frente a sus referencias

Ejecútalo:
    uv run es/L09_Probabilidad_Condicional_Independencia/src/condicional_02_pruebas_independencia.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SEED = 42
FIGURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "figuras"
    / "condicional_02_independencia.png"
)


def synthetic_orders() -> pd.DataFrame:
    """Devuelve el mismo conjunto sintético mezclado de 400 pedidos del Paso 1."""
    records = (
        [("Revisión manual", "Retrasado")] * 48
        + [("Revisión manual", "A tiempo")] * 72
        + [("Automatizado", "Retrasado")] * 32
        + [("Automatizado", "A tiempo")] * 248
    )
    frame = pd.DataFrame(records, columns=["routing", "delivery"])
    rng = np.random.default_rng(SEED)
    return frame.iloc[rng.permutation(len(frame))].reset_index(drop=True)


# --- NUEVO (1) independence_tests() ------------------------------------------
def independence_tests(orders: pd.DataFrame) -> dict[str, float | bool]:
    """Evalúa las definiciones condicional y de producto de independencia."""
    manual = orders["routing"] == "Revisión manual"
    late = orders["delivery"] == "Retrasado"
    p_manual = manual.mean()
    p_late = late.mean()
    p_joint = (manual & late).mean()
    p_late_given_manual = (manual & late).sum() / manual.sum()
    return {
        "p_manual": p_manual,
        "p_late": p_late,
        "p_joint": p_joint,
        "p_late_given_manual": p_late_given_manual,
        "p_product": p_manual * p_late,
        "independent": bool(
            np.isclose(p_late_given_manual, p_late)
            and np.isclose(p_joint, p_manual * p_late)
        ),
    }
# -----------------------------------------------------------------------------


# --- NUEVO (2) save_evidence() -----------------------------------------------
def save_evidence(results: dict[str, float | bool]) -> None:
    """Guarda dos comparaciones emparejadas usadas para evaluar independencia."""
    pairs = [
        ("Prueba condicional", results["p_late_given_manual"], results["p_late"]),
        ("Prueba de producto", results["p_joint"], results["p_product"]),
    ]
    actual = [float(pair[1]) for pair in pairs]
    benchmark = [float(pair[2]) for pair in pairs]
    x = np.arange(len(pairs))
    width = 0.34

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    bars_a = ax.bar(x - width / 2, actual, width, label="Observado", color="#D81B60")
    bars_b = ax.bar(
        x + width / 2,
        benchmark,
        width,
        label="Referencia de independencia",
        color="#1E88E5",
    )
    ax.set_xticks(x, [pair[0] for pair in pairs])
    ax.set_ylabel("Probabilidad")
    ax.set_ylim(0, 0.48)
    ax.set_title("Ambas igualdades de independencia fallan")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    for bars in (bars_a, bars_b):
        for bar in bars:
            value = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.015,
                f"{value:.2f}",
                ha="center",
            )
    fig.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)
# -----------------------------------------------------------------------------


def main() -> None:
    orders = synthetic_orders()
    results = independence_tests(orders)
    print(f"P(Retrasado): {results['p_late']:.6f}")
    print(f"P(Retrasado | Revisión manual): {results['p_late_given_manual']:.6f}")
    print(f"P(Revisión manual Y Retrasado): {results['p_joint']:.6f}")
    print(f"P(Revisión manual) x P(Retrasado): {results['p_product']:.6f}")
    print("Eventos independientes:", results["independent"])
    save_evidence(results)
    print("Figura guardada:", FIGURE_PATH)


if __name__ == "__main__":
    main()

