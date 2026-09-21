"""
Lección 17 - Paso 2: Simular 10,000 turnos
=========================================
NUEVO EN ESTE PASO: simulate_shifts(), simulation_summary() y save_figure().

La Receta
CAMBIOS RESPECTO A poisson_01_fmp.py
Introdúcelos en este orden:
    1. simulate_shifts()    10,000 extracciones Poisson(3.2) con SEED = 42
    2. simulation_summary() P(X = 0), P(X >= 6), media y varianza empíricas
    3. save_figure()        histograma frente a la FMP de Poisson

El mismo lambda = 3.2 se reconstruye desde constantes. No se importa ningún
script anterior de la lección.

Ejecútalo:
    uv run es/L17_Poisson_Eventos_Raros/src/poisson_02_simular_turnos.py
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
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def poisson_probabilities() -> dict[str, float]:
    """Devuelve P(X = 0) y P(X >= 6) para X ~ Poisson(3.2)."""
    model = stats.poisson(mu=LAMBDA)
    return {
        "p_zero": float(model.pmf(0)),
        "p_at_least_six": float(model.sf(5)),
    }


# --- NUEVO (1) simulate_shifts() ---------------------------------------------
def simulate_shifts(n_shifts: int = N_SHIFTS, seed: int = SEED) -> np.ndarray:
    """Extrae n_shifts conteos de eventos Poisson(lambda)."""
    rng = np.random.default_rng(seed)
    return rng.poisson(lam=LAMBDA, size=n_shifts)
# ------------------------------------------------------------------------------


# --- NUEVO (2) simulation_summary() ------------------------------------------
def simulation_summary(draws: np.ndarray) -> dict[str, float]:
    """Devuelve tasas empíricas de cola, media y varianza."""
    return {
        "n": float(len(draws)),
        "p_zero": float(np.mean(draws == 0)),
        "p_at_least_six": float(np.mean(draws >= 6)),
        "mean": float(np.mean(draws)),
        "variance": float(np.var(draws, ddof=0)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(draws: np.ndarray) -> Path:
    """Guarda un histograma de turnos simulados frente a la FMP de Poisson."""
    output_path = DIR_FIGURES / "poisson_02_simular_turnos.png"
    xs = np.arange(0, 13)
    masses = stats.poisson.pmf(xs, mu=LAMBDA)
    counts = np.bincount(draws, minlength=13)[:13] / len(draws)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(xs, counts, color="#5B8DEF", width=0.8, label="Simulación con semilla 42")
    ax.plot(xs, masses, "o-", color="#EC2661", lw=1.8, label="FMP de Poisson")
    ax.set_xlabel("Eventos por turno x")
    ax.set_ylabel("Frecuencia relativa / probabilidad")
    ax.set_title("10,000 turnos simulados frente a Poisson(3.2)")
    ax.set_xticks(xs)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    exact = poisson_probabilities()
    draws = simulate_shifts()
    summary = simulation_summary(draws)
    figure_path = save_figure(draws)

    print("================================================================")
    print("LECCIÓN 17 - PASO 2: TURNOS SIMULADOS")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria                : {SEED}")
    print(f"Turnos simulados                 : {int(summary['n']):,}")
    print(f"P(X = 0) exacta                  : {exact['p_zero']:.6f}")
    print(f"P(X = 0) simulada                : {summary['p_zero']:.6f}")
    print(f"P(X >= 6) exacta                 : {exact['p_at_least_six']:.6f}")
    print(f"P(X >= 6) simulada               : {summary['p_at_least_six']:.6f}")
    print(f"Media simulada                   : {summary['mean']:.6f}")
    print(f"Varianza simulada                : {summary['variance']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

