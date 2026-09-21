"""
Lección 24 - Paso 1: Una población operativa sesgada a la derecha
=================================================================
NUEVO EN ESTE PASO: delay_population(), population_summaries() y
save_figure().

La Receta
Un reloj de retraso completamente sintético es Exponencial con media 10
minutos. La población está sesgada a la derecha: media = sd = 10,
asimetría = 2. La distribución muestral de xbar aún no entra en vista.

Ejecútalo:
    uv run es/L24_Teorema_Limite_Central/src/clt_01_skewed_population.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MEAN = 10.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) delay_population() --------------------------------------------
def delay_population():
    """Retorna la población exponencial de retrasos con media 10 minutos."""
    return stats.expon(scale=MEAN)
# ------------------------------------------------------------------------------


# --- NUEVO (2) population_summaries() ----------------------------------------
def population_summaries(model) -> dict[str, float]:
    """Reporta media, sd, asimetría y P(X > 20) del reloj de retraso."""
    return {
        "mean": float(model.mean()),
        "sd": float(model.std()),
        "skewness": float(model.stats(moments="s")),
        "p_gt_20": float(1.0 - model.cdf(20.0)),
        "median": float(model.median()),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(model) -> Path:
    """Grafica la densidad exponencial de retrasos sesgada a la derecha."""
    output_path = DIR_FIGURES / "clt_01_skewed_population.png"
    x = np.linspace(0, 50, 400)
    y = model.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Exponencial media 10")
    ax.axvline(model.mean(), color="#EC2661", ls="--", lw=1.4, label="Media 10")
    ax.axvline(model.median(), color="#5B8DEF", ls=":", lw=1.4, label="Mediana")
    ax.set_xlabel("Tiempo de retraso (minutos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("Población de retrasos sesgada a la derecha: asimetría = 2")
    ax.set_xlim(0, 50)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    model = delay_population()
    values = population_summaries(model)
    figure_path = save_figure(model)

    print("================================================================")
    print("LECCIÓN 24 - PASO 1: POBLACIÓN ASIMÉTRICA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Media poblacional               : {values['mean']:.6f}")
    print(f"Desv. estándar poblacional      : {values['sd']:.6f}")
    print(f"Mediana poblacional             : {values['median']:.6f}")
    print(f"Asimetría poblacional           : {values['skewness']:.6f}")
    print(f"P(X > 20)                       : {values['p_gt_20']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

