"""
Lección 44 - Paso 3: La prueba F no nombra un par
=================================================
LA RECETA
Parte de anova_un_factor_02_tabla_ss_ms.py e introduce:
    1. f_oneway_test()     estadístico F de scipy y p-valor
    2. pairwise_mean_gaps()  tres diferencias de medias sin prueba de par
    3. save_figure()         F observada sobre la distribución F

Límite: un F significativo no dice qué par difiere. La Lección 45 organiza
esa pregunta siguiente como Tukey HSD.
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_PER_GROUP = 12
K_GROUPS = 3
N_TOTAL = N_PER_GROUP * K_GROUPS
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


def anova_pieces(sample: pd.DataFrame) -> dict[str, float]:
    """Devuelve las piezas de la tabla ANOVA manual usadas para checar scipy."""
    values = sample["cycle_time_seconds"].to_numpy()
    grand_mean = float(values.mean())
    ssb = 0.0
    sse = 0.0
    for name in TREATMENTS:
        group = sample.loc[
            sample["method"] == name, "cycle_time_seconds"
        ].to_numpy()
        group_mean = float(group.mean())
        ssb += N_PER_GROUP * (group_mean - grand_mean) ** 2
        sse += float(np.sum((group - group_mean) ** 2))
    df_between = K_GROUPS - 1
    df_error = N_TOTAL - K_GROUPS
    msb = ssb / df_between
    mse = sse / df_error
    return {
        "f_manual": msb / mse,
        "df_between": df_between,
        "df_error": df_error,
    }


# --- NUEVO (1) f_oneway_test() -----------------------------------------------
def f_oneway_test(sample: pd.DataFrame) -> dict[str, float]:
    """Calcula scipy.stats.f_oneway y el valor crítico F."""
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]
    f_stat, p_value = stats.f_oneway(*groups)
    df_between = K_GROUPS - 1
    df_error = N_TOTAL - K_GROUPS
    f_crit = float(stats.f.ppf(1.0 - ALPHA, df_between, df_error))
    return {
        "f_stat": float(f_stat),
        "p_value": float(p_value),
        "f_crit": f_crit,
        "df_between": df_between,
        "df_error": df_error,
        "reject": float(f_stat) > f_crit,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) pairwise_mean_gaps() ------------------------------------------
def pairwise_mean_gaps(sample: pd.DataFrame) -> dict[str, float]:
    """Reporta las tres diferencias de medias sin contrastar ningún par."""
    means = {
        name: float(
            sample.loc[sample["method"] == name, "cycle_time_seconds"].mean()
        )
        for name in TREATMENTS
    }
    return {
        "standard_minus_guided": means["Estándar"] - means["Guiado"],
        "standard_minus_automated": means["Estándar"] - means["Automatizado"],
        "guided_minus_automated": means["Guiado"] - means["Automatizado"],
        "mean_standard": means["Estándar"],
        "mean_guided": means["Guiado"],
        "mean_automated": means["Automatizado"],
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(test: dict[str, float], gaps: dict[str, float]) -> Path:
    """Marca la F observada en la densidad nula F y muestra brechas sin etiquetar."""
    output_path = DIR_FIGURES / "anova_un_factor_03_limite_prueba_f.png"
    x = np.linspace(0.0, 20.0, 400)
    y = stats.f.pdf(x, test["df_between"], test["df_error"])

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))
    axes[0].plot(x, y, color="#1A2E51", linewidth=2.0)
    axes[0].axvline(
        test["f_stat"],
        color="#EC2661",
        linewidth=2.0,
        label=f"F observada = {test['f_stat']:.3f}",
    )
    axes[0].axvline(
        test["f_crit"],
        color="#5B8DEF",
        linestyle="--",
        linewidth=1.5,
        label=f"F crítica = {test['f_crit']:.3f}",
    )
    axes[0].fill_between(
        x[x >= test["f_crit"]],
        y[x >= test["f_crit"]],
        color="#EC2661",
        alpha=0.18,
    )
    axes[0].set_xlabel("F")
    axes[0].set_ylabel("Densidad")
    axes[0].set_title("F significativa, sigue siendo una prueba ómnibus")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    gap_labels = [
        "Estándar\n- Guiado",
        "Estándar\n- Automatizado",
        "Guiado\n- Automatizado",
    ]
    gap_values = [
        gaps["standard_minus_guided"],
        gaps["standard_minus_automated"],
        gaps["guided_minus_automated"],
    ]
    colors = ["#5B8DEF", "#EC2661", "#1A2E51"]
    bars = axes[1].bar(gap_labels, gap_values, color=colors, width=0.62)
    axes[1].axhline(0.0, color="#646464", linewidth=1.0)
    axes[1].set_ylabel("Diferencia de medias (segundos)")
    axes[1].set_title("F no identifica qué par difiere")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, gap_values):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.15,
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
    pieces = anova_pieces(sample)
    test = f_oneway_test(sample)
    gaps = pairwise_mean_gaps(sample)
    figure_path = save_figure(test, gaps)

    print("================================================================")
    print("LECCIÓN 44 - PASO 3: LÍMITE DE LA PRUEBA F")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"F manual                        : {pieces['f_manual']:.6f}")
    print(f"F de scipy f_oneway             : {test['f_stat']:.6f}")
    print(f"p-valor                         : {test['p_value']:.6e}")
    print(f"F crítica (alpha=0.05)          : {test['f_crit']:.6f}")
    print(f"Rechazar H0: medias iguales     : {bool(test['reject'])}")
    print(f"Media Estándar                  : {gaps['mean_standard']:.6f}")
    print(f"Media Guiado                    : {gaps['mean_guided']:.6f}")
    print(f"Media Automatizado              : {gaps['mean_automated']:.6f}")
    print(
        "Estándar - Guiado               : "
        f"{gaps['standard_minus_guided']:.6f}"
    )
    print(
        "Estándar - Automatizado         : "
        f"{gaps['standard_minus_automated']:.6f}"
    )
    print(
        "Guiado - Automatizado           : "
        f"{gaps['guided_minus_automated']:.6f}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

