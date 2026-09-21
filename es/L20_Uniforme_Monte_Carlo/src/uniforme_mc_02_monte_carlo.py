"""
Lección 20 - Paso 2: Comprobación Monte Carlo de la cola uniforme
================================================================
NUEVO EN ESTE PASO: draw_processing_times(), monte_carlo_tail() y save_figure().

La Receta
CAMBIOS RESPECTO A uniforme_mc_01_uniforme_exacta.py
Introdúcelos en este orden:
    1. draw_processing_times()  100,000 extracciones Uniforme(8, 20), semilla 42
    2. monte_carlo_tail()       P(X > 16) simulada y media muestral
    3. save_figure()            histograma frente a la densidad plana exacta

El mismo modelo Uniforme(8, 20) se reconstruye. No se importa ningún script
anterior de la lección.

Ejecútalo:
    uv run es/L20_Uniforme_Monte_Carlo/src/uniforme_mc_02_monte_carlo.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
A = 8.0
B = 20.0
CUT = 16.0
N_DRAWS = 100_000
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def uniform_model():
    """Devuelve el modelo uniforme continuo en [8, 20] minutos."""
    return stats.uniform(loc=A, scale=B - A)


# --- NUEVO (1) draw_processing_times() ---------------------------------------
def draw_processing_times(model, n_draws: int = N_DRAWS) -> np.ndarray:
    """Extrae n_draws tiempos de procesamiento de Uniforme(8, 20) con semilla 42."""
    rng = np.random.default_rng(SEED)
    return model.rvs(size=n_draws, random_state=rng)
# ------------------------------------------------------------------------------


# --- NUEVO (2) monte_carlo_tail() --------------------------------------------
def monte_carlo_tail(draws: np.ndarray, exact_tail: float) -> dict[str, float]:
    """Estima la cola y la media, y reporta el error Monte Carlo."""
    estimated_tail = float(np.mean(draws > CUT))
    return {
        "estimated_tail": estimated_tail,
        "sample_mean": float(np.mean(draws)),
        "abs_error": abs(estimated_tail - exact_tail),
        "n_draws": float(len(draws)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(draws: np.ndarray, model) -> Path:
    """Compara el histograma Monte Carlo con la densidad plana exacta."""
    output_path = DIR_FIGURES / "uniforme_mc_02_monte_carlo.png"
    x = np.linspace(A, B, 200)
    y = model.pdf(x)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(
        draws,
        bins=30,
        density=True,
        color="#5B8DEF",
        alpha=0.55,
        edgecolor="#1A2E51",
        label="Histograma con semilla 42",
    )
    ax.plot(x, y, color="#1A2E51", lw=2.2, label="Uniforme(8, 20) exacta")
    ax.axvline(CUT, color="#EC2661", ls="--", lw=1.4, label="x = 16")
    ax.set_xlabel("Tiempo de procesamiento (minutos)")
    ax.set_ylabel("Densidad")
    ax.set_title("100,000 extracciones recuperan la densidad uniforme plana")
    ax.set_xlim(A, B)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    model = uniform_model()
    exact_tail = float(1.0 - model.cdf(CUT))
    exact_mean = float(model.mean())
    draws = draw_processing_times(model)
    mc = monte_carlo_tail(draws, exact_tail)
    figure_path = save_figure(draws, model)

    print("================================================================")
    print("LECCIÓN 20 - PASO 2: MONTE CARLO")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria                : {SEED}")
    print(f"Extracciones Monte Carlo         : {int(mc['n_draws']):,}")
    print(f"P(X > 16) exacta                 : {exact_tail:.6f}")
    print(f"P(X > 16) Monte Carlo            : {mc['estimated_tail']:.6f}")
    print(f"Error absoluto                   : {mc['abs_error']:.6f}")
    print(f"Media exacta                     : {exact_mean:.6f}")
    print(f"Media Monte Carlo                : {mc['sample_mean']:.6f}")
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

