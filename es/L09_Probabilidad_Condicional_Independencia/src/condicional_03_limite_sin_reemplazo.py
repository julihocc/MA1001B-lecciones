"""
Lección 09 - Paso 3: Dependencia sin reemplazo
==============================================
NUEVO EN ESTE PASO: exact_sequence_probability(), simulate_sequences() y
save_evidence().

CAMBIOS RESPECTO A condicional_02_pruebas_independencia.py
La Receta
---------
Introduce estos cambios en este orden:
    1. exact_sequence_probability()  actualiza el denominador del segundo sorteo
    2. simulate_sequences()          verifica el resultado con semilla 42
    3. save_evidence()               expone el error de independencia ingenua

Ejecútalo:
    uv run es/L09_Probabilidad_Condicional_Independencia/src/condicional_03_limite_sin_reemplazo.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SEED = 42
SIMULATIONS = 500_000
FIGURE_PATH = (
    Path(__file__).resolve().parents[1] / "figuras" / "condicional_03_secuencia.png"
)


# --- NUEVO (1) exact_sequence_probability() ----------------------------------
def exact_sequence_probability() -> tuple[float, float, float]:
    """Devuelve las probabilidades del primero, del segundo condicional y de ambos marcados."""
    p_first_flagged = 4 / 10
    p_second_flagged_given_first = 3 / 9
    p_both_flagged = p_first_flagged * p_second_flagged_given_first
    return p_first_flagged, p_second_flagged_given_first, p_both_flagged
# -----------------------------------------------------------------------------


# --- NUEVO (2) simulate_sequences() ------------------------------------------
def simulate_sequences() -> float:
    """Simula pares ordenados extraídos de forma uniforme sin reemplazo."""
    rng = np.random.default_rng(SEED)
    first = rng.integers(0, 10, size=SIMULATIONS)
    second_reduced = rng.integers(0, 9, size=SIMULATIONS)
    second = second_reduced + (second_reduced >= first)
    return float(np.mean((first < 4) & (second < 4)))
# -----------------------------------------------------------------------------


# --- NUEVO (3) save_evidence() -----------------------------------------------
def save_evidence(naive: float, exact: float, simulated: float) -> None:
    """Guarda las probabilidades de secuencia ingenua, exacta y simulada."""
    labels = [
        "Independencia\ningenua",
        "Exacta sin\nreemplazo",
        "Simulación\nsemilla 42",
    ]
    values = [naive, exact, simulated]
    colors = ["#9E9E9E", "#D81B60", "#1E88E5"]

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_ylim(0, 0.19)
    ax.set_ylabel("P(ambos pedidos seleccionados están marcados)")
    ax.set_title("Sin reemplazo, el segundo sorteo depende del primero")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.006,
            f"{value:.4f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)
# -----------------------------------------------------------------------------


def main() -> None:
    p_first, p_second_given_first, exact = exact_sequence_probability()
    naive = p_first**2
    simulated = simulate_sequences()
    print("Lote sintético de inspección: 10 pedidos, 4 marcados")
    print(f"P(primero marcado): {p_first:.6f}")
    print(f"P(segundo marcado | primero marcado): {p_second_given_first:.6f}")
    print(f"Probabilidad de independencia ingenua: {naive:.6f}")
    print(f"Probabilidad exacta sin reemplazo: {exact:.6f}")
    print(f"Simulación semilla 42 ({SIMULATIONS:,} ensayos): {simulated:.6f}")
    save_evidence(naive, exact, simulated)
    print("Figura guardada:", FIGURE_PATH)


if __name__ == "__main__":
    main()

