"""
Lección 08 - Paso 1: Probabilidades desde una tabla de contingencia
===================================================================
NUEVO EN ESTE PASO: build_operations_data(), contingency_table(),
table_probabilities() y save_contingency_figure().

La Receta
Construye el primer programa completo en este orden:
    1. build_operations_data()   crea 400 registros sintéticos de pedidos mezclados
    2. contingency_table()       clasifica en cruz el enrutamiento y el estado de entrega
    3. table_probabilities()     calcula probabilidades marginales y conjuntas
    4. save_contingency_figure() exporta la evidencia de conteos y probabilidades

Ejecútalo:
    uv run es/L08_Reglas_Probabilidad_Tablas_Contingencia/src/reglas_probabilidad_01_tabla_contingencia.py
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


# --- NUEVO (1) build_operations_data() --------------------------------------
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


# ------------------------------------------------------------------------------


# --- NUEVO (2) contingency_table() ------------------------------------------
def contingency_table(data: pd.DataFrame) -> pd.DataFrame:
    """Devuelve la tabla de conteos enrutamiento por entrega en orden fijo."""
    return pd.crosstab(data["routing"], data["delivery"]).reindex(
        index=ROUTING_ORDER,
        columns=DELIVERY_ORDER,
        fill_value=0,
    )


# ------------------------------------------------------------------------------


# --- NUEVO (3) table_probabilities() ----------------------------------------
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


# ------------------------------------------------------------------------------


# --- NUEVO (4) save_contingency_figure() ------------------------------------
def save_contingency_figure(table: pd.DataFrame) -> Path:
    """Exporta un mapa de calor con conteos de celda y probabilidades conjuntas."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "probabilidad_01_tabla.png"

    values = table.to_numpy()
    total = int(values.sum())
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    image = ax.imshow(values, cmap="Blues", vmin=0, vmax=values.max())
    ax.set_xticks(range(len(DELIVERY_ORDER)), DELIVERY_ORDER)
    ax.set_yticks(range(len(ROUTING_ORDER)), ROUTING_ORDER)
    ax.set_xlabel("Estado de entrega")
    ax.set_ylabel("Proceso de enrutamiento")
    ax.set_title(
        "Tabla de contingencia de pedidos sintéticos",
        fontweight="bold",
        pad=12,
    )

    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            count = int(values[row, column])
            color = "white" if count > values.max() / 2 else TEC_NAVY
            ax.text(
                column,
                row,
                f"{count}\n({count / total:.1%})",
                ha="center",
                va="center",
                color=color,
                fontsize=13,
                fontweight="bold",
            )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.set_label("Conteo de pedidos")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ------------------------------------------------------------------------------


def main() -> None:
    """Calcula, verifica, muestra y exporta la evidencia del Paso 1."""
    data = build_operations_data()
    table = contingency_table(data)
    probabilities = table_probabilities(table)
    output_path = save_contingency_figure(table)

    print("LECCIÓN 08 - PASO 1: PROBABILIDADES DESDE UNA TABLA DE CONTINGENCIA")
    print(f"Pedidos sintéticos                  : {len(data):,}")
    print("Conteos enrutamiento x entrega:")
    print(table.to_string())
    print(f"P(Revisión manual)                  : {probabilities['manual']:.4f}")
    print(f"P(Retrasado)                        : {probabilities['late']:.4f}")
    print(
        "P(Revisión manual Y Retrasado)      : "
        f"{probabilities['manual_and_late']:.4f}"
    )
    print(f"Figura guardada en                  : {output_path}")


if __name__ == "__main__":
    main()

