"""
Lección 34 - Paso 3: Sigma conocida rara vez es verdadera en datos de operaciones
================================================================================
NUEVO EN ESTE PASO: sample_sigma_estimate(), compare_z_with_s() y
save_figure().

La Receta
Partir de prueba_z_media_02_valor_p.py e introducir:
    1. sample_sigma_estimate()  s de las mismas n = 40 entregas
    2. compare_z_with_s()       z usando sigma frente a z usando s
    3. save_figure()            contrastar los dos valores p

Límite: los datos de operaciones casi nunca llegan con una sigma poblacional
conocida. Reemplazar sigma por s pero conservar la curva de referencia z es
la prueba incorrecta. La Lección 35 reemplaza z por un estadístico t con
gl = n - 1.
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_delivery_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n tiempos de entrega iid. El analista conoce sigma, no mu."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


# --- NUEVO (1) sample_sigma_estimate() ---------------------------------------
def sample_sigma_estimate(sample: np.ndarray) -> dict[str, float]:
    """Estima sigma a partir de la muestra. Esta s no es un parámetro conocido."""
    xbar = float(np.mean(sample))
    s = float(np.std(sample, ddof=1))
    return {
        "xbar": xbar,
        "s": s,
        "se_known": SIGMA / np.sqrt(N),
        "se_plug_in": s / np.sqrt(N),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_z_with_s() --------------------------------------------
def compare_z_with_s(stats_s: dict[str, float]) -> dict[str, float]:
    """Conserva la curva de referencia z pero sustituye sigma por s."""
    z_known = (stats_s["xbar"] - MU0) / stats_s["se_known"]
    z_plug = (stats_s["xbar"] - MU0) / stats_s["se_plug_in"]
    p_known = float(stats.norm.sf(z_known))
    p_plug = float(stats.norm.sf(z_plug))
    return {
        "z_known": float(z_known),
        "z_plug": float(z_plug),
        "p_known": p_known,
        "p_plug": p_plug,
        "p_difference": abs(p_plug - p_known),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """Contrasta valores p del z con sigma conocida frente al z inválido con s."""
    output_path = DIR_FIGURES / "prueba_z_media_03_limite_sigma_conocida.png"
    labels = ["z válido\n(sigma conocida)", "z inválido con s\n(sigma desconocida)"]
    values = [comparison["p_known"], comparison["p_plug"]]
    colors = ["#1A2E51", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.axhline(0.05, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label="alfa = 0.05")
    ax.set_ylabel("Valor p de cola superior")
    ax.set_title("Sigma conocida rara vez es verdadera en datos de operaciones")
    ax.set_ylim(0, max(0.12, max(values) + 0.03))
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.004,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_delivery_sample()
    stats_s = sample_sigma_estimate(sample)
    comparison = compare_z_with_s(stats_s)
    figure_path = save_figure(comparison)

    print("================================================================")
    print("LECCIÓN 34 - PASO 3: LÍMITE DE SIGMA CONOCIDA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Sigma conocida                  : {SIGMA:.6f}")
    print(f"Media muestral xbarra           : {stats_s['xbar']:.6f}")
    print(f"Desviación estándar muestral s  : {stats_s['s']:.6f}")
    print(f"z válido (sigma conocida)       : {comparison['z_known']:.6f}")
    print(f"Valor p válido                  : {comparison['p_known']:.6f}")
    print(f"z inválido con s                : {comparison['z_plug']:.6f}")
    print(f"Valor p inválido                : {comparison['p_plug']:.6f}")
    print(f"Diferencia absoluta de valor p  : {comparison['p_difference']:.6f}")
    print("Límite                         : sigma conocida rara vez es verdadera; use la t")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

