"""
Lección 31 - Paso 1: Varianza muestral de una muestra normal pequeña
====================================================================
NUEVO EN ESTE PASO: generate_cycle_sample(), sample_variance() y
save_figure().

La Receta
Una estación de empaque completamente sintética registra n = 20 tiempos de
ciclo. El proceso se trata como normal. La varianza muestral s^2 estima la
varianza poblacional desconocida sigma^2, con gl = n - 1 = 19.

Ejecútalo:
    uv run es/L31_Chi_Cuadrada_Intervalo_Varianza/src/chi_cuadrada_01_varianza_muestral.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 20
MU_TRUE = 12.0
SIGMA_TRUE = 3.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) generate_cycle_sample() ---------------------------------------
def generate_cycle_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n tiempos de ciclo iid normales. El analista no conoce sigma^2."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA_TRUE, size=N)
# ------------------------------------------------------------------------------


# --- NUEVO (2) sample_variance() ---------------------------------------------
def sample_variance(sample: np.ndarray) -> dict[str, float]:
    """Devuelve s^2 con divisor n - 1 y la varianza poblacional oculta."""
    s2 = float(np.var(sample, ddof=1))
    return {
        "n": float(N),
        "df": float(N - 1),
        "xbar": float(np.mean(sample)),
        "s": float(np.sqrt(s2)),
        "s2": s2,
        "hidden_sigma2": SIGMA_TRUE ** 2,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """Guarda un histograma de tiempos de ciclo con s como escala."""
    output_path = DIR_FIGURES / "chi_cuadrada_01_varianza_muestral.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(sample, bins=8, color="#A7B0BF", edgecolor="white")
    ax.axvline(metrics["xbar"], color="#EC2661", linewidth=2.4,
               label=f"Media = {metrics['xbar']:.2f} min")
    ax.axvline(metrics["xbar"] - metrics["s"], color="#5B8DEF",
               linestyle="--", linewidth=1.6)
    ax.axvline(metrics["xbar"] + metrics["s"], color="#5B8DEF",
               linestyle="--", linewidth=1.6,
               label=f"s = {metrics['s']:.2f} min")
    ax.set_xlabel("Tiempo de ciclo (minutos)")
    ax.set_ylabel("Conteo de ciclos")
    ax.set_title("Varianza muestral de n = 20 tiempos de ciclo normales")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_cycle_sample()
    metrics = sample_variance(sample)
    figure_path = save_figure(sample, metrics)

    print("================================================================")
    print("LECCIÓN 31 - PASO 1: VARIANZA MUESTRAL")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Grados de libertad n-1          : {int(metrics['df'])}")
    print(f"Media muestral (min)            : {metrics['xbar']:.6f}")
    print(f"Desviación estándar muestral s  : {metrics['s']:.6f}")
    print(f"Varianza muestral s^2           : {metrics['s2']:.6f}")
    print(f"Sigma^2 oculta                  : {metrics['hidden_sigma2']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

