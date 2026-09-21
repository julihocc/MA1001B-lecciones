"""
Lección 18 - Paso 2: Tiempo de espera binomial negativo
=======================================================
NUEVO EN ESTE PASO: negative_binomial_parameters(), trials_until_r() y
save_figure().

La Receta
CAMBIOS RESPECTO A tiempos_espera_01_geometrica.py
Introdúcelos en este orden:
    1. negative_binomial_parameters()  r = 3 éxitos, E[X] = r/p
    2. trials_until_r()    convierte fallos nbinom de scipy en conteos de ensayos
    3. save_figure()       FMP de ensayos hasta el tercer éxito

X es el número de ensayos independientes hasta encontrar r = 3 defectuosos,
cada uno con p = 0.12. El modelo geométrico es el caso especial r = 1.

Ejecútalo:
    uv run es/L18_Geometrica_Binomial_Negativa/src/tiempos_espera_02_binomial_negativa.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
P_SUCCESS = 0.12
R_SUCCESSES = 3
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def geometric_parameters() -> dict[str, float]:
    """Devuelve p y E[X] = 1/p para ensayos hasta el primer éxito."""
    return {
        "p": P_SUCCESS,
        "mean": 1.0 / P_SUCCESS,
    }


# --- NUEVO (1) negative_binomial_parameters() --------------------------------
def negative_binomial_parameters() -> dict[str, float | int]:
    """Devuelve r, p y E[X] = r/p para ensayos hasta r éxitos."""
    return {
        "r": R_SUCCESSES,
        "p": P_SUCCESS,
        "mean": R_SUCCESSES / P_SUCCESS,
        "variance": R_SUCCESSES * (1.0 - P_SUCCESS) / P_SUCCESS ** 2,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) trials_until_r() ----------------------------------------------
def trials_until_r(x_trials: np.ndarray) -> np.ndarray:
    """Devuelve P(X = x) para X = fallos antes de r éxitos más r."""
    failures = x_trials - R_SUCCESSES
    return stats.nbinom.pmf(failures, n=R_SUCCESSES, p=P_SUCCESS)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure() -> Path:
    """Guarda la FMP binomial negativa de ensayos hasta r = 3."""
    output_path = DIR_FIGURES / "tiempos_espera_02_binomial_negativa.png"
    xs = np.arange(R_SUCCESSES, 41)
    masses = trials_until_r(xs)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, masses, color="#1A2E51", width=0.8)
    ax.axvline(
        R_SUCCESSES / P_SUCCESS,
        color="#EC2661",
        linestyle="--",
        lw=2.0,
        label="E[X] = r/p = 25",
    )
    ax.set_xlabel("Ensayo del tercer éxito x")
    ax.set_ylabel("P(X = x)")
    ax.set_title("Binomial negativa: ensayos hasta r = 3 éxitos")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    geom = geometric_parameters()
    nb = negative_binomial_parameters()
    p_min = float(trials_until_r(np.array([R_SUCCESSES]))[0])
    figure_path = save_figure()

    print("================================================================")
    print("LECCIÓN 18 - PASO 2: BINOMIAL NEGATIVA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Geométrica E[X] = 1/p            : {geom['mean']:.6f}")
    print(f"r                                : {nb['r']}")
    print(f"p                                : {nb['p']:.6f}")
    print(f"E[X] = r/p                       : {nb['mean']:.6f}")
    print(f"Var(X)                           : {nb['variance']:.6f}")
    print(f"P(X = 3) = p^3                   : {p_min:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

