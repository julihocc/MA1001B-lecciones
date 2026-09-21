"""
Lección 45 - Paso 1: Pruebas t por pares sin ajuste
===================================================
NUEVO EN ESTE PASO: build_cycle_times(), unadjusted_pairwise() y
save_figure().

La Receta
El mismo experimento sintético de empaque tiene tres métodos y n=12
estaciones cada uno. Tras un F de ANOVA significativo, tres pruebas t por
pares resultan tentadoras. Este paso corre esas pruebas sin ajuste y
registra cada p-valor, antes de cualquier corrección familiar.

Ejecútalo:
    uv run es/L45_Tukey_HSD_Comparaciones/src/tukey_hsd_01_pares_sin_ajuste.py
"""

from itertools import combinations
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
ALPHA = 0.05
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


# --- NUEVO (2) unadjusted_pairwise() -----------------------------------------
def unadjusted_pairwise(sample: pd.DataFrame) -> pd.DataFrame:
    """Corre cada prueba t de dos muestras a alpha=0.05 sin corrección de multiplicidad."""
    rows = []
    for left, right in combinations(TREATMENTS, 2):
        a = sample.loc[sample["method"] == left, "cycle_time_seconds"]
        b = sample.loc[sample["method"] == right, "cycle_time_seconds"]
        t_stat, p_value = stats.ttest_ind(a, b, equal_var=True)
        diff = float(a.mean() - b.mean())
        rows.append(
            {
                "pair": f"{left} - {right}",
                "mean_diff": diff,
                "t_stat": float(t_stat),
                "p_value": float(p_value),
                "reject": float(p_value) < ALPHA,
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(pairs: pd.DataFrame) -> Path:
    """Guarda diferencias de medias por pares sin ajuste como barras etiquetadas."""
    output_path = DIR_FIGURES / "tukey_hsd_01_pares_sin_ajuste.png"
    colors = ["#5B8DEF", "#EC2661", "#1A2E51"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(pairs["pair"], pairs["mean_diff"], color=colors, width=0.62)
    ax.axhline(0.0, color="#646464", linewidth=1.0)
    ax.set_ylabel("Diferencia de medias (segundos)")
    ax.set_title("Diferencias por pares sin ajuste")
    ax.set_ylim(0, float(pairs["mean_diff"].max()) * 1.38)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, p_value, reject in zip(bars, pairs["p_value"], pairs["reject"]):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.22,
            f"p={p_value:.4f}\n{'rechazar' if reject else 'retener'}",
            ha="center",
            fontsize=8,
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_cycle_times()
    pairs = unadjusted_pairwise(sample)
    figure_path = save_figure(pairs)

    print("================================================================")
    print("LECCIÓN 45 - PASO 1: t POR PARES SIN AJUSTE")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Número de pruebas por pares     : {len(pairs)}")
    print(f"Alpha sin ajuste                : {ALPHA:.2f}")
    for _, row in pairs.iterrows():
        print(
            f"{row['pair']:<28} : diff={row['mean_diff']:.6f}, "
            f"t={row['t_stat']:.6f}, p={row['p_value']:.6f}, "
            f"rechazar={bool(row['reject'])}"
        )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

