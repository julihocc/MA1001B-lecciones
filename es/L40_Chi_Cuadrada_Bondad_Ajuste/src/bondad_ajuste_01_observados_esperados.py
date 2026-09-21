"""
Lección 40 - Paso 1: Conteos observados frente a participaciones hipotéticas
===========================================================================
NUEVO EN ESTE PASO: hypothesized_shares(), expected_counts() y save_figure().

La Receta
Un mostrador de soporte sintético afirma que los tickets llegan con la mezcla
40 por ciento teléfono, 30 por ciento chat, 20 por ciento correo y 10 por
ciento aplicación. Se cuenta una muestra de n = 200 tickets. Los conteos
esperados son n por las participaciones hipotéticas.

Ejecútalo:
    uv run es/L40_Chi_Cuadrada_Bondad_Ajuste/src/bondad_ajuste_01_observados_esperados.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 200
CATEGORIES = ("Teléfono", "Chat", "Correo", "App")
HYPOTHESIZED = np.array([0.40, 0.30, 0.20, 0.10])
OBSERVED = np.array([100, 50, 30, 20], dtype=float)
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) hypothesized_shares() -----------------------------------------
def hypothesized_shares() -> dict[str, np.ndarray | float]:
    """Devuelve las probabilidades de mezcla de tickets afirmadas."""
    return {
        "categories": np.array(CATEGORIES),
        "p": HYPOTHESIZED.copy(),
        "n": float(N),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) expected_counts() ---------------------------------------------
def expected_counts(n: int = N, p: np.ndarray = HYPOTHESIZED) -> dict[str, np.ndarray | float]:
    """Convierte las participaciones hipotéticas en conteos esperados E = n p."""
    expected = n * p
    return {
        "observed": OBSERVED.copy(),
        "expected": expected,
        "min_expected": float(np.min(expected)),
        "all_expected_ge_5": float(np.all(expected >= 5.0)),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(observed: np.ndarray, expected: np.ndarray) -> Path:
    """Compara conteos observados con conteos esperados bajo H0."""
    output_path = DIR_FIGURES / "bondad_ajuste_01_observados_esperados.png"
    x = np.arange(len(CATEGORIES))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - width / 2, observed, width, color="#EC2661", label="Observado")
    ax.bar(x + width / 2, expected, width, color="#1A2E51", label="Esperado bajo H0")
    ax.set_xticks(x, CATEGORIES)
    ax.set_ylabel("Conteo de tickets")
    ax.set_title("n = 200 tickets frente a la mezcla hipotética")
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    shares = hypothesized_shares()
    counts = expected_counts()
    figure_path = save_figure(counts["observed"], counts["expected"])

    print("================================================================")
    print("LECCIÓN 40 - PASO 1: OBSERVADOS FRENTE A ESPERADOS")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Tamaño de muestra n             : {int(shares['n'])}")
    print("Participaciones hipotéticas     : 0.40, 0.30, 0.20, 0.10")
    print("Conteos observados              : 100, 50, 30, 20")
    print(
        "Conteos esperados               : "
        + ", ".join(f"{value:.1f}" for value in counts["expected"])
    )
    print(f"Conteo esperado mínimo          : {counts['min_expected']:.6f}")
    print(
        "Todos los esperados >= 5        : "
        f"{'sí' if counts['all_expected_ge_5'] else 'no'}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

