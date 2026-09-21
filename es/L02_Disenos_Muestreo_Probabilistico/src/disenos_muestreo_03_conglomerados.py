"""
Lección 02 - Paso 3: Muestreo por conglomerados de una etapa
===========================================================
NUEVO EN ESTE PASO: draw_cluster_sample(), compare_all_designs() y
save_cluster_figure().

La Receta
CAMBIOS RESPECTO A disenos_muestreo_02_estratificado.py
Introdúcelos en este orden:
    1. draw_cluster_sample()   selecciona instalaciones y conserva todos sus pedidos
    2. compare_all_designs()   compara conteos de unidades y errores de la media
    3. save_cluster_figure()   muestra conglomerados seleccionados y el contraste

Ejecútalo:
    uv run es/L02_Disenos_Muestreo_Probabilistico/src/disenos_muestreo_03_conglomerados.py
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
CLUSTERS_TO_SELECT = 4
REGION_ORDER = ["Norte", "Centro", "Oeste", "Sureste"]
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Construye la misma población sintética usada en toda la lección."""
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


# --- NUEVO (1) draw_cluster_sample() -----------------------------------------
def draw_cluster_sample(
    population: pd.DataFrame,
    clusters_to_select: int = CLUSTERS_TO_SELECT,
    seed: int = SEED,
) -> tuple[pd.DataFrame, list[str]]:
    """Selecciona instalaciones al azar e incluye todos los pedidos de cada una."""
    facilities = np.sort(population["facility_id"].unique())
    rng = np.random.default_rng(seed)
    selected = rng.choice(facilities, size=clusters_to_select, replace=False)
    sample = population.loc[population["facility_id"].isin(selected)].copy()
    return sample, sorted(selected.tolist())
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_all_designs() -----------------------------------------
def compare_all_designs(
    population: pd.DataFrame,
    simple_random: pd.DataFrame,
    stratified: pd.DataFrame,
    cluster: pd.DataFrame,
) -> pd.DataFrame:
    """Compara tamaño de muestra y error de la media en los tres diseños."""
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    rows = []
    for design, sample in [
        ("Aleatoria simple", simple_random),
        ("Estratificado", stratified),
        ("Conglomerados", cluster),
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


# --- NUEVO (3) save_cluster_figure() -----------------------------------------
def save_cluster_figure(
    population: pd.DataFrame,
    selected_facilities: list[str],
    comparison: pd.DataFrame,
) -> Path:
    """Guarda evidencia de instalaciones seleccionadas y error de estimación."""
    output_path = DIR_FIGURES / "disenos_muestreo_03_conglomerados.png"
    facility_means = population.groupby("facility_id")[
        "processing_time_minutes"
    ].mean()
    colors = [
        "#EC2661" if facility in selected_facilities else "#A7B0BF"
        for facility in facility_means.index
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    axes[0].bar(facility_means.index, facility_means.values, color=colors)
    axes[0].axhline(
        population["processing_time_minutes"].mean(),
        color="#1A2E51",
        linestyle="--",
        linewidth=1.6,
        label="Media poblacional",
    )
    axes[0].set_ylabel("Media de la instalación (minutos)")
    axes[0].set_title("Cuatro conglomerados de instalaciones")
    axes[0].tick_params(axis="x", rotation=90, labelsize=7)
    axes[0].legend(frameon=False, fontsize=8)

    design_colors = ["#1A2E51", "#0039A6", "#EC2661"]
    axes[1].bar(
        comparison["design"],
        comparison["absolute_error"],
        color=design_colors,
    )
    axes[1].set_ylabel("Error absoluto (minutos)")
    axes[1].set_title("Error en esta comparación con semilla")
    axes[1].tick_params(axis="x", rotation=12)
    axes[1].set_ylim(0, comparison["absolute_error"].max() * 1.28)
    for index, row in comparison.iterrows():
        axes[1].text(
            index,
            row["absolute_error"] + 0.04,
            f"{row['absolute_error']:.2f}\nn={int(row['size']):,}",
            ha="center",
            fontsize=8,
        )

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("El muestreo por conglomerados selecciona grupos, no pedidos",
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
    cluster, selected_facilities = draw_cluster_sample(population)
    comparison = compare_all_designs(
        population,
        simple_random,
        stratified,
        cluster,
    )
    figure_path = save_cluster_figure(
        population,
        selected_facilities,
        comparison,
    )
    cluster_row = comparison.loc[comparison["design"] == "Conglomerados"].iloc[0]
    selected_regions = sorted(cluster["region"].unique().tolist())

    print("================================================================")
    print("LECCIÓN 02 - PASO 3: MUESTREO POR CONGLOMERADOS DE UNA ETAPA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Instalaciones en el marco        : {FACILITY_COUNT}")
    print(f"Instalaciones seleccionadas      : {', '.join(selected_facilities)}")
    print(f"Pedidos incluidos                : {len(cluster):,}")
    print(f"Probabilidad de inclusión        : {CLUSTERS_TO_SELECT / FACILITY_COUNT:.2%}")
    print(f"Regiones representadas           : {', '.join(selected_regions)}")
    print(f"Estimación media por conglomerados: {cluster_row['mean']:.2f} min")
    print(f"Error absoluto por conglomerados : {cluster_row['absolute_error']:.2f} min")
    print("----------------------------------------------------------------")
    for row in comparison.itertuples(index=False):
        print(
            f"{row.design:<16} n={row.size:>4,}, "
            f"media={row.mean:>5.2f}, error={row.absolute_error:.2f} min"
        )
    print("----------------------------------------------------------------")
    print("Límite: este resultado con semilla no es un ranking universal.")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

