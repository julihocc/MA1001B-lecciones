"""
Lección 33 - Paso 2: Tasa simulada de error de tipo I
=====================================================
NUEVO EN ESTE PASO: simulate_type_i(), type_i_rate() y save_figure().

La Receta
Partir de fundamentos_ph_01_hipotesis_alfa.py e introducir:
    1. simulate_type_i()    10000 muestras generadas bajo H0: mu = 50
    2. type_i_rate()        proporción de muestras que rechazan H0
    3. save_figure()        histograma de xbarra bajo H0 con el corte

Un error de tipo I es rechazar una H0 verdadera. Con alfa = 0.05 la tasa
simulada debería caer cerca de 0.05 cuando H0 es verdadera.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 36
MU0 = 50.0
SIGMA = 8.0
ALPHA = 0.05
N_REPS = 10_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def rejection_cutoff() -> dict[str, float]:
    """Devuelve EE, valor crítico z y corte de xbarra bajo H0."""
    se = SIGMA / np.sqrt(N)
    z_crit = float(stats.norm.ppf(1.0 - ALPHA))
    return {
        "se": float(se),
        "z_crit": z_crit,
        "xbar_crit": float(MU0 + z_crit * se),
    }


# --- NUEVO (1) simulate_type_i() ---------------------------------------------
def simulate_type_i(n_reps: int = N_REPS) -> np.ndarray:
    """Extrae medias muestrales bajo H0: mu = 50 con semilla 42."""
    rng = np.random.default_rng(SEED)
    samples = rng.normal(MU0, SIGMA, size=(n_reps, N))
    return np.mean(samples, axis=1)
# ------------------------------------------------------------------------------


# --- NUEVO (2) type_i_rate() -------------------------------------------------
def type_i_rate(xbars: np.ndarray, xbar_crit: float) -> dict[str, float]:
    """Proporción de muestras H0 cuya media cae en la región de rechazo."""
    rejections = xbars >= xbar_crit
    return {
        "n_reps": float(xbars.size),
        "n_rejections": float(np.sum(rejections)),
        "type_i_rate": float(np.mean(rejections)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(xbars: np.ndarray, xbar_crit: float) -> Path:
    """Histograma de xbarra simulada bajo H0, con el corte de alfa."""
    output_path = DIR_FIGURES / "fundamentos_ph_02_tasa_tipo_i.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(xbars, bins=30, color="#A7B0BF", edgecolor="white", density=True)
    ax.axvline(xbar_crit, color="#EC2661", linewidth=2.2,
               label=f"Corte = {xbar_crit:.2f}")
    ax.set_xlabel("Media muestral xbarra bajo H0")
    ax.set_ylabel("Densidad")
    ax.set_title("Errores de tipo I: rechazar una H0 verdadera")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    cutoff = rejection_cutoff()
    xbars = simulate_type_i()
    rates = type_i_rate(xbars, cutoff["xbar_crit"])
    figure_path = save_figure(xbars, cutoff["xbar_crit"])

    print("================================================================")
    print("LECCIÓN 33 - PASO 2: TASA DE ERROR DE TIPO I")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS}")
    print("Mu verdadera (H0 es verdadera)  : 50.000000")
    print(f"Corte de xbarra                 : {cutoff['xbar_crit']:.6f}")
    print(f"Rechazos                        : {int(rates['n_rejections'])}")
    print(f"Tasa simulada de tipo I         : {rates['type_i_rate']:.6f}")
    print(f"Alfa nominal                    : {ALPHA:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

