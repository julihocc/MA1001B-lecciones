"""
Lección 02 - Paso 1: Muestreo aleatorio simple
==============================================
NUEVO EN ESTE PASO: build_population(), draw_simple_random_sample(),
summarize_sample() y save_figure().

La Receta
Un registro sintético de operaciones contiene todos los pedidos de 24
instalaciones en un periodo de planeación. El registro completo es el marco
muestral. Un muestreo aleatorio simple da a cada muestra posible de 240
pedidos la misma probabilidad de selección.

Ejecútalo:
    uv run es/L02_Disenos_Muestreo_Probabilistico/src/disenos_muestreo_01_aleatorio_simple.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
FACILITY_COUNT = 24
ORDERS_PER_FACILITY = 500
POPULATION_SIZE = FACILITY_COUNT * ORDERS_PER_FACILITY
SAMPLE_SIZE = 240
REGION_ORDER = ["Norte", "Centro", "Oeste", "Sureste"]
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_population() --------------------------------------------
def build_population(seed: int = SEED) -> pd.DataFrame:
    """Construye una población sintética con estructura de región e instalación."""
    rng = np.random.default_rng(seed)
    facility_numbers = np.arange(FACILITY_COUNT)
    facility_ids = np.array([f"F{number + 1:02d}" for number in facility_numbers])
    facility_region = np.repeat(REGION_ORDER, FACILITY_COUNT // len(REGION_ORDER))
    facility_effect = np.tile(np.array([-8.0, -5.0, -2.0, 0.0, 3.0, 7.0]), 4)
    region_effect = {
        "Norte": -4.0,
        "Centro": 0.0,
        "Oeste": 3.0,
        "Sureste": 7.0,
    }

    facility_index = np.repeat(facility_numbers, ORDERS_PER_FACILITY)
    items = np.clip(rng.poisson(lam=3.2, size=POPULATION_SIZE) + 1, 1, 12)
    noise = rng.normal(loc=0.0, scale=6.0, size=POPULATION_SIZE)
    region_component = np.array(
        [region_effect[facility_region[index]] for index in facility_index]
    )
    processing_time = np.clip(
        42.0
        + region_component
        + facility_effect[facility_index]
        + 1.2 * items
        + noise,
        8.0,
        None,
    )

    return pd.DataFrame(
        {
            "order_id": np.arange(200_001, 200_001 + POPULATION_SIZE),
            "facility_id": facility_ids[facility_index],
            "region": facility_region[facility_index],
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )
# ------------------------------------------------------------------------------


# --- NUEVO (2) draw_simple_random_sample() -----------------------------------
def draw_simple_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae una muestra aleatoria simple de pedidos sin reemplazo."""
    return population.sample(n=sample_size, replace=False, random_state=seed)
# ------------------------------------------------------------------------------


# --- NUEVO (3) summarize_sample() --------------------------------------------
def summarize_sample(
    population: pd.DataFrame,
    sample: pd.DataFrame,
) -> dict[str, float]:
    """Devuelve el parámetro, la estimación, el error y la probabilidad de inclusión."""
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    sample_mean = sample[variable].mean()
    return {
        "population_mean": population_mean,
        "sample_mean": sample_mean,
        "absolute_error": abs(sample_mean - population_mean),
        "inclusion_probability": len(sample) / len(population),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (4) save_figure() --------------------------------------------------
def save_figure(population: pd.DataFrame, sample: pd.DataFrame) -> Path:
    """Guarda la composición y la distribución del MAS sin abrir una ventana."""
    output_path = DIR_FIGURES / "disenos_muestreo_01_aleatorio_simple.png"
    bins = np.linspace(
        population["processing_time_minutes"].min(),
        population["processing_time_minutes"].max(),
        28,
    )
    population_share = (
        population["region"].value_counts(normalize=True).reindex(REGION_ORDER)
    )
    sample_share = sample["region"].value_counts(normalize=True).reindex(REGION_ORDER)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.1))
    positions = np.arange(len(REGION_ORDER))
    width = 0.36
    axes[0].bar(
        positions - width / 2,
        population_share * 100,
        width,
        color="#1A2E51",
        label="Población",
    )
    axes[0].bar(
        positions + width / 2,
        sample_share * 100,
        width,
        color="#EC2661",
        label="MAS",
    )
    axes[0].set_xticks(positions, REGION_ORDER, rotation=15)
    axes[0].set_ylabel("Participación de pedidos (%)")
    axes[0].set_title("Composición por región")
    axes[0].legend(frameon=False)

    axes[1].hist(
        population["processing_time_minutes"],
        bins=bins,
        density=True,
        alpha=0.55,
        color="#1A2E51",
        label="Población",
    )
    axes[1].hist(
        sample["processing_time_minutes"],
        bins=bins,
        density=True,
        histtype="step",
        linewidth=2.2,
        color="#EC2661",
        label="MAS",
    )
    axes[1].set_xlabel("Tiempo de procesamiento (minutos)")
    axes[1].set_ylabel("Densidad")
    axes[1].set_title("Distribución del tiempo de procesamiento")
    axes[1].legend(frameon=False)

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Muestra aleatoria simple de un marco completo", fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    population = build_population()
    sample = draw_simple_random_sample(population)
    summary = summarize_sample(population, sample)
    figure_path = save_figure(population, sample)
    region_counts = sample["region"].value_counts().reindex(REGION_ORDER)

    print("================================================================")
    print("LECCIÓN 02 - PASO 1: MUESTREO ALEATORIO SIMPLE")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño del marco muestral (N)    : {len(population):,}")
    print(f"Tamaño de la muestra MAS (n)     : {len(sample):,}")
    print(
        "Probabilidad igual de inclusión : "
        f"{summary['inclusion_probability']:.2%}"
    )
    print(f"Parámetro media poblacional      : {summary['population_mean']:.2f} min")
    print(f"Estimación media del MAS         : {summary['sample_mean']:.2f} min")
    print(f"Error absoluto del MAS           : {summary['absolute_error']:.2f} min")
    print("Pedidos del MAS por región      : " + ", ".join(
        f"{region}={int(region_counts[region])}" for region in REGION_ORDER
    ))
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

