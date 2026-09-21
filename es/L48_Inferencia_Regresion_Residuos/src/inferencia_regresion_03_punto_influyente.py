"""
Lección 48 - Paso 3: Un punto influyente puede crear una pendiente significativa
===============================================================================
LA RECETA
Parte de inferencia_regresion_02_grafica_residuos.py e introduce:
    1. fit_with_and_without()  inferencia de pendiente en n=40 frente a n=39
    2. influence_contrast()    la pendiente significativa desaparece al quitar el punto
    3. save_figure()           dos rectas ajustadas sobre la misma nube

Límite: un punto influyente puede crear una pendiente significativa que
desaparece al quitarlo. El fin de semana de emergencia no es una semana
extra típica, de modo que la prueba t n=40 no es una decisión sobre
operaciones ordinarias.
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_ORDINARY = 39
OUTLIER_X = 48.0
OUTLIER_Y = 42.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_overtime_sample(seed: int = SEED) -> pd.DataFrame:
    """Reconstruye 39 semanas ordinarias más un fin de semana de emergencia con semilla 42."""
    rng = np.random.default_rng(seed)
    overtime = rng.uniform(6.0, 22.0, N_ORDINARY)
    units = 18.0 + 0.04 * overtime + rng.normal(0.0, 3.2, N_ORDINARY)
    x = np.append(overtime, OUTLIER_X)
    y = np.append(units, OUTLIER_Y)
    return pd.DataFrame(
        {
            "week_id": np.arange(1, x.size + 1),
            "overtime_hours": x,
            "units_completed": y,
            "emergency_weekend": np.append(
                np.zeros(N_ORDINARY, dtype=bool), True
            ),
        }
    )


def _infer(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Devuelve la inferencia de pendiente para un par de arreglos (x, y)."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    t_stat = slope / std_err
    return {
        "n": float(x.size),
        "slope": float(slope),
        "intercept": float(intercept),
        "se_slope": float(std_err),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "r_squared": float(r_value) ** 2,
    }


# --- NUEVO (1) fit_with_and_without() ----------------------------------------
def fit_with_and_without(sample: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Ajusta la recta en las 40 semanas y de nuevo tras quitar la emergencia."""
    full = _infer(
        sample["overtime_hours"].to_numpy(),
        sample["units_completed"].to_numpy(),
    )
    ordinary = sample.loc[~sample["emergency_weekend"]]
    reduced = _infer(
        ordinary["overtime_hours"].to_numpy(),
        ordinary["units_completed"].to_numpy(),
    )
    return {"with_point": full, "without_point": reduced}
# ------------------------------------------------------------------------------


# --- NUEVO (2) influence_contrast() ------------------------------------------
def influence_contrast(
    fits: dict[str, dict[str, float]],
) -> dict[str, float]:
    """Contrasta la significancia con y sin el fin de semana de emergencia."""
    with_pt = fits["with_point"]
    without = fits["without_point"]
    return {
        "slope_with": with_pt["slope"],
        "p_with": with_pt["p_value"],
        "slope_without": without["slope"],
        "p_without": without["p_value"],
        "significant_with": with_pt["p_value"] < 0.05,
        "significant_without": without["p_value"] < 0.05,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    sample: pd.DataFrame, fits: dict[str, dict[str, float]]
) -> Path:
    """Superpone las rectas n=40 y n=39 sobre la misma nube."""
    output_path = DIR_FIGURES / "inferencia_regresion_03_punto_influyente.png"
    ordinary = sample.loc[~sample["emergency_weekend"]]
    emergency = sample.loc[sample["emergency_weekend"]]
    x_full = np.linspace(5.0, 50.0, 60)
    y_with = (
        fits["with_point"]["intercept"]
        + fits["with_point"]["slope"] * x_full
    )
    y_without = (
        fits["without_point"]["intercept"]
        + fits["without_point"]["slope"] * x_full
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.scatter(
        ordinary["overtime_hours"],
        ordinary["units_completed"],
        color="#1A2E51",
        s=42,
        label="Semanas ordinarias",
    )
    ax.scatter(
        emergency["overtime_hours"],
        emergency["units_completed"],
        color="#EC2661",
        s=70,
        zorder=3,
        label="Fin de semana de emergencia",
    )
    ax.plot(
        x_full,
        y_with,
        color="#EC2661",
        linewidth=2.2,
        label="recta n = 40",
    )
    ax.plot(
        x_full,
        y_without,
        color="#5B8DEF",
        linewidth=2.2,
        linestyle="--",
        label="recta n = 39",
    )
    ax.set_xlabel("Horas extra")
    ax.set_ylabel("Unidades completadas")
    ax.set_title("Un punto influyente puede crear una pendiente significativa")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_overtime_sample()
    fits = fit_with_and_without(sample)
    contrast = influence_contrast(fits)
    figure_path = save_figure(sample, fits)
    with_pt = fits["with_point"]
    without = fits["without_point"]

    print("================================================================")
    print("LECCIÓN 48 - PASO 3: LÍMITE DEL PUNTO INFLUYENTE")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"n con fin de semana de emergencia: {int(with_pt['n'])}")
    print(f"Pendiente con el punto          : {with_pt['slope']:.6f}")
    print(f"EE con el punto                 : {with_pt['se_slope']:.6f}")
    print(f"t con el punto                  : {with_pt['t_stat']:.6f}")
    print(f"p con el punto                  : {with_pt['p_value']:.6e}")
    print(f"R-cuadrada con el punto         : {with_pt['r_squared']:.6f}")
    print(f"n sin fin de semana de emergencia: {int(without['n'])}")
    print(f"Pendiente sin el punto          : {without['slope']:.6f}")
    print(f"EE sin el punto                 : {without['se_slope']:.6f}")
    print(f"t sin el punto                  : {without['t_stat']:.6f}")
    print(f"p sin el punto                  : {without['p_value']:.6f}")
    print(f"R-cuadrada sin el punto         : {without['r_squared']:.6f}")
    print(f"Significativa a 0.05 con punto  : {bool(contrast['significant_with'])}")
    print(
        "Significativa a 0.05 sin punto  : "
        f"{bool(contrast['significant_without'])}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

