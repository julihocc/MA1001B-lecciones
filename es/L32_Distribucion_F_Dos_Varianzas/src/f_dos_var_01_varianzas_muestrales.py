"""
Lección 32 - Paso 1: Varianzas muestrales de dos grupos independientes
=====================================================================
NUEVO EN ESTE PASO: generate_two_stations(), sample_variances() y
save_figure().

La Receta
Dos estaciones de empaque completamente sintéticas se muestrean de forma
independiente. La estación A tiene n1 = 25 ciclos y la estación B tiene
n2 = 25 ciclos. Cada varianza muestral estima la varianza poblacional de
esa estación.

Ejecútalo:
    uv run es/L32_Distribucion_F_Dos_Varianzas/src/f_dos_var_01_varianzas_muestrales.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N1 = 25
N2 = 25
MU = 40.0
SIGMA1 = 8.0
SIGMA2 = 5.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) generate_two_stations() ---------------------------------------
def generate_two_stations(seed: int = SEED) -> tuple[np.ndarray, np.ndarray]:
    """Extrae muestras normales independientes de dos estaciones de empaque."""
    rng = np.random.default_rng(seed)
    station_a = rng.normal(loc=MU, scale=SIGMA1, size=N1)
    station_b = rng.normal(loc=MU, scale=SIGMA2, size=N2)
    return station_a, station_b
# ------------------------------------------------------------------------------


# --- NUEVO (2) sample_variances() --------------------------------------------
def sample_variances(
    station_a: np.ndarray,
    station_b: np.ndarray,
) -> dict[str, float]:
    """Devuelve s1^2, s2^2 y los dos grados de libertad."""
    s1_sq = float(np.var(station_a, ddof=1))
    s2_sq = float(np.var(station_b, ddof=1))
    return {
        "n1": float(N1),
        "n2": float(N2),
        "df1": float(N1 - 1),
        "df2": float(N2 - 1),
        "s1_sq": s1_sq,
        "s2_sq": s2_sq,
        "hidden_sigma1_sq": SIGMA1 ** 2,
        "hidden_sigma2_sq": SIGMA2 ** 2,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    station_a: np.ndarray,
    station_b: np.ndarray,
    metrics: dict[str, float],
) -> Path:
    """Guarda diagramas de caja lado a lado de las dos muestras de estación."""
    output_path = DIR_FIGURES / "f_dos_var_01_varianzas_muestrales.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    box = ax.boxplot(
        [station_a, station_b],
        tick_labels=["Estación A", "Estación B"],
        patch_artist=True,
        widths=0.45,
    )
    box["boxes"][0].set_facecolor("#EC2661")
    box["boxes"][1].set_facecolor("#5B8DEF")
    for median in box["medians"]:
        median.set_color("#1A2E51")
        median.set_linewidth(2)
    ax.set_ylabel("Tiempo de ciclo (minutos)")
    ax.set_title(
        f"sA^2 = {metrics['s1_sq']:.2f}   |   sB^2 = {metrics['s2_sq']:.2f}"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    station_a, station_b = generate_two_stations()
    metrics = sample_variances(station_a, station_b)
    figure_path = save_figure(station_a, station_b, metrics)

    print("================================================================")
    print("LECCIÓN 32 - PASO 1: DOS VARIANZAS MUESTRALES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Estación A n1                   : {N1}")
    print(f"Estación B n2                   : {N2}")
    print(f"gl1 = n1-1                      : {int(metrics['df1'])}")
    print(f"gl2 = n2-1                      : {int(metrics['df2'])}")
    print(f"Estación A s1^2                 : {metrics['s1_sq']:.6f}")
    print(f"Estación B s2^2                 : {metrics['s2_sq']:.6f}")
    print(f"Sigma1^2 oculta                 : {metrics['hidden_sigma1_sq']:.6f}")
    print(f"Sigma2^2 oculta                 : {metrics['hidden_sigma2_sq']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

