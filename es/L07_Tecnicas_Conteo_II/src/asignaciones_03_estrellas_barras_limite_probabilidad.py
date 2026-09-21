"""
Lección 07 - Paso 3: Estrellas y barras, luego el límite de probabilidad
=======================================================================
NUEVO EN ESTE PASO: enumerate_occupancy_profiles(), multinomial_probability(),
simulate_profile_probabilities() y save_probability_limit_figure().

CAMBIOS RESPECTO A asignaciones_02_categorias_multinomiales.py
La Receta
---------
Introduce estos cambios en este orden:
    1. enumerate_occupancy_profiles() cuenta perfiles de ocupación no negativos
    2. multinomial_probability()      pondera un perfil bajo enrutamiento aleatorio
    3. simulate_profile_probabilities() verifica las probabilidades con semilla 42
    4. save_probability_limit_figure() contrasta conteo y probabilidad

Ejecútalo:
    uv run es/L07_Tecnicas_Conteo_II/src/asignaciones_03_estrellas_barras_limite_probabilidad.py
"""

from collections import Counter
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


FIGURES_DIR = Path(__file__).resolve().parents[1] / "figuras"
QUEUE_COUNTS = {"Prioridad": 3, "Estándar": 3, "Auditoría": 2}
REQUESTS = tuple(f"R{i:02d}" for i in range(1, 9))
TOTAL_REQUESTS = 8
SERVICE_CENTERS = 4
SIMULATIONS = 500_000
SEED = 42
SELECTED_PROFILES = ((5, 1, 1, 1), (4, 2, 1, 1), (3, 2, 2, 1))
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


# --- NUEVO (1) enumerate_occupancy_profiles() -------------------------------
def enumerate_occupancy_profiles(
    total: int,
    categories: int,
) -> list[tuple[int, ...]]:
    """Enumera todos los perfiles ordenados no negativos que suman total."""
    return [
        profile
        for profile in product(range(total + 1), repeat=categories)
        if sum(profile) == total
    ]


# ------------------------------------------------------------------------------


# --- NUEVO (2) multinomial_probability() ------------------------------------
def multinomial_probability(profile: tuple[int, ...]) -> float:
    """Devuelve la probabilidad exacta bajo enrutamiento uniforme independiente."""
    multiplicity = repeated_permutation_count(profile)
    return multiplicity * (1 / len(profile)) ** sum(profile)


# ------------------------------------------------------------------------------


# --- NUEVO (3) simulate_profile_probabilities() -----------------------------
def simulate_profile_probabilities(
    profiles: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], float]:
    """Estima probabilidades de ocupación seleccionadas con un RNG determinista."""
    rng = np.random.default_rng(SEED)
    draws = rng.multinomial(
        TOTAL_REQUESTS,
        [1 / SERVICE_CENTERS] * SERVICE_CENTERS,
        size=SIMULATIONS,
    )
    return {
        profile: float(np.mean(np.all(draws == profile, axis=1)))
        for profile in profiles
    }


# ------------------------------------------------------------------------------


# --- NUEVO (4) save_probability_limit_figure() ------------------------------
def save_probability_limit_figure(
    uniform_profile_probability: float,
    exact_probabilities: dict[tuple[int, ...], float],
    simulated_probabilities: dict[tuple[int, ...], float],
) -> Path:
    """Exporta las probabilidades uniforme incorrecta, exacta y simulada."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = (
        FIGURES_DIR / "asignaciones_03_estrellas_barras_limite_probabilidad.png"
    )

    x = np.arange(len(SELECTED_PROFILES))
    width = 0.25
    uniform_values = [uniform_profile_probability] * len(SELECTED_PROFILES)
    exact_values = [exact_probabilities[item] for item in SELECTED_PROFILES]
    simulated_values = [
        simulated_probabilities[item] for item in SELECTED_PROFILES
    ]

    fig, ax = plt.subplots(figsize=(10.4, 5.2))
    ax.bar(
        x - width,
        uniform_values,
        width,
        label="Incorrecto: $1/165$",
        color=TEC_PINK,
    )
    ax.bar(
        x,
        exact_values,
        width,
        label="Multinomial exacta",
        color=TEC_BLUE,
    )
    ax.bar(
        x + width,
        simulated_values,
        width,
        label="Simulación (semilla 42)",
        color=TEC_NAVY,
    )
    ax.set_xticks(x, [str(profile) for profile in SELECTED_PROFILES])
    ax.set_xlabel("Perfil de ocupación ordenado en cuatro centros")
    ax.set_ylabel("Probabilidad")
    ax.set_title(
        "Contar perfiles no los hace igualmente probables",
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ------------------------------------------------------------------------------


def main() -> None:
    """Calcula, verifica, muestra y exporta la evidencia del Paso 3."""
    profiles = enumerate_occupancy_profiles(TOTAL_REQUESTS, SERVICE_CENTERS)
    stars_and_bars_count = comb(
        TOTAL_REQUESTS + SERVICE_CENTERS - 1,
        SERVICE_CENTERS - 1,
    )
    uniform_profile_probability = 1 / stars_and_bars_count
    exact_probabilities = {
        profile: multinomial_probability(profile)
        for profile in SELECTED_PROFILES
    }
    simulated_probabilities = simulate_profile_probabilities(SELECTED_PROFILES)
    output_path = save_probability_limit_figure(
        uniform_profile_probability,
        exact_probabilities,
        simulated_probabilities,
    )

    print("LECCIÓN 07 - PASO 3: ESTRELLAS Y BARRAS, LUEGO EL LÍMITE DE PROBABILIDAD")
    print(f"Solicitudes / unidades de asignación : {TOTAL_REQUESTS}")
    print(f"Centros de servicio etiquetados      : {SERVICE_CENTERS}")
    print(f"Fórmula de estrellas y barras        : {stars_and_bars_count:,}")
    print(f"Perfiles de ocupación enumerados     : {len(profiles):,}")
    print(f"Probabilidad igual incorrecta        : {uniform_profile_probability:.8f}")
    print(f"Simulaciones con semilla {SEED:<2}         : {SIMULATIONS:,}")
    for profile in SELECTED_PROFILES:
        print(
            f"Perfil {profile}: exacta={exact_probabilities[profile]:.8f}, "
            f"simulada={simulated_probabilities[profile]:.8f}"
        )
    print(f"Figura guardada en                   : {output_path}")


if __name__ == "__main__":
    main()

