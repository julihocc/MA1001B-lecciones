"""
Lección 44 - Paso 2: SST, SSB, SSE y cuadrados medios
=====================================================
LA RECETA
Parte de anova_un_factor_01_resumenes_grupo.py e introduce:
    1. sums_of_squares()   SST, SSB y SSE a partir de las tres muestras
    2. mean_squares()      MSB, MSE y el cociente F manual
    3. save_figure()       descomposición visual de ANOVA

Los mismos 36 tiempos de ciclo se reconstruyen con semilla 42. No se
importa ningún script anterior de la lección. La variación entre grupos se
compara con la variación dentro de grupos antes de leer un p-valor.
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PER_GROUP = 12
K_GROUPS = 3
N_TOTAL = N_PER_GROUP * K_GROUPS
TREATMENTS = ("Estándar", "Guiado", "Automatizado")
TRUE_MEANS = {"Estándar": 50.0, "Guiado": 48.0, "Automatizado": 43.0}
SIGMA = 3.2
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


# --- NUEVO (1) sums_of_squares() ---------------------------------------------
def sums_of_squares(sample: pd.DataFrame) -> dict[str, float]:
    """Descompone la variación total en piezas entre grupos y dentro de grupos."""
    values = sample["cycle_time_seconds"].to_numpy()
    grand_mean = float(values.mean())
    sst = float(np.sum((values - grand_mean) ** 2))
    ssb = 0.0
    sse = 0.0
    for name in TREATMENTS:
        group = sample.loc[
            sample["method"] == name, "cycle_time_seconds"
        ].to_numpy()
        group_mean = float(group.mean())
        ssb += N_PER_GROUP * (group_mean - grand_mean) ** 2
        sse += float(np.sum((group - group_mean) ** 2))
    return {"sst": sst, "ssb": ssb, "sse": sse, "grand_mean": grand_mean}
# ------------------------------------------------------------------------------


# --- NUEVO (2) mean_squares() ------------------------------------------------
def mean_squares(squares: dict[str, float]) -> dict[str, float]:
    """Convierte sumas de cuadrados en cuadrados medios y un F manual."""
    df_between = K_GROUPS - 1
    df_error = N_TOTAL - K_GROUPS
    df_total = N_TOTAL - 1
    msb = squares["ssb"] / df_between
    mse = squares["sse"] / df_error
    return {
        "df_between": df_between,
        "df_error": df_error,
        "df_total": df_total,
        "msb": msb,
        "mse": mse,
        "f_manual": msb / mse,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(squares: dict[str, float], ms: dict[str, float]) -> Path:
    """Guarda la descomposición SST = SSB + SSE como barras etiquetadas."""
    output_path = DIR_FIGURES / "anova_un_factor_02_tabla_ss_ms.png"
    labels = ["SSB\n(entre)", "SSE\n(dentro)", "SST\n(total)"]
    values = np.array([squares["ssb"], squares["sse"], squares["sst"]])
    colors = ["#EC2661", "#5B8DEF", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Suma de cuadrados")
    ax.set_title(
        f"Descomposición ANOVA: F = MSB/MSE = {ms['f_manual']:.3f}"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ymax = float(values.max()) * 1.18
    ax.set_ylim(0, ymax)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03 * ymax,
            f"{value:.2f}",
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
    sample = build_cycle_times()
    squares = sums_of_squares(sample)
    ms = mean_squares(squares)
    figure_path = save_figure(squares, ms)
    reconstruction = squares["ssb"] + squares["sse"]

    print("================================================================")
    print("LECCIÓN 44 - PASO 2: SS, MS Y F")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Media general                   : {squares['grand_mean']:.6f}")
    print(f"SST                             : {squares['sst']:.6f}")
    print(f"SSB (entre / factor)            : {squares['ssb']:.6f}")
    print(f"SSE (dentro / error)            : {squares['sse']:.6f}")
    print(f"SSB + SSE                       : {reconstruction:.6f}")
    print(f"gl entre                        : {int(ms['df_between'])}")
    print(f"gl error                        : {int(ms['df_error'])}")
    print(f"gl total                        : {int(ms['df_total'])}")
    print(f"MSB                             : {ms['msb']:.6f}")
    print(f"MSE                             : {ms['mse']:.6f}")
    print(f"F manual = MSB/MSE              : {ms['f_manual']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

