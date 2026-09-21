"""
Lección 19 - Paso 2: Probabilidad de intervalo como área
========================================================
NUEVO EN ESTE PASO: interval_probability(), closed_vs_open() y save_figure().

La Receta
CAMBIOS RESPECTO A va_continua_01_densidad.py
Introdúcelos en este orden:
    1. interval_probability()   P(a < X < b) como área bajo la densidad
    2. closed_vs_open()         P(a < X < b) iguala P(a <= X <= b)
    3. save_figure()            sombrea el intervalo objetivo en la densidad

El mismo modelo triangular de tiempo de servicio en [2, 14] se reconstruye.
No se importa ningún script anterior de la lección.

Ejecútalo:
    uv run es/L19_Variables_Aleatorias_Continuas/src/va_continua_02_probabilidad_intervalo.py
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
LOW = 4.0
HIGH = 10.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def service_time_model():
    """Devuelve el modelo triangular del tiempo de servicio sintético en [2, 14]."""
    c = (MODE - A) / (B - A)
    return stats.triang(c=c, loc=A, scale=B - A)


# --- NUEVO (1) interval_probability() ----------------------------------------
def interval_probability(model, left: float, right: float) -> float:
    """Devuelve P(left < X < right) como el área entre los valores de la FDA."""
    return float(model.cdf(right) - model.cdf(left))
# ------------------------------------------------------------------------------


# --- NUEVO (2) closed_vs_open() ----------------------------------------------
def closed_vs_open(model, left: float, right: float) -> dict[str, float]:
    """Compara probabilidades de intervalo abierto y cerrado para X continua."""
    open_prob = interval_probability(model, left, right)
    closed_prob = float(model.cdf(right) - model.cdf(left))
    return {
        "open": open_prob,
        "closed": closed_prob,
        "cdf_left": float(model.cdf(left)),
        "cdf_right": float(model.cdf(right)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(model, left: float, right: float, area: float) -> Path:
    """Sombrea P(4 < X < 10) en la densidad triangular de tiempo de servicio."""
    output_path = DIR_FIGURES / "va_continua_02_probabilidad_intervalo.png"
    x = np.linspace(A, B, 400)
    y = model.pdf(x)
    mask = (x >= left) & (x <= right)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2)
    ax.fill_between(x[mask], y[mask], color="#EC2661", alpha=0.35,
                    label=f"P({left:.0f} < X < {right:.0f}) = {area:.4f}")
    ax.set_xlabel("Tiempo de servicio (minutos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("La probabilidad de intervalo es área, no una altura puntual")
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
    area = interval_probability(model, LOW, HIGH)
    comparison = closed_vs_open(model, LOW, HIGH)
    figure_path = save_figure(model, LOW, HIGH, area)

    print("================================================================")
    print("LECCIÓN 19 - PASO 2: PROBABILIDAD DE INTERVALO")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Intervalo                        : ({LOW:.1f}, {HIGH:.1f})")
    print(f"F(4)                             : {comparison['cdf_left']:.6f}")
    print(f"F(10)                            : {comparison['cdf_right']:.6f}")
    print(f"P(4 < X < 10)                    : {comparison['open']:.6f}")
    print(f"P(4 <= X <= 10)                  : {comparison['closed']:.6f}")
    print("Los intervalos abierto y cerrado coinciden para X continua")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

