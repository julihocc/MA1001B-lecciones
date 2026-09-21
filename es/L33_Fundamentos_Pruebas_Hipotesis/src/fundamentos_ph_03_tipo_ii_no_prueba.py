"""
Lección 33 - Paso 3: No rechazar H0 no prueba que H0 sea verdadera
=================================================================
NUEVO EN ESTE PASO: simulate_power(), one_nonrejection() y save_figure().

La Receta
Partir de fundamentos_ph_02_tasa_tipo_i.py e introducir:
    1. simulate_power()         10000 muestras en mu = 53 (H1 es verdadera)
    2. one_nonrejection()       una muestra con semilla 42 en mu = 51 que no rechaza
    3. save_figure()            potencia en mu = 53 frente a un no rechazo

Límite: la potencia en mu = 53 es menor que 1, y una alternativa cercana
mu = 51 puede no rechazar con facilidad. No rechazar H0 no prueba que mu = 50.
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
MU_ALT = 53.0
MU_NEAR = 51.0
SIGMA = 8.0
ALPHA = 0.05
N_REPS = 10_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def rejection_cutoff() -> dict[str, float]:
    """Devuelve EE y el corte de xbarra bajo H0."""
    se = SIGMA / np.sqrt(N)
    z_crit = float(stats.norm.ppf(1.0 - ALPHA))
    return {
        "se": float(se),
        "xbar_crit": float(MU0 + z_crit * se),
    }


# --- NUEVO (1) simulate_power() ----------------------------------------------
def simulate_power(xbar_crit: float, n_reps: int = N_REPS) -> dict[str, float]:
    """Potencia en mu = 53: proporción de muestras que rechazan H0 cuando H1 es verdadera."""
    rng = np.random.default_rng(SEED)
    samples = rng.normal(MU_ALT, SIGMA, size=(n_reps, N))
    xbars = np.mean(samples, axis=1)
    power = float(np.mean(xbars >= xbar_crit))
    type_ii = 1.0 - power
    return {
        "mu_alt": MU_ALT,
        "power": power,
        "type_ii": type_ii,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) one_nonrejection() --------------------------------------------
def one_nonrejection(xbar_crit: float) -> dict[str, float]:
    """Una muestra de alternativa cercana que no rechaza H0."""
    rng = np.random.default_rng(SEED)
    sample = rng.normal(MU_NEAR, SIGMA, size=N)
    xbar = float(np.mean(sample))
    return {
        "mu_near": MU_NEAR,
        "xbar": xbar,
        "xbar_crit": xbar_crit,
        "rejected": float(xbar >= xbar_crit),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    power: dict[str, float],
    nearby: dict[str, float],
) -> Path:
    """Gráfico de barras de potencia en mu = 53 y una bandera de no rechazo cercano."""
    output_path = DIR_FIGURES / "fundamentos_ph_03_tipo_ii_no_prueba.png"
    labels = ["Potencia en mu = 53", "Tipo II en mu = 53"]
    values = [power["power"], power["type_ii"]]
    colors = ["#1A2E51", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Tasa")
    ax.set_title("No rechazar H0 no prueba que H0 sea verdadera")
    ax.set_ylim(0, 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )
    ax.text(
        0.5,
        1.05,
        f"Muestra cercana mu=51: xbarra={nearby['xbar']:.2f} "
        f"(corte {nearby['xbar_crit']:.2f}); "
        f"rechazar={'sí' if nearby['rejected'] else 'no'}",
        ha="center",
        fontsize=8,
        color="#1A2E51",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    cutoff = rejection_cutoff()
    power = simulate_power(cutoff["xbar_crit"])
    nearby = one_nonrejection(cutoff["xbar_crit"])
    figure_path = save_figure(power, nearby)

    print("================================================================")
    print("LECCIÓN 33 - PASO 3: TIPO II Y NO ES PRUEBA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS}")
    print(f"Corte de xbarra                 : {cutoff['xbar_crit']:.6f}")
    print(f"Mu alternativa                  : {power['mu_alt']:.6f}")
    print(f"Potencia en mu=53               : {power['power']:.6f}")
    print(f"Tasa de tipo II en mu=53        : {power['type_ii']:.6f}")
    print(f"Mu alternativa cercana          : {nearby['mu_near']:.6f}")
    print(f"Xbarra de la muestra cercana    : {nearby['xbar']:.6f}")
    print(f"La muestra cercana rechaza H0   : {'sí' if nearby['rejected'] else 'no'}")
    print("Límite                         : no rechazar H0 no es una prueba")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

