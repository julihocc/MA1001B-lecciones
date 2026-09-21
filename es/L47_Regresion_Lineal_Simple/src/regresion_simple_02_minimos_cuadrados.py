"""
Lección 47 - Paso 2: Pendiente e intercepto de mínimos cuadrados
================================================================
LA RECETA
Parte de regresion_simple_01_dispersion.py e introduce:
    1. least_squares_fit()  pendiente e intercepto de las ecuaciones normales
    2. fitted_values()      yhat = b0 + b1 x
    3. save_figure()        dispersión con la recta de mínimos cuadrados

Las mismas 40 semanas se reconstruyen con semilla 42. No se importa ningún
script anterior de la lección. La recta ajustada es la única que minimiza
la suma de residuales verticales al cuadrado.
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_WEEKS = 40
TRUE_INTERCEPT = 12.0
TRUE_SLOPE = 0.45
NOISE_SIGMA = 2.4
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def build_weekly_sample(seed: int = SEED) -> pd.DataFrame:
    """Reconstruye la muestra sintética de coaching de 40 semanas con semilla 42."""
    rng = np.random.default_rng(seed)
    coaching_hours = rng.uniform(8.0, 40.0, N_WEEKS)
    units_per_hour = (
        TRUE_INTERCEPT
        + TRUE_SLOPE * coaching_hours
        + rng.normal(0.0, NOISE_SIGMA, N_WEEKS)
    )
    return pd.DataFrame(
        {
            "week_id": np.arange(1, N_WEEKS + 1),
            "coaching_hours": coaching_hours,
            "units_per_hour": units_per_hour,
        }
    )


# --- NUEVO (1) least_squares_fit() -------------------------------------------
def least_squares_fit(sample: pd.DataFrame) -> dict[str, float]:
    """Estima intercepto y pendiente por mínimos cuadrados ordinarios."""
    x = sample["coaching_hours"].to_numpy()
    y = sample["units_per_hour"].to_numpy()
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    sxx = float(np.sum((x - x.mean()) ** 2))
    sxy = float(np.sum((x - x.mean()) * (y - y.mean())))
    manual_slope = sxy / sxx
    manual_intercept = float(y.mean() - manual_slope * x.mean())
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "manual_slope": manual_slope,
        "manual_intercept": manual_intercept,
        "r_value": float(r_value),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) fitted_values() -----------------------------------------------
def fitted_values(
    sample: pd.DataFrame, fit: dict[str, float]
) -> pd.DataFrame:
    """Adjunta yhat = b0 + b1 x a la muestra semanal."""
    out = sample.copy()
    out["fitted"] = fit["intercept"] + fit["slope"] * out["coaching_hours"]
    out["residual"] = out["units_per_hour"] - out["fitted"]
    return out
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(fitted: pd.DataFrame, fit: dict[str, float]) -> Path:
    """Guarda la nube con la recta de mínimos cuadrados superpuesta."""
    output_path = DIR_FIGURES / "regresion_simple_02_minimos_cuadrados.png"
    x_line = np.linspace(
        float(fitted["coaching_hours"].min()),
        float(fitted["coaching_hours"].max()),
        50,
    )
    y_line = fit["intercept"] + fit["slope"] * x_line

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.scatter(
        fitted["coaching_hours"],
        fitted["units_per_hour"],
        color="#1A2E51",
        s=42,
        alpha=0.9,
        label="Semanas observadas",
    )
    ax.plot(
        x_line,
        y_line,
        color="#EC2661",
        linewidth=2.2,
        label=(
            f"y = {fit['intercept']:.3f} + "
            f"{fit['slope']:.3f} x"
        ),
    )
    ax.set_xlabel("Horas de coaching en la semana")
    ax.set_ylabel("Unidades empacadas por hora-labor")
    ax.set_title("Recta de mínimos cuadrados del centro de correo sintético")
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_weekly_sample()
    fit = least_squares_fit(sample)
    fitted = fitted_values(sample, fit)
    figure_path = save_figure(fitted, fit)
    sse = float(np.sum(fitted["residual"] ** 2))

    print("================================================================")
    print("LECCIÓN 47 - PASO 2: MÍNIMOS CUADRADOS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Pendiente manual                : {fit['manual_slope']:.6f}")
    print(f"Pendiente scipy                 : {fit['slope']:.6f}")
    print(f"Intercepto manual               : {fit['manual_intercept']:.6f}")
    print(f"Intercepto scipy                : {fit['intercept']:.6f}")
    print(f"Pendiente verdadera             : {TRUE_SLOPE:.2f}")
    print(f"Intercepto verdadero            : {TRUE_INTERCEPT:.2f}")
    print(f"SSE                             : {sse:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

