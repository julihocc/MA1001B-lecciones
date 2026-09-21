"""
Lección 01 - Paso 1: Población, muestra, parámetro y estadístico
================================================================
NUEVO EN ESTE PASO: build_population(), draw_random_sample() y save_figure().

La Receta
Un registro sintético de operaciones representa todos los pedidos de un periodo
de planeación. En esta simulación se puede inspeccionar el registro completo,
pero un analista normalmente observa solo una muestra y usa un estadístico para
estimar un parámetro poblacional.

Ejecútalo:
    uv run es/L01_Poblacion_Muestras_Datos/src/fundos_datos_01_poblacion_muestra.py
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


# --- NUEVO (1) build_population() --------------------------------------------
def build_population(seed: int = SEED) -> pd.DataFrame:
    """Construye un registro sintético de operaciones de negocio."""
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

    return pd.DataFrame(
        {
            "order_id": np.arange(100_001, 100_001 + POPULATION_SIZE),
            "channel": channels,
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )
# ------------------------------------------------------------------------------


# --- NUEVO (2) draw_random_sample() ------------------------------------------
def draw_random_sample(
    population: pd.DataFrame,
    sample_size: int = SAMPLE_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae una muestra aleatoria simple sin reemplazo."""
    return population.sample(n=sample_size, replace=False, random_state=seed)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() --------------------------------------------------
def save_figure(
    population: pd.DataFrame,
    sample: pd.DataFrame,
) -> Path:
    """Guarda las distribuciones de población y muestra sin abrir una ventana."""
    output_path = DIR_FIGURES / "fundos_datos_01_poblacion_muestra.png"
    bins = np.linspace(
        population["processing_time_minutes"].min(),
        population["processing_time_minutes"].max(),
        28,
    )

    fig, ax = plt.subplots(figsize=(8.0, 4.5))
    ax.hist(
        population["processing_time_minutes"],
        bins=bins,
        density=True,
        alpha=0.55,
        color="#1A2E51",
        label=f"Población (N = {len(population):,})",
    )
    ax.hist(
        sample["processing_time_minutes"],
        bins=bins,
        density=True,
        histtype="step",
        linewidth=2.2,
        color="#EC2661",
        label=f"Muestra aleatoria (n = {len(sample)})",
    )
    ax.set_title("Población y muestra: tiempo de procesamiento")
    ax.set_xlabel("Tiempo de procesamiento (minutos)")
    ax.set_ylabel("Densidad")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    population = build_population()
    sample = draw_random_sample(population)

    population_mean = population["processing_time_minutes"].mean()
    sample_mean = sample["processing_time_minutes"].mean()
    estimation_error = abs(sample_mean - population_mean)
    figure_path = save_figure(population, sample)

    print("================================================================")
    print("LECCIÓN 01 - PASO 1: POBLACIÓN Y MUESTRA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño de la población (N)       : {len(population):,}")
    print(f"Tamaño de la muestra aleatoria (n): {len(sample):,}")
    print(f"Parámetro media poblacional (mu) : {population_mean:.2f} min")
    print(f"Estadístico media muestral (x-bar): {sample_mean:.2f} min")
    print(f"Error absoluto de estimación     : {estimation_error:.2f} min")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

