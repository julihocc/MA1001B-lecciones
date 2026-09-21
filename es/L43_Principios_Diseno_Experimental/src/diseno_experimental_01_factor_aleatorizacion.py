"""
Lección 43 - Paso 1: Factores y asignación aleatoria
====================================================
NUEVO EN ESTE PASO: build_experimental_units(), randomize_treatments() y
save_figure().

La Receta
Una línea de empaque sintética tiene 36 estaciones. El factor experimental
es el método de empaque con tres niveles: Estándar, Guiado y Automatizado.
Cada estación es una unidad experimental. La asignación aleatoria coloca 12
estaciones en cada tratamiento de modo que una covariable previa, la
experiencia del operador, no se usa para elegir el método.

Ejecútalo:
    uv run es/L43_Principios_Diseno_Experimental/src/diseno_experimental_01_factor_aleatorizacion.py
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_experimental_units() ------------------------------------
def build_experimental_units(seed: int = SEED) -> pd.DataFrame:
    """Construye 36 estaciones sintéticas con una covariable de experiencia previa."""
    rng = np.random.default_rng(seed)
    experience = rng.uniform(1.0, 9.0, N_UNITS)
    return pd.DataFrame(
        {
            "station_id": np.arange(1, N_UNITS + 1),
            "experience_years": experience,
        }
    )
# ------------------------------------------------------------------------------


# --- NUEVO (2) randomize_treatments() ----------------------------------------
def randomize_treatments(
    units: pd.DataFrame, seed: int = SEED
) -> pd.DataFrame:
    """Asigna 12 estaciones a cada método con una permutación de semilla 42."""
    rng = np.random.default_rng(seed)
    _ = rng.uniform(1.0, 9.0, N_UNITS)
    labels = np.repeat(np.array(TREATMENTS), N_PER_GROUP)
    rng.shuffle(labels)
    assigned = units.copy()
    assigned["method"] = labels
    return assigned
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(assigned: pd.DataFrame) -> Path:
    """Muestra conteos equilibrados y experiencia por método asignado al azar."""
    output_path = DIR_FIGURES / "diseno_experimental_01_factor_aleatorizacion.png"
    colors = ["#1A2E51", "#5B8DEF", "#EC2661"]
    counts = [int((assigned["method"] == name).sum()) for name in TREATMENTS]
    experience_groups = [
        assigned.loc[assigned["method"] == name, "experience_years"].to_numpy()
        for name in TREATMENTS
    ]

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))
    axes[0].bar(TREATMENTS, counts, color=colors, width=0.62)
    axes[0].set_ylabel("Estaciones asignadas")
    axes[0].set_title("La asignación aleatoria está equilibrada")
    axes[0].set_ylim(0, 16)
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for x, count in enumerate(counts):
        axes[0].text(x, count + 0.35, str(count), ha="center", fontweight="bold")

    boxes = axes[1].boxplot(
        experience_groups,
        positions=[1, 2, 3],
        patch_artist=True,
        widths=0.58,
        medianprops={"color": "#1A2E51", "linewidth": 1.6},
    )
    for patch, color in zip(boxes["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)
    axes[1].set_xticks([1, 2, 3])
    axes[1].set_xticklabels(TREATMENTS)
    axes[1].set_ylabel("Experiencia del operador (años)")
    axes[1].set_title("Balance de covariable tras la aleatorización")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    units = build_experimental_units()
    assigned = randomize_treatments(units)
    figure_path = save_figure(assigned)
    counts = assigned["method"].value_counts().reindex(TREATMENTS)
    experience = assigned.groupby("method")["experience_years"].mean().reindex(
        TREATMENTS
    )

    print("================================================================")
    print("LECCIÓN 43 - PASO 1: FACTOR Y ALEATORIZACIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Unidades experimentales         : {N_UNITS}")
    print(f"Niveles del factor              : {', '.join(TREATMENTS)}")
    print(f"Estaciones en Estándar          : {int(counts['Estándar'])}")
    print(f"Estaciones en Guiado            : {int(counts['Guiado'])}")
    print(f"Estaciones en Automatizado      : {int(counts['Automatizado'])}")
    print(f"Experiencia media, Estándar     : {experience['Estándar']:.6f}")
    print(f"Experiencia media, Guiado       : {experience['Guiado']:.6f}")
    print(f"Experiencia media, Automatizado : {experience['Automatizado']:.6f}")
    print(
        "Brecha experiencia Auto-Estándar: "
        f"{experience['Automatizado'] - experience['Estándar']:.6f}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

