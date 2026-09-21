"""
Lección 47 - Paso 1: Dispersión de un predictor numérico y una respuesta
=======================================================================
NUEVO EN ESTE PASO: build_weekly_sample(), describe_scatter() y
save_figure().

La Receta
Una muestra sintética de un centro de correo registra 40 semanas. El
predictor x es horas de coaching esa semana. La respuesta y es unidades
empacadas por hora-labor. La recta verdadera es y = 12 + 0.45 x más ruido.
Este paso dibuja la nube antes de ajustar cualquier recta.

Ejecútalo:
    uv run es/L47_Regresion_Lineal_Simple/src/regresion_simple_01_dispersion.py
"""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_WEEKS = 40
TRUE_INTERCEPT = 12.0
TRUE_SLOPE = 0.45
NOISE_SIGMA = 2.4
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) build_weekly_sample() -----------------------------------------
def build_weekly_sample(seed: int = SEED) -> pd.DataFrame:
    """Simula 40 semanas de horas de coaching y unidades empacadas por hora-labor."""
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
# ------------------------------------------------------------------------------


# --- NUEVO (2) describe_scatter() --------------------------------------------
def describe_scatter(sample: pd.DataFrame) -> dict[str, float]:
    """Resume las dos variables numéricas antes de ajustar una recta."""
    x = sample["coaching_hours"]
    y = sample["units_per_hour"]
    return {
        "n": float(len(sample)),
        "x_mean": float(x.mean()),
        "y_mean": float(y.mean()),
        "x_min": float(x.min()),
        "x_max": float(x.max()),
        "corr": float(np.corrcoef(x, y)[0, 1]),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: pd.DataFrame) -> Path:
    """Guarda la nube sin etiquetar de unidades frente a horas de coaching."""
    output_path = DIR_FIGURES / "regresion_simple_01_dispersion.png"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.scatter(
        sample["coaching_hours"],
        sample["units_per_hour"],
        color="#1A2E51",
        s=42,
        alpha=0.9,
    )
    ax.set_xlabel("Horas de coaching en la semana")
    ax.set_ylabel("Unidades empacadas por hora-labor")
    ax.set_title("Cuarenta semanas sintéticas, aún sin recta ajustada")
    ax.grid(linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_weekly_sample()
    summary = describe_scatter(sample)
    figure_path = save_figure(sample)

    print("================================================================")
    print("LECCIÓN 47 - PASO 1: DISPERSIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Semanas                         : {int(summary['n'])}")
    print(f"Intercepto verdadero            : {TRUE_INTERCEPT:.2f}")
    print(f"Pendiente verdadera             : {TRUE_SLOPE:.2f}")
    print(f"Media de horas de coaching      : {summary['x_mean']:.6f}")
    print(f"Media de unidades por hora      : {summary['y_mean']:.6f}")
    print(f"Rango de horas de coaching      : {summary['x_min']:.6f} a {summary['x_max']:.6f}")
    print(f"Correlación muestral            : {summary['corr']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

