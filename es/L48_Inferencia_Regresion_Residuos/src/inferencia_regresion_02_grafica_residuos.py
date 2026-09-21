"""
Lección 48 - Paso 2: Gráfica de residuos de la recta ajustada
============================================================
LA RECETA
Parte de inferencia_regresion_01_pendiente_ee_t.py e introduce:
    1. fitted_residuals()   yhat y e = y - yhat para las 40 semanas
    2. residual_summaries() media residual, DE y el residuo de emergencia
    3. save_figure()        residuo frente a ajustado, atípico marcado

Las mismas 40 semanas se reconstruyen con semilla 42. No se importa ningún
script anterior de la lección. Una gráfica de residuos es una herramienta
de decisión: puede mostrar un abanico, una curva o una semana que no
pertenece con las demás.
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


# --- NUEVO (1) fitted_residuals() --------------------------------------------
def fitted_residuals(sample: pd.DataFrame) -> pd.DataFrame:
    """Adjunta valores ajustados y residuos de la recta de 40 semanas."""
    x = sample["overtime_hours"].to_numpy()
    y = sample["units_completed"].to_numpy()
    slope, intercept, _, _, _ = stats.linregress(x, y)
    out = sample.copy()
    out["fitted"] = intercept + slope * out["overtime_hours"]
    out["residual"] = out["units_completed"] - out["fitted"]
    return out
# ------------------------------------------------------------------------------


# --- NUEVO (2) residual_summaries() ------------------------------------------
def residual_summaries(fitted: pd.DataFrame) -> dict[str, float]:
    """Resume residuos y aísla el residuo del fin de semana de emergencia."""
    residuals = fitted["residual"].to_numpy()
    emergency = fitted.loc[fitted["emergency_weekend"], "residual"].iloc[0]
    return {
        "residual_mean": float(residuals.mean()),
        "residual_sd": float(residuals.std(ddof=1)),
        "emergency_residual": float(emergency),
        "max_abs_residual": float(np.max(np.abs(residuals))),
        "n": float(len(fitted)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(fitted: pd.DataFrame) -> Path:
    """Guarda residuo frente a valores ajustados con la semana de emergencia marcada."""
    output_path = DIR_FIGURES / "inferencia_regresion_02_grafica_residuos.png"
    ordinary = fitted.loc[~fitted["emergency_weekend"]]
    emergency = fitted.loc[fitted["emergency_weekend"]]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.scatter(
        ordinary["fitted"],
        ordinary["residual"],
        color="#1A2E51",
        s=42,
        label="Semanas ordinarias",
    )
    ax.scatter(
        emergency["fitted"],
        emergency["residual"],
        color="#EC2661",
        s=70,
        zorder=3,
        label="Fin de semana de emergencia",
    )
    ax.axhline(0.0, color="#646464", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Unidades completadas ajustadas")
    ax.set_ylabel("Residuo")
    ax.set_title("Gráfica de residuos: una semana se aparta")
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_overtime_sample()
    fitted = fitted_residuals(sample)
    summary = residual_summaries(fitted)
    figure_path = save_figure(fitted)

    print("================================================================")
    print("LECCIÓN 48 - PASO 2: GRÁFICA DE RESIDUOS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Semanas                         : {int(summary['n'])}")
    print(f"Media de residuos               : {summary['residual_mean']:.6f}")
    print(f"DE de residuos                  : {summary['residual_sd']:.6f}")
    print(f"Residuo del fin de semana de emergencia: {summary['emergency_residual']:.6f}")
    print(f"|residuo| más grande            : {summary['max_abs_residual']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

