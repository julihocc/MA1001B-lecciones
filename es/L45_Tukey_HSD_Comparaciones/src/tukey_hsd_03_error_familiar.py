"""
Lección 45 - Paso 3: Las pruebas sin ajuste inflan el error familiar
===================================================================
LA RECETA
Parte de tukey_hsd_02_tukey_hsd.py e introduce:
    1. simulate_null_experiments()  5000 estudios de tres grupos bajo medias iguales
    2. familywise_rates()           tasas de rechazo t sin ajuste frente a Tukey
    3. save_figure()                compara FWER empírico con alpha=0.05

Límite: las pruebas t por pares sin corrección inflan el error familiar.
Bajo la nula global, al menos un par sin ajuste rechaza más a menudo que el
5 por ciento. Tukey mantiene esa tasa familiar cerca del alpha anunciado.
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PER_GROUP = 12
K_GROUPS = 3
N_TOTAL = K_GROUPS * N_PER_GROUP
TREATMENTS = ("Estándar", "Guiado", "Automatizado")
NULL_MEAN = 48.0
SIGMA = 3.2
ALPHA = 0.05
N_SIMULATIONS = 5000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) simulate_null_experiments() -----------------------------------
def simulate_null_experiments(seed: int = SEED) -> pd.DataFrame:
    """Simula 5000 experimentos en los que las tres medias verdaderas son iguales."""
    rng = np.random.default_rng(seed)
    data = rng.normal(
        NULL_MEAN, SIGMA, size=(N_SIMULATIONS, K_GROUPS, N_PER_GROUP)
    )
    means = data.mean(axis=2)
    group_vars = data.var(axis=2, ddof=1)
    df_pair = 2 * N_PER_GROUP - 2
    t_crit = float(stats.t.ppf(1.0 - ALPHA / 2.0, df_pair))
    pairs = ((0, 1), (0, 2), (1, 2))
    unadjusted_any = np.zeros(N_SIMULATIONS, dtype=bool)
    for i, j in pairs:
        pooled = (
            (N_PER_GROUP - 1) * group_vars[:, i]
            + (N_PER_GROUP - 1) * group_vars[:, j]
        ) / df_pair
        se_diff = np.sqrt(pooled * (2.0 / N_PER_GROUP))
        t_stat = (means[:, i] - means[:, j]) / se_diff
        unadjusted_any |= np.abs(t_stat) > t_crit

    sse = np.sum((data - means[:, :, None]) ** 2, axis=(1, 2))
    mse = sse / (N_TOTAL - K_GROUPS)
    q_crit = float(
        stats.studentized_range.ppf(1.0 - ALPHA, K_GROUPS, N_TOTAL - K_GROUPS)
    )
    hsd = q_crit * np.sqrt(mse / N_PER_GROUP)
    tukey_any = np.zeros(N_SIMULATIONS, dtype=bool)
    for i, j in pairs:
        tukey_any |= np.abs(means[:, i] - means[:, j]) > hsd

    labels = np.repeat(np.array(TREATMENTS), N_PER_GROUP)
    example = pairwise_tukeyhsd(data[0].ravel(), labels, alpha=ALPHA)
    return pd.DataFrame(
        {
            "unadjusted_any_reject": unadjusted_any,
            "tukey_any_reject": tukey_any,
        }
    ), example
# ------------------------------------------------------------------------------


# --- NUEVO (2) familywise_rates() --------------------------------------------
def familywise_rates(results: pd.DataFrame) -> dict[str, float]:
    """Estima tasas de error familiar a partir de las simulaciones nulas."""
    return {
        "unadjusted_fwer": float(results["unadjusted_any_reject"].mean()),
        "tukey_fwer": float(results["tukey_any_reject"].mean()),
        "n_simulations": float(N_SIMULATIONS),
        "target_alpha": ALPHA,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(rates: dict[str, float]) -> Path:
    """Compara el error familiar empírico con el alpha anunciado."""
    output_path = DIR_FIGURES / "tukey_hsd_03_error_familiar.png"
    labels = ["t por pares\nsin ajuste", "Tukey HSD", "Alpha\nanunciado"]
    values = [
        rates["unadjusted_fwer"],
        rates["tukey_fwer"],
        rates["target_alpha"],
    ]
    colors = ["#EC2661", "#1A2E51", "#5B8DEF"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.2)
    ax.set_ylabel("Tasa de error familiar")
    ax.set_title("Las pruebas por pares sin ajuste inflan el error familiar")
    ax.set_ylim(0, 0.22)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    results, example = simulate_null_experiments()
    rates = familywise_rates(results)
    figure_path = save_figure(rates)
    example_rejects = int(np.sum(example.reject))

    print("================================================================")
    print("LECCIÓN 45 - PASO 3: LÍMITE DE ERROR FAMILIAR")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Experimentos nulos simulados    : {int(rates['n_simulations'])}")
    print(f"Medias verdaderas bajo H0       : todas iguales a {NULL_MEAN:.1f}")
    print(f"Alpha anunciado                 : {rates['target_alpha']:.6f}")
    print(f"FWER por pares sin ajuste       : {rates['unadjusted_fwer']:.6f}")
    print(f"FWER Tukey HSD                  : {rates['tukey_fwer']:.6f}")
    print(f"Rechazos Tukey nulos de ejemplo : {example_rejects}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

