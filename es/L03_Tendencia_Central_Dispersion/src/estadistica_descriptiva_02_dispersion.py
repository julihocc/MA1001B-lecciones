"""
Lección 03 - Paso 2: Desviación estándar y rango intercuartílico
===============================================================
NUEVO EN ESTE PASO: summarize_spread() y save_spread_figure().

La Receta
CAMBIOS RESPECTO A estadistica_descriptiva_01_centro.py
Introdúcelos en este orden:
    1. summarize_spread()      calcula s muestral, cuartiles e IQR
    2. save_spread_figure()    compara media +/- s con Q1, mediana y Q3

Ejecútalo:
    uv run es/L03_Tendencia_Central_Dispersion/src/estadistica_descriptiva_02_dispersion.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 240
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_order_sample(seed: int = SEED) -> pd.DataFrame:
    """Construye la misma muestra sintética de pedidos introducida en el Paso 1."""
    rng = np.random.default_rng(seed)
    items = np.clip(rng.poisson(lam=3.2, size=SAMPLE_SIZE) + 1, 1, 12)
    queue_time = rng.gamma(shape=2.5, scale=3.0, size=SAMPLE_SIZE)
    measurement_noise = rng.normal(loc=0.0, scale=3.0, size=SAMPLE_SIZE)
    processing_time = np.clip(
        32.0 + 1.4 * items + queue_time + measurement_noise,
        8.0,
        None,
    )
    return pd.DataFrame(
        {
            "order_id": np.arange(300_001, 300_001 + SAMPLE_SIZE),
            "items_per_order": items,
            "processing_time_minutes": processing_time.round(2),
        }
    )


def summarize_center(sample: pd.DataFrame) -> dict[str, float]:
    """Devuelve la media aritmética y la mediana introducidas en el Paso 1."""
    values = sample["processing_time_minutes"]
    return {"mean": values.mean(), "median": values.median()}


# --- NUEVO (1) summarize_spread() --------------------------------------------
def summarize_spread(sample: pd.DataFrame) -> dict[str, float]:
    """Devuelve la desviación estándar muestral, los cuartiles y el IQR."""
    values = sample["processing_time_minutes"]
    first_quartile = values.quantile(0.25)
    third_quartile = values.quantile(0.75)
    return {
        "sample_standard_deviation": values.std(ddof=1),
        "first_quartile": first_quartile,
        "third_quartile": third_quartile,
        "interquartile_range": third_quartile - first_quartile,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) save_spread_figure() ------------------------------------------
def save_spread_figure(
    center: dict[str, float],
    spread: dict[str, float],
) -> Path:
    """Guarda dos resúmenes de centro y dispersión en las unidades originales."""
    output_path = DIR_FIGURES / "estadistica_descriptiva_02_dispersion.png"
    mean = center["mean"]
    median = center["median"]
    standard_deviation = spread["sample_standard_deviation"]
    first_quartile = spread["first_quartile"]
    third_quartile = spread["third_quartile"]

    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    ax.errorbar(
        mean,
        1,
        xerr=standard_deviation,
        fmt="o",
        markersize=9,
        capsize=7,
        linewidth=3,
        color="#EC2661",
    )
    ax.errorbar(
        median,
        0,
        xerr=np.array([[median - first_quartile], [third_quartile - median]]),
        fmt="o",
        markersize=9,
        capsize=7,
        linewidth=3,
        color="#0039A6",
    )
    ax.text(
        mean,
        1.14,
        f"media {mean:.2f}; s {standard_deviation:.2f}",
        fontsize=13,
        ha="center",
    )
    ax.text(
        median,
        0.14,
        f"mediana {median:.2f}; IQR {spread['interquartile_range']:.2f}",
        fontsize=13,
        ha="center",
    )
    ax.set_yticks([0, 1], ["50% central", "Alrededor de la media"])
    ax.set_xlabel("Tiempo de procesamiento (minutos)", fontsize=13)
    ax.set_ylim(-0.35, 1.45)
    ax.set_title("Dos descripciones de la dispersión", fontsize=16, fontweight="bold")
    ax.tick_params(labelsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_order_sample()
    center = summarize_center(sample)
    spread = summarize_spread(sample)
    figure_path = save_spread_figure(center, spread)

    print("================================================================")
    print("LECCIÓN 03 - PASO 2: DESVIACIÓN ESTÁNDAR E IQR")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño de la muestra (n)         : {len(sample):,}")
    print(f"Media / mediana                  : {center['mean']:.2f} / "
          f"{center['median']:.2f} min")
    print("Desviación estándar muestral (s) : "
          f"{spread['sample_standard_deviation']:.2f} min")
    print(f"Primer cuartil (Q1)              : {spread['first_quartile']:.2f} min")
    print(f"Tercer cuartil (Q3)              : {spread['third_quartile']:.2f} min")
    print(f"Rango intercuartílico (IQR)      : {spread['interquartile_range']:.2f} min")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

