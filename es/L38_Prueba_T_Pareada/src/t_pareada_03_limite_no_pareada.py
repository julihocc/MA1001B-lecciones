"""
Lección 38 - Paso 3: El análisis no pareado de datos pareados ignora el emparejamiento
======================================================================================
NUEVO EN ESTE PASO: unpaired_t_test(), compare_procedures() y save_figure().

La Receta
Partir de t_pareada_02_prueba_pareada.py e introducir:
    1. unpaired_t_test()       t de dos muestras que finge que los tiempos son independientes
    2. compare_procedures()    valor p pareado frente a valor p no pareado
    3. save_figure()           los dos valores p contra alfa = 0.05

Las estaciones están emparejadas. Tratar antes y después como muestras
independientes descarta la correlación e infla el error estándar. Esa es la
prueba incorrecta para datos pareados.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PAIRS = 25
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_pairs(seed: int = SEED) -> dict[str, np.ndarray]:
    """Extrae 25 tiempos de manejo emparejados antes-después en minutos."""
    rng = np.random.default_rng(seed)
    before = rng.normal(loc=55.0, scale=8.0, size=N_PAIRS)
    after = before - 3.2 + rng.normal(loc=0.0, scale=2.2, size=N_PAIRS)
    return {"before": before, "after": after, "diff": before - after}


# --- NUEVO (1) unpaired_t_test() ---------------------------------------------
def unpaired_t_test(before: np.ndarray, after: np.ndarray) -> dict[str, float]:
    """t de Welch de dos muestras que ignora incorrectamente el emparejamiento."""
    test = stats.ttest_ind(before, after, equal_var=False)
    se = float(
        np.sqrt(
            np.var(before, ddof=1) / before.size
            + np.var(after, ddof=1) / after.size
        )
    )
    return {
        "t_stat": float(test.statistic),
        "p_value": float(test.pvalue),
        "df": float(test.df),
        "se": se,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_procedures() ------------------------------------------
def compare_procedures(pairs: dict[str, np.ndarray]) -> dict[str, float]:
    """Coloca la t pareada correcta junto a la t no pareada incorrecta."""
    paired = stats.ttest_rel(pairs["before"], pairs["after"])
    unpaired = unpaired_t_test(pairs["before"], pairs["after"])
    se_paired = float(
        np.std(pairs["diff"], ddof=1) / np.sqrt(pairs["diff"].size)
    )
    return {
        "corr": float(np.corrcoef(pairs["before"], pairs["after"])[0, 1]),
        "paired_t": float(paired.statistic),
        "paired_p": float(paired.pvalue),
        "paired_se": se_paired,
        "unpaired_t": unpaired["t_stat"],
        "unpaired_p": unpaired["p_value"],
        "unpaired_se": unpaired["se"],
        "unpaired_df": unpaired["df"],
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(comparison: dict[str, float]) -> Path:
    """Compara valores p pareados y no pareados sobre los mismos datos emparejados."""
    output_path = DIR_FIGURES / "t_pareada_03_limite_no_pareada.png"
    labels = ["t pareada\n(correcta)", "t no pareada\n(ignora el emparejamiento)"]
    values = [comparison["paired_p"], comparison["unpaired_p"]]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=["#1A2E51", "#EC2661"], width=0.55)
    ax.axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.4,
               label="alfa = 0.05")
    ax.set_ylabel("Valor p bilateral")
    ax.set_title("El análisis no pareado de datos pareados ignora el emparejamiento")
    ax.set_ylim(0, 0.20)
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.006,
            f"{value:.4g}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    pairs = build_pairs()
    comparison = compare_procedures(pairs)
    figure_path = save_figure(comparison)
    paired_decision = (
        "rechazar H0" if comparison["paired_p"] < ALPHA else "no rechazar H0"
    )
    unpaired_decision = (
        "rechazar H0" if comparison["unpaired_p"] < ALPHA else "no rechazar H0"
    )

    print("================================================================")
    print("LECCIÓN 38 - PASO 3: LÍMITE NO PAREADO")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Correlación antes con después   : {comparison['corr']:.6f}")
    print(f"EE pareado de la diferencia media: {comparison['paired_se']:.6f}")
    print(f"EE de Welch no pareado          : {comparison['unpaired_se']:.6f}")
    print(f"Estadístico t pareado           : {comparison['paired_t']:.6f}")
    print(f"Estadístico t no pareado        : {comparison['unpaired_t']:.6f}")
    print(f"Valor p bilateral pareado       : {comparison['paired_p']:.6e}")
    print(f"Valor p bilateral no pareado    : {comparison['unpaired_p']:.6f}")
    print(f"Decisión pareada                : {paired_decision}")
    print(f"Decisión no pareada             : {unpaired_decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

