"""
Lección 07 - Paso 2: Asignaciones multinomiales a categorías
===========================================================
NUEVO EN ESTE PASO: enumerate_labeled_allocations(), first_request_counts() y
save_multinomial_figure().

CAMBIOS RESPECTO A asignaciones_01_permutaciones_repetidas.py
La Receta
---------
Introduce estos cambios en este orden:
    1. enumerate_labeled_allocations() asigna solicitudes etiquetadas a colas fijas
    2. first_request_counts()          revisa una solicitud en todas las asignaciones
    3. save_multinomial_figure()       exporta la evidencia de fórmula y asignación

Ejecútalo:
    uv run es/L07_Tecnicas_Conteo_II/src/asignaciones_02_categorias_multinomiales.py
"""

from collections import Counter
from itertools import combinations, permutations
from math import factorial
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figuras"
QUEUE_COUNTS = {"Prioridad": 3, "Estándar": 3, "Auditoría": 2}
REQUESTS = tuple(f"R{i:02d}" for i in range(1, 9))
TEC_BLUE = "#0039A6"
TEC_NAVY = "#1A2E51"
TEC_PINK = "#EC2661"


def repeated_permutation_count(counts: tuple[int, ...]) -> int:
    """Devuelve el número de secuencias distintas con etiquetas repetidas."""
    total = sum(counts)
    denominator = 1
    for count in counts:
        denominator *= factorial(count)
    return factorial(total) // denominator


def enumerate_queue_sequences() -> list[tuple[str, ...]]:
    """Enumera cada secuencia distinta de etiquetas de cola para ocho solicitudes."""
    labels = [
        queue
        for queue, count in QUEUE_COUNTS.items()
        for _ in range(count)
    ]
    return sorted(set(permutations(labels)))


# --- NUEVO (1) enumerate_labeled_allocations() ------------------------------
def enumerate_labeled_allocations() -> list[dict[str, tuple[str, ...]]]:
    """Asigna ocho solicitudes etiquetadas a tres colas etiquetadas de tamaños fijos."""
    allocations: list[dict[str, tuple[str, ...]]] = []
    for priority in combinations(REQUESTS, QUEUE_COUNTS["Prioridad"]):
        after_priority = tuple(item for item in REQUESTS if item not in priority)
        for standard in combinations(
            after_priority,
            QUEUE_COUNTS["Estándar"],
        ):
            audit = tuple(item for item in after_priority if item not in standard)
            allocations.append(
                {
                    "Prioridad": priority,
                    "Estándar": standard,
                    "Auditoría": audit,
                }
            )
    return allocations


# ------------------------------------------------------------------------------


# --- NUEVO (2) first_request_counts() ---------------------------------------
def first_request_counts(
    allocations: list[dict[str, tuple[str, ...]]],
) -> Counter[str]:
    """Cuenta la cola que contiene R01 en cada asignación válida."""
    counts: Counter[str] = Counter()
    for allocation in allocations:
        for queue, requests in allocation.items():
            if REQUESTS[0] in requests:
                counts[queue] += 1
                break
    return counts


# ------------------------------------------------------------------------------


# --- NUEVO (3) save_multinomial_figure() ------------------------------------
def save_multinomial_figure(
    formula_count: int,
    enumerated_count: int,
    request_counts: Counter[str],
) -> Path:
    """Exporta la verificación de la fórmula y los conteos de R01."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "asignaciones_02_categorias_multinomiales.png"

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.9))
    bars = axes[0].bar(
        ["Fórmula\nmultinomial", "Enumeración"],
        [formula_count, enumerated_count],
        color=[TEC_BLUE, TEC_NAVY],
        width=0.58,
    )
    axes[0].set_title("Total de asignaciones de tamaño fijo", fontweight="bold")
    axes[0].set_ylabel("Número de asignaciones")
    axes[0].set_ylim(0, 640)
    axes[0].grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, [formula_count, enumerated_count], strict=True):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            value + 16,
            f"{value:,}",
            ha="center",
            fontweight="bold",
        )

    queues = list(QUEUE_COUNTS)
    values = [request_counts[queue] for queue in queues]
    bars = axes[1].bar(
        queues,
        values,
        color=[TEC_PINK, TEC_BLUE, TEC_NAVY],
        width=0.62,
    )
    axes[1].set_title("¿A dónde va la solicitud R01?", fontweight="bold")
    axes[1].set_ylabel("Asignaciones que contienen R01")
    axes[1].set_ylim(0, 245)
    axes[1].grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values, strict=True):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 6,
            f"{value:,}",
            ha="center",
            fontweight="bold",
        )

    fig.suptitle(
        "Un coeficiente multinomial, dos lecturas verificables",
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ------------------------------------------------------------------------------


def main() -> None:
    """Calcula, verifica, muestra y exporta la evidencia del Paso 2."""
    formula_count = repeated_permutation_count(tuple(QUEUE_COUNTS.values()))
    allocations = enumerate_labeled_allocations()
    request_counts = first_request_counts(allocations)
    output_path = save_multinomial_figure(
        formula_count,
        len(allocations),
        request_counts,
    )

    print("LECCIÓN 07 - PASO 2: ASIGNACIONES MULTINOMIALES A CATEGORÍAS")
    print(f"Solicitudes etiquetadas            : {len(REQUESTS)}")
    print("Tamaños fijos de cola              : Prioridad=3, Estándar=3, Auditoría=2")
    print(f"Fórmula multinomial                : {formula_count:,}")
    print(f"Asignaciones enumeradas            : {len(allocations):,}")
    for queue in QUEUE_COUNTS:
        print(f"Asignaciones con R01 en {queue:<10} : {request_counts[queue]:,}")
    print(f"Figura guardada en                 : {output_path}")


if __name__ == "__main__":
    main()

