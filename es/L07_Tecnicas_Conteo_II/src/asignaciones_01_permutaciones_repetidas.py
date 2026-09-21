"""
Lección 07 - Paso 1: Permutaciones con repetición
=================================================
NUEVO EN ESTE PASO: repeated_permutation_count(), enumerate_queue_sequences()
y save_repeated_permutations_figure().

La Receta
Construye el primer programa completo en este orden:
    1. repeated_permutation_count()  elimina reordenamientos duplicados
    2. enumerate_queue_sequences()   verifica la fórmula de forma exhaustiva
    3. save_repeated_permutations_figure() exporta la evidencia de conteo

Ejecútalo:
    uv run es/L07_Tecnicas_Conteo_II/src/asignaciones_01_permutaciones_repetidas.py
"""

from itertools import permutations
from math import factorial
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figuras"
QUEUE_COUNTS = {"Prioridad": 3, "Estándar": 3, "Auditoría": 2}
TEC_BLUE = "#0039A6"
TEC_NAVY = "#1A2E51"
TEC_PINK = "#EC2661"


# --- NUEVO (1) repeated_permutation_count() ---------------------------------
def repeated_permutation_count(counts: tuple[int, ...]) -> int:
    """Devuelve el número de secuencias distintas con etiquetas repetidas."""
    total = sum(counts)
    denominator = 1
    for count in counts:
        denominator *= factorial(count)
    return factorial(total) // denominator


# ------------------------------------------------------------------------------


# --- NUEVO (2) enumerate_queue_sequences() ----------------------------------
def enumerate_queue_sequences() -> list[tuple[str, ...]]:
    """Enumera cada secuencia distinta de etiquetas de cola para ocho solicitudes."""
    labels = [
        queue
        for queue, count in QUEUE_COUNTS.items()
        for _ in range(count)
    ]
    return sorted(set(permutations(labels)))


# ------------------------------------------------------------------------------


# --- NUEVO (3) save_repeated_permutations_figure() --------------------------
def save_repeated_permutations_figure(
    naive_count: int,
    formula_count: int,
    enumerated_count: int,
) -> Path:
    """Exporta una gráfica que compara el conteo ingenuo con el ajustado."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "asignaciones_01_permutaciones_repetidas.png"

    labels = ["Ingenuo $8!$", "Fórmula con\netiquetas repetidas", "Enumeración"]
    values = [naive_count, formula_count, enumerated_count]
    colors = [TEC_PINK, TEC_BLUE, TEC_NAVY]

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_yscale("log")
    ax.set_ylabel("Número de secuencias (escala logarítmica)")
    ax.set_title(
        "Las etiquetas repetidas colapsan reordenamientos duplicados",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value * 1.12,
            f"{value:,}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    ax.text(
        0.98,
        0.05,
        "Ejemplo sintético de red de servicio",
        transform=ax.transAxes,
        ha="right",
        color="#646464",
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ------------------------------------------------------------------------------


def main() -> None:
    """Calcula, verifica, muestra y exporta la evidencia del Paso 1."""
    counts = tuple(QUEUE_COUNTS.values())
    naive_count = factorial(sum(counts))
    formula_count = repeated_permutation_count(counts)
    sequences = enumerate_queue_sequences()
    duplicate_factor = naive_count // formula_count
    output_path = save_repeated_permutations_figure(
        naive_count,
        formula_count,
        len(sequences),
    )

    print("LECCIÓN 07 - PASO 1: PERMUTACIONES CON REPETICIÓN")
    print("Conteos sintéticos de cola       : Prioridad=3, Estándar=3, Auditoría=2")
    print(f"Conteo ingenuo 8!                : {naive_count:,}")
    print(f"Fórmula de permutación repetida  : {formula_count:,}")
    print(f"Secuencias distintas enumeradas  : {len(sequences):,}")
    print(f"Factor de reordenamiento duplicado: {duplicate_factor}")
    print(f"Figura guardada en               : {output_path}")


if __name__ == "__main__":
    main()

