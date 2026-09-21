"""
Lección 38 - Paso 1: Diferencias pareadas de tiempos antes-después
==================================================================
NUEVO EN ESTE PASO: build_pairs(), difference_summaries() y save_figure().

La Receta
Una celda de empaque completamente sintética registra el tiempo de manejo en
las mismas 25 estaciones antes y después de un cambio de layout. La unidad
observacional es la estación, así que los datos son 25 diferencias pareadas
d = antes - después, no dos muestras independientes.

Ejecútalo:
    uv run es/L38_Prueba_T_Pareada/src/t_pareada_01_diferencias.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PAIRS = 25
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_pairs() -------------------------------------------------
def build_pairs(seed: int = SEED) -> dict[str, np.ndarray]:
    """Extrae 25 tiempos de manejo emparejados antes-después en minutos."""
    rng = np.random.default_rng(seed)
    before = rng.normal(loc=55.0, scale=8.0, size=N_PAIRS)
    after = before - 3.2 + rng.normal(loc=0.0, scale=2.2, size=N_PAIRS)
    return {"before": before, "after": after, "diff": before - after}
# ------------------------------------------------------------------------------


# --- NUEVO (2) difference_summaries() ----------------------------------------
def difference_summaries(pairs: dict[str, np.ndarray]) -> dict[str, float]:
    """Resume antes, después y las diferencias emparejadas."""
    before = pairs["before"]
    after = pairs["after"]
    diff = pairs["diff"]
    return {
        "n": float(diff.size),
        "mean_before": float(np.mean(before)),
        "mean_after": float(np.mean(after)),
        "s_before": float(np.std(before, ddof=1)),
        "s_after": float(np.std(after, ddof=1)),
        "mean_diff": float(np.mean(diff)),
        "s_diff": float(np.std(diff, ddof=1)),
        "corr": float(np.corrcoef(before, after)[0, 1]),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(pairs: dict[str, np.ndarray]) -> Path:
    """Dibuja líneas emparejadas antes-después para las 25 estaciones."""
    output_path = DIR_FIGURES / "t_pareada_01_diferencias.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    x = np.array([0, 1])
    for before, after in zip(pairs["before"], pairs["after"]):
        color = "#EC2661" if before > after else "#5B8DEF"
        ax.plot(x, [before, after], color=color, alpha=0.55, linewidth=1.2)
        ax.scatter(x, [before, after], color=color, s=18, zorder=3)
    ax.set_xticks([0, 1], ["Antes", "Después"])
    ax.set_ylabel("Tiempo de manejo (minutos)")
    ax.set_title("25 estaciones emparejadas: antes frente a después")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    pairs = build_pairs()
    summary = difference_summaries(pairs)
    figure_path = save_figure(pairs)

    print("================================================================")
    print("LECCIÓN 38 - PASO 1: DIFERENCIAS PAREADAS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Número de pares emparejados     : {int(summary['n'])}")
    print(f"Media antes (minutos)           : {summary['mean_before']:.6f}")
    print(f"Media después (minutos)         : {summary['mean_after']:.6f}")
    print(f"s muestral antes                : {summary['s_before']:.6f}")
    print(f"s muestral después              : {summary['s_after']:.6f}")
    print(f"Media de d = antes-después      : {summary['mean_diff']:.6f}")
    print(f"s muestral de las diferencias   : {summary['s_diff']:.6f}")
    print(f"Correlación antes con después   : {summary['corr']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

