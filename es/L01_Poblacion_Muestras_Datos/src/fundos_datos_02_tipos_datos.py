"""
Lección 01 - Paso 2: Tipos de datos de negocio
==============================================
NUEVO EN ESTE PASO: add_business_variables(), classify_variables() y
save_data_types_figure().

La Receta
CAMBIOS RESPECTO A fundamentos_datos_01_poblacion_muestra.py
Introdúcelos en este orden:
    1. add_business_variables()    agrega región y valor del pedido
    2. classify_variables()        separa el rol analítico del tipo de almacenamiento
    3. save_data_types_figure()    compara categórica, discreta y continua

Ejecútalo:
    uv run es/L01_Poblacion_Muestras_Datos/src/fundos_datos_02_tipos_datos.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
POPULATION_SIZE = 12_000
SAMPLE_SIZE = 200
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Construye el mismo registro sintético introducido en el Paso 1."""
    rng = np.random.default_rng(seed)
    channels = rng.choice(
        ["Mostrador", "En línea", "Socio"],
        size=POPULATION_SIZE,
        p=[0.45, 0.35, 0.20],
    )
    channel_effect = pd.Series(channels).map(
        {"Mostrador": 6.0, "En línea": -5.0, "Socio": 2.0}
    )
    items = np.clip(rng.poisson(lam=3.2, size=POPULATION_SIZE) + 1, 1, 12)
    noise = rng.normal(loc=0.0, scale=7.0, size=POPULATION_SIZE)
    processing_time = np.clip(
        38.0 + channel_effect.to_numpy() + 1.4 * items + noise,
        8.0,
        None,
    )
    population = pd.DataFrame(
        {
            "order_id": np.arange(100_001, 100_001 + POPULATION_SIZE),
            "channel": channels,
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )
    return add_business_variables(population, rng)


def draw_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae la misma muestra aleatoria simple introducida en el Paso 1."""
    return population.sample(n=sample_size, replace=False, random_state=seed)


# --- NUEVO (1) add_business_variables() --------------------------------------
def add_business_variables(
    population: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Agrega una variable categórica y una continua de negocio."""
    result = population.copy()
    result["region"] = rng.choice(
        ["Norte", "Centro", "Sur"],
        size=len(result),
        p=[0.30, 0.45, 0.25],
    )
    unit_value = rng.gamma(shape=3.0, scale=180.0, size=len(result))
    result["order_value_mxn"] = (
        unit_value * result["items_per_order"]
    ).round(2)
    return result
# ------------------------------------------------------------------------------


# --- NUEVO (2) classify_variables() ------------------------------------------
def classify_variables() -> dict[str, str]:
    """Devuelve el rol analítico de cada variable en la lección."""
    return {
        "order_id": "Identificador (rol categórico)",
        "channel": "Categórica",
        "region": "Categórica",
        "items_per_order": "Cuantitativa discreta",
        "processing_time_minutes": "Cuantitativa continua",
        "order_value_mxn": "Cuantitativa continua",
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_data_types_figure() --------------------------------------
def save_data_types_figure(sample: pd.DataFrame) -> Path:
    """Guarda ejemplos de variables categóricas, discretas y continuas."""
    output_path = DIR_FIGURES / "fundos_datos_02_tipos_datos.png"
    colors = ["#0039A6", "#EC2661", "#646464"]
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.8))

    channel_counts = sample["channel"].value_counts().reindex(
        ["Mostrador", "En línea", "Socio"]
    )
    axes[0].bar(channel_counts.index, channel_counts.values, color=colors)
    axes[0].set_title("Categórica")
    axes[0].set_ylabel("Pedidos")
    axes[0].tick_params(axis="x", rotation=20)

    item_counts = sample["items_per_order"].value_counts().sort_index()
    axes[1].bar(item_counts.index, item_counts.values, color="#0039A6")
    axes[1].set_title("Cuantitativa discreta")
    axes[1].set_xlabel("Artículos por pedido")

    axes[2].hist(
        sample["processing_time_minutes"],
        bins=14,
        color="#EC2661",
        alpha=0.85,
    )
    axes[2].set_title("Cuantitativa continua")
    axes[2].set_xlabel("Tiempo de procesamiento")

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Una muestra, tres tipos analíticos de datos", fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    population = build_population()
    sample = draw_random_sample(population)
    variable_roles = classify_variables()
    figure_path = save_data_types_figure(sample)

    print("================================================================")
    print("LECCIÓN 01 - PASO 2: TIPOS DE DATOS DE NEGOCIO")
    print("================================================================")
    print("Aviso de datos sintéticos: No se usan datos reales de empresa")
    for variable, role in variable_roles.items():
        print(f"{variable:<28}: {role}")
    print("----------------------------------------------------------------")
    print("Precaución: order_id contiene números pero actúa como etiqueta.")
    print(f"Filas de la muestra              : {len(sample):,}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

