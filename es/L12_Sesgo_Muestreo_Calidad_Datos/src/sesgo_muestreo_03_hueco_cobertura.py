"""
Lección 12 - Paso 3: Hueco de cobertura, datos faltantes y limpieza
===================================================================
NUEVO EN ESTE PASO: coverage_gap_frame(), clean_incomplete_rows() y save_figure().

CAMBIOS RESPECTO A sesgo_muestreo_02_conveniencia_web.py
La Receta
---------
Introduce estos cambios en este orden:
    1. coverage_gap_frame()     elimina la región Oeste del marco de muestreo
    2. clean_incomplete_rows()  eliminación listwise de banderas de queja faltantes
    3. save_figure()            limpiar un marco sesgado no restaura el Oeste

Los tickets del Oeste tienen una tasa de quejas más alta y una tasa de
faltantes más alta. Un marco que nunca incluyó el Oeste, luego "limpiado" de
filas incompletas, sigue conteniendo cero unidades del Oeste. El error no
muestral no es error de muestreo.

Ejecútalo:
    uv run es/L12_Sesgo_Muestreo_Calidad_Datos/src/sesgo_muestreo_03_hueco_cobertura.py
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


def draw_web_convenience(
    register: pd.DataFrame,
    sample_size: int = CONVENIENCE_SIZE,
) -> pd.DataFrame:
    """Toma los primeros tickets En línea disponibles como muestra de conveniencia."""
    web_tickets = register.loc[register["channel"] == "En línea"]
    if len(web_tickets) < sample_size:
        raise ValueError("El registro sintético tiene demasiado pocos tickets En línea.")
    return web_tickets.head(sample_size)


# --- NUEVO (1) coverage_gap_frame() ------------------------------------------
def coverage_gap_frame(register: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el marco operativo que nunca incluyó la región Oeste."""
    return register.loc[register["region"] != "Oeste"].copy()
# ------------------------------------------------------------------------------


# --- NUEVO (2) clean_incomplete_rows() ---------------------------------------
def clean_incomplete_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas cuya bandera de queja falta (eliminación listwise)."""
    return frame.loc[frame["complaint_missing"] == 0].copy()
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    population_rate: float,
    srs_error: float,
    convenience_error: float,
    coverage_error: float,
    cleaned_error: float,
    west_after_cleaning: int,
) -> Path:
    """Contrasta errores y muestra que la limpieza no restaura tickets del Oeste."""
    output_path = DIR_FIGURES / "sesgo_muestreo_03_hueco_cobertura.png"
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))
    labels = ["MAS", "Solo en línea", "Sin Oeste", "Limpio\nsin Oeste"]
    errors = [srs_error, convenience_error, coverage_error, cleaned_error]
    colors = ["#5B8DEF", "#EC2661", "#1A2E51", "#F4A6B8"]

    axes[0].bar(labels, errors, color=colors, width=0.62)
    axes[0].set_ylabel("Error absoluto")
    axes[0].set_title("Error respecto a la tasa poblacional")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(errors):
        axes[0].text(idx, value + 0.002, f"{value:.3f}", ha="center", fontsize=8)

    axes[1].bar(
        ["Oeste en\npoblación", "Oeste tras\nlimpieza"],
        [1200, west_after_cleaning],
        color=["#1A2E51", "#EC2661"],
        width=0.55,
    )
    axes[1].set_ylabel("Tickets del Oeste")
    axes[1].set_title("La limpieza no restaura unidades faltantes")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    axes[1].text(0, 1200 + 30, "1200", ha="center", fontsize=8)
    axes[1].text(1, west_after_cleaning + 30, str(west_after_cleaning), ha="center", fontsize=8)

    fig.suptitle(f"Tasa poblacional de quejas = {population_rate:.4f}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    register = build_register()
    srs = draw_srs(register)
    convenience = draw_web_convenience(register)
    frame = coverage_gap_frame(register)
    cleaned = clean_incomplete_rows(frame)

    population_rate = float(register["complaint"].mean())
    west_rate = float(register.loc[register["region"] == "Oeste", "complaint"].mean())
    other_rate = float(register.loc[register["region"] != "Oeste", "complaint"].mean())
    missing_total = int(register["complaint_missing"].sum())
    missing_west = int(
        register.loc[register["region"] == "Oeste", "complaint_missing"].sum()
    )
    srs_rate = float(srs["complaint"].mean())
    conv_rate = float(convenience["complaint"].mean())
    coverage_rate = float(frame["complaint"].mean())
    cleaned_rate = float(cleaned["complaint"].mean())
    west_after_cleaning = int((cleaned["region"] == "Oeste").sum())

    srs_error = abs(srs_rate - population_rate)
    conv_error = abs(conv_rate - population_rate)
    coverage_error = abs(coverage_rate - population_rate)
    cleaned_error = abs(cleaned_rate - population_rate)
    figure_path = save_figure(
        population_rate,
        srs_error,
        conv_error,
        coverage_error,
        cleaned_error,
        west_after_cleaning,
    )

    print("================================================================")
    print("LECCIÓN 12 - PASO 3: HUECO DE COBERTURA Y LIMPIEZA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tasa poblacional de quejas      : {population_rate:.6f}")
    print(f"Tasa de quejas del Oeste        : {west_rate:.6f}")
    print(f"Tasa de quejas no Oeste         : {other_rate:.6f}")
    print(f"Banderas de queja faltantes     : {missing_total:,}")
    print(f"Banderas faltantes en el Oeste  : {missing_west:,}")
    print(f"Error absoluto MAS              : {srs_error:.6f}")
    print(f"Error absoluto de conveniencia  : {conv_error:.6f}")
    print(f"Tamaño del marco sin Oeste      : {len(frame):,}")
    print(f"Tasa del marco sin Oeste        : {coverage_rate:.6f}")
    print(f"Error absoluto sin Oeste        : {coverage_error:.6f}")
    print(f"Tamaño limpio sin Oeste         : {len(cleaned):,}")
    print(f"Tasa limpia sin Oeste           : {cleaned_rate:.6f}")
    print(f"Error absoluto limpio sin Oeste : {cleaned_error:.6f}")
    print(f"Tickets del Oeste tras limpieza : {west_after_cleaning}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

