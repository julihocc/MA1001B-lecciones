"""
Lección 36 - Paso 1: Proporción muestral y condiciones normales
===============================================================
NUEVO EN ESTE PASO: sample_proportion(), normal_conditions() y save_figure().

La Receta
Un proceso de inspección de entrada completamente sintético afirma que la
proporción de banderas de retraso es 10 por ciento. Una muestra de n = 200
lotes registra x = 28 banderas de retraso. Antes de usar una prueba z, np0 y
n(1 - p0) deben superar 5.

Ejecútalo:
    uv run es/L36_Prueba_Hipotesis_Proporcion/src/prueba_proporcion_01_muestra_y_condiciones.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
N = 200
X_LATE = 28
P0 = 0.10
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) sample_proportion() -------------------------------------------
def sample_proportion(x: int = X_LATE, n: int = N) -> dict[str, float]:
    """Devuelve el conteo observado de banderas de retraso y la proporción muestral."""
    phat = x / n
    return {"n": float(n), "x": float(x), "phat": float(phat), "p0": P0}
# ------------------------------------------------------------------------------


# --- NUEVO (2) normal_conditions() -------------------------------------------
def normal_conditions(n: int = N, p0: float = P0) -> dict[str, float]:
    """Comprueba las condiciones np0 y n(1-p0) bajo H0."""
    np0 = n * p0
    nq0 = n * (1.0 - p0)
    return {
        "np0": float(np0),
        "nq0": float(nq0),
        "conditions_ok": float(np0 > 5.0 and nq0 > 5.0),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(summary: dict[str, float]) -> Path:
    """Compara la proporción hipotética con la proporción muestral."""
    output_path = DIR_FIGURES / "prueba_proporcion_01_muestra_y_condiciones.png"
    labels = ["Proporción H0 p0", "Proporción muestral phat"]
    values = [summary["p0"], summary["phat"]]
    colors = ["#1A2E51", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_ylabel("Proporción de retraso")
    ax.set_title("n = 200 lotes; x = 28 banderas de retraso")
    ax.set_ylim(0, 0.22)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.008,
            f"{value:.2f}",
            ha="center",
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    summary = sample_proportion()
    conditions = normal_conditions()
    figure_path = save_figure(summary)

    print("================================================================")
    print("LECCIÓN 36 - PASO 1: PROPORCIÓN MUESTRAL Y CONDICIONES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print(f"Tamaño de muestra n             : {int(summary['n'])}")
    print(f"Conteo de banderas de retraso x : {int(summary['x'])}")
    print(f"Proporción muestral phat        : {summary['phat']:.6f}")
    print(f"Proporción hipotética p0        : {summary['p0']:.6f}")
    print(f"np0 bajo H0                     : {conditions['np0']:.6f}")
    print(f"n(1-p0) bajo H0                 : {conditions['nq0']:.6f}")
    print(
        "Condiciones normales np0, nq0 > 5: "
        f"{'sí' if conditions['conditions_ok'] else 'no'}"
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

