"""
Lección 47 - Paso 3: Una R-cuadrada alta no es una palanca causal
================================================================
LA RECETA
Parte de regresion_simple_02_minimos_cuadrados.py e introduce:
    1. r_squared()          SST, SSR, SSE y R^2 = 1 - SSE/SST
    2. observational_warning()  el ajuste no es un efecto de tratamiento aleatorizado
    3. save_figure()        descomposición de R^2 con una advertencia de causalidad

Límite: una R^2 alta no implica una palanca causal. Las horas de coaching
se observaron, no se asignaron al azar. Las semanas que ya empacan más
rápido también pueden recibir más coaching, de modo que la pendiente no es
un botón de política.
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


# --- NUEVO (1) r_squared() ---------------------------------------------------
def r_squared(sample: pd.DataFrame) -> dict[str, float]:
    """Descompone la variación total y forma R^2 = 1 - SSE/SST."""
    x = sample["coaching_hours"].to_numpy()
    y = sample["units_per_hour"].to_numpy()
    slope, intercept, r_value, _, _ = stats.linregress(x, y)
    fitted = intercept + slope * x
    residual = y - fitted
    sst = float(np.sum((y - y.mean()) ** 2))
    sse = float(np.sum(residual ** 2))
    ssr = float(np.sum((fitted - y.mean()) ** 2))
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "sst": sst,
        "ssr": ssr,
        "sse": sse,
        "r_squared": 1.0 - sse / sst,
        "r_value_squared": float(r_value) ** 2,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) observational_warning() ---------------------------------------
def observational_warning(fit: dict[str, float]) -> dict[str, float]:
    """Cuantifica un aumento de 10 horas de coaching como un cambio ajustado, no causal."""
    return {
        "fitted_gain_10h": 10.0 * fit["slope"],
        "r_squared": fit["r_squared"],
        "randomized": 0.0,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(fit: dict[str, float]) -> Path:
    """Guarda la descomposición SST = SSR + SSE y la advertencia de R^2."""
    output_path = DIR_FIGURES / "regresion_simple_03_limite_r_cuadrada.png"
    labels = ["SSR\n(modelo)", "SSE\n(residual)", "SST\n(total)"]
    values = np.array([fit["ssr"], fit["sse"], fit["sst"]])
    colors = ["#EC2661", "#5B8DEF", "#1A2E51"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylabel("Suma de cuadrados")
    ax.set_title(
        f"R^2 = {fit['r_squared']:.3f} no es una palanca causal"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ymax = float(values.max()) * 1.18
    ax.set_ylim(0, ymax)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.03 * ymax,
            f"{value:.1f}",
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
    sample = build_weekly_sample()
    fit = r_squared(sample)
    warning = observational_warning(fit)
    figure_path = save_figure(fit)

    print("================================================================")
    print("LECCIÓN 47 - PASO 3: LÍMITE DE R-CUADRADA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"SST                             : {fit['sst']:.6f}")
    print(f"SSR                             : {fit['ssr']:.6f}")
    print(f"SSE                             : {fit['sse']:.6f}")
    print(f"SSR + SSE                       : {fit['ssr'] + fit['sse']:.6f}")
    print(f"R-cuadrada                      : {fit['r_squared']:.6f}")
    print(f"Chequeo de r al cuadrado        : {fit['r_value_squared']:.6f}")
    print(f"Ganancia ajustada por +10 horas : {warning['fitted_gain_10h']:.6f}")
    print("¿Palanca causal?                : No; el coaching no se aleatorizó")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

