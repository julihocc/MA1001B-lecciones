"""
Lección 08 - Paso 2: Reglas de complemento y adición
====================================================
NUEVO EN ESTE PASO: complement_and_union() y save_addition_figure().

CAMBIOS RESPECTO A reglas_probabilidad_01_tabla_contingencia.py
La Receta
---------
Introduce estos cambios en este orden:
    1. complement_and_union() calcula complementos y el O corregido por traslape
    2. save_addition_figure() compara la adición ingenua con la unión correcta

Ejecútalo:
    uv run es/L08_Reglas_Probabilidad_Tablas_Contingencia/src/reglas_probabilidad_02_complemento_adicion.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figuras"
SEED = 42
TABLE_COUNTS = {
    ("Revisión manual", "Retrasado"): 48,
    ("Revisión manual", "A tiempo"): 72,
    ("Automatizado", "Retrasado"): 32,
    ("Automatizado", "A tiempo"): 248,
}
ROUTING_ORDER = ["Revisión manual", "Automatizado"]
DELIVERY_ORDER = ["Retrasado", "A tiempo"]
TEC_BLUE = "#0039A6"
TEC_NAVY = "#1A2E51"
TEC_PINK = "#EC2661"


def build_operations_data() -> pd.DataFrame:
    """Crea y mezcla de forma determinista 400 registros sintéticos de pedidos."""
    records: list[dict[str, str]] = []
    for (routing, delivery), count in TABLE_COUNTS.items():
        records.extend(
            {"routing": routing, "delivery": delivery}
            for _ in range(count)
        )

    rng = np.random.default_rng(SEED)
    shuffled = rng.permutation(len(records))
    data = pd.DataFrame(records).iloc[shuffled].reset_index(drop=True)
    data.insert(0, "order_id", [f"SO-{i:03d}" for i in range(1, len(data) + 1)])
    return data


def contingency_table(data: pd.DataFrame) -> pd.DataFrame:
    """Devuelve la tabla de conteos enrutamiento por entrega en orden fijo."""
    return pd.crosstab(data["routing"], data["delivery"]).reindex(
        index=ROUTING_ORDER,
        columns=DELIVERY_ORDER,
        fill_value=0,
    )


def table_probabilities(table: pd.DataFrame) -> dict[str, float]:
    """Calcula probabilidades marginales y conjuntas seleccionadas."""
    total = int(table.to_numpy().sum())
    manual = int(table.loc["Revisión manual"].sum())
    late = int(table["Retrasado"].sum())
    manual_and_late = int(table.loc["Revisión manual", "Retrasado"])
    return {
        "manual": manual / total,
        "late": late / total,
        "manual_and_late": manual_and_late / total,
    }


# --- NUEVO (1) complement_and_union() ---------------------------------------
def complement_and_union(probabilities: dict[str, float]) -> dict[str, float]:
    """Calcula complemento, suma ingenua y unión corregida por traslape."""
    manual = probabilities["manual"]
    late = probabilities["late"]
    overlap = probabilities["manual_and_late"]
    return {
        "not_manual": 1 - manual,
        "naive_sum": manual + late,
        "overlap": overlap,
        "corrected_union": manual + late - overlap,
    }


# ------------------------------------------------------------------------------


# --- NUEVO (2) save_addition_figure() ---------------------------------------
def save_addition_figure(results: dict[str, float]) -> Path:
    """Exporta las probabilidades de unión ingenua, corregida y directa."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "probabilidad_02_adicion.png"

    labels = [
        "Suma ingenua\n$P(M)+P(L)$",
        "Regla de adición\nresta el traslape",
        "Conteo directo\nde la tabla",
    ]
    values = [
        results["naive_sum"],
        results["corrected_union"],
        results["corrected_union"],
    ]
    colors = [TEC_PINK, TEC_BLUE, TEC_NAVY]

    fig, ax = plt.subplots(figsize=(9.4, 5.2))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.58)
    ax.set_ylabel("Probabilidad")
    ax.set_title(
        "La regla de adición elimina el traslape contado dos veces",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.015,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )
    ax.annotate(
        f"Restar traslape = {results['overlap']:.2f}",
        xy=(0.5, results["corrected_union"]),
        xytext=(0.5, 0.53),
        ha="center",
        arrowprops={"arrowstyle": "->", "color": TEC_NAVY},
        color=TEC_NAVY,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ------------------------------------------------------------------------------


def main() -> None:
    """Calcula, verifica, muestra y exporta la evidencia del Paso 2."""
    data = build_operations_data()
    table = contingency_table(data)
    probabilities = table_probabilities(table)
    results = complement_and_union(probabilities)
    direct_union = float(
        ((data["routing"] == "Revisión manual") | (data["delivery"] == "Retrasado")).mean()
    )
    output_path = save_addition_figure(results)

    print("LECCIÓN 08 - PASO 2: REGLAS DE COMPLEMENTO Y ADICIÓN")
    print(f"P(Revisión manual)                  : {probabilities['manual']:.4f}")
    print(f"P(NO Revisión manual)               : {results['not_manual']:.4f}")
    print(f"P(Retrasado)                        : {probabilities['late']:.4f}")
    print(f"P(Revisión manual Y Retrasado)      : {results['overlap']:.4f}")
    print(f"Suma ingenua P(Revisión) + P(Retrasado): {results['naive_sum']:.4f}")
    print(f"Unión por regla de adición          : {results['corrected_union']:.4f}")
    print(f"Unión directa de la tabla           : {direct_union:.4f}")
    print(f"Figura guardada en                  : {output_path}")


if __name__ == "__main__":
    main()

