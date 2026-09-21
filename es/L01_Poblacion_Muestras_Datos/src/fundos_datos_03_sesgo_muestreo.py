"""
Lección 01 - Paso 3: El tamaño de muestra no elimina el sesgo de selección
=========================================================================
NUEVO EN ESTE PASO: draw_convenience_sample(), compare_estimates() y
save_bias_figure().

La Receta
CAMBIOS RESPECTO A fundamentos_datos_02_tipos_datos.py
Introdúcelos en este orden:
    1. draw_convenience_sample()  selecciona solo pedidos En línea disponibles
    2. compare_estimates()        mide el error frente a la media poblacional
    3. save_bias_figure()         contrasta tamaño de muestra y error

Ejecútalo:
    uv run es/L01_Poblacion_Muestras_Datos/src/fundos_datos_03_sesgo_muestreo.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
POPULATION_SIZE = 12_000
RANDOM_SAMPLE_SIZE = 200
CONVENIENCE_SAMPLE_SIZE = 1_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_population(seed: int = SEED) -> pd.DataFrame:
    """Construye el mismo registro sintético usado en toda la lección."""
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
    sample_size: int = RANDOM_SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae una muestra aleatoria simple sin reemplazo."""
    return population.sample(n=sample_size, replace=False, random_state=seed)


def add_business_variables(
    population: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Agrega región y valor del pedido como en el Paso 2."""
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


# --- NUEVO (1) draw_convenience_sample() -------------------------------------
def draw_convenience_sample(
    population: pd.DataFrame,
    sample_size: int = CONVENIENCE_SAMPLE_SIZE,
) -> pd.DataFrame:
    """Toma los primeros pedidos En línea disponibles como muestra de conveniencia."""
    available = population.loc[population["channel"] == "En línea"]
    if len(available) < sample_size:
        raise ValueError("La población sintética tiene muy pocos pedidos En línea.")
    return available.head(sample_size)
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_estimates() -------------------------------------------
def compare_estimates(
    population: pd.DataFrame,
    random_sample: pd.DataFrame,
    convenience_sample: pd.DataFrame,
) -> pd.DataFrame:
    """Compara cada media muestral con el parámetro poblacional."""
    variable = "processing_time_minutes"
    population_mean = population[variable].mean()
    rows = []
    for label, sample in [
        ("Aleatoria", random_sample),
        ("Conveniencia", convenience_sample),
    ]:
        sample_mean = sample[variable].mean()
        rows.append(
            {
                "sample": label,
                "size": len(sample),
                "mean": sample_mean,
                "absolute_error": abs(sample_mean - population_mean),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_bias_figure() --------------------------------------------
def save_bias_figure(comparison: pd.DataFrame) -> Path:
    """Guarda tamaños de muestra y errores de estimación."""
    output_path = DIR_FIGURES / "fundos_datos_03_sesgo_muestreo.png"
    colors = ["#0039A6", "#EC2661"]
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.0))

    axes[0].bar(comparison["sample"], comparison["size"], color=colors)
    axes[0].set_title("Tamaño de muestra")
    axes[0].set_ylabel("Número de pedidos")

    axes[1].bar(
        comparison["sample"],
        comparison["absolute_error"],
        color=colors,
    )
    axes[1].set_title("Error respecto a la media poblacional")
    axes[1].set_ylabel("Error absoluto (minutos)")

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle(
        "Una muestra sesgada más grande puede producir más error",
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    population = build_population()
    random_sample = draw_random_sample(population)
    convenience_sample = draw_convenience_sample(population)
    comparison = compare_estimates(
        population,
        random_sample,
        convenience_sample,
    )
    figure_path = save_bias_figure(comparison)

    population_mean = population["processing_time_minutes"].mean()
    random_row = comparison.loc[comparison["sample"] == "Aleatoria"].iloc[0]
    convenience_row = comparison.loc[
        comparison["sample"] == "Conveniencia"
    ].iloc[0]

    print("================================================================")
    print("LECCIÓN 01 - PASO 3: TAMAÑO DE MUESTRA Y SESGO DE SELECCIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Parámetro media poblacional      : {population_mean:.2f} min")
    print(
        f"Muestra aleatoria (n={int(random_row['size']):,}) media: "
        f"{random_row['mean']:.2f} min"
    )
    print(f"Error absoluto muestra aleatoria : {random_row['absolute_error']:.2f} min")
    print(
        f"Muestra conveniencia (n={int(convenience_row['size']):,}) media: "
        f"{convenience_row['mean']:.2f} min"
    )
    print(
        "Error absoluto de conveniencia    : "
        f"{convenience_row['absolute_error']:.2f} min"
    )
    print(
        "La muestra grande tiene más error : "
        f"{convenience_row['absolute_error'] > random_row['absolute_error']}"
    )
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

