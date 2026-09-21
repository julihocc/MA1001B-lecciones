"""
Lección 46 - Paso 2: Varianzas iguales y residuo frente a ajustado
=================================================================
LA RECETA
Parte de diagnostico_anova_01_normalidad_residuos.py e introduce:
    1. levene_test()        scipy.stats.levene para los tres métodos
    2. residual_vs_fitted() desviaciones estándar de grupo y valores ajustados
    3. save_figure()        dispersión residuo frente a ajustado

Los mismos 36 tiempos de ciclo se reconstruyen con semilla 42. No se
importa ningún script anterior de la lección. Homocedasticidad significa
que las dispersiones dentro del método son comparables; la independencia es
una afirmación de diseño, no un estadístico de gráfica.
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


def anova_residuals(sample: pd.DataFrame) -> pd.DataFrame:
    """Forma residuos y medias de grupo ajustadas."""
    fitted = sample.groupby("method")["cycle_time_seconds"].transform("mean")
    out = sample.copy()
    out["fitted"] = fitted
    out["residual"] = out["cycle_time_seconds"] - fitted
    return out


# --- NUEVO (1) levene_test() -------------------------------------------------
def levene_test(sample: pd.DataFrame) -> dict[str, float]:
    """Contrasta varianzas iguales del tiempo de ciclo entre métodos de empaque."""
    groups = [
        sample.loc[sample["method"] == name, "cycle_time_seconds"].to_numpy()
        for name in TREATMENTS
    ]
    statistic, p_value = stats.levene(*groups)
    return {"levene_stat": float(statistic), "levene_p": float(p_value)}
# ------------------------------------------------------------------------------


# --- NUEVO (2) residual_vs_fitted() ------------------------------------------
def residual_vs_fitted(diagnosed: pd.DataFrame) -> dict[str, float]:
    """Reporta desviaciones estándar de grupo usadas en el chequeo de varianzas iguales."""
    out: dict[str, float] = {}
    for name in TREATMENTS:
        values = diagnosed.loc[
            diagnosed["method"] == name, "cycle_time_seconds"
        ]
        out[name] = float(values.std(ddof=1))
    out["residual_mean"] = float(diagnosed["residual"].mean())
    return out
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(diagnosed: pd.DataFrame) -> Path:
    """Guarda residuo frente a valores ajustados para el experimento equilibrado."""
    output_path = DIR_FIGURES / "diagnostico_anova_02_levene_homocedasticidad.png"
    colors = {"Estándar": "#1A2E51", "Guiado": "#5B8DEF", "Automatizado": "#EC2661"}
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    for name in TREATMENTS:
        block = diagnosed.loc[diagnosed["method"] == name]
        ax.scatter(
            block["fitted"],
            block["residual"],
            color=colors[name],
            s=42,
            alpha=0.9,
            label=name,
        )
    ax.axhline(0.0, color="#646464", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Media de grupo ajustada (segundos)")
    ax.set_ylabel("Residuo (segundos)")
    ax.set_title("Residuos frente a ajustados: dispersión comparable")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_cycle_times()
    diagnosed = anova_residuals(sample)
    levene = levene_test(sample)
    spreads = residual_vs_fitted(diagnosed)
    figure_path = save_figure(diagnosed)

    print("================================================================")
    print("LECCIÓN 46 - PASO 2: LEVENE Y DISPERSIÓN IGUAL")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"DE Estándar                     : {spreads['Estándar']:.6f}")
    print(f"DE Guiado                       : {spreads['Guiado']:.6f}")
    print(f"DE Automatizado                 : {spreads['Automatizado']:.6f}")
    print(f"Estadístico de Levene           : {levene['levene_stat']:.6f}")
    print(f"p-valor de Levene               : {levene['levene_p']:.6f}")
    print("Independencia                   : supuesto de diseño, no una gráfica")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

