"""
Lección 22 - Paso 2: Un desplazamiento de la media reduce el rendimiento
=======================================================================
NUEVO EN ESTE PASO: shifted_model(), yield_drop() y save_figure().

La Receta
CAMBIOS RESPECTO A tolerancias_normal_01_rendimiento_espec.py
Introdúcelos en este orden:
    1. shifted_model()          mueve la media de llenado de 50 a 52
    2. yield_drop()             compara el rendimiento centrado con el desplazado
    3. save_figure()            superpone ambos procesos en la misma especificación

La especificación [44, 56] no se mueve. Desplazar mu a 52 cambia los cortes z
y baja la probabilidad en especificación. No se importa ningún script anterior
de la lección.

Ejecútalo:
    uv run es/L22_Aplicaciones_Normal_Tolerancias/src/tolerancias_normal_02_desplazamiento_media.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 50.0
MU_SHIFT = 52.0
SIGMA = 4.0
LSL = 44.0
USL = 56.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def process_model(mu: float = MU, sigma: float = SIGMA):
    """Devuelve el modelo Normal del proceso de llenado."""
    return stats.norm(loc=mu, scale=sigma)


def spec_yield(model, lsl: float = LSL, usl: float = USL) -> dict[str, float]:
    """Convierte límites de especificación en cortes z y la probabilidad en espec."""
    mu = float(model.mean())
    sigma = float(model.std())
    return {
        "mu": mu,
        "z_low": (lsl - mu) / sigma,
        "z_high": (usl - mu) / sigma,
        "yield": float(model.cdf(usl) - model.cdf(lsl)),
        "below": float(model.cdf(lsl)),
        "above": float(1.0 - model.cdf(usl)),
    }


# --- NUEVO (1) shifted_model() -----------------------------------------------
def shifted_model():
    """Devuelve el proceso de llenado después de un desplazamiento de media de +2 g."""
    return process_model(mu=MU_SHIFT, sigma=SIGMA)
# ------------------------------------------------------------------------------


# --- NUEVO (2) yield_drop() --------------------------------------------------
def yield_drop(centered: dict[str, float], shifted: dict[str, float]) -> float:
    """Devuelve cuánta probabilidad en especificación se pierde tras el desplazamiento."""
    return centered["yield"] - shifted["yield"]
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(centered_model, shifted_m, drop: float) -> Path:
    """Superpone los procesos de llenado centrado y desplazado."""
    output_path = DIR_FIGURES / "tolerancias_normal_02_desplazamiento_media.png"
    x = np.linspace(MU - 4 * SIGMA, MU + 5 * SIGMA, 400)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, centered_model.pdf(x), color="#1A2E51", lw=2.2,
            label="Centrado mu = 50")
    ax.plot(x, shifted_m.pdf(x), color="#EC2661", lw=2.2,
            label="Desplazado mu = 52")
    ax.axvline(LSL, color="#646464", ls="--", lw=1.2)
    ax.axvline(USL, color="#646464", ls="--", lw=1.2)
    ax.set_xlabel("Peso de llenado (gramos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title(f"Un desplazamiento de media de +2 g reduce el rendimiento en {drop:.4f}")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    centered_model = process_model()
    shifted_m = shifted_model()
    centered = spec_yield(centered_model)
    shifted = spec_yield(shifted_m)
    drop = yield_drop(centered, shifted)
    figure_path = save_figure(centered_model, shifted_m, drop)

    print("================================================================")
    print("LECCIÓN 22 - PASO 2: DESPLAZAMIENTO DE LA MEDIA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"mu centrado                      : {centered['mu']:.6f}")
    print(f"Cortes z centrados               : {centered['z_low']:.6f} a {centered['z_high']:.6f}")
    print(f"Rendimiento centrado             : {centered['yield']:.6f}")
    print(f"mu desplazado                    : {shifted['mu']:.6f}")
    print(f"Cortes z desplazados             : {shifted['z_low']:.6f} a {shifted['z_high']:.6f}")
    print(f"Rendimiento desplazado           : {shifted['yield']:.6f}")
    print(f"Caída de rendimiento             : {drop:.6f}")
    print(f"P(por debajo del LIE) desplazada : {shifted['below']:.6f}")
    print(f"P(por encima del LSE) desplazada : {shifted['above']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

