"""
Lección 03 - Paso 3: Sensibilidad a un retraso extremo
=====================================================
NUEVO EN ESTE PASO: inject_extreme_delay(), compare_summaries() y
save_sensitivity_figure().

La Receta
CAMBIOS RESPECTO A estadistica_descriptiva_02_dispersion.py
Introdúcelos en este orden:
    1. inject_extreme_delay()      cambia un pedido a un retraso de 180 minutos
    2. compare_summaries()         mide cambios en cuatro resúmenes
    3. save_sensitivity_figure()   contrasta las muestras original y modificada

Ejecútalo:
    uv run es/L03_Tendencia_Central_Dispersion/src/estadistica_descriptiva_03_sensibilidad.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 240
EXTREME_DELAY_MINUTES = 180.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_order_sample(seed: int = SEED) -> pd.DataFrame:
    """Construye la misma muestra sintética de pedidos usada en toda la lección."""
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


def summarize_spread(sample: pd.DataFrame) -> dict[str, float]:
    """Devuelve las medidas de dispersión introducidas en el Paso 2."""
    values = sample["processing_time_minutes"]
    first_quartile = values.quantile(0.25)
    third_quartile = values.quantile(0.75)
    return {
        "sample_standard_deviation": values.std(ddof=1),
        "first_quartile": first_quartile,
        "third_quartile": third_quartile,
        "interquartile_range": third_quartile - first_quartile,
    }


# --- NUEVO (1) inject_extreme_delay() ----------------------------------------
def inject_extreme_delay(
    sample: pd.DataFrame,
    delay_minutes: float = EXTREME_DELAY_MINUTES,
) -> tuple[pd.DataFrame, int, float]:
    """Reemplaza el máximo actual por un retraso sintético extremo."""
    modified = sample.copy()
    row_index = int(modified["processing_time_minutes"].idxmax())
    original_value = float(modified.loc[row_index, "processing_time_minutes"])
    modified.loc[row_index, "processing_time_minutes"] = delay_minutes
    return modified, row_index, original_value
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_summaries() -------------------------------------------
def compare_summaries(
    original: pd.DataFrame,
    modified: pd.DataFrame,
) -> pd.DataFrame:
    """Compara centro y dispersión antes y después de un retraso extremo."""
    rows = []
    for scenario, sample in [("Original", original), ("Un extremo", modified)]:
        center = summarize_center(sample)
        spread = summarize_spread(sample)
        rows.append(
            {
                "scenario": scenario,
                "mean": center["mean"],
                "median": center["median"],
                "sample_standard_deviation": spread["sample_standard_deviation"],
                "interquartile_range": spread["interquartile_range"],
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_sensitivity_figure() -------------------------------------
def save_sensitivity_figure(
    original: pd.DataFrame,
    modified: pd.DataFrame,
    comparison: pd.DataFrame,
) -> Path:
    """Guarda la observación cambiada y su efecto en cuatro resúmenes."""
    output_path = DIR_FIGURES / "estadistica_descriptiva_03_sensibilidad.png"
    metric_labels = ["Media", "Mediana", "s muestral", "IQR"]
    columns = [
        "mean",
        "median",
        "sample_standard_deviation",
        "interquartile_range",
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    original_sorted = np.sort(original["processing_time_minutes"].to_numpy())
    modified_sorted = np.sort(modified["processing_time_minutes"].to_numpy())
    ranks = np.arange(1, len(original_sorted) + 1)
    axes[0].plot(ranks, original_sorted, color="#1A2E51", label="Original")
    axes[0].plot(
        ranks,
        modified_sorted,
        color="#EC2661",
        linewidth=2,
        label="Un retraso extremo",
    )
    axes[0].set_xlabel("Observación ordenada", fontsize=12)
    axes[0].set_ylabel("Tiempo de procesamiento (minutos)", fontsize=12)
    axes[0].set_title("Solo cambia un valor registrado", fontsize=14)
    axes[0].legend(frameon=False, fontsize=11)

    positions = np.arange(len(columns))
    width = 0.36
    axes[1].bar(
        positions - width / 2,
        comparison.loc[0, columns],
        width,
        color="#1A2E51",
        label="Original",
    )
    axes[1].bar(
        positions + width / 2,
        comparison.loc[1, columns],
        width,
        color="#EC2661",
        label="Un extremo",
    )
    axes[1].set_xticks(positions, metric_labels)
    axes[1].set_ylabel("Minutos", fontsize=12)
    axes[1].set_title("La media y s muestral responden más", fontsize=14)
    axes[1].legend(frameon=False, fontsize=11)

    for axis in axes:
        axis.tick_params(labelsize=10)
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle(
        "Sensibilidad a un retraso sintético extremo",
        fontsize=16,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    original = build_order_sample()
    modified, row_index, original_value = inject_extreme_delay(original)
    comparison = compare_summaries(original, modified)
    figure_path = save_sensitivity_figure(original, modified, comparison)
    before = comparison.iloc[0]
    after = comparison.iloc[1]

    print("================================================================")
    print("LECCIÓN 03 - PASO 3: SENSIBILIDAD A UN RETRASO EXTREMO")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño de muestra en ambos casos : {len(original):,}")
    print(f"ID del pedido modificado         : {int(original.loc[row_index, 'order_id'])}")
    print(f"Valor modificado                 : {original_value:.2f} -> "
          f"{EXTREME_DELAY_MINUTES:.2f} min")
    print("----------------------------------------------------------------")
    for label, column in [
        ("Media", "mean"),
        ("Mediana", "median"),
        ("Desviación estándar muestral", "sample_standard_deviation"),
        ("Rango intercuartílico", "interquartile_range"),
    ]:
        change = after[column] - before[column]
        print(
            f"{label:<27}: {before[column]:>6.2f} -> "
            f"{after[column]:>6.2f} min (cambio {change:+.2f})"
        )
    print("----------------------------------------------------------------")
    print("Límite: la sensibilidad no es un diagnóstico automático de anomalía.")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

