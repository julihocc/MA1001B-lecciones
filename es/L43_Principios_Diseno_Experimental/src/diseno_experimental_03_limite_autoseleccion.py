"""
Lección 43 - Paso 3: La autoselección no es un tratamiento
==========================================================
LA RECETA
Parte de diseno_experimental_02_resultados_aleatorizados.py e introduce:
    1. self_selected_assignment()  los operadores eligen un método por experiencia
    2. observational_contrast()    tiempos confundidos frente a aleatorizados
    3. save_figure()               medias aleatorizadas junto a medias autoseleccionadas

Límite: un factor observacional no es un tratamiento aleatorizado. Los
operadores que ya trabajan más rápido eligen Automatizado, de modo que la
brecha autoseleccionada mezcla el método con quién lo eligió.
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
RAND_EXPERIENCE_SLOPE = -0.35
OBS_EXPERIENCE_SLOPE = -1.6
NOISE_SIGMA = 2.4
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_both_designs(seed: int = SEED) -> pd.DataFrame:
    """Reconstruye diseños aleatorizado y autoseleccionado desde las mismas estaciones."""
    rng = np.random.default_rng(seed)
    experience = rng.uniform(1.0, 9.0, N_UNITS)
    randomized = np.repeat(np.array(TREATMENTS), N_PER_GROUP)
    rng.shuffle(randomized)
    noise_rand = rng.normal(0.0, NOISE_SIGMA, N_UNITS)
    y_rand = (
        BASE_MEAN
        + np.array([EFFECTS[name] for name in randomized])
        + RAND_EXPERIENCE_SLOPE * (experience - experience.mean())
        + noise_rand
    )
    tertiles = np.quantile(experience, [1.0 / 3.0, 2.0 / 3.0])
    self_selected = np.where(
        experience <= tertiles[0],
        "Estándar",
        np.where(experience <= tertiles[1], "Guiado", "Automatizado"),
    )
    noise_obs = rng.normal(0.0, NOISE_SIGMA, N_UNITS)
    y_obs = (
        BASE_MEAN
        + np.array([EFFECTS[name] for name in self_selected])
        + OBS_EXPERIENCE_SLOPE * (experience - experience.mean())
        + noise_obs
    )
    return pd.DataFrame(
        {
            "station_id": np.arange(1, N_UNITS + 1),
            "experience_years": experience,
            "randomized_method": randomized,
            "randomized_cycle_time": y_rand,
            "self_selected_method": self_selected,
            "observational_cycle_time": y_obs,
        }
    )


# --- NUEVO (1) self_selected_assignment() ------------------------------------
def self_selected_assignment(designs: pd.DataFrame) -> pd.DataFrame:
    """Resume quién elige cada método cuando la experiencia impulsa la selección."""
    rows = []
    for name in TREATMENTS:
        block = designs.loc[designs["self_selected_method"] == name]
        rows.append(
            {
                "method": name,
                "n": int(len(block)),
                "mean_experience": float(block["experience_years"].mean()),
            }
        )
    return pd.DataFrame(rows)
# ------------------------------------------------------------------------------


# --- NUEVO (2) observational_contrast() --------------------------------------
def observational_contrast(designs: pd.DataFrame) -> dict[str, float]:
    """Compara brechas Automatizado menos Estándar en ambos diseños."""
    def gap(method_col: str, value_col: str) -> float:
        auto = designs.loc[designs[method_col] == "Automatizado", value_col].mean()
        std = designs.loc[designs[method_col] == "Estándar", value_col].mean()
        return float(auto - std)

    return {
        "randomized_y_gap": gap("randomized_method", "randomized_cycle_time"),
        "observational_y_gap": gap(
            "self_selected_method", "observational_cycle_time"
        ),
        "randomized_experience_gap": gap(
            "randomized_method", "experience_years"
        ),
        "observational_experience_gap": gap(
            "self_selected_method", "experience_years"
        ),
        "true_automated_effect": EFFECTS["Automatizado"],
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(designs: pd.DataFrame) -> Path:
    """Contrasta medias aleatorizadas con medias observacionales autoseleccionadas."""
    output_path = DIR_FIGURES / "diseno_experimental_03_limite_autoseleccion.png"
    rand_means = [
        float(
            designs.loc[
                designs["randomized_method"] == name, "randomized_cycle_time"
            ].mean()
        )
        for name in TREATMENTS
    ]
    obs_means = [
        float(
            designs.loc[
                designs["self_selected_method"] == name,
                "observational_cycle_time",
            ].mean()
        )
        for name in TREATMENTS
    ]
    x = np.arange(len(TREATMENTS))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(
        x - width / 2,
        rand_means,
        width=width,
        color="#1A2E51",
        label="Experimento aleatorizado",
    )
    ax.bar(
        x + width / 2,
        obs_means,
        width=width,
        color="#EC2661",
        label="Grupos autoseleccionados",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(TREATMENTS)
    ax.set_ylabel("Tiempo de ciclo medio (segundos)")
    ax.set_title("Un factor observacional no es un tratamiento aleatorizado")
    ax.set_ylim(0, 70)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False)
    for offset, values in ((-width / 2, rand_means), (width / 2, obs_means)):
        for i, value in enumerate(values):
            ax.text(
                x[i] + offset,
                value + 1.2,
                f"{value:.1f}",
                ha="center",
                fontsize=8,
                fontweight="bold",
            )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    designs = build_both_designs()
    selection = self_selected_assignment(designs)
    contrast = observational_contrast(designs)
    figure_path = save_figure(designs)

    print("================================================================")
    print("LECCIÓN 43 - PASO 3: LÍMITE DE AUTOSELECCIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Efecto verdadero Automatizado   : {contrast['true_automated_effect']:.6f}")
    for _, row in selection.iterrows():
        print(
            f"n autoselec., experiencia ({row['method']:<13}): "
            f"{int(row['n']):>2}, {row['mean_experience']:.6f}"
        )
    print(
        "Brecha experiencia aleatorizada : "
        f"{contrast['randomized_experience_gap']:.6f}"
    )
    print(
        "Brecha experiencia observacional: "
        f"{contrast['observational_experience_gap']:.6f}"
    )
    print(
        "Brecha Y aleatorizada Auto-Est. : "
        f"{contrast['randomized_y_gap']:.6f}"
    )
    print(
        "Brecha observacional Auto-Est.  : "
        f"{contrast['observational_y_gap']:.6f}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

