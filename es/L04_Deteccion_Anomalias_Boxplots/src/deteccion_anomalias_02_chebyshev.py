"""
Lección 04 - Paso 2: La regla de Chebyshov
=========================================
NUEVO EN ESTE PASO: add_queue_delays(), chebyshev_coverage() y
save_chebyshev_figure().

La Receta
CAMBIOS RESPECTO A deteccion_anomalias_01_regla_empirica.py
Introdúcelos en este orden:
    1. add_queue_delays()       crea una versión con cola derecha de la muestra
    2. chebyshev_coverage()     compara la cobertura observada con cotas inferiores
    3. save_chebyshev_figure()  muestra la forma y la garantía juntas

Ejecútalo:
    uv run es/L04_Deteccion_Anomalias_Boxplots/src/deteccion_anomalias_02_chebyshev.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 600
DELAY_PROBABILITY = 0.10
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_baseline_orders(seed: int = SEED) -> pd.DataFrame:
    """Construye la muestra sintética de pedidos con forma de campana del Paso 1."""
    rng = np.random.default_rng(seed)
    processing_time = np.clip(
        rng.normal(loc=45.0, scale=5.0, size=SAMPLE_SIZE),
        20.0,
        None,
    )
    return pd.DataFrame(
        {
            "order_id": np.arange(400_001, 400_001 + SAMPLE_SIZE),
            "processing_time_minutes": processing_time.round(2),
        }
    )


def empirical_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Calcula el centro, la dispersión y la cobertura por intervalos del Paso 1."""
    values = orders["processing_time_minutes"]
    mean = float(values.mean())
    standard_deviation = float(values.std(ddof=1))
    coverage = {
        k: float((values.sub(mean).abs() <= k * standard_deviation).mean() * 100)
        for k in (1, 2, 3)
    }
    return {
        "mean": mean,
        "sample_standard_deviation": standard_deviation,
        "coverage_percent": coverage,
    }


# --- NUEVO (1) add_queue_delays() --------------------------------------------
def add_queue_delays(seed: int = SEED) -> tuple[pd.DataFrame, int]:
    """Agrega retrasos de cola con distribución gamma a un subconjunto sembrado."""
    orders = build_baseline_orders(seed)
    rng = np.random.default_rng(seed)
    rng.normal(loc=45.0, scale=5.0, size=SAMPLE_SIZE)
    delayed = rng.random(SAMPLE_SIZE) < DELAY_PROBABILITY
    queue_delay = np.where(
        delayed,
        rng.gamma(shape=2.0, scale=5.0, size=SAMPLE_SIZE),
        0.0,
    )
    orders["processing_time_minutes"] = (
        orders["processing_time_minutes"] + queue_delay
    ).round(2)
    orders["has_queue_delay"] = delayed
    return orders, int(delayed.sum())
# ------------------------------------------------------------------------------


# --- NUEVO (2) chebyshev_coverage() ------------------------------------------
def chebyshev_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Calcula cobertura y cotas inferiores de Chebyshov para k = 2 y 3."""
    values = orders["processing_time_minutes"]
    mean = float(values.mean())
    standard_deviation = float(values.std(ddof=1))
    coverage = {
        k: float((values.sub(mean).abs() <= k * standard_deviation).mean() * 100)
        for k in (2, 3)
    }
    bounds = {k: (1 - 1 / k**2) * 100 for k in (2, 3)}
    return {
        "mean": mean,
        "sample_standard_deviation": standard_deviation,
        "skewness": float(values.skew()),
        "coverage_percent": coverage,
        "lower_bound_percent": bounds,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_chebyshev_figure() ---------------------------------------
def save_chebyshev_figure(
    orders: pd.DataFrame,
    summary: dict[str, object],
) -> Path:
    """Guarda los datos con cola derecha y las comparaciones de Chebyshov."""
    output_path = DIR_FIGURES / "deteccion_anomalias_02_chebyshev.png"
    coverage = summary["coverage_percent"]
    bounds = summary["lower_bound_percent"]

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    axes[0].hist(
        orders["processing_time_minutes"],
        bins=28,
        color="#A7B0BF",
        edgecolor="white",
    )
    axes[0].axvline(
        summary["mean"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Media = {summary['mean']:.2f}",
    )
    axes[0].set_title("Tiempos de procesamiento con cola derecha", fontsize=15)
    axes[0].set_xlabel("Tiempo de procesamiento (minutos)", fontsize=12)
    axes[0].set_ylabel("Pedidos", fontsize=12)
    axes[0].tick_params(labelsize=10)
    axes[0].legend(frameon=False, fontsize=10)

    positions = np.arange(2)
    width = 0.34
    actual = [coverage[k] for k in (2, 3)]
    minimum = [bounds[k] for k in (2, 3)]
    axes[1].bar(
        positions - width / 2,
        minimum,
        width,
        color="#1A2E51",
        label="Cota inferior de Chebyshov",
    )
    axes[1].bar(
        positions + width / 2,
        actual,
        width,
        color="#EC2661",
        label="Cobertura observada",
    )
    axes[1].set_xticks(positions, ["Dentro de 2s", "Dentro de 3s"])
    axes[1].set_ylim(0, 108)
    axes[1].set_ylabel("Porcentaje", fontsize=12)
    axes[1].set_title("Garantía y observación", fontsize=15)
    axes[1].tick_params(labelsize=10)
    axes[1].legend(
        frameon=False,
        fontsize=10,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=2,
    )
    for position, lower, observed in zip(positions, minimum, actual):
        axes[1].text(position - width / 2, lower + 1.5, f"{lower:.2f}%", ha="center")
        axes[1].text(position + width / 2, observed + 1.5, f"{observed:.2f}%", ha="center")

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Regla de Chebyshov para cualquier forma de distribución", fontsize=17,
                 fontweight="bold")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    orders, delayed_count = add_queue_delays()
    summary = chebyshev_coverage(orders)
    figure_path = save_chebyshev_figure(orders, summary)
    coverage = summary["coverage_percent"]
    bounds = summary["lower_bound_percent"]

    print("================================================================")
    print("LECCIÓN 04 - PASO 2: LA REGLA DE CHEBYSHOV")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño de la muestra (n)         : {len(orders):,}")
    print(f"Pedidos con retraso de cola      : {delayed_count}")
    print(f"Media                            : {summary['mean']:.2f} min")
    print("Desviación estándar muestral (s) : "
          f"{summary['sample_standard_deviation']:.2f} min")
    print(f"Asimetría muestral               : {summary['skewness']:.2f}")
    for k in (2, 3):
        print(
            f"Dentro de {k}s: observado / cota   : "
            f"{coverage[k]:.2f}% / {bounds[k]:.2f}%"
        )
    print("Alcance                          : Cualquier forma de distribución")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

