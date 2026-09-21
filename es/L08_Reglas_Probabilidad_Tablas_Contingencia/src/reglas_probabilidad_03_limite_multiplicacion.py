"""
Lección 08 - Paso 3: El límite de la regla de multiplicación
============================================================
NUEVO EN ESTE PASO: multiplication_diagnostics() y
save_multiplication_limit_figure().

CAMBIOS RESPECTO A reglas_probabilidad_02_complemento_adicion.py
La Receta
---------
Introduce estos cambios en este orden:
    1. multiplication_diagnostics() compara productos marginales y condicionales
    2. save_multiplication_limit_figure() expone el supuesto de independencia

Ejecútalo:
    uv run es/L08_Reglas_Probabilidad_Tablas_Contingencia/src/reglas_probabilidad_03_limite_multiplicacion.py
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


# --- NUEVO (1) multiplication_diagnostics() --------------------------------
def multiplication_diagnostics(
    probabilities: dict[str, float],
) -> dict[str, float]:
    """Compara la intersección observada con dos productos de probabilidad."""
    manual = probabilities["manual"]
    late = probabilities["late"]
    intersection = probabilities["manual_and_late"]
    late_given_manual = intersection / manual
    return {
        "intersection": intersection,
        "marginal_product": manual * late,
        "late_given_manual": late_given_manual,
        "general_product": manual * late_given_manual,
    }


# ------------------------------------------------------------------------------


# --- NUEVO (2) save_multiplication_limit_figure() ---------------------------
def save_multiplication_limit_figure(results: dict[str, float]) -> Path:
    """Exporta producto marginal, regla general e intersección de la tabla."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "probabilidad_03_limite.png"

    labels = [
        "Asumir independencia\n$P(M)P(L)$",
        "Regla general\n$P(M)P(L|M)$",
        "Tabla directa\n$P(M\\cap L)$",
    ]
    values = [
        results["marginal_product"],
        results["general_product"],
        results["intersection"],
    ]
    colors = [TEC_PINK, TEC_BLUE, TEC_NAVY]

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.145)
    ax.set_ylabel("Probabilidad")
    ax.set_title(
        "Multiplicar marginales puede ocultar dependencia",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.004,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )
    ax.text(
        0.98,
        0.95,
        f"$P(L|M)={results['late_given_manual']:.2f}$ mientras $P(L)=0.20$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=TEC_NAVY,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ------------------------------------------------------------------------------


def main() -> None:
    """Calcula, verifica, muestra y exporta la evidencia del Paso 3."""
    data = build_operations_data()
    table = contingency_table(data)
    probabilities = table_probabilities(table)
    results = multiplication_diagnostics(probabilities)
    output_path = save_multiplication_limit_figure(results)

    print("LECCIÓN 08 - PASO 3: EL LÍMITE DE LA REGLA DE MULTIPLICACIÓN")
    print(f"P(Revisión manual)                  : {probabilities['manual']:.4f}")
    print(f"P(Retrasado)                        : {probabilities['late']:.4f}")
    print(f"P observada (Revisión Y Retrasado)  : {results['intersection']:.4f}")
    print(f"Producto marginal ingenuo           : {results['marginal_product']:.4f}")
    print(f"P(Retrasado DADO Revisión manual)   : {results['late_given_manual']:.4f}")
    print(f"Regla general de multiplicación     : {results['general_product']:.4f}")
    print(f"Figura guardada en                  : {output_path}")


if __name__ == "__main__":
    main()

