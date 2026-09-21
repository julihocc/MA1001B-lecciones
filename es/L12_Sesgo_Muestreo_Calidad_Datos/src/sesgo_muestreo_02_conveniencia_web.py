"""
Lección 12 - Paso 2: Muestra de conveniencia solo de tickets en línea
=====================================================================
NUEVO EN ESTE PASO: draw_web_convenience(), compare_estimates() y save_figure().

CAMBIOS RESPECTO A sesgo_muestreo_01_mas.py
La Receta
---------
Introduce estos cambios en este orden:
    1. draw_web_convenience()   toma una muestra grande solo del canal En línea
    2. compare_estimates()      error MAS versus error de conveniencia
    3. save_figure()            el tamaño de muestra no repara el sesgo de selección

El mismo registro sintético de 8,000 filas se reconstruye con SEED = 42. No se
importa ningún script anterior. Los tickets en línea tienen una tasa de quejas
menor, de modo que una muestra más grande solo en línea puede desviarse más
del parámetro poblacional que la MAS.

Ejecútalo:
    uv run es/L12_Sesgo_Muestreo_Calidad_Datos/src/sesgo_muestreo_02_conveniencia_web.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_ROWS = 8_000
SRS_SIZE = 400
CONVENIENCE_SIZE = 1_200
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)
REGION_LABELS = {
    "North": "Norte",
    "South": "Sur",
    "East": "Este",
    "West": "Oeste",
}
CHANNEL_LABELS = {"Web": "En línea", "Store": "Tienda"}


def build_register(seed: int = SEED) -> pd.DataFrame:
    """Construye el registro sintético de 8,000 tickets usado en cada paso."""
    rng = np.random.default_rng(seed)
    regions = np.repeat(
        np.array(["North", "South", "East", "West"]),
        np.array([2400, 2400, 2000, 1200]),
    )
    rng.shuffle(regions)
    p_web = {"North": 0.45, "South": 0.40, "East": 0.75, "West": 0.20}
    p_web_arr = np.array([p_web[region] for region in regions])
    channel = np.where(rng.random(N_ROWS) < p_web_arr, "Web", "Store")
    p_complaint = np.where(channel == "Web", 0.05, 0.14)
    p_complaint = p_complaint + np.where(regions == "West", 0.16, 0.00)
    complaint = (rng.random(N_ROWS) < p_complaint).astype(int)
    p_missing = np.where(regions == "West", 0.22, 0.05)
    complaint_missing = (rng.random(N_ROWS) < p_missing).astype(int)
    recorded = complaint.astype(float)
    recorded[complaint_missing == 1] = np.nan
    return pd.DataFrame(
        {
            "ticket_id": np.arange(100_001, 100_001 + N_ROWS),
            "region": pd.Series(regions).map(REGION_LABELS).to_numpy(),
            "channel": pd.Series(channel).map(CHANNEL_LABELS).to_numpy(),
            "complaint": complaint,
            "complaint_missing": complaint_missing,
            "complaint_recorded": recorded,
        }
    )


def draw_srs(
    register: pd.DataFrame,
    sample_size: int = SRS_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae una muestra aleatoria simple sin reemplazo del registro completo."""
    return register.sample(n=sample_size, replace=False, random_state=seed)


# --- NUEVO (1) draw_web_convenience() ----------------------------------------
def draw_web_convenience(
    register: pd.DataFrame,
    sample_size: int = CONVENIENCE_SIZE,
) -> pd.DataFrame:
    """Toma los primeros tickets En línea disponibles como muestra de conveniencia."""
    web_tickets = register.loc[register["channel"] == "En línea"]
    if len(web_tickets) < sample_size:
        raise ValueError("El registro sintético tiene demasiado pocos tickets En línea.")
    return web_tickets.head(sample_size)
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_estimates() -------------------------------------------
def compare_estimates(
    register: pd.DataFrame,
    srs: pd.DataFrame,
    convenience: pd.DataFrame,
) -> pd.DataFrame:
    """Compara cada tasa muestral de quejas con el parámetro poblacional."""
    population_rate = float(register["complaint"].mean())
    rows = []
    for label, sample in [("MAS", srs), ("Conveniencia en línea", convenience)]:
        sample_rate = float(sample["complaint"].mean())
        rows.append(
            {
                "sample": label,
                "size": len(sample),
                "rate": sample_rate,
                "absolute_error": abs(sample_rate - population_rate),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(comparison: pd.DataFrame) -> Path:
    """Guarda tamaños de muestra junto a errores absolutos de MAS y conveniencia."""
    output_path = DIR_FIGURES / "sesgo_muestreo_02_conveniencia_web.png"
    colors = ["#5B8DEF", "#EC2661"]
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))

    axes[0].bar(comparison["sample"], comparison["size"], color=colors, width=0.55)
    axes[0].set_title("Tamaño de muestra")
    axes[0].set_ylabel("Tickets")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    axes[1].bar(
        comparison["sample"],
        comparison["absolute_error"],
        color=colors,
        width=0.55,
    )
    axes[1].set_title("Error absoluto respecto a la tasa poblacional")
    axes[1].set_ylabel("Error absoluto")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.suptitle("Una muestra más grande solo en línea puede producir más error")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    register = build_register()
    srs = draw_srs(register)
    convenience = draw_web_convenience(register)
    comparison = compare_estimates(register, srs, convenience)
    population_rate = float(register["complaint"].mean())
    web_rate = float(register.loc[register["channel"] == "En línea", "complaint"].mean())
    store_rate = float(
        register.loc[register["channel"] == "Tienda", "complaint"].mean()
    )
    srs_row = comparison.loc[comparison["sample"] == "MAS"].iloc[0]
    conv_row = comparison.loc[comparison["sample"] == "Conveniencia en línea"].iloc[0]
    figure_path = save_figure(comparison)

    print("================================================================")
    print("LECCIÓN 12 - PASO 2: MUESTRA DE CONVENIENCIA EN LÍNEA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tasa poblacional de quejas      : {population_rate:.6f}")
    print(f"Tasa de quejas del canal En línea: {web_rate:.6f}")
    print(f"Tasa de quejas del canal Tienda : {store_rate:.6f}")
    print(f"Tamaño MAS n                    : {int(srs_row['size']):,}")
    print(f"Tasa de quejas MAS              : {srs_row['rate']:.6f}")
    print(f"Error absoluto MAS              : {srs_row['absolute_error']:.6f}")
    print(f"Tamaño de conveniencia n        : {int(conv_row['size']):,}")
    print(f"Tasa de quejas de conveniencia  : {conv_row['rate']:.6f}")
    print(f"Error absoluto de conveniencia  : {conv_row['absolute_error']:.6f}")
    print(
        "La muestra más grande tiene más error: "
        f"{conv_row['absolute_error'] > srs_row['absolute_error']}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

