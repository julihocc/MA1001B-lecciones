"""
Lección 22 - Paso 3: Conformidad no es lo mismo que estar centrado
=================================================================
NUEVO EN ESTE PASO: tight_offcenter_model(), compliance_table() y save_figure().

La Receta
CAMBIOS RESPECTO A tolerancias_normal_02_desplazamiento_media.py
Introdúcelos en este orden:
    1. tight_offcenter_model()  mu = 52, sigma = 2 en la misma especificación
    2. compliance_table()       un rendimiento alto puede ocultar una media descentrada
    3. save_figure()            compara centrado-ancho frente a estrecho-desplazado

Un proceso puede cumplir la especificación [44, 56] a una tasa alta y aun así
no estar centrado en 50. La conformidad con la especificación no es lo mismo
que un proceso centrado.

Ejecútalo:
    uv run es/L22_Aplicaciones_Normal_Tolerancias/src/tolerancias_normal_03_centrado_vs_conforme.py
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
SIGMA_TIGHT = 2.0
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
        "sigma": sigma,
        "z_low": (lsl - mu) / sigma,
        "z_high": (usl - mu) / sigma,
        "yield": float(model.cdf(usl) - model.cdf(lsl)),
    }


# --- NUEVO (1) tight_offcenter_model() ---------------------------------------
def tight_offcenter_model():
    """Devuelve un proceso más estrecho desplazado a 52 gramos."""
    return process_model(mu=MU_SHIFT, sigma=SIGMA_TIGHT)
# ------------------------------------------------------------------------------


# --- NUEVO (2) compliance_table() --------------------------------------------
def compliance_table() -> dict[str, dict[str, float]]:
    """Compara el rendimiento centrado-ancho con el estrecho descentrado."""
    centered = spec_yield(process_model(MU, SIGMA))
    tight = spec_yield(tight_offcenter_model())
    return {"centered": centered, "tight": tight}
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(table: dict[str, dict[str, float]]) -> Path:
    """Superpone un proceso centrado-ancho y un proceso estrecho descentrado."""
    output_path = DIR_FIGURES / "tolerancias_normal_03_centrado_vs_conforme.png"
    centered = process_model(MU, SIGMA)
    tight = tight_offcenter_model()
    x = np.linspace(MU - 4 * SIGMA, MU + 5 * SIGMA, 400)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(
        x,
        centered.pdf(x),
        color="#1A2E51",
        lw=2.2,
        label=f"Centrado sigma=4, rend.={table['centered']['yield']:.4f}",
    )
    ax.plot(
        x,
        tight.pdf(x),
        color="#EC2661",
        lw=2.2,
        label=f"Descentrado sigma=2, rend.={table['tight']['yield']:.4f}",
    )
    ax.axvline(LSL, color="#646464", ls="--", lw=1.2, label="Espec [44, 56]")
    ax.axvline(USL, color="#646464", ls="--", lw=1.2)
    ax.axvline(MU, color="#5B8DEF", ls=":", lw=1.2, label="Objetivo 50")
    ax.set_xlabel("Peso de llenado (gramos)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("Un rendimiento alto puede ocultar un proceso que no está centrado")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    table = compliance_table()
    figure_path = save_figure(table)
    centered = table["centered"]
    tight = table["tight"]

    print("================================================================")
    print("LECCIÓN 22 - PASO 3: CENTRADO FRENTE A CONFORME")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"mu, sigma centrados              : {centered['mu']:.6f}, {centered['sigma']:.6f}")
    print(f"Cortes z centrados               : {centered['z_low']:.6f} a {centered['z_high']:.6f}")
    print(f"Rendimiento centrado             : {centered['yield']:.6f}")
    print(f"mu, sigma estrechos              : {tight['mu']:.6f}, {tight['sigma']:.6f}")
    print(f"Cortes z estrechos               : {tight['z_low']:.6f} a {tight['z_high']:.6f}")
    print(f"Rendimiento estrecho             : {tight['yield']:.6f}")
    print("Límite: la conformidad con la espec no es lo mismo que estar centrado")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

