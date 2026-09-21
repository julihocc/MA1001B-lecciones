"""
Lección 44 - Paso 1: Resúmenes de tres grupos
=============================================
NUEVO EN ESTE PASO: build_cycle_times(), group_summaries() y save_figure().

La Receta
Un experimento de empaque sintético asigna 12 estaciones a cada uno de tres
métodos: Estándar, Guiado y Automatizado. El tiempo de ciclo en segundos es
la respuesta numérica. Antes de cualquier prueba F, la lección lee n, medias
y desviaciones estándar muestrales de las tres muestras independientes.

Ejecútalo:
    uv run es/L44_ANOVA_Un_Factor/src/anova_un_factor_01_resumenes_grupo.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

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
            pd.DataFrame(
                {
                    "method": name,
                    "cycle_time_seconds": cycle_time,
                }
            )
        )
    return pd.concat(frames, ignore_index=True)
# ------------------------------------------------------------------------------


# --- NUEVO (2) group_summaries() ---------------------------------------------
def group_summaries(sample: pd.DataFrame) -> pd.DataFrame:
    """Devuelve n, media y desviación estándar muestral por método."""
    rows = []
    for name in TREATMENTS:
        values = sample.loc[sample["method"] == name, "cycle_time_seconds"]
        rows.append(
            {
                "method": name,
                "n": int(values.size),
                "mean": float(values.mean()),
                "std": float(values.std(ddof=1)),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: pd.DataFrame, summary: pd.DataFrame) -> Path:
    """Guarda diagramas de caja de tiempo de ciclo con medias de grupo marcadas."""
    output_path = DIR_FIGURES / "anova_un_factor_01_resumenes_grupo.png"
    colors = ["#1A2E51", "#5B8DEF", "#EC2661"]
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]
    means = summary["mean"].to_numpy()

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    boxes = ax.boxplot(
        groups,
        positions=[1, 2, 3],
        patch_artist=True,
        widths=0.58,
        medianprops={"color": "#1A2E51", "linewidth": 1.6},
    )
    for patch, color in zip(boxes["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)
    ax.scatter([1, 2, 3], means, color="#EC2661", zorder=3, label="Media de grupo")
    ax.axhline(
        float(sample["cycle_time_seconds"].mean()),
        color="#646464",
        linestyle="--",
        linewidth=1.2,
        label="Media general",
    )
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(TREATMENTS)
    ax.set_ylabel("Tiempo de ciclo (segundos)")
    ax.set_title("Tres muestras independientes de tiempo de ciclo de empaque")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_cycle_times()
    summary = group_summaries(sample)
    figure_path = save_figure(sample, summary)
    grand_mean = float(sample["cycle_time_seconds"].mean())

    print("================================================================")
    print("LECCIÓN 44 - PASO 1: RESÚMENES DE GRUPO")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Grupos                          : {', '.join(TREATMENTS)}")
    print(f"Estaciones por método           : {N_PER_GROUP}")
    print(f"Media general                   : {grand_mean:.6f}")
    for _, row in summary.iterrows():
        print(
            f"n, media, s ({row['method']:<13}): "
            f"{int(row['n'])}, {row['mean']:.6f}, {row['std']:.6f}"
        )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

