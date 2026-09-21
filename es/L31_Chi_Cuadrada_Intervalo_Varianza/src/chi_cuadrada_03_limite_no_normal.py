"""
Lección 31 - Paso 3: Datos no normales invalidan el intervalo chi-cuadrada
=========================================================================
NUEVO EN ESTE PASO: coverage_normal(), coverage_exponential() y
save_figure().

La Receta
Partir de chi_cuadrada_02_intervalo_varianza.py e introducir:
    1. coverage_normal()       cobertura con semilla 42 del intervalo chi-cuadrada
    2. coverage_exponential()  la misma fórmula sobre ciclos sesgados a la derecha
    3. save_figure()           contrastar las dos tasas empíricas de cobertura

Límite: el intervalo chi-cuadrada para sigma^2 supone una población normal.
Cuando los tiempos de ciclo son exponenciales, la misma fórmula ya no cubre
cerca del 95% de las veces.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 20
DF = N - 1
N_REPS = 5000
MU_TRUE = 12.0
SIGMA_TRUE = 3.0
EXP_SCALE = 12.0
CONFIDENCE = 0.95
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def chi_square_bounds(s2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve los límites chi-cuadrada para una o muchas varianzas muestrales."""
    chi2_l = float(stats.chi2.ppf(0.025, DF))
    chi2_u = float(stats.chi2.ppf(0.975, DF))
    return DF * s2 / chi2_u, DF * s2 / chi2_l


# --- NUEVO (1) coverage_normal() ---------------------------------------------
def coverage_normal(n_reps: int = N_REPS) -> dict[str, float]:
    """Cobertura empírica cuando el supuesto de normalidad es verdadero."""
    rng = np.random.default_rng(SEED)
    samples = rng.normal(MU_TRUE, SIGMA_TRUE, size=(n_reps, N))
    s2 = np.var(samples, axis=1, ddof=1)
    lower, upper = chi_square_bounds(s2)
    true_var = SIGMA_TRUE ** 2
    return {
        "n_reps": float(n_reps),
        "true_var": true_var,
        "coverage": float(np.mean((lower <= true_var) & (true_var <= upper))),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) coverage_exponential() ----------------------------------------
def coverage_exponential(n_reps: int = N_REPS) -> dict[str, float]:
    """Cobertura empírica cuando los tiempos de ciclo son exponenciales, por tanto sesgados."""
    rng = np.random.default_rng(SEED)
    samples = rng.exponential(scale=EXP_SCALE, size=(n_reps, N))
    s2 = np.var(samples, axis=1, ddof=1)
    lower, upper = chi_square_bounds(s2)
    true_var = EXP_SCALE ** 2
    return {
        "n_reps": float(n_reps),
        "true_var": true_var,
        "coverage": float(np.mean((lower <= true_var) & (true_var <= upper))),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    normal_cov: float,
    exponential_cov: float,
) -> Path:
    """Contrasta la cobertura nominal del 95% con las dos tasas simuladas."""
    output_path = DIR_FIGURES / "chi_cuadrada_03_limite_no_normal.png"
    labels = ["Ciclos normales", "Ciclos exponenciales"]
    values = [normal_cov, exponential_cov]
    colors = ["#1A2E51", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.axhline(0.95, color="#5B8DEF", linestyle="--", linewidth=1.8,
               label="Nominal 95%")
    ax.set_ylabel("Cobertura empírica")
    ax.set_title("Los datos no normales invalidan el intervalo chi-cuadrada")
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03,
            f"{value:.3f}",
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
    normal = coverage_normal()
    exponential = coverage_exponential()
    figure_path = save_figure(normal["coverage"], exponential["coverage"])

    print("================================================================")
    print("LECCIÓN 31 - PASO 3: LÍMITE DE COBERTURA NO NORMAL")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra n             : {N}")
    print(f"Replicaciones                   : {N_REPS}")
    print(f"Sigma^2 verdadera normal        : {normal['true_var']:.6f}")
    print(f"Cobertura empírica normal       : {normal['coverage']:.6f}")
    print(f"Sigma^2 verdadera exponencial   : {exponential['true_var']:.6f}")
    print(f"Cobertura empírica exponencial  : {exponential['coverage']:.6f}")
    print("Límite                         : los datos no normales invalidan el IC chi-cuadrada")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

