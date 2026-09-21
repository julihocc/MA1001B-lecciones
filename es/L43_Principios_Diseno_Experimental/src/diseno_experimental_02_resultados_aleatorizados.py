"""
Lección 43 - Paso 2: Resultados tras la asignación aleatoria
============================================================
LA RECETA
Parte de diseno_experimental_01_factor_aleatorizacion.py e introduce:
    1. randomized_outcomes()   tiempos de ciclo tras la asignación aleatoria
    2. group_summaries()       experiencia media y tiempo de ciclo medio por método
    3. save_figure()           diagramas de caja del experimento aleatorizado

Las mismas 36 estaciones se reconstruyen con semilla 42. No se importa
ningún script anterior de la lección. La asignación aleatoria es lo que
convierte una diferencia de medias posterior en una comparación de
tratamiento y no en una comparación de quién eligió qué.
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_UNITS = 36
N_PER_GROUP = 12
TREATMENTS = ("Estándar", "Guiado", "Automatizado")
BASE_MEAN = 52.0
EFFECTS = {"Estándar": 0.0, "Guiado": -2.0, "Automatizado": -7.0}
EXPERIENCE_SLOPE = -0.35
NOISE_SIGMA = 2.4
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_randomized_experiment(seed: int = SEED) -> pd.DataFrame:
    """Reconstruye estaciones, asignación aleatoria y tiempos de ciclo con semilla 42."""
    rng = np.random.default_rng(seed)
    experience = rng.uniform(1.0, 9.0, N_UNITS)
    labels = np.repeat(np.array(TREATMENTS), N_PER_GROUP)
    rng.shuffle(labels)
    noise = rng.normal(0.0, NOISE_SIGMA, N_UNITS)
    effect = np.array([EFFECTS[name] for name in labels])
    cycle_time = (
        BASE_MEAN
        + effect
        + EXPERIENCE_SLOPE * (experience - experience.mean())
        + noise
    )
    return pd.DataFrame(
        {
            "station_id": np.arange(1, N_UNITS + 1),
            "experience_years": experience,
            "method": labels,
            "cycle_time_seconds": cycle_time,
        }
    )


# --- NUEVO (1) randomized_outcomes() -----------------------------------------
def randomized_outcomes(experiment: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el experimento aleatorizado con la respuesta de tiempo de ciclo."""
    return experiment.copy()
# ------------------------------------------------------------------------------


# --- NUEVO (2) group_summaries() ---------------------------------------------
def group_summaries(experiment: pd.DataFrame) -> pd.DataFrame:
    """Resume experiencia y tiempo de ciclo por método asignado al azar."""
    rows = []
    for name in TREATMENTS:
        block = experiment.loc[experiment["method"] == name]
        rows.append(
            {
                "method": name,
                "n": int(len(block)),
                "mean_experience": float(block["experience_years"].mean()),
                "mean_cycle_time": float(block["cycle_time_seconds"].mean()),
                "sd_cycle_time": float(block["cycle_time_seconds"].std(ddof=1)),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(experiment: pd.DataFrame) -> Path:
    """Guarda diagramas de caja de tiempo de ciclo para el factor aleatorizado."""
    output_path = DIR_FIGURES / "diseno_experimental_02_resultados_aleatorizados.png"
    colors = ["#1A2E51", "#5B8DEF", "#EC2661"]
    groups = [
        experiment.loc[
            experiment["method"] == name, "cycle_time_seconds"
        ].to_numpy()
        for name in TREATMENTS
    ]
    means = [float(np.mean(values)) for values in groups]

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
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(TREATMENTS)
    ax.set_ylabel("Tiempo de ciclo (segundos)")
    ax.set_title("Experimento aleatorizado: tiempo de ciclo por método de empaque")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    experiment = randomized_outcomes(build_randomized_experiment())
    summary = group_summaries(experiment)
    figure_path = save_figure(experiment)
    auto_minus_std = (
        float(summary.loc[summary["method"] == "Automatizado", "mean_cycle_time"].iloc[0])
        - float(summary.loc[summary["method"] == "Estándar", "mean_cycle_time"].iloc[0])
    )

    print("================================================================")
    print("LECCIÓN 43 - PASO 2: RESULTADOS ALEATORIZADOS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Efecto verdadero Automatizado (s): {EFFECTS['Automatizado']:.1f}")
    for _, row in summary.iterrows():
        print(
            f"n, media Y, media exp. ({row['method']:<13}): "
            f"{int(row['n']):>2}, {row['mean_cycle_time']:.6f}, "
            f"{row['mean_experience']:.6f}"
        )
    print(f"Brecha aleatorizada Auto-Estándar: {auto_minus_std:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

