"""
Lección 39 - Paso 2: Prueba z combinada para pA menos pB
========================================================
LA RECETA
Parte de dos_proporciones_01_tasas_muestrales.py e introduce:
    1. pooled_standard_error()  EE de phatA - phatB bajo H0: pA = pB
    2. two_proportion_z_test()  estadístico z y p-valor bilateral
    3. save_figure()            colas de la normal estándar para la z A/B

Los mismos conteos nA = 400, xA = 72, nB = 410, xB = 61 se reconstruyen
desde constantes. No se importa ningún script anterior de la lección.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_A = 400
X_A = 72
N_B = 410
X_B = 61
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def sample_rates() -> dict[str, float]:
    """Devuelve tamaños, conteos de conversión y proporciones muestrales."""
    return {
        "n_a": float(N_A),
        "x_a": float(X_A),
        "n_b": float(N_B),
        "x_b": float(X_B),
        "phat_a": X_A / N_A,
        "phat_b": X_B / N_B,
        "diff": X_A / N_A - X_B / N_B,
    }


# --- NUEVO (1) pooled_standard_error() ---------------------------------------
def pooled_standard_error(p_pool: float, n_a: int = N_A, n_b: int = N_B) -> float:
    """Error estándar de phatA - phatB usando la proporción combinada."""
    return float(np.sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_a + 1.0 / n_b)))
# ------------------------------------------------------------------------------


# --- NUEVO (2) two_proportion_z_test() ---------------------------------------
def two_proportion_z_test() -> dict[str, float]:
    """Prueba z bilateral de H0: pA = pB."""
    phat_a = X_A / N_A
    phat_b = X_B / N_B
    p_pool = (X_A + X_B) / (N_A + N_B)
    se = pooled_standard_error(p_pool)
    z_stat = (phat_a - phat_b) / se
    p_value = float(2.0 * stats.norm.sf(np.abs(z_stat)))
    return {
        "phat_a": phat_a,
        "phat_b": phat_b,
        "p_pool": p_pool,
        "se": se,
        "z_stat": float(z_stat),
        "p_value": p_value,
        "z_critical": float(stats.norm.ppf(1.0 - ALPHA / 2.0)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(z_stat: float, z_critical: float) -> Path:
    """Sombrea ambas colas de N(0, 1) más allá de la z A/B observada."""
    output_path = DIR_FIGURES / "dos_proporciones_02_z_combinada.png"
    x = np.linspace(-3.6, 3.6, 600)
    y = stats.norm.pdf(x)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color="#1A2E51", linewidth=2.0)
    ax.fill_between(x, y, where=(x <= -abs(z_stat)), color="#EC2661", alpha=0.45)
    ax.fill_between(x, y, where=(x >= abs(z_stat)), color="#EC2661", alpha=0.45)
    ax.axvline(z_stat, color="#EC2661", linewidth=1.6,
               label=f"z observada = {z_stat:.2f}")
    ax.axvline(z_critical, color="#646464", linestyle="--", linewidth=1.2,
               label=f"z* = {z_critical:.2f}")
    ax.axvline(-z_critical, color="#646464", linestyle="--", linewidth=1.2)
    ax.set_xlabel("z")
    ax.set_ylabel("Densidad")
    ax.set_title("Prueba z bilateral para pA menos pB")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    test = two_proportion_z_test()
    decision = "rechazar H0" if test["p_value"] < ALPHA else "no rechazar H0"
    figure_path = save_figure(test["z_stat"], test["z_critical"])

    print("================================================================")
    print("LECCIÓN 39 - PASO 2: PRUEBA z COMBINADA")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print("Hipótesis                       : H0: pA = pB vs H1: pA != pB")
    print(f"Diferencia p-sombrero A menos B : {test['phat_a'] - test['phat_b']:.6f}")
    print(f"Proporción combinada            : {test['p_pool']:.6f}")
    print(f"EE combinado                    : {test['se']:.6f}")
    print(f"Estadístico z                   : {test['z_stat']:.6f}")
    print(f"p-valor bilateral               : {test['p_value']:.6f}")
    print(f"z* crítica (bilateral)          : {test['z_critical']:.6f}")
    print(f"Decisión a alpha = 0.05         : {decision}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

