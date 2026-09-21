"""
Lección 48 - Paso 1: Error estándar de la pendiente y prueba t
=============================================================
NUEVO EN ESTE PASO: build_overtime_sample(), slope_inference() y
save_figure().

La Receta
Una muestra sintética de un centro de correo registra 40 semanas de horas
extra (x) y unidades completadas (y). Treinta y nueve semanas ordinarias
son una nube débil. Un fin de semana de emergencia está en (48, 42). Este
paso estima la pendiente, su error estándar y la prueba t de H0: beta1 = 0
usando las 40 semanas.

Ejecútalo:
    uv run es/L48_Inferencia_Regresion_Residuos/src/inferencia_regresion_01_pendiente_ee_t.py
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


# --- NUEVO (1) build_overtime_sample() ---------------------------------------
def build_overtime_sample(seed: int = SEED) -> pd.DataFrame:
    """Simula 39 semanas ordinarias más un fin de semana de emergencia."""
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
# ------------------------------------------------------------------------------


# --- NUEVO (2) slope_inference() ---------------------------------------------
def slope_inference(sample: pd.DataFrame) -> dict[str, float]:
    """Estima pendiente, EE, estadístico t y p-valor bilateral."""
    x = sample["overtime_hours"].to_numpy()
    y = sample["units_completed"].to_numpy()
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    df = x.size - 2
    t_stat = slope / std_err
    t_crit = float(stats.t.ppf(0.975, df))
    return {
        "n": float(x.size),
        "slope": float(slope),
        "intercept": float(intercept),
        "se_slope": float(std_err),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "df": float(df),
        "t_crit": t_crit,
        "r_squared": float(r_value) ** 2,
        "reject": abs(t_stat) > t_crit,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(sample: pd.DataFrame, inf: dict[str, float]) -> Path:
    """Guarda la nube de 40 semanas con la recta ajustada, resaltando el atípico."""
    output_path = DIR_FIGURES / "inferencia_regresion_01_pendiente_ee_t.png"
    ordinary = sample.loc[~sample["emergency_weekend"]]
    emergency = sample.loc[sample["emergency_weekend"]]
    x_line = np.linspace(
        float(sample["overtime_hours"].min()),
        float(sample["overtime_hours"].max()),
        50,
    )
    y_line = inf["intercept"] + inf["slope"] * x_line

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
    ax.plot(x_line, y_line, color="#5B8DEF", linewidth=2.2, label="Recta ajustada")
    ax.set_xlabel("Horas extra")
    ax.set_ylabel("Unidades completadas")
    ax.set_title(
        f"t de pendiente = {inf['t_stat']:.2f}, p = {inf['p_value']:.2e} (n = 40)"
    )
    ax.legend(frameon=False)
    ax.grid(linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    sample = build_overtime_sample()
    inf = slope_inference(sample)
    figure_path = save_figure(sample, inf)

    print("================================================================")
    print("LECCIÓN 48 - PASO 1: EE DE LA PENDIENTE Y t")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Semanas incluyendo emergencia   : {int(inf['n'])}")
    print(f"Pendiente                       : {inf['slope']:.6f}")
    print(f"Intercepto                      : {inf['intercept']:.6f}")
    print(f"EE de la pendiente              : {inf['se_slope']:.6f}")
    print(f"Estadístico t                   : {inf['t_stat']:.6f}")
    print(f"gl                              : {int(inf['df'])}")
    print(f"t crítica (bilateral 0.05)      : {inf['t_crit']:.6f}")
    print(f"p-valor                         : {inf['p_value']:.6e}")
    print(f"R-cuadrada                      : {inf['r_squared']:.6f}")
    print(f"Rechazar H0: pendiente = 0      : {bool(inf['reject'])}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

