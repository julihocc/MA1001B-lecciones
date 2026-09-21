"""
Lección 34 - Paso 1: Estadístico z para una media con sigma conocida
====================================================================
NUEVO EN ESTE PASO: generate_delivery_sample(), z_statistic() y
save_figure().

La Receta
Un proceso de última milla completamente sintético trata sigma = 6 minutos
como conocida. Una muestra de n = 40 entregas con semilla 42 se prueba
contra H0: mu = 80 minutos. El estadístico z es (xbarra - mu0) / (sigma / sqrt(n)).

Ejecútalo:
    uv run es/L34_Prueba_Z_Una_Media/src/prueba_z_media_01_estadistico_z.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 40
MU0 = 80.0
MU_TRUE = 82.0
SIGMA = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) generate_delivery_sample() ------------------------------------
def generate_delivery_sample(seed: int = SEED) -> np.ndarray:
    """Extrae n tiempos de entrega iid. El analista conoce sigma, no mu."""
    rng = np.random.default_rng(seed)
    return rng.normal(loc=MU_TRUE, scale=SIGMA, size=N)
# ------------------------------------------------------------------------------


# --- NUEVO (2) z_statistic() -------------------------------------------------
def z_statistic(sample: np.ndarray) -> dict[str, float]:
    """Calcula xbarra, EE y el estadístico z bajo H0: mu = 80."""
    xbar = float(np.mean(sample))
    se = SIGMA / np.sqrt(N)
    z = (xbar - MU0) / se
    return {
        "n": float(N),
        "mu0": MU0,
        "sigma": SIGMA,
        "xbar": xbar,
        "se": float(se),
        "z": float(z),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: np.ndarray, metrics: dict[str, float]) -> Path:
    """Guarda un histograma de entregas con xbarra y el valor de H0."""
    output_path = DIR_FIGURES / "prueba_z_media_01_estadistico_z.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(sample, bins=10, color="#A7B0BF", edgecolor="white")
    ax.axvline(metrics["xbar"], color="#EC2661", linewidth=2.4,
               label=f"xbarra = {metrics['xbar']:.2f} min")
    ax.axvline(MU0, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label=f"H0 mu = {MU0:.0f} min")
    ax.set_xlabel("Tiempo de entrega (minutos)")
    ax.set_ylabel("Conteo de entregas")
    ax.set_title("Estadístico z de n = 40 entregas, sigma conocida")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = generate_delivery_sample()
    metrics = z_statistic(sample)
    figure_path = save_figure(sample, metrics)

    print("================================================================")
    print("LECCIÓN 34 - PASO 1: ESTADÍSTICO Z")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print("H0                             : mu = 80")
    print("H1                             : mu > 80")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Sigma conocida (min)            : {SIGMA:.6f}")
    print(f"Media muestral xbarra (min)     : {metrics['xbar']:.6f}")
    print(f"EE = sigma/sqrt(n)              : {metrics['se']:.6f}")
    print(f"z = (xbarra - 80) / EE          : {metrics['z']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

