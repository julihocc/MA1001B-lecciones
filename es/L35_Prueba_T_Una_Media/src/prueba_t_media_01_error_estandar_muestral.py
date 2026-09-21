"""
Lección 35 - Paso 1: Media muestral, s muestral y el estadístico t
==================================================================
NUEVO EN ESTE PASO: build_pack_times(), t_statistic() y save_figure().

La Receta
Una línea de empaque de salida completamente sintética afirma que el tiempo
medio de ciclo es 50 minutos. Operaciones extrae n = 40 empaques completados.
A diferencia de una prueba z, la desviación estándar poblacional es
desconocida, así que el error estándar usa la s muestral y la distribución
de referencia es t de Student con gl = n - 1.

Ejecútalo:
    uv run es/L35_Prueba_T_Una_Media/src/prueba_t_media_01_error_estandar_muestral.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 40
MU0 = 50.0
PROCESS_MEAN = 52.0
PROCESS_SD = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_pack_times() --------------------------------------------
def build_pack_times(seed: int = SEED) -> np.ndarray:
    """Extrae n = 40 tiempos de ciclo de empaque sintéticos en minutos."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=PROCESS_MEAN, scale=PROCESS_SD, size=N)
# ------------------------------------------------------------------------------


# --- NUEVO (2) t_statistic() -------------------------------------------------
def t_statistic(times: np.ndarray, mu0: float = MU0) -> dict[str, float]:
    """Calcula x-barra, s, EE, grados de libertad y la t de una muestra."""
    n = times.size
    xbar = float(np.mean(times))
    sample_sd = float(np.std(times, ddof=1))
    se = sample_sd / np.sqrt(n)
    t_stat = (xbar - mu0) / se
    return {
        "n": float(n),
        "xbar": xbar,
        "sample_sd": sample_sd,
        "se": float(se),
        "df": float(n - 1),
        "t_stat": float(t_stat),
        "mu0": mu0,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(times: np.ndarray, summary: dict[str, float]) -> Path:
    """Guarda un histograma de tiempos de empaque con las medias hipotética y muestral."""
    output_path = DIR_FIGURES / "prueba_t_media_01_error_estandar_muestral.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(times, bins=10, color="#5B8DEF", edgecolor="#1A2E51", alpha=0.85)
    ax.axvline(summary["mu0"], color="#646464", linestyle="--", linewidth=1.8,
               label=f"media H0 = {summary['mu0']:.0f}")
    ax.axvline(summary["xbar"], color="#EC2661", linestyle="-", linewidth=1.8,
               label=f"media muestral = {summary['xbar']:.2f}")
    ax.set_xlabel("Tiempo de ciclo de empaque (minutos)")
    ax.set_ylabel("Frecuencia")
    ax.set_title("n = 40 tiempos de empaque sintéticos; sigma desconocida")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    times = build_pack_times()
    summary = t_statistic(times)
    figure_path = save_figure(times, summary)

    print("================================================================")
    print("LECCIÓN 35 - PASO 1: ERROR ESTÁNDAR MUESTRAL Y ESTADÍSTICO T")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {int(summary['n'])}")
    print(f"Media hipotética mu0            : {summary['mu0']:.6f}")
    print(f"Media muestral x-barra          : {summary['xbar']:.6f}")
    print(f"Desviación estándar muestral s  : {summary['sample_sd']:.6f}")
    print(f"Error estándar s/sqrt(n)        : {summary['se']:.6f}")
    print(f"Grados de libertad n-1          : {int(summary['df'])}")
    print(f"Estadístico t (x-barra - mu0)/EE: {summary['t_stat']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

