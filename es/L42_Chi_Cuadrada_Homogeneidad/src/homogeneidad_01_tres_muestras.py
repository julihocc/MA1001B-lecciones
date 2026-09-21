"""
Lección 42 - Paso 1: Tres muestras independientes, mismas categorías
===================================================================
NUEVO EN ESTE PASO: site_counts(), category_shares() y save_figure().

La Receta
Tres almacenes sintéticos se muestrean de forma independiente: Norte n = 120,
Centro n = 100 y Sur n = 90. Cada ticket se clasifica como teléfono, chat o
correo. La homogeneidad pregunta si los tres sitios comparten la misma
mezcla. Los totales de fila los fijó el plan de muestreo.

Ejecútalo:
    uv run es/L42_Chi_Cuadrada_Homogeneidad/src/homogeneidad_01_tres_muestras.py
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SEED = 42
SITES = ("Norte", "Centro", "Sur")
CATEGORIES = ("Teléfono", "Chat", "Correo")
OBSERVED = np.array([[60, 40, 20], [35, 40, 25], [25, 30, 35]], dtype=float)
DIR_FIGURES = Path(__file__).resolve().parent.parent / "figuras"
DIR_FIGURES.mkdir(parents=True, exist_ok=True)


# --- NUEVO (1) site_counts() -------------------------------------------------
def site_counts() -> dict[str, np.ndarray | float]:
    """Devuelve los tres conteos sitio-por-canal muestreados de forma independiente."""
    return {
        "observed": OBSERVED.copy(),
        "row_totals": OBSERVED.sum(axis=1),
        "col_totals": OBSERVED.sum(axis=0),
        "n": float(OBSERVED.sum()),
    }
# ------------------------------------------------------------------------------


# --- NUEVO (2) category_shares() ---------------------------------------------
def category_shares(observed: np.ndarray) -> np.ndarray:
    """Convierte cada muestra independiente en participaciones dentro del sitio."""
    return observed / observed.sum(axis=1, keepdims=True)
# ------------------------------------------------------------------------------


# --- NUEVO (3) save_figure() -------------------------------------------------
def save_figure(shares: np.ndarray) -> Path:
    """Barras apiladas de las tres mezclas de canal muestreadas de forma independiente."""
    output_path = DIR_FIGURES / "homogeneidad_01_tres_muestras.png"
    colors = ["#1A2E51", "#5B8DEF", "#EC2661"]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    bottoms = np.zeros(len(SITES))
    for j, category in enumerate(CATEGORIES):
        ax.bar(
            SITES,
            shares[:, j],
            bottom=bottoms,
            color=colors[j],
            label=category,
            width=0.62,
        )
        bottoms = bottoms + shares[:, j]
    ax.set_ylabel("Participación dentro del sitio")
    ax.set_title("Tres muestras independientes de mezcla de tickets")
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)
    return output_path
# ------------------------------------------------------------------------------


def main() -> None:
    counts = site_counts()
    shares = category_shares(counts["observed"])
    figure_path = save_figure(shares)

    print("================================================================")
    print("LECCIÓN 42 - PASO 1: TRES MUESTRAS INDEPENDIENTES")
    print("================================================================")
    print("Aviso de datos sintéticos       : No se usan datos reales de empresa")
    print(f"Semilla aleatoria (reservada)   : {SEED}")
    print("Plan de muestreo                : tres muestras independientes de sitio")
    print(f"Norte n, conteos                : 120; 60, 40, 20")
    print(f"Centro n, conteos               : 100; 35, 40, 25")
    print(f"Sur n, conteos                  : 90; 25, 30, 35")
    print(f"n combinado                     : {int(counts['n'])}")
    print(
        "Participaciones Norte           : "
        + ", ".join(f"{value:.6f}" for value in shares[0])
    )
    print(
        "Participaciones Centro          : "
        + ", ".join(f"{value:.6f}" for value in shares[1])
    )
    print(
        "Participaciones Sur             : "
        + ", ".join(f"{value:.6f}" for value in shares[2])
    )
    print(f"Figura guardada en              : {figure_path}")
    print("================================================================")


if __name__ == "__main__":
    main()

