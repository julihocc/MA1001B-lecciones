"""
Lección 36 - Paso 2: Estadístico z con p0 en el error estándar
==============================================================
NUEVO EN ESTE PASO: se_under_h0(), z_and_p_value() y save_figure().

La Receta
Partir de prueba_proporcion_01_muestra_y_condiciones.py e introducir:
    1. se_under_h0()          el error estándar usa p0, no phat
    2. z_and_p_value()        prueba z de cola derecha para H1: p > p0
    3. save_figure()          sombrear la cola superior de N(0, 1)

Los mismos conteos sintéticos n = 200, x = 28 se reconstruyen a partir de
constantes. No se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 200
X_LATE = 28
P0 = 0.10
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def sample_proportion(x: int = X_LATE, n: int = N) -> dict[str, float]:
    """Devuelve el conteo observado de banderas de retraso y la proporción muestral."""
    phat = x / n
    return {"n": float(n), "x": float(x), "phat": float(phat), "p0": P0}


# --- NUEVO (1) se_under_h0() -------------------------------------------------
def se_under_h0(n: int = N, p0: float = P0) -> float:
    """Error estándar de phat cuando H0: p = p0 es verdadera."""
    return float(np.sqrt(p0 * (1.0 - p0) / n))
# ------------------------------------------------------------------------------


# --- NUEVO (2) z_and_p_value() -----------------------------------------------
def z_and_p_value(phat: float, p0: float, se: float) -> dict[str, float]:
    """Estadístico z de cola derecha y valor p para H1: p > p0."""
    z_stat = (phat - p0) / se
    p_value = float(stats.norm.sf(z_stat))
    z_critical = float(stats.norm.ppf(1.0 - ALPHA))
    return {
        "z_stat": float(z_stat),
        "p_value": p_value,
        "z_critical": z_critical,
        "alpha": ALPHA,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(z_stat: float, z_critical: float) -> Path:
    """Sombrea la cola derecha de la normal estándar más allá del z observado."""
    output_path = DIR_FIGURES / "prueba_proporcion_02_z_valor_p.png"
    x = np.linspace(-3.6, 3.6, 600)
    y = stats.norm.pdf(x)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    ax.fill_between(x, y, where=(x >= z_stat), color="#EC2661", alpha=0.45)
    ax.axvline(z_stat, color="#EC2661", linewidth=1.6,
               label=f"z observado = {z_stat:.2f}")
    ax.axvline(z_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"z* = {z_critical:.2f}")
    ax.set_xlabel("z")
    ax.set_ylabel("Densidad")
    ax.set_title("Prueba z de cola derecha para una proporción")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    summary = sample_proportion()
    se = se_under_h0()
    test = z_and_p_value(summary["phat"], summary["p0"], se)
    decision = "rechazar H0" if test["p_value"] < ALPHA else "no rechazar H0"
    figure_path = save_figure(test["z_stat"], test["z_critical"])

    print("================================================================")
    print("LECCIÓN 36 - PASO 2: ESTADÍSTICO Z Y VALOR P")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Hipótesis                       : H0: p = {P0:.2f} frente a H1: p > {P0:.2f}")
    print(f"Proporción muestral phat        : {summary['phat']:.6f}")
    print(f"EE bajo H0 sqrt(p0(1-p0)/n)     : {se:.6f}")
    print(f"Estadístico z (phat - p0)/EE    : {test['z_stat']:.6f}")
    print(f"Valor p de cola derecha         : {test['p_value']:.6f}")
    print(f"z* crítica (alfa = 0.05)        : {test['z_critical']:.6f}")
    print(f"Decisión con alfa = 0.05        : {decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

