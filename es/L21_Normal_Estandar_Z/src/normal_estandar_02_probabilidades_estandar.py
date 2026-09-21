"""
Lección 21 - Paso 2: Probabilidades normales estándar
====================================================
NUEVO EN ESTE PASO: standard_normal(), left_tail_probability() y save_figure().

La Receta
CAMBIOS RESPECTO A normal_estandar_01_puntuaciones_z.py
Introdúcelos en este orden:
    1. standard_normal()        Z ~ N(0, 1) como la regla estandarizada
    2. left_tail_probability()  P(Z <= 1.25) desde scipy.stats.norm
    3. save_figure()            sombrea la cola izquierda estándar

El mismo modelo Normal(50, 8) de puntuación de auditoría se reconstruye.
P(X <= 60) iguala P(Z <= 1.25). No se importa ningún script anterior de la
lección.

Ejecútalo:
    uv run es/L21_Normal_Estandar_Z/src/normal_estandar_02_probabilidades_estandar.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 50.0
SIGMA = 8.0
X_MARK = 60.0
Z_MARK = (X_MARK - MU) / SIGMA
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) standard_normal() ---------------------------------------------
def standard_normal():
    """Devuelve el modelo normal estándar Z ~ N(0, 1)."""
    return stats.norm(loc=0.0, scale=1.0)
# ------------------------------------------------------------------------------


# --- NUEVO (2) left_tail_probability() ---------------------------------------
def left_tail_probability(z_model, z_mark: float) -> dict[str, float]:
    """Calcula P(Z <= z), P(Z > z) y la probabilidad de puntuación cruda coincidente."""
    p_left = float(z_model.cdf(z_mark))
    operating = stats.norm(loc=MU, scale=SIGMA)
    return {
        "z_mark": z_mark,
        "p_z_le": p_left,
        "p_z_gt": 1.0 - p_left,
        "p_x_le": float(operating.cdf(X_MARK)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(z_model, z_mark: float, p_left: float) -> Path:
    """Sombrea P(Z <= 1.25) en la curva normal estándar."""
    output_path = DIR_FIGURES / "normal_estandar_02_probabilidades_estandar.png"
    z = np.linspace(-4, 4, 400)
    y = z_model.pdf(z)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(z, y, color="#1A2E51", lw=2.2)
    ax.fill_between(z[z <= z_mark], y[z <= z_mark], color="#5B8DEF", alpha=0.35,
                    label=f"P(Z <= {z_mark:.2f}) = {p_left:.4f}")
    ax.axvline(z_mark, color="#EC2661", ls="--", lw=1.4)
    ax.set_xlabel("z")
    ax.set_ylabel("Densidad")
    ax.set_title("Cola izquierda normal estándar en z = 1.25")
    ax.set_xlim(-4, 4)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    z_model = standard_normal()
    values = left_tail_probability(z_model, Z_MARK)
    figure_path = save_figure(z_model, Z_MARK, values["p_z_le"])

    print("================================================================")
    print("LECCIÓN 21 - PASO 2: PROBABILIDADES ESTÁNDAR")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"z = (60 - 50) / 8                : {values['z_mark']:.6f}")
    print(f"P(Z <= 1.25)                     : {values['p_z_le']:.6f}")
    print(f"P(Z > 1.25)                      : {values['p_z_gt']:.6f}")
    print(f"P(X <= 60) en Normal(50, 8)      : {values['p_x_le']:.6f}")
    print("P(X <= 60) iguala P(Z <= 1.25)")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

