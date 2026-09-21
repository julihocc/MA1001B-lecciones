"""
Lección 02 - Paso 2: Muestreo estratificado proporcional
=======================================================
NUEVO EN ESTE PASO: allocate_proportionally(), draw_stratified_sample(),
compare_designs() y save_stratified_figure().

La Receta
CAMBIOS RESPECTO A disenos_muestreo_01_aleatorio_simple.py
Introdúcelos en este orden:
    1. allocate_proportionally()  asigna la muestra a todas las regiones
    2. draw_stratified_sample()   extrae un MAS dentro de cada región
    3. compare_designs()          compara composición muestral y error de la media
    4. save_stratified_figure()   visualiza representación y estimación

Ejecútalo:
    uv run es/L02_Disenos_Muestreo_Probabilistico/src/disenos_muestreo_02_estratificado.py
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


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Construye la misma población sintética introducida en el Paso 1."""
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


def draw_simple_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae la muestra aleatoria simple introducida en el Paso 1."""
    return population.sample(n=sample_size, replace=False, random_state=seed)


# --- NUEVO (1) allocate_proportionally() -------------------------------------
def allocate_proportionally(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
) -> pd.Series:
    """Asigna conteos enteros de muestra a partir de las participaciones de los estratos."""
    counts = population["region"].value_counts().reindex(REGION_ORDER)
    raw_allocation = counts / len(population) * sample_size
    allocation = np.floor(raw_allocation).astype(int)
    remaining = sample_size - int(allocation.sum())
    fractions = (raw_allocation - allocation).sort_values(ascending=False)
    for region in fractions.index[:remaining]:
        allocation.loc[region] += 1
    return allocation
# ------------------------------------------------------------------------------


# --- NUEVO (2) draw_stratified_sample() --------------------------------------
def draw_stratified_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae una muestra aleatoria simple proporcional dentro de cada región."""
    allocation = allocate_proportionally(population, sample_size)
    pieces = []
    for index, region in enumerate(REGION_ORDER):
        stratum = population.loc[population["region"] == region]
        pieces.append(
            stratum.sample(
                n=int(allocation.loc[region]),
                replace=False,
                random_state=seed + index,
            )
        )
    return pd.concat(pieces, ignore_index=True)
# ------------------------------------------------------------------------------


# --- NUEVO (3) compare_designs() ---------------------------------------------
def compare_designs(
    population: pd.DataFrame,
    simple_random: pd.DataFrame,
    stratified: pd.DataFrame,
) -> pd.DataFrame:
    """Compara las dos medias muestrales con el parámetro poblacional."""
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    rows = []
    for design, sample in [
        ("Aleatoria simple", simple_random),
        ("Estratificado", stratified),
    ]:
        sample_mean = sample[variable].mean()
        rows.append(
            {
                "design": design,
                "size": len(sample),
                "mean": sample_mean,
                "absolute_error": abs(sample_mean - population_mean),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (4) save_stratified_figure() --------------------------------------
def save_stratified_figure(
    simple_random: pd.DataFrame,
    stratified: pd.DataFrame,
    comparison: pd.DataFrame,
) -> Path:
    """Guarda evidencia de representación y error de dos diseños probabilísticos."""
    output_path = DIR_FIGURES / "disenos_muestreo_02_estratificado.png"
    simple_counts = simple_random["region"].value_counts().reindex(REGION_ORDER)
    stratified_counts = stratified["region"].value_counts().reindex(REGION_ORDER)

    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.1))
    positions = np.arange(len(REGION_ORDER))
    width = 0.36
    axes[0].bar(
        positions - width / 2,
        simple_counts,
        width,
        color="#1A2E51",
        label="Aleatoria simple",
    )
    axes[0].bar(
        positions + width / 2,
        stratified_counts,
        width,
        color="#EC2661",
        label="Estratificado",
    )
    axes[0].set_xticks(positions, REGION_ORDER, rotation=15)
    axes[0].set_ylabel("Pedidos muestreados")
    axes[0].set_title("Representación por región")
    axes[0].legend(frameon=False)

    axes[1].bar(
        comparison["design"],
        comparison["absolute_error"],
        color=["#1A2E51", "#EC2661"],
    )
    axes[1].set_ylabel("Error absoluto (minutos)")
    axes[1].set_title("Error en esta muestra con semilla")
    axes[1].set_ylim(0, comparison["absolute_error"].max() * 1.25)
    for index, value in enumerate(comparison["absolute_error"]):
        axes[1].text(index, value + 0.02, f"{value:.2f}", ha="center")

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("La estratificación garantiza representación de cada región",
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    population = build_population()
    simple_random = draw_simple_random_sample(population)
    stratified = draw_stratified_sample(population)
    allocation = allocate_proportionally(population)
    comparison = compare_designs(population, simple_random, stratified)
    figure_path = save_stratified_figure(simple_random, stratified, comparison)

    population_mean = population["processing_time_minutes"].mean()
    simple_row = comparison.loc[comparison["design"] == "Aleatoria simple"].iloc[0]
    stratified_row = comparison.loc[comparison["design"] == "Estratificado"].iloc[0]

    print("================================================================")
    print("LECCIÓN 02 - PASO 2: MUESTREO ESTRATIFICADO PROPORCIONAL")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Parámetro media poblacional      : {population_mean:.2f} min")
    print("Asignación por región           : " + ", ".join(
        f"{region}={int(allocation[region])}" for region in REGION_ORDER
    ))
    print(f"MAS media / error absoluto       : {simple_row['mean']:.2f} / "
          f"{simple_row['absolute_error']:.2f} min")
    print(f"Estratificado media / error abs. : {stratified_row['mean']:.2f} / "
          f"{stratified_row['absolute_error']:.2f} min")
    print("Todas las regiones representadas: True")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

