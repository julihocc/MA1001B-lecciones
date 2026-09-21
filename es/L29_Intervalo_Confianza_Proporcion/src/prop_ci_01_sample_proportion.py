"""
Lección 29 - Paso 1: Proporción muestral y conteos éxito-fracaso
===============================================================
NUEVO EN ESTE PASO: first_contact_counts(), sample_proportion() y
save_figure().

La Receta
Un registro de servicio completamente sintético anota si un ticket se
resuelve en el primer contacto. En una instantánea de aula con semilla 42,
x = 27 de n = 150 tickets son resoluciones en primer contacto. La
estimación puntual es phat = x / n. La aproximación normal posterior
requiere verificar n phat y n(1-phat).

Ejecútalo:
    uv run es/L29_Intervalo_Confianza_Proporcion/src/prop_ci_01_sample_proportion.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 150
X_SUCCESS = 27
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) first_contact_counts() ----------------------------------------
def first_contact_counts() -> dict[str, int]:
    """Retorna los conteos sintéticos de la instantánea de primer contacto."""
    return {
        "n": N,
        "successes": X_SUCCESS,
        "failures": N - X_SUCCESS,
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) sample_proportion() -------------------------------------------
def sample_proportion(counts: dict[str, int]) -> dict[str, float]:
    """Calcula phat y los dos productos éxito-fracaso usados en la verificación."""
    phat = counts["successes"] / counts["n"]
    return {
        "phat": phat,
        "qhat": 1.0 - phat,
        "n_phat": counts["n"] * phat,
        "n_qhat": counts["n"] * (1.0 - phat),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(counts: dict[str, int], props: dict[str, float]) -> Path:
    """Guarda un gráfico de barras de dos categorías de resultados de primer contacto."""
    output_path = DIR_FIGURES / "prop_ci_01_sample_proportion.png"
    labels = ["Resolución en\nprimer contacto", "No primer\ncontacto"]
    values = [counts["successes"], counts["failures"]]
    colors = ["#EC2661", "#1A2E51"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Número de tickets")
    ax.set_title(f"Proporción muestral phat = {props['phat']:.4f} (n = {N})")
    ax.set_ylim(0, max(values) * 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 3,
            str(value),
            ha="center",
            fontweight="bold",
            fontsize=11,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    counts = first_contact_counts()
    props = sample_proportion(counts)
    figure_path = save_figure(counts, props)

    print("================================================================")
    print("LECCIÓN 29 - PASO 1: PROPORCIÓN MUESTRAL")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Tamaño de muestra n             : {counts['n']}")
    print(f"Resoluciones en primer contacto x: {counts['successes']}")
    print(f"No primer contacto              : {counts['failures']}")
    print(f"Proporción muestral phat        : {props['phat']:.6f}")
    print(f"Complemento qhat                : {props['qhat']:.6f}")
    print(f"n * phat                        : {props['n_phat']:.6f}")
    print(f"n * (1-phat)                    : {props['n_qhat']:.6f}")
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

