"""
Lección 22 - Paso 1: Rendimiento dentro de un intervalo de especificación
========================================================================
NUEVO EN ESTE PASO: process_model(), spec_yield() y save_figure().

La Receta
Un proceso de llenado completamente sintético se modela como Normal(mu=50,
sigma=4) gramos. El intervalo de especificación es [44, 56]. El rendimiento
es la probabilidad de que una unidad caiga dentro de la especificación,
calculada a partir de dos cortes z.

Ejecútalo:
    uv run es/L22_Aplicaciones_Normal_Tolerancias/src/tolerancias_normal_01_rendimiento_espec.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 50.0
SIGMA = 4.0
LSL = 44.0
USL = 56.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) process_model() -----------------------------------------------
def process_model(mu: float = MU, sigma: float = SIGMA):
    """Devuelve el modelo Normal del proceso de llenado."""
    return stats.norm(loc=mu, scale=sigma)
# ------------------------------------------------------------------------------


# --- NUEVO (2) spec_yield() --------------------------------------------------
def spec_yield(model, lsl: float = LSL, usl: float = USL) -> dict[str, float]:
    """Convierte límites de especificación en cortes z y la probabilidad en espec."""
    mu = float(model.mean())
    sigma = float(model.std())
    z_low = (lsl - mu) / sigma
    z_high = (usl - mu) / sigma
    yield_p = float(model.cdf(usl) - model.cdf(lsl))
    return {
        "mu": mu,
        "sigma": sigma,
        "z_low": z_low,
        "z_high": z_high,
        "yield": yield_p,
        "below": float(model.cdf(lsl)),
        "above": float(1.0 - model.cdf(usl)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(model, summary: dict[str, float]) -> Path:
    """Sombrea la región en especificación del proceso de llenado centrado."""
    output_path = DIR_FIGURES / "tolerancias_normal_01_rendimiento_espec.png"
    x = np.linspace(MU - 4 * SIGMA, MU + 4 * SIGMA, 400)
    y = model.pdf(x)
    mask = (x >= LSL) & (x <= USL)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", lw=2.2)
    ax.fill_between(x[mask], y[mask], color="#5B8DEF", alpha=0.35,
                    label=f"Rendimiento = {summary['yield']:.4f}")
    ax.axvline(LSL, color="#EC2661", ls="--", lw=1.3, label="LIE = 44")
    ax.axvline(USL, color="#EC2661", ls="--", lw=1.3, label="LSE = 56")
    ax.axvline(MU, color="#646464", ls=":", lw=1.2, label="mu = 50")
    ax.set_xlabel("Peso de llenado (gramos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("Proceso centrado: rendimiento dentro de [44, 56]")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    model = process_model()
    summary = spec_yield(model)
    figure_path = save_figure(model, summary)

    print("================================================================")
    print("LECCIÓN 22 - PASO 1: RENDIMIENTO DE ESPECIFICACIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Media mu                         : {summary['mu']:.6f}")
    print(f"Desviación estándar sigma        : {summary['sigma']:.6f}")
    print(f"Intervalo de especificación      : [{LSL:.1f}, {USL:.1f}]")
    print(f"z en LIE                         : {summary['z_low']:.6f}")
    print(f"z en LSE                         : {summary['z_high']:.6f}")
    print(f"P(por debajo del LIE)            : {summary['below']:.6f}")
    print(f"P(por encima del LSE)            : {summary['above']:.6f}")
    print(f"Rendimiento P(en espec)          : {summary['yield']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

