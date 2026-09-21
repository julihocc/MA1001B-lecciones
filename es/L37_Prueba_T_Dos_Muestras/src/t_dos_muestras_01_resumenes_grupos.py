"""
Lección 37 - Paso 1: Dos muestras independientes y resúmenes de grupo
=====================================================================
NUEVO EN ESTE PASO: build_shift_samples(), group_summaries() y save_figure().

La Receta
Un almacén completamente sintético registra tiempos de recolección de dos
turnos muestreados de forma independiente: n1 = 30 en el turno A y n2 = 32
en el turno B. Cada grupo tiene su propia media y desviación estándar
muestral. Las muestras no están pareadas.

Ejecútalo:
    uv run es/L37_Prueba_T_Dos_Muestras/src/t_dos_muestras_01_resumenes_grupos.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_A = 30
N_B = 32
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_shift_samples() -----------------------------------------
def build_shift_samples(seed: int = SEED) -> dict[str, np.ndarray]:
    """Extrae tiempos de recolección sintéticos independientes y años de experiencia."""
    rng = np.random.default_rng(seed)
    times_a = rng.normal(loc=48.0, scale=6.0, size=N_A)
    times_b = rng.normal(loc=52.5, scale=7.5, size=N_B)
    experience_a = rng.normal(loc=4.5, scale=1.0, size=N_A)
    experience_b = rng.normal(loc=2.0, scale=0.8, size=N_B)
    return {
        "times_a": times_a,
        "times_b": times_b,
        "experience_a": experience_a,
        "experience_b": experience_b,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) group_summaries() ---------------------------------------------
def group_summaries(times_a: np.ndarray, times_b: np.ndarray) -> dict[str, float]:
    """Devuelve n, media y s muestral de cada turno independiente."""
    return {
        "n_a": float(times_a.size),
        "n_b": float(times_b.size),
        "mean_a": float(np.mean(times_a)),
        "mean_b": float(np.mean(times_b)),
        "s_a": float(np.std(times_a, ddof=1)),
        "s_b": float(np.std(times_b, ddof=1)),
        "mean_diff": float(np.mean(times_a) - np.mean(times_b)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(times_a: np.ndarray, times_b: np.ndarray) -> Path:
    """Guarda diagramas de caja lado a lado de los dos turnos independientes."""
    output_path = DIR_FIGURES / "t_dos_muestras_01_resumenes_grupos.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    box = ax.boxplot(
        [times_a, times_b],
        tick_labels=["Turno A", "Turno B"],
        patch_artist=True,
        widths=0.55,
    )
    colors = ["#5B8DEF", "#EC2661"]
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
        patch.set_edgecolor("#1A2E51")
    ax.set_ylabel("Tiempo de recolección (minutos)")
    ax.set_title("Dos turnos independientes, nA = 30 y nB = 32")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    samples = build_shift_samples()
    summary = group_summaries(samples["times_a"], samples["times_b"])
    figure_path = save_figure(samples["times_a"], samples["times_b"])

    print("================================================================")
    print("LECCIÓN 37 - PASO 1: RESÚMENES DE DOS GRUPOS INDEPENDIENTES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Tamaño de muestra turno A nA    : {int(summary['n_a'])}")
    print(f"Tamaño de muestra turno B nB    : {int(summary['n_b'])}")
    print(f"Media turno A (minutos)         : {summary['mean_a']:.6f}")
    print(f"Media turno B (minutos)         : {summary['mean_b']:.6f}")
    print(f"s muestral turno A              : {summary['s_a']:.6f}")
    print(f"s muestral turno B              : {summary['s_b']:.6f}")
    print(f"Diferencia de medias A menos B  : {summary['mean_diff']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

