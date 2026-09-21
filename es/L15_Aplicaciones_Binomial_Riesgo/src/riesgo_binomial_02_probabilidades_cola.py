"""
Lección 15 - Paso 2: Probabilidades de cola P(X >= 3)
=====================================================
NUEVO EN ESTE PASO: tail_probability(), compare_tails() y save_figure().

La Receta
CAMBIOS RESPECTO A riesgo_binomial_01_dos_politicas.py
Introdúcelos en este orden:
    1. tail_probability()   P(X >= 3) = 1 - F(2) para una política binomial
    2. compare_tails()      Política A frente a Política B
    3. save_figure()        comparación de barras de las dos colas

La misma media np = 2 no implica la misma chance de tres o más defectuosos.

Ejecútalo:
    uv run es/L15_Aplicaciones_Binomial_Riesgo/src/riesgo_binomial_02_probabilidades_cola.py
"""

from pathlib import Path

import matplotlib
import numpy as np
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
POLICY_A = {"name": "A", "n": 50, "p": 0.04}
POLICY_B = {"name": "B", "n": 20, "p": 0.10}
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


def policy_a() -> dict[str, float | int | str]:
    """Devuelve la Política A: muestra más grande, menor chance de defecto."""
    n = POLICY_A["n"]
    p = POLICY_A["p"]
    return {"name": "A", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}


def policy_b() -> dict[str, float | int | str]:
    """Devuelve la Política B: muestra más pequeña, mayor chance de defecto."""
    n = POLICY_B["n"]
    p = POLICY_B["p"]
    return {"name": "B", "n": n, "p": p, "mean": n * p, "variance": n * p * (1.0 - p)}


# --- NUEVO (1) tail_probability() --------------------------------------------
def tail_probability(n: int, p: float, threshold: int = 3) -> float:
    """Devuelve P(X >= threshold) para X ~ Binomial(n, p)."""
    return float(stats.binom.sf(threshold - 1, n=n, p=p))
# ------------------------------------------------------------------------------


# --- NUEVO (2) compare_tails() -----------------------------------------------
def compare_tails() -> dict[str, float]:
    """Devuelve P(X = 0), P(X >= 3) y la cola lejana P(X >= 8)."""
    return {
        "p0_a": float(stats.binom.pmf(0, n=POLICY_A["n"], p=POLICY_A["p"])),
        "p0_b": float(stats.binom.pmf(0, n=POLICY_B["n"], p=POLICY_B["p"])),
        "tail3_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 3),
        "tail3_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 3),
        "tail8_a": tail_probability(POLICY_A["n"], POLICY_A["p"], 8),
        "tail8_b": tail_probability(POLICY_B["n"], POLICY_B["p"], 8),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(tails: dict[str, float]) -> Path:
    """Guarda P(X = 0) y la cola lejana P(X >= 8) de ambas políticas."""
    output_path = DIR_FIGURES / "riesgo_binomial_02_probabilidades_cola.png"
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))
    labels = ["Política A", "Política B"]
    colors = ["#1A2E51", "#EC2661"]

    zeros = [tails["p0_a"], tails["p0_b"]]
    axes[0].bar(labels, zeros, color=colors, width=0.55)
    axes[0].set_ylabel("P(X = 0)")
    axes[0].set_title("Probabilidad de muestra limpia")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(zeros):
        axes[0].text(idx, value + 0.003, f"{value:.4f}", ha="center", fontsize=8)

    far = [tails["tail8_a"], tails["tail8_b"]]
    axes[1].bar(labels, far, color=colors, width=0.55)
    axes[1].set_ylabel("P(X >= 8)")
    axes[1].set_title("Riesgo de cola lejana")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(far):
        axes[1].text(idx, value + 0.00002, f"{value:.6f}", ha="center", fontsize=8)

    fig.suptitle("La misma np = 2 no iguala P(X = 0) ni P(X >= 8)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    a = policy_a()
    b = policy_b()
    tails = compare_tails()
    figure_path = save_figure(tails)

    print("================================================================")
    print("LECCIÓN 15 - PASO 2: PROBABILIDADES DE COLA")
    print("================================================================")
    print("Aviso de datos sintéticos        : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)    : {SEED}")
    print(f"Política A media                 : {a['mean']:.6f}")
    print(f"Política B media                 : {b['mean']:.6f}")
    print(f"Política A P(X = 0)              : {tails['p0_a']:.6f}")
    print(f"Política B P(X = 0)              : {tails['p0_b']:.6f}")
    print(f"Política A P(X >= 3)             : {tails['tail3_a']:.6f}")
    print(f"Política B P(X >= 3)             : {tails['tail3_b']:.6f}")
    print(f"Política A P(X >= 8)             : {tails['tail8_a']:.6f}")
    print(f"Política B P(X >= 8)             : {tails['tail8_b']:.6f}")
    print(
        "Razón de cola lejana A/B          : "
        f"{tails['tail8_a'] / tails['tail8_b']:.6f}"
    )
    print(f"Figura guardada en               : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

