"""
Lección 46 - Paso 1: Residuos de ANOVA y normalidad
===================================================
NUEVO EN ESTE PASO: build_cycle_times(), anova_residuals() y save_figure().

La Receta
El mismo experimento sintético de empaque tiene tres métodos y n=12
estaciones cada uno. ANOVA de un factor supone que los residuos son
aproximadamente normales. Este paso forma e_ij = y_ij - ybarra_i e
inspecciona su histograma.

Ejecútalo:
    uv run es/L46_Diagnostico_Supuestos_ANOVA/src/diagnostico_anova_01_normalidad_residuos.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PER_GROUP = 12
TREATMENTS = ("Estándar", "Guiado", "Automatizado")
TRUE_MEANS = {"Estándar": 50.0, "Guiado": 48.0, "Automatizado": 43.0}
SIGMA = 3.2
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_cycle_times() -------------------------------------------
def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """Simula 12 tiempos de ciclo para cada método de empaque con semilla 42."""
    rng = np.random.default_rng(seed)
    frames = []
    for name in TREATMENTS:
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )
    return pd.concat(frames, ignore_index=True)
# ------------------------------------------------------------------------------


# --- NUEVO (2) anova_residuals() ---------------------------------------------
def anova_residuals(sample: pd.DataFrame) -> pd.DataFrame:
    """Forma residuos e = y - media de grupo para cada método de empaque."""
    fitted = sample.groupby("method")["cycle_time_seconds"].transform("mean")
    out = sample.copy()
    out["fitted"] = fitted
    out["residual"] = out["cycle_time_seconds"] - fitted
    return out
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(diagnosed: pd.DataFrame) -> Path:
    """Guarda un histograma de residuos con una curva de referencia normal."""
    output_path = DIR_FIGURES / "diagnostico_anova_01_normalidad_residuos.png"
    residuals = diagnosed["residual"].to_numpy()
    x = np.linspace(residuals.min() - 1.0, residuals.max() + 1.0, 200)
    density = stats.norm.pdf(x, loc=0.0, scale=float(residuals.std(ddof=1)))

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(
        residuals,
        bins=10,
        color="#5B8DEF",
        edgecolor="white",
        density=True,
        alpha=0.85,
        label="Residuos",
    )
    ax.plot(x, density, color="#EC2661", linewidth=2.2, label="Referencia normal")
    ax.axvline(0.0, color="#1A2E51", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Residuo (segundos)")
    ax.set_ylabel("Densidad")
    ax.set_title("Los residuos de ANOVA se ven aproximadamente normales")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_cycle_times()
    diagnosed = anova_residuals(sample)
    residuals = diagnosed["residual"].to_numpy()
    shapiro = stats.shapiro(residuals)
    figure_path = save_figure(diagnosed)

    print("================================================================")
    print("LECCIÓN 46 - PASO 1: NORMALIDAD DE RESIDUOS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Conteo de residuos              : {residuals.size}")
    print(f"Media de residuos               : {float(residuals.mean()):.6f}")
    print(f"DE de residuos                  : {float(residuals.std(ddof=1)):.6f}")
    print(f"Shapiro-Wilk W                  : {float(shapiro.statistic):.6f}")
    print(f"p-valor Shapiro-Wilk            : {float(shapiro.pvalue):.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

