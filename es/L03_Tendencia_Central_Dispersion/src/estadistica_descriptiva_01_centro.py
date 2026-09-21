"""
Lección 03 - Paso 1: Media y mediana
===================================
NUEVO EN ESTE PASO: build_order_sample(), summarize_center() y
save_center_figure().

La Receta
Una muestra sintética contiene tiempos de procesamiento de 240 pedidos de
negocio. La media usa cada valor numérico, mientras que la mediana es el
punto medio de las observaciones ordenadas.

Ejecútalo:
    uv run es/L03_Tendencia_Central_Dispersion/src/estadistica_descriptiva_01_centro.py
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


# --- NUEVO (1) build_order_sample() ------------------------------------------
def build_order_sample(seed: int = SEED) -> pd.DataFrame:
    """Construye una muestra sintética de tiempos de procesamiento de pedidos."""
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
# ------------------------------------------------------------------------------


# --- NUEVO (2) summarize_center() --------------------------------------------
def summarize_center(sample: pd.DataFrame) -> dict[str, float]:
    """Devuelve la media aritmética y la mediana del tiempo de procesamiento."""
    values = sample["processing_time_minutes"]
    return {
        "mean": values.mean(),
        "median": values.median(),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_center_figure() ------------------------------------------
def save_center_figure(
    sample: pd.DataFrame,
    center: dict[str, float],
) -> Path:
    """Guarda un histograma con líneas de referencia de media y mediana."""
    output_path = DIR_FIGURES / "estadistica_descriptiva_01_centro.png"
    values = sample["processing_time_minutes"]

    fig, ax = plt.subplots(figsize=(8.2, 4.5))
    ax.hist(values, bins=18, color="#A7B0BF", edgecolor="white")
    ax.axvline(
        center["mean"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Media = {center['mean']:.2f}",
    )
    ax.axvline(
        center["median"],
        color="#0039A6",
        linewidth=2.4,
        linestyle="--",
        label=f"Mediana = {center['median']:.2f}",
    )
    ax.set_title(
        "Centro de tiempos sintéticos de procesamiento",
        fontsize=16,
        fontweight="bold",
    )
    ax.set_xlabel("Tiempo de procesamiento (minutos)", fontsize=13)
    ax.set_ylabel("Pedidos", fontsize=13)
    ax.tick_params(labelsize=11)
    ax.legend(frameon=False, fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_order_sample()
    center = summarize_center(sample)
    figure_path = save_center_figure(sample, center)

    print("================================================================")
    print("LECCIÓN 03 - PASO 1: MEDIA Y MEDIANA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño de la muestra (n)         : {len(sample):,}")
    print(f"Media aritmética                 : {center['mean']:.2f} min")
    print(f"Mediana                          : {center['median']:.2f} min")
    print(f"Media menos mediana              : {center['mean'] - center['median']:.2f} min")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

