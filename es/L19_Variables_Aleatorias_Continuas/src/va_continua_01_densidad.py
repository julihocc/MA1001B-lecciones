"""
Lección 19 - Paso 1: Densidad continua del tiempo de servicio
=============================================================
NUEVO EN ESTE PASO: service_time_model(), density_at_points() y save_figure().

La Receta
Un reloj de mesa de ayuda completamente sintético registra el tiempo de
servicio X en [2, 14] minutos. El modelo operativo es una densidad triangular
con moda 6. A diferencia de una FMP discreta, la altura f(x) no es una
probabilidad.

Ejecútalo:
    uv run es/L19_Variables_Aleatorias_Continuas/src/va_continua_01_densidad.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
A = 2.0
B = 14.0
MODE = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) service_time_model() ------------------------------------------
def service_time_model():
    """Devuelve el modelo triangular del tiempo de servicio sintético en [2, 14]."""
    c = (MODE - A) / (B - A)
    return stats.triang(c=c, loc=A, scale=B - A)
# ------------------------------------------------------------------------------


# --- NUEVO (2) density_at_points() -------------------------------------------
def density_at_points(model) -> dict[str, float]:
    """Evalúa densidad, media y área total del modelo de tiempo de servicio."""
    return {
        "f_at_a": float(model.pdf(A)),
        "f_at_mode": float(model.pdf(MODE)),
        "f_at_b": float(model.pdf(B)),
        "mean": float(model.mean()),
        "total_area": float(model.cdf(B) - model.cdf(A)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(model) -> Path:
    """Guarda la densidad triangular del reloj sintético de tiempo de servicio."""
    output_path = DIR_FIGURES / "va_continua_01_densidad.png"
    x = np.linspace(A, B, 400)
    y = model.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Densidad f(x)")
    ax.fill_between(x, y, color="#5B8DEF", alpha=0.28)
    ax.axvline(MODE, color="#EC2661", ls="--", lw=1.4, label="Moda en 6 min")
    ax.plot(MODE, model.pdf(MODE), "o", color="#EC2661", zorder=3)
    ax.set_xlabel("Tiempo de servicio (minutos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("Densidad triangular en [2, 14]: la altura no es probabilidad")
    ax.set_xlim(A, B)
    ax.set_ylim(0, 0.22)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    model = service_time_model()
    values = density_at_points(model)
    figure_path = save_figure(model)

    print("================================================================")
    print("LECCIÓN 19 - PASO 1: DENSIDAD CONTINUA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Soporte [a, b]                   : [{A:.1f}, {B:.1f}]")
    print(f"Moda                             : {MODE:.1f}")
    print(f"f(2)                             : {values['f_at_a']:.6f}")
    print(f"f(6) en la moda                  : {values['f_at_mode']:.6f}")
    print(f"f(14)                            : {values['f_at_b']:.6f}")
    print(f"Media (a + b + moda) / 3         : {values['mean']:.6f}")
    print(f"Área total bajo f                : {values['total_area']:.6f}")
    print("f(6) es una altura de densidad, no P(X = 6)")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

