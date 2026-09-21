"""
Lección 04 - Paso 3: Banderas de boxplot e investigación
=======================================================
NUEVO EN ESTE PASO: inject_extreme_cases(), flag_with_iqr_rule() y
save_boxplot_figure().

La Receta
CAMBIOS RESPECTO A deteccion_anomalias_02_chebyshev.py
Introdúcelos en este orden:
    1. inject_extreme_cases()  inserta cuatro retrasos sintéticos extremos conocidos
    2. flag_with_iqr_rule()    calcula cercas 1.5-IQR y valores atípicos potenciales
    3. save_boxplot_figure()   distingue banderas de la regla de inyecciones conocidas

Ejecútalo:
    uv run es/L04_Deteccion_Anomalias_Boxplots/src/deteccion_anomalias_03_banderas_boxplot.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SAMPLE_SIZE = 600
DELAY_PROBABILITY = 0.10
INJECTED_ROW_INDICES = np.array([41, 187, 333, 512])
INJECTED_DELAYS = np.array([95.0, 110.0, 130.0, 160.0])
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


def add_queue_delays(seed: int = SEED) -> tuple[pd.DataFrame, int]:
    """Crea la muestra de tiempos de procesamiento con cola derecha del Paso 2."""
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


def chebyshev_coverage(orders: pd.DataFrame) -> dict[str, object]:
    """Devuelve la comparación de Chebyshov introducida en el Paso 2."""
    values = orders["processing_time_minutes"]
    mean = float(values.mean())
    standard_deviation = float(values.std(ddof=1))
    coverage = {
        k: float((values.sub(mean).abs() <= k * standard_deviation).mean() * 100)
        for k in (2, 3)
    }
    return {
        "mean": mean,
        "sample_standard_deviation": standard_deviation,
        "coverage_percent": coverage,
    }


# --- NUEVO (1) inject_extreme_cases() ----------------------------------------
def inject_extreme_cases(orders: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza cuatro tiempos de procesamiento por retrasos extremos sintéticos."""
    modified = orders.copy()
    modified["known_injected_extreme"] = False
    modified.loc[INJECTED_ROW_INDICES, "processing_time_minutes"] = INJECTED_DELAYS
    modified.loc[INJECTED_ROW_INDICES, "known_injected_extreme"] = True
    return modified
# ------------------------------------------------------------------------------


# --- NUEVO (2) flag_with_iqr_rule() ------------------------------------------
def flag_with_iqr_rule(orders: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """Marca valores fuera de Q1 - 1.5 IQR y Q3 + 1.5 IQR."""
    result = orders.copy()
    values = result["processing_time_minutes"]
    first_quartile = float(values.quantile(0.25))
    third_quartile = float(values.quantile(0.75))
    interquartile_range = third_quartile - first_quartile
    lower_fence = first_quartile - 1.5 * interquartile_range
    upper_fence = third_quartile + 1.5 * interquartile_range
    result["flagged_by_iqr_rule"] = values.lt(lower_fence) | values.gt(upper_fence)
    return result, {
        "first_quartile": first_quartile,
        "third_quartile": third_quartile,
        "interquartile_range": interquartile_range,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_boxplot_figure() -----------------------------------------
def save_boxplot_figure(
    orders: pd.DataFrame,
    fences: dict[str, float],
) -> Path:
    """Guarda un boxplot y separa inyecciones conocidas de otras banderas."""
    output_path = DIR_FIGURES / "deteccion_anomalias_03_banderas_boxplot.png"
    flagged = orders[orders["flagged_by_iqr_rule"]]
    known_flagged = int(flagged["known_injected_extreme"].sum())
    other_flagged = len(flagged) - known_flagged

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    sns.boxplot(
        data=orders,
        x="processing_time_minutes",
        color="#A7B0BF",
        width=0.35,
        ax=axes[0],
    )
    axes[0].scatter(
        flagged["processing_time_minutes"],
        np.zeros(len(flagged)),
        color="#EC2661",
        edgecolor="white",
        linewidth=0.6,
        s=44,
        label="Bandera de la regla IQR",
        zorder=3,
    )
    axes[0].axvline(
        fences["upper_fence"],
        color="#0039A6",
        linestyle="--",
        linewidth=2,
        label=f"Cerca superior = {fences['upper_fence']:.2f}",
    )
    axes[0].set_xlabel("Tiempo de procesamiento (minutos)", fontsize=12)
    axes[0].set_title("Boxplot y valores atípicos potenciales", fontsize=15)
    axes[0].tick_params(labelsize=10)
    axes[0].legend(frameon=False, fontsize=10, loc="upper right")

    categories = ["Extremos inyectados\nconocidos", "Otras\nbanderas"]
    bars = axes[1].bar(
        categories,
        [known_flagged, other_flagged],
        color=["#1A2E51", "#EC2661"],
        width=0.58,
    )
    axes[1].set_ylabel("Pedidos marcados", fontsize=12)
    axes[1].set_title("Una bandera no identifica su causa", fontsize=15)
    axes[1].tick_params(labelsize=10)
    axes[1].set_ylim(0, max(known_flagged, other_flagged) + 5)
    for bar in bars:
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.6,
            f"{int(bar.get_height())}",
            fontsize=12,
            ha="center",
        )

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.25)
    fig.suptitle("La regla 1.5-IQR produce candidatos a investigación",
                 fontsize=17, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    delayed_orders, delayed_count = add_queue_delays()
    modified_orders = inject_extreme_cases(delayed_orders)
    flagged_orders, fences = flag_with_iqr_rule(modified_orders)
    figure_path = save_boxplot_figure(flagged_orders, fences)

    flagged = flagged_orders[flagged_orders["flagged_by_iqr_rule"]]
    injected_count = int(flagged_orders["known_injected_extreme"].sum())
    injected_flagged = int(flagged["known_injected_extreme"].sum())
    other_flagged = len(flagged) - injected_flagged

    print("================================================================")
    print("LECCIÓN 04 - PASO 3: BANDERAS DE BOXPLOT")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Tamaño de la muestra (n)         : {len(flagged_orders):,}")
    print(f"Pedidos con retraso de cola      : {delayed_count}")
    print(f"Extremos inyectados conocidos    : {injected_count}")
    print(f"Primer cuartil (Q1)              : {fences['first_quartile']:.2f} min")
    print(f"Tercer cuartil (Q3)              : {fences['third_quartile']:.2f} min")
    print(f"Rango intercuartílico (IQR)      : {fences['interquartile_range']:.2f} min")
    print(f"Cerca inferior                   : {fences['lower_fence']:.2f} min")
    print(f"Cerca superior                   : {fences['upper_fence']:.2f} min")
    print(f"Pedidos marcados por la regla IQR: {len(flagged)}")
    print(f"Extremos inyectados marcados     : {injected_flagged} de {injected_count}")
    print(f"Otros pedidos marcados           : {other_flagged}")
    print("Interpretación                   : Cada bandera requiere investigación")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

