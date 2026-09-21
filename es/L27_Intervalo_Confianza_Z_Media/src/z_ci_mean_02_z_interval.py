"""
Lección 27 - Paso 2: Intervalo de confianza Z con sigma conocida
===============================================================
La Receta
Partir de z_ci_mean_01_sample_standard_error.py e introducir:
    1. z_critical()             z* = 1.96 para un intervalo al 95 por ciento
    2. z_confidence_interval()  xbar +/- z* * sigma / sqrt(n)
    3. save_figure()            dibujar el intervalo alrededor de la media muestral

Se reconstruyen los mismos n = 36 llenados sintéticos con SEED = 42. No se
importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 36
SIGMA = 10.0
MU_TRUE = 502.0
CONFIDENCE = 0.95
Z_STAR = 1.96
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n llenados iid de N(mu_true, sigma). El analista no conoce mu."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)


def sampling_metrics(sample: np.ndarray) -> dict[str, float]:
    """Retorna la media muestral y el error estándar con sigma conocida."""
    xbar = float(np.mean(sample))
    se = SIGMA / np.sqrt(N)
    return {
        "n": float(N),
        "sigma": SIGMA,
        "xbar": xbar,
        "se": float(se),
    }


# --- NUEVO (1) z_critical() --------------------------------------------------
def z_critical(confidence: float = CONFIDENCE) -> dict[str, float]:
    """Retorna el z* de libro 1.96 y la confirmación de scipy.stats.norm."""
    alpha = 1.0 - confidence
    scipy_z = float(stats.norm.ppf(1.0 - alpha / 2.0))
    return {
        "confidence": confidence,
        "alpha": alpha,
        "z_star": Z_STAR,
        "scipy_z": scipy_z,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) z_confidence_interval() ---------------------------------------
def z_confidence_interval(
    metrics: dict[str, float],
    z_star: float,
) -> dict[str, float]:
    """Construye xbar +/- z* * EE cuando sigma se trata como conocida."""
    margin = z_star * metrics["se"]
    lower = metrics["xbar"] - margin
    upper = metrics["xbar"] + margin
    return {
        "margin": float(margin),
        "lower": float(lower),
        "upper": float(upper),
        "width": float(upper - lower),
        "covers_true_mu": float(lower <= MU_TRUE <= upper),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    metrics: dict[str, float],
    interval: dict[str, float],
) -> Path:
    """Guarda un intervalo z de una muestra alrededor de la media observada."""
    output_path = DIR_FIGURES / "z_ci_mean_02_z_interval.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.errorbar(
        [metrics["xbar"]],
        [1],
        xerr=[[metrics["xbar"] - interval["lower"]],
              [interval["upper"] - metrics["xbar"]]],
        fmt="o",
        color="#1A2E51",
        ecolor="#EC2661",
        elinewidth=3.0,
        capsize=8,
        markersize=9,
    )
    ax.axvline(MU_TRUE, color="#5B8DEF", linestyle="--", linewidth=1.6,
               label=f"mu verdadera = {MU_TRUE:.1f} ml (oculta)")
    ax.set_yticks([1])
    ax.set_yticklabels(["Intervalo z al 95%"])
    ax.set_xlabel("Volumen de llenado (ml)")
    ax.set_title("Intervalo Z: xbar +/- 1.96 * sigma / sqrt(n)")
    ax.set_xlim(interval["lower"] - 4, interval["upper"] + 4)
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        metrics["xbar"],
        1.18,
        f"[{interval['lower']:.2f}, {interval['upper']:.2f}]",
        ha="center",
        fontsize=10,
        color="#1A2E51",
        fontweight="bold",
    )
    ax.set_ylim(0.4, 1.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_fill_sample()
    metrics = sampling_metrics(sample)
    critical = z_critical()
    interval = z_confidence_interval(metrics, critical["z_star"])
    figure_path = save_figure(metrics, interval)

    print("================================================================")
    print("LECCIÓN 27 - PASO 2: INTERVALO DE CONFIANZA Z")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Sigma conocida (ml)             : {SIGMA:.6f}")
    print(f"Media muestral xbar (ml)        : {metrics['xbar']:.6f}")
    print(f"Error estándar                  : {metrics['se']:.6f}")
    print(f"Nivel de confianza              : {critical['confidence']:.2f}")
    print(f"z-estrella de libro             : {critical['z_star']:.6f}")
    print(f"z-estrella scipy.stats.norm.ppf : {critical['scipy_z']:.6f}")
    print(f"Margen de error (ml)            : {interval['margin']:.6f}")
    print(f"Límite inferior (ml)            : {interval['lower']:.6f}")
    print(f"Límite superior (ml)            : {interval['upper']:.6f}")
    print(f"Anchura del intervalo (ml)      : {interval['width']:.6f}")
    print(f"Cubre la mu verdadera           : {'Sí' if interval['covers_true_mu'] else 'No'}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

