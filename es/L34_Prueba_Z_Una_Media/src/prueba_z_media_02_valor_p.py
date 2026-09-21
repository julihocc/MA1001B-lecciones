"""
Lección 34 - Paso 2: Valor p de la prueba z unilateral
=====================================================
NUEVO EN ESTE PASO: p_value_upper(), test_decision() y save_figure().

La Receta
Partir de prueba_z_media_01_estadistico_z.py e introducir:
    1. p_value_upper()      p = scipy.stats.norm.sf(z)
    2. test_decision()      comparar p con alfa = 0.05
    3. save_figure()        sombrear la cola normal estándar más allá de z

Las mismas n = 40 entregas sintéticas se reconstruyen con SEED = 42. No se
importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 40
MU0 = 80.0
MU_TRUE = 82.0
SIGMA = 6.0
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_delivery_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n tiempos de entrega iid. El analista conoce sigma, no mu."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


def z_statistic(sample: np.ndarray) -> dict[str, float]:
    """Calcula xbarra, EE y el estadístico z bajo H0: mu = 80."""
    xbar = float(np.mean(sample))
    se = SIGMA / np.sqrt(N)
    z = (xbar - MU0) / se
    return {"xbar": xbar, "se": float(se), "z": float(z)}


# --- NUEVO (1) p_value_upper() -----------------------------------------------
def p_value_upper(z: float) -> float:
    """Valor p de cola superior P(Z >= z) bajo la normal estándar."""
    return float(stats.norm.sf(z))
# ------------------------------------------------------------------------------


# --- NUEVO (2) test_decision() -----------------------------------------------
def test_decision(p_value: float, alpha: float = ALPHA) -> dict[str, float]:
    """Rechazar H0 cuando el valor p es menor que alfa."""
    return {
        "alpha": alpha,
        "p_value": p_value,
        "reject_h0": float(p_value < alpha),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(z: float, p_value: float) -> Path:
    """Sombrea la cola superior de la normal estándar más allá del z observado."""
    output_path = DIR_FIGURES / "prueba_z_media_02_valor_p.png"
    x = np.linspace(-4.0, 4.0, 400)
    y = stats.norm.pdf(x)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    ax.fill_between(
        x[x >= z],
        y[x >= z],
        color="#EC2661",
        alpha=0.55,
        label=f"valor p = {p_value:.4f}",
    )
    ax.axvline(z, color="#EC2661", linewidth=2.0)
    ax.set_xlabel("z de la normal estándar")
    ax.set_ylabel("Densidad")
    ax.set_title("Valor p de cola superior de la prueba z")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_delivery_sample()
    metrics = z_statistic(sample)
    p_value = p_value_upper(metrics["z"])
    decision = test_decision(p_value)
    figure_path = save_figure(metrics["z"], p_value)

    print("================================================================")
    print("LECCIÓN 34 - PASO 2: VALOR P Y DECISIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Media muestral xbarra (min)     : {metrics['xbar']:.6f}")
    print(f"Estadístico z                   : {metrics['z']:.6f}")
    print(f"Valor p de cola superior        : {p_value:.6f}")
    print(f"Nivel de significancia alfa     : {decision['alpha']:.6f}")
    print(f"Rechazar H0 con alfa=0.05       : {'sí' if decision['reject_h0'] else 'no'}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

