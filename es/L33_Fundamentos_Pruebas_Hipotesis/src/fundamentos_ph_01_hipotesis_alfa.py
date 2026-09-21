"""
Lección 33 - Paso 1: Hipótesis, alfa y la región de rechazo
===========================================================
NUEVO EN ESTE PASO: state_hypotheses(), rejection_cutoff() y
save_figure().

La Receta
Un objetivo de empaque completamente sintético es mu = 50 minutos. La prueba
es H0: mu = 50 frente a H1: mu > 50, con alfa = 0.05. En esta lección de
fundamentos, sigma = 8 se trata como conocida y n = 36, de modo que el
corte es un valor crítico z.

Ejecútalo:
    uv run es/L33_Fundamentos_Pruebas_Hipotesis/src/fundamentos_ph_01_hipotesis_alfa.py
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) state_hypotheses() --------------------------------------------
def state_hypotheses() -> dict[str, float]:
    """Devuelve las hipótesis unilaterales de media y el EE con sigma conocida."""
    se = SIGMA / np.sqrt(N)
    return {
        "mu0": MU0,
        "n": float(N),
        "sigma": SIGMA,
        "alpha": ALPHA,
        "se": float(se),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) rejection_cutoff() --------------------------------------------
def rejection_cutoff(se: float) -> dict[str, float]:
    """Convierte alfa en un valor crítico z y un corte de xbarra."""
    z_crit = float(stats.norm.ppf(1.0 - ALPHA))
    xbar_crit = MU0 + z_crit * se
    return {
        "z_crit": z_crit,
        "xbar_crit": float(xbar_crit),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(se: float, cutoff: dict[str, float]) -> Path:
    """Sombrea la región de rechazo alfa = 0.05 en la distribución muestral."""
    output_path = DIR_FIGURES / "fundamentos_ph_01_hipotesis_alfa.png"
    x = np.linspace(MU0 - 4 * se, MU0 + 4 * se, 400)
    y = stats.norm.pdf(x, loc=MU0, scale=se)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    ax.fill_between(
        x[x >= cutoff["xbar_crit"]],
        y[x >= cutoff["xbar_crit"]],
        color="#EC2661",
        alpha=0.55,
        label=f"región de rechazo alfa = {ALPHA:.2f}",
    )
    ax.axvline(cutoff["xbar_crit"], color="#EC2661", linewidth=2.0)
    ax.set_xlabel("Media muestral xbarra (minutos)")
    ax.set_ylabel("Densidad bajo H0")
    ax.set_title("H0: mu = 50 frente a H1: mu > 50, alfa = 0.05")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    setup = state_hypotheses()
    cutoff = rejection_cutoff(setup["se"])
    figure_path = save_figure(setup["se"], cutoff)

    print("================================================================")
    print("LECCIÓN 33 - PASO 1: HIPÓTESIS Y ALFA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print("H0                             : mu = 50")
    print("H1                             : mu > 50")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Sigma conocida                  : {SIGMA:.6f}")
    print(f"EE = sigma/sqrt(n)              : {setup['se']:.6f}")
    print(f"Nivel de significancia alfa     : {ALPHA:.6f}")
    print(f"z crítico                       : {cutoff['z_crit']:.6f}")
    print(f"Corte de xbarra                 : {cutoff['xbar_crit']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

