"""
Lección 21 - Paso 3: El sesgo rompe una comparación de puntuación z
===================================================================
NUEVO EN ESTE PASO: delay_model(), percentile_mismatch() y save_figure().

La Receta
CAMBIOS RESPECTO A normal_estandar_02_probabilidades_estandar.py
Introdúcelos en este orden:
    1. delay_model()            retrasos exponenciales con media 20 (así de = 20)
    2. percentile_mismatch()    z = -1 es 16% en una campana y 0% en un reloj de retraso
    3. save_figure()            superpone densidades de campana y retraso estandarizadas

Una comparación de puntuación z requiere forma similar. Los tiempos de retraso
sesgados a la derecha no pueden bajar de 0, de modo que z = -1 queda fuera del
soporte. El sesgo rompe la lectura percentil.

Ejecútalo:
    uv run es/L21_Normal_Estandar_Z/src/normal_estandar_03_sesgo_rompe_z.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU_BELL = 50.0
SIGMA_BELL = 8.0
MU_DELAY = 20.0
SIGMA_DELAY = 20.0
Z_LEFT = -1.0
Z_RIGHT = 1.25
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) delay_model() -------------------------------------------------
def delay_model():
    """Devuelve un reloj de retraso exponencial con media 20 minutos."""
    return stats.expon(scale=MU_DELAY)
# ------------------------------------------------------------------------------


# --- NUEVO (2) percentile_mismatch() -----------------------------------------
def percentile_mismatch(delay) -> dict[str, float]:
    """Compara percentiles de campana y retraso en los mismos valores z."""
    bell = stats.norm()
    x_left_bell = MU_BELL + Z_LEFT * SIGMA_BELL
    x_left_delay = MU_DELAY + Z_LEFT * SIGMA_DELAY
    x_right_delay = MU_DELAY + Z_RIGHT * SIGMA_DELAY
    return {
        "delay_mean": float(delay.mean()),
        "delay_sd": float(delay.std()),
        "x_left_bell": x_left_bell,
        "x_left_delay": x_left_delay,
        "bell_p_left": float(bell.cdf(Z_LEFT)),
        "delay_p_left": float(delay.cdf(x_left_delay)),
        "bell_p_right": float(bell.cdf(Z_RIGHT)),
        "delay_p_right": float(delay.cdf(x_right_delay)),
        "delay_support_min_z": (0.0 - MU_DELAY) / SIGMA_DELAY,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(delay, comparison: dict[str, float]) -> Path:
    """Grafica densidades de campana y retraso estandarizadas en el eje z."""
    output_path = DIR_FIGURES / "normal_estandar_03_sesgo_rompe_z.png"
    z = np.linspace(-3.5, 4.5, 500)
    bell_y = stats.norm.pdf(z)
    x_delay = MU_DELAY + z * SIGMA_DELAY
    delay_y = delay.pdf(x_delay) * SIGMA_DELAY
    delay_y = np.where(x_delay >= 0, delay_y, 0.0)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(z, bell_y, color="#1A2E51", lw=2.2, label="Normal estándar")
    ax.plot(z, delay_y, color="#EC2661", lw=2.2, label="Exponencial estandarizada")
    ax.axvline(Z_LEFT, color="#646464", ls="--", lw=1.3, label="z = -1")
    ax.set_xlabel("z = (x - mu) / sigma")
    ax.set_ylabel("Densidad")
    ax.set_title("z = -1 es 16% en una campana y 0% en un reloj de retraso")
    ax.set_xlim(-3.5, 4.5)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    delay = delay_model()
    comparison = percentile_mismatch(delay)
    figure_path = save_figure(delay, comparison)

    print("================================================================")
    print("LECCIÓN 21 - PASO 3: EL SESGO ROMPE Z")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Media retraso = desv. est. retraso: {comparison['delay_mean']:.6f}")
    print(f"Soporte de retraso empieza en z  : {comparison['delay_support_min_z']:.6f}")
    print(f"x de campana en z = -1           : {comparison['x_left_bell']:.6f}")
    print(f"x de retraso en z = -1           : {comparison['x_left_delay']:.6f}")
    print(f"Normal P(Z <= -1)                : {comparison['bell_p_left']:.6f}")
    print(f"Retraso P(X <= 0)                : {comparison['delay_p_left']:.6f}")
    print(f"Normal P(Z <= 1.25)              : {comparison['bell_p_right']:.6f}")
    print(f"Retraso P(Z <= 1.25)             : {comparison['delay_p_right']:.6f}")
    print("Límite: la comparación de puntuación z requiere forma similar")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

