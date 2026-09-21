"""
Lección 46 - Paso 3: n igual no rescata una heterocedasticidad fuerte
=====================================================================
LA RECETA
Parte de diagnostico_anova_02_levene_homocedasticidad.py e introduce:
    1. build_heterogeneous()  n igual, varianzas fuertemente desiguales
    2. broken_anova()         Levene más F cuando falla el supuesto de dispersión
    3. save_figure()          abanico residual del método de alta varianza

Límite: ANOVA con n igual no es inmune a una desigualdad fuerte de
varianzas. Un F significativo puede aparecer cuando un grupo es mucho más
ruidoso que los otros, de modo que la comparación de medias ya no es una
historia limpia de ANOVA.
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
TREATMENTS = ("Estándar", "Guiado", "Automatizado")
HETERO_MEANS = {"Estándar": 50.0, "Guiado": 50.0, "Automatizado": 56.0}
HETERO_SIGMAS = {"Estándar": 1.6, "Guiado": 1.8, "Automatizado": 12.0}
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_heterogeneous() -----------------------------------------
def build_heterogeneous(seed: int = SEED) -> pd.DataFrame:
    """Construye tres muestras de n igual con un grupo Automatizado mucho más ruidoso."""
    rng = np.random.default_rng(seed)
    frames = []
    for name in TREATMENTS:
        cycle_time = rng.normal(
            HETERO_MEANS[name], HETERO_SIGMAS[name], N_PER_GROUP
        )
        frames.append(
            pd.DataFrame({"method": name, "cycle_time_seconds": cycle_time})
        )
    sample = pd.concat(frames, ignore_index=True)
    fitted = sample.groupby("method")["cycle_time_seconds"].transform("mean")
    sample["fitted"] = fitted
    sample["residual"] = sample["cycle_time_seconds"] - fitted
    return sample
# ------------------------------------------------------------------------------


# --- NUEVO (2) broken_anova() ------------------------------------------------
def broken_anova(sample: pd.DataFrame) -> dict[str, float]:
    """Calcula Levene y F cuando las varianzas son fuertemente desiguales."""
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]
    levene_stat, levene_p = stats.levene(*groups)
    f_stat, f_p = stats.f_oneway(*groups)
    sds = [float(np.std(group, ddof=1)) for group in groups]
    return {
        "sd_standard": sds[0],
        "sd_guided": sds[1],
        "sd_automated": sds[2],
        "mean_standard": float(groups[0].mean()),
        "mean_guided": float(groups[1].mean()),
        "mean_automated": float(groups[2].mean()),
        "levene_stat": float(levene_stat),
        "levene_p": float(levene_p),
        "f_stat": float(f_stat),
        "f_p": float(f_p),
        "n_per_group": float(N_PER_GROUP),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: pd.DataFrame) -> Path:
    """Muestra el abanico residual creado por un método de alta varianza."""
    output_path = (
        DIR_FIGURES / "diagnostico_anova_03_limite_varianzas_desiguales.png"
    )
    colors = {"Estándar": "#1A2E51", "Guiado": "#5B8DEF", "Automatizado": "#EC2661"}
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]
    boxes = axes[0].boxplot(
        groups,
        positions=[1, 2, 3],
        patch_artist=True,
        widths=0.58,
        medianprops={"color": "#1A2E51", "linewidth": 1.6},
    )
    for patch, name in zip(boxes["boxes"], TREATMENTS):
        patch.set_facecolor(colors[name])
        patch.set_alpha(0.45)
    axes[0].set_xticks([1, 2, 3])
    axes[0].set_xticklabels(TREATMENTS)
    axes[0].set_ylabel("Tiempo de ciclo (segundos)")
    axes[0].set_title("n igual, dispersión desigual")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    for name in TREATMENTS:
        block = sample.loc[sample["method"] == name]
        axes[1].scatter(
            block["fitted"],
            block["residual"],
            color=colors[name],
            s=42,
            alpha=0.9,
            label=name,
        )
    axes[1].axhline(0.0, color="#646464", linestyle="--", linewidth=1.2)
    axes[1].set_xlabel("Media de grupo ajustada (segundos)")
    axes[1].set_ylabel("Residuo (segundos)")
    axes[1].set_title("Abanico residual: supuesto de ANOVA roto")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_heterogeneous()
    results = broken_anova(sample)
    figure_path = save_figure(sample)

    print("================================================================")
    print("LECCIÓN 46 - PASO 3: LÍMITE DE VARIANZAS DESIGUALES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"n por método                    : {int(results['n_per_group'])}")
    print(f"Media Estándar                  : {results['mean_standard']:.6f}")
    print(f"Media Guiado                    : {results['mean_guided']:.6f}")
    print(f"Media Automatizado              : {results['mean_automated']:.6f}")
    print(f"DE Estándar                     : {results['sd_standard']:.6f}")
    print(f"DE Guiado                       : {results['sd_guided']:.6f}")
    print(f"DE Automatizado                 : {results['sd_automated']:.6f}")
    print(f"Estadístico de Levene           : {results['levene_stat']:.6f}")
    print(f"p-valor de Levene               : {results['levene_p']:.6e}")
    print(f"F de ANOVA                      : {results['f_stat']:.6f}")
    print(f"p-valor de ANOVA                : {results['f_p']:.6e}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

