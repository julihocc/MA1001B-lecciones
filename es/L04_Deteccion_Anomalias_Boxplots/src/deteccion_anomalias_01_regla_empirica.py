"""
Lección 04 - Paso 1: La regla empírica
=====================================
NUEVO EN ESTE PASO: build_baseline_orders(), empirical_coverage() y
save_empirical_rule_figure().

La Receta
Crea una muestra sintética de tiempos de procesamiento con forma de campana,
calcula su media y desviación estándar muestral, y compara la cobertura
observada con los puntos de referencia de la regla empírica. La regla es una
aproximación para datos simétricos con forma de campana.

Ejecútalo:
    uv run es/L04_Deteccion_Anomalias_Boxplots/src/deteccion_anomalias_01_regla_empirica.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 600
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_baseline_orders() ---------------------------------------
def build_baseline_orders(seed: int = SEED) -> pd.DataFrame:
    """Construye tiempos de procesamiento con forma de campana para pedidos sintéticos."""
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
# ------------------------------------------------------------------------------


# --- NUEVO (2) empirical_coverage() ------------------------------------------
def empirical_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Calcula la cobertura observada dentro de una, dos y tres s muestrales."""
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
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_empirical_rule_figure() ----------------------------------
def save_empirical_rule_figure(
    orders: pd.DataFrame,
    summary: dict[str, object],
) -> Path:
    """Guarda la distribución en forma de campana y su cobertura por intervalos."""
    output_path = DIR_FIGURES / "deteccion_anomalias_01_regla_empirica.png"
    values = orders["processing_time_minutes"]
    mean = float(summary["mean"])
    standard_deviation = float(summary["sample_standard_deviation"])
    coverage = summary["coverage_percent"]

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    axes[0].hist(values, bins=24, color="#A7B0BF", edgecolor="white")
    axes[0].axvline(mean, color="#1A2E51", linewidth=2.4, label="Media")
    for k, color in [(1, "#EC2661"), (2, "#FF8A3D"), (3, "#0039A6")]:
        axes[0].axvline(
            mean - k * standard_deviation,
            color=color,
            linestyle="--",
            linewidth=1.6,
        )
        axes[0].axvline(
            mean + k * standard_deviation,
            color=color,
            linestyle="--",
            linewidth=1.6,
            label=f"+/- {k}s",
        )
    axes[0].set_title("Tiempos sintéticos con forma de campana", fontsize=15)
    axes[0].set_xlabel("Tiempo de procesamiento (minutos)", fontsize=12)
    axes[0].set_ylabel("Pedidos", fontsize=12)
    axes[0].tick_params(labelsize=10)
    axes[0].legend(frameon=False, fontsize=10)

    positions = np.arange(3)
    observed = [coverage[k] for k in (1, 2, 3)]
    bars = axes[1].bar(positions, observed, color="#EC2661", width=0.62)
    axes[1].set_xticks(
        positions,
        ["Dentro de 1s\ncerca de 68%", "Dentro de 2s\ncerca de 95%", "Dentro de 3s\nmás de 99%"],
    )
    axes[1].set_ylim(0, 108)
    axes[1].set_ylabel("Porcentaje observado", fontsize=12)
    axes[1].set_title("Cobertura en esta muestra", fontsize=15)
    axes[1].tick_params(labelsize=10)
    for bar, value in zip(bars, observed):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.8,
            f"{value:.2f}%",
            fontsize=11,
            ha="center",
        )

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("Comprobación de la regla empírica", fontsize=17, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    orders = build_baseline_orders()
    summary = empirical_coverage(orders)
    figure_path = save_empirical_rule_figure(orders, summary)
    coverage = summary["coverage_percent"]

    print("================================================================")
    print("LECCIÓN 04 - PASO 1: LA REGLA EMPÍRICA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño de la muestra (n)         : {len(orders):,}")
    print(f"Media                            : {summary['mean']:.2f} min")
    print("Desviación estándar muestral (s) : "
          f"{summary['sample_standard_deviation']:.2f} min")
    for k in (1, 2, 3):
        print(f"Observado dentro de {k}s           : {coverage[k]:.2f}%")
    print("Condición                        : Datos simétricos con forma de campana")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

