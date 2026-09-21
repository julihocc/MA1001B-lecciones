"""
Lección 26 - Paso 2: Eficiencia y consistencia
==============================================
La Receta
Partir de point_estimation_01_unbiasedness.py e introducir:
    1. estimator_spreads()      varianza de xbar versus varianza de X1
    2. consistency_check()      n = 20 versus n = 200
    3. save_figure()            diagramas de caja de las cuatro distribuciones

xbar es más eficiente que X1 en el mismo n. Subir n de 20 a 200 reduce la
dispersión de xbar: consistencia.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
MU = 100.0
SIGMA = 15.0
N_SMALL = 20
N_LARGE = 200
N_REPS = 8_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def draw_samples(n: int, n_reps: int = N_REPS) -> np.ndarray:
    """Extrae n_reps muestras de tamaño n de N(100, 15)."""
    rng = np.random.default_rng(SEED)
    return rng.normal(loc=MU, scale=SIGMA, size=(n_reps, n))


# --- NUEVO (1) estimator_spreads() -------------------------------------------
def estimator_spreads(draws: np.ndarray) -> dict[str, float]:
    """Compara la varianza de xbar con la varianza de X1."""
    xbar = draws.mean(axis=1)
    one_obs = draws[:, 0]
    return {
        "var_xbar": float(np.var(xbar, ddof=1)),
        "var_one": float(np.var(one_obs, ddof=1)),
        "sd_xbar": float(np.std(xbar, ddof=1)),
        "sd_one": float(np.std(one_obs, ddof=1)),
        "efficiency_ratio": float(np.var(one_obs, ddof=1) / np.var(xbar, ddof=1)),
        "formula_var_xbar": SIGMA**2 / draws.shape[1],
        "formula_var_one": SIGMA**2,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) consistency_check() -------------------------------------------
def consistency_check() -> dict[str, np.ndarray]:
    """Retorna muestras de xbar para n = 20 y n = 200."""
    small = draw_samples(N_SMALL).mean(axis=1)
    large = draw_samples(N_LARGE).mean(axis=1)
    return {"n20": small, "n200": large}
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    draws_small: np.ndarray,
    means_large: np.ndarray,
) -> Path:
    """Diagrama de caja de X1, xbar n=20 y xbar n=200."""
    output_path = DIR_FIGURES / "point_estimation_02_efficiency_consistency.png"
    data = [draws_small[:, 0], draws_small.mean(axis=1), means_large]
    labels = ["X1", "xbar n=20", "xbar n=200"]
    colors = ["#EC2661", "#5B8DEF", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    boxes = ax.boxplot(data, tick_labels=labels, patch_artist=True, widths=0.55)
    for patch, color in zip(boxes["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.55)
    ax.axhline(MU, color="#646464", ls="--", lw=1.3)
    ax.set_ylabel("Valor del estimador")
    ax.set_title("xbar es más eficiente que X1; un n mayor es más consistente")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    draws_small = draw_samples(N_SMALL)
    spreads = estimator_spreads(draws_small)
    means = consistency_check()
    figure_path = save_figure(draws_small, means["n200"])
    sd_n200 = float(np.std(means["n200"], ddof=1))

    print("================================================================")
    print("LECCIÓN 26 - PASO 2: EFICIENCIA Y CONSISTENCIA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Replicaciones                   : {N_REPS:,}")
    print(f"Var(X1) de fórmula              : {spreads['formula_var_one']:.6f}")
    print(f"Var(X1) empírica                : {spreads['var_one']:.6f}")
    print(f"Var(xbar n=20) de fórmula       : {spreads['formula_var_xbar']:.6f}")
    print(f"Var(xbar n=20) empírica         : {spreads['var_xbar']:.6f}")
    print(f"Razón de eficiencia Var(X1)/Var(xbar): {spreads['efficiency_ratio']:.6f}")
    print(f"SD(xbar n=20)                   : {spreads['sd_xbar']:.6f}")
    print(f"SD(xbar n=200)                  : {sd_n200:.6f}")
    print(f"EE de fórmula n=200             : {SIGMA / np.sqrt(N_LARGE):.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

