"""
Lección 27 - Paso 1: Media muestral y error estándar con sigma conocida
======================================================================
NUEVO EN ESTE PASO: generate_fill_sample(), sampling_metrics() y
save_figure().

La Receta
Una línea de llenado completamente sintética produce botellas de bebida.
La capacidad histórica del proceso trata la desviación estándar poblacional
como conocida: sigma = 10 ml. Se extrae una muestra de n = 36 botellas con
semilla 42 para estimar el volumen medio de llenado desconocido. El error
estándar muestral es sigma / sqrt(n).

Ejecútalo:
    uv run es/L27_Intervalo_Confianza_Z_Media/src/z_ci_mean_01_sample_standard_error.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 36
SIGMA = 10.0
MU_TRUE = 502.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) generate_fill_sample() ----------------------------------------
def generate_fill_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n llenados iid de N(mu_true, sigma). El analista no conoce mu."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)
# ------------------------------------------------------------------------------


# --- NUEVO (2) sampling_metrics() --------------------------------------------
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
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """Guarda un histograma de llenados con la media muestral y la banda de EE."""
    output_path = DIR_FIGURES / "z_ci_mean_01_sample_standard_error.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(sample, bins=10, color="#A7B0BF", edgecolor="white")
    ax.axvline(
        metrics["xbar"],
        color="#EC2661",
        linewidth=2.4,
        label=f"Media muestral = {metrics['xbar']:.2f} ml",
    )
    ax.axvspan(
        metrics["xbar"] - metrics["se"],
        metrics["xbar"] + metrics["se"],
        color="#5B8DEF",
        alpha=0.22,
        label=f"EE = {metrics['se']:.4f} ml",
    )
    ax.set_xlabel("Volumen de llenado (ml)")
    ax.set_ylabel("Conteo de botellas")
    ax.set_title("Sigma conocida: error estándar de la media muestral")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_fill_sample()
    metrics = sampling_metrics(sample)
    figure_path = save_figure(sample, metrics)

    print("================================================================")
    print("LECCIÓN 27 - PASO 1: MEDIA MUESTRAL Y ERROR ESTÁNDAR")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Sigma conocida (ml)             : {metrics['sigma']:.6f}")
    print(f"mu verdadera (oculta al analista): {MU_TRUE:.6f}")
    print(f"Media muestral xbar (ml)        : {metrics['xbar']:.6f}")
    print(f"Error estándar sigma/sqrt(n)    : {metrics['se']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

