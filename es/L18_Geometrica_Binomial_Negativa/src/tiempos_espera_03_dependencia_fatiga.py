"""
Lección 18 - Paso 3: La fatiga hace dependientes los ensayos
===========================================================
NUEVO EN ESTE PASO: fatigue_success_probability(), simulate_waiting_times() y
save_figure().

La Receta
CAMBIOS RESPECTO A tiempos_espera_02_binomial_negativa.py
Introdúcelos en este orden:
    1. fatigue_success_probability()  p declina con el número de ensayo
    2. simulate_waiting_times()       tiempos de espera con semilla 42 bajo fatiga
    3. save_figure()                  media geométrica frente a media fatigada

Si la fatiga del inspector baja p en ensayos posteriores, los ensayos ya no
son independientes con p constante. Los tiempos de espera entonces exceden
1/p.

Ejecútalo:
    uv run es/L18_Geometrica_Binomial_Negativa/src/tiempos_espera_03_dependencia_fatiga.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
P_SUCCESS = 0.12
FATIGUE_RATIO = 0.97
N_SIMULATIONS = 10_000
MAX_TRIALS = 400
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def geometric_parameters() -> dict[str, float]:
    """Devuelve p y E[X] = 1/p para ensayos hasta el primer éxito."""
    return {
        "p": P_SUCCESS,
        "mean": 1.0 / P_SUCCESS,
    }


# --- NUEVO (1) fatigue_success_probability() ---------------------------------
def fatigue_success_probability(trial_number: np.ndarray) -> np.ndarray:
    """Devuelve una probabilidad de éxito declinante p * 0.97^(t-1)."""
    return P_SUCCESS * (FATIGUE_RATIO ** (trial_number - 1))
# ------------------------------------------------------------------------------


# --- NUEVO (2) simulate_waiting_times() --------------------------------------
def simulate_waiting_times(
    n_simulations: int = N_SIMULATIONS,
    seed: int = SEED,
) -> np.ndarray:
    """Simula tiempos de espera cuando p declina con cada ensayo."""
    rng = np.random.default_rng(seed)
    waits = np.full(n_simulations, MAX_TRIALS, dtype=int)
    still_open = np.ones(n_simulations, dtype=bool)
    for trial in range(1, MAX_TRIALS + 1):
        p_t = float(fatigue_success_probability(np.array([trial]))[0])
        success = rng.random(n_simulations) < p_t
        newly_done = still_open & success
        waits[newly_done] = trial
        still_open[newly_done] = False
        if not np.any(still_open):
            break
    return waits
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(geometric_mean: float, fatigued_mean: float) -> Path:
    """Contrasta la media de p constante con la media fatigada."""
    output_path = DIR_FIGURES / "tiempos_espera_03_dependencia_fatiga.png"
    labels = ["Geométrica\nE[X] = 1/p", "Fatiga\nmedia simulada"]
    values = [geometric_mean, fatigued_mean]
    colors = ["#1A2E51", "#EC2661"]

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Tiempo medio de espera (ensayos)")
    ax.set_title("Un p declinante hace la espera más larga que 1/p")
    ax.set_ylim(0, 22)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.25,
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
    geom = geometric_parameters()
    p_trial_1 = float(fatigue_success_probability(np.array([1]))[0])
    p_trial_10 = float(fatigue_success_probability(np.array([10]))[0])
    waits = simulate_waiting_times()
    fatigued_mean = float(np.mean(waits))
    geometric_draws = stats.geom.rvs(p=P_SUCCESS, size=N_SIMULATIONS, random_state=SEED)
    figure_path = save_figure(geom["mean"], fatigued_mean)

    print("================================================================")
    print("LECCIÓN 18 - PASO 3: DEPENDENCIA POR FATIGA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria                : {SEED}")
    print(f"Tiempos de espera simulados      : {N_SIMULATIONS:,}")
    print(f"Geométrica E[X] = 1/p            : {geom['mean']:.6f}")
    print(f"Fatiga p en el ensayo 1          : {p_trial_1:.6f}")
    print(f"Fatiga p en el ensayo 10         : {p_trial_10:.6f}")
    print(f"Media fatigada simulada          : {fatigued_mean:.6f}")
    print(f"Media simulada con p constante   : {float(np.mean(geometric_draws)):.6f}")
    print(f"La media fatigada excede 1/p     : {fatigued_mean > geom['mean']}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

