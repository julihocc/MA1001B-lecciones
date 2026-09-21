"""
Lección 39 - Paso 3: Espiar p-valores infla el error tipo I
==========================================================
LA RECETA
Parte de dos_proporciones_02_z_combinada.py e introduce:
    1. two_proportion_pvalue()  p-valor z a partir de conteos interinos
    2. simulate_peeking()       tasa tipo I con semilla 42 y cuatro miradas
    3. save_figure()            una prueba planeada frente a espiar

Bajo H0 las dos versiones comparten la misma probabilidad de conversión.
Mirar p al 25, 50, 75 y 100 por ciento del tráfico, y detenerse en el
primer p < 0.05, infla la tasa de falsos positivos por encima de alpha.
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N_A = 400
N_B = 410
P_NULL = 0.16
N_SIM = 8000
LOOK_FRACTIONS = (0.25, 0.50, 0.75, 1.00)
ALPHA = 0.05
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) two_proportion_pvalue() ---------------------------------------
def two_proportion_pvalue(x_a: int, n_a: int, x_b: int, n_b: int) -> float:
    """p-valor z combinado bilateral a partir de conteos interinos."""
    if n_a <= 0 or n_b <= 0:
        return 1.0
    p_pool = (x_a + x_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_a + 1.0 / n_b))
    if se == 0.0:
        return 1.0
    z_stat = (x_a / n_a - x_b / n_b) / se
    return float(2.0 * stats.norm.sf(np.abs(z_stat)))
# ------------------------------------------------------------------------------


# --- NUEVO (2) simulate_peeking() --------------------------------------------
def simulate_peeking(seed: int = SEED) -> dict[str, float]:
    """Estima el error tipo I con una prueba final frente a cuatro miradas."""
    rng = np.random.default_rng(seed)
    reject_once = 0
    reject_peek = 0
    for _ in range(N_SIM):
        arm_a = rng.binomial(1, P_NULL, N_A)
        arm_b = rng.binomial(1, P_NULL, N_B)
        peeked = False
        for fraction in LOOK_FRACTIONS:
            n_a = int(N_A * fraction)
            n_b = int(N_B * fraction)
            p_value = two_proportion_pvalue(
                int(arm_a[:n_a].sum()), n_a, int(arm_b[:n_b].sum()), n_b
            )
            if fraction == 1.0 and p_value < ALPHA:
                reject_once += 1
            if p_value < ALPHA:
                peeked = True
        if peeked:
            reject_peek += 1
    return {
        "n_sim": float(N_SIM),
        "n_looks": float(len(LOOK_FRACTIONS)),
        "type_i_once": reject_once / N_SIM,
        "type_i_peek": reject_peek / N_SIM,
        "alpha": ALPHA,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(results: dict[str, float]) -> Path:
    """Compara la tasa tipo I planeada con la tasa tipo I al espiar."""
    output_path = DIR_FIGURES / "dos_proporciones_03_limite_espiar.png"
    labels = ["Una prueba en nA, nB", "Cuatro miradas, parar si p < 0.05"]
    values = [results["type_i_once"], results["type_i_peek"]]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=["#1A2E51", "#EC2661"], width=0.55)
    ax.axhline(ALPHA, color="#646464", linestyle="--", linewidth=1.4,
               label="alpha nominal = 0.05")
    ax.set_ylabel("Tasa de falsos positivos bajo H0")
    ax.set_title("Espiar infla el error tipo I")
    ax.set_ylim(0, 0.18)
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.005,
            f"{value:.3f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    results = simulate_peeking()
    figure_path = save_figure(results)

    print("================================================================")
    print("LECCIÓN 39 - PASO 3: LÍMITE DE ESPIAR")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria               : {SEED}")
    print(f"Experimentos simulados          : {int(results['n_sim'])}")
    print(f"Probabilidad nula de conversión : {P_NULL:.2f}")
    print(f"Miradas por experimento         : {int(results['n_looks'])}")
    print(f"Tasa tipo I, una prueba final   : {results['type_i_once']:.6f}")
    print(f"Tasa tipo I al espiar           : {results['type_i_peek']:.6f}")
    print(f"Alpha nominal                   : {results['alpha']:.2f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

