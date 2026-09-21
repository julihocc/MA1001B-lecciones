"""
Lección 12 - Paso 1: Muestra aleatoria simple de un registro completo
=====================================================================
NUEVO EN ESTE PASO: build_register(), draw_srs() y save_figure().

Contexto:
Un registro sintético de 8,000 filas de tickets de servicio registra región,
canal y una bandera de queja. El parámetro poblacional es la tasa de quejas.
Una muestra aleatoria simple de 400 tickets estima esa tasa solo con error de
muestreo.

Ejecútalo:
    uv run es/L12_Sesgo_Muestreo_Calidad_Datos/src/sesgo_muestreo_01_mas.py
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)
REGION_LABELS = {
    "North": "Norte",
    "South": "Sur",
    "East": "Este",
    "West": "Oeste",
}
CHANNEL_LABELS = {"Web": "En línea", "Store": "Tienda"}


# --- NUEVO (1) build_register() ----------------------------------------------
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
# ------------------------------------------------------------------------------


# --- NUEVO (2) draw_srs() ----------------------------------------------------
def draw_srs(
    register: pd.DataFrame,
    sample_size: int = SRS_SIZE,
    seed: int = SEED,
) -> pd.DataFrame:
    """Extrae una muestra aleatoria simple sin reemplazo del registro completo."""
    return register.sample(n=sample_size, replace=False, random_state=seed)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(population_rate: float, srs_rate: float) -> Path:
    """Guarda la tasa poblacional de quejas junto a la estimación MAS."""
    output_path = DIR_FIGURES / "sesgo_muestreo_01_mas.png"
    labels = ["Parámetro\npoblacional", "MAS n=400\nestimación"]
    values = [population_rate, srs_rate]
    colors = ["#1A2E51", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Tasa de quejas")
    ax.set_title("La muestra aleatoria simple sigue la tasa poblacional")
    ax.set_ylim(0, 0.25)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    register = build_register()
    srs = draw_srs(register)
    population_rate = float(register["complaint"].mean())
    srs_rate = float(srs["complaint"].mean())
    abs_error = abs(srs_rate - population_rate)
    region_counts = register["region"].value_counts().to_dict()
    figure_path = save_figure(population_rate, srs_rate)

    print("================================================================")
    print("LECCIÓN 12 - PASO 1: MUESTRA ALEATORIA SIMPLE")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Filas del registro N            : {len(register):,}")
    print(f"Tickets Norte                   : {region_counts['Norte']:,}")
    print(f"Tickets Sur                     : {region_counts['Sur']:,}")
    print(f"Tickets Este                    : {region_counts['Este']:,}")
    print(f"Tickets Oeste                   : {region_counts['Oeste']:,}")
    print(f"Tasa poblacional de quejas      : {population_rate:.6f}")
    print(f"Tamaño MAS n                    : {len(srs):,}")
    print(f"Tasa de quejas MAS              : {srs_rate:.6f}")
    print(f"Error absoluto MAS              : {abs_error:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

