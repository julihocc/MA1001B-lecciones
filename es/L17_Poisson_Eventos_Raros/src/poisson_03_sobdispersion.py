"""
Lección 17 - Paso 3: El agrupamiento produce sobredispersión
===========================================================
NUEVO EN ESTE PASO: clustered_rate(), simulate_clustered() y save_figure().

La Receta
CAMBIOS RESPECTO A poisson_02_simular_turnos.py
Introdúcelos en este orden:
    1. clustered_rate()     70% de los turnos tienen lambda=2.0, 30% tienen lambda=6.0
    2. simulate_clustered() mezcla con semilla 42 y la misma media global 3.2
    3. save_figure()        varianza de Poisson frente a varianza agrupada

Si los eventos se agrupan, la varianza excede lambda. Esa sobredispersión es
el límite del supuesto Poisson de media igual a varianza.

Ejecútalo:
    uv run es/L17_Poisson_Eventos_Raros/src/poisson_03_sobdispersion.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
LAMBDA = 3.2
N_SHIFTS = 10_000
P_BUSY = 0.30
LAMBDA_QUIET = 2.0
LAMBDA_BUSY = 6.0
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def simulate_shifts(n_shifts: int = N_SHIFTS, seed: int = SEED) -> np.ndarray:
    """Extrae n_shifts conteos de eventos Poisson(lambda)."""
    rng = np.random.default_rng(seed)
    return rng.poisson(lam=LAMBDA, size=n_shifts)


# --- NUEVO (1) clustered_rate() ----------------------------------------------
def clustered_rate() -> dict[str, float]:
    """Devuelve la mezcla de dos tasas con media 3.2."""
    mean_lambda = (1.0 - P_BUSY) * LAMBDA_QUIET + P_BUSY * LAMBDA_BUSY
    var_lambda = (1.0 - P_BUSY) * (LAMBDA_QUIET - mean_lambda) ** 2 + P_BUSY * (
        LAMBDA_BUSY - mean_lambda
    ) ** 2
    return {
        "mean_lambda": mean_lambda,
        "var_lambda": var_lambda,
        "mixture_variance": mean_lambda + var_lambda,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) simulate_clustered() ------------------------------------------
def simulate_clustered(n_shifts: int = N_SHIFTS, seed: int = SEED) -> np.ndarray:
    """Extrae conteos agrupados de una mezcla de Poisson con semilla 42."""
    rng = np.random.default_rng(seed)
    is_busy = rng.random(n_shifts) < P_BUSY
    rates = np.where(is_busy, LAMBDA_BUSY, LAMBDA_QUIET)
    return rng.poisson(lam=rates)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(
    poisson_draws: np.ndarray,
    clustered_draws: np.ndarray,
    expected_clustered_var: float,
) -> Path:
    """Contrasta la varianza de Poisson con la sobredispersión agrupada."""
    output_path = DIR_FIGURES / "poisson_03_sobdispersion.png"
    labels = ["Varianza\nPoisson", "Varianza\nagrupada"]
    values = [float(np.var(poisson_draws, ddof=0)), float(np.var(clustered_draws, ddof=0))]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.axhline(LAMBDA, color="#5B8DEF", linestyle="--", lw=1.6, label="lambda = 3.2")
    ax.axhline(
        expected_clustered_var,
        color="#EC2661",
        linestyle=":",
        lw=1.6,
        label=f"Var de la mezcla = {expected_clustered_var:.2f}",
    )
    ax.set_ylabel("Varianza del conteo de eventos")
    ax.set_title("El agrupamiento hace que la varianza exceda lambda")
    ax.set_ylim(0, 8)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(fontsize=8)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.15,
            f"{value:.3f}",
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
    rates = clustered_rate()
    poisson_draws = simulate_shifts()
    clustered_draws = simulate_clustered()
    poisson_var = float(np.var(poisson_draws, ddof=0))
    clustered_mean = float(np.mean(clustered_draws))
    clustered_var = float(np.var(clustered_draws, ddof=0))
    figure_path = save_figure(poisson_draws, clustered_draws, rates["mixture_variance"])

    print("================================================================")
    print("LECCIÓN 17 - PASO 3: SOBREDISPERSIÓN")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria                : {SEED}")
    print(f"Lambda en calma                  : {LAMBDA_QUIET:.6f}")
    print(f"Lambda ocupado                   : {LAMBDA_BUSY:.6f}")
    print(f"Media lambda de la mezcla        : {rates['mean_lambda']:.6f}")
    print(f"Varianza teórica de la mezcla    : {rates['mixture_variance']:.6f}")
    print(f"Varianza Poisson simulada        : {poisson_var:.6f}")
    print(f"Media agrupada simulada          : {clustered_mean:.6f}")
    print(f"Varianza agrupada simulada       : {clustered_var:.6f}")
    print(f"La varianza excede lambda        : {clustered_var > LAMBDA}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

