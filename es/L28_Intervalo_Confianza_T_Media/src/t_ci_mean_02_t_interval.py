"""
Lección 28 - Paso 2: Intervalo t de Student con sigma desconocida
================================================================
La Receta
Partir de t_ci_mean_01_sample_sd.py e introducir:
    1. t_critical()             t* de scipy.stats.t.ppf con gl = n - 1
    2. t_confidence_interval()  xbar +/- t* * s / sqrt(n)
    3. save_figure()            dibujar el intervalo t y comparar t* con 1.96

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
SIGMA_TRUE = 10.0
MU_TRUE = 502.0
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n llenados iid. El analista observa la muestra, no sigma."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)


def sample_sd_metrics(sample: np.ndarray) -> dict[str, float]:
    """Retorna xbar, s, EE estimado y grados de libertad."""
    xbar = float(np.mean(sample))
    s = float(np.std(sample, ddof=1))
    se_hat = s / np.sqrt(N)
    return {
        "n": float(N),
        "df": float(N - 1),
        "xbar": xbar,
        "s": s,
        "se_hat": float(se_hat),
    }


# --- NUEVO (1) t_critical() --------------------------------------------------
def t_critical(df: float, confidence: float = CONFIDENCE) -> dict[str, float]:
    """Retorna t* = t.ppf(1 - alpha/2, gl) y el contraste z* = 1.96."""
    alpha = 1.0 - confidence
    t_star = float(stats.t.ppf(1.0 - alpha / 2.0, df))
    return {
        "confidence": confidence,
        "alpha": alpha,
        "df": df,
        "t_star": t_star,
        "z_star": 1.96,
        "t_minus_z": t_star - 1.96,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) t_confidence_interval() ---------------------------------------
def t_confidence_interval(
    metrics: dict[str, float],
    t_star: float,
) -> dict[str, float]:
    """Construye xbar +/- t* * s / sqrt(n) cuando sigma es desconocida."""
    margin = t_star * metrics["se_hat"]
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
    critical: dict[str, float],
    interval: dict[str, float],
) -> Path:
    """Guarda el intervalo t y anota t* versus z*."""
    output_path = DIR_FIGURES / "t_ci_mean_02_t_interval.png"
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
    ax.set_yticklabels(["Intervalo t al 95%"])
    ax.set_xlabel("Volumen de llenado (ml)")
    ax.set_title("Intervalo t: xbar +/- t* * s / sqrt(n), gl = 35")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.text(
        metrics["xbar"],
        1.18,
        f"t* = {critical['t_star']:.3f}  |  "
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
    metrics = sample_sd_metrics(sample)
    critical = t_critical(metrics["df"])
    interval = t_confidence_interval(metrics, critical["t_star"])
    figure_path = save_figure(metrics, critical, interval)

    print("================================================================")
    print("LECCIÓN 28 - PASO 2: INTERVALO T DE STUDENT")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Grados de libertad              : {int(critical['df'])}")
    print(f"Media muestral xbar (ml)        : {metrics['xbar']:.6f}")
    print(f"Desv. estándar muestral s       : {metrics['s']:.6f}")
    print(f"EE estimado                     : {metrics['se_hat']:.6f}")
    print(f"Nivel de confianza              : {critical['confidence']:.2f}")
    print(f"t-estrella (scipy t.ppf)        : {critical['t_star']:.6f}")
    print(f"Contraste z-estrella            : {critical['z_star']:.6f}")
    print(f"t-estrella menos z-estrella     : {critical['t_minus_z']:.6f}")
    print(f"Margen de error (ml)            : {interval['margin']:.6f}")
    print(f"Límite inferior (ml)            : {interval['lower']:.6f}")
    print(f"Límite superior (ml)            : {interval['upper']:.6f}")
    print(f"Anchura del intervalo (ml)      : {interval['width']:.6f}")
    print(f"Cubre la mu verdadera           : {'Sí' if interval['covers_true_mu'] else 'No'}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

