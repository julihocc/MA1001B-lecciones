"""
Lección 45 - Paso 2: Comparaciones simultáneas Tukey HSD
========================================================
LA RECETA
Parte de tukey_hsd_01_pares_sin_ajuste.py e introduce:
    1. tukey_comparisons()  statsmodels pairwise_tukeyhsd a FWER=0.05
    2. decision_table()     diffs de medias, p ajustada, IC simultáneos
    3. save_figure()        intervalos Tukey que controlan el error familiar

Los mismos 36 tiempos de ciclo se reconstruyen con semilla 42. No se
importa ningún script anterior de la lección. Tukey responde la pregunta
por pares que un F significativo de ANOVA dejó abierta, y mantiene el
error familiar en 0.05.
"""

from itertools import combinations
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

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


def build_cycle_times(seed: int = SEED) -> pd.DataFrame:
    """Reconstruye las tres muestras sintéticas de tiempo de ciclo con semilla 42."""
    rng = np.random.default_rng(seed)
    frames = []
    for name in TREATMENTS:
        cycle_time = rng.normal(TRUE_MEANS[name], SIGMA, N_PER_GROUP)
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )
    return pd.concat(frames, ignore_index=True)


# --- NUEVO (1) tukey_comparisons() -------------------------------------------
def tukey_comparisons(sample: pd.DataFrame) -> object:
    """Ajusta Tukey HSD con tasa de error familiar 0.05."""
    return pairwise_tukeyhsd(
        endog=sample["cycle_time_seconds"],
        groups=sample["method"],
        alpha=ALPHA,
    )
# ------------------------------------------------------------------------------


# --- NUEVO (2) decision_table() ----------------------------------------------
def decision_table(tukey: object) -> pd.DataFrame:
    """Extrae diferencias de medias, p-valores ajustados e IC simultáneos."""
    unique_groups = list(tukey.groupsunique)
    pair_names = list(combinations(unique_groups, 2))
    rows = []
    for (group1, group2), diff, p_adj, bounds, reject in zip(
        pair_names,
        tukey.meandiffs,
        tukey.pvalues,
        tukey.confint,
        tukey.reject,
    ):
        rows.append(
            {
                "group1": group1,
                "group2": group2,
                "meandiff": float(diff),
                "p-adj": float(p_adj),
                "lower": float(bounds[0]),
                "upper": float(bounds[1]),
                "reject": bool(reject),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(table: pd.DataFrame) -> Path:
    """Guarda intervalos de confianza simultáneos Tukey para cada par."""
    output_path = DIR_FIGURES / "tukey_hsd_02_tukey_hsd.png"
    labels = [f"{g1} -\n{g2}" for g1, g2 in zip(table["group1"], table["group2"])]
    diffs = table["meandiff"].to_numpy(dtype=float)
    lower = table["lower"].to_numpy(dtype=float)
    upper = table["upper"].to_numpy(dtype=float)
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hlines(y, lower, upper, color="#1A2E51", linewidth=2.2)
    ax.scatter(diffs, y, color="#EC2661", zorder=3, s=42, label="Diferencia de medias")
    ax.axvline(0.0, color="#646464", linestyle="--", linewidth=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Diferencia de medias (segundos)")
    ax.set_title("Intervalos simultáneos 95% Tukey HSD")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_cycle_times()
    tukey = tukey_comparisons(sample)
    table = decision_table(tukey)
    figure_path = save_figure(table)

    print("================================================================")
    print("LECCIÓN 45 - PASO 2: TUKEY HSD")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Alpha familiar                  : {ALPHA:.2f}")
    for _, row in table.iterrows():
        print(
            f"{row['group1']} vs {row['group2']:<13}: "
            f"diff={float(row['meandiff']):.6f}, "
            f"p-adj={float(row['p-adj']):.6f}, "
            f"IC=({float(row['lower']):.6f}, {float(row['upper']):.6f}), "
            f"rechazar={bool(row['reject'])}"
        )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

