"""
Lección 21 - Paso 1: Estandarizar una puntuación operativa
=========================================================
NUEVO EN ESTE PASO: operating_model(), z_score() y save_figure().

La Receta
Un reloj de puntuación de auditoría completamente sintético se modela como
Normal(mu=50, sigma=8). La puntuación z (x - mu) / sigma localiza una
puntuación cruda en la regla normal estándar. Una puntuación de 60 está a
1.25 desviaciones estándar por encima de la media.

Ejecútalo:
    uv run es/L21_Normal_Estandar_Z/src/normal_estandar_01_puntuaciones_z.py
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) operating_model() ---------------------------------------------
def operating_model():
    """Devuelve el modelo Normal(50, 8) de la puntuación de auditoría sintética."""
    return stats.norm(loc=MU, scale=SIGMA)
# ------------------------------------------------------------------------------


# --- NUEVO (2) z_score() -----------------------------------------------------
def z_score(x: float, mu: float = MU, sigma: float = SIGMA) -> float:
    """Convierte una puntuación cruda a unidades de desviación estándar."""
    return (x - mu) / sigma
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(model, z_mark: float) -> Path:
    """Grafica la densidad operativa y marca la puntuación cruda x = 60."""
    output_path = DIR_FIGURES / "normal_estandar_01_puntuaciones_z.png"
    x = np.linspace(MU - 4 * SIGMA, MU + 4 * SIGMA, 400)
    y = model.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Normal(50, 8)")
    ax.axvline(MU, color="#5B8DEF", ls=":", lw=1.3, label="Media 50")
    ax.axvline(X_MARK, color="#EC2661", ls="--", lw=1.4,
               label=f"x = 60, z = {z_mark:.2f}")
    ax.fill_between(x[x <= X_MARK], y[x <= X_MARK], color="#5B8DEF", alpha=0.25)
    ax.set_xlabel("Puntuación de auditoría")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("Una puntuación cruda de 60 es z = 1.25 en la regla estándar")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    model = operating_model()
    z_mark = z_score(X_MARK)
    z_low = z_score(MU - SIGMA)
    z_high = z_score(MU + SIGMA)
    figure_path = save_figure(model, z_mark)

    print("================================================================")
    print("LECCIÓN 21 - PASO 1: PUNTUACIONES Z")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Media mu                         : {MU:.6f}")
    print(f"Desviación estándar sigma        : {SIGMA:.6f}")
    print(f"Puntuación cruda x               : {X_MARK:.6f}")
    print(f"z = (x - mu) / sigma             : {z_mark:.6f}")
    print(f"z en mu - sigma                  : {z_low:.6f}")
    print(f"z en mu + sigma                  : {z_high:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

